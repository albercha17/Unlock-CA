// Carta 40 — El skyline del casino (rascacielos 5×5): torres de 1 a 5 plantas, sin repetir en filas ni columnas, de modo que cada número del borde diga
// cuántas torres se ven desde allí. Las pistas del borde están repartidas en las cartas 41 (arriba e izquierda) y 43 (abajo y derecha); la regla, en la 45.
// Aquí solo se ve la rejilla vacía. Vale cualquier relleno correcto (instancias_espia.py, RASCACIELOS, solución única). Pulsaciones: D.pulsa.
import { openGame } from './ui.js';
import { rejilla, teclado } from './comun.js';

const D = /*DATOS*/{"n": 5, "pistas": {"N": [0, 0, 4, 0, 0], "S": [0, 0, 0, 3, 0], "O": [4, 3, 0, 3, 2], "E": [0, 0, 3, 0, 0]}, "solucion": [[2, 3, 1, 4, 5], [3, 4, 2, 5, 1], [5, 1, 4, 2, 3], [1, 2, 5, 3, 4], [4, 5, 3, 1, 2]], "pulsa": "2"}/*FIN*/;

function vistas(linea) {
  let m = 0, c = 0;
  for (const v of linea) if (v > m) { m = v; c++; }
  return c;
}

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 40 — El skyline del casino', instr: 'Elegid una casilla y tocad la altura de la torre (1 a 5). Los números del borde están en las cartas 41 y 43; la regla, en la 45.', ...opts });
  const n = D.n;
  const val = {};
  let sel = null, resuelto = false;
  const r = rejilla(n, n, (f, c) => { if (resuelto) return; sel = f + ',' + c; ui.say(''); pintar(); }, 'ras');
  r.el.setAttribute('aria-label', 'Skyline');
  const nums = teclado(1, n, d => {
    if (resuelto) return;
    if (!sel) { ui.say('Elegid primero una casilla.', 'bad'); return; }
    val[sel] = d;
    ui.say('');
    pintar();
  });
  ui.body.append(r.el, nums);
  function pintar() {
    for (let f = 0; f < n; f++) for (let c = 0; c < n; c++) {
      const k = f + ',' + c, b = r.celda(f, c);
      b.classList.toggle('sel', sel === k);
      b.textContent = val[k] ? String(val[k]) : '';
      b.dataset.v = val[k] ? String(val[k]) : '';
    }
  }
  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    const g = [];
    for (let f = 0; f < n; f++) {
      g.push([]);
      for (let c = 0; c < n; c++) g[f].push(val[f + ',' + c] || 0);
    }
    if (g.some(f => f.includes(0))) { ui.say('Quedan casillas sin torre.', 'bad'); return; }
    for (let i = 0; i < n; i++) {
      if (new Set(g[i]).size < n) { ui.say('Hay una fila con dos torres de la misma altura.', 'bad'); return; }
      if (new Set(g.map(f => f[i])).size < n) { ui.say('Hay una columna con dos torres de la misma altura.', 'bad'); return; }
    }
    let malas = 0;
    for (let i = 0; i < n; i++) {
      const col = g.map(f => f[i]);
      if (D.pistas.N[i] && vistas(col) !== D.pistas.N[i]) malas++;
      if (D.pistas.S[i] && vistas(col.slice().reverse()) !== D.pistas.S[i]) malas++;
      if (D.pistas.O[i] && vistas(g[i]) !== D.pistas.O[i]) malas++;
      if (D.pistas.E[i] && vistas(g[i].slice().reverse()) !== D.pistas.E[i]) malas++;
    }
    if (malas) { ui.say('El skyline no cuadra: ' + malas + (malas === 1 ? ' número del borde no coincide' : ' números del borde no coinciden') + ' con lo que se ve.', 'bad'); return; }
    resuelto = true;
    ui.say('Las torres se ven justo como dicen los planos y una trampilla se abre en la azotea. Teléfono rojo: pulsad ' + D.pulsa + '. Coged la carta 30.', 'ok');
  });
  ui.button('Borrar la casilla', 'ghost', () => { if (!resuelto && sel) { delete val[sel]; ui.say(''); pintar(); } });
  ui.button('Vaciar', 'ghost', () => { if (!resuelto) { Object.keys(val).forEach(k => delete val[k]); ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
