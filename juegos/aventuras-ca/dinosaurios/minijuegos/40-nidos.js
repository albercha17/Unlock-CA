// Carta 40 — La playa de los nidos (tipo «Tents»): marcar los nidos de las madres maiasaura. Cada nido va pegado de lado a su helecho
// y ninguno toca a otro, ni en diagonal (carta 45). Cuántos huevos se ven por fila y por columna: cartas 41 y 43 (la app no lo dice).
// Solución única (instancias_dinosaurios.py, NIDOS).
import { openGame } from './ui.js';
import { estilo, rejilla } from './valle.js';

const D = /*DATOS*/{"n": 6, "helechos": [[0, 2], [1, 0], [1, 4], [2, 5], [3, 5], [5, 0], [5, 4]], "filas": [1, 1, 1, 1, 2, 1], "cols": [2, 1, 1, 0, 1, 2], "solucion": [[0, 0], [0, 4], [1, 2], [2, 4], [4, 5], [5, 1], [5, 3]]}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 40 — La playa de los nidos', instr: 'Tocad la arena donde creáis que hay un nido (otra vez para quitarlo). Los helechos ya están dibujados. Cuando lo tengáis, pulsad «Comprobar».', ...opts });
  estilo('dn-nidos', `
    .nid .dn-cel{background:#d8c08a}
    .nid .dn-cel.hel{background:#3f6a2a;font-size:1.3rem}
    .nid .dn-cel.nido{background:radial-gradient(circle,#fff8e6 30%,#a87a3a 34%,#d8c08a 62%)}`);
  const hel = new Set(D.helechos.map(([x, y]) => x + ',' + y));
  const nidos = new Set();
  let resuelto = false;
  const r = rejilla(D.n, (x, y, b) => {
    if (resuelto || hel.has(x + ',' + y)) return;
    const k = x + ',' + y;
    nidos.has(k) ? nidos.delete(k) : nidos.add(k);
    b.classList.toggle('nido', nidos.has(k));
    ui.say('');
  }, true);
  r.el.classList.add('nid');
  for (const k of hel) { const [x, y] = k.split(',').map(Number); const c = r.celda(x, y); c.classList.add('hel'); c.textContent = '🌿'; c.disabled = true; }
  ui.body.appendChild(r.el);
  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    const sol = new Set(D.solucion.map(([x, y]) => x + ',' + y));
    const toca = [...nidos].some(a => [...nidos].some(b => a !== b && Math.max(Math.abs(a.split(',')[0] - b.split(',')[0]), Math.abs(a.split(',')[1] - b.split(',')[1])) <= 1));
    if (toca) { ui.say('Dos madres no soportan tenerse al lado, ni en diagonal (carta 45).', 'bad'); return; }
    if (nidos.size === sol.size && [...nidos].every(k => sol.has(k))) {
      resuelto = true;
      ui.say('¡Todos los nidos! Las madres se calman y os dejan pasar entre ellos hasta la tienda de la doctora. Coged la carta 30.', 'ok');
    } else ui.say('Desde el acantilado y desde la duna no se verían así los huevos (cartas 41 y 43).', 'bad');
  });
  return { close: ui.close };
}
