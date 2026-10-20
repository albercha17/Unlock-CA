// Carta 71 — Anillos de Ra: poner sol, ojo y escarabajo (acertijo de la carta 26).
import { openGame } from './ui.js';

const SIMBOLOS = ['sol', 'ojo', 'escarabajo', 'serpiente', 'agua', 'halcon'];
const ico = s => '<img alt="" src="./img/ui/glifos/' + s + '.jpg">';
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
    .far-anillo{display:flex;flex-direction:column;align-items:center;gap:6px;background:linear-gradient(rgba(20,12,4,.6),rgba(20,12,4,.8)),url(./img/ui/piedra.jpg) center/cover;border:3px solid #6b5320;border-radius:14px;padding:8px 10px;box-shadow:inset 0 0 18px rgba(0,0,0,.7)}
    .far-anillo img{display:block;object-fit:contain;mix-blend-mode:screen}
    .far-anillo .lado{opacity:.32;line-height:0;filter:blur(.4px)}
    .far-anillo .lado img{width:40px;height:40px}
    .far-anillo .centro{line-height:0;background:radial-gradient(circle,rgba(255,210,122,.22),rgba(0,0,0,.55));border:2px solid #b8893b;border-radius:12px;padding:6px}
    .far-anillo .centro img{width:72px;height:72px;filter:drop-shadow(0 0 8px rgba(255,210,122,.6))}
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
      ant.innerHTML = ico(SIMBOLOS[(v - 1 + n) % n]);
      const cen = document.createElement('div');
      cen.className = 'centro';
      cen.innerHTML = ico(SIMBOLOS[v]);
      cen.dataset.simbolo = SIMBOLOS[v];
      const sig = document.createElement('div');
      sig.className = 'lado';
      sig.innerHTML = ico(SIMBOLOS[(v + 1) % n]);
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
      ui.say('¡Los anillos encajan con un clac! Una puerta de piedra se abre a una capilla escondida. Coged la carta 35.', 'ok');
    } else {
      ui.say('Los anillos no encajan. Releed el acertijo de la cartela.', 'bad');
    }
  });

  pintar();
  return { close: ui.close };
}
