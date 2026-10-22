// Piezas comunes de los minijuegos de «El Cuarto de Leo, 1995» (versión de 62 cartas): estilos de juguetería y botoneras.

export function estilo(id, css) {
  if (document.getElementById(id)) return;
  const s = document.createElement('style');
  s.id = id;
  s.textContent = css;
  document.head.appendChild(s);
}

estilo('ju-base', `
  .ju-btns{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:8px 0}
  .ju-opc{min-width:44px;min-height:44px;border-radius:12px;border:3px solid #ffcc33;background:#1e3470;color:#fff;font:700 1rem 'Fredoka',system-ui,sans-serif;cursor:pointer;padding:0 10px}
  .ju-opc.sel{background:#ffcc33;color:#1a2a5a}
  .ju-pie{text-align:center;color:#ffcc33;font:700 .95rem 'Fredoka',system-ui,sans-serif;margin:6px 0}
  .ju-in{display:block;width:100%;max-width:300px;margin:8px auto;padding:10px;border-radius:10px;border:3px solid #ffcc33;background:#fff;color:#1a2a5a;font:700 1.2rem 'Fredoka',system-ui,sans-serif;text-align:center}
`);

// Botón de opción con texto; `onClick` recibe el botón.
export function opcion(texto, onClick, clase = 'ju-opc') {
  const b = document.createElement('button');
  b.type = 'button';
  b.className = clase;
  b.textContent = texto;
  b.addEventListener('click', () => onClick(b));
  return b;
}
