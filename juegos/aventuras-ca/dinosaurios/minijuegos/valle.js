// Piezas comunes de los minijuegos de «Dinosaurios» (versión de 60 cartas): estilos y cuadrículas.

export function estilo(id, css) {
  if (document.getElementById(id)) return;
  const s = document.createElement('style');
  s.id = id;
  s.textContent = css;
  document.head.appendChild(s);
}

estilo('dn-base', `
  .dn-rejilla{display:grid;gap:3px;width:min(84vw,320px);margin:6px auto;padding:6px;border-radius:10px;background:#2a3a1e;box-shadow:inset 0 0 18px rgba(0,0,0,.6)}
  .dn-cel{aspect-ratio:1;border:0;border-radius:4px;background:#5f7a3e;padding:0;cursor:pointer;font:800 .8rem system-ui;color:#f6f0d8;display:flex;align-items:center;justify-content:center;line-height:1}
  .dn-cel:disabled{cursor:default}
  .dn-chips{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin:8px auto;max-width:340px}
  .dn-chip{border-radius:999px;border:2px solid #b5e35b;background:#2f4a1e;color:#f2ffd6;font:700 .78rem system-ui;padding:7px 11px;cursor:pointer}
  .dn-chip.sel{background:#b5e35b;color:#1a2a0c}
  .dn-chip.usado{opacity:.35}
  .dn-num{min-width:64px;text-align:center;font:800 2rem Georgia,serif;color:#f2ffd6}
  .dn-fila{display:flex;align-items:center;justify-content:center;gap:10px;margin:8px 0}
  .dn-fila button{width:46px;height:46px;border-radius:50%;border:2px solid #b5e35b;background:#3d5a24;color:#f2ffd6;font:800 1.3rem system-ui;cursor:pointer}
  .dn-etq{font:700 .85rem system-ui;color:#f2ffd6;min-width:110px;text-align:right}
  .dn-dirs{display:grid;grid-template-columns:repeat(3,54px);grid-template-rows:repeat(2,44px);gap:6px;justify-content:center;margin:8px auto}
  .dn-dirs button{border-radius:10px;border:2px solid #b5e35b;background:#3d5a24;color:#f2ffd6;font:800 1.2rem system-ui;cursor:pointer}
  .dn-dirs [data-d=arriba]{grid-column:2;grid-row:1}.dn-dirs [data-d=izquierda]{grid-column:1;grid-row:2}
  .dn-dirs [data-d=abajo]{grid-column:2;grid-row:2}.dn-dirs [data-d=derecha]{grid-column:3;grid-row:2}
  .dn-pie{text-align:center;color:#f2ffd6;font:700 .85rem system-ui;margin:2px 0}
`);

export const LETRAS = 'ABCDEFGH';
export const DIRS = { arriba: [0, -1], derecha: [1, 0], abajo: [0, 1], izquierda: [-1, 0] };

// Rejilla n x n de botones; devuelve { el, celda(x, y) }. Con etiquetas, añade letras arriba y números a la izquierda.
export function rejilla(n, onClick, etiquetas = false) {
  const el = document.createElement('div');
  el.className = 'dn-rejilla';
  const m = etiquetas ? n + 1 : n;
  el.style.gridTemplateColumns = 'repeat(' + m + ',1fr)';
  const celdas = {};
  for (let y = etiquetas ? -1 : 0; y < n; y++) {
    for (let x = etiquetas ? -1 : 0; x < n; x++) {
      if (x < 0 || y < 0) {
        const e = document.createElement('div');
        e.className = 'dn-pie';
        e.textContent = x < 0 && y < 0 ? '' : y < 0 ? LETRAS[x] : String(y + 1);
        el.appendChild(e);
        continue;
      }
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'dn-cel';
      b.dataset.x = String(x);
      b.dataset.y = String(y);
      b.setAttribute('aria-label', 'Casilla ' + LETRAS[x] + (y + 1));
      b.addEventListener('click', () => onClick(x, y, b));
      celdas[x + ',' + y] = b;
      el.appendChild(b);
    }
  }
  return { el, celda: (x, y) => celdas[x + ',' + y] };
}

export function flechas(onDir) {
  const d = document.createElement('div');
  d.className = 'dn-dirs';
  Object.keys(DIRS).forEach(k => {
    const b = document.createElement('button');
    b.type = 'button';
    b.dataset.d = k;
    b.textContent = { arriba: '▲', abajo: '▼', izquierda: '◀', derecha: '▶' }[k];
    b.setAttribute('aria-label', 'Hacia ' + k);
    b.addEventListener('click', () => onDir(k));
    d.appendChild(b);
  });
  return d;
}

export function contador(etq, max, onCambio, clave) {
  const f = document.createElement('div');
  f.className = 'dn-fila';
  f.dataset.c = clave;
  const t = document.createElement('span'); t.className = 'dn-etq'; t.textContent = etq;
  const menos = document.createElement('button'); menos.type = 'button'; menos.textContent = '−'; menos.dataset.d = '-1';
  const num = document.createElement('span'); num.className = 'dn-num';
  const mas = document.createElement('button'); mas.type = 'button'; mas.textContent = '+'; mas.dataset.d = '1';
  f.append(t, menos, num, mas);
  let v = 0;
  const pintar = () => { num.textContent = String(v); f.dataset.v = String(v); };
  [menos, mas].forEach(b => b.addEventListener('click', () => { v = Math.max(0, Math.min(max, v + Number(b.dataset.d))); pintar(); onCambio(v); }));
  pintar();
  return { el: f, valor: () => v };
}
