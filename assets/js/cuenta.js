// cuenta.js — cuentas y registro de partidas de Unlock C&A (Supabase, correo + contraseña).
// Común a toda la web (menús, juegos y «Mis partidas»). Si no hay conexión o falla Supabase, todo sigue funcionando en local:
// las partidas se guardan en este dispositivo y se sincronizan cuando haya sesión y red.
//
// La clave «publishable» es pública por diseño: la seguridad la da el RLS de supabase/unlock_partidas.sql.
// Es el mismo proyecto de Supabase que «Noches de Cine» (el de «La Arena» está pausado): las cuentas viven en ese proyecto.
// Si algún día se cambia de proyecto, las cuentas y las partidas no se mueven solas.

const SUPABASE_URL = 'https://tomwaoskswxfbwxsrkkl.supabase.co';
const SUPABASE_KEY = 'sb_publishable_GcN8b2gK-85Fqpeomul48g_DhUAPTZY';
const TABLA = 'unlock_partidas';
const K_HECHAS = 'ca-hechas';
const K_USUARIO = 'ca-usuario';

let clientePromesa = null;
const oyentes = new Set();

// ---------------------------------------------------------------- almacenamiento local
function leerLocal() {
  try { return JSON.parse(localStorage.getItem(K_HECHAS) || '[]'); } catch (e) { return []; }
}
function escribirLocal(lista) {
  try { localStorage.setItem(K_HECHAS, JSON.stringify(lista.slice(-300))); } catch (e) { /* sin almacenamiento */ }
}
export function usuarioRecordado() {
  try { return localStorage.getItem(K_USUARIO) || ''; } catch (e) { return ''; }
}
function recordarUsuario(email) {
  try { if (email) localStorage.setItem(K_USUARIO, email); else localStorage.removeItem(K_USUARIO); } catch (e) { /* nada */ }
}

// ---------------------------------------------------------------- cliente
function cargarLibreria() {
  return new Promise((resolve, reject) => {
    if (window.supabase && window.supabase.createClient) { resolve(window.supabase); return; }
    const s = document.createElement('script');
    s.src = new URL('./vendor/supabase.js', import.meta.url).href;
    s.onload = () => (window.supabase ? resolve(window.supabase) : reject(new Error('sin supabase')));
    s.onerror = () => reject(new Error('no se pudo cargar supabase'));
    document.head.appendChild(s);
  });
}

async function cliente() {
  if (!clientePromesa) {
    clientePromesa = cargarLibreria().then((sb) => {
      const c = sb.createClient(SUPABASE_URL, SUPABASE_KEY, { auth: { persistSession: true, autoRefreshToken: true, storageKey: 'ca-auth' } });
      c.auth.onAuthStateChange((evento, ses) => {
        recordarUsuario(ses && ses.user ? ses.user.email : '');
        oyentes.forEach((fn) => { try { fn(ses && ses.user ? ses.user : null); } catch (e) { /* nada */ } });
        if (ses && ses.user) sincronizar().catch(() => {});
      });
      return c;
    }).catch((e) => { clientePromesa = null; throw e; });
  }
  return clientePromesa;
}

/** Permite engancharse a los cambios de sesión (login / logout). */
export function alCambiarSesion(fn) { oyentes.add(fn); return () => oyentes.delete(fn); }

function traducir(error) {
  const m = String((error && error.message) || error || '');
  if (/Invalid login credentials/i.test(m)) return 'Correo o contraseña incorrectos.';
  if (/Email not confirmed/i.test(m)) return 'Falta confirmar el correo: abre el mensaje que te enviamos y pulsa el enlace.';
  if (/already registered|already been registered/i.test(m)) return 'Ese correo ya tiene cuenta: prueba a entrar.';
  if (/Password should be at least/i.test(m)) return 'La contraseña es demasiado corta (mínimo 6 caracteres).';
  if (/rate limit|too many/i.test(m)) return 'Demasiados intentos seguidos: espera un minuto y vuelve a probar.';
  if (/Failed to fetch|NetworkError|network/i.test(m)) return 'No hay conexión con el servidor. Tus partidas se guardan en este dispositivo y se subirán más tarde.';
  if (/valid email|Unable to validate email/i.test(m)) return 'Ese correo no parece válido.';
  return 'No se pudo completar la operación: ' + m;
}

// ---------------------------------------------------------------- sesión
export async function sesion() {
  try {
    const c = await cliente();
    const { data } = await c.auth.getSession();
    const u = data && data.session ? data.session.user : null;
    recordarUsuario(u ? u.email : '');
    return u;
  } catch (e) { return null; }
}

export async function entrar(email, clave) {
  try {
    const c = await cliente();
    const { data, error } = await c.auth.signInWithPassword({ email: email.trim(), password: clave });
    if (error) return { ok: false, mensaje: traducir(error) };
    sincronizar().catch(() => {});
    return { ok: true, usuario: data.user };
  } catch (e) { return { ok: false, mensaje: traducir(e) }; }
}

export async function registrar(email, clave) {
  try {
    const c = await cliente();
    const { data, error } = await c.auth.signUp({ email: email.trim(), password: clave });
    if (error) return { ok: false, mensaje: traducir(error) };
    if (!data.session) return { ok: true, pendiente: true, mensaje: 'Cuenta creada. Te hemos enviado un correo: confírmalo y luego entra con tu contraseña.' };
    sincronizar().catch(() => {});
    return { ok: true, usuario: data.user };
  } catch (e) { return { ok: false, mensaje: traducir(e) }; }
}

export async function salir() {
  try { const c = await cliente(); await c.auth.signOut(); } catch (e) { /* nada */ }
  recordarUsuario('');
}

// ---------------------------------------------------------------- partidas
function idLocal() { return Date.now().toString(36) + Math.random().toString(36).slice(2, 8); }

/** Guarda una partida terminada: siempre en local, y en la nube si hay sesión. Devuelve { nube, local, mensaje }. */
export async function guardarPartida({ juego, tiempo_seg, pistas = 0, cartas = 0, informe = '' }) {
  const reg = { cliente_id: idLocal(), juego, tiempo_seg: Math.max(0, Math.round(tiempo_seg)), pistas, cartas, informe, fin: new Date().toISOString(), sync: false };
  const lista = leerLocal();
  lista.push(reg);
  escribirLocal(lista);
  const u = await sesion();
  if (!u) return { nube: false, local: true, reg, mensaje: 'Partida guardada en este dispositivo. Inicia sesión para guardarla en tu cuenta.' };
  const r = await sincronizar();
  return { nube: r.ok, local: true, reg, mensaje: r.ok ? 'Partida guardada en tu cuenta.' : r.mensaje };
}

/** Sube a la nube las partidas locales que aún no estén. */
export async function sincronizar() {
  const lista = leerLocal();
  const pendientes = lista.filter((p) => !p.sync);
  if (!pendientes.length) return { ok: true, subidas: 0 };
  try {
    const c = await cliente();
    const { data } = await c.auth.getSession();
    if (!data || !data.session) return { ok: false, mensaje: 'Sin sesión.' };
    const filas = pendientes.map((p) => ({ cliente_id: p.cliente_id, juego: p.juego, tiempo_seg: p.tiempo_seg, pistas: p.pistas, cartas: p.cartas, completada: true, informe: p.informe || null, fin: p.fin }));
    const { error } = await c.from(TABLA).upsert(filas, { onConflict: 'user_id,cliente_id', ignoreDuplicates: true });
    if (error) {
      if (/relation .* does not exist|schema cache|Could not find the table/i.test(error.message || '')) return { ok: false, mensaje: 'La cuenta funciona, pero falta crear la tabla de partidas en Supabase (supabase/unlock_partidas.sql). La partida queda en este dispositivo.' };
      return { ok: false, mensaje: traducir(error) };
    }
    pendientes.forEach((p) => { p.sync = true; });
    escribirLocal(lista);
    return { ok: true, subidas: pendientes.length };
  } catch (e) { return { ok: false, mensaje: traducir(e) }; }
}

/** Todas las partidas conocidas: las de la nube (si hay sesión) y las locales aún sin subir. */
export async function misPartidas() {
  const locales = leerLocal();
  const u = await sesion();
  let nube = [];
  let aviso = '';
  if (u) {
    try {
      const c = await cliente();
      const { data, error } = await c.from(TABLA).select('cliente_id,juego,tiempo_seg,pistas,cartas,fin').order('fin', { ascending: false }).limit(500);
      if (error) aviso = /does not exist|schema cache|Could not find the table/i.test(error.message || '') ? 'Falta crear la tabla de partidas en Supabase (supabase/unlock_partidas.sql).' : traducir(error);
      else nube = data || [];
    } catch (e) { aviso = traducir(e); }
  }
  const ids = new Set(nube.map((p) => p.cliente_id));
  const extra = locales.filter((p) => !ids.has(p.cliente_id) && (!u || !p.sync || aviso)).map((p) => ({ ...p, pendiente: true }));
  const todas = nube.concat(extra).sort((a, b) => String(b.fin).localeCompare(String(a.fin)));
  return { usuario: u, partidas: todas, aviso };
}

/** { juego: { mejor, veces, ultima } } para pintar marcas en los menús. */
export function resumenPorJuego(partidas) {
  const r = {};
  partidas.forEach((p) => {
    const x = r[p.juego] || (r[p.juego] = { mejor: Infinity, veces: 0, ultima: '' });
    x.veces++;
    x.mejor = Math.min(x.mejor, p.tiempo_seg);
    if (String(p.fin) > x.ultima) x.ultima = String(p.fin);
  });
  return r;
}

/** Resumen solo con lo guardado en este dispositivo (no requiere red ni sesión). */
export function resumenLocal() { return resumenPorJuego(leerLocal()); }

// al volver la conexión, sube las partidas que quedaron guardadas en el dispositivo
if (typeof window !== 'undefined') window.addEventListener('online', () => { sincronizar().catch(() => {}); });

export function formatoTiempo(seg) {
  const s = Math.max(0, Math.round(seg));
  const h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), x = s % 60;
  return (h ? h + ':' + String(m).padStart(2, '0') : String(m)) + ':' + String(x).padStart(2, '0');
}
