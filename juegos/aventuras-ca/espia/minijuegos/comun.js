// Piezas comunes de los minijuegos de «Montecarlo, 1965: Operación Cristal» (versión de 60 cartas): estilos pop de espías, rejillas y teclado de cifras.

export function estilo(id, css) {
  if (document.getElementById(id)) return;
  const s = document.createElement('style');
  s.id = id;
  s.textContent = css;
  document.head.appendChild(s);
}

export const COLORES = { rojo: '#d63a3a', azul: '#2f6fd6', amarillo: '#f2c230', negro: '#1c1c22', blanco: '#f4f4f4' };

estilo('es-base', `
  .es-rejilla{display:grid;gap:3px;width:min(86vw,330px);margin:8px auto;padding:6px;border-radius:8px;background:#0a2a36;border:3px solid #ff6fa8}
  .es-cel{aspect-ratio:1;border:0;border-radius:3px;background:#e9f8fa;padding:0;cursor:pointer;color:#0a2a36;font:800 1.3rem system-ui,Arial,sans-serif;display:flex;align-items:center;justify-content:center;min-height:36px}
  .es-cel.sel{outline:3px solid #ff6fa8;background:#fff3a8}
  .es-nums{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;max-width:340px;margin:8px auto}
  .es-nums button,.es-btns button{min-width:44px;min-height:44px;border-radius:8px;border:2px solid #ff6fa8;background:linear-gradient(180deg,#1c7a8a,#0a2a36);color:#e9fcff;font:700 1rem system-ui,Arial,sans-serif;cursor:pointer;box-shadow:0 3px 0 #04141a;padding:0 12px}
  .es-btns{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:8px 0}
  .es-btns button.sel,.es-nums button.sel{background:#ff6fa8;color:#1c0a14}
  .es-pie{text-align:center;color:#7fe8f0;font:700 .9rem system-ui,Arial,sans-serif;margin:4px 0}
  .es-in{display:block;width:100%;max-width:340px;margin:10px auto;padding:12px;border-radius:8px;border:3px solid #ff6fa8;background:#e9f8fa;color:#0a2a36;font:700 1.1rem system-ui,Arial,sans-serif;text-transform:uppercase}
`);

// Rejilla de `cols` columnas por `filas` filas de botones; devuelve el elemento y un acceso a las celdas.
export function rejilla(cols, filas, onClick, clase = '') {
  const el = document.createElement('div');
  el.className = 'es-rejilla ' + clase;
  el.style.gridTemplateColumns = 'repeat(' + cols + ',1fr)';
  const celdas = {};
  for (let r = 0; r < filas; r++) for (let c = 0; c < cols; c++) {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'es-cel';
    b.dataset.r = String(r);
    b.dataset.c = String(c);
    b.setAttribute('aria-label', 'Casilla fila ' + (r + 1) + ', columna ' + (c + 1));
    b.addEventListener('click', () => onClick(r, c, b));
    celdas[r + ',' + c] = b;
    el.appendChild(b);
  }
  return { el, celda: (r, c) => celdas[r + ',' + c] };
}

// Fila de botones con las cifras de `desde` a `hasta`.
export function teclado(desde, hasta, onClick, clase = 'es-nums') {
  const el = document.createElement('div');
  el.className = clase;
  for (let d = desde; d <= hasta; d++) {
    const b = document.createElement('button');
    b.type = 'button';
    b.dataset.n = String(d);
    b.textContent = String(d);
    b.addEventListener('click', () => onClick(d));
    el.appendChild(b);
  }
  return el;
}

estilo('es-cont', `
  .es-cont{display:flex;align-items:center;justify-content:space-between;gap:8px;max-width:340px;margin:8px auto;padding:8px 10px;border-radius:8px;background:#0a2a36;border:2px solid #7fe8f0;color:#e9fcff;font:700 .95rem system-ui,Arial,sans-serif}
  .es-cont output{min-width:56px;text-align:center;font:800 1.4rem system-ui,Arial,sans-serif;color:#ffe08a}
  .es-cont button{min-width:44px;min-height:44px;border-radius:8px;border:2px solid #ff6fa8;background:#1c7a8a;color:#fff;font:800 1.2rem system-ui,Arial,sans-serif;cursor:pointer}
`);

// Contador con botones − y +; devuelve el elemento y un acceso al valor.
export function contador(etiqueta, min, max, inicial, nombre) {
  const el = document.createElement('div');
  el.className = 'es-cont';
  el.dataset.nombre = nombre;
  let v = inicial;
  const t = document.createElement('span');
  t.textContent = etiqueta;
  const menos = document.createElement('button');
  const mas = document.createElement('button');
  const o = document.createElement('output');
  menos.type = mas.type = 'button';
  menos.textContent = '−';
  mas.textContent = '+';
  menos.dataset.d = '-1';
  mas.dataset.d = '1';
  menos.setAttribute('aria-label', 'Restar a ' + etiqueta);
  mas.setAttribute('aria-label', 'Sumar a ' + etiqueta);
  const pintar = () => { o.textContent = String(v); el.dataset.v = String(v); };
  menos.addEventListener('click', () => { if (v > min) v--; pintar(); });
  mas.addEventListener('click', () => { if (v < max) v++; pintar(); });
  el.append(t, menos, o, mas);
  pintar();
  return { el, valor: () => v };
}

// Normaliza un texto: mayúsculas, sin acentos ni espacios.
export function limpio(t) {
  return String(t).normalize('NFD').replace(/[̀-ͯ]/g, '').toUpperCase().replace(/[^A-Z]/g, '');
}
