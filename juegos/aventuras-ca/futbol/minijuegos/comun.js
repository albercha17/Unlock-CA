// Piezas comunes de los minijuegos de «La Final del Siglo, 1970» (versión de 60 cartas): estilos de césped y marcador, contadores y botoneras.

export function estilo(id, css) {
  if (document.getElementById(id)) return;
  const s = document.createElement('style');
  s.id = id;
  s.textContent = css;
  document.head.appendChild(s);
}

estilo('fu-base', `
  .fu-btns{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:8px 0}
  .fu-btns button,.fu-opc{min-width:44px;min-height:44px;border-radius:8px;border:2px solid #f2c230;background:linear-gradient(180deg,#2f8a40,#145a24);color:#f4fff0;font:700 .95rem system-ui,Arial,sans-serif;cursor:pointer;box-shadow:0 3px 0 #08300f;padding:0 12px}
  .fu-btns button.sel,.fu-opc.sel{background:#f2c230;color:#12310f}
  .fu-pie{text-align:center;color:#c9f5c0;font:700 .9rem system-ui,Arial,sans-serif;margin:6px 0}
  .fu-fila{max-width:340px;margin:8px auto;padding:8px;border-radius:8px;background:#0e3a18;border:2px solid #f2c230;color:#f4fff0;font:700 .9rem system-ui,Arial,sans-serif}
  .fu-fila b{display:block;color:#f2c230;margin-bottom:6px}
  .fu-in{display:block;width:100%;max-width:340px;margin:10px auto;padding:12px;border-radius:8px;border:3px solid #f2c230;background:#f4fff0;color:#12310f;font:700 1.1rem system-ui,Arial,sans-serif}
`);

estilo('fu-cont', `
  .fu-cont{display:flex;align-items:center;justify-content:space-between;gap:8px;max-width:340px;margin:8px auto;padding:8px 10px;border-radius:8px;background:#0e3a18;border:2px solid #c9f5c0;color:#f4fff0;font:700 .95rem system-ui,Arial,sans-serif}
  .fu-cont output{min-width:48px;text-align:center;font:800 1.4rem system-ui,Arial,sans-serif;color:#ffe08a}
  .fu-cont button{min-width:44px;min-height:44px;border-radius:8px;border:2px solid #f2c230;background:#2f8a40;color:#fff;font:800 1.2rem system-ui,Arial,sans-serif;cursor:pointer}
`);

// Contador con botones − y +; devuelve el elemento y un acceso al valor.
export function contador(etiqueta, min, max, inicial, nombre) {
  const el = document.createElement('div');
  el.className = 'fu-cont';
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

// Botón de opción con texto; `onClick` recibe el botón.
export function opcion(texto, onClick, clase = 'fu-opc') {
  const b = document.createElement('button');
  b.type = 'button';
  b.className = clase;
  b.textContent = texto;
  b.addEventListener('click', () => onClick(b));
  return b;
}
