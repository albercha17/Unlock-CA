// Piezas comunes de los minijuegos de «El Faro de Cabo Niebla» (versión de 60 cartas): estilos propios, que se añaden una sola vez.

export function estilo(id, css) {
  if (document.getElementById(id)) return;
  const s = document.createElement('style');
  s.id = id;
  s.textContent = css;
  document.head.appendChild(s);
}

estilo('fa-base', `
  .fa-fila{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:8px 0}
  .fa-opc{min-width:44px;min-height:44px;border-radius:10px;border:1.5px solid rgba(201,164,90,.6);background:linear-gradient(180deg,rgba(255,255,255,.12),rgba(0,0,0,.2));color:#fff;font:700 1rem system-ui,sans-serif;cursor:pointer;padding:0 10px}
  .fa-opc.sel{background:#c9a45a;color:#10202c}
  .fa-pie{text-align:center;color:#ffd27a;font:700 .9rem system-ui,sans-serif;margin:6px 0}
`);
