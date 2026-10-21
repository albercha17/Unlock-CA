// Carta 64 — El tapiz del sigilo (nonograma de 8 x 8): pintar las casillas del tapiz que dibujan el sigilo del dragón. Las pistas de cada fila,
// en la carta 66; las de cada columna, en la 67 (la app no las enseña). Solución única (instancias_trono.py, TAPIZ).
import { openGame } from './ui.js';
import { estilo, rejilla } from './reino.js';

const D = /*DATOS*/{"solucion": [[0, 0, 0, 0, 0, 0, 1, 1], [0, 0, 0, 1, 1, 1, 1, 0], [1, 1, 1, 0, 0, 1, 0, 1], [0, 1, 1, 0, 1, 1, 0, 0], [1, 0, 1, 0, 1, 0, 0, 0], [0, 1, 1, 1, 1, 1, 1, 0], [1, 0, 1, 1, 0, 1, 1, 1], [0, 1, 0, 1, 0, 0, 1, 0]]}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 64 — El tapiz del sigilo', instr: 'Tocad las casillas que van pintadas (otra vez para borrar). Cada número de las cartas 66 (filas) y 67 (columnas) dice cuántas casillas seguidas se pintan; entre grupos hay al menos un hueco.', ...opts });
  estilo('tr-tap', `.tap .tr-cel{background:#c9d6e2}.tap .tr-cel.on{background:#2c3a4a}`);
  const g = Array.from({ length: D.solucion.length }, () => Array(D.solucion.length).fill(0));
  let resuelto = false;
  const r = rejilla(D.solucion.length, (x, y, b) => {
    if (resuelto) return;
    g[y][x] ^= 1; b.classList.toggle('on', !!g[y][x]); ui.say('');
    r.el.dataset.estado = g.map(f => f.join('')).join('/');
  }, true);
  r.el.classList.add('tap');
  ui.body.appendChild(r.el);
  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    if (g.every((f, y) => f.every((v, x) => v === D.solucion[y][x]))) {
      resuelto = true;
      ui.say('El sigilo del dragón aparece entero en el tapiz y la pared se abre con un temblor. Coged la carta 62.', 'ok');
    } else ui.say('Hay filas o columnas que no cuadran con sus números (cartas 66 y 67).', 'bad');
  });
  ui.button('Borrar todo', 'ghost', () => { if (!resuelto) { g.forEach(f => f.fill(0)); r.el.querySelectorAll('.tr-cel').forEach(b => b.classList.remove('on')); ui.say(''); } });
  return { close: ui.close };
}
