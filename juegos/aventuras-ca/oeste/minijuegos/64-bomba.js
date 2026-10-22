// Carta 64 — La bomba de agua (tuberías): girar los tubos del pozo hasta que todos queden unidos en una sola red sin extremos abiertos. Cinco tubos
// (mejor dicho, seis) tienen que quedar como los dibujó el fontanero en las cartas 66 y 67 (dos mitades). Vale cualquier red que cumpla todo eso
// (instancias_oeste.py, TUBERIAS: solución única con los tubos dibujados).
import { openGame } from './ui.js';
import { estilo } from './comun.js';

const D = /*DATOS*/{"n": 5, "tubos": [[6, 10, 10, 10, 8], [7, 14, 10, 10, 8], [1, 7, 14, 14, 12], [6, 13, 1, 1, 5], [1, 3, 10, 8, 1]], "inicio": [[12, 10, 10, 10, 1], [7, 11, 5, 5, 4], [8, 13, 13, 7, 12], [12, 14, 8, 1, 10], [2, 3, 5, 4, 8]], "fijas": [[1, 1, 14], [1, 2, 10], [1, 4, 8], [2, 2, 14], [3, 0, 6], [4, 3, 8]]}/*FIN*/;
const BITS = [[1, 0, -1], [2, 1, 0], [4, 0, 1], [8, -1, 0]];
const DIRS = [[1, -1, 0, 4], [2, 0, 1, 8], [4, 1, 0, 1], [8, 0, -1, 2]];

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 64 — La bomba de agua', instr: 'Tocad un tubo para girarlo un cuarto de vuelta. Tienen que quedar todos unidos en una sola red, sin ningún extremo abierto. Algunos tubos tienen que quedar como en el plano de las cartas 66 y 67.', ...opts });
  estilo('oe-bom', `.bom-tab{display:grid;gap:3px;width:min(86vw,340px);margin:8px auto;padding:6px;border-radius:8px;background:#3a2412;border:3px solid #8a5a2a}.bom-c{aspect-ratio:1;border:0;border-radius:3px;background:#e6c88c;padding:0;cursor:pointer;min-height:40px}.bom-c svg{width:100%;height:100%;display:block}`);
  const n = D.n;
  const m = D.inicio.map(f => f.slice());
  let resuelto = false;
  const tab = document.createElement('div');
  tab.className = 'bom-tab';
  tab.style.gridTemplateColumns = 'repeat(' + n + ',1fr)';
  const celdas = [];
  for (let r = 0; r < n; r++) for (let c = 0; c < n; c++) {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'bom-c';
    b.dataset.r = String(r);
    b.dataset.c = String(c);
    b.setAttribute('aria-label', 'Tubo fila ' + (r + 1) + ', columna ' + (c + 1));
    b.addEventListener('click', () => { if (resuelto) return; m[r][c] = ((m[r][c] << 1) | (m[r][c] >> 3)) & 15; ui.say(''); pintar(); });
    tab.appendChild(b);
    celdas.push(b);
  }
  ui.body.appendChild(tab);
  function dibujo(mask) {
    let s = '<svg viewBox="0 0 40 40" aria-hidden="true">';
    BITS.forEach(([b, dx, dy]) => { if (mask & b) s += '<line x1="20" y1="20" x2="' + (20 + dx * 20) + '" y2="' + (20 + dy * 20) + '" stroke="#3a2412" stroke-width="9" stroke-linecap="butt"/>'; });
    return s + '<circle cx="20" cy="20" r="6" fill="#3a2412"/></svg>';
  }
  function pintar() {
    celdas.forEach((b, i) => { const r = Math.floor(i / n), c = i % n; b.innerHTML = dibujo(m[r][c]); b.dataset.m = String(m[r][c]); });
  }
  function revisar() {
    for (let r = 0; r < n; r++) for (let c = 0; c < n; c++) {
      for (const [b, dr, dc, ob] of DIRS) {
        const abre = !!(m[r][c] & b);
        const r2 = r + dr, c2 = c + dc;
        const dentro = r2 >= 0 && c2 >= 0 && r2 < n && c2 < n;
        if (abre && (!dentro || !(m[r2][c2] & ob))) return 'Hay un tubo con el extremo abierto: el agua se escapa.';
      }
    }
    const vis = new Set(['0,0']);
    const pila = [[0, 0]];
    while (pila.length) {
      const [r, c] = pila.pop();
      for (const [b, dr, dc] of DIRS) {
        if (m[r][c] & b) { const k = (r + dr) + ',' + (c + dc); if (!vis.has(k)) { vis.add(k); pila.push([r + dr, c + dc]); } }
      }
    }
    if (vis.size < n * n) return 'Los tubos forman varias redes sueltas: tienen que quedar todos unidos.';
    for (const [r, c, mk] of D.fijas) if (m[r][c] !== mk) return 'Algún tubo no está como lo dibujó el fontanero en el plano (cartas 66 y 67).';
    return '';
  }
  ui.button('Abrir la llave', 'primary', () => {
    if (resuelto) return;
    const e = revisar();
    if (e) { ui.say(e, 'bad'); return; }
    resuelto = true;
    ui.say('El agua recorre toda la red de tubos y la bomba se pone en marcha. Coged la carta 62.', 'ok');
  });
  pintar();
  return { close: ui.close };
}
