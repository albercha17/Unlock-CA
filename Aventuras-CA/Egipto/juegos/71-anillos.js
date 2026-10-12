// Carta 71 — Anillos de Ra: poner sol, ojo y escarabajo (acertijo de la carta 26).
import { openGame } from './ui.js';

const SIMBOLOS = ['☀️', '👁️', '🐞', '🐍', '🌊', '🦅'];
const OBJETIVO = [0, 1, 2];
const INICIAL = [3, 1, 4];

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 71 — Anillos de Ra',
    instr: 'Gira cada anillo hasta que el símbolo central sea el correcto.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .far-anillos{display:flex;gap:14px;justify-content:center;margin-bottom:12px}
    .far-anillo{display:flex;flex-direction:column;align-items:center;gap:6px;background:#2b1f0e;border:2px solid #b8893b;border-radius:14px;padding:8px 10px}
    .far-anillo .lado{font-size:1.4rem;opacity:.35;line-height:1}
    .far-anillo .centro{font-size:2.6rem;line-height:1.3;background:#4a3414;border-radius:10px;padding:2px 10px}
    .far-anillo .flecha{width:100%}
  `;
  ui.body.appendChild(style);

  const fila = document.createElement('div');
  fila.className = 'far-anillos';
  ui.body.appendChild(fila);

  const idx = INICIAL.slice();
  const n = SIMBOLOS.length;
  let resuelto = false;

  function pintar() {
    fila.innerHTML = '';
    idx.forEach((v, i) => {
      const col = document.createElement('div');
      col.className = 'far-anillo';
      const arriba = document.createElement('button');
      arriba.type = 'button';
      arriba.className = 'far-key flecha';
      arriba.textContent = '▲';
      arriba.setAttribute('aria-label', 'Anillo ' + (i + 1) + ' arriba');
      const ant = document.createElement('div');
      ant.className = 'lado';
      ant.textContent = SIMBOLOS[(v - 1 + n) % n];
      const cen = document.createElement('div');
      cen.className = 'centro';
      cen.textContent = SIMBOLOS[v];
      const sig = document.createElement('div');
      sig.className = 'lado';
      sig.textContent = SIMBOLOS[(v + 1) % n];
      const abajo = document.createElement('button');
      abajo.type = 'button';
      abajo.className = 'far-key flecha';
      abajo.textContent = '▼';
      abajo.setAttribute('aria-label', 'Anillo ' + (i + 1) + ' abajo');
      arriba.addEventListener('click', () => { if (!resuelto) { idx[i] = (idx[i] - 1 + n) % n; ui.say(''); pintar(); } });
      abajo.addEventListener('click', () => { if (!resuelto) { idx[i] = (idx[i] + 1) % n; ui.say(''); pintar(); } });
      col.append(arriba, ant, cen, sig, abajo);
      fila.appendChild(col);
    });
  }

  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    if (idx.every((v, i) => v === OBJETIVO[i])) {
      resuelto = true;
      ui.say('¡Los anillos encajan con un clac! La puerta del tesoro se abre. Coged la carta 80.', 'ok');
    } else {
      ui.say('Los anillos no encajan. Releed el acertijo de la cartela.', 'bad');
    }
  });

  pintar();
  return { close: ui.close };
}
