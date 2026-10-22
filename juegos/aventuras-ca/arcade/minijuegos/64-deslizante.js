// Carta 64 — El puzle deslizante: ordenar las ocho fichas de un tablero de 3 x 3 con un hueco hasta que formen el dibujo final. El dibujo, en las
// cartas 66 y 67 (dos mitades). El tablero de partida es solucionable (instancias_arcade.py, DESLIZANTE).
import { openGame } from './ui.js';
import { estilo, NEON } from './maquina.js';

const D = /*DATOS*/{"inicio": [[8, 1, 7], [6, 3, 5], [0, 2, 4]], "objetivo": [[1, 2, 3], [8, 0, 4], [7, 6, 5]]}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 64 — El puzle deslizante', instr: 'Tocad una ficha junto al hueco para deslizarla. Dejad las ocho fichas como en el dibujo final de las cartas 66 y 67.', ...opts });
  estilo('ar-des', `
    .des-tab{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;width:min(78vw,300px);margin:10px auto;padding:8px;border-radius:10px;background:#0a0418;border:2px solid #2ee67a}
    .des-ficha{aspect-ratio:1;border-radius:8px;border:4px solid;background:#1c0a30;font:800 2rem ui-monospace,monospace;cursor:pointer;padding:0}
    .des-hueco{aspect-ratio:1}
  `);
  const g = D.inicio.map(f => f.slice());
  let mov = 0, resuelto = false;
  const tab = document.createElement('div');
  tab.className = 'des-tab';
  const info = document.createElement('div');
  info.className = 'ar-pie';
  ui.body.append(tab, info);
  function pintar() {
    tab.innerHTML = '';
    for (let y = 0; y < 3; y++) for (let x = 0; x < 3; x++) {
      const v = g[y][x];
      if (!v) { const h = document.createElement('div'); h.className = 'des-hueco'; tab.appendChild(h); continue; }
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'des-ficha';
      b.dataset.v = String(v);
      b.textContent = String(v);
      b.style.borderColor = NEON[v - 1];
      b.style.color = NEON[v - 1];
      b.setAttribute('aria-label', 'Ficha ' + v);
      b.addEventListener('click', () => mover(x, y));
      tab.appendChild(b);
    }
    info.textContent = 'Movimientos: ' + mov;
    tab.dataset.mov = String(mov);
  }
  function mover(x, y) {
    if (resuelto) return;
    for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
      const nx = x + dx, ny = y + dy;
      if (nx >= 0 && ny >= 0 && nx < 3 && ny < 3 && g[ny][nx] === 0) {
        g[ny][nx] = g[y][x]; g[y][x] = 0; mov++;
        ui.say('');
        pintar();
        if (g.every((f, j) => f.every((v, i) => v === D.objetivo[j][i]))) {
          resuelto = true;
          ui.say('Las fichas forman el dibujo final en ' + mov + ' movimientos y el tablero se ilumina. Coged la carta 62.', 'ok');
        }
        return;
      }
    }
    ui.say('Esa ficha no está junto al hueco.', 'bad');
  }
  ui.button('Empezar de nuevo', 'ghost', () => {
    if (resuelto) return;
    D.inicio.forEach((f, j) => f.forEach((v, i) => { g[j][i] = v; }));
    mov = 0; ui.say(''); pintar();
  });
  pintar();
  return { close: ui.close };
}
