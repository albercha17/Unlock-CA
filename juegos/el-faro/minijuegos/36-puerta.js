// Carta 36 — Puerta de la escalera: teclado de 4 cifras. Código: 0435 (3:15 + 1 h 20 min).
import { openGame } from './ui.js';

const CODE = '0435';

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 36 — Puerta de la escalera',
    instr: 'Introduce el código de 4 cifras.',
    ...opts
  });

  const display = document.createElement('div');
  display.className = 'far-display';
  const pad = document.createElement('div');
  pad.className = 'far-keypad';
  ui.body.append(display, pad);

  let entered = '';
  const render = () => { display.textContent = entered.padEnd(4, '·').split('').join(' '); };

  ['1', '2', '3', '4', '5', '6', '7', '8', '9', '⌫', '0', '✓'].forEach(k => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'far-key';
    b.textContent = k;
    b.addEventListener('click', () => {
      if (k === '⌫') { entered = entered.slice(0, -1); render(); return; }
      if (k === '✓') { check(); return; }
      if (entered.length < 4) { entered += k; render(); }
    });
    pad.appendChild(b);
  });

  function check() {
    if (entered === CODE) {
      ui.say('¡Clac! La cerradura cede. Coged la carta 40.', 'ok');
      pad.querySelectorAll('button').forEach(b => { b.disabled = true; });
    } else {
      ui.say('Código incorrecto. Pensad en la hora real.', 'bad');
      entered = '';
      render();
    }
  }

  render();
  return { close: ui.close };
}
