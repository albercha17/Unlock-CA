// Carta 20 — El punto de fuga: marcar en la cuadrícula del suelo (cartas 19 y 21, dos mitades) la casilla donde se juntan las rectas dibujadas;
// el acertijo, en la carta 18. Se acepta la casilla exacta o una vecina (la regla no es perfecta). Solución en instancias_florencia.py (PERSPECTIVA).
import { openGame } from './ui.js';
import { estilo } from './taller.js';

const D = /*DATOS*/{"cols": 6, "filas": 15, "solucion": [3, 4], "tolerancia": 1}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 20 — El punto de fuga', instr: 'Tocad la casilla de la cuadrícula del suelo donde se encuentran todas las rectas si se alargan. Las columnas son letras (A a F) y las filas, números (1 a 15).', ...opts });
  estilo('fl-per', `.per-rej{display:grid;gap:2px;width:min(76vw,260px);margin:8px auto;padding:4px;border-radius:8px;background:#2a1f0c}.per-c{height:22px;border:0;border-radius:3px;background:#c9a96a;cursor:pointer;padding:0;font:700 .6rem system-ui;color:#2a1f0c}.per-c.sel{background:#ffd36a;outline:2px solid #fff}.per-e{font:700 .6rem system-ui;color:#f6e7bf;text-align:center;line-height:22px}`);
  const g = document.createElement('div'); g.className = 'per-rej';
  g.style.gridTemplateColumns = 'repeat(' + (D.cols + 1) + ',1fr)';
  let sel = null, resuelto = false;
  const btn = {};
  g.appendChild(document.createElement('div'));
  for (let c = 0; c < D.cols; c++) { const e = document.createElement('div'); e.className = 'per-e'; e.textContent = 'ABCDEF'[c]; g.appendChild(e); }
  for (let f = 0; f < D.filas; f++) {
    const e = document.createElement('div'); e.className = 'per-e'; e.textContent = String(f + 1); g.appendChild(e);
    for (let c = 0; c < D.cols; c++) {
      const b = document.createElement('button'); b.type = 'button'; b.className = 'per-c'; b.dataset.c = String(c); b.dataset.f = String(f);
      b.setAttribute('aria-label', 'Casilla ' + 'ABCDEF'[c] + (f + 1));
      b.addEventListener('click', () => {
        if (resuelto) return;
        if (sel) btn[sel[0] + ',' + sel[1]].classList.remove('sel');
        sel = [c, f]; b.classList.add('sel'); ui.say('Marcada la casilla ' + 'ABCDEF'[c] + (f + 1) + '.');
      });
      btn[c + ',' + f] = b; g.appendChild(b);
    }
  }
  ui.body.appendChild(g);
  ui.button('Fijar el punto de fuga', 'primary', () => {
    if (resuelto) return;
    if (!sel) { ui.say('Marcad antes una casilla.', 'bad'); return; }
    const d = Math.max(Math.abs(sel[0] - D.solucion[0]), Math.abs(sel[1] - D.solucion[1]));
    if (d <= D.tolerancia) {
      resuelto = true;
      ui.say('Las rectas se juntan justo ahí: el suelo del taller se hunde con un crujido y deja ver una cavidad. Coged la carta 28.', 'ok');
    } else ui.say('Ahí no se juntan las rectas. Alargadlas con una regla desde la lámina de abajo hasta que se encuentren (cartas 18, 19 y 21).', 'bad');
  });
  return { close: ui.close };
}
