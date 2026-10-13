// Carta 52 — Panel de oxígeno: girar tuberías para llevar el oxígeno de la entrada (izquierda) a la salida (derecha).
import { openGame } from './ui.js';

const COLS = 5, ROWS = 3, CELL = 100;
const CONN = {
  S: [['W', 'E'], ['N', 'S']],
  C: [['N', 'E'], ['E', 'S'], ['S', 'W'], ['W', 'N']]
};
const DELTA = { N: [0, -1], E: [1, 0], S: [0, 1], W: [-1, 0] };
const OPP = { N: 'S', E: 'W', S: 'N', W: 'E' };
const MID = { N: [50, 0], E: [100, 50], S: [50, 100], W: [0, 50] };
const NS = 'http://www.w3.org/2000/svg';
// [fila][columna] = tipo (S recta, C codo) y giro inicial
const GRID = [
  [{ t: 'C', r: 0 }, { t: 'C', r: 3 }, { t: 'S', r: 1 }, { t: 'C', r: 0 }, { t: 'S', r: 1 }],
  [{ t: 'S', r: 1 }, { t: 'C', r: 1 }, { t: 'S', r: 0 }, { t: 'S', r: 0 }, { t: 'C', r: 2 }],
  [{ t: 'S', r: 1 }, { t: 'C', r: 2 }, { t: 'C', r: 1 }, { t: 'C', r: 2 }, { t: 'C', r: 0 }]
];
const FILA_ENTRADA = 1;

function trazar() {
  const camino = [];
  let c = 0, r = FILA_ENTRADA, entrada = 'W';
  for (let i = 0; i < 30; i++) {
    if (c < 0 || c >= COLS || r < 0 || r >= ROWS) return { camino, ok: false };
    const celda = GRID[r][c];
    const con = CONN[celda.t][celda.r % CONN[celda.t].length];
    if (!con.includes(entrada)) return { camino, ok: false };
    camino.push(c + ',' + r);
    const salida = con[0] === entrada ? con[1] : con[0];
    if (c === COLS - 1 && r === FILA_ENTRADA && salida === 'E') return { camino, ok: true };
    c += DELTA[salida][0];
    r += DELTA[salida][1];
    entrada = OPP[salida];
  }
  return { camino, ok: false };
}

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 52 — Panel de oxígeno',
    instr: 'Toca las tuberías para girarlas hasta que el oxígeno llegue de la entrada a la salida.',
    ...opts
  });

  const svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('viewBox', `-60 0 ${COLS * CELL + 120} ${ROWS * CELL}`);
  svg.setAttribute('width', '100%');
  svg.style.background = '#0a1218';
  svg.style.borderRadius = '10px';
  svg.style.touchAction = 'manipulation';
  ui.body.appendChild(svg);

  let resuelto = false;

  function el(tag, attrs) {
    const e = document.createElementNS(NS, tag);
    Object.keys(attrs).forEach(k => e.setAttribute(k, attrs[k]));
    svg.appendChild(e);
    return e;
  }

  function pintar() {
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    const { camino, ok } = trazar();
    for (let r = 0; r < ROWS; r++) {
      for (let c = 0; c < COLS; c++) {
        const x0 = c * CELL, y0 = r * CELL;
        el('rect', { x: x0 + 3, y: y0 + 3, width: CELL - 6, height: CELL - 6, rx: 8, fill: '#12202b' });
        const celda = GRID[r][c];
        const agua = camino.includes(c + ',' + r);
        CONN[celda.t][celda.r % CONN[celda.t].length].forEach(lado => {
          el('line', {
            x1: x0 + 50, y1: y0 + 50, x2: x0 + MID[lado][0], y2: y0 + MID[lado][1],
            stroke: agua ? '#4cc9f0' : '#7a8896', 'stroke-width': 18
          });
        });
        el('circle', { cx: x0 + 50, cy: y0 + 50, r: 11, fill: agua ? '#4cc9f0' : '#7a8896' });
        const hot = el('rect', { x: x0, y: y0, width: CELL, height: CELL, fill: 'transparent' });
        hot.style.cursor = resuelto ? 'default' : 'pointer';
        hot.addEventListener('click', () => {
          if (resuelto) return;
          celda.r = (celda.r + 1) % CONN[celda.t].length;
          ui.say('');
          pintar();
        });
      }
    }
    const t1 = el('text', { x: -30, y: FILA_ENTRADA * CELL + 58, 'text-anchor': 'middle', 'font-size': 26, fill: '#ffb347', 'font-weight': 700, 'font-family': 'system-ui,sans-serif' });
    t1.textContent = 'O₂ ▶';
    const t2 = el('text', { x: COLS * CELL + 32, y: FILA_ENTRADA * CELL + 58, 'text-anchor': 'middle', 'font-size': 24, fill: ok ? '#9dffb0' : '#7a8896', 'font-weight': 700, 'font-family': 'system-ui,sans-serif' });
    t2.textContent = '▶ 🏠';
    if (ok && !resuelto) {
      resuelto = true;
      ui.say('¡El oxígeno circula! El soporte vital se reactiva. Coged la carta 66.', 'ok');
    }
  }

  pintar();
  return { close: ui.close };
}
