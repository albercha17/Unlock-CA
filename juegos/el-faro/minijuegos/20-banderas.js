// Carta 20 — El armario de banderas: deletrear con el teclado las seis letras del mensaje de banderas (carta 18) con la tabla de las cartas 19 y 21.
import { openGame } from './ui.js';
import { estilo } from './comun.js';

const D = /*DATOS*/{"palabra": "NIEBLA", "cifra": 1}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 20 — El armario de banderas',
    instr: 'Escribid la palabra que deletrean las banderas del mensaje (carta 18). La tabla de banderas está en las cartas 19 y 21.',
    ...opts
  });
  estilo('fa-ban', '.fa-ban-d{letter-spacing:4px}');

  const display = document.createElement('div');
  display.className = 'far-display fa-ban-d';
  const kb = document.createElement('div');
  kb.className = 'far-keyboard';
  ui.body.append(display, kb);

  let entered = '';
  const render = () => { display.textContent = entered === '' ? '—' : entered; };

  'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('').forEach(l => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'far-key';
    b.textContent = l;
    b.addEventListener('click', () => { if (entered.length < D.palabra.length) { entered += l; render(); } });
    kb.appendChild(b);
  });

  ui.button('Borrar', 'ghost', () => { entered = entered.slice(0, -1); render(); });
  ui.button('Comprobar', 'primary', () => {
    if (entered === D.palabra) {
      ui.say('¡Mensaje descifrado! El armario se abre y, detrás de las banderas, asoma algo de cuero. Cifra de las banderas: ' + D.cifra + '. Coged la carta 28.', 'ok');
      kb.querySelectorAll('button').forEach(b => { b.disabled = true; });
    } else if (entered.length < D.palabra.length) {
      ui.say('El mensaje tiene ' + D.palabra.length + ' letras: una por bandera.', 'bad');
    } else {
      ui.say('Esa palabra no es. Mirad bien los colores y los dibujos: hay banderas casi gemelas.', 'bad');
    }
  });

  render();
  return { close: ui.close };
}
