// Carta 46 — La bodega: empujar tres barriles de pólvora hasta las X del plano de estiba (carta 40), que en la app no se ven.
// Instancia de herramientas/instancias_piratas.py (BFS: 30 movimientos y 13 empujes como mínimo). Las X se pueden marcar con tiza.
import { openGame } from './ui.js';

const ANCHO = 7;
const ALTO = 6;
const MUROS = [[0, 5], [1, 4], [2, 5], [3, 4], [4, 5]];
const CAJAS = [[1, 3], [2, 2], [3, 2]];
const METAS = [[0, 0], [1, 0], [4, 1]];
const JUGADOR = [5, 3];
const DIRS = { arriba: [0, -1], abajo: [0, 1], izquierda: [-1, 0], derecha: [1, 0] };
const k = (x, y) => x + ',' + y;

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 46 — La bodega',
    instr: 'Mueve al marinero con las flechas y empuja los barriles (no se puede tirar de ellos) hasta las X del plano de estiba. Toca una casilla para marcarla con tiza. Proa arriba.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .pir-proa{text-align:center;font:700 .8rem system-ui,sans-serif;letter-spacing:.2em;color:#e8b84a;margin:0}
    .pir-bodega{display:grid;grid-template-columns:repeat(${ANCHO},1fr);gap:3px;width:min(86vw,320px);margin:4px auto 8px;padding:6px;border-radius:8px;background:#3a2412;border:3px solid #6a4422}
    .pir-celda{position:relative;aspect-ratio:1;border:0;border-radius:4px;padding:0;background:repeating-linear-gradient(90deg,#b07a46 0 9px,#a46e3c 9px 10px);cursor:pointer}
    .pir-celda.muro{background:#4a2c14 linear-gradient(45deg,transparent 46%,#7a4e28 47% 53%,transparent 54%);cursor:default}
    .pir-celda.tiza::before{content:'';position:absolute;inset:18%;background:linear-gradient(45deg,transparent 42%,rgba(250,250,240,.85) 43% 57%,transparent 58%),linear-gradient(-45deg,transparent 42%,rgba(250,250,240,.85) 43% 57%,transparent 58%)}
    .pir-celda.barril::after{content:'';position:absolute;inset:6%;background:url('./img/ui/barril.png') center / contain no-repeat}
    .pir-celda.marinero::after{content:'';position:absolute;inset:20%;border-radius:50%;background:radial-gradient(circle at 40% 35%,#fff4c0,#e8b84a 45%,#8a5a14);box-shadow:0 0 12px rgba(255,220,120,.9)}
    .pir-bodega.ok{border-color:#7be495;box-shadow:0 0 24px rgba(123,228,149,.6)}
    .pir-mando{display:grid;grid-template-columns:repeat(3,56px);grid-template-rows:repeat(2,50px);gap:6px;justify-content:center;margin:0 auto 8px}
    .pir-mando button{border-radius:10px;border:2px solid #e8b84a;background:#173a46;color:#f6e7b8;font-size:1.3rem;cursor:pointer}
    .pir-mando [data-d=arriba]{grid-column:2;grid-row:1}.pir-mando [data-d=izquierda]{grid-column:1;grid-row:2}
    .pir-mando [data-d=abajo]{grid-column:2;grid-row:2}.pir-mando [data-d=derecha]{grid-column:3;grid-row:2}
  `;
  ui.body.appendChild(style);

  const proa = document.createElement('p');
  proa.className = 'pir-proa';
  proa.textContent = 'PROA';
  const rejilla = document.createElement('div');
  rejilla.className = 'pir-bodega';
  const popa = document.createElement('p');
  popa.className = 'pir-proa';
  popa.textContent = 'POPA';
  const mando = document.createElement('div');
  mando.className = 'pir-mando';
  ui.body.appendChild(proa);
  ui.body.appendChild(rejilla);
  ui.body.appendChild(popa);
  ui.body.appendChild(mando);

  const muros = new Set(MUROS.map(c => k(...c)));
  const metas = new Set(METAS.map(c => k(...c)));
  const tiza = new Set();
  let cajas, jug, historia, resuelto = false;

  function reiniciar() {
    cajas = new Set(CAJAS.map(c => k(...c)));
    jug = JUGADOR.slice();
    historia = [];
  }

  function pintar() {
    rejilla.className = 'pir-bodega' + (resuelto ? ' ok' : '');
    rejilla.innerHTML = '';
    for (let y = 0; y < ALTO; y++) {
      for (let x = 0; x < ANCHO; x++) {
        const b = document.createElement('button');
        b.type = 'button';
        b.dataset.x = String(x);
        b.dataset.y = String(y);
        const id = k(x, y);
        b.className = 'pir-celda' + (muros.has(id) ? ' muro' : '') + (tiza.has(id) ? ' tiza' : '') + (cajas.has(id) ? ' barril' : '') + (jug[0] === x && jug[1] === y ? ' marinero' : '');
        b.setAttribute('aria-label', 'Casilla ' + (x + 1) + ', ' + (y + 1) + (muros.has(id) ? ': cuaderna' : cajas.has(id) ? ': barril' : '') + (tiza.has(id) ? ', marcada con tiza' : ''));
        if (!muros.has(id)) b.addEventListener('click', () => { if (resuelto) return; tiza.has(id) ? tiza.delete(id) : tiza.add(id); pintar(); });
        rejilla.appendChild(b);
      }
    }
  }

  const libre = (x, y) => x >= 0 && y >= 0 && x < ANCHO && y < ALTO && !muros.has(k(x, y));

  function mover(dir) {
    if (resuelto) return;
    const [dx, dy] = DIRS[dir];
    const nx = jug[0] + dx, ny = jug[1] + dy;
    if (!libre(nx, ny)) { ui.say('Ahí hay una cuaderna: no se puede pasar.', 'bad'); return; }
    const id = k(nx, ny);
    if (cajas.has(id)) {
      const bx = nx + dx, by = ny + dy;
      if (!libre(bx, by) || cajas.has(k(bx, by))) { ui.say('El barril no se mueve: detrás hay una cuaderna u otro barril.', 'bad'); return; }
      historia.push({ jug: jug.slice(), cajas: new Set(cajas) });
      cajas.delete(id);
      cajas.add(k(bx, by));
    } else {
      historia.push({ jug: jug.slice(), cajas: new Set(cajas) });
    }
    jug = [nx, ny];
    ui.say('');
    if ([...cajas].every(c => metas.has(c))) {
      resuelto = true;
      pintar();
      ui.say('¡Los tres barriles están en su sitio, bien lejos de la cocina! El contramaestre los ata con fuerza y suspira de alivio. Coged la carta 44.', 'ok');
      return;
    }
    pintar();
  }

  Object.keys(DIRS).forEach(d => {
    const b = document.createElement('button');
    b.type = 'button';
    b.dataset.d = d;
    b.textContent = { arriba: '▲', abajo: '▼', izquierda: '◀', derecha: '▶' }[d];
    b.setAttribute('aria-label', 'Mover hacia ' + d);
    b.addEventListener('click', () => mover(d));
    mando.appendChild(b);
  });
  const teclas = e => {
    const d = { ArrowUp: 'arriba', ArrowDown: 'abajo', ArrowLeft: 'izquierda', ArrowRight: 'derecha' }[e.key];
    if (d) { e.preventDefault(); mover(d); }
  };
  document.addEventListener('keydown', teclas);
  ui.onClose(() => document.removeEventListener('keydown', teclas));

  ui.button('Deshacer', '', () => {
    if (resuelto || !historia.length) return;
    const h = historia.pop();
    jug = h.jug;
    cajas = h.cajas;
    ui.say('');
    pintar();
  });
  ui.button('Empezar de nuevo', '', () => { if (!resuelto) { reiniciar(); ui.say('Los barriles vuelven a donde estaban.'); pintar(); } });

  reiniciar();
  pintar();
  return { close: ui.close };
}
