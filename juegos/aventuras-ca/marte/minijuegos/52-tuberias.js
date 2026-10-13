// Carta 52 — Panel de oxígeno: girar tuberías para llevar el oxígeno de la entrada (izquierda) a la salida (derecha).
import { openGame } from './ui.js';

const COLS = 5, ROWS = 3;
const CONN = {
  S: [['W', 'E'], ['N', 'S']],
  C: [['N', 'E'], ['E', 'S'], ['S', 'W'], ['W', 'N']]
};
const DELTA = { N: [0, -1], E: [1, 0], S: [0, 1], W: [-1, 0] };
const OPP = { N: 'S', E: 'W', S: 'N', W: 'E' };
const IMG = './img/ui/tuberias/';
// [fila][columna] = tipo (S recta, C codo) y giro inicial
const GRID = [
  [{ t: 'C', r: 0 }, { t: 'C', r: 3 }, { t: 'S', r: 1 }, { t: 'C', r: 0 }, { t: 'S', r: 1 }],
  [{ t: 'S', r: 1 }, { t: 'C', r: 1 }, { t: 'S', r: 0 }, { t: 'S', r: 0 }, { t: 'C', r: 2 }],
  [{ t: 'S', r: 1 }, { t: 'C', r: 2 }, { t: 'C', r: 1 }, { t: 'C', r: 2 }, { t: 'C', r: 0 }]
];
const FILA_ENTRADA = 1;

function trazar() {
  const camino = [];
  let c = 0, r = FILA_ENTRADA, entrada = 'W';
  for (let i = 0; i < 30; i++) {
    if (c < 0 || c >= COLS || r < 0 || r >= ROWS) return { camino, ok: false };
    const celda = GRID[r][c];
    const con = CONN[celda.t][celda.r % CONN[celda.t].length];
    if (!con.includes(entrada)) return { camino, ok: false };
    camino.push(c + ',' + r);
    const salida = con[0] === entrada ? con[1] : con[0];
    if (c === COLS - 1 && r === FILA_ENTRADA && salida === 'E') return { camino, ok: true };
    c += DELTA[salida][0];
    r += DELTA[salida][1];
    entrada = OPP[salida];
  }
  return { camino, ok: false };
}

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 52 — Panel de oxígeno',
    instr: 'Toca las tuberías para girarlas hasta que el oxígeno llegue de la entrada a la salida.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .mar-tub{display:grid;grid-template-columns:1.1fr repeat(5,1fr) 1.1fr;grid-template-rows:repeat(3,1fr);gap:3px;max-width:350px;margin:0 auto 10px;padding:8px;border-radius:10px;border:2px solid #5b3a24;background:linear-gradient(rgba(10,14,20,.8),rgba(10,14,20,.92)),url(./img/ui/panel.jpg) center/cover;box-shadow:inset 0 0 24px rgba(0,0,0,.8)}
    .mar-celda{position:relative;aspect-ratio:1;padding:0;border:1px solid rgba(255,255,255,.06);border-radius:6px;background:#04080c;cursor:pointer;overflow:hidden;touch-action:manipulation}
    .mar-celda img{position:absolute;inset:0;width:100%;height:100%;object-fit:fill;mix-blend-mode:screen;pointer-events:none;transition:transform .25s ease,filter .4s}
    .mar-celda.agua img{filter:brightness(1.25) saturate(1.2) drop-shadow(0 0 5px #4cc9f0) hue-rotate(-12deg)}
    .mar-celda.agua{box-shadow:inset 0 0 14px rgba(76,201,240,.55)}
    .mar-extremo{position:relative;aspect-ratio:auto;display:flex;align-items:center;justify-content:center;overflow:hidden;border-radius:6px;background:#04080c}
    .mar-extremo img{width:100%;height:100%;object-fit:contain;mix-blend-mode:screen}
    .mar-extremo.ok img{filter:brightness(1.3) drop-shadow(0 0 8px #3fff8a)}
  `;
  ui.body.appendChild(style);

  const panel = document.createElement('div');
  panel.className = 'mar-tub';
  ui.body.appendChild(panel);

  const extremo = (src) => {
    const d = document.createElement('div');
    d.className = 'mar-extremo';
    d.innerHTML = '<img alt="" src="' + IMG + src + '.jpg">';
    return d;
  };
  const entrada = extremo('entrada');
  const salida = extremo('salida');
  const vacio = () => { const v = document.createElement('div'); return v; };

  const celdas = [];
  let resuelto = false;

  function giro(celda) {
    // recta: horizontal en r=0; codo: la imagen une izquierda y abajo (r=2)
    return celda.t === 'S' ? (celda.r % 2) * 90 : (celda.r - 2) * 90;
  }

  function construir() {
    panel.innerHTML = '';
    for (let r = 0; r < ROWS; r++) {
      if (r === FILA_ENTRADA) panel.appendChild(entrada); else panel.appendChild(vacio());
      for (let c = 0; c < COLS; c++) {
        const celda = GRID[r][c];
        const b = document.createElement('button');
        b.type = 'button';
        b.className = 'mar-celda';
        b.dataset.i = String(r * COLS + c);
        b.setAttribute('aria-label', 'Tubería ' + 'ABCDE'[c] + (r + 1));
        b.innerHTML = '<img alt="" src="' + IMG + (celda.t === 'S' ? 'recta' : 'codo') + '.jpg">';
        b.addEventListener('click', () => {
          if (resuelto) return;
          celda.r = (celda.r + 1) % CONN[celda.t].length;
          ui.say('');
          pintar();
        });
        panel.appendChild(b);
        celdas[r * COLS + c] = b;
      }
      if (r === FILA_ENTRADA) panel.appendChild(salida); else panel.appendChild(vacio());
    }
  }

  const angulos = [];
  function pintar() {
    const { camino, ok } = trazar();
    for (let r = 0; r < ROWS; r++) {
      for (let c = 0; c < COLS; c++) {
        const i = r * COLS + c;
        const b = celdas[i];
        const celda = GRID[r][c];
        // el ángulo se acumula para que el giro siempre sea en el mismo sentido (sin "rebobinar")
        const objetivo = giro(celda);
        let a = angulos[i] === undefined ? objetivo : angulos[i];
        while (((a % 360) + 360) % 360 !== ((objetivo % 360) + 360) % 360) a += 90;
        angulos[i] = a;
        b.querySelector('img').style.transform = 'rotate(' + a + 'deg)';
        b.classList.toggle('agua', camino.includes(c + ',' + r));
        b.style.cursor = resuelto ? 'default' : 'pointer';
      }
    }
    salida.classList.toggle('ok', ok);
    if (ok && !resuelto) {
      resuelto = true;
      ui.say('¡El oxígeno circula! El soporte vital se reactiva. Coged la carta 66.', 'ok');
    }
  }

  construir();
  pintar();
  return { close: ui.close };
}
