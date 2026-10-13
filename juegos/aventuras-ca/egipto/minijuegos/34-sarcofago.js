// Carta 34 — Sarcófago sellado: teclado de 4 cifras. Código: 2343 (inscripción numérica, carta 46).
import { openGame } from './ui.js';

const CODE = '2343';

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 34 — Sarcófago sellado',
    instr: 'Introduce el número de la inscripción para romper el sello.',
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
      ui.say('El sello se rompe y la tapa se desliza. Dentro hay una cerradura de bronce. Coged la carta 25.', 'ok');
      pad.querySelectorAll('button').forEach(b => { b.disabled = true; });
    } else {
      ui.say('El sello no cede. Contad bien los signos de la inscripción.', 'bad');
      entered = '';
      render();
    }
  }

  render();
  return { close: ui.close };
}
