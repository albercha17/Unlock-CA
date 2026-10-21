// Carta 40 — El nilómetro: decir hasta qué altura subirá la crecida de este año. Las marcas de los cinco años anteriores, en las cartas 41
// y 43; cuánto mide un codo y un palmo, en la 45 (la app no lo dice). Las diferencias suben de dos en dos. Solución: 7 codos y 6 palmos.
import { openGame } from './ui.js';
import { guardarSello, contador } from './nilo.js';

const D = /*DATOS*/{"alturas_palmos": [20, 23, 28, 35, 44], "siguiente_palmos": 55, "solucion": [7, 6]}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 40 — El nilómetro', instr: 'Los sacerdotes necesitan saber a qué altura llegará la crecida de este año para abrir las compuertas. Decidlo en codos y palmos.', ...opts });
  const co = contador('Codos', 15, () => ui.say(''), 'codos');
  const pa = contador('Palmos', 6, () => ui.say(''), 'palmos');
  ui.body.append(co.el, pa.el);
  let resuelto = false;
  ui.button('Avisar a los sacerdotes', 'primary', () => {
    if (resuelto) return;
    if (co.valor() === D.solucion[0] && pa.valor() === D.solucion[1]) {
      resuelto = true; guardarSello('40');
      ui.say('Las compuertas se abren justo a tiempo y el agua llena los canales sin desbordarse. Los sacerdotes os dejan pasar. Coged la carta 30.', 'ok');
    } else ui.say('Con esa altura el agua se desbordaría o no llegaría a los campos. Mirad cómo han ido creciendo los años (cartas 41, 43 y 45).', 'bad');
  });
  return { close: ui.close };
}
