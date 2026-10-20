// accesos.js — qué juegos ve cada cuenta (tabla unlock_accesos, ver supabase/unlock_accesos.sql).
// Los administradores (tienda_admins) lo ven todo, con Cristina y Alberto. El resto, solo los juegos que se le han dado,
// con su portada personalizada y el enlace a su pack. Se guarda una copia en el dispositivo para que funcione sin conexión.
// Un administrador puede «ver como» otro correo (tienda/accesos.html) para comprobar lo que verá el cliente.
import { sesion, clienteSupabase } from './cuenta.js';

const K_CACHE = 'ca-accesos';
const K_VER_COMO = 'ca-ver-como';

// «ver como» llega en la dirección (?ver-como=correo) desde tienda/accesos.html y dura lo que la pestaña
try {
  const q = new URLSearchParams(location.search).get('ver-como');
  if (q) { sessionStorage.setItem(K_VER_COMO, q.trim().toLowerCase()); history.replaceState(null, '', location.pathname); }
} catch (e) { /* nada */ }

function leerCache() { try { return JSON.parse(localStorage.getItem(K_CACHE) || 'null'); } catch (e) { return null; } }
function escribirCache(d) { try { localStorage.setItem(K_CACHE, JSON.stringify(d)); } catch (e) { /* nada */ } }
export function verComo() { try { return sessionStorage.getItem(K_VER_COMO) || ''; } catch (e) { return ''; } }
export function dejarDeVerComo() { try { sessionStorage.removeItem(K_VER_COMO); } catch (e) { /* nada */ } }

function vista(d) {
  // con «ver como», el administrador ve exactamente lo que verá ese cliente
  if (d.admin && d.verComo) return { ...d, admin: false, email: d.verComo, lista: d.listaVerComo || [] };
  return d;
}

/** Lo último conocido para el correo recordado (sin red). null si no hay nada guardado de esa cuenta. */
export function accesosGuardados(email) {
  const c = leerCache();
  if (!c || !email || c.cuenta !== email) return null;
  return vista({ ...c, verComo: verComo() });
}

/** { usuario, admin, email, lista: [{juego, url, portada, quienes}], verComo, sinRed } */
export async function misAccesos() {
  const u = await sesion();
  if (!u) return { usuario: null, admin: false, email: '', lista: [] };
  const como = verComo();
  try {
    const c = await clienteSupabase();
    const adm = await c.rpc('es_admin_tienda');
    if (adm.error) throw adm.error;
    const admin = adm.data === true;
    const sel = 'juego,url,portada,quienes,email,creado';
    let lista = [];
    let listaVerComo = [];
    if (!admin) {
      const r = await c.from('unlock_accesos').select(sel).order('creado');
      if (r.error) throw r.error;
      lista = r.data || [];
    } else if (como) {
      const r = await c.from('unlock_accesos').select(sel).eq('email', como).order('creado');
      if (r.error) throw r.error;
      listaVerComo = r.data || [];
    }
    const d = { cuenta: u.email, admin, email: u.email, lista, listaVerComo, t: Date.now() };
    escribirCache(d);
    return vista({ ...d, usuario: u, verComo: como });
  } catch (e) {
    const g = accesosGuardados(u.email);
    if (g) return { ...g, usuario: u, sinRed: true };
    const falta = /does not exist|schema cache|Could not find/i.test(String((e && e.message) || ''));
    return { usuario: u, admin: false, email: u.email, lista: [], sinRed: !falta, faltaTabla: falta };
  }
}
