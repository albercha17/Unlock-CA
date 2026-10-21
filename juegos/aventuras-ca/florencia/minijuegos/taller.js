// Piezas comunes de los minijuegos de «Florencia» (versión de 60 cartas): estilos, figuras en SVG y contadores.

export function estilo(id, css) {
  if (document.getElementById(id)) return;
  const s = document.createElement('style');
  s.id = id;
  s.textContent = css;
  document.head.appendChild(s);
}

estilo('fl-base', `
  .fl-fila{display:flex;align-items:center;justify-content:center;gap:10px;margin:8px 0}
  .fl-fila button{width:46px;height:46px;border-radius:50%;border:2px solid #d9a441;background:linear-gradient(180deg,#76603a,#4d3c20);color:#f6e7bf;font:800 1.3rem system-ui;cursor:pointer}
  .fl-num{min-width:60px;text-align:center;font:800 2rem Georgia,serif;color:#f6e7bf}
  .fl-etq{font:700 .85rem system-ui;color:#f6e7bf;min-width:90px;text-align:right}
  .fl-chips{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin:8px auto;max-width:340px}
  .fl-chip{border-radius:999px;border:2px solid #d9a441;background:#4d3c20;color:#f6e7bf;font:700 .78rem system-ui;padding:7px 11px;cursor:pointer}
  .fl-chip.sel{background:#d9a441;color:#2a1f0c}
  .fl-rejilla{display:grid;gap:3px;width:min(84vw,330px);margin:6px auto;padding:6px;border-radius:10px;background:#2a1f0c}
  .fl-cel{aspect-ratio:1;border:0;border-radius:4px;background:#c9a96a;padding:0;cursor:pointer;color:#2a1f0c;font:800 .8rem system-ui;display:flex;align-items:center;justify-content:center}
  .fl-pie{text-align:center;color:#f6e7bf;font:700 .85rem system-ui;margin:2px 0}
`);

export const NS = 'http://www.w3.org/2000/svg';

// Dibuja una figura de las instancias (cajas de 100 x 100) como SVG.
export function figuraSVG(fig, color = '#2a1f0c', fondo = '#f6e7bf', tam = 56, espejo = false) {
  const s = document.createElementNS(NS, 'svg');
  s.setAttribute('viewBox', '0 0 100 100');
  s.setAttribute('width', String(tam));
  s.setAttribute('height', String(tam));
  s.setAttribute('aria-hidden', 'true');
  const g = document.createElementNS(NS, 'g');
  if (espejo) g.setAttribute('transform', 'translate(100,0) scale(-1,1)');
  (fig || []).forEach(e => {
    const col = e.f === 'fondo' ? fondo : color;
    let n;
    if (e.t === 'p') {
      n = document.createElementNS(NS, 'polygon');
      n.setAttribute('points', e.p.map(q => q.join(',')).join(' '));
      n.setAttribute('fill', col);
    } else if (e.t === 'l') {
      n = document.createElementNS(NS, 'polyline');
      n.setAttribute('points', e.p.map(q => q.join(',')).join(' '));
      n.setAttribute('fill', 'none');
      n.setAttribute('stroke', col);
      n.setAttribute('stroke-width', String(e.w));
      n.setAttribute('stroke-linecap', 'round');
      n.setAttribute('stroke-linejoin', 'round');
    } else {
      n = document.createElementNS(NS, 'circle');
      n.setAttribute('cx', String(e.c[0])); n.setAttribute('cy', String(e.c[1])); n.setAttribute('r', String(e.r));
      if (e.w) { n.setAttribute('fill', 'none'); n.setAttribute('stroke', col); n.setAttribute('stroke-width', String(e.w)); } else n.setAttribute('fill', col);
    }
    g.appendChild(n);
  });
  s.appendChild(g);
  return s;
}

export function contador(etq, max, onCambio, clave, icono) {
  const f = document.createElement('div');
  f.className = 'fl-fila';
  f.dataset.c = clave;
  const t = document.createElement('span'); t.className = 'fl-etq';
  if (icono) t.appendChild(icono); else t.textContent = etq;
  const menos = document.createElement('button'); menos.type = 'button'; menos.textContent = '−'; menos.dataset.d = '-1';
  const num = document.createElement('span'); num.className = 'fl-num';
  const mas = document.createElement('button'); mas.type = 'button'; mas.textContent = '+'; mas.dataset.d = '1';
  f.append(t, menos, num, mas);
  let v = 0;
  const pintar = () => { num.textContent = String(v); f.dataset.v = String(v); };
  [menos, mas].forEach(b => b.addEventListener('click', () => { v = Math.max(0, Math.min(max, v + Number(b.dataset.d))); pintar(); onCambio(v); }));
  pintar();
  return { el: f, valor: () => v };
}

export function rejilla(n, onClick, etiquetas = false) {
  const el = document.createElement('div');
  el.className = 'fl-rejilla';
  el.style.gridTemplateColumns = 'repeat(' + (etiquetas ? n + 1 : n) + ',1fr)';
  const celdas = {};
  for (let y = etiquetas ? -1 : 0; y < n; y++) for (let x = etiquetas ? -1 : 0; x < n; x++) {
    if (x < 0 || y < 0) {
      const e = document.createElement('div'); e.className = 'fl-pie';
      e.textContent = x < 0 && y < 0 ? '' : y < 0 ? 'ABCDEFGH'[x] : String(y + 1);
      el.appendChild(e);
      continue;
    }
    const b = document.createElement('button'); b.type = 'button'; b.className = 'fl-cel';
    b.dataset.x = String(x); b.dataset.y = String(y);
    b.setAttribute('aria-label', 'Casilla ' + 'ABCDEFGH'[x] + (y + 1));
    b.addEventListener('click', () => onClick(x, y, b));
    celdas[x + ',' + y] = b;
    el.appendChild(b);
  }
  return { el, celda: (x, y) => celdas[x + ',' + y] };
}
