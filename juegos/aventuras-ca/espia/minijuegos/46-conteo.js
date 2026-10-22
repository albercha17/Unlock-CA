// Carta 46 — La cuenta del crupier: el crupier reparte veintiocho cartas; cada una suma o resta según su valor (alta-baja). Hay que decir cuál era la cuenta
// al llegar al corte y cuál al final. Las cartas, en las cartas 37 y 39 (primera y segunda parte); la regla, en la 33 (instancias_espia.py, CONTEO).
import { openGame } from './ui.js';
import { contador } from './comun.js';

const D = /*DATOS*/{"corte": 14, "cuenta_corte": -4, "cuenta_final": -3}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 46 — La cuenta del crupier', instr: 'Decid cuánto vale la cuenta tras las primeras cartas y cuánto al final. Las cartas están en la 37 y la 39; la regla de la cuenta, en la 33.', ...opts });
  const a = contador('Cuenta tras las ' + D.corte + ' primeras cartas', -14, 14, 0, 'corte');
  const b = contador('Cuenta tras todas las cartas', -28, 28, 0, 'final');
  ui.body.append(a.el, b.el);
  let resuelto = false;
  ui.button('Cantar la cuenta', 'primary', () => {
    if (resuelto) return;
    if (a.valor() !== D.cuenta_corte) { ui.say('El crupier frunce el ceño: esa no es la cuenta en el corte.', 'bad'); return; }
    if (b.valor() !== D.cuenta_final) { ui.say('La cuenta en el corte es buena, pero la del final no cuadra.', 'bad'); return; }
    resuelto = true;
    ui.say('El crupier sonríe: «cuenta perfecta». Y os desliza la otra mitad de la llave. Coged la carta 56.', 'ok');
  });
  return { close: ui.close };
}
