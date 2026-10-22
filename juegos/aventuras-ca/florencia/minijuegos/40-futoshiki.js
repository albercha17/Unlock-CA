// Carta 40 — El tablero del león (futoshiki): rellenar el cuadrado con los números del 1 al 5 sin repetir en filas ni columnas, respetando los signos
// de desigualdad entre casillas vecinas. El tablero, con sus signos, en las cartas 41 y 43 (dos mitades); el acertijo, en la 45. Solución única
// (instancias_florencia.py, FUTOSHIKI). La app solo enseña el cuadrado vacío.
import { openGame } from './ui.js';
import { estilo, rejilla } from './taller.js';

const D = /*DATOS*/{"n": 5, "solucion": [[3, 5, 4, 1, 2], [4, 2, 1, 5, 3], [1, 3, 5, 2, 4], [2, 1, 3, 4, 5], [5, 4, 2, 3, 1]]}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 40 — El tablero del león', instr: 'Tocad una casilla para cambiar su número (1 a 5, y otra vez vacía). Filas y columnas llevan del 1 al 5 sin repetir y los signos del tablero (cartas 41, 43 y 45) han de cumplirse.', ...opts });
  estilo('fl-fut', `.fut .fl-cel{background:#f6e7bf;font:800 1.4rem Georgia,serif}`);
  const v = Array.from({ length: D.n }, () => Array(D.n).fill(0));
  let resuelto = false;
  const r = rejilla(D.n, (x, y, b) => {
    if (resuelto) return;
    v[y][x] = (v[y][x] + 1) % (D.n + 1); b.textContent = v[y][x] ? String(v[y][x]) : ''; ui.say('');
    r.el.dataset.estado = v.map(f => f.join('')).join('/');
  });
  r.el.classList.add('fut');
  ui.body.appendChild(r.el);
  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    if (v.some(f => f.includes(0))) { ui.say('Quedan casillas vacías.', 'bad'); return; }
    if (v.every((f, y) => f.every((x, i) => x === D.solucion[y][i]))) {
      resuelto = true;
      ui.say('El león abre las fauces con un rugido de engranajes. Coged la carta 30.', 'ok');
    } else ui.say('Algún número se repite o un signo no se cumple (cartas 41, 43 y 45).', 'bad');
  });
  return { close: ui.close };
}
