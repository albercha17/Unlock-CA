// Carta 40 — Los barracones: Fillomino 6 x 6. Cada casilla lleva el tamaño de su barracón; los números ya puestos están en la lista del
// intendente y en el plano a medio hacer. Solución única (herramientas/instancias_colosos.py, barracones).
import { openGame } from './ui.js';
import { rejilla, tamCasilla } from './comun.js';

const D = /*DATOS*/{"n": 6, "solucion": {"4,4": 2, "4,3": 2, "2,1": 4, "1,1": 4, "2,0": 4, "2,2": 4, "0,4": 2, "0,3": 2, "3,2": 6, "3,1": 6, "3,0": 6, "4,2": 6, "3,3": 6, "4,1": 6, "3,4": 5, "2,4": 5, "1,4": 5, "1,5": 5, "2,3": 5, "0,5": 1, "0,0": 6, "0,1": 6, "0,2": 6, "1,0": 6, "1,2": 6, "1,3": 6, "5,3": 5, "5,2": 5, "5,1": 5, "5,4": 5, "5,0": 5, "5,5": 4, "4,5": 4, "3,5": 4, "2,5": 4, "4,0": 1}, "marca": "26"}/*FIN*/;
const COLORES = ['', '#7a3b8a', '#2f6aa8', '#2f8a5a', '#b8862a', '#b8502a', '#8a2a3a'];

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 40 — Los barracones',
    instr: 'Tocad una cama para cambiar su número (del 1 al 6, y vacía). Cada barracón de N camas: N casillas pegadas con el número N.',
    ...opts
  });
  const n = D.n;
  const v = Array.from({ length: n }, () => Array(n).fill(0));
  const { el, celdas } = rejilla(n, (f, c, b) => {
    b.addEventListener('click', () => { v[f][c] = (v[f][c] + 1) % 7; pintar(); });
  }, tamCasilla(n, 48));
  ui.body.append(el);

  function pintar() {
    for (let f = 0; f < n; f++) for (let c = 0; c < n; c++) {
      const b = celdas[f][c];
      b.textContent = v[f][c] ? String(v[f][c]) : '';
      b.dataset.v = v[f][c];
      b.style.background = v[f][c] ? COLORES[v[f][c]] : '';
    }
  }

  ui.button('Vaciar', 'ghost', () => { v.forEach(r => r.fill(0)); pintar(); ui.say('', ''); });
  ui.button('Repartir', 'primary', () => {
    if (v.some(r => r.includes(0))) { ui.say('Quedan camas sin número: todas las familias necesitan sitio.', ''); return; }
    let bien = true;
    for (let f = 0; f < n; f++) for (let c = 0; c < n; c++) if (v[f][c] !== D.solucion[f + ',' + c]) bien = false;
    if (bien) {
      ui.say('Las familias entran en orden, cada una en su barracón. Marca de los barracones: ' + D.marca + '. Coged la carta 30.', 'ok');
      celdas.flat().forEach(b => { b.disabled = true; });
    } else {
      ui.say('El intendente se rasca la calva: algún barracón no cumple las normas o no cuadra con su lista.', 'bad');
    }
  });
  pintar();
  return { close: ui.close };
}
