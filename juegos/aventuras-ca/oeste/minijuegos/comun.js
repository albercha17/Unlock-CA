// Piezas comunes de los minijuegos de «Dry Gulch, 1878» (versión de 60 cartas): estilos, colores y rejillas en estilo Lejano Oeste.

export function estilo(id, css) {
  if (document.getElementById(id)) return;
  const s = document.createElement('style');
  s.id = id;
  s.textContent = css;
  document.head.appendChild(s);
}

export const COLORES = ['#b03a2e', '#3c5c80', '#546e3c', '#d6a046', '#8c5478', '#c86e32', '#5a4632', '#78808a'];

estilo('oe-base', `
  .oe-rejilla{display:grid;gap:3px;width:min(86vw,340px);margin:8px auto;padding:6px;border-radius:8px;background:#3a2412;border:3px solid #8a5a2a}
  .oe-cel{aspect-ratio:1;border:0;border-radius:3px;background:#e6c88c;padding:0;cursor:pointer;color:#3a2412;font:700 1.1rem Georgia,serif;display:flex;align-items:center;justify-content:center;min-height:34px}
  .oe-pie{text-align:center;color:#f5d48a;font:700 .85rem Georgia,serif;margin:4px 0}
  .oe-btns{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:8px 0}
  .oe-btns button{min-width:44px;min-height:44px;border-radius:8px;border:2px solid #e0a040;background:linear-gradient(180deg,#8a5a2a,#4a2c14);color:#f5d48a;font:700 1rem Georgia,serif;cursor:pointer;box-shadow:0 3px 0 #2a1608;padding:0 12px}
  .oe-btns button.sel{background:#e0a040;color:#2a1404}
`);

// Rejilla de `cols` columnas por `filas` filas de botones; devuelve el elemento y un acceso a las celdas.
export function rejilla(cols, filas, onClick, clase = '') {
  const el = document.createElement('div');
  el.className = 'oe-rejilla ' + clase;
  el.style.gridTemplateColumns = 'repeat(' + cols + ',1fr)';
  const celdas = {};
  for (let r = 0; r < filas; r++) for (let c = 0; c < cols; c++) {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'oe-cel';
    b.dataset.r = String(r);
    b.dataset.c = String(c);
    b.setAttribute('aria-label', 'Casilla fila ' + (r + 1) + ', columna ' + (c + 1));
    b.addEventListener('click', () => onClick(r, c, b));
    celdas[r + ',' + c] = b;
    el.appendChild(b);
  }
  return { el, celda: (r, c) => celdas[r + ',' + c] };
}

// Normaliza un texto: mayúsculas, sin acentos ni espacios.
export function limpio(t) {
  return String(t).normalize('NFD').replace(/[̀-ͯ]/g, '').toUpperCase().replace(/[^A-Z]/g, '');
}
