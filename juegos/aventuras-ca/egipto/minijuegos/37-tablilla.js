// Carta 37 — Tablilla rota: puzle deslizante 3x3. El orden correcto está en la carta 28 (Orden de los dioses).
// Orden: ☀️ 👁️ 🐞 / 🐍 🌊 🦅 / 🏺 🐂 y el hueco abajo a la derecha.
import { openGame } from './ui.js';

const SIMBOLOS = { 1: '☀️', 2: '👁️', 3: '🐞', 4: '🐍', 5: '🌊', 6: '🦅', 7: '🏺', 8: '🐂' };
const META = [1, 2, 3, 4, 5, 6, 7, 8, 0];
const INICIAL = [2, 6, 3, 4, 0, 5, 1, 7, 8];

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 37 — Tablilla rota',
    instr: 'Desliza las piezas al hueco hasta ordenar la tablilla como indica el orden de los dioses.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .far-tabla{display:grid;grid-template-columns:repeat(3,84px);gap:6px;justify-content:center;margin:4px 0 10px;background:#2b1f0e;border:3px solid #b8893b;border-radius:12px;padding:8px;width:fit-content;margin-inline:auto}
    .far-pieza{width:84px;height:84px;border-radius:10px;border:2px solid #b8893b;background:linear-gradient(180deg,#d9b46a,#b88f45);font-size:2.4rem;cursor:pointer;display:flex;align-items:center;justify-content:center;font-family:inherit;padding:0}
    .far-pieza:active{transform:scale(.96)}
    .far-pieza.hueco{background:transparent;border:2px dashed #6b5320;cursor:default}
    .far-movs{color:#9fb4c8;font-size:.85rem;margin-bottom:6px}
  `;
  ui.body.appendChild(style);

  const tabla = document.createElement('div');
  tabla.className = 'far-tabla';
  const movs = document.createElement('div');
  movs.className = 'far-movs';
  ui.body.append(tabla, movs);

  let estado = INICIAL.slice();
  let n = 0;
  let resuelto = false;

  function pintar() {
    tabla.innerHTML = '';
    estado.forEach((v, i) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'far-pieza' + (v === 0 ? ' hueco' : '');
      b.dataset.pos = String(i);
      if (v !== 0) {
        b.textContent = SIMBOLOS[v];
        b.setAttribute('aria-label', 'Pieza ' + SIMBOLOS[v]);
        b.addEventListener('click', () => mover(i));
      } else {
        b.disabled = true;
        b.setAttribute('aria-label', 'Hueco');
      }
      tabla.appendChild(b);
    });
    movs.textContent = 'Movimientos: ' + n;
  }

  function mover(i) {
    if (resuelto) return;
    const h = estado.indexOf(0);
    const [fi, ci] = [Math.floor(i / 3), i % 3];
    const [fh, ch] = [Math.floor(h / 3), h % 3];
    if (Math.abs(fi - fh) + Math.abs(ci - ch) !== 1) return;
    estado[h] = estado[i];
    estado[i] = 0;
    n++;
    pintar();
    if (estado.every((v, k) => v === META[k])) {
      resuelto = true;
      ui.say('¡La tablilla encaja! Del hueco cae un escarabajo de oro. Coged la carta 55.', 'ok');
    }
  }

  ui.button('Barajar de nuevo', 'ghost', () => {
    if (resuelto) return;
    estado = INICIAL.slice();
    n = 0;
    ui.say('');
    pintar();
  });

  pintar();
  return { close: ui.close };
}
