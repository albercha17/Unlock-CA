// Carta 70 — Espejos de la lente: llevar el haz de luz de la izquierda a la lámpara (5,4).
// Solución: espejos de camino (2,2)='/', (2,0)='/', (5,0)='\'. Los otros tres son señuelos.
import { openGame } from './ui.js';

const COLS = 7, ROWS = 5, CELL = 100;
const SOURCE_ROW = 2;
const TARGET = { c: 5, r: 4 };
const mirrors = {
  '2,2': '\\', '2,0': '\\', '5,0': '/',
  '4,2': '/', '3,3': '\\', '1,4': '/'
};
const DIRS = { E: [1, 0], W: [-1, 0], N: [0, -1], S: [0, 1] };
const SLASH = { E: 'N', N: 'E', W: 'S', S: 'W' };
const BACK = { E: 'S', S: 'E', W: 'N', N: 'W' };
const NS = 'http://www.w3.org/2000/svg';

function trace() {
  const pts = [[0, SOURCE_ROW * CELL + CELL / 2]];
  let c = -1, r = SOURCE_ROW, dir = 'E', hit = false;
  for (let i = 0; i < 80; i++) {
    c += DIRS[dir][0];
    r += DIRS[dir][1];
    if (c < 0 || c >= COLS || r < 0 || r >= ROWS) {
      const x = Math.max(0, Math.min(COLS * CELL, (c + 0.5) * CELL));
      const y = Math.max(0, Math.min(ROWS * CELL, (r + 0.5) * CELL));
      pts.push([dir === 'E' ? COLS * CELL : dir === 'W' ? 0 : x, dir === 'S' ? ROWS * CELL : dir === 'N' ? 0 : y]);
      break;
    }
    pts.push([(c + 0.5) * CELL, (r + 0.5) * CELL]);
    if (c === TARGET.c && r === TARGET.r) { hit = true; break; }
    const m = mirrors[c + ',' + r];
    if (m) dir = m === '/' ? SLASH[dir] : BACK[dir];
  }
  return { pts, hit };
}

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 70 — Espejos de la lente',
    instr: 'Toca los espejos para girarlos y lleva la luz hasta la lámpara de abajo a la derecha.',
    ...opts
  });

  const svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('viewBox', `0 0 ${COLS * CELL} ${ROWS * CELL}`);
  svg.setAttribute('width', '100%');
  svg.style.background = '#0a1118';
  svg.style.borderRadius = '10px';
  svg.style.touchAction = 'manipulation';
  ui.body.appendChild(svg);

  let solved = false;

  function draw() {
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    for (let c = 0; c < COLS; c++) for (let r = 0; r < ROWS; r++) {
      const cell = document.createElementNS(NS, 'rect');
      cell.setAttribute('x', c * CELL + 2); cell.setAttribute('y', r * CELL + 2);
      cell.setAttribute('width', CELL - 4); cell.setAttribute('height', CELL - 4);
      cell.setAttribute('fill', '#101a24'); cell.setAttribute('rx', '6');
      svg.appendChild(cell);
    }
    const { pts, hit } = trace();
    const beam = document.createElementNS(NS, 'polyline');
    beam.setAttribute('points', pts.map(p => p.join(',')).join(' '));
    beam.setAttribute('fill', 'none');
    beam.setAttribute('stroke', '#ffd27a');
    beam.setAttribute('stroke-width', '7');
    beam.setAttribute('stroke-linejoin', 'round');
    beam.setAttribute('stroke-linecap', 'round');
    svg.appendChild(beam);

    Object.keys(mirrors).forEach(key => {
      const [c, r] = key.split(',').map(Number);
      const x0 = c * CELL, y0 = r * CELL;
      const line = document.createElementNS(NS, 'line');
      const slash = mirrors[key] === '/';
      line.setAttribute('x1', x0 + 16); line.setAttribute('x2', x0 + CELL - 16);
      line.setAttribute('y1', slash ? y0 + CELL - 16 : y0 + 16);
      line.setAttribute('y2', slash ? y0 + 16 : y0 + CELL - 16);
      line.setAttribute('stroke', '#9fd4ff'); line.setAttribute('stroke-width', '10');
      line.setAttribute('stroke-linecap', 'round');
      svg.appendChild(line);
      const hot = document.createElementNS(NS, 'rect');
      hot.setAttribute('x', x0); hot.setAttribute('y', y0);
      hot.setAttribute('width', CELL); hot.setAttribute('height', CELL);
      hot.setAttribute('fill', 'transparent');
      hot.style.cursor = solved ? 'default' : 'pointer';
      hot.addEventListener('click', () => {
        if (solved) return;
        mirrors[key] = mirrors[key] === '/' ? '\\' : '/';
        draw();
      });
      svg.appendChild(hot);
    });

    const lamp = document.createElementNS(NS, 'circle');
    lamp.setAttribute('cx', (TARGET.c + 0.5) * CELL); lamp.setAttribute('cy', (TARGET.r + 0.5) * CELL);
    lamp.setAttribute('r', '26');
    lamp.setAttribute('fill', hit ? '#fff6c8' : '#3a4a5c');
    lamp.setAttribute('stroke', hit ? '#ffd27a' : '#667a8f'); lamp.setAttribute('stroke-width', '5');
    svg.appendChild(lamp);
    const src = document.createElementNS(NS, 'circle');
    src.setAttribute('cx', 10); src.setAttribute('cy', SOURCE_ROW * CELL + CELL / 2);
    src.setAttribute('r', '12'); src.setAttribute('fill', '#ffd27a');
    svg.appendChild(src);

    if (hit && !solved) {
      solved = true;
      ui.say('¡La luz llega a la lámpara! El mecanismo queda alineado. Descartad la carta 70.', 'ok');
    }
  }

  draw();
  return { close: ui.close };
}
