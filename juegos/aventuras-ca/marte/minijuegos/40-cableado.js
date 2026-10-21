// Carta 40 — La placa de bornes (Numberlink): pintar el recorrido de cada cable. Los bornes gemelos de cada color están en las cartas 41 y 43
// (dos mitades); la norma, en la 45. Cada casilla se pinta con un cable (1 a 5) y todas deben llevar uno. Solución única (instancias_marte.py).
// Dato de la misión: 5.
import { openGame } from './ui.js';
import { estilo, rejilla } from './cupula.js';

const D = /*DATOS*/{"n": 6, "colores": 5, "solucion": [[2, 2, 2, 0, 0, 0], [2, 3, 2, 0, 1, 4], [3, 3, 2, 2, 1, 4], [3, 1, 1, 2, 1, 4], [4, 1, 1, 1, 1, 4], [4, 4, 4, 4, 4, 4]], "dato": 5}/*FIN*/;
const TONO = ['#be322c', '#3c64d2', '#46a05a', '#e8be3c', '#8c50be'];

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 40 — La placa de bornes', instr: 'Tocad una casilla para pintarla con un cable (1 a 5, y otra vez sin pintar). Cada cable une sus dos bornes sin cruzarse con otro y sin dejar casillas vacías. Los bornes, en las cartas 41 y 43.', ...opts });
  estilo('mr-cab', `.cab .mr-cel{background:#c8d6ce;color:#fff;font:800 1.1rem system-ui}`);
  const col = Array.from({ length: D.n }, () => Array(D.n).fill(null));
  let resuelto = false;
  const r = rejilla(D.n, (x, y, b) => {
    if (resuelto) return;
    col[y][x] = col[y][x] === null ? 0 : col[y][x] + 1 >= D.colores ? null : col[y][x] + 1;
    b.style.background = col[y][x] === null ? '' : TONO[col[y][x]]; b.textContent = col[y][x] === null ? '' : String(col[y][x] + 1);
    ui.say('');
    r.el.dataset.estado = col.map(f => f.map(c => c === null ? '-' : c).join('')).join('/');
  });
  r.el.classList.add('cab');
  ui.body.appendChild(r.el);
  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    if (col.some(f => f.includes(null))) { ui.say('Quedan casillas sin pintar: en una placa buena no queda ninguna vacía (carta 45).', 'bad'); return; }
    if (col.every((f, y) => f.every((c, x) => c === D.solucion[y][x]))) {
      resuelto = true;
      ui.say('Los cinco cables unen sus bornes sin cruzarse y la placa se enciende. Dato de la misión: ' + D.dato + '. Coged la carta 30.', 'ok');
    } else ui.say('Hay un cable que no une sus dos bornes, se cruza con otro o sobra una casilla (cartas 41, 43 y 45).', 'bad');
  });
  return { close: ui.close };
}
