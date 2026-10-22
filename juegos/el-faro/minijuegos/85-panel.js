// Carta 85 — Panel de arranque: combinación de cinco cifras. Cinco puzles dejaron una cifra cada uno («Cifra de la puerta: …»); el orden de arranque está en la carta 86
// y las válvulas por las que pasa cada cifra, en la 87 (herramientas/instancias_faro.py, meta).
import { openGame } from './ui.js';

const D = /*DATOS*/{"codigo": "17958"}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 85 — Panel de arranque',
    instr: 'Introducid la combinación de cinco cifras: las cifras que dejaron cinco puzles, en el orden de arranque (carta 86) y pasadas por las válvulas (carta 87).',
    ...opts
  });

  ui.textura('f36.jpg', { opacidad: 0.5 });
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
      ui.say('¡Clac, clac, clac! El generador ruge, la lámpara prende y la lente empieza a girar con el haz de Cabo Niebla. Coged la carta 99.', 'ok');
      pad.querySelectorAll('button').forEach(b => { b.disabled = true; });
    } else {
      ui.say('El panel zumba y se apaga: esa no es la combinación. Repasad las cifras, su orden y las válvulas.', 'bad');
      entered = '';
      render();
    }
  }

  render();
  return { close: ui.close };
}
