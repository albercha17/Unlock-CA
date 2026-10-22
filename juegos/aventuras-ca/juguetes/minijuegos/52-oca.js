// Carta 52 — El juego de la oca de Leo: sesenta casillas con escaleras que suben y toboganes que bajan (tablero en las cartas 54 y 55, dos mitades) y diez
// tiradas de dado de su hermana Marta (carta 59). Hay que decir en qué casilla acaba la ficha (instancias_juguetes.py, OCA). Nota de la nana: O.nota.
import { openGame } from './ui.js';
import { estilo } from './comun.js';

const O = /*DATOS*/{"casillas": 60, "final": 39, "nota": "LA"}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 52 — La oca de Leo', instr: 'Escribid en qué casilla acaba la ficha tras las diez tiradas, empezando fuera del tablero. El tablero está en las cartas 54 y 55 y las tiradas, en la 59.', ...opts });
  estilo('ju-oca', '.oca-t{display:block;text-align:center;font:700 .9rem system-ui,sans-serif;color:#c9d8ff;margin:4px 0}');
  const aviso = document.createElement('div');
  aviso.className = 'oca-t';
  aviso.textContent = 'Casilla final (de 1 a ' + O.casillas + ')';
  const entrada = document.createElement('input');
  entrada.type = 'number';
  entrada.min = '0';
  entrada.max = String(O.casillas);
  entrada.value = '0';
  entrada.className = 'ju-in';
  entrada.setAttribute('aria-label', 'Casilla final');
  entrada.addEventListener('input', () => ui.say(''));
  ui.body.append(aviso, entrada);
  let resuelto = false;
  ui.button('Mover la ficha', 'primary', () => {
    if (resuelto) return;
    const v = Number(entrada.value);
    if (!v) { ui.say('Todavía no habéis escrito ninguna casilla.', 'bad'); return; }
    if (v !== O.final) { ui.say('La ficha de Leo no acaba ahí: seguid las diez tiradas una a una, con las escaleras que suben y los toboganes que bajan.', 'bad'); return; }
    resuelto = true;
    ui.say('La ficha acaba en la casilla ' + O.final + ', y Marta no se lo cree. Debajo del tablero hay una trampilla. Nota de la oca: ' + O.nota + '. Coged la carta 44.', 'ok');
  });
  return { close: ui.close };
}
