// Carta 52 — La paleta de Leonardo: decir cuántas cucharadas de cada pigmento hay que echar para obtener el color del maestro. Lo que lleva cada pigmento,
// en la carta 54; el color que se quiere, en la 55; el acertijo, en la 59. Solución única (instancias_florencia.py, PIGMENTOS). Letra de la clave: S.
import { openGame } from './ui.js';
import { contador } from './taller.js';

const D = /*DATOS*/{"pigmentos": [[2, 1, 0], [1, 3, 1], [0, 1, 3]], "solucion": [3, 2, 4], "letra": "S"}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 52 — La paleta de Leonardo', instr: 'Decid cuántas cucharadas de cada pigmento mezclar para conseguir el color del maestro (cartas 54, 55 y 59).', ...opts });
  const cs = D.pigmentos.map((_, j) => {
    const c = contador('Pigmento ' + ['I', 'II', 'III'][j], 12, () => ui.say(''), 'p' + j);
    ui.body.appendChild(c.el);
    return c;
  });
  let resuelto = false;
  ui.button('Mezclar', 'primary', () => {
    if (resuelto) return;
    const v = cs.map(c => c.valor());
    if (v.every((x, j) => x === D.solucion[j])) {
      resuelto = true;
      ui.say('La mezcla sale exactamente del color del maestro y se seca al instante, brillante. Letra de la clave: ' + D.letra + '. Coged la carta 44.', 'ok');
    } else ui.say('Ese no es el color: las gotas de rojo, de amarillo y de azul no suman lo que pide Leonardo (cartas 54, 55 y 59).', 'bad');
  });
  return { close: ui.close };
}
