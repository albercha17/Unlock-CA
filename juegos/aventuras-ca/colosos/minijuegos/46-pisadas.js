// Carta 46 — Las pisadas: Hitori 6 x 6. La app enseña los tejados sin número (los números están en los tejados del norte y del sur).
// Solución única (herramientas/instancias_colosos.py, pisadas).
import { openGame } from './ui.js';
import { rejilla, tamCasilla, tono } from './comun.js';

const D = /*DATOS*/{"n": 6, "solucion": [[0, 1], [0, 3], [2, 0], [2, 5], [3, 1], [3, 3], [4, 2], [4, 4], [5, 0]]}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 46 — Las pisadas',
    instr: 'Tocad los tejados que vais a pisar (cobertizos vacíos). Sin familias repetidas sin pisar en ninguna fila ni columna, sin dos pisadas juntas y sin partir la ciudad.',
    ...opts
  });
  const n = D.n;
  const pis = new Set();
  const { el, celdas } = rejilla(n, (f, c, b) => {
    b.classList.add('tejado');
    b.addEventListener('click', () => {
      const k = f + ',' + c;
      if (pis.has(k)) pis.delete(k); else { pis.add(k); tono(90, 0.25, 'sine', 0.2); }
      pintar();
    });
  }, tamCasilla(n, 48));
  ui.body.append(el);

  function pintar() {
    for (let f = 0; f < n; f++) for (let c = 0; c < n; c++) {
      const k = f + ',' + c;
      celdas[f][c].classList.toggle('pisada', pis.has(k));
      celdas[f][c].classList.toggle('tejado', !pis.has(k));
      celdas[f][c].textContent = pis.has(k) ? '👣' : '';
    }
  }
  function juntas() {
    return [...pis].some(k => { const [f, c] = k.split(',').map(Number); return pis.has((f + 1) + ',' + c) || pis.has(f + ',' + (c + 1)); });
  }
  function partida() {
    const libres = [];
    for (let f = 0; f < n; f++) for (let c = 0; c < n; c++) if (!pis.has(f + ',' + c)) libres.push(f + ',' + c);
    const vis = new Set([libres[0]]);
    const pila = [libres[0]];
    while (pila.length) {
      const [f, c] = pila.pop().split(',').map(Number);
      [[1, 0], [-1, 0], [0, 1], [0, -1]].forEach(([a, b]) => {
        const k = (f + a) + ',' + (c + b);
        if (f + a >= 0 && f + a < n && c + b >= 0 && c + b < n && !pis.has(k) && !vis.has(k)) { vis.add(k); pila.push(k); }
      });
    }
    return vis.size !== libres.length;
  }

  ui.button('Borrar pisadas', 'ghost', () => { pis.clear(); pintar(); ui.say('', ''); });
  ui.button('Cruzar la plaza', 'primary', () => {
    if (!pis.size) { ui.say('Si no pisáis nada, no llegáis a la puerta.', ''); return; }
    const sol = new Set(D.solucion.map(([f, c]) => f + ',' + c));
    if (pis.size === sol.size && [...pis].every(k => sol.has(k))) {
      ui.say('¡Cruzáis la plaza a zancadas sin aplastar ni una casa! Entre las tablas de un cobertizo asoma algo de hueso tallado. Coged la carta 56.', 'ok');
      celdas.flat().forEach(b => { b.disabled = true; });
    } else if (juntas()) {
      ui.say('¡Crac! Dos pisadas juntas y el suelo se hunde. Volved a pensarlo.', 'bad');
    } else if (partida()) {
      ui.say('Habéis dejado la ciudad partida: las familias no pueden ir de casa en casa.', 'bad');
    } else {
      ui.say('La doctora grita desde abajo: «¡Ahí vive gente!» o alguna familia sigue repetida. Mirad los números de los tejados.', 'bad');
    }
  });
  pintar();
  return { close: ui.close };
}
