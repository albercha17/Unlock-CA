// Carta 85 — El punto de la niebla: cinco rumbos de rosa de los vientos con las distancias, en casillas, que dejaron otros cinco puzles (carta 86); la carta de la
// isla, con una casilla de salida, está en la carta 87. Hay que marcar la casilla donde acaba el viaje (instancias_piratas.py, ISLA).
import { openGame } from './ui.js';
import { estilo } from './comun.js';

const D = /*DATOS*/{"n": 10, "inicio": [1, 7], "final": [5, 4]}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 85 — El punto de la niebla', instr: 'Tocad la casilla donde echáis el ancla, en el punto de la niebla, al terminar los cinco rumbos. Los rumbos están en la carta 86 y la carta de la isla, con la salida, en la 87. Las distancias, en casillas, las dejaron la bitácora, las estrellas, el cañón, la balanza y la gruta.', ...opts });
  estilo('pi-isl', '.isl-g{display:grid;gap:2px;width:min(88vw,330px);margin:8px auto;padding:4px;border-radius:8px;background:#0c3440;border:3px solid #e8b84a}.isl-g button{aspect-ratio:1;min-height:20px;border:0;border-radius:3px;background:linear-gradient(160deg,#3a8aa0,#22647a);padding:0;cursor:pointer;color:#fff;font:700 .6rem system-ui,sans-serif}.isl-g button.sel{background:#e8b84a;color:#10242c}.isl-g button.salida{box-shadow:inset 0 0 0 2px #fff}');
  let sel = null, resuelto = false;
  const g = document.createElement('div');
  g.className = 'isl-g';
  g.style.gridTemplateColumns = 'repeat(' + D.n + ',1fr)';
  const bs = [];
  for (let y = 0; y < D.n; y++) for (let x = 0; x < D.n; x++) {
    const b = document.createElement('button');
    b.type = 'button';
    b.dataset.x = String(x + 1);
    b.dataset.y = String(y + 1);
    b.textContent = (x + 1) + ',' + (y + 1);
    b.setAttribute('aria-label', 'Casilla columna ' + (x + 1) + ', fila ' + (y + 1));
    if (x === D.inicio[0] && y === D.inicio[1]) b.classList.add('salida');
    b.addEventListener('click', () => { if (resuelto) return; sel = [x, y]; ui.say(''); pintar(); });
    g.appendChild(b);
    bs.push(b);
  }
  ui.body.appendChild(g);
  function pintar() { bs.forEach((b, i) => b.classList.toggle('sel', !!sel && i === sel[1] * D.n + sel[0])); }
  ui.button('Echar el ancla', 'primary', () => {
    if (resuelto) return;
    if (!sel) { ui.say('Elegid primero una casilla.', 'bad'); return; }
    if (sel[0] !== D.final[0] || sel[1] !== D.final[1]) { ui.say('El ancla no muerde el fondo: en esa casilla no hay nada de lo que buscáis. Repasad los cinco rumbos desde la salida.', 'bad'); return; }
    resuelto = true;
    ui.say('La niebla se espesa a vuestro alrededor y el anillo del Cronoportal empieza a brillar: este es el punto. La capitana Bruma levanta su sombrero. Coged la carta 99.', 'ok');
  });
  pintar();
  return { close: ui.close };
}
