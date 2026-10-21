// Carta 48 — El campo de rocas (buscaminas): marcar las rocas ocultas con los números del radar (cartas 42 y 49, dos mitades; el aviso, en la 53).
// En la app todas las casillas parecen iguales: las pistas no están. Solución única (instancias_marte.py, ROCAS).
import { openGame } from './ui.js';
import { estilo, rejilla } from './cupula.js';

const D = /*DATOS*/{"n": 8, "solucion": [[3, 0], [5, 0], [6, 0], [1, 1], [3, 1], [6, 1], [5, 2], [0, 3], [1, 3], [0, 6], [1, 6]]}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 48 — El campo de rocas', instr: 'El rover no puede pisar una roca. Tocad las casillas donde creéis que hay una roca escondida (otra vez para quitar la marca). El radar, en las cartas 42, 49 y 53.', ...opts });
  estilo('mr-roc', `.roc .mr-cel{background:#9a7a64}.roc .mr-cel.roca{background:radial-gradient(circle,#4a4a50 40%,#2a2a30 70%)}`);
  const marcas = new Set();
  let resuelto = false;
  const r = rejilla(D.n, (x, y, b) => {
    if (resuelto) return;
    const k = x + ',' + y;
    marcas.has(k) ? marcas.delete(k) : marcas.add(k);
    b.classList.toggle('roca', marcas.has(k)); ui.say('');
    r.el.dataset.rocas = [...marcas].sort().join(';');
  }, true);
  r.el.classList.add('roc');
  ui.body.appendChild(r.el);
  ui.button('Mandar al rover', 'primary', () => {
    if (resuelto) return;
    const sol = new Set(D.solucion.map(([x, y]) => x + ',' + y));
    if (marcas.size === sol.size && [...marcas].every(k => sol.has(k))) {
      resuelto = true;
      ui.say('El rover cruza el campo sin tocar una sola roca y llega al anexo. Coged la carta 36.', 'ok');
    } else ui.say('El rover se atasca contra una roca que no estaba marcada, o rodea una casilla despejada. Repasad los números (cartas 42, 49 y 53).', 'bad');
  });
  return { close: ui.close };
}
