// Carta 48 — El patio de ajedrez (recorrido del caballo): pisar con saltos de caballo todas las casillas libres, una sola vez cada una, empezando en la
// casilla marcada. Las casillas tachadas, solo en el patio (cartas 42 y 49, dos mitades); el acertijo, en la 53. Vale cualquier recorrido correcto
// (instancias_florencia.py, CABALLO). Letra de la clave: E.
import { openGame } from './ui.js';
import { estilo, rejilla } from './taller.js';

const D = /*DATOS*/{"n": 6, "huecos": [[1, 5], [2, 0], [2, 3], [3, 4], [4, 5]], "inicio": [0, 0], "letra": "E"}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 48 — El patio de ajedrez', instr: 'Tocad las casillas en el orden de los saltos del caballo, empezando por donde está. Pasad por todas las libres, una sola vez. Qué casillas están tachadas, en las cartas 42, 49 y 53.', ...opts });
  estilo('fl-cab', `.cab .fl-cel{background:#e8d3a8;font:800 1rem system-ui}.cab .fl-cel.ruta{background:#c98a52;color:#fff}`);
  const ruta = [];
  let resuelto = false;
  const r = rejilla(D.n, (x, y, b) => {
    if (resuelto) return;
    const k = ruta.findIndex(p => p[0] === x && p[1] === y);
    if (k >= 0) { if (k === ruta.length - 1) { ruta.pop(); pintar(); ui.say(''); } return; }
    ruta.push([x, y]); ui.say(''); pintar();
  }, true);
  r.el.classList.add('cab');
  function pintar() {
    for (let y = 0; y < D.n; y++) for (let x = 0; x < D.n; x++) { const c = r.celda(x, y); c.classList.remove('ruta'); c.textContent = ''; }
    ruta.forEach(([x, y], i) => { const c = r.celda(x, y); c.classList.add('ruta'); c.textContent = String(i + 1); });
    r.el.dataset.ruta = ruta.map(p => p.join(',')).join(';');
  }
  ui.body.appendChild(r.el);
  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    const huecos = new Set(D.huecos.map(([x, y]) => x + ',' + y));
    const libres = D.n * D.n - huecos.size;
    if (!ruta.length) { ui.say('Todavía no habéis marcado ningún salto.', 'bad'); return; }
    if (ruta[0][0] !== D.inicio[0] || ruta[0][1] !== D.inicio[1]) { ui.say('El caballo empieza en la casilla marcada del patio (cartas 42 y 49).', 'bad'); return; }
    for (let i = 0; i < ruta.length; i++) {
      if (huecos.has(ruta[i].join(','))) { ui.say('El salto ' + (i + 1) + ' cae en una casilla tachada del patio (cartas 42 y 49).', 'bad'); return; }
      if (i) {
        const dx = Math.abs(ruta[i][0] - ruta[i - 1][0]), dy = Math.abs(ruta[i][1] - ruta[i - 1][1]);
        if (!((dx === 1 && dy === 2) || (dx === 2 && dy === 1))) { ui.say('El salto ' + (i + 1) + ' no es de caballo: dos casillas en recto y una de lado (carta 53).', 'bad'); return; }
      }
    }
    if (ruta.length < libres) { ui.say('Faltan casillas libres por pisar: llevan ' + ruta.length + ' y hay ' + libres + '.', 'bad'); return; }
    resuelto = true;
    ui.say('El caballo recorre el patio entero sin repetir casilla y se abre la compuerta del fondo. Letra de la clave: ' + D.letra + '. Coged la carta 36.', 'ok');
  });
  ui.button('Quitar el último', 'ghost', () => { if (!resuelto && ruta.length) { ruta.pop(); ui.say(''); pintar(); } });
  ui.button('Empezar de nuevo', 'ghost', () => { if (!resuelto) { ruta.length = 0; ui.say(''); pintar(); } });
  return { close: ui.close };
}
