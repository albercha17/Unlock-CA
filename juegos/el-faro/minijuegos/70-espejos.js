// Carta 70 — Espejos de la lente: llevar el rayo del foco, por orden, a la galería, a la lente y a la lámpara.
// Pista del nido (carta 27): «La luz sube, cruza y baja». Tablero 8×6, 11 espejos (7 del camino y 4 señuelos), 3 rocas.
// Solución única (por el camino): los espejos que toca el rayo quedan así:
//   B4 '/', B3 '/', D3 '/', D2 '/', G2 '\', G3 '/', F3 '/'  (columna A-H, fila 1-6)
// Los señuelos (A6, A3, H2, H5) pueden quedar como estén. El rayo pasa por: galería (E2), lente (F5) y lámpara (F6).
import { openGame } from './ui.js';

const COLS = 8, ROWS = 6, CELL = 80;
const NS = 'http://www.w3.org/2000/svg';
const LETRAS = 'ABCDEFGH';
const FILA_FOCO = 3;
const MARCAS = { '4,1': 'G', '5,4': 'L', '5,5': 'A' };
const NOMBRE = { G: 'Galería', L: 'Lente', A: 'Lámpara' };
const ORDEN = ['G', 'L', 'A'];
const ROCAS = ['2,1', '3,5', '6,5'];
// Estado inicial: ni mucho menos resuelto (5 de los 7 espejos del camino están al revés).
const INICIAL = {
  '1,3': '\\', '1,2': '\\', '3,2': '\\', '3,1': '/', '6,1': '/', '6,2': '/', '5,2': '\\',
  '0,5': '/', '0,2': '\\', '7,1': '\\', '7,4': '/'
};
const DIRS = { E: [1, 0], O: [-1, 0], N: [0, -1], S: [0, 1] };
const REFL = { '/': { E: 'N', N: 'E', O: 'S', S: 'O' }, '\\': { E: 'S', S: 'E', O: 'N', N: 'O' } };
const SPR = './img/ui/espejos/';
const nombreCelda = k => { const [c, r] = k.split(',').map(Number); return LETRAS[c] + (r + 1); };

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 70 — Espejos de la lente',
    instr: 'Toca los espejos para girarlos y lleva el rayo del foco por los tres puntos del tablero, en el orden que dice el papel del nido.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .far-lente-svg{display:block;width:100%;border-radius:12px;border:2px solid #6b4a1e;background:#0a1118;touch-action:manipulation}
    .far-mirror{transform-box:fill-box;transform-origin:center;transition:transform .28s cubic-bezier(.3,1.4,.5,1)}
    .far-m-hot{cursor:pointer}
    .far-m-hot:hover + .far-m-anillo{opacity:1}
    .far-m-anillo{opacity:0;transition:opacity .15s;pointer-events:none}
    .far-luz-flujo{animation:far-flujo .9s linear infinite}
    .far-marca-lit{animation:far-latido 1.6s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
    .far-estado{display:flex;gap:8px;justify-content:center;margin:10px 0 2px}
    .far-estado span{flex:1;max-width:120px;padding:7px 4px;border-radius:9px;border:1.5px solid rgba(255,255,255,.18);background:rgba(0,0,0,.3);color:#9fb4c8;font-weight:700;font-size:.82rem}
    .far-estado span.hecho{border-color:#ffd27a;color:#ffd27a;background:rgba(255,210,122,.14);box-shadow:0 0 12px rgba(255,210,122,.35)}
    @keyframes far-flujo{to{stroke-dashoffset:-36}}
    @keyframes far-latido{0%,100%{transform:scale(1)}50%{transform:scale(1.08)}}
    @media (prefers-reduced-motion:reduce){.far-luz-flujo,.far-marca-lit,.far-mirror{animation:none!important;transition:none!important}}
  `;
  ui.body.appendChild(style);

  const ancho = COLS * CELL, alto = ROWS * CELL;
  const svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('viewBox', `-84 -8 ${ancho + 96} ${alto + 16}`);
  svg.classList.add('far-lente-svg');
  const estado = document.createElement('div');
  estado.className = 'far-estado';
  const aviso = document.createElement('div');
  aviso.className = 'far-instr';
  aviso.style.cssText = 'min-height:1.2em;margin:6px 0 0;font-size:.82rem;color:#ffd27a';
  ui.body.append(svg, estado, aviso);

  const espejos = { ...INICIAL };
  let resuelto = false;
  const fichas = {};
  ORDEN.forEach(m => {
    const s = document.createElement('span');
    s.dataset.marca = m;
    s.textContent = NOMBRE[m];
    estado.appendChild(s);
    fichas[m] = s;
  });

  function el(tag, attrs, padre) {
    const e = document.createElementNS(NS, tag);
    Object.keys(attrs || {}).forEach(k => e.setAttribute(k, attrs[k]));
    (padre || svg).appendChild(e);
    return e;
  }
  function imagen(nombre, x, y, w, h, extra, padre) {
    const i = el('image', Object.assign({ href: SPR + nombre + '.jpg', x, y, width: w, height: h, preserveAspectRatio: 'xMidYMid meet' }, extra || {}), padre);
    i.style.mixBlendMode = 'screen';
    return i;
  }

  // --- capas estáticas ---
  el('image', { href: SPR + 'tablero.jpg', x: 0, y: 0, width: ancho, height: alto, preserveAspectRatio: 'xMidYMid slice' });
  el('rect', { x: 0, y: 0, width: ancho, height: alto, fill: 'rgba(6,10,16,.58)' });
  for (let c = 0; c <= COLS; c++) el('line', { x1: c * CELL, y1: 0, x2: c * CELL, y2: alto, stroke: 'rgba(255,230,170,.10)' });
  for (let r = 0; r <= ROWS; r++) el('line', { x1: 0, y1: r * CELL, x2: ancho, y2: r * CELL, stroke: 'rgba(255,230,170,.10)' });
  for (let c = 0; c < COLS; c++) el('text', { x: c * CELL + CELL / 2, y: alto + 1, 'text-anchor': 'middle', 'font-size': 9, fill: 'rgba(255,230,170,.55)', 'font-family': 'system-ui,sans-serif' }, null).textContent = LETRAS[c];
  for (let r = 0; r < ROWS; r++) el('text', { x: 6, y: r * CELL + 11, 'font-size': 9, fill: 'rgba(255,230,170,.55)', 'font-family': 'system-ui,sans-serif' }, null).textContent = String(r + 1);

  const defs = el('defs');
  const clip = el('clipPath', { id: 'far-roca-recorte', clipPathUnits: 'objectBoundingBox' }, defs);
  el('circle', { cx: 0.5, cy: 0.5, r: 0.46 }, clip);
  ROCAS.forEach(k => {
    const [c, r] = k.split(',').map(Number);
    el('image', { href: SPR + 'roca.jpg', x: c * CELL + 6, y: r * CELL + 6, width: CELL - 12, height: CELL - 12, 'clip-path': 'url(#far-roca-recorte)', preserveAspectRatio: 'xMidYMid slice' });
  });

  // foco (fuente del rayo)
  const yFoco = FILA_FOCO * CELL + CELL / 2;
  imagen('foco', -80, yFoco - 36, 72, 72);

  // rayo (debajo de espejos y marcas)
  const capaRayo = el('g');
  const rayoHalo = el('polyline', { fill: 'none', stroke: 'rgba(255,190,80,.32)', 'stroke-width': 17, 'stroke-linejoin': 'round', 'stroke-linecap': 'round' }, capaRayo);
  const rayo = el('polyline', { fill: 'none', stroke: '#ffd27a', 'stroke-width': 6, 'stroke-linejoin': 'round', 'stroke-linecap': 'round' }, capaRayo);
  const rayoFlujo = el('polyline', { fill: 'none', stroke: '#fff6d0', 'stroke-width': 2.2, 'stroke-linejoin': 'round', 'stroke-dasharray': '10 8', class: 'far-luz-flujo' }, capaRayo);

  // marcas: galería, lente, lámpara
  const marcaEl = {};
  Object.keys(MARCAS).forEach(k => {
    const [c, r] = k.split(',').map(Number);
    const m = MARCAS[k];
    const g = el('g', { 'data-marca': m });
    const nombre = m === 'G' ? 'galeria' : (m === 'L' ? 'lente' : 'lampara-apagada');
    const halo = el('circle', { cx: c * CELL + CELL / 2, cy: r * CELL + CELL / 2, r: CELL * 0.42, fill: 'rgba(255,210,122,0)', stroke: 'rgba(255,210,122,.0)', 'stroke-width': 3 }, g);
    const spr = imagen(nombre, c * CELL + 6, r * CELL + 6, CELL - 12, CELL - 12, null, g);
    const num = el('text', { x: c * CELL + CELL - 14, y: r * CELL + 18, 'text-anchor': 'middle', 'font-size': 15, 'font-weight': 800, fill: '#ffd27a', 'font-family': 'system-ui,sans-serif', opacity: 0, stroke: '#1a1008', 'stroke-width': 3, 'paint-order': 'stroke' }, g);
    marcaEl[m] = { g, halo, spr, num, nombre };
  });

  // espejos
  const espejoEl = {};
  Object.keys(INICIAL).forEach(k => {
    const [c, r] = k.split(',').map(Number);
    const x0 = c * CELL, y0 = r * CELL;
    const g = el('g', { class: 'far-mirror', 'data-c': k });
    imagen('espejo', x0 + 4, y0 + 4, CELL - 8, CELL - 8, null, g);
    const hot = el('rect', { x: x0, y: y0, width: CELL, height: CELL, fill: 'transparent', class: 'far-m-hot', 'data-c': k, role: 'button', 'aria-label': 'Espejo en ' + nombreCelda(k) }, svg);
    el('circle', { cx: x0 + CELL / 2, cy: y0 + CELL / 2, r: CELL * 0.44, fill: 'none', stroke: '#ffd27a', 'stroke-width': 2, 'stroke-dasharray': '4 4', class: 'far-m-anillo' }, svg);
    hot.addEventListener('click', () => {
      if (resuelto) return;
      espejos[k] = espejos[k] === '/' ? '\\' : '/';
      actualizar();
    });
    espejoEl[k] = g;
  });

  // --- física del rayo ---
  function trazar() {
    const pts = [[-10, yFoco]];
    let x = -1, y = FILA_FOCO, d = 'E';
    const visto = new Set();
    const marcasVistas = [];
    for (let i = 0; i < 400; i++) {
      x += DIRS[d][0];
      y += DIRS[d][1];
      if (x < 0 || x >= COLS || y < 0 || y >= ROWS) {
        const [px, py] = pts[pts.length - 1];
        pts.push(d === 'E' ? [ancho, py] : d === 'O' ? [0, py] : d === 'S' ? [px, alto] : [px, 0]);
        break;
      }
      const k = x + ',' + y;
      pts.push([(x + 0.5) * CELL, (y + 0.5) * CELL]);
      if (ROCAS.includes(k)) break;
      if (visto.has(k + d)) break;
      visto.add(k + d);
      if (MARCAS[k] && !marcasVistas.includes(MARCAS[k])) marcasVistas.push(MARCAS[k]);
      if (espejos[k]) d = REFL[espejos[k]][d];
    }
    return { pts, marcasVistas };
  }

  function actualizar() {
    Object.keys(espejos).forEach(k => {
      espejoEl[k].setAttribute('data-o', espejos[k]);
      espejoEl[k].style.transform = espejos[k] === '/' ? 'scaleX(1)' : 'scaleX(-1)';
    });
    const { pts, marcasVistas } = trazar();
    const p = pts.map(q => q.join(',')).join(' ');
    rayoHalo.setAttribute('points', p);
    rayo.setAttribute('points', p);
    rayoFlujo.setAttribute('points', p);
    // marcas encendidas en orden
    let n = 0;
    const lit = {};
    ORDEN.forEach(m => { if (marcasVistas.includes(m) && n === ORDEN.indexOf(m)) { lit[m] = true; n++; } });
    ORDEN.forEach(m => {
      const e = marcaEl[m];
      const on = !!lit[m];
      e.halo.setAttribute('fill', on ? 'rgba(255,210,122,.30)' : 'rgba(255,210,122,0)');
      e.halo.setAttribute('stroke', on ? 'rgba(255,210,122,.9)' : 'rgba(255,210,122,0)');
      e.g.classList.toggle('far-marca-lit', on);
      e.num.setAttribute('opacity', on ? 1 : 0);
      e.num.textContent = on ? String(ORDEN.indexOf(m) + 1) : '';
      if (m === 'A') e.spr.setAttribute('href', SPR + (on ? 'lampara-encendida' : 'lampara-apagada') + '.jpg');
      fichas[m].classList.toggle('hecho', on);
    });
    // aviso si llega a un punto antes de tiempo
    const fuera = marcasVistas.find((m, i) => !lit[m]);
    aviso.textContent = fuera ? 'La luz toca «' + NOMBRE[fuera] + '» antes de tiempo: el orden importa (el papel del nido).' : '';
    if (!resuelto && lit.A) {
      resuelto = true;
      svg.querySelectorAll('.far-m-hot').forEach(h => { h.style.cursor = 'default'; });
      ui.say('¡La luz sube a la galería, cruza la lente y baja hasta la lámpara! El mecanismo queda alineado. Descartad las cartas 70 y 27.', 'ok');
    }
  }

  ui.button('Reiniciar espejos', 'ghost', () => {
    if (resuelto) return;
    Object.assign(espejos, INICIAL);
    ui.say('');
    actualizar();
  });

  actualizar();
  return { close: ui.close };
}
