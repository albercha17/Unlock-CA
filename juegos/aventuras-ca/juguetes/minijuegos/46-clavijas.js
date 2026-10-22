// Carta 46 — El solitario de clavijas: un tablero en cruz de 33 agujeros con nueve clavijas (carta 37). Una clavija salta sobre otra, en línea recta, a un agujero
// vacío y se come a la saltada (regla en la carta 39); hay que dejar una sola clavija en el agujero del medio (la meta, en la carta 33).
// instancias_juguetes.py, CLAVIJAS: se construyó deshaciendo ocho saltos desde la meta, así que hay solución.
import { openGame } from './ui.js';
import { estilo } from './comun.js';

const D = /*DATOS*/{"agujeros": [[0, 2], [0, 3], [0, 4], [1, 2], [1, 3], [1, 4], [2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [3, 0], [3, 1], [3, 2], [3, 3], [3, 4], [3, 5], [3, 6], [4, 0], [4, 1], [4, 2], [4, 3], [4, 4], [4, 5], [4, 6], [5, 2], [5, 3], [5, 4], [6, 2], [6, 3], [6, 4]], "clavijas": [[1, 3], [1, 4], [2, 2], [2, 3], [2, 4], [2, 5], [3, 2], [3, 4], [3, 5]], "centro": [3, 3]}/*FIN*/;
const k = (r, c) => r + ',' + c;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 46 — El solitario de clavijas', instr: 'Tocad una clavija y luego el agujero vacío al que salta, sobre otra clavija y en línea recta. Dejad una sola en el agujero del medio. El tablero está en la carta 37, la regla en la 39 y la meta, en la 33.', ...opts });
  estilo('ju-cla', '.cla-t{display:grid;grid-template-columns:repeat(7,1fr);gap:3px;width:min(86vw,320px);margin:8px auto;padding:10px;border-radius:12px;background:#c48c56;border:4px solid #6a4022}.cla-t button{aspect-ratio:1;border:0;border-radius:50%;padding:0;cursor:pointer;background:#78502e;box-shadow:inset 0 2px 4px rgba(0,0,0,.4)}.cla-t button.vacio{visibility:visible}.cla-t button.fuera{visibility:hidden}.cla-t button.peg{background:radial-gradient(circle at 35% 30%,#ff8a80,#d63430 55%,#7a1010)}.cla-t button.sel{outline:4px solid #fff}');
  const agujeros = new Set(D.agujeros.map(a => k(a[0], a[1])));
  let pegs, sel = null, historia = [], resuelto = false;
  const reiniciar = () => { pegs = new Set(D.clavijas.map(a => k(a[0], a[1]))); sel = null; historia = []; };
  reiniciar();
  const tabla = document.createElement('div');
  tabla.className = 'cla-t';
  const pie = document.createElement('div');
  pie.className = 'ju-pie';
  ui.body.append(tabla, pie);
  function hay_saltos() {
    for (const p of pegs) {
      const [r, c] = p.split(',').map(Number);
      for (const [dr, dc] of [[0, 1], [1, 0], [0, -1], [-1, 0]]) {
        if (pegs.has(k(r + dr, c + dc)) && agujeros.has(k(r + 2 * dr, c + 2 * dc)) && !pegs.has(k(r + 2 * dr, c + 2 * dc))) return true;
      }
    }
    return false;
  }
  function pintar() {
    tabla.innerHTML = '';
    for (let r = 0; r < 7; r++) for (let c = 0; c < 7; c++) {
      const b = document.createElement('button');
      b.type = 'button';
      b.dataset.r = String(r);
      b.dataset.c = String(c);
      const id = k(r, c);
      b.className = !agujeros.has(id) ? 'fuera' : pegs.has(id) ? 'peg' : 'vacio';
      if (sel === id) b.classList.add('sel');
      b.setAttribute('aria-label', 'Agujero fila ' + (r + 1) + ', columna ' + (c + 1) + (pegs.has(id) ? ', con clavija' : ', vacío'));
      if (agujeros.has(id)) b.addEventListener('click', () => tocar(r, c));
      tabla.appendChild(b);
    }
    pie.textContent = 'Clavijas: ' + pegs.size;
  }
  function tocar(r, c) {
    if (resuelto) return;
    const id = k(r, c);
    if (pegs.has(id)) { sel = sel === id ? null : id; ui.say(''); pintar(); return; }
    if (!sel) { ui.say('Elegid primero una clavija.', 'bad'); return; }
    const [sr, sc] = sel.split(',').map(Number);
    const dr = r - sr, dc = c - sc;
    const recto = (Math.abs(dr) === 2 && dc === 0) || (Math.abs(dc) === 2 && dr === 0);
    const medio = k(sr + dr / 2, sc + dc / 2);
    if (!recto) { ui.say('Una clavija salta en línea recta, por encima de la de al lado: nunca en diagonal.', 'bad'); return; }
    if (!pegs.has(medio)) { ui.say('Solo se puede saltar por encima de otra clavija.', 'bad'); return; }
    historia.push([new Set(pegs)]);
    pegs.delete(sel);
    pegs.delete(medio);
    pegs.add(id);
    sel = null;
    pintar();
    if (pegs.size === 1 && pegs.has(k(D.centro[0], D.centro[1]))) {
      resuelto = true;
      ui.say('¡Solo queda una clavija, justo en el medio! La tapa del tablero se abre y asoma media llave de cuerda dorada. Coged la carta 56.', 'ok');
    } else if (!hay_saltos()) {
      ui.say(pegs.size === 1 ? 'Queda una sola clavija, pero no en el agujero del medio. Probad otro orden.' : 'Ya no quedan saltos posibles y sobran clavijas. Probad otro orden.', 'bad');
    } else {
      ui.say('');
    }
  }
  ui.button('Deshacer', '', () => { if (!resuelto && historia.length) { pegs = historia.pop()[0]; sel = null; ui.say(''); pintar(); } });
  ui.button('Empezar de nuevo', '', () => { if (!resuelto) { reiniciar(); ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
