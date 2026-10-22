// Carta 46 — El marcador del jefe (cuadrado mágico 4 x 4): colocar los números del 1 al 16 sin repetir para que todas las filas, columnas y las dos
// diagonales sumen 34. Seis números ya puestos, en la carta 37; la regla, en la 39; las fichas que faltan, en la 33. Vale cualquier cuadrado correcto
// que respete los seis números (instancias_arcade.py, MAGICO).
import { openGame } from './ui.js';
import { estilo, rejilla } from './maquina.js';

const D = /*DATOS*/{"dados": [[1, 0, 10], [2, 0, 5], [1, 1, 7], [2, 2, 9], [2, 3, 8], [3, 3, 2]], "solucion": [[16, 10, 5, 3], [1, 7, 12, 14], [4, 6, 9, 15], [13, 11, 8, 2]]}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 46 — El marcador del jefe', instr: 'Elegid una casilla y tocad la ficha que queréis poner. Los dieciséis números del 1 al 16 van una vez cada uno. Los seis que ya están puestos se ven en la carta 37; la regla, en la 39.', ...opts });
  estilo('ar-cua', `
    .cua .ar-cel{font-size:1.2rem}.cua .ar-cel.sel{outline:3px solid #ffde46;background:#3a1458}.cua .ar-cel.fija{background:#0c3a52;color:#ffde46}
    .cua-fichas{display:grid;grid-template-columns:repeat(8,1fr);gap:5px;max-width:340px;margin:8px auto}
    .cua-num{min-height:40px;border-radius:8px;border:2px solid #ff5ad8;background:#1c0a30;color:#ffd6f6;font:700 .9rem system-ui;cursor:pointer;padding:0}
    .cua-num.usada{opacity:.35}
  `);
  const g = Array.from({ length: 4 }, () => Array(4).fill(0));
  const fija = new Set();
  let sel = null, resuelto = false;
  const r = rejilla(4, 4, (x, y) => { if (resuelto) return; sel = [x, y]; ui.say(''); pintar(); }, 'cua');
  const fichas = document.createElement('div');
  fichas.className = 'cua-fichas';
  const bt = [];
  for (let n = 1; n <= 16; n++) {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'cua-num';
    b.dataset.n = String(n);
    b.textContent = String(n);
    b.addEventListener('click', () => {
      if (resuelto) return;
      if (!sel) { ui.say('Elegid primero una casilla del marcador.', 'bad'); return; }
      const [x, y] = sel;
      if (fija.has(x + ',' + y)) { ui.say('Esa casilla ya viene puesta de fábrica.', 'bad'); return; }
      for (let j = 0; j < 4; j++) for (let i = 0; i < 4; i++) if (g[j][i] === n && !fija.has(i + ',' + j)) g[j][i] = 0;
      if (fija.size && [...fija].some(k => { const [i, j] = k.split(',').map(Number); return g[j][i] === n; })) { ui.say('El ' + n + ' ya está puesto en una casilla fija.', 'bad'); return; }
      g[y][x] = n;
      ui.say('');
      pintar();
      if (g.every(f => f.every(v => v))) comprobar();
    });
    bt.push(b);
    fichas.appendChild(b);
  }
  D.dados.forEach(([x, y, v]) => { g[y][x] = v; fija.add(x + ',' + y); });
  r.el.setAttribute('aria-label', 'Marcador de cuatro por cuatro');
  ui.body.append(r.el, fichas);
  function pintar() {
    for (let y = 0; y < 4; y++) for (let x = 0; x < 4; x++) {
      const c = r.celda(x, y);
      c.textContent = g[y][x] ? String(g[y][x]) : '';
      c.dataset.v = String(g[y][x]);
      c.classList.toggle('sel', !!sel && sel[0] === x && sel[1] === y);
      c.classList.toggle('fija', fija.has(x + ',' + y));
    }
    const puestos = new Set(g.flat());
    bt.forEach(b => b.classList.toggle('usada', puestos.has(Number(b.dataset.n))));
  }
  function comprobar() {
    if (resuelto) return;
    const lineas = [];
    for (let i = 0; i < 4; i++) { lineas.push(g[i]); lineas.push(g.map(f => f[i])); }
    lineas.push([0, 1, 2, 3].map(i => g[i][i]), [0, 1, 2, 3].map(i => g[i][3 - i]));
    if (g.flat().some(v => !v)) { ui.say('Faltan casillas por rellenar.', 'bad'); return; }
    if (new Set(g.flat()).size < 16) { ui.say('Hay números repetidos: del 1 al 16, uno de cada.', 'bad'); return; }
    const malas = lineas.filter(l => l.reduce((a, b) => a + b, 0) !== 34).length;
    if (malas) { ui.say('El marcador no cuadra: ' + malas + (malas === 1 ? ' línea no suma' : ' líneas no suman') + ' 34.', 'bad'); return; }
    resuelto = true;
    ui.say('Todas las filas, columnas y diagonales suman 34: el marcador se enciende. Coged la carta 56.', 'ok');
  }
  ui.button('Comprobar', 'primary', () => { if (!resuelto) comprobar(); });
  ui.button('Vaciar', 'ghost', () => {
    if (resuelto) return;
    for (let y = 0; y < 4; y++) for (let x = 0; x < 4; x++) if (!fija.has(x + ',' + y)) g[y][x] = 0;
    ui.say(''); pintar();
  });
  pintar();
  return { close: ui.close };
}
