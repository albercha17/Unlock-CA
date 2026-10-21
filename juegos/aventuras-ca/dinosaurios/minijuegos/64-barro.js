// Carta 64 — La balsa en el barro: la balsa resbala en línea recta hasta chocar con una roca o con la orilla (carta 67). Hay que pararla
// justo en la boca de la cueva, que solo está dibujada en la carta 66. Mínimo de empujones en instancias_dinosaurios.py (BARRO).
import { openGame } from './ui.js';
import { estilo, rejilla, flechas, DIRS } from './valle.js';

const D = /*DATOS*/{"n": 7, "rocas": [[1, 6], [3, 0], [3, 1], [3, 3], [3, 4], [4, 3], [5, 0], [5, 2], [6, 0]], "inicio": [0, 6], "cueva": [4, 2], "minimo": 7, "solucion": ["arriba", "derecha", "abajo", "derecha", "arriba", "izquierda", "abajo"]}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 64 — La balsa en el barro', instr: 'Empujad la balsa con las flechas. En este barro no frena: resbala hasta que choca. Hay que dejarla parada en la boca de la cueva.', ...opts });
  estilo('dn-barro', `.bar .dn-cel{background:#8a6a44}.bar .dn-cel.roca{background:radial-gradient(circle,#a8a8a0 40%,#5a5a52 70%)}.bar .dn-cel.balsa{background:#d8a050;outline:3px solid #ffe08a}`);
  const rocas = new Set(D.rocas.map(([x, y]) => x + ',' + y));
  let pos = D.inicio.slice(), empujones = 0, resuelto = false;
  const r = rejilla(D.n, () => {}, false);
  r.el.classList.add('bar');
  const pie = document.createElement('p'); pie.className = 'dn-pie';
  ui.body.append(r.el, pie);
  function pintar() {
    for (let y = 0; y < D.n; y++) for (let x = 0; x < D.n; x++) {
      const k = x + ',' + y, c = r.celda(x, y);
      c.disabled = true;
      c.className = 'dn-cel' + (rocas.has(k) ? ' roca' : '') + (k === pos.join(',') ? ' balsa' : '');
    }
    pie.textContent = 'Empujones: ' + empujones;
    r.el.dataset.pos = pos.join(',');
  }
  ui.body.appendChild(flechas(d => {
    if (resuelto) return;
    const [dx, dy] = DIRS[d];
    let [x, y] = pos;
    while (x + dx >= 0 && y + dy >= 0 && x + dx < D.n && y + dy < D.n && !rocas.has((x + dx) + ',' + (y + dy))) { x += dx; y += dy; }
    if (x === pos[0] && y === pos[1]) { ui.say('Por ahí la balsa no se mueve: está pegada a una roca o a la orilla.', 'bad'); return; }
    pos = [x, y]; empujones++; ui.say(''); pintar();
    if (x === D.cueva[0] && y === D.cueva[1]) {
      resuelto = true;
      ui.say('La balsa se detiene en la boca de la cueva. Al fondo, entre raíces, brilla algo azul: ¡el núcleo del Cronoportal! Coged la carta 62.', 'ok');
    }
  }));
  ui.button('Volver a la orilla', '', () => { if (!resuelto) { pos = D.inicio.slice(); empujones = 0; ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
