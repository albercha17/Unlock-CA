// Carta 20 — El invernadero: marcar qué plantas estarán vivas mañana (un paso del «juego de la vida»). Cómo está hoy el invernadero, en las cartas 19
// y 21 (dos mitades); las reglas, en la 18. Solución única (instancias_marte.py, VIDA). Dato de la misión: 8.
import { openGame } from './ui.js';
import { estilo, rejilla } from './cupula.js';

const D = /*DATOS*/{"n": 6, "solucion": [[0, 1, 1, 1, 0, 0], [1, 0, 0, 0, 1, 0], [1, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0]], "dato": 8}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 20 — El invernadero', instr: 'Marcad las casillas donde habrá una planta viva MAÑANA, aplicando las reglas del invernadero a cómo está hoy (cartas 18, 19 y 21).', ...opts });
  estilo('mr-inv', `.inv .mr-cel{background:#5a4034}.inv .mr-cel.viva{background:radial-gradient(circle,#7be49a 35%,#2f7a46 40%,#5a4034 42%)}`);
  const viva = Array.from({ length: D.n }, () => Array(D.n).fill(0));
  let resuelto = false;
  const r = rejilla(D.n, (x, y, b) => {
    if (resuelto) return;
    viva[y][x] ^= 1; b.classList.toggle('viva', !!viva[y][x]); ui.say('');
    r.el.dataset.estado = viva.map(f => f.join('')).join('/');
  });
  r.el.classList.add('inv');
  ui.body.appendChild(r.el);
  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    const mal = D.solucion.reduce((s, f, y) => s + f.filter((v, x) => v !== viva[y][x]).length, 0);
    if (!mal) {
      resuelto = true;
      ui.say('El invernadero amanece justo como decían las reglas y la puerta del módulo se abre. Dato de la misión: ' + D.dato + '. Coged la carta 28.', 'ok');
    } else ui.say('Alguna casilla no sale como dicen las reglas: repasad cada planta con sus ocho vecinas (cartas 18, 19 y 21).', 'bad');
  });
  ui.button('Vaciar', 'ghost', () => { if (!resuelto) { viva.forEach(f => f.fill(0)); r.el.querySelectorAll('.mr-cel').forEach(b => b.classList.remove('viva')); ui.say(''); } });
  return { close: ui.close };
}
