// Carta 69 — Atasco ante la puerta (bloques deslizantes): sacar el ariete por el lado derecho. Los troncos solo se deslizan en horizontal y
// los carros solo en vertical. La nota del maestre (carta 70) dice cuál es el ariete: no se señala en la pantalla.
// Instancia con 10 movimientos mínimos (herramientas/instancias_trono.py).
import { openGame } from './ui.js';
import { guardarPalabra, estilo, conImagen, texturaSi } from './comun.js';

const N = 6;
// fila, columna, largo, horizontal; la primera pieza es el ariete
const PIEZAS = [[2, 0, 2, true], [0, 4, 3, false], [4, 5, 2, false], [4, 3, 2, false], [3, 4, 2, true], [1, 2, 2, false]];
const PALABRA = 'AL';

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 69 — Atasco ante la puerta',
    instr: 'Tocad una pieza para elegirla y moverla con los botones, o arrastradla. Los troncos solo van de lado y los carros solo arriba y abajo. Sacad el ariete por el lado derecho.',
    ...opts
  });
  texturaSi(ui, 'puerta.jpg', { opacidad: 0.3, mezcla: 'screen' });

  estilo(ui.body, `
    .pue-tablero{position:relative;width:min(330px,84vw);aspect-ratio:1;margin:0 auto 6px;background:linear-gradient(#10161d,#070b10);border:3px solid #4a5a68;border-radius:8px;touch-action:none}
    .pue-salida{position:absolute;right:-16px;top:0;bottom:0;width:13px;background:repeating-linear-gradient(0deg,#b7843c 0 8px,#7a5420 8px 12px);border-radius:0 6px 6px 0}
    .pue-pieza{position:absolute;border-radius:7px;border:2px solid rgba(255,255,255,.4);box-shadow:0 3px 8px rgba(0,0,0,.55);cursor:grab;transition:left .12s,top .12s;touch-action:none;display:flex;align-items:center;justify-content:center;color:#f4e6c8;font:700 .8rem Poppins,sans-serif;overflow:hidden}
    .pue-pieza.tronco{background:repeating-linear-gradient(90deg,#7a5230 0 10px,#5e3d22 10px 13px)}
    .pue-pieza.carro{background:linear-gradient(135deg,#4a5a68,#2a3540);border-style:dashed}
    .pue-pieza.carro::before,.pue-pieza.carro::after{content:"";position:absolute;width:30%;height:22%;border-radius:50%;background:#14191f;border:2px solid #8aa0b2}
    .pue-pieza.carro::before{left:8%;bottom:-6%}.pue-pieza.carro::after{right:8%;bottom:-6%}
    .pue-pieza.sel{outline:3px solid #8fc7ee;box-shadow:0 0 14px #8fc7ee}
    .pue-pieza.img{background-image:var(--img);background-size:cover}
    .pue-mando{display:flex;justify-content:center;align-items:center;gap:10px;margin:8px 0 0}
    .pue-mando button{min-width:84px;min-height:48px}
    .pue-info{font-size:.82rem;color:#a9bccb;margin-top:4px;min-height:1.2em}
  `);

  const tablero = document.createElement('div');
  tablero.className = 'pue-tablero';
  const salida = document.createElement('div');
  salida.className = 'pue-salida';
  salida.setAttribute('aria-hidden', 'true');
  tablero.appendChild(salida);
  const mando = document.createElement('div');
  mando.className = 'pue-mando';
  const info = document.createElement('div');
  info.className = 'pue-info';
  ui.body.append(tablero, mando, info);

  let piezas, movs, resuelto, sel = -1;
  const els = [];

  const celda = () => tablero.clientWidth / N;
  function ocupado(excepto) {
    const o = new Set();
    piezas.forEach((k, i) => { if (i !== excepto) for (let j = 0; j < k.largo; j++) o.add((k.hor ? k.r : k.r + j) + ',' + (k.hor ? k.c + j : k.c)); });
    return o;
  }
  function puede(i, nr, nc) {
    const k = piezas[i];
    const o = ocupado(i);
    for (let j = 0; j < k.largo; j++) {
      const y = k.hor ? nr : nr + j, x = k.hor ? nc + j : nc;
      if (y < 0 || x < 0 || y >= N || x >= N || o.has(y + ',' + x)) return false;
    }
    return true;
  }
  function mover(i, paso) {
    const k = piezas[i];
    const nr = k.hor ? k.r : k.r + paso, nc = k.hor ? k.c + paso : k.c;
    if (resuelto || !puede(i, nr, nc)) return false;
    k.r = nr; k.c = nc; movs++;
    pintar();
    if (piezas[0].c + piezas[0].largo === N) {
      resuelto = true;
      guardarPalabra('69', PALABRA);
      ui.say('¡El ariete embiste y la barricada se desmorona! La puerta de bronce queda libre. Palabra de la profecía: «' + PALABRA + '». Anotadla. Coged la carta 80.', 'ok');
    }
    return true;
  }

  const bMenos = document.createElement('button');
  bMenos.type = 'button';
  bMenos.className = 'far-btn ghost pue-menos';
  const bMas = document.createElement('button');
  bMas.type = 'button';
  bMas.className = 'far-btn ghost pue-mas';
  mando.append(bMenos, bMas);
  bMenos.addEventListener('click', () => { if (sel >= 0 && !mover(sel, -1) && !resuelto) ui.say('Esa pieza no puede moverse en esa dirección: hay algo en medio.', 'bad'); else if (!resuelto) ui.say(''); });
  bMas.addEventListener('click', () => { if (sel >= 0 && !mover(sel, 1) && !resuelto) ui.say('Esa pieza no puede moverse en esa dirección: hay algo en medio.', 'bad'); else if (!resuelto) ui.say(''); });

  function etiquetas() {
    if (sel < 0) { bMenos.textContent = 'Elegid una pieza'; bMas.textContent = ''; bMenos.disabled = true; bMas.disabled = true; bMas.style.display = 'none'; bMenos.style.display = ''; return; }
    const hor = piezas[sel].hor;
    bMenos.style.display = ''; bMas.style.display = '';
    bMenos.disabled = false; bMas.disabled = false;
    bMenos.textContent = hor ? '‹ Izquierda' : '˄ Arriba';
    bMas.textContent = hor ? 'Derecha ›' : 'Abajo ˅';
  }

  function pintar() {
    const s = celda();
    piezas.forEach((k, i) => {
      const e = els[i];
      e.style.left = (k.c * s + 2) + 'px'; e.style.top = (k.r * s + 2) + 'px';
      e.style.width = ((k.hor ? k.largo : 1) * s - 4) + 'px'; e.style.height = ((k.hor ? 1 : k.largo) * s - 4) + 'px';
      e.classList.toggle('sel', sel === i);
    });
    info.textContent = 'Movimientos: ' + movs;
    etiquetas();
  }

  let arr = null;
  function empezarArrastre(ev, i) {
    if (resuelto) return;
    ev.preventDefault();
    sel = i;
    pintar();
    arr = { i, x0: ev.clientX, y0: ev.clientY, acum: 0 };
    try { ev.target.setPointerCapture(ev.pointerId); } catch (e) { /* ignore */ }
    ev.target.onpointermove = e => {
      if (!arr) return;
      const k = piezas[arr.i], s2 = celda();
      const d = k.hor ? e.clientX - arr.x0 : e.clientY - arr.y0;
      const pasos = Math.trunc(d / s2) - arr.acum;
      for (let p = 0; p < Math.abs(pasos); p++) { if (mover(arr.i, Math.sign(pasos))) arr.acum += Math.sign(pasos); else break; }
    };
    ev.target.onpointerup = ev.target.onpointercancel = () => { arr = null; };
  }

  function inicio() {
    piezas = PIEZAS.map(c => ({ r: c[0], c: c[1], largo: c[2], hor: c[3] }));
    movs = 0; resuelto = false; sel = -1;
    ui.say('');
    pintar();
  }

  PIEZAS.forEach((c, i) => {
    const e = document.createElement('div');
    e.className = 'pue-pieza ' + (c[3] ? 'tronco' : 'carro');
    e.dataset.i = String(i);
    e.setAttribute('role', 'button');
    e.setAttribute('tabindex', '0');
    e.setAttribute('aria-label', (c[3] ? 'Tronco' : 'Carro') + ' de ' + c[2] + ' casillas, fila ' + (c[0] + 1) + ' columna ' + (c[1] + 1));
    e.addEventListener('pointerdown', ev => empezarArrastre(ev, i));
    e.addEventListener('click', () => { if (!resuelto) { sel = i; pintar(); } });
    e.addEventListener('keydown', ev => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); sel = i; pintar(); } });
    tablero.appendChild(e);
    els.push(e);
    conImagen(e, c[3] ? 'tronco.jpg' : 'carro.jpg');
  });

  const onResize = () => pintar();
  window.addEventListener('resize', onResize);
  ui.onClose(() => window.removeEventListener('resize', onResize));
  ui.button('Reiniciar', 'ghost', () => { inicio(); });
  inicio();
  return { close: ui.close };
}
