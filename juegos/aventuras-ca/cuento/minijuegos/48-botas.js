// Carta 48 — Las botas de siete leguas: llegar a la casa del leñador saltando, por turnos, dos y tres casillas en línea recta (acertijo de
// la carta 53). El mapa, con los árboles y el agua, solo está en las cartas 42 y 49: en la app el bosque está a oscuras.
// Instancia de herramientas/instancias_cuento.py (BOTAS, comprobada por BFS).
import { openGame } from './ui.js';
import { estilo } from './libro.js';

const B = /*DATOS*/{"n": 7, "saltos": [2, 3], "obstaculos": [[0, 0], [0, 1], [0, 2], [0, 4], [1, 0], [2, 1], [3, 0], [3, 3], [3, 5], [4, 0], [4, 1], [4, 4], [5, 5], [6, 4]], "inicio": [0, 6], "fin": [6, 0], "solucion": ["derecha", "derecha", "arriba", "arriba", "izquierda", "derecha", "abajo", "arriba"]}/*FIN*/;
const DIR = { arriba: [0, -1], abajo: [0, 1], izquierda: [-1, 0], derecha: [1, 0] };

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 48 — Las botas de siete leguas', instr: 'El bosque está a oscuras: solo veis dónde estáis y la casa del leñador. Elegid la dirección de cada salto. Si caéis en un árbol o en el agua, volvéis al principio.', ...opts });
  estilo('cu-botas', `
    .bot-bosque{display:grid;gap:3px;width:min(80vw,300px);margin:6px auto;padding:6px;border-radius:10px;background:#1c2a1c}
    .bot-cel{aspect-ratio:1;border-radius:4px;background:#2a3a2a}
    .bot-cel.yo{background:radial-gradient(circle,#ffe08a,#c89a30 70%)}
    .bot-cel.fin{background:radial-gradient(circle,#f0d0f0,#9a6ab0 70%)}
    .bot-cel.pisada{background:#3e5a3e}
    .bot-dirs{display:grid;grid-template-columns:repeat(3,56px);grid-template-rows:repeat(2,46px);gap:6px;justify-content:center;margin:8px auto}
    .bot-dirs button{border-radius:10px;border:2px solid #ffe08a;background:#5a3aa8;color:#fff7d6;font:800 1.2rem system-ui;cursor:pointer}
    .bot-dirs [data-d=arriba]{grid-column:2;grid-row:1}.bot-dirs [data-d=izquierda]{grid-column:1;grid-row:2}
    .bot-dirs [data-d=abajo]{grid-column:2;grid-row:2}.bot-dirs [data-d=derecha]{grid-column:3;grid-row:2}
    .bot-pie{text-align:center;color:#fff7d6;font:700 .85rem system-ui;margin:0}`);
  const bosque = document.createElement('div'); bosque.className = 'bot-bosque';
  bosque.style.gridTemplateColumns = 'repeat(' + B.n + ',1fr)';
  const pie = document.createElement('p'); pie.className = 'bot-pie';
  const dirs = document.createElement('div'); dirs.className = 'bot-dirs';
  ui.body.append(bosque, pie, dirs);
  const obst = new Set(B.obstaculos.map(([x, y]) => x + ',' + y));
  let pos, turno, pisadas, resuelto = false;
  const reiniciar = () => { pos = B.inicio.slice(); turno = 0; pisadas = new Set([pos.join(',')]); };
  function pintar() {
    bosque.innerHTML = '';
    for (let y = 0; y < B.n; y++) for (let x = 0; x < B.n; x++) {
      const c = document.createElement('div'); const k = x + ',' + y;
      c.className = 'bot-cel' + (k === pos.join(',') ? ' yo' : k === B.fin.join(',') ? ' fin' : pisadas.has(k) ? ' pisada' : '');
      bosque.appendChild(c);
    }
    bosque.dataset.pos = pos.join(',');
    pie.textContent = pos.join(',') === B.inicio.join(',') ? 'Estáis en el borde del bosque.' : '';
  }
  Object.keys(DIR).forEach(d => {
    const b = document.createElement('button'); b.type = 'button'; b.dataset.d = d; b.textContent = { arriba: '▲', abajo: '▼', izquierda: '◀', derecha: '▶' }[d];
    b.setAttribute('aria-label', 'Saltar hacia ' + d);
    b.addEventListener('click', () => {
      if (resuelto) return;
      const s = B.saltos[turno], nx = pos[0] + DIR[d][0] * s, ny = pos[1] + DIR[d][1] * s;
      if (nx < 0 || ny < 0 || nx >= B.n || ny >= B.n) { ui.say('Ese salto os saca del bosque. Probad otra dirección.', 'bad'); return; }
      if (obst.has(nx + ',' + ny)) { ui.say('¡Plaf! Habéis caído contra un árbol o en el agua. Volvéis a empezar. Mirad bien el mapa (cartas 42 y 49).', 'bad'); reiniciar(); pintar(); return; }
      pos = [nx, ny]; turno = 1 - turno; pisadas.add(pos.join(',')); ui.say('');
      if (nx === B.fin[0] && ny === B.fin[1]) { resuelto = true; pintar(); ui.say('¡Último salto y aterrizáis delante de la casa del leñador, que os abre la puerta. Coged la carta 36.', 'ok'); return; }
      pintar();
    });
    dirs.appendChild(b);
  });
  ui.button('Volver al principio', '', () => { if (!resuelto) { reiniciar(); ui.say(''); pintar(); } });
  reiniciar();
  pintar();
  return { close: ui.close };
}
