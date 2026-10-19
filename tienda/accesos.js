// accesos.js — panel de accesos (tienda/accesos.html): qué juegos ve cada cuenta en la app (tabla unlock_accesos).
// Solo funciona con una cuenta de public.tienda_admins (el RLS no deja al resto ni leer ni escribir).
// Se puede abrir ya relleno desde un pedido: accesos.html?email=…&quienes=…&pack=…&juegos=egipto,marte&pedido=<id>
(() => {
  'use strict';

  const SUPABASE_URL = 'https://tomwaoskswxfbwxsrkkl.supabase.co';
  const SUPABASE_KEY = 'sb_publishable_GcN8b2gK-85Fqpeomul48g_DhUAPTZY';
  const TABLA = 'unlock_accesos';

  const $ = (s, el = document) => el.querySelector(s);
  const esc = (t) => String(t ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const fecha = (t) => (t ? new Date(t).toLocaleDateString('es-ES', { day: '2-digit', month: 'short', year: 'numeric' }) : '');

  let sb;
  let catalogo = [];
  let accesos = [];

  function cliente() {
    if (!sb) sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY, { auth: { persistSession: true, autoRefreshToken: true, storageKey: 'ca-tienda-admin' } });
    return sb;
  }

  function mostrar(vista) {
    $('#cargando').hidden = true;
    $('#login').hidden = vista !== 'login';
    $('#panel').hidden = vista !== 'panel';
    $('#salir').hidden = vista !== 'panel';
  }

  const nombreJuego = (id) => (catalogo.find((j) => j.id === id) || {}).nombre || id;
  const esAventura = (id) => ((catalogo.find((j) => j.id === id) || {}).ruta || '').startsWith('juegos/aventuras-ca/');

  // ---------- sesión ----------
  async function arrancar() {
    try { catalogo = await (await fetch('../juegos/catalogo.json')).json(); } catch { catalogo = []; }
    pintarJuegos();
    rellenarDesdeEnlace();
    const { data } = await cliente().auth.getSession();
    if (data.session) await entrar(); else mostrar('login');
  }

  $('#form-login').addEventListener('submit', async (e) => {
    e.preventDefault();
    const f = e.target.elements;
    $('#error-login').textContent = '';
    const { error } = await cliente().auth.signInWithPassword({ email: f.email.value.trim(), password: f.clave.value });
    if (error) { $('#error-login').textContent = /invalid/i.test(error.message) ? 'Correo o contraseña incorrectos.' : error.message; return; }
    await entrar();
  });

  $('#salir').addEventListener('click', async () => { await cliente().auth.signOut(); mostrar('login'); });

  async function entrar() {
    const { data: admin, error } = await cliente().rpc('es_admin_tienda');
    if (error || !admin) {
      await cliente().auth.signOut();
      mostrar('login');
      $('#error-login').textContent = error ? `No se pudo comprobar la cuenta: ${error.message}` : 'Esta cuenta no es administradora.';
      return;
    }
    mostrar('panel');
    await cargar();
  }

  // ---------- datos ----------
  async function cargar() {
    const { data, error } = await cliente().from(TABLA).select('*').order('creado', { ascending: false });
    if (error) {
      $('#error-panel').textContent = /does not exist|schema cache|Could not find/i.test(error.message)
        ? 'Falta crear la tabla de accesos: ejecuta supabase/unlock_accesos.sql en el SQL Editor de Supabase.'
        : `No se pudieron cargar los accesos: ${error.message}`;
      return;
    }
    $('#error-panel').textContent = '';
    accesos = data || [];
    pintarLista();
  }

  // ---------- formulario ----------
  function pintarJuegos() {
    $('#juegos').innerHTML = catalogo.map((j) => `
      <label class="juego-dar"><input type="checkbox" name="juego" value="${esc(j.id)}">
        <img src="../${esc(j.ruta)}img/P.jpg" alt="" loading="lazy"><span>${esc(j.nombre)}</span></label>`).join('');
    contar();
  }

  function contar() {
    const n = document.querySelectorAll('#juegos input:checked').length;
    $('#n-elegidos').textContent = n ? `· ${n} elegido${n > 1 ? 's' : ''}` : '';
  }
  $('#juegos').addEventListener('change', contar);

  function rellenarDesdeEnlace() {
    const q = new URLSearchParams(location.search);
    const f = $('#form-dar').elements;
    if (q.get('email')) f.email.value = q.get('email');
    if (q.get('quienes')) f.quienes.value = q.get('quienes');
    if (q.get('pack')) f.pack.value = q.get('pack');
    if (q.get('pedido')) f.pedido.value = q.get('pedido');
    const juegos = (q.get('juegos') || '').split(',').filter(Boolean);
    document.querySelectorAll('#juegos input').forEach((i) => { i.checked = juegos.includes(i.value); });
    contar();
  }

  $('#form-dar').addEventListener('submit', async (e) => {
    e.preventDefault();
    const f = e.target.elements;
    const err = $('#error-dar');
    const email = f.email.value.trim().toLowerCase();
    const quienes = f.quienes.value.trim();
    const pack = f.pack.value.trim().replace(/\/+$/, '').replace(/\/(juegos\/aventuras-ca\/?)?(index\.html)?$/, '');
    const juegos = [...document.querySelectorAll('#juegos input:checked')].map((i) => i.value);
    err.textContent = '';
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) { err.textContent = 'Escribe un correo válido.'; return; }
    if (pack && !/^https:\/\/\S+$/.test(pack)) { err.textContent = 'La web del pack tiene que empezar por https://'; return; }
    if (!juegos.length) { err.textContent = 'Elige al menos un juego.'; return; }
    const sueltos = pack ? juegos.filter((j) => !esAventura(j)) : [];
    const filas = juegos.map((j) => {
      const enPack = pack && esAventura(j);
      const base = enPack ? `${pack}/juegos/aventuras-ca/${j}/` : '';
      return { email, juego: j, quienes, url: enPack ? `${base}index.html` : '', portada: enPack ? `${base}img/P.jpg` : '', pedido_id: f.pedido.value || null };
    });
    const b = e.target.querySelector('button[type="submit"]');
    b.disabled = true;
    const { error } = await cliente().from(TABLA).upsert(filas, { onConflict: 'email,juego,url' });
    b.disabled = false;
    if (error) { err.textContent = `No se pudo guardar: ${error.message}`; return; }
    err.textContent = `✓ ${email} ya tiene ${juegos.length} juego${juegos.length > 1 ? 's' : ''} más.` +
      (sueltos.length ? ` (${sueltos.map(nombreJuego).join(', ')} no va en el pack: se abre el normal.)` : '');
    document.querySelectorAll('#juegos input').forEach((i) => { i.checked = false; });
    contar();
    history.replaceState(null, '', location.pathname);
    await cargar();
  });

  // ---------- lista ----------
  function pintarLista() {
    const filtro = $('#buscar').value.trim().toLowerCase();
    const grupos = new Map();
    for (const a of accesos) {
      if (filtro && !`${a.email} ${a.quienes}`.toLowerCase().includes(filtro)) continue;
      if (!grupos.has(a.email)) grupos.set(a.email, []);
      grupos.get(a.email).push(a);
    }
    if (!grupos.size) { $('#lista').innerHTML = `<p class="vacio">${accesos.length ? 'Nadie coincide con la búsqueda.' : 'Todavía no has dado acceso a nadie.'}</p>`; return; }
    $('#lista').innerHTML = [...grupos].map(([email, lista]) => {
      const quienes = [...new Set(lista.map((a) => a.quienes).filter(Boolean))].join(', ');
      return `
      <article class="pedido-admin" data-email="${esc(email)}">
        <header>
          <div><span class="codigo">${esc(email)}</span>${quienes ? `<span class="cuando">${esc(quienes)}</span>` : ''}</div>
          <div class="dar-botones">
            <button class="btn btn-linea btn-sm" type="button" data-accion="ver">Ver la app como esta cuenta</button>
            <button class="btn btn-linea btn-sm" type="button" data-accion="mas">Darle más juegos</button>
          </div>
        </header>
        <div class="accesos-lista">${lista.map((a) => `
          <div class="acceso">
            <img src="${esc(a.portada || `../${(catalogo.find((j) => j.id === a.juego) || {}).ruta || ''}img/P.jpg`)}" alt="" loading="lazy">
            <div><strong>${esc(nombreJuego(a.juego))}</strong>
              <small>${a.url ? `<a href="${esc(a.url)}" target="_blank" rel="noopener">Personalizado</a>` : 'Normal'} · desde el ${fecha(a.creado)}</small></div>
            <button class="btn btn-peligro btn-sm" type="button" data-accion="quitar" data-id="${esc(a.id)}">Quitar</button>
          </div>`).join('')}
        </div>
      </article>`;
    }).join('');
  }
  $('#buscar').addEventListener('input', pintarLista);

  $('#lista').addEventListener('click', async (e) => {
    const b = e.target.closest('button[data-accion]');
    if (!b) return;
    const email = b.closest('[data-email]').dataset.email;
    if (b.dataset.accion === 'quitar') {
      const a = accesos.find((x) => x.id === b.dataset.id);
      if (!confirm(`¿Quitar «${nombreJuego(a.juego)}» a ${email}? Dejará de verlo en la app.`)) return;
      const { error } = await cliente().from(TABLA).delete().eq('id', a.id);
      if (error) alert(`No se pudo quitar: ${error.message}`);
      await cargar();
    } else if (b.dataset.accion === 'ver') {
      window.open(`../index.html?ver-como=${encodeURIComponent(email)}`, '_blank');
    } else if (b.dataset.accion === 'mas') {
      const f = $('#form-dar').elements;
      const una = accesos.find((x) => x.email === email && x.url) || accesos.find((x) => x.email === email);
      f.email.value = email;
      f.quienes.value = una ? una.quienes : '';
      f.pack.value = '';
      f.pedido.value = '';
      $('#form-dar').scrollIntoView({ behavior: 'smooth' });
      f.pack.focus();
    }
  });

  window.addEventListener('DOMContentLoaded', () => {
    if (!window.supabase) { $('#cargando').textContent = 'No se pudo cargar la conexión. Recarga la página.'; return; }
    arrancar();
  });
})();
