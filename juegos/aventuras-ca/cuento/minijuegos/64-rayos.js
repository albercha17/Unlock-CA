// Carta 64 — Rayos de luna: colocar EXACTAMENTE tres espejos (/ o \) para que el rayo de luna que entra por la flecha llegue a la flor,
// y que el rayo toque los tres. La flor NO está marcada: la carta 66 dice que está en E5. Muros: A1, E1, D3, B4 y C4.
// Solución única (generadores_puzles.rayos(5, 3, 7)): / en A2, \ en E2 y / en A4. Letra del libro: I.
import { openGame } from './ui.js';
import { guardarLetra, estilo, conImagen, NOMBRES_COLUMNA } from './libro.js';

const LETRA = 'I';
const N = 5;
const PAREDES = new Set([0, 4, 13, 16, 17]);
const FILA = 3;
const FLOR = 24;
const ESPEJOS = 3;

function nombre(i) { return NOMBRES_COLUMNA[i % N] + (Math.floor(i / N) + 1); }

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 64 — Rayos de luna',
    instr: 'El rayo de luna entra por la flecha y avanza recto. Toca una casilla para poner un espejo /, otra vez para \\ y otra vez para quitarlo. Usad exactamente tres espejos, que el rayo toque los tres, y que llegue a la flor (carta 66).',
    ...opts
  });
  estilo('cu-rayos-estilo', `
    .ray-marco{display:grid;grid-template-columns:24px 18px 1fr;grid-template-rows:18px auto;max-width:360px;margin:0 auto 6px;font-size:.75rem;color:#ffe08a}
    .ray-letras{grid-column:3;display:grid;grid-template-columns:repeat(${N},1fr);justify-items:center;align-items:center}
    .ray-nums{grid-column:2;grid-row:2;display:grid;grid-template-rows:repeat(${N},1fr);justify-items:center;align-items:center}
    .ray-tablero{grid-column:3;grid-row:2;position:relative}
    .ray-rej{display:grid;grid-template-columns:repeat(${N},1fr);gap:3px;position:relative}
    .ray-cel{aspect-ratio:1;border-radius:8px;border:1px solid rgba(255,224,138,.3);background:linear-gradient(180deg,#2a1c58,#1a1038);padding:0;position:relative;cursor:pointer;color:#fff;min-width:0}
    .ray-cel.muro{background:repeating-linear-gradient(45deg,#4a4658 0 6px,#34303f 6px 12px);cursor:default}
    .ray-cel svg{position:absolute;inset:0;width:100%;height:100%}
    .ray-cel.flor.on::after{content:"";position:absolute;inset:18%;border-radius:50%;background:radial-gradient(circle,#fff,#bfe0ff 50%,transparent 70%);box-shadow:0 0 22px #bfe0ff}
    .ray-rayo{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
    .ray-rayo polyline{fill:none;stroke:#e8f4ff;stroke-width:.1;stroke-linecap:round;stroke-linejoin:round;filter:drop-shadow(0 0 .12px #9fd0ff)}
    .ray-flecha{position:absolute;left:-22px;width:0;height:0;border-left:14px solid #bfe0ff;border-top:9px solid transparent;border-bottom:9px solid transparent;filter:drop-shadow(0 0 5px #bfe0ff)}
    .ray-cont{display:flex;justify-content:space-between;font-size:.85rem;color:#d8e2ee;margin:6px 4px}
    .ray-img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.5;pointer-events:none;border-radius:8px}
  `);

  const marco = document.createElement('div');
  marco.className = 'ray-marco';
  const letras = document.createElement('div');
  letras.className = 'ray-letras';
  for (let c = 0; c < N; c++) { const s = document.createElement('span'); s.textContent = NOMBRES_COLUMNA[c]; letras.appendChild(s); }
  const nums = document.createElement('div');
  nums.className = 'ray-nums';
  for (let r = 0; r < N; r++) { const s = document.createElement('span'); s.textContent = String(r + 1); nums.appendChild(s); }
  const tablero = document.createElement('div');
  tablero.className = 'ray-tablero';
  const rej = document.createElement('div');
  rej.className = 'ray-rej';
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('class', 'ray-rayo');
  svg.setAttribute('viewBox', '0 0 ' + N + ' ' + N);
  svg.setAttribute('aria-hidden', 'true');
  const flecha = document.createElement('div');
  flecha.className = 'ray-flecha';
  flecha.setAttribute('aria-hidden', 'true');
  flecha.style.top = 'calc(' + (FILA * 100 / N) + '% + ' + (100 / N / 2) + '% - 9px)';
  tablero.append(rej, svg, flecha);
  marco.append(letras, nums, tablero);
  const cont = document.createElement('div');
  cont.className = 'ray-cont';
  cont.innerHTML = '<span>Espejos puestos: <b class="ray-n">0</b> de ' + ESPEJOS + '</span><span class="ray-estado"></span>';
  ui.body.append(marco, cont);
  conImagen(tablero, 'sala-espejos.jpg', { clase: 'ray-img', mezcla: 'screen' });

  let esp = {};
  let resuelto = false;
  const celdas = [];
  for (let i = 0; i < N * N; i++) {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'ray-cel' + (PAREDES.has(i) ? ' muro' : '') + (i === FLOR ? ' flor' : '');
    b.dataset.i = String(i);
    b.setAttribute('aria-label', (PAREDES.has(i) ? 'Muro ' : 'Casilla ') + nombre(i));
    if (!PAREDES.has(i)) b.addEventListener('click', () => ciclo(i));
    celdas.push(b);
    rej.appendChild(b);
  }

  function ciclo(i) {
    if (resuelto) return;
    const m = esp[i];
    if (!m) {
      if (Object.keys(esp).length >= ESPEJOS) { ui.say('Ya habéis puesto los tres espejos. Quitad alguno antes de poner otro.', 'bad'); return; }
      esp[i] = '/';
    } else if (m === '/') esp[i] = '\\';
    else delete esp[i];
    ui.say('');
    pintar();
  }

  function trazar() {
    let x = 0, y = FILA, dx = 1, dy = 0;
    const pts = [[-0.5, y + 0.5]];
    const tocados = new Set();
    let llega = false;
    for (let k = 0; k < 4 * N * N; k++) {
      if (x < 0 || x >= N || y < 0 || y >= N) { pts.push([x + 0.5 - dx * 0.5, y + 0.5 - dy * 0.5]); break; }
      const c = y * N + x;
      if (PAREDES.has(c)) { pts.push([x + 0.5 - dx * 0.5, y + 0.5 - dy * 0.5]); break; }
      pts.push([x + 0.5, y + 0.5]);
      if (c === FLOR) { llega = true; break; }
      const m = esp[c];
      if (m) { tocados.add(c); const t = m === '/' ? [-dy, -dx] : [dy, dx]; dx = t[0]; dy = t[1]; }
      x += dx; y += dy;
    }
    return { pts, llega, tocados };
  }

  function pintar() {
    celdas.forEach((b, i) => {
      const viejo = b.querySelector('svg');
      if (viejo) viejo.remove();
      if (esp[i]) {
        const s = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        s.setAttribute('viewBox', '0 0 10 10');
        const l = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        const a = esp[i] === '/' ? [2, 8, 8, 2] : [2, 2, 8, 8];
        l.setAttribute('x1', a[0]); l.setAttribute('y1', a[1]); l.setAttribute('x2', a[2]); l.setAttribute('y2', a[3]);
        l.setAttribute('stroke', '#f2e8ff'); l.setAttribute('stroke-width', '1.6'); l.setAttribute('stroke-linecap', 'round');
        s.appendChild(l);
        b.appendChild(s);
        b.setAttribute('aria-label', 'Espejo ' + (esp[i] === '/' ? 'inclinado a la derecha' : 'inclinado a la izquierda') + ' en ' + nombre(i));
      } else if (!PAREDES.has(i)) {
        b.setAttribute('aria-label', 'Casilla ' + nombre(i));
      }
    });
    const r = trazar();
    svg.innerHTML = '<polyline points="' + r.pts.map((p) => p.join(',')).join(' ') + '"/>';
    celdas[FLOR].classList.toggle('on', r.llega);
    ui.body.querySelector('.ray-n').textContent = String(Object.keys(esp).length);
    return r;
  }

  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    const r = pintar();
    const usados = Object.keys(esp).length;
    if (usados !== ESPEJOS) { ui.say('Hay que usar exactamente ' + ESPEJOS + ' espejos y habéis puesto ' + usados + '.', 'bad'); return; }
    if (!r.llega) { ui.say('El rayo no llega a la flor de luna (casilla E5). Seguid su camino desde la flecha y mirad dónde se pierde.', 'bad'); return; }
    if (r.tocados.size !== ESPEJOS) { ui.say('El rayo llega, pero hay espejos que no toca: los tres deben servir.', 'bad'); return; }
    resuelto = true;
    guardarLetra('64', LETRA);
    ui.say('¡La flor de luna se abre bañada de luz! Coged la carta 78. Letra del libro: ' + LETRA + '.', 'ok');
  });
  ui.button('Quitar todos', 'ghost', () => { if (!resuelto) { esp = {}; ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
