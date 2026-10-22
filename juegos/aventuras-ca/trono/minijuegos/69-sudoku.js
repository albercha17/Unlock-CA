// Carta 69 — El tablero de las seis casas (sudoku de 6 x 6): colocar los seis escudos en cada fila, cada columna y cada recuadro de dos por tres sin repetir.
// El tablero y los escudos ya puestos, en las cartas 70 y 71 (dos mitades). Solución única (instancias_trono.py, SUDOKU).
import { openGame } from './ui.js';
import { estilo, figuraSVG } from './reino.js';

const D = /*DATOS*/{"dados": [[0, 0, 2, 1, 0, 4], [3, 0, 4, 0, 0, 0], [0, 0, 0, 0, 0, 1], [0, 0, 6, 0, 4, 5], [2, 3, 5, 0, 0, 0], [4, 0, 0, 0, 2, 0]], "solucion": [[6, 5, 2, 1, 3, 4], [3, 1, 4, 6, 5, 2], [5, 4, 3, 2, 6, 1], [1, 2, 6, 3, 4, 5], [2, 3, 5, 4, 1, 6], [4, 6, 1, 5, 2, 3]], "casas": ["lobo", "leon", "kraken", "rosa", "sol", "trucha"], "figuras": {"lobo": [{"t": "p", "p": [[18, 74], [24, 20], [42, 42], [58, 42], [76, 20], [82, 74], [62, 92], [38, 92]]}, {"t": "c", "c": [38, 62], "r": 5, "f": "fondo"}, {"t": "c", "c": [62, 62], "r": 5, "f": "fondo"}], "leon": [{"t": "c", "c": [50, 50], "r": 36, "w": 10}, {"t": "c", "c": [50, 50], "r": 22}, {"t": "c", "c": [42, 46], "r": 4, "f": "fondo"}, {"t": "c", "c": [58, 46], "r": 4, "f": "fondo"}], "kraken": [{"t": "p", "p": [[76.0, 38.0], [75.1, 44.2], [72.5, 50.0], [68.4, 55.0], [63.0, 58.8], [56.7, 61.2], [50.0, 62.0], [43.3, 61.2], [37.0, 58.8], [31.6, 55.0], [27.5, 50.0], [24.9, 44.2], [24.0, 38.0], [24.9, 31.8], [27.5, 26.0], [31.6, 21.0], [37.0, 17.2], [43.3, 14.8], [50.0, 14.0], [56.7, 14.8], [63.0, 17.2], [68.4, 21.0], [72.5, 26.0], [75.1, 31.8]]}, {"t": "l", "p": [[28, 54], [18, 78], [28, 92]], "w": 7}, {"t": "l", "p": [[42, 60], [38, 80], [46, 94]], "w": 7}, {"t": "l", "p": [[58, 60], [62, 80], [54, 94]], "w": 7}, {"t": "l", "p": [[72, 54], [82, 78], [72, 92]], "w": 7}, {"t": "c", "c": [42, 36], "r": 4, "f": "fondo"}, {"t": "c", "c": [58, 36], "r": 4, "f": "fondo"}], "rosa": [{"t": "c", "c": [50, 24], "r": 16}, {"t": "c", "c": [24, 44], "r": 16}, {"t": "c", "c": [76, 44], "r": 16}, {"t": "c", "c": [34, 74], "r": 16}, {"t": "c", "c": [66, 74], "r": 16}, {"t": "c", "c": [50, 52], "r": 12, "f": "fondo"}], "sol": [{"t": "c", "c": [50, 50], "r": 22}, {"t": "l", "p": [[80.0, 50.0], [96.0, 50.0]], "w": 7}, {"t": "l", "p": [[71.21320343559643, 71.21320343559643], [82.5269119345812, 82.5269119345812]], "w": 7}, {"t": "l", "p": [[50.0, 80.0], [50.0, 96.0]], "w": 7}, {"t": "l", "p": [[28.786796564403577, 71.21320343559643], [17.473088065418814, 82.5269119345812]], "w": 7}, {"t": "l", "p": [[20.0, 50.00000000000001], [4.0, 50.00000000000001]], "w": 7}, {"t": "l", "p": [[28.78679656440357, 28.786796564403577], [17.473088065418807, 17.473088065418814]], "w": 7}, {"t": "l", "p": [[49.99999999999999, 20.0], [49.99999999999999, 4.0]], "w": 7}, {"t": "l", "p": [[71.21320343559643, 28.78679656440357], [82.52691193458118, 17.473088065418807]], "w": 7}], "trucha": [{"t": "p", "p": [[78.0, 50.0], [76.8, 55.2], [73.4, 60.0], [68.0, 64.1], [61.0, 67.3], [52.8, 69.3], [44.0, 70.0], [35.2, 69.3], [27.0, 67.3], [20.0, 64.1], [14.6, 60.0], [11.2, 55.2], [10.0, 50.0], [11.2, 44.8], [14.6, 40.0], [20.0, 35.9], [27.0, 32.7], [35.2, 30.7], [44.0, 30.0], [52.8, 30.7], [61.0, 32.7], [68.0, 35.9], [73.4, 40.0], [76.8, 44.8]]}, {"t": "p", "p": [[74, 50], [96, 26], [96, 74]]}, {"t": "c", "c": [28, 44], "r": 4, "f": "fondo"}]}}/*FIN*/;
const TONO = ['#8a8a96', '#c89628', '#2f8296', '#b43c50', '#e68220', '#46a0c8'];

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 69 — El tablero de las seis casas', instr: 'Tocad una casilla vacía para cambiar su escudo (los ya puestos no se mueven). Cada fila, cada columna y cada recuadro de dos por tres llevan los seis escudos sin repetir. Los ya puestos, en las cartas 70 y 71.', ...opts });
  estilo('tr-sud', `.sud-t{display:grid;grid-template-columns:repeat(6,1fr);gap:2px;width:min(88vw,330px);margin:10px auto;padding:3px;background:#0c121a;border-radius:8px}.sud-c{aspect-ratio:1;border:0;background:#e6f1fb;padding:2px;cursor:pointer;display:flex;align-items:center;justify-content:center}.sud-c[data-f="1"]{border-bottom:3px solid #0c121a}.sud-c[data-f="3"]{border-bottom:3px solid #0c121a}.sud-c[data-c="2"]{border-right:3px solid #0c121a}`);
  const v = D.dados.map(r => r.slice());
  let resuelto = false;
  const g = document.createElement('div'); g.className = 'sud-t';
  const btn = [];
  for (let f = 0; f < 6; f++) for (let c = 0; c < 6; c++) {
    const b = document.createElement('button'); b.type = 'button'; b.className = 'sud-c'; b.dataset.f = String(f); b.dataset.c = String(c); b.setAttribute('aria-label', 'Casilla ' + (f + 1) + ',' + (c + 1));
    b.addEventListener('click', () => { if (resuelto || D.dados[f][c]) return; v[f][c] = (v[f][c] + 1) % 7; ui.say(''); pintar(); });
    btn.push(b); g.appendChild(b);
  }
  function pintar() {
    btn.forEach((b, i) => {
      const f = Math.floor(i / 6), c = i % 6, x = v[f][c];
      b.innerHTML = '';
      if (x) b.appendChild(figuraSVG(D.figuras[D.casas[x - 1]], TONO[x - 1], '#e6f1fb', 44));
    });
    g.dataset.estado = v.map(r => r.join('')).join('/');
  }
  ui.body.appendChild(g);
  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    if (v.some(r => r.includes(0))) { ui.say('Quedan casillas sin escudo.', 'bad'); return; }
    if (v.every((r, f) => r.every((x, c) => x === D.solucion[f][c]))) {
      resuelto = true;
      ui.say('Los seis escudos quedan en paz en cada fila, columna y recuadro: el tablero se abre y deja ver una escalera. Coged la carta 80.', 'ok');
    } else ui.say('Algún escudo se repite en una fila, columna o recuadro, o no cuadra con los ya puestos (cartas 70 y 71).', 'bad');
  });
  ui.button('Vaciar', 'ghost', () => { if (!resuelto) { v.forEach((r, f) => r.forEach((x, c) => { if (!D.dados[f][c]) v[f][c] = 0; })); ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
