// Carta 85 — La puerta de la profecía (metapuzle): la puerta se abre con el número que sale de una cuenta con las «cifras de la profecía» que dejaron
// cuatro puzles al resolverse (cuervos, jarras, piedras y centinelas, en ese orden): primera por segunda, menos la tercera, más la cuarta.
// Los acertijos, en las cartas 86 y 87 (instancias_trono.py, PROFECIA).
import { openGame } from './ui.js';
import { contador } from './reino.js';

const D = /*DATOS*/{"resultado": 43}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 85 — La puerta de la profecía', instr: 'La puerta se abre con un número: el que sale de la cuenta de la profecía con las cuatro cifras que dejaron otros puzles. Los acertijos, en las cartas 86 y 87.', ...opts });
  const c = contador('Número', 99, () => ui.say(''), 'numero');
  ui.body.appendChild(c.el);
  let resuelto = false;
  ui.button('Abrir la puerta', 'primary', () => {
    if (resuelto) return;
    if (c.valor() === D.resultado) {
      resuelto = true;
      ui.say('La puerta de piedra gira sobre sus goznes y deja ver una sala con una luz dorada al fondo. Coged la carta 99.', 'ok');
    } else ui.say('La puerta no se mueve: ese no es el número que sale de la cuenta de la profecía (cartas 86 y 87).', 'bad');
  });
  return { close: ui.close };
}
