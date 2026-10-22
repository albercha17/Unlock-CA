// Carta 20 — Los centinelas de la muralla (problema de las ocho damas): ocho centinelas en una muralla de 8 x 8 sin que ninguno vea a otro por fila,
// columna o diagonal. Los tres que ya están puestos, en la muralla de las cartas 19 y 21 (dos mitades); el acertijo, en la 18.
// Solución única (instancias_trono.py, CENTINELAS). Cifra de la profecía: 4.
import { openGame } from './ui.js';
import { estilo, rejilla } from './reino.js';

const D = /*DATOS*/{"n": 8, "fijas": [[4, 0], [1, 1], [0, 7]], "solucion": [[4, 0], [1, 1], [3, 2], [6, 3], [2, 4], [7, 5], [5, 6], [0, 7]], "dato": 4}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 20 — Los centinelas de la muralla', instr: 'Tocad las casillas donde colocáis un centinela (otra vez para quitarlo). Son ocho y ninguno puede ver a otro. Los tres ya puestos, en las cartas 19, 21 y 18.', ...opts });
  estilo('tr-cen', `.cen .tr-cel{background:#9fb6c9;font-size:1.1rem}.cen .tr-cel.on{background:radial-gradient(circle,#b05050 40%,#9fb6c9 42%)}`);
  const on = new Set();
  let resuelto = false;
  const r = rejilla(D.n, (x, y, b) => {
    if (resuelto) return;
    const k = x + ',' + y;
    on.has(k) ? on.delete(k) : on.add(k);
    b.classList.toggle('on', on.has(k)); ui.say('');
    r.el.dataset.centinelas = [...on].sort().join(';');
  }, true);
  r.el.classList.add('cen');
  ui.body.appendChild(r.el);
  ui.button('Dar el relevo', 'primary', () => {
    if (resuelto) return;
    if (on.size !== D.n) { ui.say('Hacen falta ' + D.n + ' centinelas y habéis puesto ' + on.size + '.', 'bad'); return; }
    const p = [...on].map(k => k.split(',').map(Number));
    const ve = p.some((a, i) => p.some((b, j) => i < j && (a[0] === b[0] || a[1] === b[1] || Math.abs(a[0] - b[0]) === Math.abs(a[1] - b[1]))));
    if (ve) { ui.say('Hay dos centinelas que se ven: están en la misma fila, columna o diagonal (carta 18).', 'bad'); return; }
    const sol = new Set(D.solucion.map(([x, y]) => x + ',' + y));
    if ([...on].every(k => sol.has(k))) {
      resuelto = true;
      ui.say('Ningún centinela ve a otro y los tres que ya estaban siguen en su sitio: la guardia queda perfecta. Cifra de la profecía: ' + D.dato + '. Coged la carta 28.', 'ok');
    } else ui.say('Ninguno ve a otro, pero no es la disposición que cuadra con los tres centinelas que ya había (cartas 19 y 21).', 'bad');
  });
  return { close: ui.close };
}
