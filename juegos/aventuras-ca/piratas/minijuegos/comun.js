// Piezas comunes de los minijuegos de «Mar de las Brumas, 1715» (versión de 60 cartas): estilos de cubierta y bodega, contadores y botoneras.

export function estilo(id, css) {
  if (document.getElementById(id)) return;
  const s = document.createElement('style');
  s.id = id;
  s.textContent = css;
  document.head.appendChild(s);
}

estilo('pi-base', `
  .pi-btns{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:8px 0}
  .pi-btns button,.pi-opc{min-width:44px;min-height:44px;border-radius:10px;border:2px solid #e8b84a;background:#173a46;color:#f6e7b8;font:700 1rem system-ui,sans-serif;cursor:pointer;padding:0 12px}
  .pi-btns button.sel,.pi-opc.sel{background:#e8b84a;color:#10242c}
  .pi-pie{text-align:center;color:#9fe0e0;font:700 .9rem system-ui,sans-serif;margin:6px 0}
  .pi-fila{max-width:340px;margin:8px auto;padding:8px;border-radius:8px;background:#0c2a34;border:2px solid #e8b84a;color:#f6e7b8;font:700 .9rem system-ui,sans-serif}
  .pi-fila b{display:block;color:#e8b84a;margin-bottom:6px}
`);

estilo('pi-cont', `
  .pi-cont{display:flex;align-items:center;justify-content:space-between;gap:8px;max-width:340px;margin:8px auto;padding:8px 10px;border-radius:8px;background:#0c2a34;border:2px solid #9fe0e0;color:#f6e7b8;font:700 .95rem system-ui,sans-serif}
  .pi-cont output{min-width:48px;text-align:center;font:800 1.4rem system-ui,sans-serif;color:#ffe08a}
  .pi-cont button{min-width:44px;min-height:44px;border-radius:8px;border:2px solid #e8b84a;background:#1d5566;color:#fff;font:800 1.2rem system-ui,sans-serif;cursor:pointer}
`);

// Contador con botones − y +; devuelve el elemento y un acceso al valor. `paso` es lo que suma o resta cada pulsación.
export function contador(etiqueta, min, max, inicial, nombre, paso = 1) {
  const el = document.createElement('div');
  el.className = 'pi-cont';
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
  menos.addEventListener('click', () => { if (v - paso >= min) v -= paso; pintar(); });
  mas.addEventListener('click', () => { if (v + paso <= max) v += paso; pintar(); });
  el.append(t, menos, o, mas);
  pintar();
  return { el, valor: () => v };
}

// Botón de opción con texto; `onClick` recibe el botón.
export function opcion(texto, onClick, clase = 'pi-opc') {
  const b = document.createElement('button');
  b.type = 'button';
  b.className = clase;
  b.textContent = texto;
  b.addEventListener('click', () => onClick(b));
  return b;
}
