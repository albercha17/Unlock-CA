// Carta 23 — Muro de jeroglíficos: descifrar 5 signos con la piedra de traducción (carta 31). Palabra: HORUS.
import { openGame } from './ui.js';

const GLIFOS = ['🏺', '👁️', '☀️', '🐞', '🐍'];
const PALABRA = 'HORUS';

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 23 — Muro de jeroglíficos',
    instr: 'Traduce los cinco signos con la piedra de traducción y escribe la palabra.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .far-glifos{display:flex;gap:8px;justify-content:center;margin-bottom:12px;background:#2b1f0e;border:2px solid #b8893b;border-radius:10px;padding:12px 6px}
    .far-glifo{font-size:2.2rem;width:3rem;text-align:center}
  `;
  ui.body.appendChild(style);

  const fila = document.createElement('div');
  fila.className = 'far-glifos';
  GLIFOS.forEach(g => {
    const s = document.createElement('span');
    s.className = 'far-glifo';
    s.textContent = g;
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
