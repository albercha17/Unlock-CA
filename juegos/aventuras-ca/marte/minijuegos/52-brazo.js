// Carta 52 — El brazo de la antena: colocar tres pesos de repuesto en las marcas del brazo para que no se incline. El brazo, con lo que ya cuelga,
// en la carta 54; cuánto pesa cada pieza, en la 55; la norma, en la 59. Solución única (instancias_marte.py, BALANCIN). Dato de la misión: 2.
import { openGame } from './ui.js';
import { estilo, NS } from './cupula.js';

const D = /*DATOS*/{"posiciones": [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5], "libres": 3, "solucion": [-4, -3, -1], "dato": 2}/*FIN*/;
const FORMAS = ['circulo', 'cuadrado', 'triangulo'];

function forma(f, col) {
  const s = document.createElementNS(NS, 'svg');
  s.setAttribute('viewBox', '0 0 40 40'); s.setAttribute('width', '34'); s.setAttribute('height', '34'); s.setAttribute('aria-hidden', 'true');
  let n;
  if (f === 'circulo') { n = document.createElementNS(NS, 'circle'); n.setAttribute('cx', '20'); n.setAttribute('cy', '20'); n.setAttribute('r', '15'); }
  else { n = document.createElementNS(NS, 'polygon'); n.setAttribute('points', f === 'cuadrado' ? '6,6 34,6 34,34 6,34' : '20,4 36,34 4,34'); }
  n.setAttribute('fill', col); n.setAttribute('stroke', '#2a120c'); n.setAttribute('stroke-width', '3');
  s.appendChild(n);
  return s;
}

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 52 — El brazo de la antena', instr: 'Tocad una pieza de repuesto y luego la marca del brazo donde la colgáis. Cada marca admite un solo peso. Las piezas, en la carta 55.', ...opts });
  estilo('mr-bra', `.bra-brazo{display:grid;grid-template-columns:repeat(11,1fr);gap:3px;max-width:340px;margin:10px auto}.bra-m{min-height:48px;border-radius:6px;border:2px solid #6a4a3a;background:#4a2a1c;color:#ffe6d6;font:700 .65rem system-ui;cursor:pointer;padding:0;display:flex;flex-direction:column;align-items:center;justify-content:center}.bra-m.eje{background:#2a120c;cursor:default;border-style:dashed}.bra-m.on{background:#7a4430}.bra-piezas{display:flex;gap:12px;justify-content:center;margin:8px 0}.bra-p{width:54px;height:54px;border-radius:10px;border:3px solid #6a4a3a;background:#4a2a1c;cursor:pointer;display:flex;align-items:center;justify-content:center;padding:0}.bra-p.sel{border-color:#ffd36a;background:#7a4430}.bra-p.puesta{opacity:.4}`);
  const brazo = document.createElement('div'); brazo.className = 'bra-brazo';
  const piezas = document.createElement('div'); piezas.className = 'bra-piezas';
  ui.body.append(brazo, piezas);
  const puesto = Array(D.libres).fill(null);       // posición donde está cada pieza
  let sel = null, resuelto = false;
  function pintar() {
    brazo.querySelectorAll('.bra-m[data-p]').forEach(b => {
      const k = puesto.indexOf(Number(b.dataset.p));
      b.classList.toggle('on', k >= 0);
      b.querySelector('span').textContent = '';
      if (k >= 0) b.querySelector('span').appendChild(forma(FORMAS[k], '#ff8a50'));
    });
    piezas.querySelectorAll('.bra-p').forEach(b => { const k = Number(b.dataset.k); b.classList.toggle('sel', sel === k); b.classList.toggle('puesta', puesto[k] !== null); });
    brazo.dataset.puesto = puesto.map(p => p === null ? '-' : p).join(',');
  }
  for (let i = -5; i <= 5; i++) {
    const b = document.createElement('button'); b.type = 'button'; b.className = 'bra-m' + (i === 0 ? ' eje' : '');
    if (i === 0) { b.disabled = true; b.innerHTML = '<span>▲</span><small>eje</small>'; }
    else {
      b.dataset.p = String(i); b.setAttribute('aria-label', (i < 0 ? 'Izquierda ' : 'Derecha ') + Math.abs(i));
      b.innerHTML = '<span></span><small>' + (i < 0 ? '◀' : '▶') + Math.abs(i) + '</small>';
      b.addEventListener('click', () => {
        if (resuelto) return;
        const ocupa = puesto.indexOf(i);
        if (sel !== null) { if (ocupa >= 0 && ocupa !== sel) puesto[ocupa] = null; puesto[sel] = i; sel = null; }
        else if (ocupa >= 0) puesto[ocupa] = null;
        ui.say(''); pintar();
      });
    }
    brazo.appendChild(b);
  }
  for (let k = 0; k < D.libres; k++) {
    const b = document.createElement('button'); b.type = 'button'; b.className = 'bra-p'; b.dataset.k = String(k);
    b.setAttribute('aria-label', 'Pieza ' + (k + 1));
    b.appendChild(forma(FORMAS[k], '#ff8a50'));
    b.addEventListener('click', () => { if (!resuelto) { sel = sel === k ? null : k; pintar(); } });
    piezas.appendChild(b);
  }
  ui.button('Soltar el brazo', 'primary', () => {
    if (resuelto) return;
    if (puesto.includes(null)) { ui.say('Faltan piezas por colgar.', 'bad'); return; }
    if (puesto.every((p, k) => p === D.solucion[k])) {
      resuelto = true;
      ui.say('El brazo queda horizontal, firme como una regla, y la antena apunta a la Tierra. Dato de la misión: ' + D.dato + '. Coged la carta 44.', 'ok');
    } else ui.say('El brazo se inclina hacia un lado y gime: lo que empuja a cada lado no es igual (cartas 54, 55 y 59).', 'bad');
  });
  pintar();
  return { close: ui.close };
}
