// Carta 51 — La bodega de barriles (Sokoban): empujar tres barriles hasta sus huecos del suelo. Los barriles solo se empujan, de uno en uno, hacia delante.
// Los huecos NO se ven aquí: están dibujados en las cartas 61 y 63 (dos mitades); el refrán del tabernero, en la 26. Vale cualquier solución
// (instancias_oeste.py, SOKOBAN). Coordenada de Polibio: D.coord.
import { openGame } from './ui.js';
import { estilo } from './comun.js';

const D = /*DATOS*/{"filas": 6, "cols": 8, "muros": [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [1, 0], [1, 1], [1, 7], [2, 0], [2, 1], [2, 7], [3, 0], [3, 1], [3, 7], [4, 0], [4, 4], [4, 7], [5, 0], [5, 1], [5, 2], [5, 3], [5, 4], [5, 5], [5, 6], [5, 7]], "metas": [[2, 6], [3, 4], [4, 3]], "cajas": [[2, 5], [3, 4], [3, 5]], "jugador": [4, 1], "coord": "42"}/*FIN*/;
const MOV = { U: [-1, 0], D: [1, 0], L: [0, -1], R: [0, 1] };

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 51 — La bodega de barriles', instr: 'Moved al tabernero con las flechas y empujad los barriles hasta los huecos del suelo. Los huecos están dibujados en las cartas 61 y 63; el refrán, en la 26.', ...opts });
  estilo('oe-bod', `
    .bod-tab{display:grid;gap:2px;width:min(88vw,360px);margin:8px auto;padding:6px;border-radius:8px;background:#3a2412;border:3px solid #8a5a2a}
    .bod-c{aspect-ratio:1;border-radius:3px;background:#e6c88c;display:flex;align-items:center;justify-content:center;font-size:1.1rem;color:#3a2412;font-weight:800}
    .bod-c.muro{background:#5a3a1e}.bod-c.caja{background:#b0722e;border:3px solid #3a2412}.bod-c.yo{background:#f5d48a}.bod-c.yo::after{content:'';width:60%;height:60%;border-radius:50%;background:#b03a2e}
    .bod-flechas{display:grid;grid-template-columns:repeat(3,64px);grid-template-rows:repeat(2,50px);gap:6px;justify-content:center;margin:6px 0}
    .bod-flechas button{border-radius:8px;border:2px solid #e0a040;background:linear-gradient(180deg,#8a5a2a,#4a2c14);color:#f5d48a;font:700 1.3rem Georgia,serif;cursor:pointer}`);
  const F = D.filas, C = D.cols;
  const muros = new Set(D.muros.map(q => q.join(',')));
  const metas = new Set(D.metas.map(q => q.join(',')));
  let cajas, yo, hist, resuelto = false;
  function empezar() { cajas = new Set(D.cajas.map(q => q.join(','))); yo = D.jugador.slice(); hist = []; }
  empezar();
  const tab = document.createElement('div');
  tab.className = 'bod-tab';
  tab.style.gridTemplateColumns = 'repeat(' + C + ',1fr)';
  const celdas = [];
  for (let r = 0; r < F; r++) for (let c = 0; c < C; c++) { const e = document.createElement('div'); e.className = 'bod-c'; tab.appendChild(e); celdas.push(e); }
  const info = document.createElement('div');
  info.className = 'oe-pie';
  const flechas = document.createElement('div');
  flechas.className = 'bod-flechas';
  [['U', '↑', 2, 1], ['L', '←', 1, 2], ['D', '↓', 2, 2], ['R', '→', 3, 2]].forEach(([m, t, col, fila]) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'bod-mv';
    b.dataset.m = m;
    b.textContent = t;
    b.style.gridColumn = String(col);
    b.style.gridRow = String(fila);
    b.setAttribute('aria-label', 'Mover ' + m);
    b.addEventListener('click', () => mover(m));
    flechas.appendChild(b);
  });
  ui.body.append(tab, flechas, info);
  function pintar() {
    celdas.forEach((e, i) => {
      const r = Math.floor(i / C), c = i % C, k = r + ',' + c;
      e.className = 'bod-c' + (muros.has(k) ? ' muro' : '') + (cajas.has(k) ? ' caja' : '') + (yo[0] === r && yo[1] === c ? ' yo' : '');
    });
    const dentro = [...cajas].filter(k => metas.has(k)).length;
    info.textContent = 'Barriles encajados: ' + dentro + ' de ' + metas.size + ' · pasos: ' + hist.length;
    tab.dataset.encajados = String(dentro);
  }
  function mover(m) {
    if (resuelto) return;
    const [dr, dc] = MOV[m];
    const q = [yo[0] + dr, yo[1] + dc], k = q.join(',');
    if (q[0] < 0 || q[1] < 0 || q[0] >= F || q[1] >= C || muros.has(k)) return;
    const previo = { yo: yo.slice(), cajas: new Set(cajas) };
    if (cajas.has(k)) {
      const q2 = [q[0] + dr, q[1] + dc], k2 = q2.join(',');
      if (q2[0] < 0 || q2[1] < 0 || q2[0] >= F || q2[1] >= C || muros.has(k2) || cajas.has(k2)) { ui.say('El barril no se mueve: hay un muro u otro barril detrás.', 'bad'); return; }
      cajas.delete(k);
      cajas.add(k2);
    }
    yo = q;
    hist.push(previo);
    ui.say('');
    pintar();
    if ([...cajas].every(x => metas.has(x))) {
      resuelto = true;
      ui.say('Los tres barriles encajan en sus huecos con un clonc y el suelo se abre. Coordenada de Polibio: ' + D.coord + '. Coged la carta 58.', 'ok');
    }
  }
  document.addEventListener('keydown', function tecla(e) {
    const m = { ArrowUp: 'U', ArrowDown: 'D', ArrowLeft: 'L', ArrowRight: 'R' }[e.key];
    if (m && document.body.contains(tab)) { e.preventDefault(); mover(m); } else if (!document.body.contains(tab)) document.removeEventListener('keydown', tecla);
  });
  ui.button('Deshacer', 'ghost', () => { if (!resuelto && hist.length) { const h = hist.pop(); yo = h.yo; cajas = h.cajas; ui.say(''); pintar(); } });
  ui.button('Empezar de nuevo', 'ghost', () => { if (!resuelto) { empezar(); ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
