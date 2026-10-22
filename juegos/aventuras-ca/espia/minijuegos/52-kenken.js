// Carta 52 — La caja fuerte del joyero (KenKen 5×5): cifras del 1 al 5 sin repetir en filas ni columnas; cada jaula de trazo grueso lleva un número y una
// operación que han de cumplir sus cifras. El tablero con las jaulas, en las cartas 54 y 55 (dos mitades); la regla, en la 59. Aquí solo se ve la rejilla
// vacía. Vale cualquier relleno correcto (instancias_espia.py, KENKEN, solución única). Pulsaciones: D.pulsa.
import { openGame } from './ui.js';
import { rejilla, teclado } from './comun.js';

const D = /*DATOS*/{"n": 5, "jaulas": [{"celdas": [[2, 2], [2, 1], [3, 1]], "op": "+", "objetivo": 8}, {"celdas": [[3, 0], [2, 0], [4, 0]], "op": "x", "objetivo": 40}, {"celdas": [[0, 0], [1, 0]], "op": "x", "objetivo": 3}, {"celdas": [[4, 4]], "op": "=", "objetivo": 2}, {"celdas": [[3, 2], [3, 3]], "op": "-", "objetivo": 3}, {"celdas": [[0, 4], [0, 3]], "op": "+", "objetivo": 6}, {"celdas": [[4, 3], [4, 2], [4, 1]], "op": "+", "objetivo": 8}, {"celdas": [[3, 4], [2, 4]], "op": "-", "objetivo": 2}, {"celdas": [[0, 1], [0, 2], [1, 2]], "op": "x", "objetivo": 60}, {"celdas": [[2, 3], [1, 3], [1, 4]], "op": "x", "objetivo": 15}, {"celdas": [[1, 1]], "op": "=", "objetivo": 2}], "pulsa": "777"}/*FIN*/;

function cumple(j, v) {
  switch (j.op) {
    case '=': return v[0] === j.objetivo;
    case '+': return v.reduce((a, b) => a + b, 0) === j.objetivo;
    case 'x': return v.reduce((a, b) => a * b, 1) === j.objetivo;
    case '-': return Math.abs(v[0] - v[1]) === j.objetivo;
    case '/': { const a = Math.max(...v), b = Math.min(...v); return a % b === 0 && a / b === j.objetivo; }
    default: return false;
  }
}

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 52 — La caja fuerte del joyero', instr: 'Elegid una casilla y tocad una cifra (1 a 5). Las jaulas están en las cartas 54 y 55; la regla, en la 59.', ...opts });
  const n = D.n;
  const val = {};
  let sel = null, resuelto = false;
  const r = rejilla(n, n, (f, c) => { if (resuelto) return; sel = f + ',' + c; ui.say(''); pintar(); }, 'ken');
  r.el.setAttribute('aria-label', 'Caja fuerte');
  const nums = teclado(1, n, d => {
    if (resuelto) return;
    if (!sel) { ui.say('Elegid primero una casilla.', 'bad'); return; }
    val[sel] = d;
    ui.say('');
    pintar();
  });
  ui.body.append(r.el, nums);
  function pintar() {
    for (let f = 0; f < n; f++) for (let c = 0; c < n; c++) {
      const k = f + ',' + c, b = r.celda(f, c);
      b.classList.toggle('sel', sel === k);
      b.textContent = val[k] ? String(val[k]) : '';
      b.dataset.v = val[k] ? String(val[k]) : '';
    }
  }
  ui.button('Probar la combinación', 'primary', () => {
    if (resuelto) return;
    const g = [];
    for (let f = 0; f < n; f++) {
      g.push([]);
      for (let c = 0; c < n; c++) g[f].push(val[f + ',' + c] || 0);
    }
    if (g.some(f => f.includes(0))) { ui.say('Quedan casillas sin cifra.', 'bad'); return; }
    for (let i = 0; i < n; i++) {
      if (new Set(g[i]).size < n) { ui.say('Hay una fila con una cifra repetida.', 'bad'); return; }
      if (new Set(g.map(f => f[i])).size < n) { ui.say('Hay una columna con una cifra repetida.', 'bad'); return; }
    }
    const malas = D.jaulas.filter(j => !cumple(j, j.celdas.map(([f, c]) => g[f][c]))).length;
    if (malas) { ui.say('La caja no cede: ' + malas + (malas === 1 ? ' jaula no cumple' : ' jaulas no cumplen') + ' su operación.', 'bad'); return; }
    resuelto = true;
    ui.say('Clic: la caja fuerte se abre y dentro hay una llave a medias. Teléfono rojo: pulsad ' + D.pulsa + '. Coged la carta 44.', 'ok');
  });
  ui.button('Borrar la casilla', 'ghost', () => { if (!resuelto && sel) { delete val[sel]; ui.say(''); pintar(); } });
  ui.button('Vaciar', 'ghost', () => { if (!resuelto) { Object.keys(val).forEach(k => delete val[k]); ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
