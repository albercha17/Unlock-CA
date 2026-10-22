// Carta 46 — Los castillos del reino (Hashi): unir los castillos con puentes rectos para que cada uno tenga tantos como dice su número, sin cruces, con
// uno o dos puentes entre cada par, y todos conectados. Los números, en el mapa de las cartas 37 y 39 (dos mitades); el acertijo, en la 33.
// En la app los castillos solo llevan su letra. Solución única (instancias_trono.py, CAMINOS).
import { openGame } from './ui.js';
import { estilo, NS } from './reino.js';

const D = /*DATOS*/{"n": 9, "islas": [{"x": 8, "y": 1, "letra": "A"}, {"x": 5, "y": 3, "letra": "B"}, {"x": 8, "y": 3, "letra": "C"}, {"x": 2, "y": 4, "letra": "D"}, {"x": 4, "y": 4, "letra": "E"}, {"x": 3, "y": 6, "letra": "F"}, {"x": 4, "y": 6, "letra": "G"}, {"x": 5, "y": 6, "letra": "H"}, {"x": 8, "y": 6, "letra": "I"}, {"x": 2, "y": 8, "letra": "J"}, {"x": 4, "y": 8, "letra": "K"}], "puentes": [[[4, 4], [4, 6], 2], [[4, 6], [4, 8], 1], [[2, 4], [2, 8], 1], [[8, 1], [8, 3], 2], [[4, 6], [5, 6], 2], [[2, 4], [4, 4], 2], [[5, 6], [8, 6], 1], [[2, 8], [4, 8], 2], [[5, 3], [5, 6], 2], [[3, 6], [4, 6], 2], [[5, 3], [8, 3], 1]]}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 46 — Los castillos del reino', instr: 'Tocad un castillo y luego otro para tender un puente entre ellos (otra vez para un segundo puente, y otra para quitarlos). Los números de cada castillo, en las cartas 37, 39 y 33.', ...opts });
  estilo('tr-cam', `.cam-svg{display:block;width:min(90vw,340px);margin:10px auto;background:#1c2a38;border-radius:10px}.cam-isla{cursor:pointer}`);
  const n = D.n, L = 36, M = 18;
  const svg = document.createElementNS(NS, 'svg'); svg.setAttribute('class', 'cam-svg'); svg.setAttribute('viewBox', '0 0 ' + (n * L + 2 * M) + ' ' + (n * L + 2 * M));
  ui.body.appendChild(svg);
  const lde = {}; D.islas.forEach(i => { lde[i.letra] = i; });
  const puentes = {};                   // 'A-B' -> 0, 1 o 2
  let sel = null, resuelto = false;
  const centro = i => [M + i.x * L + L / 2, M + i.y * L + L / 2];
  const clave = (a, b) => [a, b].sort().join('-');
  function vecinas(a, b) {
    const A = lde[a], B = lde[b];
    if (A.x !== B.x && A.y !== B.y) return false;
    return !D.islas.some(i => i.letra !== a && i.letra !== b && ((A.x === B.x && i.x === A.x && i.y > Math.min(A.y, B.y) && i.y < Math.max(A.y, B.y)) ||
      (A.y === B.y && i.y === A.y && i.x > Math.min(A.x, B.x) && i.x < Math.max(A.x, B.x))));
  }
  function cruza(a, b) {
    const A = lde[a], B = lde[b];
    return Object.keys(puentes).some(k => {
      if (!puentes[k]) return false;
      const [c, d] = k.split('-'); if ([a, b].includes(c) || [a, b].includes(d)) return false;
      const C = lde[c], E = lde[d];
      const hor1 = A.y === B.y, hor2 = C.y === E.y;
      if (hor1 === hor2) return false;
      const [h1, h2, v1, v2] = hor1 ? [A, B, C, E] : [C, E, A, B];
      return Math.min(h1.x, h2.x) < v1.x && v1.x < Math.max(h1.x, h2.x) && Math.min(v1.y, v2.y) < h1.y && h1.y < Math.max(v1.y, v2.y);
    });
  }
  function pintar() {
    svg.innerHTML = '';
    Object.keys(puentes).forEach(k => {
      const c = puentes[k]; if (!c) return;
      const [a, b] = k.split('-'), A = centro(lde[a]), B = centro(lde[b]);
      const dx = A[0] === B[0] ? 3 : 0, dy = A[1] === B[1] ? 3 : 0;
      (c === 2 ? [-1, 1] : [0]).forEach(s => {
        const l = document.createElementNS(NS, 'line');
        l.setAttribute('x1', A[0] + dx * s); l.setAttribute('y1', A[1] + dy * s); l.setAttribute('x2', B[0] + dx * s); l.setAttribute('y2', B[1] + dy * s);
        l.setAttribute('stroke', '#e6f1fb'); l.setAttribute('stroke-width', '2.4'); svg.appendChild(l);
      });
    });
    D.islas.forEach(i => {
      const [cx, cy] = centro(i);
      const g = document.createElementNS(NS, 'g'); g.setAttribute('class', 'cam-isla'); g.dataset.l = i.letra;
      const c = document.createElementNS(NS, 'circle'); c.setAttribute('cx', cx); c.setAttribute('cy', cy); c.setAttribute('r', '13'); c.setAttribute('fill', sel === i.letra ? '#8fc7ee' : '#5d7288'); c.setAttribute('stroke', '#0c121a'); c.setAttribute('stroke-width', '2');
      const t = document.createElementNS(NS, 'text'); t.setAttribute('x', cx); t.setAttribute('y', cy + 5); t.setAttribute('text-anchor', 'middle'); t.setAttribute('font-size', '13'); t.setAttribute('font-weight', '800'); t.setAttribute('fill', sel === i.letra ? '#0c121a' : '#e6f1fb'); t.textContent = i.letra;
      g.append(c, t);
      g.addEventListener('click', () => toca(i.letra));
      svg.appendChild(g);
    });
    svg.dataset.puentes = Object.keys(puentes).filter(k => puentes[k]).sort().map(k => k + ':' + puentes[k]).join(',');
  }
  function toca(l) {
    if (resuelto) return;
    if (!sel) { sel = l; pintar(); return; }
    if (sel === l) { sel = null; pintar(); return; }
    const a = sel; sel = null;
    if (!vecinas(a, l)) { ui.say('Entre ' + a + ' y ' + l + ' no se puede tender un puente recto sin pasar por otro castillo.', 'bad'); pintar(); return; }
    const k = clave(a, l);
    if (!puentes[k] && cruza(a, l)) { ui.say('Ese puente cruzaría otro: los puentes no se cruzan (carta 33).', 'bad'); pintar(); return; }
    puentes[k] = ((puentes[k] || 0) + 1) % 3;
    ui.say(''); pintar();
  }
  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    const sol = {};
    D.puentes.forEach(([a, b, c]) => {
      const la = D.islas.find(i => i.x === a[0] && i.y === a[1]).letra, lb = D.islas.find(i => i.x === b[0] && i.y === b[1]).letra;
      sol[clave(la, lb)] = c;
    });
    const mios = Object.keys(puentes).filter(k => puentes[k]);
    if (mios.length === Object.keys(sol).length && mios.every(k => sol[k] === puentes[k])) {
      resuelto = true;
      ui.say('Todos los castillos quedan unidos con los puentes justos y se abre el paso hacia el salón del consejo. Coged la carta 56.', 'ok');
    } else ui.say('Algún castillo no tiene los puentes que dice su número, o hay castillos sin conectar (cartas 37, 39 y 33).', 'bad');
  });
  ui.button('Quitar todos', 'ghost', () => { if (!resuelto) { Object.keys(puentes).forEach(k => { puentes[k] = 0; }); sel = null; ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
