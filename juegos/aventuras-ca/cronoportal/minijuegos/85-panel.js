// Carta 85 — El panel de vuelta: dos cifras, las que dejaron el plano y la vitrina, en el orden que dice la nota de Alberto (carta 86). Enseña a apuntar las cifras.
import { openGame } from './ui.js';

const D = /*DATOS*/{"codigo": "74"}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 85 — El panel de vuelta',
    instr: 'Marcad las dos cifras que dejaron los puzles que ya habéis resuelto, en el orden que dice la nota de Alberto.',
    ...opts
  });
  const display = document.createElement('div');
  display.className = 'far-display';
  const pad = document.createElement('div');
  pad.className = 'far-keypad';
  ui.body.append(display, pad);

  let entered = '';
  const n = D.codigo.length;
  const render = () => { display.textContent = entered.padEnd(n, '·').split('').join(' '); };

  ['1', '2', '3', '4', '5', '6', '7', '8', '9', '⌫', '0', '✓'].forEach(k => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'far-key';
    b.textContent = k;
    b.addEventListener('click', () => {
      if (k === '⌫') { entered = entered.slice(0, -1); render(); return; }
      if (k === '✓') { check(); return; }
      if (entered.length < n) { entered += k; render(); }
    });
    pad.appendChild(b);
  });

  function check() {
    if (entered === D.codigo) {
      ui.say('¡El panel parpadea en verde y el anillo del portal se abre otra vez! Coged la carta 99.', 'ok');
      pad.querySelectorAll('button').forEach(b => { b.disabled = true; });
    } else {
      ui.say('El panel zumba y se apaga. Revisad las cifras que apuntasteis y su orden.', 'bad');
      entered = '';
      render();
    }
  }

  render();
  return { close: ui.close };
}
