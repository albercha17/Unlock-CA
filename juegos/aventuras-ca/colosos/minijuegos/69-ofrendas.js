// Carta 69 — Las ofrendas: caja negra. Con las ofrendas aceptadas y rechazadas de las cartas, deducir la regla del Coloso Viejo y elegir
// cuáles de seis ofrendas nuevas aceptaría. Solución única (herramientas/instancias_colosos.py, ofrendas).
import { openGame } from './ui.js';
import { estilo } from './comun.js';

const D = /*DATOS*/{"prueba": [[["azul", "picuda"], ["azul", "picuda"], ["roja", "picuda"]], [["azul", "redonda"], ["roja", "redonda"], ["blanca", "redonda"]], [["roja", "picuda"], ["azul", "picuda"], ["blanca", "redonda"]], [["blanca", "redonda"], ["roja", "picuda"], ["azul", "redonda"]], [["azul", "redonda"], ["azul", "picuda"], ["roja", "picuda"]], [["blanca", "redonda"], ["blanca", "redonda"], ["roja", "redonda"]]], "solucion": [2, 3, 4]}/*FIN*/;
const COL = { roja: '#c43c30', azul: '#3460b0', blanca: '#f4f2e8' };

estilo('co-ofr', `
  .co-ofrendas{display:flex;flex-direction:column;gap:6px;max-width:340px;margin:6px auto}
  .co-ofr{display:flex;align-items:center;gap:10px;padding:6px 10px;border-radius:10px;border:1.5px solid rgba(224,166,64,.5);background:rgba(255,240,210,.08);cursor:pointer;color:#fff6e4;font:700 1rem system-ui,sans-serif}
  .co-ofr.sel{background:rgba(110,180,110,.35);border-color:#8fe08f}
  .co-ofr .marca{margin-left:auto;font-size:1.2rem}
`);

function piedraSVG(color, forma) {
  const ns = 'http://www.w3.org/2000/svg';
  const s = document.createElementNS(ns, 'svg');
  s.setAttribute('viewBox', '0 0 40 40');
  s.setAttribute('width', 34);
  s.setAttribute('height', 34);
  const e = document.createElementNS(ns, forma === 'redonda' ? 'circle' : 'polygon');
  if (forma === 'redonda') { e.setAttribute('cx', 20); e.setAttribute('cy', 20); e.setAttribute('r', 15); }
  else e.setAttribute('points', '20,3 37,35 3,35');
  e.setAttribute('fill', COL[color]);
  e.setAttribute('stroke', '#241a12');
  e.setAttribute('stroke-width', 2.5);
  s.appendChild(e);
  s.setAttribute('aria-label', `${color} ${forma}`);
  return s;
}

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 69 — Las ofrendas',
    instr: 'Tocad las ofrendas que aceptaría el Coloso Viejo (todas y solo esas) y pulsad «Ofrecer».',
    ...opts
  });
  const sel = new Set();
  const lista = document.createElement('div');
  lista.className = 'co-ofrendas';
  const filas = D.prueba.map((piedras, i) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'co-ofr';
    b.dataset.ofrenda = i;
    const num = document.createElement('span');
    num.textContent = (i + 1) + '.';
    b.appendChild(num);
    piedras.forEach(([c, f]) => b.appendChild(piedraSVG(c, f)));
    const m = document.createElement('span');
    m.className = 'marca';
    b.appendChild(m);
    b.addEventListener('click', () => { if (sel.has(i)) sel.delete(i); else sel.add(i); pintar(); });
    lista.appendChild(b);
    return { b, m };
  });
  ui.body.append(lista);

  function pintar() {
    filas.forEach(({ b, m }, i) => { b.classList.toggle('sel', sel.has(i)); m.textContent = sel.has(i) ? '✔' : ''; });
  }

  ui.button('Ofrecer', 'primary', () => {
    if (!sel.size) { ui.say('El Coloso Viejo espera con la mano abierta: elegid alguna ofrenda.', ''); return; }
    const sol = new Set(D.solucion);
    if (sel.size === sol.size && [...sel].every(i => sol.has(i))) {
      ui.say('El Coloso Viejo coge las ofrendas una a una, las mira contra la luna y sonríe con la boca llena de musgo. Coged la carta 80.', 'ok');
      filas.forEach(({ b }) => { b.disabled = true; });
    } else {
      ui.say('El Coloso Viejo gruñe y aparta alguna piedra con el dedo. No es su regla.', 'bad');
      sel.clear();
      pintar();
    }
  });
  pintar();
  return { close: ui.close };
}
