// Carta 72 — El reparto de tierras (Shikaku): dividir el campo en parcelas rectangulares de modo que cada una lleve un solo número y tenga
// tantas casillas como dice. Los números, en las cartas 75 y 79 (las dos mitades del campo); la app solo enseña el campo vacío.
// Para marcar una parcela se tocan dos esquinas opuestas; tocar una parcela ya hecha la borra. Solución única (instancias_egipto.py, TIERRAS).
import { openGame } from './ui.js';
import { estilo, rejilla, guardarSello } from './nilo.js';

const D = /*DATOS*/{"n": 8, "solucion": [[0, 0, 2, 4], [2, 0, 3, 1], [5, 0, 1, 2], [6, 0, 2, 4], [2, 1, 1, 3], [3, 1, 2, 2], [5, 2, 1, 2], [3, 3, 2, 1], [0, 4, 2, 4], [2, 4, 4, 2], [6, 4, 1, 2], [7, 4, 1, 4], [2, 6, 1, 2], [3, 6, 4, 2]]}/*FIN*/;
const TONOS = ['#e8b86a', '#8fc9c9', '#c9a0d8', '#a8d890', '#e8908a', '#9ab0e8', '#e8d870'];

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 72 — El reparto de tierras', instr: 'Marcad cada parcela tocando dos esquinas opuestas. Cada parcela es un rectángulo con un solo número y tantas casillas como ese número. Tocad una parcela ya marcada para borrarla.', ...opts });
  estilo('eg-tie', `.tie .eg-cel{background:#e6d6a0}`);
  const rects = [];
  let esquina = null, resuelto = false;
  const r = rejilla(D.n, (x, y) => {
    if (resuelto) return;
    if (!esquina) {
      const i = rects.findIndex(q => x >= q[0] && x < q[0] + q[2] && y >= q[1] && y < q[1] + q[3]);
      if (i >= 0) { rects.splice(i, 1); ui.say(''); pintar(); return; }
      esquina = [x, y]; pintar(); return;
    }
    const x0 = Math.min(x, esquina[0]), y0 = Math.min(y, esquina[1]);
    const w = Math.abs(x - esquina[0]) + 1, h = Math.abs(y - esquina[1]) + 1;
    esquina = null;
    if (rects.some(q => x0 < q[0] + q[2] && q[0] < x0 + w && y0 < q[1] + q[3] && q[1] < y0 + h)) { ui.say('Esa parcela pisa a otra ya marcada.', 'bad'); pintar(); return; }
    rects.push([x0, y0, w, h]); ui.say(''); pintar();
  }, false);
  r.el.classList.add('tie');
  ui.body.appendChild(r.el);
  function pintar() {
    for (let y = 0; y < D.n; y++) for (let x = 0; x < D.n; x++) {
      const c = r.celda(x, y);
      const i = rects.findIndex(q => x >= q[0] && x < q[0] + q[2] && y >= q[1] && y < q[1] + q[3]);
      c.style.background = i >= 0 ? TONOS[i % TONOS.length] : (esquina && esquina[0] === x && esquina[1] === y ? '#fff' : '');
    }
    r.el.dataset.rects = rects.map(q => q.join(':')).join(',');
  }
  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    const casillas = rects.reduce((s, q) => s + q[2] * q[3], 0);
    if (casillas < D.n * D.n) { ui.say('Quedan ' + (D.n * D.n - casillas) + ' casillas sin repartir.', 'bad'); return; }
    const k = q => q.join(':');
    const sol = new Set(D.solucion.map(k));
    if (rects.length === sol.size && rects.every(q => sol.has(k(q)))) {
      resuelto = true; guardarSello('72');
      ui.say('Cada parcela encaja con su número y los campesinos aplauden: el reparto es justo. Coged la carta 82.', 'ok');
    } else ui.say('Todo el campo está repartido, pero alguna parcela no cuadra con sus números (cartas 75 y 79).', 'bad');
  });
  ui.button('Borrar todo', 'ghost', () => { if (!resuelto) { rects.length = 0; esquina = null; ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
