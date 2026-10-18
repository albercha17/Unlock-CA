// Carta 24 — El panel del radar: pulsar la casilla del cofre dorado (cartas 30 a 33 juntas). Columna = letra (arriba), fila = número (a la izquierda).
// Solución: F4.
import { openGame } from './ui.js';

const COLUMNAS = 'ABCDEFGH'.split('');
const FILAS = 6;
const SOLUCION = { c: 'F', f: 4 };

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 24 — El panel del radar',
    instr: 'Toca la casilla en la que está el cofre dorado del radar y pulsa Escanear. La letra es la columna y el número, la fila.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .arc-radar{display:grid;grid-template-columns:26px repeat(8,1fr);gap:3px;max-width:340px;margin:4px auto 12px;padding:10px;border-radius:10px;border:2px solid #28e6ff;background:#060a1c;box-shadow:inset 0 0 18px rgba(40,230,255,.3)}
    .arc-eje{display:flex;align-items:center;justify-content:center;color:#28e6ff;font:700 .85rem "Courier New",monospace}
    .arc-casilla{aspect-ratio:1;min-height:30px;border-radius:4px;border:1px solid #1a2a5c;background:#0b1230;padding:0;cursor:pointer}
    .arc-casilla.sel{background:#ffe23c;border-color:#fff;box-shadow:0 0 10px #ffe23c}
    .arc-radar.ok .arc-casilla.sel{background:#46ff82;box-shadow:0 0 12px #46ff82}
  `;
  ui.body.appendChild(style);

  const radar = document.createElement('div');
  radar.className = 'arc-radar';
  ui.body.appendChild(radar);

  let elegida = null;
  let resuelto = false;

  function pintar() {
    radar.className = 'arc-radar' + (resuelto ? ' ok' : '');
    radar.innerHTML = '<div></div>' + COLUMNAS.map(c => '<div class="arc-eje">' + c + '</div>').join('');
    for (let f = 1; f <= FILAS; f++) {
      const e = document.createElement('div');
      e.className = 'arc-eje';
      e.textContent = String(f);
      radar.appendChild(e);
      COLUMNAS.forEach(c => {
        const b = document.createElement('button');
        b.type = 'button';
        b.className = 'arc-casilla' + (elegida && elegida.c === c && elegida.f === f ? ' sel' : '');
        b.dataset.c = c;
        b.dataset.f = String(f);
        b.setAttribute('aria-label', 'Casilla ' + c + f);
        b.addEventListener('click', () => { if (!resuelto) { elegida = { c, f }; ui.say(''); pintar(); } });
        radar.appendChild(b);
      });
    }
  }

  ui.button('Escanear', 'primary', () => {
    if (resuelto) return;
    if (!elegida) { ui.say('Elegid primero una casilla.', 'bad'); return; }
    if (elegida.c === SOLUCION.c && elegida.f === SOLUCION.f) {
      resuelto = true;
      pintar();
      ui.say('¡Eco dorado! El cofre del radar se abre y la pared del fondo se desliza: aparece la sala de la marquesina. Coged la carta 28.', 'ok');
    } else {
      ui.say('Ahí no hay nada: solo una señal falsa o la oscuridad. Juntad las cuatro piezas del radar y buscad el cofre dorado; mirad la letra de su columna y el número de su fila.', 'bad');
    }
  });

  pintar();
  return { close: ui.close };
}
