// Carta 14 — Puerta de la escalera: teclado de 4 cifras. El reloj del recibidor (carta 16) se paró en las 3:20; lo pusieron en hora a las 12:00 y atrasa
// 20 minutos cada hora: la hora real es la del código (herramientas/instancias_faro.py, puerta).
import { openGame } from './ui.js';

const D = /*DATOS*/{"codigo": "1700", "cifra": 3}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 14 — Puerta de la escalera',
    instr: 'Introducid el código de 4 cifras: la hora real a la que se paró el reloj del recibidor (carta 16), en formato de 24 horas.',
    ...opts
  });

  ui.textura('f36.jpg', { opacidad: 0.5 });
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
    if (entered === D.codigo) {
      ui.say('¡Clac! La cerradura cede y la puerta de la escalera se abre. Cifra de la puerta: ' + D.cifra + '. Coged la carta 24.', 'ok');
      pad.querySelectorAll('button').forEach(b => { b.disabled = true; });
    } else {
      ui.say('Código incorrecto. El reloj atrasa: pensad en la hora real, no en la que marca.', 'bad');
      entered = '';
      render();
    }
  }

  render();
  return { close: ui.close };
}
