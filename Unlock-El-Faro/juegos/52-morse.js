// Carta 52 — Ventana de señales: descifrar un mensaje en morse. Palabra: LLAVE.
import { openGame } from './ui.js';

const WORD = 'LLAVE';
const MORSE = {
  A: '.-', B: '-...', C: '-.-.', D: '-..', E: '.', F: '..-.', G: '--.', H: '....', I: '..',
  J: '.---', K: '-.-', L: '.-..', M: '--', N: '-.', O: '---', P: '.--.', Q: '--.-', R: '.-.',
  S: '...', T: '-', U: '..-', V: '...-', W: '.--', X: '-..-', Y: '-.--', Z: '--..'
};
const sleep = ms => new Promise(r => setTimeout(r, ms));

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 52 — Ventana de señales',
    instr: 'El carguero parpadea un mensaje. Descífralo con la tabla del cuaderno (carta 15).',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .far-lamp{width:84px;height:84px;margin:0 auto 10px;border-radius:50%;background:#1a2430;border:3px solid #3a4a5c;transition:background .05s,box-shadow .05s}
    .far-lamp.on{background:#fff6c8;box-shadow:0 0 40px 14px rgba(255,236,150,.85);border-color:#fff6c8}
    .far-tape{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:1.6rem;letter-spacing:4px;white-space:pre;min-height:2.2rem;color:#ffd27a;margin-bottom:12px}
  `;
  ui.body.appendChild(style);

  const lamp = document.createElement('div');
  lamp.className = 'far-lamp';
  const tape = document.createElement('div');
  tape.className = 'far-tape';
  const display = document.createElement('div');
  display.className = 'far-display';
  const kb = document.createElement('div');
  kb.className = 'far-keyboard';
  ui.body.append(lamp, tape, display, kb);

  let run = 0;
  ui.onClose(() => { run = -1; });

  async function play() {
    const id = ++run;
    tape.textContent = '';
    replay.disabled = true;
    for (const letter of WORD) {
      for (const sym of MORSE[letter]) {
        if (id !== run) return;
        lamp.classList.add('on');
        await sleep(sym === '.' ? 280 : 840);
        lamp.classList.remove('on');
        tape.textContent += sym === '.' ? '·' : '−';
        await sleep(300);
      }
      tape.textContent += '   ';
      await sleep(700);
    }
    if (id === run) replay.disabled = false;
  }

  let entered = '';
  const render = () => { display.textContent = entered === '' ? '—' : entered; };

  'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('').forEach(l => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'far-key';
    b.textContent = l;
    b.addEventListener('click', () => { if (entered.length < WORD.length) { entered += l; render(); } });
    kb.appendChild(b);
  });

  const replay = ui.button('Repetir mensaje', 'ghost', play);
  ui.button('Borrar', 'ghost', () => { entered = entered.slice(0, -1); render(); });
  ui.button('Comprobar', 'primary', () => {
    if (entered === WORD) {
      ui.say('¡Mensaje descifrado: LLAVE! Anselmo la dejó donde él sabía. Mirad la foto del recibidor (carta 29).', 'ok');
      kb.querySelectorAll('button').forEach(b => { b.disabled = true; });
    } else {
      ui.say('Esa palabra no es. Fijaos bien en puntos y rayas.', 'bad');
    }
  });

  render();
  setTimeout(play, 500);
  return { close: ui.close };
}
