// Carta 64 — La escalera de caracol (hidato): numerar las casillas del 1 al 25 en un camino sin saltos, de modo que cada número esté pegado al siguiente
// (también en diagonal). Los números que ya están puestos, en las cartas 66 y 67 (dos mitades). Se tocan las casillas en orden: la primera es el 1, la
// segunda el 2... Solución única (instancias_florencia.py, HIDATO).
import { openGame } from './ui.js';
import { estilo, rejilla } from './taller.js';

const D = /*DATOS*/{"n": 5, "camino": [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [1, 4], [2, 4], [3, 4], [4, 4], [4, 3], [4, 2], [4, 1], [4, 0], [3, 0], [3, 1], [2, 1], [2, 0], [1, 0], [1, 1], [1, 2], [2, 2], [3, 2], [3, 3], [2, 3], [1, 3]]}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 64 — La escalera de caracol', instr: 'Tocad las casillas en el orden de los números: la primera que toquéis será el 1, la siguiente el 2, y así hasta el ' + D.n * D.n + '. Los números que ya están puestos, en las cartas 66 y 67.', ...opts });
  estilo('fl-hid', `.hid .fl-cel{background:#e8d3a8;font:800 .95rem system-ui}.hid .fl-cel.puesto{background:#c98a52;color:#fff}`);
  const ruta = [];
  let resuelto = false;
  const r = rejilla(D.n, (x, y) => {
    if (resuelto) return;
    const k = ruta.findIndex(p => p[0] === x && p[1] === y);
    if (k >= 0) { if (k === ruta.length - 1) { ruta.pop(); pintar(); ui.say(''); } return; }
    ruta.push([x, y]); ui.say(''); pintar();
    if (ruta.length === D.n * D.n) {
      if (ruta.every((p, i) => p[0] === D.camino[i][0] && p[1] === D.camino[i][1])) {
        resuelto = true;
        ui.say('Todos los peldaños tienen su número y la escalera de caracol se desenrolla hasta el fondo del sótano. Coged la carta 62.', 'ok');
      } else ui.say('Se han numerado todas las casillas, pero algún número no coincide con los que ya estaban puestos o hay un salto (cartas 66 y 67). Quitad el último o empezad de nuevo.', 'bad');
    }
  });
  r.el.classList.add('hid');
  function pintar() {
    for (let y = 0; y < D.n; y++) for (let x = 0; x < D.n; x++) { const c = r.celda(x, y); c.classList.remove('puesto'); c.textContent = ''; }
    ruta.forEach(([x, y], i) => { const c = r.celda(x, y); c.classList.add('puesto'); c.textContent = String(i + 1); });
    r.el.dataset.ruta = ruta.map(p => p.join(',')).join(';');
  }
  ui.body.appendChild(r.el);
  ui.button('Quitar el último', 'ghost', () => { if (!resuelto && ruta.length) { ruta.pop(); ui.say(''); pintar(); } });
  ui.button('Empezar de nuevo', 'ghost', () => { if (!resuelto) { ruta.length = 0; ui.say(''); pintar(); } });
  return { close: ui.close };
}
