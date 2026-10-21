// Carta 72 — Planear con el Quetzal: llevar al pterosaurio del acantilado al nido de la doctora. Cada casilla cuesta un palmo de altura;
// las térmicas (solo en la carta 75) devuelven altura la primera vez; las montañas, tampoco en la app, no se cruzan (regla: carta 79).
// Vale cualquier vuelo que llegue (instancias_dinosaurios.py, PLANEAR; hacen falta al menos tres térmicas).
import { openGame } from './ui.js';
import { estilo, rejilla, flechas, DIRS } from './valle.js';

const D = /*DATOS*/{"n": 6, "inicio": [0, 0], "nido": [5, 5], "altura": 3, "montes": [[1, 5], [3, 2], [4, 0], [4, 3], [5, 2]], "termicas": [[2, 0, 3], [3, 1, 4], [3, 4, 4], [5, 0, 2]], "minimo_termicas": 3, "solucion": ["derecha", "derecha", "derecha", "abajo", "izquierda", "abajo", "abajo", "derecha", "abajo", "derecha", "derecha", "abajo"]}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 72 — Planear con el Quetzal', instr: 'Montáis en el pterosaurio y saltáis del acantilado. Guiadlo casilla a casilla con las flechas hasta el nido de la doctora sin tocar el suelo.', ...opts });
  estilo('dn-planear', `.pla .dn-cel{background:#8ab4d0}.pla .dn-cel.yo{background:radial-gradient(circle,#ffe08a 30%,#8ab4d0 70%)}.pla .dn-cel.paso{background:#a6c8de}.pla .dn-cel.nido{background:radial-gradient(circle,#fff8e6 22%,#a87a3a 26%,#8ab4d0 55%)}`);
  const montes = new Set(D.montes.map(([x, y]) => x + ',' + y));
  const term = {}; D.termicas.forEach(([x, y, k]) => { term[x + ',' + y] = k; });
  let pos, alt, usadas, pasos, resuelto = false;
  const r = rejilla(D.n, () => {}, false);
  r.el.classList.add('pla');
  const pie = document.createElement('p'); pie.className = 'dn-pie';
  ui.body.append(r.el, pie);
  const reiniciar = () => { pos = D.inicio.slice(); alt = D.altura; usadas = new Set(); pasos = new Set([pos.join(',')]); };
  function pintar() {
    for (let y = 0; y < D.n; y++) for (let x = 0; x < D.n; x++) {
      const k = x + ',' + y, c = r.celda(x, y);
      c.disabled = true;
      c.className = 'dn-cel' + (k === pos.join(',') ? ' yo' : k === D.nido.join(',') ? ' nido' : pasos.has(k) ? ' paso' : '');
    }
    pie.textContent = 'Altura: ' + '▮'.repeat(alt) + ' (' + alt + ' palmos)';
    r.el.dataset.pos = pos.join(','); r.el.dataset.alt = String(alt);
  }
  ui.body.appendChild(flechas(d => {
    if (resuelto) return;
    const [dx, dy] = DIRS[d], x = pos[0] + dx, y = pos[1] + dy, k = x + ',' + y;
    if (x < 0 || y < 0 || x >= D.n || y >= D.n) { ui.say('Por ahí se sale del valle.', 'bad'); return; }
    if (montes.has(k)) { ui.say('¡Una montaña! El Quetzal da media vuelta asustado y volvéis al acantilado.', 'bad'); reiniciar(); pintar(); return; }
    if (alt === 0) { ui.say('Sin altura no se puede seguir: el Quetzal toca el suelo. Volvéis al acantilado (cartas 75 y 79).', 'bad'); reiniciar(); pintar(); return; }
    alt -= 1; pos = [x, y]; pasos.add(k);
    if (term[k] && !usadas.has(k)) { alt += term[k]; usadas.add(k); ui.say('¡Una térmica! El Quetzal sube en espiral.', 'ok'); } else ui.say('');
    if (x === D.nido[0] && y === D.nido[1]) {
      resuelto = true; pintar();
      ui.say('El Quetzal se posa en el nido de la doctora, en lo alto de la cueva. Dentro hay un diario y tres cortes de tronco. Coged la carta 82.', 'ok');
      return;
    }
    pintar();
  }));
  ui.button('Volver al acantilado', '', () => { if (!resuelto) { reiniciar(); ui.say(''); pintar(); } });
  reiniciar();
  pintar();
  return { close: ui.close };
}
