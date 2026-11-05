// Carta 14 — La vitrina del cristal: candado de tres cifras. El código es cuántos engranajes rojos, azules y amarillos hay en la pizarra de Alberto
// (herramientas/instancias_cronoportal.py, cerradura). Es la primera app que se juega: enseña el botón Acción y las cifras que dejan los puzles.
import { openGame } from './ui.js';

const D = /*DATOS*/{"codigo": "352", "cifra": 4}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 14 — La vitrina del cristal',
    instr: 'El candado tiene tres ruedas: una cifra por cada color de engranaje de la pizarra, en el orden rojo, azul, amarillo.',
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
      ui.say('¡Clic! El candado se abre y la vitrina se levanta. Cifra de la vitrina: ' + D.cifra + ' (apuntadla, la necesitaréis). Coged la carta 24.', 'ok');
      pad.querySelectorAll('button').forEach(b => { b.disabled = true; });
    } else if (entered.length < n) {
      ui.say('El candado tiene ' + n + ' ruedas: una por color.', 'bad');
    } else {
      ui.say('El candado no se abre. Contad otra vez los engranajes de cada color.', 'bad');
      entered = '';
      render();
    }
  }

  render();
  return { close: ui.close };
}
