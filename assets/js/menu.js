// menu.js — decora los menús: dificultad, duración y nº de cartas de cada juego (antes de elegir), marcas de partidas
// ya hechas con el mejor tiempo, y el botón de cuenta. Lee juegos/catalogo.json (lo genera herramientas/generar_catalogo.py).
// También decide qué juegos se ven (accesos.js): el administrador ve todo; cada cliente, solo los juegos que se le han dado,
// con su portada personalizada; sin sesión, una bienvenida para entrar.
import { resumenLocal, misPartidas, resumenPorJuego, formatoTiempo, usuarioRecordado, alCambiarSesion } from './cuenta.js';
import { montarCuenta, abrirLogin } from './cuenta-ui.js';
import { misAccesos, accesosGuardados, dejarDeVerComo } from './accesos.js';

const NIVELES = ['', 'Muy fácil', 'Fácil', 'Media', 'Difícil', 'Muy difícil'];
const raiz = document.body.dataset.raiz || '';
const esc = (t) => String(t ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

function fila(j) {
  const n = Math.max(1, Math.min(5, j.dificultad || 3));
  const d = document.createElement('div');
  d.className = 'dif-fila';
  d.setAttribute('aria-label', 'Dificultad ' + NIVELES[n].toLowerCase() + ', ' + n + ' de 5. ' + j.minutos + ' minutos, ' + j.cartas + ' cartas.');
  d.innerHTML = '<span class="dif-t">Dificultad</span><span class="puntos" aria-hidden="true">' +
    [1, 2, 3, 4, 5].map((k) => '<i class="' + (k <= n ? 'on' : '') + '"></i>').join('') + '</span><b class="dif-n n' + n + '">' + NIVELES[n] + '</b>' +
    '<span class="dif-meta">' + j.minutos + ' min · ' + j.cartas + ' cartas</span>';
  return d;
}

function filaHub(js) {
  const ns = js.map((j) => j.dificultad);
  const min = Math.min(...ns), max = Math.max(...ns);
  const d = document.createElement('div');
  d.className = 'dif-fila';
  d.setAttribute('aria-label', js.length + ' aventuras, de dificultad ' + NIVELES[min].toLowerCase() + ' a ' + NIVELES[max].toLowerCase());
  d.innerHTML = '<span class="dif-t">' + js.length + ' aventuras</span><span class="puntos" aria-hidden="true">' +
    [1, 2, 3, 4, 5].map((k) => '<i class="' + (k >= min && k <= max ? 'on' : '') + '"></i>').join('') + '</span><b class="dif-n n' + min + '">' +
    (min === max ? NIVELES[min] : NIVELES[min] + ' a ' + NIVELES[max].toLowerCase()) + '</b>';
  return d;
}

function ponerFila(el, f) {
  const destino = el.querySelector('.cuerpo') || el.querySelector('.opt-meta') || el;
  const titulo = destino.querySelector('h3');
  if (titulo && titulo.nextSibling) titulo.parentNode.insertBefore(f, titulo.nextSibling); else destino.prepend(f);
}

function marca(resumen) {
  if (!resumen) return null;
  const m = document.createElement('div');
  m.className = 'hecha';
  m.textContent = '✓ Completada · mejor tiempo ' + formatoTiempo(resumen.mejor) + (resumen.veces > 1 ? ' · ' + resumen.veces + ' veces' : '');
  return m;
}

function pintarMarcas(catalogo, resumen) {
  document.querySelectorAll('.hecha').forEach((e) => e.remove());
  document.querySelectorAll('[data-juego]').forEach((el) => {
    const r = resumen[el.dataset.juego];
    const m = marca(r);
    if (m) (el.querySelector('.cuerpo') || el.querySelector('.opt-meta') || el).appendChild(m);
  });
  document.querySelectorAll('[data-hub]').forEach((el) => {
    const ids = catalogo.filter((j) => j.ruta.startsWith('juegos/aventuras-ca/')).map((j) => j.id);
    const hechas = ids.filter((i) => resumen[i]).length;
    if (hechas) {
      const m = document.createElement('div');
      m.className = 'hecha';
      m.textContent = '✓ ' + hechas + ' de ' + ids.length + ' aventuras completadas';
      (el.querySelector('.opt-meta') || el).appendChild(m);
    }
  });
}

// ---------------------------------------------------------------- qué juegos ve cada cuenta

function portadaDe(a, j) {
  if (a.portada) return a.portada;
  if (a.url) return a.url.replace(/[^/]*$/, '') + 'img/P.jpg';
  return j ? raiz + j.ruta + 'img/P.jpg' : '';
}

function enlaceDe(a, j) {
  if (a.url) return a.url;
  return j ? raiz + j.ruta + 'index.html' : '#';
}

function bienvenida(caja) {
  caja.innerHTML = '<div class="mis-vacio"><h2>Tus aventuras</h2>' +
    '<p>Entra con tu cuenta para ver tus juegos. Si os han regalado un pack, usad el correo con el que se compró.</p>' +
    '<p class="mis-botones"><button type="button" class="mis-btn" data-entrar>Entrar o crear cuenta</button>' +
    '<a class="mis-btn sec" href="' + raiz + 'tienda/">Ver la tienda</a></p></div>';
  caja.querySelector('[data-entrar]').addEventListener('click', () => abrirLogin({ motivo: 'Entra con el correo con el que se compró el pack.' }));
}

function pintarMis(caja, d, por) {
  const quienes = [...new Set(d.lista.map((a) => a.quienes).filter(Boolean))];
  let html = '';
  if (d.verComo) html += '<p class="mis-aviso">Estás viendo la app como <b>' + esc(d.verComo) + '</b>. <button type="button" data-volver>Volver a mi vista</button></p>';
  if (d.sinRed) html += '<p class="mis-aviso">Sin conexión: se enseñan los juegos que tenías la última vez.</p>';
  if (d.faltaTabla) html += '<p class="mis-aviso">Falta crear la tabla de accesos en Supabase (supabase/unlock_accesos.sql).</p>';
  if (!d.lista.length) {
    html += '<div class="mis-vacio"><h2>Tus aventuras</h2><p>Todavía no hay juegos en esta cuenta (<b>' + esc(d.email) + '</b>). ' +
      'Cuando estén listos aparecerán aquí. Si se compraron con otro correo, sal y entra con ese.</p>' +
      '<p class="mis-botones"><a class="mis-btn" href="' + raiz + 'tienda/">Ver la tienda</a></p></div>';
  } else {
    const saltos = document.body.dataset.estilo === 'saltos';  // el hub de Aventuras usa sus tarjetas grandes
    const titulo = quienes.length ? 'Las aventuras de ' + esc(quienes.join(', ')) : 'Tus aventuras';
    const cuantos = d.lista.length + ' juego' + (d.lista.length > 1 ? 's' : '') + ' en tu cuenta';
    html += saltos
      ? '<h2 class="seccion">' + titulo + '</h2><p class="sub">' + cuantos + '</p><div class="saltos">'
      : '<h2 class="grupo">' + titulo + '<small>' + cuantos + '</small></h2><section class="cards" aria-label="Tus aventuras">';
    d.lista.forEach((a, i) => {
      const j = por[a.juego];
      const img = esc(encodeURI(portadaDe(a, j)));
      const nombre = esc(j ? j.nombre : a.juego);
      const con = a.quienes ? '<p class="opt-desc">Con ' + esc(a.quienes) + ' de protagonistas</p>' : '';
      html += saltos
        ? '<a class="salto ' + esc(a.juego) + '" data-juego="' + esc(a.juego) + '" data-dif="' + (j ? j.dificultad : 3) + '" data-buscar="' + esc(a.juego) + '" href="' + esc(enlaceDe(a, j)) + '">' +
          '<div class="cartel" aria-hidden="true"><img src="' + img + '" alt=""></div><div class="cuerpo"><h3>' + nombre + '</h3>' + con + '</div></a>'
        : '<a class="option" data-juego="' + esc(a.juego) + '" data-dif="' + (j ? j.dificultad : 3) + '" data-buscar="' + esc(a.juego) + '" href="' + esc(enlaceDe(a, j)) + '">' +
          '<div class="opt-thumb" style="background-image:url(&quot;' + img.replace(/'/g, '%27') + '&quot;);background-position:center 30%"></div>' +
          '<div class="opt-meta"><h3 class="opt-title">' + nombre + '</h3>' + con + '</div>' +
          '<div class="opt-num">' + String(i + 1).padStart(2, '0') + '</div></a>';
    });
    html += saltos ? '</div>' : '</section>';
  }
  caja.innerHTML = html;
  const v = caja.querySelector('[data-volver]');
  if (v) v.addEventListener('click', () => { dejarDeVerComo(); location.reload(); });
  caja.querySelectorAll('[data-juego]').forEach((el) => {
    const j = por[el.dataset.juego];
    if (j) ponerFila(el, fila(j));
  });
  // con muchos juegos, buscador y filtro de dificultad (assets/js/filtro-juegos.js)
  const lista = caja.querySelector('.cards, .saltos');
  if (lista && d.lista.length > 4 && window.FiltroJuegos) window.FiltroJuegos.montar(lista, { items: '[data-juego]', nombre: 'aventura', antes: lista });
}

/** Enseña el catálogo completo (administrador) o solo los juegos de la cuenta. */
function aplicarVista(d, por) {
  const todo = document.getElementById('todo');
  const mis = document.getElementById('mis');
  if (d && d.admin) {
    if (todo) todo.hidden = false;
    if (mis) { mis.hidden = true; mis.replaceChildren(); }
    document.body.classList.remove('accesos-pend');
    return;
  }
  if (todo) todo.hidden = true;
  if (mis) {
    mis.hidden = false;
    if (d) pintarMis(mis, d, por); else bienvenida(mis);
  }
  document.body.classList.remove('accesos-pend');
}

async function iniciar() {
  const cont = document.getElementById('cuenta');
  if (cont) montarCuenta(cont, { perfil: raiz + 'perfil.html' });
  let catalogo = [];
  try { catalogo = await (await fetch(raiz + 'juegos/catalogo.json')).json(); } catch (e) { /* sin catálogo: sin decorar */ }
  const por = Object.fromEntries(catalogo.map((j) => [j.id, j]));
  // primero lo guardado en el dispositivo (al instante y sin red); luego lo de la nube
  const guardado = accesosGuardados(usuarioRecordado());
  if (guardado) aplicarVista(guardado, por);
  const ahora = await misAccesos();
  aplicarVista(ahora.usuario ? ahora : null, por);
  decorar(catalogo, por);
  let ultimo = ahora.usuario ? ahora.usuario.id : '';
  alCambiarSesion(async (u) => {
    if ((u ? u.id : '') === ultimo) return;
    ultimo = u ? u.id : '';
    if (!u) dejarDeVerComo();
    const d = await misAccesos();
    aplicarVista(d.usuario ? d : null, por);
    decorar(catalogo, por);
  });
}

async function decorar(catalogo, por) {
  if (!catalogo.length) return;
  document.querySelectorAll('#todo [data-juego], .saltos [data-juego]').forEach((el) => {
    const j = por[el.dataset.juego];
    if (j && !el.querySelector('.dif-fila')) ponerFila(el, fila(j));
    if (j) { el.dataset.dif = j.dificultad; el.dataset.buscar = j.id + ' ' + j.nombre; }
  });
  // hub de aventuras completo (administrador): buscador y filtro de dificultad, una sola vez
  const hub = document.querySelector('#todo .saltos');
  if (hub && !hub.dataset.filtro && window.FiltroJuegos && hub.querySelectorAll('[data-juego]').length > 4) {
    hub.dataset.filtro = '1';
    window.FiltroJuegos.montar(hub, { items: '[data-juego]', nombre: 'aventura' });
  }
  document.querySelectorAll('[data-hub]').forEach((el) => {
    if (!el.querySelector('.dif-fila')) ponerFila(el, filaHub(catalogo.filter((j) => j.ruta.startsWith('juegos/aventuras-ca/'))));
  });
  pintarMarcas(catalogo, resumenLocal());
  // con sesión, se completa con lo guardado en la nube
  try {
    const r = await misPartidas();
    if (r.usuario) pintarMarcas(catalogo, resumenPorJuego(r.partidas));
  } catch (e) { /* sin red: se queda lo local */ }
}

iniciar();
