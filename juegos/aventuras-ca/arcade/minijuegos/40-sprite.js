// Carta 40 — El sprite comprimido: dibujar en una rejilla de 12 x 12 el sprite que describen las tandas de casillas (cartas 41 y 43, filas 1-6 y 7-12;
// la regla de la compresión, en la 45). Solución única (instancias_arcade.py, SPRITE_D). Byte de la máquina: el de D.dato.
import { openGame } from './ui.js';
import { estilo, rejilla } from './maquina.js';

const D = /*DATOS*/{"pixeles": [[0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0], [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1], [1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1], [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], "dato": 11}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 40 — El sprite comprimido', instr: 'Pintad las casillas de la rejilla para que aparezca el sprite descrito por las tandas de las cartas 41 y 43. Tocad una casilla para encenderla o apagarla.', ...opts });
  estilo('ar-spr', `.spr .ar-cel{background:#1e1040;border:1px solid #2b1860}.spr .ar-cel[data-v="1"]{background:#ffde46;box-shadow:inset 0 0 6px #ff9632}`);
  const F = D.pixeles.length, C = D.pixeles[0].length;
  const est = Array.from({ length: F }, () => Array(C).fill(0));
  let resuelto = false;
  const r = rejilla(C, F, (x, y) => { if (resuelto) return; est[y][x] ^= 1; ui.say(''); pintar(); }, 'spr');
  function pintar() {
    for (let y = 0; y < F; y++) for (let x = 0; x < C; x++) r.celda(x, y).dataset.v = String(est[y][x]);
  }
  r.el.setAttribute('aria-label', 'Rejilla del sprite');
  ui.body.appendChild(r.el);
  const pie = document.createElement('div');
  pie.className = 'ar-pie';
  pie.textContent = 'Doce filas de doce casillas.';
  ui.body.appendChild(pie);
  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    if (!est.some(f => f.some(v => v))) { ui.say('La pantalla sigue en negro: encended alguna casilla.', 'bad'); return; }
    const malas = [];
    for (let y = 0; y < F; y++) if (est[y].some((v, x) => v !== D.pixeles[y][x])) malas.push(y + 1);
    if (malas.length) { ui.say('Hay ' + (malas.length === 1 ? 'una fila' : malas.length + ' filas') + ' que no cuadra con sus tandas (cartas 41 y 43).', 'bad'); return; }
    resuelto = true;
    ui.say('El sprite aparece en la pantalla y la máquina lo reconoce. Byte de la máquina: ' + D.dato + '. Coged la carta 30.', 'ok');
  });
  ui.button('Borrar todo', 'ghost', () => { if (!resuelto) { est.forEach(f => f.fill(0)); ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
