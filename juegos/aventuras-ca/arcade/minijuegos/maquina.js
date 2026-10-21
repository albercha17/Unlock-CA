// Piezas comunes de los minijuegos de «Game Over, 1985» (versión de 60 cartas): estilos, contadores y rejillas en estilo recreativa.

export function estilo(id, css) {
  if (document.getElementById(id)) return;
  const s = document.createElement('style');
  s.id = id;
  s.textContent = css;
  document.head.appendChild(s);
}

export const NEON = ['#ff505a', '#00e2ff', '#5aff96', '#ffde46', '#ff46c8', '#ff9632', '#966eff', '#f0f0ff'];

estilo('ar-base', `
  .ar-fila{display:flex;align-items:center;justify-content:center;gap:10px;margin:8px 0}
  .ar-fila button{width:46px;height:46px;border-radius:8px;border:2px solid #ff5ad8;background:linear-gradient(180deg,#3a1458,#1c0a30);color:#ffd6f6;font:700 1.2rem system-ui;cursor:pointer;box-shadow:0 3px 0 #0d0518}
  .ar-num{min-width:60px;text-align:center;font:700 1.6rem ui-monospace,monospace;color:#8ffcff}
  .ar-etq{font:700 .8rem system-ui;color:#ffd6f6;min-width:110px;text-align:right}
  .ar-rejilla{display:grid;gap:3px;width:min(84vw,340px);margin:6px auto;padding:6px;border-radius:10px;background:#0a0418;border:2px solid #2ee67a}
  .ar-cel{aspect-ratio:1;border:0;border-radius:3px;background:#1e1040;padding:0;cursor:pointer;color:#8ffcff;font:700 .85rem ui-monospace,monospace;display:flex;align-items:center;justify-content:center}
  .ar-pie{text-align:center;color:#ffd6f6;font:700 .85rem system-ui;margin:4px 0}
  .ar-pantalla{margin:6px auto 12px;padding:10px 12px;border-radius:10px;border:2px solid #2ee67a;background:#04140a;color:#7dffae;font:700 1.05rem ui-monospace,monospace;text-align:center;box-shadow:inset 0 0 18px rgba(46,230,122,.3)}
  .ar-btns{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:8px 0}
  .ar-btns button{min-width:44px;min-height:44px;border-radius:8px;border:2px solid #ff5ad8;background:linear-gradient(180deg,#3a1458,#1c0a30);color:#ffd6f6;font:700 1rem system-ui;cursor:pointer;box-shadow:0 3px 0 #0d0518;padding:0 12px}
`);

// Fila con una etiqueta, «−», un número y «+»; `clave` queda en data-c y el valor en data-v.
export function contador(etq, max, onCambio, clave) {
  const f = document.createElement('div');
  f.className = 'ar-fila';
  f.dataset.c = clave;
  const t = document.createElement('span');
  t.className = 'ar-etq';
  t.textContent = etq;
  const menos = document.createElement('button'); menos.type = 'button'; menos.textContent = '−'; menos.dataset.d = '-1';
  const num = document.createElement('span'); num.className = 'ar-num';
  const mas = document.createElement('button'); mas.type = 'button'; mas.textContent = '+'; mas.dataset.d = '1';
  f.append(t, menos, num, mas);
  let v = 0;
  const pintar = () => { num.textContent = String(v); f.dataset.v = String(v); };
  [menos, mas].forEach(b => b.addEventListener('click', () => { v = Math.max(0, Math.min(max, v + Number(b.dataset.d))); pintar(); onCambio(v); }));
  pintar();
  return { el: f, valor: () => v, poner(x) { v = x; pintar(); } };
}

// Rejilla de n columnas por m filas de botones; devuelve el elemento y un acceso a las celdas.
export function rejilla(cols, filas, onClick, clase = '') {
  const el = document.createElement('div');
  el.className = 'ar-rejilla ' + clase;
  el.style.gridTemplateColumns = 'repeat(' + cols + ',1fr)';
  const celdas = {};
  for (let y = 0; y < filas; y++) for (let x = 0; x < cols; x++) {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'ar-cel';
    b.dataset.x = String(x);
    b.dataset.y = String(y);
    b.setAttribute('aria-label', 'Casilla ' + (x + 1) + ',' + (y + 1));
    b.addEventListener('click', () => onClick(x, y, b));
    celdas[x + ',' + y] = b;
    el.appendChild(b);
  }
  return { el, celda: (x, y) => celdas[x + ',' + y] };
}
