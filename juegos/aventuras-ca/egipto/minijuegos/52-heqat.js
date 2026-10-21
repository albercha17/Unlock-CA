// Carta 52 — La medida del heqat: el escriba cobra con las seis partes del Ojo de Horus (1/2, 1/4, 1/8, 1/16, 1/32 y 1/64); cada parte
// se usa una vez o ninguna. Qué forma es cada parte, en la carta 54; los pagos del día, en las 55 y 59. Solución: 1/2, 1/16 y 1/64.
import { openGame } from './ui.js';
import { estilo, guardarSello, NS } from './nilo.js';

const D = /*DATOS*/{"partes": [[1, 2], [1, 4], [1, 8], [1, 16], [1, 32], [1, 64]], "formas": ["circulo", "cuadrado", "triangulo", "rombo", "estrella", "hexagono"], "manana": [[1, 4], [1, 8], [1, 8]], "tarde": [[1, 32], [1, 32], [1, 64]], "total64": 37, "solucion": [0, 3, 5]}/*FIN*/;

function forma(f, color) {
  const s = document.createElementNS(NS, 'svg');
  s.setAttribute('viewBox', '0 0 100 100'); s.setAttribute('width', '44'); s.setAttribute('height', '44'); s.setAttribute('aria-hidden', 'true');
  const pts = {
    triangulo: '50,10 92,84 8,84', rombo: '50,4 92,50 50,96 8,50', cuadrado: '14,14 86,14 86,86 14,86',
    estrella: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9].map(k => { const a = -Math.PI / 2 + k * Math.PI / 5, r = k % 2 ? 22 : 46; return (50 + Math.cos(a) * r).toFixed(1) + ',' + (50 + Math.sin(a) * r).toFixed(1); }).join(' '),
    hexagono: [0, 1, 2, 3, 4, 5].map(k => (50 + Math.cos(k * Math.PI / 3) * 44).toFixed(1) + ',' + (50 + Math.sin(k * Math.PI / 3) * 44).toFixed(1)).join(' ')
  };
  let n;
  if (f === 'circulo') { n = document.createElementNS(NS, 'circle'); n.setAttribute('cx', '50'); n.setAttribute('cy', '50'); n.setAttribute('r', '40'); }
  else { n = document.createElementNS(NS, 'polygon'); n.setAttribute('points', pts[f]); }
  n.setAttribute('fill', color); n.setAttribute('stroke', '#2a1f0c'); n.setAttribute('stroke-width', '4');
  s.appendChild(n);
  return s;
}

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 52 — La medida del heqat', instr: 'El escriba del templo cobra con las partes del Ojo de Horus, y cada parte se usa una vez o ninguna. Tocad las partes que sumadas dan lo que se ha cobrado hoy, y pulsad «Medir».', ...opts });
  estilo('eg-heqat', `.heq-partes{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;max-width:300px;margin:10px auto}.heq-parte{border-radius:12px;border:3px solid #6d5a36;background:#4d3c20;padding:10px 0;cursor:pointer;display:flex;justify-content:center}.heq-parte.on{border-color:#ffd36a;background:#7a5f26}`);
  const c = document.createElement('div'); c.className = 'heq-partes';
  const on = new Set();
  D.formas.forEach((f, i) => {
    const b = document.createElement('button'); b.type = 'button'; b.className = 'heq-parte'; b.dataset.i = String(i);
    b.setAttribute('aria-label', 'Parte ' + (i + 1));
    b.appendChild(forma(f, '#4aa3a3'));
    b.addEventListener('click', () => { if (resuelto) return; on.has(i) ? on.delete(i) : on.add(i); b.classList.toggle('on', on.has(i)); ui.say(''); });
    c.appendChild(b);
  });
  ui.body.appendChild(c);
  let resuelto = false;
  ui.button('Medir', 'primary', () => {
    if (resuelto) return;
    if (!on.size) { ui.say('Elegid alguna parte.', 'bad'); return; }
    const sol = new Set(D.solucion);
    if (on.size === sol.size && [...on].every(i => sol.has(i))) {
      resuelto = true; guardarSello('52');
      ui.say('La balanza de cebada se equilibra y el escriba sonríe: las cuentas del día cuadran. Coged la carta 44.', 'ok');
    } else ui.say('El escriba frunce el ceño: esa medida no es lo que se ha cobrado hoy (cartas 54, 55 y 59).', 'bad');
  });
  ui.button('Vaciar', 'ghost', () => { if (!resuelto) { on.clear(); c.querySelectorAll('.heq-parte').forEach(b => b.classList.remove('on')); ui.say(''); } });
  return { close: ui.close };
}
