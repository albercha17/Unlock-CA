// Carta 69 — El pozo del jefe: llenar el pozo del todo con las piezas que dice la hoja de piezas (carta 70). Las piezas se pueden girar, no darles la vuelta.
// Instancia (herramientas/instancias_arcade.py): pozo de 4 x 6 con 4 casillas ocupadas; piezas: I, J, O, O y T (solución única).
import { openGame } from './ui.js';

const FILAS = 4;
const COLS = 6;
const BLOQUEADAS = [[1, 0], [2, 4], [2, 5], [3, 2]];
const PIEZAS = { I: 1, J: 1, O: 2, T: 1 };
const BASE = {
  I: [[0, 0], [0, 1], [0, 2], [0, 3]], O: [[0, 0], [0, 1], [1, 0], [1, 1]], T: [[0, 0], [0, 1], [0, 2], [1, 1]],
  S: [[0, 1], [0, 2], [1, 0], [1, 1]], Z: [[0, 0], [0, 1], [1, 1], [1, 2]], J: [[0, 0], [1, 0], [1, 1], [1, 2]], L: [[0, 2], [1, 0], [1, 1], [1, 2]]
};
const COLOR = { I: '#28e6ff', O: '#ffe23c', T: '#9650ff', S: '#46ff82', Z: '#ff4246', J: '#3c6eff', L: '#ff8e28' };

function normalizar(celdas) {
  const mr = Math.min(...celdas.map(x => x[0]));
  const mc = Math.min(...celdas.map(x => x[1]));
  return celdas.map(([r, c]) => [r - mr, c - mc]).sort((a, b) => a[0] - b[0] || a[1] - b[1]);
}
function girar(celdas) { return normalizar(celdas.map(([r, c]) => [c, -r])); }   // 90° en el sentido de las agujas del reloj
function forma(tipo, giros) {
  let c = normalizar(BASE[tipo]);
  for (let i = 0; i < giros; i++) c = girar(c);
  return c;
}

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 69 — El pozo del jefe',
    instr: 'Elige una pieza, gírala y toca la casilla de arriba a la izquierda donde va. Toca una pieza puesta para quitarla. Usa las piezas de la hoja.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .arc-pozo{display:grid;grid-template-columns:repeat(6,1fr);gap:2px;max-width:300px;margin:4px auto 10px;padding:6px;border-radius:10px;border:2px solid #9650ff;background:#07040f}
    .arc-hueco{aspect-ratio:1;border-radius:3px;border:1px solid #20204a;background:#10102a;padding:0;cursor:pointer;font:700 .8rem system-ui,sans-serif;color:#07040f}
    .arc-hueco.fijo{background:#555a80;border-color:#3a3e60;cursor:default}
    .arc-pozo.ok .arc-hueco{box-shadow:0 0 6px #9dffb0}
    .arc-paleta{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;max-width:330px;margin:0 auto 10px}
    .arc-pieza{display:flex;flex-direction:column;align-items:center;gap:3px;padding:5px 7px;border-radius:8px;border:2px solid #4a3a7a;background:#1a0e30;color:#e8dcff;font:700 .8rem system-ui,sans-serif;cursor:pointer}
    .arc-pieza.sel{border-color:#fff;background:#3a2060}
    .arc-mini{display:grid;gap:1px}
    .arc-mini i{display:block;width:8px;height:8px;border-radius:1px}
  `;
  ui.body.appendChild(style);

  const pozo = document.createElement('div');
  pozo.className = 'arc-pozo';
  const paleta = document.createElement('div');
  paleta.className = 'arc-paleta';
  ui.body.appendChild(pozo);
  ui.body.appendChild(paleta);

  const fijas = new Set(BLOQUEADAS.map(([r, c]) => r + ',' + c));
  let puestas = [];                 // { tipo, celdas: ['r,c', ...] }
  let tipo = 'I';
  let giros = 0;
  let resuelto = false;

  function ocupada(k) { return puestas.findIndex(p => p.celdas.includes(k)); }

  function pintarPozo() {
    pozo.className = 'arc-pozo' + (resuelto ? ' ok' : '');
    pozo.innerHTML = '';
    for (let r = 0; r < FILAS; r++) {
      for (let c = 0; c < COLS; c++) {
        const k = r + ',' + c;
        const b = document.createElement('button');
        b.type = 'button';
        b.dataset.r = String(r);
        b.dataset.c = String(c);
        const i = ocupada(k);
        b.className = 'arc-hueco' + (fijas.has(k) ? ' fijo' : '');
        if (i >= 0) { b.style.background = COLOR[puestas[i].tipo]; b.textContent = puestas[i].tipo; }
        b.setAttribute('aria-label', 'Casilla fila ' + (r + 1) + ' columna ' + (c + 1) + (fijas.has(k) ? ' (ocupada)' : i >= 0 ? ' (pieza ' + puestas[i].tipo + ')' : ' (libre)'));
        b.addEventListener('click', () => tocar(r, c));
        pozo.appendChild(b);
      }
    }
  }

  function pintarPaleta() {
    paleta.innerHTML = '';
    Object.keys(BASE).forEach(t => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'arc-pieza' + (t === tipo ? ' sel' : '');
      b.dataset.t = t;
      b.setAttribute('aria-label', 'Pieza ' + t);
      const f = forma(t, t === tipo ? giros : 0);
      const filas = Math.max(...f.map(x => x[0])) + 1, cols = Math.max(...f.map(x => x[1])) + 1;
      let mini = '<span class="arc-mini" style="grid-template-columns:repeat(' + cols + ',8px)">';
      for (let r = 0; r < filas; r++) for (let c = 0; c < cols; c++) mini += '<i style="background:' + (f.some(x => x[0] === r && x[1] === c) ? COLOR[t] : 'transparent') + '"></i>';
      b.innerHTML = mini + '</span><span>' + t + '</span>';
      b.addEventListener('click', () => { if (!resuelto) { tipo = t; giros = 0; ui.say(''); pintarPaleta(); } });
      paleta.appendChild(b);
    });
  }

  function tocar(r, c) {
    if (resuelto) return;
    const k = r + ',' + c;
    if (fijas.has(k)) return;
    const i = ocupada(k);
    if (i >= 0) { puestas.splice(i, 1); ui.say(''); pintarPozo(); return; }
    const celdas = forma(tipo, giros).map(([dr, dc]) => [r + dr, c + dc]);
    if (celdas.some(([rr, cc]) => rr >= FILAS || cc >= COLS || fijas.has(rr + ',' + cc) || ocupada(rr + ',' + cc) >= 0)) {
      ui.say('Esa pieza no cabe ahí: se sale del pozo o choca con otra.', 'bad');
      return;
    }
    puestas.push({ tipo, celdas: celdas.map(([rr, cc]) => rr + ',' + cc) });
    ui.say('');
    pintarPozo();
  }

  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    const llenas = puestas.reduce((n, p) => n + p.celdas.length, 0) + fijas.size;
    if (llenas < FILAS * COLS) { ui.say('Todavía quedan huecos en el pozo.', 'bad'); return; }
    const cuenta = {};
    puestas.forEach(p => { cuenta[p.tipo] = (cuenta[p.tipo] || 0) + 1; });
    const bien = Object.keys(PIEZAS).every(t => cuenta[t] === PIEZAS[t]) && Object.keys(cuenta).every(t => PIEZAS[t]);
    if (bien) {
      resuelto = true;
      pintarPozo();
      ui.say('¡LÍNEA COMPLETA! El pozo se llena y el jefe se desmorona en una lluvia de píxeles. Coged la carta 82.', 'ok');
    } else {
      ui.say('El pozo está lleno, pero no con las piezas de la hoja. Mirad cuántas hay de cada una (I, J, O y T) y volved a intentarlo.', 'bad');
    }
  });
  ui.button('Girar', '', () => { if (!resuelto) { giros = (giros + 1) % 4; pintarPaleta(); } });
  ui.button('Vaciar', '', () => { if (!resuelto) { puestas = []; ui.say(''); pintarPozo(); } });

  pintarPozo();
  pintarPaleta();
  return { close: ui.close };
}
