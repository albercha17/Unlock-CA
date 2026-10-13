// Carta 54 — Caja de Pacioli: cuadrado mágico 4×4 con los números 1..16 (cada fila, columna y diagonal suma 34).
// Casillas bloqueadas en la app: 16 (fila 1, col. 1), 2 (fila 1, col. 3) y 4 (fila 4, col. 1).
// El boceto de Pacioli (carta 56) añade: 3 (fila 1, col. 2), 10 (fila 2, col. 2) y 7 (fila 3, col. 3). Con esos seis datos la solución es única.
import { openGame } from './ui.js';

const SOLUCION = [16, 3, 2, 13, 5, 10, 11, 8, 9, 6, 7, 12, 4, 15, 14, 1];
const BLOQUEADAS = { 0: 16, 2: 2, 12: 4 };
const LINEAS = [
  [0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15],       // filas
  [0, 4, 8, 12], [1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15],       // columnas
  [0, 5, 10, 15], [3, 6, 9, 12]                                       // diagonales
];

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 54 — Caja de Pacioli',
    instr: 'Llena el cuadrado con los números del 1 al 16, sin repetir, para que todas las filas, columnas y diagonales sumen lo mismo.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .far-q-malla{display:grid;grid-template-columns:repeat(4,58px) 50px;grid-auto-rows:58px;gap:5px;justify-content:center;margin-bottom:6px}
    .far-q-malla .sumas{height:34px}
    .far-q-cell{border-radius:9px;border:2px solid #8a5a2a;background:linear-gradient(180deg,#d9b46a,#b88f45);color:#2a1600;font-size:1.5rem;font-weight:800;cursor:pointer;font-family:inherit}
    .far-q-cell.sel{outline:3px solid #fff;outline-offset:1px}
    .far-q-cell.fija{background:linear-gradient(180deg,#7a5a30,#5a3f1e);color:#f4e9c8;cursor:default}
    .far-q-suma{display:flex;align-items:center;justify-content:center;font-weight:700;font-size:1rem;border-radius:8px;color:#9fb4c8;background:rgba(255,255,255,.04)}
    .far-q-suma.ok{color:#9dffb0;background:rgba(80,200,120,.15)}
    .far-q-suma.mal{color:#ffb3b3;background:rgba(220,80,80,.15)}
    .far-q-diag{display:flex;gap:10px;justify-content:center;margin-bottom:10px}
    .far-q-diag .far-q-suma{padding:5px 12px}
    .far-q-nums{display:grid;grid-template-columns:repeat(8,1fr);gap:5px;margin-bottom:6px}
    .far-q-num{padding:9px 0;border-radius:8px;border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.07);color:#fff;font-weight:700;cursor:pointer;font-family:inherit}
    .far-q-num.usado{opacity:.4}
  `;
  ui.body.appendChild(style);

  const malla = document.createElement('div');
  malla.className = 'far-q-malla';
  const diag = document.createElement('div');
  diag.className = 'far-q-diag';
  const nums = document.createElement('div');
  nums.className = 'far-q-nums';
  ui.body.append(malla, diag, nums);

  const valores = Array(16).fill(0);
  Object.keys(BLOQUEADAS).forEach(i => { valores[i] = BLOQUEADAS[i]; });
  let sel = null;
  let resuelto = false;

  function estadoLinea(l) {
    const v = l.map(i => valores[i]);
    const completa = v.every(x => x > 0);
    const suma = v.reduce((a, b) => a + b, 0);
    return { completa, suma, ok: completa && suma === 34 };
  }

  function sumaEl(l, extra) {
    const e = estadoLinea(l);
    const d = document.createElement('div');
    d.className = 'far-q-suma' + (extra ? ' ' + extra : '') + (e.completa ? (e.ok ? ' ok' : ' mal') : '');
    d.textContent = e.completa ? String(e.suma) : '?';
    return d;
  }

  function pintar() {
    malla.innerHTML = '';
    for (let f = 0; f < 4; f++) {
      for (let c = 0; c < 4; c++) {
        const i = f * 4 + c;
        const b = document.createElement('button');
        b.type = 'button';
        b.className = 'far-q-cell' + (BLOQUEADAS[i] ? ' fija' : '') + (sel === i ? ' sel' : '');
        b.dataset.i = String(i);
        b.textContent = valores[i] ? String(valores[i]) : '';
        b.setAttribute('aria-label', 'Fila ' + (f + 1) + ', columna ' + (c + 1));
        b.addEventListener('click', () => { if (!resuelto && !BLOQUEADAS[i]) { sel = sel === i ? null : i; pintar(); } });
        malla.appendChild(b);
      }
      malla.appendChild(sumaEl(LINEAS[f]));
    }
    for (let c = 0; c < 4; c++) malla.appendChild(sumaEl(LINEAS[4 + c], 'sumas'));
    malla.appendChild(document.createElement('div'));
    diag.innerHTML = '';
    const a = sumaEl(LINEAS[8]); a.textContent = '↘ ' + a.textContent;
    const b = sumaEl(LINEAS[9]); b.textContent = '↙ ' + b.textContent;
    diag.append(a, b);
    nums.innerHTML = '';
    for (let n = 1; n <= 16; n++) {
      const x = document.createElement('button');
      x.type = 'button';
      x.className = 'far-q-num' + (valores.includes(n) ? ' usado' : '');
      x.dataset.n = String(n);
      x.textContent = String(n);
      x.addEventListener('click', () => poner(n));
      nums.appendChild(x);
    }
  }

  function poner(n) {
    if (resuelto) return;
    if (sel === null) { ui.say('Toca primero una casilla vacía del cuadrado.', 'bad'); return; }
    if (Object.values(BLOQUEADAS).includes(n)) { ui.say('El ' + n + ' ya está fijo en la caja.', 'bad'); return; }
    const antes = valores.indexOf(n);
    if (antes >= 0 && !BLOQUEADAS[antes]) valores[antes] = 0;   // se mueve de sitio
    valores[sel] = n;
    ui.say('');
    pintar();
  }

  ui.button('Borrar casilla', 'ghost', () => {
    if (resuelto || sel === null || BLOQUEADAS[sel]) return;
    valores[sel] = 0;
    pintar();
  });
  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    if (valores.some(v => v === 0)) { ui.say('Aún quedan casillas vacías. Fijaos en las sumas de las líneas ya completas.', 'bad'); return; }
    const mal = LINEAS.filter(l => !estadoLinea(l).ok).length;
    if (mal === 0) {
      resuelto = true;
      ui.say('¡Todas las líneas suman lo mismo! La caja de Pacioli se abre y dentro brilla la lente maestra de Leonardo. Coged la carta 62.', 'ok');
    } else {
      ui.say('Hay ' + mal + (mal === 1 ? ' línea' : ' líneas') + ' que no suma' + (mal === 1 ? '' : 'n') + ' lo mismo (en rojo). Revisad esos números.', 'bad');
    }
  });

  pintar();
  return { close: ui.close };
}
