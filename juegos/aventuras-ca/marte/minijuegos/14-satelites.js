// Carta 14 — La ventana de comunicaciones: decir cuántas horas faltan para que los tres satélites pasen a la vez por la antena. Los pasos de cada
// satélite, dibujados en la carta 16 (la app no los enseña). Solución: 53 horas (instancias_marte.py, SATELITES). Dato de la misión: 3.
import { openGame } from './ui.js';
import { contador } from './cupula.js';

const D = /*DATOS*/{"sats": [{"nombre": "Fobos-1"}, {"nombre": "Deimos-2"}, {"nombre": "Aurora-3"}], "solucion": 53, "dato": 3}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 14 — La ventana de comunicaciones', instr: 'La antena solo puede llamar a la Tierra cuando los tres satélites (' + D.sats.map(s => s.nombre).join(', ') + ') pasan a la vez. Decid dentro de cuántas horas ocurre la primera vez.', ...opts });
  const c = contador('Horas', 99, () => ui.say(''), 'horas');
  ui.body.appendChild(c.el);
  let resuelto = false;
  ui.button('Programar la llamada', 'primary', () => {
    if (resuelto) return;
    const v = c.valor();
    if (v === D.solucion) {
      resuelto = true;
      ui.say('La antena conecta justo cuando pasan los tres: la voz de la doctora Reyes llega entrecortada. Dato de la misión: ' + D.dato + '. Coged la carta 24.', 'ok');
    } else ui.say('A las ' + v + ' horas no coinciden los tres satélites. Mirad los pasos de cada uno (carta 16).', 'bad');
  });
  return { close: ui.close };
}
