// admin.js — panel de pedidos de la tienda: ver pedidos y fotos, cambiar el estado y mandar a producción («Desarrollarlo»).
// Solo funciona con una cuenta que esté en public.tienda_admins (supabase/tienda_admin.sql); al resto el RLS no le deja ver nada.
// El botón «Desarrollarlo» deja el pedido en estado «desarrollar»; lo recoge herramientas/tienda/produccion.py en el PC.
(() => {
  'use strict';

  const SUPABASE_URL = 'https://tomwaoskswxfbwxsrkkl.supabase.co';
  const SUPABASE_KEY = 'sb_publishable_GcN8b2gK-85Fqpeomul48g_DhUAPTZY';
  const REFRESCO_MS = 30000;

  const AVENTURAS = { egipto: 'Egipto', marte: 'Marte', florencia: 'Florencia', dinosaurios: 'Dinosaurios', cuento: 'Érase una vez', trono: 'Hielo y Fuego' };
  const ESTADOS = {
    nuevo: 'Nuevo', pagado: 'Pagado', desarrollar: 'En cola', en_produccion: 'En producción',
    listo: 'Listo', entregado: 'Entregado', cancelado: 'Cancelado',
  };
  const FILTROS = [
    ['activos', 'Activos', (p) => !['entregado', 'cancelado'].includes(p.estado)],
    ['nuevo', 'Nuevos', (p) => p.estado === 'nuevo'],
    ['produccion', 'En producción', (p) => ['desarrollar', 'en_produccion'].includes(p.estado)],
    ['listo', 'Listos', (p) => p.estado === 'listo'],
    ['entregado', 'Entregados', (p) => p.estado === 'entregado'],
    ['todos', 'Todos', () => true],
  ];

  const $ = (s, el = document) => el.querySelector(s);
  const esc = (t) => String(t ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const codigo = (p) => p.id.slice(0, 8).toUpperCase();
  const fecha = (t) => (t ? new Date(t).toLocaleString('es-ES', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' }) : '');

  let sb;
  let pedidos = [];
  let fotos = {};            // ruta → URL firmada
  let filtro = 'activos';
  let temporizador;

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

  // ---------- sesión ----------
  async function arrancar() {
    const { data } = await cliente().auth.getSession();
    cliente().auth.onAuthStateChange(async (evento) => {
      if (evento === 'PASSWORD_RECOVERY') {
        const nueva = prompt('Escribe tu nueva contraseña (mínimo 6 caracteres):');
        if (nueva) {
          const { error } = await cliente().auth.updateUser({ password: nueva });
          alert(error ? `No se pudo cambiar: ${error.message}` : 'Contraseña cambiada.');
        }
      }
    });
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

  $('#olvido').addEventListener('click', async () => {
    const email = $('#form-login').elements.email.value.trim();
    if (!email) { $('#error-login').textContent = 'Escribe primero tu correo.'; return; }
    const { error } = await cliente().auth.resetPasswordForEmail(email, { redirectTo: location.href.split('#')[0] });
    $('#error-login').textContent = error ? error.message : 'Te hemos mandado un correo para cambiar la contraseña.';
  });

  $('#salir').addEventListener('click', async () => {
    clearInterval(temporizador);
    await cliente().auth.signOut();
    mostrar('login');
  });

  async function entrar() {
    const { data: admin, error } = await cliente().rpc('es_admin_tienda');
    if (error || !admin) {
      await cliente().auth.signOut();
      mostrar('login');
      $('#error-login').textContent = error ? `No se pudo comprobar la cuenta: ${error.message}` : 'Esta cuenta no es administradora de la tienda.';
      return;
    }
    mostrar('panel');
    await cargar();
    clearInterval(temporizador);
    temporizador = setInterval(() => { if (!document.hidden) cargar(true); }, REFRESCO_MS);
  }

  // ---------- datos ----------
  async function cargar(silencioso) {
    if (!silencioso) $('#lista').classList.add('cargando-lista');
    const { data, error } = await cliente().from('tienda_pedidos').select('*').order('creado', { ascending: false });
    $('#lista').classList.remove('cargando-lista');
    if (error) { $('#error-panel').textContent = `No se pudieron cargar los pedidos: ${error.message}`; return; }
    $('#error-panel').textContent = '';
    pedidos = data;
    await firmarFotos();
    pintar();
    if (!silencioso && location.hash.length > 1) {
      const el = document.getElementById(`p-${location.hash.slice(1)}`);
      if (el) { el.classList.add('resaltado'); el.scrollIntoView({ block: 'center' }); }
    }
  }

  async function firmarFotos() {
    const rutas = [];
    for (const p of pedidos) {
      for (const pr of p.protagonistas || []) for (const r of pr.fotos || []) if (!fotos[r]) rutas.push(r);
      if (p.estado !== 'nuevo' && p.estado !== 'pagado' && p.estado !== 'cancelado') rutas.push(`${p.id}/hoja.jpg`);
    }
    if (!rutas.length) return;
    const { data } = await cliente().storage.from('tienda-fotos').createSignedUrls(rutas, 3600);
    for (const x of data || []) if (x.signedUrl && !x.error) fotos[x.path] = x.signedUrl;
  }

  // ---------- pintar ----------
  function pintar() {
    $('#filtros').innerHTML = FILTROS.map(([id, txt, f]) => {
      const n = pedidos.filter(f).length;
      return `<button type="button" role="tab" aria-selected="${id === filtro}" data-filtro="${id}">${txt} <span>${n}</span></button>`;
    }).join('');
    const visibles = pedidos.filter(FILTROS.find(([id]) => id === filtro)[2]);
    $('#lista').innerHTML = visibles.length ? visibles.map(tarjeta).join('') : '<p class="vacio">No hay pedidos aquí.</p>';
  }

  function tarjeta(p) {
    const protas = (p.protagonistas || []).map((pr) => `
      <div class="prota-admin">
        <div class="fotos-admin">${(pr.fotos || []).map((r) => fotos[r]
          ? `<a href="${esc(fotos[r])}" target="_blank" rel="noopener"><img src="${esc(fotos[r])}" alt="Foto de ${esc(pr.nombre)}"></a>`
          : '<span class="sin-foto">foto</span>').join('')}</div>
        <div><strong>${esc(pr.nombre)}</strong>${pr.genero ? ` · ${esc(pr.genero)}` : ''}${pr.edad ? ` · ${esc(pr.edad)} años` : ''}
          ${pr.sobre ? `<br><small>${esc(pr.sobre)}</small>` : ''}</div>
      </div>`).join('');
    const hoja = fotos[`${p.id}/hoja.jpg`];
    const enMarcha = ['desarrollar', 'en_produccion'].includes(p.estado);
    const detalles = [
      ['Formato', `${p.formato === 'impreso' ? 'Impreso' : 'Digital'} · ${p.precio} €`],
      ['Ocasión', p.ocasion], ['Para el', p.fecha_deseada && new Date(p.fecha_deseada).toLocaleDateString('es-ES')],
      ['Dedicatoria', p.dedicatoria], ['Dirección', p.direccion], ['Notas', p.notas],
    ].filter(([, v]) => v).map(([k, v]) => `<dt>${k}</dt><dd>${esc(v)}</dd>`).join('');

    return `
    <article class="pedido-admin estado-${p.estado}" id="p-${p.id}" data-id="${p.id}">
      <header>
        <div>
          <span class="codigo">${codigo(p)}</span>
          <span class="chip chip-${p.estado}">${ESTADOS[p.estado] || esc(p.estado)}</span>
          <span class="cuando">${fecha(p.creado)}</span>
        </div>
        <select data-accion="estado" aria-label="Estado del pedido">
          ${Object.entries(ESTADOS).map(([k, v]) => `<option value="${k}" ${k === p.estado ? 'selected' : ''}>${v}</option>`).join('')}
        </select>
      </header>
      <div class="cuerpo">
        <div class="col">
          <p class="cliente"><strong>${esc(p.nombre)}</strong> · <a href="mailto:${esc(p.email)}">${esc(p.email)}</a>${p.telefono ? ` · <a href="tel:${esc(p.telefono)}">${esc(p.telefono)}</a>` : ''}</p>
          <p class="aventuras-admin">${(p.aventuras || []).map((a) => `<span>${esc(AVENTURAS[a] || a)}</span>`).join('')}</p>
          <dl>${detalles}</dl>
        </div>
        <div class="col">${protas}${hoja ? `<div class="hoja"><a href="${esc(hoja)}" target="_blank" rel="noopener"><img src="${esc(hoja)}" alt="Hoja de personajes"></a><small>Hoja de personajes (ilustración de prueba)</small></div>` : ''}</div>
      </div>
      ${p.progreso ? `<p class="progreso ${enMarcha ? 'vivo' : ''}">${esc(p.progreso)}</p>` : ''}
      <footer>
        ${enMarcha
          ? '<button class="btn btn-linea btn-sm" type="button" disabled>Desarrollándose…</button>'
          : `<button class="btn btn-oro btn-sm" type="button" data-accion="desarrollar">${p.estado === 'listo' || p.estado === 'entregado' ? 'Volver a desarrollar' : 'Desarrollarlo'}</button>`}
        ${p.entrega_url ? `<a class="btn btn-linea btn-sm" href="${esc(p.entrega_url)}" target="_blank" rel="noopener">Ver el pack</a>
          <button class="btn btn-linea btn-sm" type="button" data-accion="mensaje">Copiar mensaje para el cliente</button>
          <a class="btn btn-oro btn-sm" href="${esc(enlaceAcceso(p))}">Dar acceso en la app</a>` : ''}
        ${p.estado === 'listo' ? '<button class="btn btn-linea btn-sm" type="button" data-accion="entregado">Marcar entregado</button>' : ''}
        <button class="btn btn-peligro btn-sm" type="button" data-accion="borrar">Borrar</button>
      </footer>
    </article>`;
  }

  // abre tienda/accesos.html ya relleno con el correo, los protagonistas, la web del pack y sus aventuras
  function enlaceAcceso(p) {
    const q = new URLSearchParams({
      email: p.email, quienes: (p.protagonistas || []).map((x) => x.nombre).join(' y '),
      pack: p.entrega_url || '', juegos: (p.aventuras || []).join(','), pedido: p.id,
    });
    return `accesos.html?${q}`;
  }

  // ---------- acciones ----------
  async function actualizar(id, cambios) {
    const { error } = await cliente().from('tienda_pedidos').update(cambios).eq('id', id);
    if (error) { alert(`No se pudo guardar: ${error.message}`); return false; }
    await cargar(true);
    return true;
  }

  $('#filtros').addEventListener('click', (e) => {
    const b = e.target.closest('[data-filtro]');
    if (b) { filtro = b.dataset.filtro; pintar(); }
  });
  $('#recargar').addEventListener('click', () => cargar());

  $('#lista').addEventListener('change', (e) => {
    if (e.target.dataset.accion !== 'estado') return;
    const id = e.target.closest('[data-id]').dataset.id;
    actualizar(id, { estado: e.target.value });
  });

  $('#lista').addEventListener('click', async (e) => {
    const b = e.target.closest('button[data-accion]');
    if (!b) return;
    const id = b.closest('[data-id]').dataset.id;
    const p = pedidos.find((x) => x.id === id);
    const accion = b.dataset.accion;

    if (accion === 'desarrollar') {
      const nombres = (p.protagonistas || []).map((x) => x.nombre).join(' y ');
      if (!confirm(`¿Desarrollar el pack ${codigo(p)} con ${nombres}?\n\nTu PC creará la hoja de personajes y las ilustraciones con ChatGPT y publicará el pack. Puede tardar uno o dos días por el cupo de imágenes.`)) return;
      b.disabled = true;
      await actualizar(id, { estado: 'desarrollar', progreso: 'En cola: tu PC lo empezará en unos minutos (tiene que estar encendido).' });
    } else if (accion === 'entregado') {
      await actualizar(id, { estado: 'entregado' });
    } else if (accion === 'mensaje') {
      const nombres = (p.protagonistas || []).map((x) => x.nombre).join(' y ');
      const texto = `¡Hola, ${p.nombre}!\n\nVuestro pack de escape rooms ya está listo. ${nombres} sois los protagonistas de estas cuatro aventuras:\n\n${p.entrega_url}\n\nAbrid el enlace en el móvil para jugar. También las tenéis en la app (https://albercha17.github.io/Unlock-CA/): entrad con este correo (${p.email}) y aparecerán con vuestras portadas. En cada aventura tenéis también las cartas para imprimir.\n\n¡Que lo disfrutéis!\nCronoportal`;
      try { await navigator.clipboard.writeText(texto); b.textContent = '✓ Copiado'; }
      catch { prompt('Copia este mensaje:', texto); }
    } else if (accion === 'borrar') {
      if (!confirm(`¿Borrar el pedido ${codigo(p)} de ${p.nombre} y sus fotos? No se puede deshacer.`)) return;
      const { data: lista } = await cliente().storage.from('tienda-fotos').list(id);
      if (lista && lista.length) await cliente().storage.from('tienda-fotos').remove(lista.map((f) => `${id}/${f.name}`));
      const { error } = await cliente().from('tienda_pedidos').delete().eq('id', id);
      if (error) alert(`No se pudo borrar: ${error.message}`);
      await cargar(true);
    }
  });

  window.addEventListener('DOMContentLoaded', () => {
    if (!window.supabase) { $('#cargando').textContent = 'No se pudo cargar la conexión. Recarga la página.'; return; }
    arrancar();
  });
})();
