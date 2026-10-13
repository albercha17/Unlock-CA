// Carta 23 — Muro de jeroglíficos: descifrar 5 signos con la piedra de traducción (carta 31). Palabra: HORUS.
import { openGame } from './ui.js';

const GLIFOS = ['vasija', 'ojo', 'sol', 'escarabajo', 'serpiente'];
const PALABRA = 'HORUS';

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 23 — Muro de jeroglíficos',
    instr: 'Traduce los cinco signos con la piedra de traducción y escribe la palabra.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .far-glifos{display:flex;gap:6px;justify-content:center;margin-bottom:12px;background:linear-gradient(rgba(20,12,4,.55),rgba(20,12,4,.7)),url(./img/ui/piedra.jpg) center/cover;border:3px solid #6b5320;border-radius:6px;padding:14px 6px;box-shadow:inset 0 0 26px rgba(0,0,0,.75)}
    .far-glifo{width:15%;max-width:64px;aspect-ratio:1;object-fit:contain;mix-blend-mode:screen;filter:drop-shadow(0 0 6px rgba(255,210,122,.35))}
  `;
  ui.body.appendChild(style);

  const fila = document.createElement('div');
  fila.className = 'far-glifos';
  GLIFOS.forEach(g => {
    const s = document.createElement('img');
    s.className = 'far-glifo';
    s.alt = 'Signo ' + g;
    s.src = './img/ui/glifos/' + g + '.jpg';
    fila.appendChild(s);
  });
  const display = document.createElement('div');
  display.className = 'far-display';
  const kb = document.createElement('div');
  kb.className = 'far-keyboard';
  ui.body.append(fila, display, kb);

  let entered = '';
  const render = () => { display.textContent = entered === '' ? '—' : entered; };

  'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('').forEach(l => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'far-key';
    b.textContent = l;
    b.addEventListener('click', () => { if (entered.length < PALABRA.length) { entered += l; render(); } });
    kb.appendChild(b);
  });

  ui.button('Borrar', 'ghost', () => { entered = entered.slice(0, -1); render(); });
  ui.button('Comprobar', 'primary', () => {
    if (entered === PALABRA) {
      ui.say('¡El muro tiembla y se abre una hornacina! Dentro hay medio medallón. Coged la carta 18.', 'ok');
      kb.querySelectorAll('button').forEach(b => { b.disabled = true; });
    } else {
      ui.say('Nada sucede. Revisad la piedra de traducción, signo por signo.', 'bad');
    }
  });

  render();
  return { close: ui.close };
}
