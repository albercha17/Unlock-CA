// Carta 69 — La caja de pigmentos (Mastermind): la caja se abre con cuatro pigmentos de colores distintos en cierto orden. Los intentos del aprendiz y lo que
// acertó cada vez, en la carta 70; los seis pigmentos y la norma, en la 71. La app no dice cuántos aciertos hay. Solución única
// (instancias_florencia.py, MASTERMIND). Letra de la clave: L.
import { openGame } from './ui.js';
import { estilo } from './taller.js';

const D = /*DATOS*/{"colores": ["rojo", "azul", "verde", "amarillo", "violeta", "blanco"], "solucion": [2, 0, 1, 4], "letra": "L"}/*FIN*/;
const TONO = ['#be322c', '#3c64d2', '#3c966a', '#e8be3c', '#8c50be', '#f0e8d8'];

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 69 — La caja de pigmentos', instr: 'Elegid un color y tocad el hueco de la caja donde va. Son cuatro pigmentos distintos. Los intentos anteriores y su norma, en las cartas 70 y 71.', ...opts });
  estilo('fl-mas', `.mas-hue{display:flex;gap:10px;justify-content:center;margin:12px 0}.mas-h{width:56px;height:56px;border-radius:50%;border:3px dashed #d9a441;background:rgba(0,0,0,.3);cursor:pointer;padding:0}.mas-pal{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin:10px 0}.mas-c{width:46px;height:46px;border-radius:50%;border:3px solid #6d5a36;cursor:pointer;padding:0}.mas-c.sel{border-color:#fff;box-shadow:0 0 0 3px #d9a441}.mas-c.usado{opacity:.35}`);
  const hue = document.createElement('div'); hue.className = 'mas-hue';
  const pal = document.createElement('div'); pal.className = 'mas-pal';
  ui.body.append(hue, pal);
  const sel_ = [null, null, null, null];
  let sel = null, resuelto = false;
  function pintar() {
    hue.querySelectorAll('.mas-h').forEach((h, i) => { h.style.background = sel_[i] === null ? '' : TONO[sel_[i]]; h.style.borderStyle = sel_[i] === null ? 'dashed' : 'solid'; });
    pal.querySelectorAll('.mas-c').forEach(c => { const k = Number(c.dataset.k); c.classList.toggle('sel', sel === k); c.classList.toggle('usado', sel_.includes(k)); });
    hue.dataset.orden = sel_.map(x => x === null ? '-' : x).join(',');
  }
  for (let i = 0; i < 4; i++) {
    const h = document.createElement('button'); h.type = 'button'; h.className = 'mas-h'; h.dataset.i = String(i); h.setAttribute('aria-label', 'Hueco ' + (i + 1));
    h.addEventListener('click', () => {
      if (resuelto) return;
      if (sel !== null) { const o = sel_.indexOf(sel); if (o >= 0 && o !== i) sel_[o] = null; sel_[i] = sel; sel = null; }
      else sel_[i] = null;
      ui.say(''); pintar();
    });
    hue.appendChild(h);
  }
  D.colores.forEach((n, k) => {
    const c = document.createElement('button'); c.type = 'button'; c.className = 'mas-c'; c.dataset.k = String(k); c.style.background = TONO[k]; c.setAttribute('aria-label', n);
    c.addEventListener('click', () => { if (!resuelto) { sel = sel === k ? null : k; pintar(); } });
    pal.appendChild(c);
  });
  ui.button('Abrir la caja', 'primary', () => {
    if (resuelto) return;
    if (sel_.includes(null)) { ui.say('Faltan pigmentos por colocar.', 'bad'); return; }
    if (sel_.every((c, i) => c === D.solucion[i])) {
      resuelto = true;
      ui.say('La caja se abre con un chasquido y huele a aceite de linaza. Letra de la clave: ' + D.letra + '. Coged la carta 80.', 'ok');
    } else ui.say('La caja no se abre: ese orden contradice alguno de los intentos anteriores (cartas 70 y 71).', 'bad');
  });
  pintar();
  return { close: ui.close };
}
