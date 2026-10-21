// Carta 69 — El programa del rover: escribir un programa con avanzar, girar y «repetir» que lleve al rover de la salida a la bandera dentro del límite
// de bloques. El terreno, en la carta 70; los comandos y el límite, en la 71. La app muestra la rejilla sin muros y el programa se ejecuta de verdad:
// si el rover choca, se queda donde chocó. Vale cualquier programa correcto (instancias_marte.py, PROGRAMA).
import { openGame } from './ui.js';
import { estilo, rejilla } from './cupula.js';

const D = /*DATOS*/{"n": 7, "muros": [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [2, 6], [3, 0], [3, 1], [3, 2], [3, 3], [3, 6], [4, 0], [4, 1], [4, 2], [4, 3], [4, 5], [4, 6], [5, 0], [5, 1], [5, 2], [5, 5], [5, 6], [6, 0], [6, 1], [6, 2], [6, 4], [6, 5], [6, 6]], "inicio": [0, 6], "mira": 1, "meta": [6, 3], "limite": 7, "solucion": [["r", 3, [["a"], ["i"], ["a"], ["d"], ["a"]]]], "camino": [[0, 6], [1, 6], [1, 5], [2, 5], [3, 5], [3, 4], [4, 4], [5, 4], [5, 3], [6, 3]]}/*FIN*/;
const DIR = [[0, -1], [1, 0], [0, 1], [-1, 0]];
const FLECHA = ['▲', '▶', '▼', '◀'];

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 69 — El programa del rover', instr: 'Armad el programa con los botones y pulsad «Ejecutar». El rover sale de abajo a la izquierda. El terreno, en la carta 70; los comandos y el límite de bloques, en la 71.', ...opts });
  estilo('mr-pro', `.pro-rej .mr-cel{background:#e8d8c8;cursor:default}.pro-rej .mr-cel.rastro{background:#c8e0e8}.pro-rej .mr-cel.rover{background:#28a0b8;color:#fff;font-size:1rem}.pro-prog{margin:8px auto;max-width:330px;background:#2a1c18;border-radius:8px;padding:6px 10px;color:#ffe6d6;font:600 .8rem/1.5 monospace;min-height:56px;white-space:pre}.pro-bot{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin:6px 0}.pro-bot button{padding:7px 11px;border-radius:9px;border:2px solid #ff8a50;background:#4a2a1c;color:#ffe6d6;font:700 .8rem system-ui;cursor:pointer}.pro-bot select{padding:7px;border-radius:9px;border:2px solid #ff8a50;background:#4a2a1c;color:#ffe6d6;font:700 .8rem system-ui}`);
  const muros = new Set(D.muros.map(([x, y]) => x + ',' + y));
  const prog = [];
  let abierto = null, resuelto = false;
  const rej = rejilla(D.n, () => {});
  rej.el.classList.add('pro-rej');
  const caja = document.createElement('div'); caja.className = 'pro-prog'; caja.setAttribute('aria-live', 'polite');
  const bot = document.createElement('div'); bot.className = 'pro-bot';
  ui.body.append(rej.el, caja, bot);
  const bloques = lista => lista.reduce((s, b) => s + 1 + (b[0] === 'r' ? bloques(b[2]) : 0), 0);
  const texto = (lista, sang) => lista.map(b => {
    const pad = '  '.repeat(sang);
    if (b[0] === 'a') return pad + 'avanzar';
    if (b[0] === 'i') return pad + 'girar izquierda';
    if (b[0] === 'd') return pad + 'girar derecha';
    return pad + 'repetir ' + b[1] + ' veces:\n' + texto(b[2], sang + 1);
  }).join('\n');
  function pintar(rastro, rover, dir) {
    for (let y = 0; y < D.n; y++) for (let x = 0; x < D.n; x++) {
      const c = rej.celda(x, y), k = x + ',' + y;
      c.disabled = true;
      c.className = 'mr-cel' + (rover && rover[0] === x && rover[1] === y ? ' rover' : rastro && rastro.has(k) ? ' rastro' : '');
      c.textContent = rover && rover[0] === x && rover[1] === y ? FLECHA[dir] : '';
    }
    caja.textContent = prog.length ? texto(prog, 0) : '(programa vacío)';
    caja.dataset.bloques = bloques(prog) + '/' + D.limite;
    rej.el.dataset.rover = rover ? rover.join(',') : '';
  }
  function anadir(b) {
    if (resuelto) return;
    if (bloques(prog) + 1 + (b[0] === 'r' ? 0 : 0) > D.limite) { ui.say('Ya no caben más bloques: el límite es ' + D.limite + ' (carta 71).', 'bad'); return; }
    (abierto ? abierto[2] : prog).push(b);
    if (b[0] === 'r') abierto = b;
    ui.say(''); pintar(null, D.inicio, D.mira);
  }
  [['a', 'Avanzar'], ['i', '↰ Izquierda'], ['d', '↱ Derecha']].forEach(([c, t]) => {
    const b = document.createElement('button'); b.type = 'button'; b.dataset.c = c; b.textContent = t; b.addEventListener('click', () => anadir([c])); bot.appendChild(b);
  });
  const veces = document.createElement('select'); veces.setAttribute('aria-label', 'Veces que se repite');
  for (let k = 2; k <= 6; k++) { const o = document.createElement('option'); o.value = String(k); o.textContent = '×' + k; veces.appendChild(o); }
  const rep = document.createElement('button'); rep.type = 'button'; rep.dataset.c = 'r'; rep.textContent = 'Repetir…';
  rep.addEventListener('click', () => { if (abierto) { ui.say('Ya hay una repetición abierta: cerradla antes (botón «Cerrar repetición»).', 'bad'); return; } anadir(['r', Number(veces.value), []]); });
  const cerr = document.createElement('button'); cerr.type = 'button'; cerr.dataset.c = 'x'; cerr.textContent = 'Cerrar repetición';
  cerr.addEventListener('click', () => { abierto = null; pintar(null, D.inicio, D.mira); });
  bot.append(veces, rep, cerr);
  ui.button('Borrar el último', 'ghost', () => {
    if (resuelto) return;
    if (abierto) { if (abierto[2].length) abierto[2].pop(); else { prog.pop(); abierto = null; } }
    else prog.pop();
    ui.say(''); pintar(null, D.inicio, D.mira);
  });
  ui.button('Vaciar', 'ghost', () => { if (!resuelto) { prog.length = 0; abierto = null; ui.say(''); pintar(null, D.inicio, D.mira); } });
  ui.button('Ejecutar', 'primary', () => {
    if (resuelto) return;
    abierto = null;
    let x = D.inicio[0], y = D.inicio[1], d = D.mira, pasos = 0, choque = false;
    const rastro = new Set([x + ',' + y]);
    const ejecuta = lista => {
      for (const b of lista) {
        if (++pasos > 400 || choque) return;
        if (b[0] === 'a') {
          const nx = x + DIR[d][0], ny = y + DIR[d][1];
          if (nx < 0 || ny < 0 || nx >= D.n || ny >= D.n || muros.has(nx + ',' + ny)) { choque = true; return; }
          x = nx; y = ny; rastro.add(x + ',' + y);
        } else if (b[0] === 'i') d = (d + 3) % 4;
        else if (b[0] === 'd') d = (d + 1) % 4;
        else for (let k = 0; k < b[1] && !choque; k++) ejecuta(b[2]);
      }
    };
    ejecuta(prog);
    pintar(rastro, [x, y], d);
    if (choque) { ui.say('¡Crac! El rover ha chocado contra una roca o contra el borde y se ha quedado parado. Mirad el terreno (carta 70).', 'bad'); return; }
    if (x === D.meta[0] && y === D.meta[1]) {
      resuelto = true;
      ui.say('El rover llega a la bandera siguiendo vuestro programa. Se abre el archivo de la colonia. Coged la carta 80.', 'ok');
    } else ui.say('El rover acaba el programa sin llegar a la bandera: se queda en la casilla ' + 'ABCDEFG'[x] + (y + 1) + '. Revisad el programa.', 'bad');
  });
  pintar(null, D.inicio, D.mira);
  return { close: ui.close };
}
