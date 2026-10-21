// Carta 48 — El cuadro de apuestas (Kakuro): rellenar con cifras del 1 al 9 las casillas blancas para que cada racha, hacia la derecha o hacia abajo, sume lo
// que dice su número y no repita cifra. El cuadro con los números, en las cartas 42 y 49 (dos mitades); la regla, en la 53. Aquí solo se ve la forma del cuadro.
// Vale cualquier relleno correcto (instancias_oeste.py, KAKURO, solución única).
import { openGame } from './ui.js';
import { estilo, rejilla } from './comun.js';

const D = /*DATOS*/{"n": 6, "blancas": [[1, 2], [1, 3], [2, 2], [2, 3], [2, 4], [3, 3], [3, 4], [3, 5], [4, 1], [4, 2], [4, 4], [4, 5], [5, 1], [5, 2], [5, 4], [5, 5]], "tandas": [{"tipo": "h", "r": 1, "c": 2, "largo": 2, "suma": 3}, {"tipo": "h", "r": 2, "c": 2, "largo": 3, "suma": 11}, {"tipo": "h", "r": 3, "c": 3, "largo": 3, "suma": 12}, {"tipo": "h", "r": 4, "c": 1, "largo": 2, "suma": 16}, {"tipo": "h", "r": 4, "c": 4, "largo": 2, "suma": 17}, {"tipo": "h", "r": 5, "c": 1, "largo": 2, "suma": 10}, {"tipo": "h", "r": 5, "c": 4, "largo": 2, "suma": 11}, {"tipo": "v", "r": 4, "c": 1, "largo": 2, "suma": 17}, {"tipo": "v", "r": 1, "c": 2, "largo": 2, "suma": 3}, {"tipo": "v", "r": 4, "c": 2, "largo": 2, "suma": 9}, {"tipo": "v", "r": 1, "c": 3, "largo": 3, "suma": 19}, {"tipo": "v", "r": 2, "c": 4, "largo": 4, "suma": 14}, {"tipo": "v", "r": 3, "c": 5, "largo": 3, "suma": 18}]}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 48 — El cuadro de apuestas', instr: 'Elegid una casilla blanca y tocad una cifra para ponerla. Los números de las rachas están en las cartas 42 y 49; la regla, en la 53.', ...opts });
  estilo('oe-kak', `.kak .oe-cel{font-size:1.3rem}.kak .oe-cel.negra{background:#2a1a10;cursor:default}.kak .oe-cel.sel{outline:3px solid #b03a2e}.kak-nums{display:grid;grid-template-columns:repeat(9,1fr);gap:4px;max-width:340px;margin:8px auto}.kak-nums button{min-height:42px;border-radius:6px;border:2px solid #e0a040;background:linear-gradient(180deg,#8a5a2a,#4a2c14);color:#f5d48a;font:700 1rem Georgia,serif;cursor:pointer;padding:0}`);
  const n = D.n;
  const blancas = new Set(D.blancas.map(q => q.join(',')));
  const val = {};
  let sel = null, resuelto = false;
  const r = rejilla(n, n, (f, c) => { if (resuelto || !blancas.has(f + ',' + c)) return; sel = f + ',' + c; ui.say(''); pintar(); }, 'kak');
  const nums = document.createElement('div');
  nums.className = 'kak-nums';
  for (let d = 1; d <= 9; d++) {
    const b = document.createElement('button');
    b.type = 'button';
    b.dataset.n = String(d);
    b.textContent = String(d);
    b.addEventListener('click', () => {
      if (resuelto) return;
      if (!sel) { ui.say('Elegid primero una casilla blanca.', 'bad'); return; }
      val[sel] = d;
      ui.say('');
      pintar();
    });
    nums.appendChild(b);
  }
  r.el.setAttribute('aria-label', 'Cuadro de apuestas');
  ui.body.append(r.el, nums);
  function pintar() {
    for (let f = 0; f < n; f++) for (let c = 0; c < n; c++) {
      const k = f + ',' + c, b = r.celda(f, c);
      b.classList.toggle('negra', !blancas.has(k));
      b.classList.toggle('sel', sel === k);
      b.textContent = val[k] ? String(val[k]) : '';
      b.dataset.v = val[k] ? String(val[k]) : '';
    }
  }
  function celdasDe(t) {
    const cs = [];
    for (let i = 0; i < t.largo; i++) cs.push(t.tipo === 'h' ? t.r + ',' + (t.c + i) : (t.r + i) + ',' + t.c);
    return cs;
  }
  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    if (D.blancas.some(q => !val[q.join(',')])) { ui.say('Quedan casillas blancas sin cifra.', 'bad'); return; }
    for (const t of D.tandas) {
      const v = celdasDe(t).map(k => val[k]);
      if (new Set(v).size < v.length) { ui.say('Hay una racha con una cifra repetida.', 'bad'); return; }
    }
    const malas = D.tandas.filter(t => celdasDe(t).reduce((a, k) => a + val[k], 0) !== t.suma).length;
    if (malas) { ui.say('El cuadro no cuadra: ' + malas + (malas === 1 ? ' racha no suma' : ' rachas no suman') + ' lo que dice su número.', 'bad'); return; }
    resuelto = true;
    ui.say('Todas las rachas suman lo que mandan y el tahúr suelta las cartas. Coged la carta 36.', 'ok');
  });
  ui.button('Borrar la casilla', 'ghost', () => { if (!resuelto && sel) { delete val[sel]; ui.say(''); pintar(); } });
  ui.button('Vaciar', 'ghost', () => { if (!resuelto) { Object.keys(val).forEach(k => delete val[k]); ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
