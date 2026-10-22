// Carta 14 — La bitácora: tres anotaciones de a bordo dicen cuántas campanadas sonaron en qué guardia (carta 16). Hay que decir cuánto tiempo pasó entre el
// aviso 1 y el aviso 3 (instancias_piratas.py, BITACORA). Distancia de la bitácora: D.distancia.
import { openGame } from './ui.js';
import { contador } from './comun.js';

const D = /*DATOS*/{"entre_horas": 8, "entre_min": 30, "distancia": 3}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 14 — La bitácora', instr: 'Decid cuánto tiempo pasó entre el aviso 1 y el aviso 3 de la bitácora, en horas y minutos. La bitácora está en la carta 16.', ...opts });
  const horas = contador('Horas', 0, 23, 0, 'horas');
  const minutos = contador('Minutos', 0, 45, 0, 'minutos', 15);
  ui.body.append(horas.el, minutos.el);
  let resuelto = false;
  ui.button('Anotar en el cuaderno', 'primary', () => {
    if (resuelto) return;
    if (horas.valor() !== D.entre_horas || minutos.valor() !== D.entre_min) {
      ui.say('La capitana Bruma cuenta con los dedos y niega con la cabeza: ese no es el tiempo entre los dos avisos.', 'bad');
      return;
    }
    resuelto = true;
    ui.say(D.entre_horas + ' horas' + (D.entre_min ? ' y ' + D.entre_min + ' minutos' : '') + ': la capitana asiente. Distancia de la bitácora: ' + D.distancia + (D.distancia === 1 ? ' casilla' : ' casillas') + '. Coged la carta 24.', 'ok');
  });
  return { close: ui.close };
}
