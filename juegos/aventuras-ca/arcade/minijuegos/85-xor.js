// Carta 85 — El arranque de la máquina: la clave es la «o exclusiva» (XOR) de los cuatro bytes que dejaron los puzles del circuito, los fantasmas, el
// sprite y la rana. Se anotan los cuatro bytes (0 a 15) y se escribe la clave. Las reglas, en las cartas 86 y 87. La app solo comprueba que los cuatro
// bytes son los de la máquina (en cualquier orden) y que la clave es su XOR (instancias_arcade.py, XOR).
import { openGame } from './ui.js';
import { contador } from './maquina.js';

const D = /*DATOS*/{"bytes": [6, 9, 11, 12], "resultado": 8}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 85 — El arranque de la máquina', instr: 'Apuntad los cuatro bytes que dejaron el circuito, los fantasmas, el sprite y la rana, y la clave que sale de aplicarles la «o exclusiva». Las reglas están en las cartas 86 y 87.', ...opts });
  let resuelto = false;
  const nombres = ['Byte del circuito', 'Byte de los fantasmas', 'Byte del sprite', 'Byte de la rana'];
  const b = nombres.map((n, i) => contador(n, 15, () => ui.say(''), 'b' + i));
  const clave = contador('CLAVE', 15, () => ui.say(''), 'clave');
  b.forEach(c => ui.body.appendChild(c.el));
  const sep = document.createElement('div');
  sep.className = 'ar-pie';
  sep.textContent = '— clave de arranque —';
  ui.body.append(sep, clave.el);
  ui.button('Arrancar', 'primary', () => {
    if (resuelto) return;
    const dados = b.map(c => c.valor()).sort((x, y) => x - y);
    const ref = D.bytes.slice().sort((x, y) => x - y);
    if (dados.some((v, i) => v !== ref[i])) { ui.say('Alguno de los cuatro bytes no es el que dejó su puzle: la máquina no los reconoce.', 'bad'); return; }
    const xor = dados.reduce((x, y) => x ^ y, 0);
    if (clave.valor() !== xor) { ui.say('Los bytes están bien, pero la clave no sale de aplicarles la «o exclusiva» (cartas 86 y 87).', 'bad'); return; }
    resuelto = true;
    ui.say('La máquina arranca con un chasquido y la pantalla se enciende: la última moneda cae. Coged la carta 99.', 'ok');
  });
  return { close: ui.close };
}
