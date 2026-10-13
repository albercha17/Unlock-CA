// Carta 52 — Ventana de señales: descifrar un mensaje en morse. Palabra: ANCLA.
import { openGame } from './ui.js';

const WORD = 'ANCLA';
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
    .far-lamp{position:relative;width:170px;height:176px;margin:0 auto 10px;border-radius:50%;background:radial-gradient(circle at 50% 50%,#0f1b28,#050a10 72%);border:1px solid rgba(201,164,90,.4);display:flex;align-items:center;justify-content:center;overflow:visible}
    .far-lamp img{position:absolute;max-width:150px;max-height:158px;object-fit:contain;mix-blend-mode:screen;transition:opacity .04s}
    .far-lamp .enc{opacity:0}
    .far-lamp.on .enc{opacity:1}
    .far-lamp.on{box-shadow:0 0 60px 22px rgba(255,236,150,.55)}
  `;
  ui.body.appendChild(style);

  const lamp = document.createElement('div');
  lamp.className = 'far-lamp';
  lamp.innerHTML = '<img class="apa" alt="" src="./img/ui/morse/linterna-apagada.jpg"><img class="enc" alt="" src="./img/ui/morse/linterna-encendida.jpg">';
  const display = document.createElement('div');
  display.className = 'far-display';
  const kb = document.createElement('div');
  kb.className = 'far-keyboard';
  ui.body.append(lamp, display, kb);

  let run = 0;
  ui.onClose(() => { run = -1; });

  async function play() {
    const id = ++run;
    replay.disabled = true;
    for (const letter of WORD) {
      for (const sym of MORSE[letter]) {
        if (id !== run) return;
        lamp.classList.add('on');
        await sleep(sym === '.' ? 280 : 840);
        lamp.classList.remove('on');
        await sleep(300);
      }
      await sleep(1100);
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
      ui.say('¡Mensaje descifrado! Coged la carta 33.', 'ok');
      kb.querySelectorAll('button').forEach(b => { b.disabled = true; });
    } else {
      ui.say('Esa palabra no es. Volved a mirar los destellos: cortos y largos.', 'bad');
    }
  });

  render();
  setTimeout(play, 500);
  return { close: ui.close };
}
