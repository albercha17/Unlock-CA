// Carta 40 — La caja del carro (pentominós): llenar un tablero de 5 x 6 con las seis piezas de cinco cuadros de la carta 45, cada una una sola vez, girada o
// dada la vuelta como haga falta. Dos piezas ya están puestas en el tablero de las cartas 41 y 43 (dos mitades). Se pintan las casillas con la letra de la
// pieza. Vale cualquier relleno correcto (instancias_oeste.py, PENTOMINO, único con las dos piezas puestas). Coordenada de Polibio: D.coord.
import { openGame } from './ui.js';
import { estilo, rejilla, COLORES } from './comun.js';

const D = /*DATOS*/{"filas": 5, "cols": 6, "piezas": ["P", "T", "Z", "V", "Y", "I"], "fijas": {"V": [[0, 3], [0, 4], [0, 5], [1, 5], [2, 5]], "T": [[0, 0], [0, 1], [0, 2], [1, 1], [2, 1]]}, "coord": "11"}/*FIN*/;
const FORMAS = {
  F: [[0, 1], [0, 2], [1, 0], [1, 1], [2, 1]], I: [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4]], L: [[0, 0], [1, 0], [2, 0], [3, 0], [3, 1]],
  N: [[0, 1], [1, 1], [2, 0], [2, 1], [3, 0]], P: [[0, 0], [0, 1], [1, 0], [1, 1], [2, 0]], T: [[0, 0], [0, 1], [0, 2], [1, 1], [2, 1]],
  U: [[0, 0], [0, 2], [1, 0], [1, 1], [1, 2]], V: [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2]], W: [[0, 0], [1, 0], [1, 1], [2, 1], [2, 2]],
  X: [[0, 1], [1, 0], [1, 1], [1, 2], [2, 1]], Y: [[0, 1], [1, 0], [1, 1], [2, 1], [3, 1]], Z: [[0, 0], [0, 1], [1, 1], [2, 1], [2, 2]]
};

function normal(cs) {
  const mr = Math.min(...cs.map(q => q[0])), mc = Math.min(...cs.map(q => q[1]));
  return cs.map(([r, c]) => [r - mr, c - mc]).sort((a, b) => a[0] - b[0] || a[1] - b[1]).map(q => q.join(',')).join(';');
}
function orientaciones(cs) {
  const res = new Set();
  let cur = cs;
  for (let e = 0; e < 2; e++) {
    for (let g = 0; g < 4; g++) { cur = cur.map(([r, c]) => [c, -r]); res.add(normal(cur)); }
    cur = cur.map(([r, c]) => [r, -c]);
  }
  return res;
}

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 40 — La caja del carro', instr: 'Elegid una letra y tocad casillas del tablero para pintarlas con esa pieza (tocad otra vez para borrar). Las seis piezas llenan el tablero entero. Las formas, en la carta 45; las dos piezas ya puestas, en las cartas 41 y 43.', ...opts });
  estilo('oe-caj', `.caj .oe-cel{color:#fff;font-size:1.2rem}.caj-pal{display:flex;gap:6px;justify-content:center;margin:8px 0}.caj-pal button{width:46px;height:46px;border-radius:8px;border:3px solid #3a2412;color:#fff;font:800 1.2rem Georgia,serif;cursor:pointer}.caj-pal button.sel{outline:3px solid #f5d48a}`);
  const F = D.filas, C = D.cols;
  const est = Array.from({ length: F }, () => Array(C).fill(''));
  let sel = 'A', resuelto = false;
  const letras = 'ABCDEF'.split('');
  const pal = document.createElement('div');
  pal.className = 'caj-pal';
  const botones = letras.map((l, i) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.dataset.p = l;
    b.textContent = l;
    b.style.background = COLORES[i];
    b.setAttribute('aria-label', 'Pieza ' + l);
    b.addEventListener('click', () => { sel = l; pintar(); });
    pal.appendChild(b);
    return b;
  });
  const r = rejilla(C, F, (f, c) => {
    if (resuelto) return;
    est[f][c] = est[f][c] === sel ? '' : sel;
    ui.say('');
    pintar();
  }, 'caj');
  function pintar() {
    botones.forEach(b => b.classList.toggle('sel', b.dataset.p === sel));
    for (let f = 0; f < F; f++) for (let c = 0; c < C; c++) {
      const b = r.celda(f, c);
      b.dataset.v = est[f][c];
      b.textContent = est[f][c];
      b.style.background = est[f][c] ? COLORES[letras.indexOf(est[f][c])] : '';
    }
  }
  ui.body.append(pal, r.el);
  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    if (est.some(f => f.some(v => !v))) { ui.say('Quedan casillas sin llenar en la caja.', 'bad'); return; }
    for (let k = 0; k < letras.length; k++) {
      const l = letras[k], pieza = D.piezas[k];
      const cs = [];
      est.forEach((f, i) => f.forEach((v, j) => { if (v === l) cs.push([i, j]); }));
      if (cs.length !== 5 || !orientaciones(FORMAS[pieza]).has(normal(cs))) { ui.say('La pieza ' + l + ' no tiene la forma que le toca (carta 45).', 'bad'); return; }
    }
    for (const [pz, cs] of Object.entries(D.fijas)) {
      const l = letras[D.piezas.indexOf(pz)];
      if (cs.some(([i, j]) => est[i][j] !== l)) { ui.say('La pieza ' + l + ' tiene que estar donde la dibujaron en las cartas 41 y 43.', 'bad'); return; }
    }
    resuelto = true;
    ui.say('Las seis piezas encajan y la caja cierra con un golpe seco. Coordenada de Polibio: ' + D.coord + '. Coged la carta 30.', 'ok');
  });
  ui.button('Borrar todo', 'ghost', () => { if (!resuelto) { est.forEach(f => f.fill('')); ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
