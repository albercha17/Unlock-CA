// Carta 64 — Los paneles de refrigeración (Lights Out): encender el patrón de las cartas 66 y 67 (dos mitades) sabiendo que cada panel que se toca
// cambia él y sus cuatro vecinos en cruz. Se empieza con todos apagados. Vale cualquier combinación de toques (instancias_marte.py, PANELES).
import { openGame } from './ui.js';
import { estilo, rejilla } from './cupula.js';

const D = /*DATOS*/{"n": 5, "objetivo": [[0, 1, 1, 0, 1], [0, 0, 0, 1, 0], [1, 1, 1, 1, 0], [1, 0, 0, 1, 0], [0, 0, 0, 0, 1]]}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 64 — Los paneles de refrigeración', instr: 'Tocad paneles hasta que queden encendidos exactamente los del patrón (cartas 66 y 67). Cada toque cambia el panel y sus cuatro vecinos en cruz.', ...opts });
  estilo('mr-pan', `.pan .mr-cel{background:#4a5260}.pan .mr-cel.on{background:radial-gradient(circle,#b8f4ff 35%,#28a0b8 60%,#4a5260 62%)}`);
  const g = Array.from({ length: D.n }, () => Array(D.n).fill(0));
  let resuelto = false, toques = 0;
  const r = rejilla(D.n, (x, y) => {
    if (resuelto) return;
    [[0, 0], [1, 0], [-1, 0], [0, 1], [0, -1]].forEach(([dx, dy]) => {
      const a = x + dx, b = y + dy;
      if (a >= 0 && b >= 0 && a < D.n && b < D.n) g[b][a] ^= 1;
    });
    toques++; ui.say(''); pintar();
    if (g.every((f, j) => f.every((v, i) => v === D.objetivo[j][i]))) {
      resuelto = true;
      ui.say('¡El patrón es idéntico! Los paneles se iluminan y el reactor empieza a enfriarse. Coged la carta 62.', 'ok');
    }
  });
  r.el.classList.add('pan');
  ui.body.appendChild(r.el);
  function pintar() {
    for (let y = 0; y < D.n; y++) for (let x = 0; x < D.n; x++) r.celda(x, y).classList.toggle('on', !!g[y][x]);
    r.el.dataset.estado = g.map(f => f.join('')).join('/');
  }
  ui.button('Apagar todos', 'ghost', () => { if (!resuelto) { g.forEach(f => f.fill(0)); toques = 0; ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
