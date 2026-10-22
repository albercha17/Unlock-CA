// Carta 72 — El mosaico de la grada: las butacas de la primera fila están pintadas (carta 75) y cada butaca de las filas siguientes se pinta según las dos
// vecinas de la fila de arriba (carta 79; la grada es un anillo). Hay que pintar la fila D.pasos + 1 (instancias_futbol.py, GRADA). Aro de la grada: D.aro.
import { openGame } from './ui.js';
import { estilo } from './comun.js';

const D = /*DATOS*/{"final": [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0], "n": 12, "pasos": 6, "aro": 2}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 72 — El mosaico de la grada', instr: 'Pintad de rojo las butacas de la fila ' + (D.pasos + 1) + '. La primera fila está en la carta 75 y la regla, en la 79.', ...opts });
  estilo('fu-gra', '.gra-f{display:grid;gap:3px;max-width:340px;margin:10px auto}.gra-f button{aspect-ratio:1;min-height:24px;border:2px solid #12310f;border-radius:4px;background:#f4fff0;padding:0;cursor:pointer}.gra-f button.roja{background:#d63a3a}');
  const fila = Array(D.n).fill(0);
  let resuelto = false;
  const cuadro = document.createElement('div');
  cuadro.className = 'gra-f';
  cuadro.style.gridTemplateColumns = 'repeat(' + D.n + ',1fr)';
  const bs = fila.map((_, i) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.dataset.i = String(i);
    b.setAttribute('aria-label', 'Butaca ' + (i + 1));
    b.addEventListener('click', () => { if (resuelto) return; fila[i] ^= 1; ui.say(''); pintar(); });
    cuadro.appendChild(b);
    return b;
  });
  const pie = document.createElement('div');
  pie.className = 'fu-pie';
  pie.textContent = 'Fila ' + (D.pasos + 1);
  ui.body.append(cuadro, pie);
  function pintar() { bs.forEach((b, i) => { b.classList.toggle('roja', fila[i] === 1); b.dataset.v = String(fila[i]); }); }
  ui.button('Comprobar la fila', 'primary', () => {
    if (resuelto) return;
    if (fila.some((v, i) => v !== D.final[i])) { ui.say('La fila no cuadra con la regla: alguna butaca está mal pintada.', 'bad'); return; }
    resuelto = true;
    ui.say('La grada completa el mosaico y los hinchas aplauden. Aro de la grada: ' + D.aro + '. Coged la carta 82.', 'ok');
  });
  ui.button('Vaciar', 'ghost', () => { if (!resuelto) { fila.fill(0); ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
