// Carta 92 — Rayo del amanecer: colocar la lente en uno de los tres atriles y tres espejos de modo que el rayo
// que entra por el lucernario (sobre la columna A) atraviese la lente y llegue al Cronoportal (A3).
// El plano (carta 94) dice: lente en el atril de la columna B, fila 3.
// Solución única: lente en B3; espejos \ en A2, \ en C2 y / en C3.
import { openGame } from './ui.js';

const NS = 'http://www.w3.org/2000/svg';
const COLS = 6, FILAS = 5, CELL = 52, MARGEN = 26;
const SOL_COL = 0;
const PORTAL = '0,2';
const ATRILES = ['3,4', '1,2', '4,2'];
const OBSTACULOS = ['2,0', '3,1', '3,3', '4,3', '4,4'];
const LETRAS = 'ABCDEF';
const MAX_ESPEJOS = 3;
const DIRS = { N: [0, -1], S: [0, 1], E: [1, 0], O: [-1, 0] };
const REFL = { '/': { E: 'N', N: 'E', O: 'S', S: 'O' }, '\\': { E: 'S', S: 'E', O: 'N', N: 'O' } };
const nombre = k => { const [x, y] = k.split(',').map(Number); return LETRAS[x] + (y + 1); };

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 92 — Rayo del amanecer',
    instr: 'Coloca la lente en un atril y tres espejos para llevar el rayo del lucernario hasta el Cronoportal. Toca un espejo ya puesto para girarlo o quitarlo.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .far-e-svg{display:block;width:100%;background:#1a1109;border:2px solid #6b4a1e;border-radius:12px}
    .far-e-cell{cursor:pointer}
    .far-e-tools{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:10px 0 6px}
    .far-e-tool{padding:10px 4px;border-radius:9px;border:2px solid rgba(255,255,255,.14);background:rgba(255,255,255,.06);color:#fff;font-weight:700;font-size:.85rem;cursor:pointer;font-family:inherit}
    .far-e-tool.sel{border-color:#ffd27a;color:#ffd27a;background:rgba(255,210,122,.16)}
    .far-e-info{color:#9fb4c8;font-size:.82rem;text-align:center;min-height:1.2em}
  `;
  ui.body.appendChild(style);

  const svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('viewBox', `${-MARGEN} ${-MARGEN - 8} ${COLS * CELL + 2 * MARGEN} ${FILAS * CELL + 2 * MARGEN + 8}`);
  svg.classList.add('far-e-svg');
  const tools = document.createElement('div');
  tools.className = 'far-e-tools';
  const info = document.createElement('div');
  info.className = 'far-e-info';
  ui.body.append(svg, tools, info);

  let herramienta = 'lente';
  let lente = null;                // clave "x,y" del atril con la lente
  const espejos = {};              // "x,y" -> '/' | '\\'
  let resuelto = false;

  function el(tag, attrs, texto) {
    const e = document.createElementNS(NS, tag);
    Object.keys(attrs).forEach(k => e.setAttribute(k, attrs[k]));
    if (texto !== undefined) e.textContent = texto;
    svg.appendChild(e);
    return e;
  }

  // Recorre el rayo desde el lucernario. Devuelve la lista de puntos, si llegó al portal y si pasó por la lente.
  function trazar() {
    let x = SOL_COL, y = 0, d = 'S';
    const puntos = [[x * CELL + CELL / 2, -MARGEN + 4]];
    let pasoLente = false, llega = false, fin = null;
    const visto = new Set();
    while (x >= 0 && x < COLS && y >= 0 && y < FILAS) {
      const k = x + ',' + y;
      const marca = k + d;
      if (visto.has(marca)) { fin = 'bucle'; break; }
      visto.add(marca);
      const cx = x * CELL + CELL / 2, cy = y * CELL + CELL / 2;
      if (OBSTACULOS.includes(k)) { puntos.push([cx, cy]); fin = 'obstaculo:' + k; break; }
      if (k === lente) pasoLente = true;
      if (k === PORTAL) { puntos.push([cx, cy]); llega = true; break; }
      if (espejos[k]) { puntos.push([cx, cy]); d = REFL[espejos[k]][d]; }
      x += DIRS[d][0]; y += DIRS[d][1];
    }
    if (!llega && fin === null) {
      // salió de la rejilla
      const [px, py] = [Math.max(-MARGEN + 4, Math.min(COLS * CELL + MARGEN - 4, x * CELL + CELL / 2)), Math.max(-MARGEN + 4, Math.min(FILAS * CELL + MARGEN - 4, y * CELL + CELL / 2))];
      puntos.push([px, py]);
      fin = 'borde';
    }
    return { puntos, llega, pasoLente, fin };
  }

  function pintar() {
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    for (let c = 0; c < COLS; c++) el('text', { x: c * CELL + CELL / 2, y: -10, 'text-anchor': 'middle', 'font-size': 12, fill: '#e8d9b0', 'font-family': 'system-ui,sans-serif' }, LETRAS[c]);
    for (let r = 0; r < FILAS; r++) el('text', { x: -10, y: r * CELL + CELL / 2 + 4, 'text-anchor': 'middle', 'font-size': 12, fill: '#e8d9b0', 'font-family': 'system-ui,sans-serif' }, String(r + 1));
    for (let r = 0; r < FILAS; r++) {
      for (let c = 0; c < COLS; c++) {
        const k = c + ',' + r;
        const g = el('g', { class: 'far-e-cell', 'data-c': k });
        const rect = document.createElementNS(NS, 'rect');
        [['x', c * CELL + 1.5], ['y', r * CELL + 1.5], ['width', CELL - 3], ['height', CELL - 3], ['rx', 5], ['fill', '#3a2814']].forEach(([a, v]) => rect.setAttribute(a, v));
        g.appendChild(rect);
        svg.appendChild(g);
        g.addEventListener('click', () => pulsar(k));
      }
    }
    // elementos fijos
    OBSTACULOS.forEach(k => {
      const [x, y] = k.split(',').map(Number);
      el('text', { x: x * CELL + CELL / 2, y: y * CELL + CELL / 2 + 10, 'text-anchor': 'middle', 'font-size': 28, 'pointer-events': 'none' }, '🏛️');
    });
    ATRILES.forEach(k => {
      const [x, y] = k.split(',').map(Number);
      el('circle', { cx: x * CELL + CELL / 2, cy: y * CELL + CELL / 2, r: 17, fill: 'none', stroke: '#e8d9b0', 'stroke-width': 2, 'stroke-dasharray': '4 3', 'pointer-events': 'none' });
      if (k === lente) el('text', { x: x * CELL + CELL / 2, y: y * CELL + CELL / 2 + 9, 'text-anchor': 'middle', 'font-size': 26, 'pointer-events': 'none' }, '🔍');
    });
    const [px, py] = PORTAL.split(',').map(Number);
    el('text', { x: px * CELL + CELL / 2, y: py * CELL + CELL / 2 + 9, 'text-anchor': 'middle', 'font-size': 28, 'pointer-events': 'none' }, '🌀');
    el('text', { x: SOL_COL * CELL + CELL / 2, y: -MARGEN + 8, 'text-anchor': 'middle', 'font-size': 18, 'pointer-events': 'none' }, '☀️');
    // espejos
    Object.keys(espejos).forEach(k => {
      const [x, y] = k.split(',').map(Number);
      const cx = x * CELL + CELL / 2, cy = y * CELL + CELL / 2;
      const a = espejos[k] === '/' ? [cx - 17, cy + 17, cx + 17, cy - 17] : [cx - 17, cy - 17, cx + 17, cy + 17];
      el('line', { x1: a[0], y1: a[1], x2: a[2], y2: a[3], stroke: '#e3b34f', 'stroke-width': 7, 'stroke-linecap': 'round', 'pointer-events': 'none' });
      el('line', { x1: a[0], y1: a[1], x2: a[2], y2: a[3], stroke: '#fff3c4', 'stroke-width': 2.5, 'stroke-linecap': 'round', 'pointer-events': 'none', class: 'far-e-espejo', 'data-c': k, 'data-o': espejos[k] });
    });
    // rayo
    const t = trazar();
    const pts = t.puntos.map(p => p.join(',')).join(' ');
    el('polyline', { points: pts, fill: 'none', stroke: 'rgba(255,210,100,.35)', 'stroke-width': 9, 'stroke-linejoin': 'round', 'pointer-events': 'none' });
    el('polyline', { points: pts, fill: 'none', stroke: '#fff1b0', 'stroke-width': 3, 'stroke-linejoin': 'round', 'pointer-events': 'none' });
    // herramientas
    tools.innerHTML = '';
    [['lente', 'Lente'], ['espejo', 'Espejo (' + (MAX_ESPEJOS - Object.keys(espejos).length) + ')'], ['quitar', 'Quitar']].forEach(([id, txt]) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'far-e-tool' + (herramienta === id ? ' sel' : '');
      b.dataset.tool = id;
      b.textContent = txt;
      b.addEventListener('click', () => { herramienta = id; pintar(); });
      tools.appendChild(b);
    });
    info.textContent = lente ? 'Lente en ' + nombre(lente) + ' · Espejos: ' + (Object.keys(espejos).map(k => nombre(k) + ' ' + espejos[k]).join(', ') || 'ninguno') : 'Aún no hay lente colocada.';
  }

  function pulsar(k) {
    if (resuelto) return;
    ui.say('');
    if (herramienta === 'lente') {
      if (!ATRILES.includes(k)) { ui.say('La lente solo cabe en un atril (los círculos de puntos).', 'bad'); return; }
      lente = k;
    } else if (herramienta === 'quitar') {
      if (k === lente) lente = null;
      delete espejos[k];
    } else {
      if (OBSTACULOS.includes(k) || ATRILES.includes(k) || k === PORTAL) { ui.say('Ahí no se puede poner un espejo.', 'bad'); return; }
      if (espejos[k] === '/') espejos[k] = '\\';
      else if (espejos[k] === '\\') delete espejos[k];
      else {
        if (Object.keys(espejos).length >= MAX_ESPEJOS) { ui.say('Solo tenéis tres espejos: quitad uno antes.', 'bad'); return; }
        espejos[k] = '/';
      }
    }
    pintar();
  }

  ui.button('Probar', 'primary', () => {
    if (resuelto) return;
    if (!lente) { ui.say('Falta la lente: colócala en uno de los atriles.', 'bad'); return; }
    const t = trazar();
    if (t.llega && t.pasoLente) {
      resuelto = true;
      ui.say('El rayo atraviesa la lente, se concentra y llega al Cronoportal, que despierta con un destello dorado. ¡El portal de vuelta se abre! Coged la carta 99.', 'ok');
    } else if (t.llega) {
      ui.say('El rayo llega al Cronoportal, pero sin pasar por la lente: la luz no se concentra y no basta.', 'bad');
    } else if (t.fin && t.fin.startsWith('obstaculo')) {
      ui.say('El rayo se detiene contra una columna en ' + nombre(t.fin.split(':')[1]) + '.', 'bad');
    } else if (t.fin === 'bucle') {
      ui.say('El rayo da vueltas sin llegar a ninguna parte.', 'bad');
    } else {
      ui.say('El rayo se pierde fuera del taller. Probad otra colocación.', 'bad');
    }
  });

  pintar();
  return { close: ui.close };
}
