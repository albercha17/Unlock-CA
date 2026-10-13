// Carta 64 — Cristales de la cueva: pared de 4 x 3 cristales. Al tocar uno cambian él y sus vecinos en cruz.
// Objetivo (dibujo rupestre, carta 66): ○ ○ ● ○ / ● ● ● ● / ○ ○ ● ●. Se empieza con todos apagados.
// Una solución: B1, A2, B2, A3 y D3.
import { openGame } from './ui.js';

const COLS = 4, ROWS = 3;
const OBJETIVO = [0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1];
const LETRAS = 'ABCD';

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 64 — Cristales de la cueva',
    instr: 'Al tocar un cristal cambian él y los cuatro que lo rodean en cruz (se encienden o se apagan). Deja la pared como el dibujo rupestre.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .cri-pared{display:grid;grid-template-columns:repeat(${COLS},1fr);gap:6px;max-width:330px;margin:0 auto 8px;padding:12px;border-radius:12px;border:3px solid #2a1a10;background:linear-gradient(rgba(8,4,2,.35),rgba(8,4,2,.55)),url(./img/ui/roca-cueva.jpg) center/cover;box-shadow:inset 0 0 30px rgba(0,0,0,.85)}
    .cri-cell{position:relative;aspect-ratio:1;padding:0;border:0;border-radius:10px;background:#000;overflow:hidden;cursor:pointer;transition:box-shadow .25s,transform .1s}
    .cri-cell:active{transform:scale(.94)}
    .cri-cell img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;mix-blend-mode:screen;transition:opacity .25s}
    .cri-cell img.on{opacity:0}
    .cri-cell[data-on="1"] img.on{opacity:1}
    .cri-cell[data-on="1"] img.off{opacity:0}
    .cri-cell[data-on="1"]{box-shadow:0 0 16px rgba(110,190,255,.75)}
    .cri-cont{color:#cfe0f0;font-size:.85rem;margin-bottom:4px}
  `;
  ui.body.appendChild(style);

  const pared = document.createElement('div');
  pared.className = 'cri-pared';
  const cont = document.createElement('div');
  cont.className = 'cri-cont';
  ui.body.append(pared, cont);

  let estado = Array(COLS * ROWS).fill(0);
  let toques = 0;
  let resuelto = false;
  const celdas = [];

  function tocar(i) {
    if (resuelto) return;
    const c = i % COLS, r = Math.floor(i / COLS);
    [[0, 0], [1, 0], [-1, 0], [0, 1], [0, -1]].forEach(([dc, dr]) => {
      const x = c + dc, y = r + dr;
      if (x >= 0 && x < COLS && y >= 0 && y < ROWS) estado[y * COLS + x] ^= 1;
    });
    toques++;
    ui.say('');
    pintar();
    if (estado.every((v, k) => v === OBJETIVO[k])) {
      resuelto = true;
      celdas.forEach(b => { b.disabled = true; });
      ui.say('¡La pared brilla como en el dibujo y se abre con un temblor! Entráis en una cámara caliente. Coged la carta 78.', 'ok');
    }
  }

  for (let i = 0; i < COLS * ROWS; i++) {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'cri-cell';
    b.dataset.i = String(i);
    b.setAttribute('aria-label', 'Cristal ' + LETRAS[i % COLS] + (Math.floor(i / COLS) + 1));
    b.innerHTML = '<img class="off" alt="" src="./img/ui/cristales/apagado.jpg"><img class="on" alt="" src="./img/ui/cristales/encendido.jpg">';
    b.addEventListener('click', () => tocar(i));
    celdas.push(b);
    pared.appendChild(b);
  }

  function pintar() {
    celdas.forEach((b, i) => { b.dataset.on = String(estado[i]); });
    cont.textContent = 'Toques: ' + toques;
  }

  ui.button('Apagar todo', 'ghost', () => { if (!resuelto) { estado = estado.map(() => 0); toques = 0; ui.say(''); pintar(); } });

  pintar();
  return { close: ui.close };
}
