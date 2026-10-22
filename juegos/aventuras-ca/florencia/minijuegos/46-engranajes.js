// Carta 46 — El reloj del taller: decir cuántas vueltas da la rueda D y hacia qué lado gira cuando la rueda A da las vueltas de la manivela. El tren de
// ruedas, en la carta 37; la manivela, en la 39; el acertijo, en la 33. Solución: 2 vueltas hacia la derecha (instancias_florencia.py, ENGRANAJES).
import { openGame } from './ui.js';
import { estilo, contador } from './taller.js';

const D = /*DATOS*/{"solucion": {"vueltas": 2, "sentido": "derecha"}}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 46 — El reloj del taller', instr: 'Se gira la manivela de la rueda A. Decid cuántas vueltas da la rueda D y hacia qué lado gira. El tren de ruedas, en las cartas 37, 39 y 33.', ...opts });
  estilo('fl-eng', `.eng-lados{display:flex;gap:10px;justify-content:center;margin:10px 0}.eng-lados button{padding:9px 16px;border-radius:10px;border:2px solid #d9a441;background:#4d3c20;color:#f6e7bf;font:700 .9rem system-ui;cursor:pointer}.eng-lados button.sel{background:#d9a441;color:#2a1f0c}`);
  const c = contador('Vueltas de D', 30, () => ui.say(''), 'vueltas');
  const l = document.createElement('div'); l.className = 'eng-lados';
  let lado = null, resuelto = false;
  ['derecha', 'izquierda'].forEach(k => {
    const b = document.createElement('button'); b.type = 'button'; b.dataset.l = k; b.textContent = k === 'derecha' ? '↻ A la derecha' : '↺ A la izquierda';
    b.addEventListener('click', () => { if (!resuelto) { lado = k; l.querySelectorAll('button').forEach(x => x.classList.toggle('sel', x === b)); ui.say(''); } });
    l.appendChild(b);
  });
  ui.body.append(c.el, l);
  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    if (!lado) { ui.say('Decid también hacia qué lado gira la rueda D.', 'bad'); return; }
    if (c.valor() === D.solucion.vueltas && lado === D.solucion.sentido) {
      resuelto = true;
      ui.say('El reloj marca la hora exacta y el panel de la pared se desliza. Coged la carta 56.', 'ok');
    } else if (c.valor() === D.solucion.vueltas) ui.say('Las vueltas están bien, pero la rueda D gira hacia el otro lado (carta 33).', 'bad');
    else ui.say('El reloj se atasca: las vueltas de D no son esas (cartas 37, 39 y 33).', 'bad');
  });
  return { close: ui.close };
}
