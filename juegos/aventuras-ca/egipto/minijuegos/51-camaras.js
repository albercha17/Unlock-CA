// Carta 51 — Las cámaras de colores: pintar las doce cámaras del templo con ocre, turquesa y lapislázuli de modo que dos cámaras con una
// puerta entre ellas no lleven la misma pintura. Las puertas y las cámaras ya pintadas, solo en el plano (cartas 61 y 63);
// la norma, en el papiro de la sacerdotisa (carta 26). Solución única (instancias_egipto.py, CAMARAS).
import { openGame } from './ui.js';
import { estilo, guardarSello } from './nilo.js';

const D = /*DATOS*/{"cols": 4, "filas": 3, "aristas": [[0, 1], [0, 4], [1, 2], [1, 4], [1, 5], [2, 3], [2, 6], [3, 6], [3, 7], [4, 5], [4, 8], [5, 6], [5, 8], [5, 9], [6, 7], [6, 9], [6, 10], [6, 11], [7, 11], [8, 9], [9, 10], [10, 11]], "fijos": {"6": 1, "10": 0}, "colores": ["ocre", "turquesa", "lapislazuli"], "solucion": [0, 1, 0, 2, 2, 0, 1, 0, 1, 2, 0, 2]}/*FIN*/;
const TONO = ['#c88c3c', '#2f9a9a', '#3a4fa8'];
const SIG = ['O', 'T', 'L'];
const LETRA = 'ABCDEFGHIJKL';

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 51 — Las cámaras de colores', instr: 'Tocad una cámara para pintarla (ocre, turquesa, lapislázuli y otra vez sin pintar). El plano, con sus puertas, en las cartas 61 y 63.', ...opts });
  estilo('eg-cam', `.cam-plano{display:grid;gap:8px;max-width:330px;margin:10px auto}.cam-cel{aspect-ratio:1;border-radius:50%;border:3px solid #2a1f0c;background:#f6e7bf;color:#2a1f0c;font:800 1rem system-ui;cursor:pointer;display:flex;flex-direction:column;align-items:center;justify-content:center;line-height:1.1}.cam-cel small{font:700 .6rem system-ui}`);
  const plano = document.createElement('div'); plano.className = 'cam-plano';
  plano.style.gridTemplateColumns = 'repeat(' + D.cols + ',1fr)';
  ui.body.appendChild(plano);
  const n = D.cols * D.filas;
  const col = Array(n).fill(null);
  const btn = [];
  for (let i = 0; i < n; i++) {
    const b = document.createElement('button'); b.type = 'button'; b.className = 'cam-cel'; b.dataset.i = String(i);
    b.setAttribute('aria-label', 'Cámara ' + LETRA[i]);
    b.innerHTML = LETRA[i] + '<small></small>';
    b.addEventListener('click', () => { if (resuelto) return; col[i] = col[i] === null ? 0 : col[i] === 2 ? null : col[i] + 1; ui.say(''); pintar(); });
    btn.push(b); plano.appendChild(b);
  }
  function pintar() {
    btn.forEach((b, i) => { b.style.background = col[i] === null ? '#f6e7bf' : TONO[col[i]]; b.style.color = col[i] === null ? '#2a1f0c' : '#fff'; b.querySelector('small').textContent = col[i] === null ? '' : SIG[col[i]]; });
    plano.dataset.col = col.map(c => c === null ? '-' : c).join('');
  }
  let resuelto = false;
  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    if (col.includes(null)) { ui.say('Quedan cámaras sin pintar.', 'bad'); return; }
    if (col.every((c, i) => c === D.solucion[i])) {
      resuelto = true; guardarSello('51');
      ui.say('Las doce cámaras brillan cada una con su pintura y la sacerdotisa os sonríe. Coged la carta 58.', 'ok');
    } else ui.say('Alguna cámara no cuadra con el plano: o dos vecinas comparten pintura, o una de las ya pintadas no tiene su color (cartas 26, 61 y 63).', 'bad');
  });
  pintar();
  return { close: ui.close };
}
