// Carta 72 — Tapiz del sigilo (nonograma 6x6 que dibuja una llama de dragón). Los números de las filas están en la pantalla y los de las
// columnas en las notas de las tejedoras (carta 76). Solución única comprobada por herramientas/instancias_trono.py.
import { openGame } from './ui.js';
import { guardarPalabra, estilo, conImagen, texturaSi } from './comun.js';

const F = 6, C = 6;
const FILAS = [[2], [4], [6], [2, 2], [4], [2]];
const COLUMNAS = [[2], [4], [3, 2], [3, 2], [4], [2]];
const LETRAS = 'ABCDEF';
const PALABRA = 'EL';

function tramos(linea) {
  const t = [];
  let n = 0;
  linea.forEach(v => { if (v) n++; else if (n) { t.push(n); n = 0; } });
  if (n) t.push(n);
  return t;
}
const igual = (a, b) => a.length === b.length && a.every((x, i) => x === b[i]);

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 72 — Tapiz del sigilo',
    instr: 'Pintad las casillas del tapiz para que aparezca el sigilo. Cada número dice cuántas casillas seguidas van pintadas en esa fila o columna; entre bloques hay al menos una vacía. Tocad una casilla para pintarla, otra vez para marcar una cruz y otra para vaciarla.',
    ...opts
  });
  texturaSi(ui, 'pergamino.jpg', { opacidad: 0.25, mezcla: 'screen' });

  estilo(ui.body, `
    .tap-malla{display:grid;grid-template-columns:auto repeat(${C},1fr);gap:3px;max-width:340px;margin:0 auto 6px;padding:8px;border-radius:8px;border:3px solid #5b4426;background:linear-gradient(#2a2014,#1a130b)}
    .tap-col{display:flex;flex-direction:column;justify-content:flex-end;align-items:center;font:700 .8rem Georgia,serif;color:#ffd9a0;line-height:1.15;padding-bottom:2px;min-height:34px}
    .tap-col.oculta{color:#8aa0b2;font-style:italic}
    .tap-fila{display:flex;justify-content:flex-end;align-items:center;gap:5px;font:700 .85rem Georgia,serif;color:#ffd9a0;padding-right:5px}
    .tap-cel{aspect-ratio:1;border-radius:4px;border:1px solid rgba(255,217,160,.25);background:rgba(10,8,5,.6);padding:0;cursor:pointer;touch-action:manipulation;color:#8aa0b2;font:700 1rem Georgia,serif;min-height:34px}
    .tap-cel[data-v="1"]{background:linear-gradient(135deg,#e2552b,#a3220e);border-color:#ffb27a;box-shadow:inset 0 0 6px rgba(255,220,160,.5)}
    .tap-cel[data-v="1"].dorado{background:linear-gradient(135deg,#f0c15a,#b0781c)}
    .tap-cel.img[data-v="1"]{background-image:var(--img);background-size:cover}
    .tap-nota{font-size:.78rem;color:#a9bccb}
  `);

  const malla = document.createElement('div');
  malla.className = 'tap-malla';
  const nota = document.createElement('div');
  nota.className = 'tap-nota';
  nota.textContent = 'Las columnas muestran «?»: sus números están en las notas de las tejedoras (carta 76).';
  ui.body.append(malla, nota);

  const estado = Array(F * C).fill(0); // 0 vacía, 1 pintada, 2 cruz
  let resuelto = false;
  const celdas = [];

  malla.appendChild(document.createElement('div'));
  for (let c = 0; c < C; c++) {
    const d = document.createElement('div');
    d.className = 'tap-col oculta';
    d.innerHTML = '<span>?</span>';
    d.setAttribute('aria-label', 'Columna ' + LETRAS[c] + ': números en la carta 76');
    malla.appendChild(d);
  }
  for (let r = 0; r < F; r++) {
    const p = document.createElement('div');
    p.className = 'tap-fila';
    p.innerHTML = FILAS[r].map(n => '<span>' + n + '</span>').join('');
    p.setAttribute('aria-label', 'Fila ' + (r + 1) + ': ' + FILAS[r].join(' y '));
    malla.appendChild(p);
    for (let c = 0; c < C; c++) {
      const i = r * C + c;
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'tap-cel' + ((r + c) % 2 ? ' dorado' : '');
      b.dataset.i = String(i);
      b.setAttribute('aria-label', 'Casilla ' + LETRAS[c] + (r + 1));
      b.addEventListener('click', () => {
        if (resuelto) return;
        estado[i] = (estado[i] + 1) % 3;
        ui.say('');
        pintar();
        if (filasOk() && columnasOk()) terminar();
      });
      celdas.push(b);
      malla.appendChild(b);
      conImagen(b, 'tapiz/hilo.jpg');
    }
  }

  function filasOk() {
    for (let r = 0; r < F; r++) if (!igual(tramos(estado.slice(r * C, r * C + C).map(v => (v === 1 ? 1 : 0))), FILAS[r])) return false;
    return true;
  }
  function columnasOk() {
    for (let c = 0; c < C; c++) {
      const col = [];
      for (let r = 0; r < F; r++) col.push(estado[r * C + c] === 1 ? 1 : 0);
      if (!igual(tramos(col), COLUMNAS[c])) return false;
    }
    return true;
  }

  function pintar() {
    celdas.forEach((b, i) => {
      b.dataset.v = String(estado[i]);
      b.textContent = estado[i] === 2 ? '×' : '';
    });
  }
  function terminar() {
    if (resuelto) return;
    resuelto = true;
    guardarPalabra('72', PALABRA);
    ui.say('¡El sigilo brilla: una llama de dragón! El dragón se apacigua y se acomoda en su sueño. Palabra de la profecía: «' + PALABRA + '». Anotadla. Coged la carta 82.', 'ok');
  }

  ui.button('Vaciar', 'ghost', () => { if (!resuelto) { estado.fill(0); ui.say(''); pintar(); } });
  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    if (!estado.some(v => v === 1)) { ui.say('Todavía no habéis pintado ninguna casilla.', 'bad'); return; }
    const fo = filasOk(), co = columnasOk();
    if (fo && co) terminar();
    else if (!fo) ui.say('Alguna fila no coincide con sus números: contad los bloques de casillas seguidas.', 'bad');
    else ui.say('Las filas cuadran, pero alguna columna no coincide con las notas de las tejedoras (carta 76).', 'bad');
  });

  pintar();
  return { close: ui.close };
}
