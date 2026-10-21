// Carta 51 — El circuito del reactor (Slitherlink): trazar un solo bucle cerrado por los puntos del esquema; cada número dice por cuántos lados
// de su casilla pasa el anillo. El esquema, en las cartas 61 y 63 (dos mitades); la nota de la doctora, en la 26. Los números no están en la app.
// Solución única (instancias_marte.py, ANILLO).
import { openGame } from './ui.js';
import { estilo, NS } from './cupula.js';

const D = /*DATOS*/{"n": 6, "solucion": [["h", 0, 0], ["h", 0, 6], ["h", 1, 1], ["h", 1, 6], ["h", 2, 2], ["h", 2, 6], ["h", 3, 2], ["h", 3, 6], ["h", 4, 5], ["h", 4, 6], ["v", 0, 0], ["v", 0, 1], ["v", 0, 2], ["v", 0, 3], ["v", 0, 4], ["v", 0, 5], ["v", 1, 0], ["v", 2, 1], ["v", 4, 2], ["v", 4, 3], ["v", 4, 4], ["v", 5, 5]]}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 51 — El circuito del reactor', instr: 'Tocad un lado entre dos puntos para trazar el cable (otra vez para quitarlo). Tiene que quedar un solo bucle cerrado. El esquema con los números, en las cartas 61 y 63.', ...opts });
  estilo('mr-ani', `.ani-svg{display:block;width:min(88vw,330px);margin:10px auto;background:#2a2430;border-radius:10px}.ani-svg .lado{stroke:rgba(255,255,255,.12);stroke-width:5;stroke-linecap:round}.ani-svg .lado.on{stroke:#ff8a50;stroke-width:7}.ani-svg .hit{stroke:transparent;stroke-width:22;cursor:pointer}`);
  const n = D.n, L = 40, M = 20;
  const svg = document.createElementNS(NS, 'svg'); svg.setAttribute('class', 'ani-svg'); svg.setAttribute('viewBox', '0 0 ' + (n * L + 2 * M) + ' ' + (n * L + 2 * M));
  ui.body.appendChild(svg);
  const on = new Set();
  const clave = (t, x, y) => t + x + ',' + y;
  let resuelto = false;
  function lado(t, x, y) {
    const x1 = M + x * L, y1 = M + y * L, x2 = t === 'h' ? x1 + L : x1, y2 = t === 'v' ? y1 + L : y1;
    const vis = document.createElementNS(NS, 'line');
    [['x1', x1], ['y1', y1], ['x2', x2], ['y2', y2]].forEach(([k, v]) => vis.setAttribute(k, v)); vis.setAttribute('class', 'lado');
    const hit = document.createElementNS(NS, 'line');
    [['x1', x1], ['y1', y1], ['x2', x2], ['y2', y2]].forEach(([k, v]) => hit.setAttribute(k, v)); hit.setAttribute('class', 'hit');
    hit.dataset.k = clave(t, x, y);
    hit.addEventListener('click', () => {
      if (resuelto) return;
      const k = clave(t, x, y);
      on.has(k) ? on.delete(k) : on.add(k);
      vis.classList.toggle('on', on.has(k)); ui.say('');
      svg.dataset.lados = [...on].sort().join(';');
    });
    svg.appendChild(vis); svg.appendChild(hit);
  }
  for (let y = 0; y <= n; y++) for (let x = 0; x < n; x++) lado('h', x, y);
  for (let y = 0; y < n; y++) for (let x = 0; x <= n; x++) lado('v', x, y);
  for (let y = 0; y <= n; y++) for (let x = 0; x <= n; x++) {
    const c = document.createElementNS(NS, 'circle'); c.setAttribute('cx', M + x * L); c.setAttribute('cy', M + y * L); c.setAttribute('r', '4'); c.setAttribute('fill', '#ffe6d6'); c.style.pointerEvents = 'none';
    svg.appendChild(c);
  }
  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    const sol = new Set(D.solucion.map(([t, x, y]) => clave(t, x, y)));
    if (on.size === sol.size && [...on].every(k => sol.has(k))) {
      resuelto = true;
      ui.say('El anillo se cierra y el circuito del reactor se llena de luz naranja. Coged la carta 58.', 'ok');
    } else ui.say(on.size ? 'El circuito no cuadra: o no es un solo bucle cerrado, o algún número no ve los lados que pide (cartas 61, 63 y 26).' : 'Todavía no hay ningún cable trazado.', 'bad');
  });
  ui.button('Borrar todo', 'ghost', () => { if (!resuelto) { on.clear(); svg.querySelectorAll('.lado').forEach(l => l.classList.remove('on')); ui.say(''); } });
  return { close: ui.close };
}
