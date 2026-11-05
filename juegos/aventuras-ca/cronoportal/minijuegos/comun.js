// Piezas comunes de los minijuegos de «El primer salto» (nivel de prueba): estilos que se añaden una sola vez.

export function estilo(id, css) {
  if (document.getElementById(id)) return;
  const s = document.createElement('style');
  s.id = id;
  s.textContent = css;
  document.head.appendChild(s);
}
