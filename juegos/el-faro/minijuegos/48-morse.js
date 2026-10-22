// Carta 48 — La ventana de señales: el carguero transmite una palabra en morse con una lámpara blanca, pero su sirena averiada mete destellos ROJOS que no son
// letras (carta 53). La tabla morse está en las cartas 42 y 49 (herramientas/instancias_faro.py, morse).
import { openGame } from './ui.js';

const D = /*DATOS*/{"palabra": "BALIZA", "letras": [[{"c": "r", "s": "-"}, {"c": "b", "s": "-"}, {"c": "b", "s": "."}, {"c": "b", "s": "."}, {"c": "r", "s": "."}, {"c": "b", "s": "."}], [{"c": "b", "s": "."}, {"c": "b", "s": "-"}], [{"c": "b", "s": "."}, {"c": "b", "s": "-"}, {"c": "r", "s": "."}, {"c": "b", "s": "."}, {"c": "b", "s": "."}], [{"c": "b", "s": "."}, {"c": "b", "s": "."}], [{"c": "b", "s": "-"}, {"c": "b", "s": "-"}, {"c": "b", "s": "."}, {"c": "r", "s": "."}, {"c": "b", "s": "."}], [{"c": "b", "s": "."}, {"c": "b", "s": "-"}]], "cifra": 8}/*FIN*/;
const sleep = ms => new Promise(r => setTimeout(r, ms));

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 48 — La ventana de señales',
    instr: 'El carguero parpadea un mensaje. Escribid la palabra que transmite con la tabla morse (cartas 42 y 49). Leed el aviso de la carta 53.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .far-lamp{position:relative;width:170px;height:176px;margin:0 auto 10px;border-radius:50%;background:radial-gradient(circle at 50% 50%,#0f1b28,#050a10 72%);border:1px solid rgba(201,164,90,.4);display:flex;align-items:center;justify-content:center}
    .far-lamp img{position:absolute;max-width:150px;max-height:158px;object-fit:contain;mix-blend-mode:screen;transition:opacity .04s}
    .far-lamp .enc{opacity:0}
    .far-lamp.on .enc{opacity:1}
    .far-lamp.on{box-shadow:0 0 60px 22px rgba(255,236,150,.55)}
    .far-lamp.rojo .enc{filter:hue-rotate(-48deg) saturate(4) brightness(.9)}
    .far-lamp.on.rojo{box-shadow:0 0 60px 22px rgba(230,40,30,.6)}
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
    await sleep(300);
    for (const letra of D.letras) {
      for (const t of letra) {
        if (id !== run) return;
        lamp.classList.toggle('rojo', t.c === 'r');
        lamp.classList.add('on');
        await sleep(t.s === '.' ? 280 : 840);
        lamp.classList.remove('on');
        await sleep(t.c === 'r' ? 420 : 300);
      }
      await sleep(1500);
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
    b.addEventListener('click', () => { if (entered.length < D.palabra.length) { entered += l; render(); } });
    kb.appendChild(b);
  });

  const replay = ui.button('Repetir mensaje', 'ghost', play);
  ui.button('Borrar', 'ghost', () => { entered = entered.slice(0, -1); render(); });
  ui.button('Comprobar', 'primary', () => {
    if (entered === D.palabra) {
      ui.say('¡Mensaje descifrado! El carguero contesta y, con un chasquido, se abre la trampilla de la sala de señales. Cifra de la ventana: ' + D.cifra + '. Coged la carta 36.', 'ok');
      kb.querySelectorAll('button').forEach(b => { b.disabled = true; });
    } else {
      ui.say('Esa palabra no es. Volved a mirar los destellos: cortos y largos, y ojo con los rojos.', 'bad');
    }
  });

  render();
  setTimeout(play, 500);
  return { close: ui.close };
}
