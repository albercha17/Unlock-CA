// Carta 20 — El cuadro del banquero (Hitori): tachar cifras de un cuadro de 5 x 5 hasta que no quede ninguna repetida en su fila ni en su columna, sin que dos
// tachones se toquen por un lado y con todas las casillas en blanco unidas. Las cifras, en las cartas 19 y 21 (dos mitades); la regla, en la 18.
// Vale cualquier solución (instancias_oeste.py, HITORI, solución única).
import { openGame } from './ui.js';
import { estilo, rejilla } from './comun.js';

const D = /*DATOS*/{"cifras": [[4, 2, 3, 3, 5], [5, 4, 1, 5, 2], [1, 4, 5, 2, 4], [5, 1, 2, 5, 3], [4, 5, 4, 3, 4]], "tachones": [[0, 0, 0, 1, 0], [1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 1, 0], [1, 0, 0, 0, 1]]}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 20 — El cuadro del banquero', instr: 'Tachad cifras tocando las casillas. Las cifras del cuadro y el acertijo del banquero están en las cartas 18, 19 y 21.', ...opts });
  estilo('oe-ban', `.ban .oe-cel{font-size:1.5rem}.ban .oe-cel[data-v="1"]{background:#1e1208;color:#6b4a2a}`);
  const n = D.cifras.length;
  const est = Array.from({ length: n }, () => Array(n).fill(0));
  let resuelto = false;
  const r = rejilla(n, n, (f, c) => { if (resuelto) return; est[f][c] ^= 1; ui.say(''); pintar(); }, 'ban');
  function pintar() {
    for (let f = 0; f < n; f++) for (let c = 0; c < n; c++) {
      const b = r.celda(f, c);
      b.dataset.v = String(est[f][c]);
    }
  }
  // Las cifras no se ven en la app: el cuadro está solo en las cartas. Aquí las casillas son anónimas.
  r.el.setAttribute('aria-label', 'Cuadro de cifras del banco');
  ui.body.appendChild(r.el);
  const pie = document.createElement('div');
  pie.className = 'oe-pie';
  pie.textContent = 'Cuadro de ' + n + ' por ' + n + '. Las cifras, en las cartas.';
  ui.body.appendChild(pie);
  function comprobar() {
    for (let f = 0; f < n; f++) for (let c = 0; c < n; c++) if (est[f][c] && ((f && est[f - 1][c]) || (c && est[f][c - 1]))) return 'Dos tachones se tocan por un lado.';
    for (let f = 0; f < n; f++) {
      const v = new Set();
      for (let c = 0; c < n; c++) if (!est[f][c]) { if (v.has(D.cifras[f][c])) return 'Queda una cifra repetida en una fila.'; v.add(D.cifras[f][c]); }
    }
    for (let c = 0; c < n; c++) {
      const v = new Set();
      for (let f = 0; f < n; f++) if (!est[f][c]) { if (v.has(D.cifras[f][c])) return 'Queda una cifra repetida en una columna.'; v.add(D.cifras[f][c]); }
    }
    const blancas = [];
    for (let f = 0; f < n; f++) for (let c = 0; c < n; c++) if (!est[f][c]) blancas.push(f + ',' + c);
    const vis = new Set([blancas[0]]);
    const pila = [blancas[0]];
    while (pila.length) {
      const [f, c] = pila.pop().split(',').map(Number);
      [[1, 0], [-1, 0], [0, 1], [0, -1]].forEach(([df, dc]) => {
        const k = (f + df) + ',' + (c + dc);
        if (blancas.includes(k) && !vis.has(k)) { vis.add(k); pila.push(k); }
      });
    }
    if (vis.size !== blancas.length) return 'Los tachones parten el cuadro: lo blanco tiene que quedar todo unido.';
    return '';
  }
  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    if (!est.some(f => f.some(v => v))) { ui.say('Todavía no habéis tachado ninguna casilla.', 'bad'); return; }
    const m = comprobar();
    if (m) { ui.say(m, 'bad'); return; }
    resuelto = true;
    ui.say('El cuadro queda limpio de copias y el banquero abre la reja. Coged la carta 28.', 'ok');
  });
  ui.button('Borrar todo', 'ghost', () => { if (!resuelto) { est.forEach(f => f.fill(0)); ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
