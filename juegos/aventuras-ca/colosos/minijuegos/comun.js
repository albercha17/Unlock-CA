// Piezas comunes de los minijuegos de «Altamuralla: El Valle de los Colosos»: estilos de piedra y latón, rejillas con coordenadas y glifos.

export function estilo(id, css) {
  if (document.getElementById(id)) return;
  const s = document.createElement('style');
  s.id = id;
  s.textContent = css;
  document.head.appendChild(s);
}

estilo('co-base', `
  .co-rej{display:grid;gap:3px;margin:6px auto;width:max-content;max-width:100%;touch-action:manipulation;user-select:none}
  .co-rej .co-et{display:flex;align-items:center;justify-content:center;color:#ffd27a;font:700 .8rem system-ui,sans-serif}
  .co-c{width:var(--t,40px);height:var(--t,40px);border-radius:6px;border:1.5px solid rgba(224,166,64,.55);background:rgba(255,240,210,.1);
    color:#fff6e4;font:700 1.15rem system-ui,sans-serif;display:flex;align-items:center;justify-content:center;cursor:pointer;padding:0;
    transition:background .18s,transform .12s,box-shadow .18s}
  .co-c:active{transform:scale(.94)}
  .co-c.muro{background:linear-gradient(180deg,#5a4634,#36281c);border-color:#2a1e14;cursor:default}
  .co-c.luz{background:rgba(255,206,110,.32);box-shadow:inset 0 0 10px rgba(255,200,90,.45)}
  .co-c.farol{background:radial-gradient(circle,#fff2b0 0,#ffbe40 45%,#a86414 100%);box-shadow:0 0 14px rgba(255,190,70,.9)}
  .co-c.pisada{background:linear-gradient(180deg,#8a6a40,#4e3a1e);box-shadow:inset 0 0 8px rgba(0,0,0,.6)}
  .co-c.tejado{background:linear-gradient(180deg,#b8573c,#7a301e)}
  .co-btns{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:8px 0}
  .co-opc{min-width:46px;min-height:46px;border-radius:10px;border:1.5px solid #e0a640;background:linear-gradient(180deg,rgba(255,255,255,.1),rgba(0,0,0,.25));
    color:#fff6e4;font:700 1rem system-ui,sans-serif;cursor:pointer;padding:4px 10px;touch-action:manipulation}
  .co-opc.sel{background:#e0a640;color:#241404}
  .co-opc:disabled{opacity:.45}
  .co-pie{text-align:center;color:#ffd27a;font:700 .92rem system-ui,sans-serif;margin:6px 0;min-height:1.2em}
  .co-lista{display:flex;flex-direction:column;gap:6px;max-width:320px;margin:6px auto}
  .co-lista .co-paso{padding:8px 10px;border-radius:8px;background:rgba(255,240,210,.12);border:1px solid rgba(224,166,64,.5);color:#fff6e4;font:600 .95rem system-ui,sans-serif}
  .co-glifo svg{display:block}
  @media (prefers-reduced-motion: reduce){.co-c,.co-opc{transition:none}}
`);

export function boton(texto, onClick, clase = 'co-opc') {
  const b = document.createElement('button');
  b.type = 'button';
  b.className = clase;
  b.textContent = texto;
  b.addEventListener('click', () => onClick(b));
  return b;
}

export const LET = 'ABCDEFGH';

// Rejilla n x n con letras arriba y números a la izquierda. `celda(f, c, el)` prepara cada casilla. Devuelve {el, celdas}.
export function rejilla(n, celda, tam = 40) {
  const g = document.createElement('div');
  g.className = 'co-rej';
  g.style.gridTemplateColumns = `18px repeat(${n}, ${tam}px)`;
  g.style.setProperty('--t', tam + 'px');
  const celdas = [];
  g.appendChild(document.createElement('span'));
  for (let c = 0; c < n; c++) {
    const e = document.createElement('span');
    e.className = 'co-et';
    e.textContent = LET[c];
    g.appendChild(e);
  }
  for (let f = 0; f < n; f++) {
    const e = document.createElement('span');
    e.className = 'co-et';
    e.textContent = String(f + 1);
    g.appendChild(e);
    celdas.push([]);
    for (let c = 0; c < n; c++) {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'co-c';
      b.dataset.f = f;
      b.dataset.c = c;
      b.setAttribute('aria-label', LET[c] + (f + 1));
      celda(f, c, b);
      g.appendChild(b);
      celdas[f].push(b);
    }
  }
  return { el: g, celdas };
}

// Tamaño de casilla que cabe en la pantalla.
export function tamCasilla(n, max = 46) {
  const ancho = Math.min(window.innerWidth || 390, 520) - 70;
  return Math.max(30, Math.min(max, Math.floor(ancho / n) - 3));
}

// Glifo de la lengua del viajero en SVG: trazos de 0 a 1 ("l" línea, "c" círculo, "p" punto).
export function glifoSVG(trazos, tam = 40, color = '#fff6e4') {
  const ns = 'http://www.w3.org/2000/svg';
  const s = document.createElementNS(ns, 'svg');
  s.setAttribute('viewBox', '0 0 100 100');
  s.setAttribute('width', tam);
  s.setAttribute('height', tam);
  s.setAttribute('aria-hidden', 'true');
  trazos.forEach(t => {
    let e;
    if (t[0] === 'l') {
      e = document.createElementNS(ns, 'line');
      e.setAttribute('x1', t[1] * 100); e.setAttribute('y1', t[2] * 100); e.setAttribute('x2', t[3] * 100); e.setAttribute('y2', t[4] * 100);
    } else if (t[0] === 'c') {
      e = document.createElementNS(ns, 'circle');
      e.setAttribute('cx', t[1] * 100); e.setAttribute('cy', t[2] * 100); e.setAttribute('r', t[3] * 100); e.setAttribute('fill', 'none');
    } else {
      e = document.createElementNS(ns, 'circle');
      e.setAttribute('cx', t[1] * 100); e.setAttribute('cy', t[2] * 100); e.setAttribute('r', 7); e.setAttribute('fill', color);
    }
    e.setAttribute('stroke', color);
    e.setAttribute('stroke-width', 8);
    e.setAttribute('stroke-linecap', 'round');
    s.appendChild(e);
  });
  return s;
}

// Tono corto con Web Audio (si el sonido está desactivado o no hay audio, no hace nada).
let ctx = null;
export function tono(freq, dur = 0.4, tipo = 'sine', vol = 0.18) {
  try {
    if (localStorage.getItem('far-sonido') === '0') return;
  } catch (e) { /* sin almacenamiento */ }
  try {
    ctx = ctx || new (window.AudioContext || window.webkitAudioContext)();
    const o = ctx.createOscillator();
    const g = ctx.createGain();
    o.type = tipo;
    o.frequency.value = freq;
    g.gain.setValueAtTime(0.0001, ctx.currentTime);
    g.gain.exponentialRampToValueAtTime(vol, ctx.currentTime + 0.03);
    g.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + dur);
    o.connect(g).connect(ctx.destination);
    o.start();
    o.stop(ctx.currentTime + dur + 0.05);
  } catch (e) { /* sin audio */ }
}
