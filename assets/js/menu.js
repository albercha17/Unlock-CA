// menu.js — decora los menús: dificultad, duración y nº de cartas de cada juego (antes de elegir), marcas de partidas
// ya hechas con el mejor tiempo, y el botón de cuenta. Lee juegos/catalogo.json (lo genera herramientas/generar_catalogo.py).
import { resumenLocal, misPartidas, resumenPorJuego, formatoTiempo } from './cuenta.js';
import { montarCuenta } from './cuenta-ui.js';

const NIVELES = ['', 'Muy fácil', 'Fácil', 'Media', 'Difícil', 'Muy difícil'];
const raiz = document.body.dataset.raiz || '';

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

async function iniciar() {
  const cont = document.getElementById('cuenta');
  if (cont) montarCuenta(cont, { perfil: raiz + 'perfil.html' });
  let catalogo = [];
  try { catalogo = await (await fetch(raiz + 'juegos/catalogo.json')).json(); } catch (e) { return; }
  const por = Object.fromEntries(catalogo.map((j) => [j.id, j]));
  document.querySelectorAll('[data-juego]').forEach((el) => {
    const j = por[el.dataset.juego];
    if (!j) return;
    const destino = el.querySelector('.cuerpo') || el.querySelector('.opt-meta') || el;
    const titulo = destino.querySelector('h3');
    const f = fila(j);
    if (titulo && titulo.nextSibling) titulo.parentNode.insertBefore(f, titulo.nextSibling); else destino.prepend(f);
  });
  document.querySelectorAll('[data-hub]').forEach((el) => {
    const js = catalogo.filter((j) => j.ruta.startsWith('juegos/aventuras-ca/'));
    const destino = el.querySelector('.opt-meta') || el;
    const titulo = destino.querySelector('h3');
    const f = filaHub(js);
    if (titulo && titulo.nextSibling) titulo.parentNode.insertBefore(f, titulo.nextSibling); else destino.prepend(f);
  });
  pintarMarcas(catalogo, resumenLocal());
  // con sesión, se completa con lo guardado en la nube
  try {
    const r = await misPartidas();
    if (r.usuario) pintarMarcas(catalogo, resumenPorJuego(r.partidas));
  } catch (e) { /* sin red: se queda lo local */ }
}

iniciar();
