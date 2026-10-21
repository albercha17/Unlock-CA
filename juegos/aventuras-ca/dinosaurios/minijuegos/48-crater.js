// Carta 48 — El cráter: marcar en el mapa del valle dónde cayó la piedra de fuego. Tres vigías la vieron caer en una dirección cada uno
// (carta 53); dónde está cada vigía, en el mapa (cartas 42 y 49). En la app el valle está vacío. Solución única (instancias_dinosaurios.py, CRATER).
import { openGame } from './ui.js';
import { estilo, rejilla, LETRAS } from './valle.js';

const D = /*DATOS*/{"n": 8, "vigias": [{"nombre": "Roca del Cuerno", "x": 3, "y": 1, "rumbo": "SE"}, {"nombre": "Árbol Hueco", "x": 5, "y": 1, "rumbo": "S"}, {"nombre": "Colina Pelada", "x": 3, "y": 5, "rumbo": "NE"}], "solucion": [5, 3]}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 48 — El cráter', instr: 'Tocad la casilla del valle donde cayó la piedra de fuego y pulsad «Ir allí». Solo hay fuerzas para una expedición cada vez.', ...opts });
  estilo('dn-crater', `.cra .dn-cel{background:#7d9a54}.cra .dn-cel.marca{background:radial-gradient(circle,#ffb04a 25%,#c8501a 45%,#7d9a54 70%)}`);
  let marca = null, resuelto = false;
  const r = rejilla(D.n, (x, y, b) => {
    if (resuelto) return;
    if (marca) r.celda(marca[0], marca[1]).classList.remove('marca');
    marca = [x, y]; b.classList.add('marca'); ui.say('Marcada la casilla ' + LETRAS[x] + (y + 1) + '.');
  }, true);
  r.el.classList.add('cra');
  ui.body.appendChild(r.el);
  ui.button('Ir allí', 'primary', () => {
    if (resuelto) return;
    if (!marca) { ui.say('Marcad antes una casilla.', 'bad'); return; }
    if (marca[0] === D.solucion[0] && marca[1] === D.solucion[1]) {
      resuelto = true;
      ui.say('Ahí está el cráter, todavía humeante. En el borde, alguien agita un sombrero y os llama a gritos. Coged la carta 36.', 'ok');
    } else ui.say('Allí solo hay helechos aplastados. Alguno de los tres vigías no vio caer nada en esa dirección (cartas 42, 49 y 53).', 'bad');
  });
  return { close: ui.close };
}
