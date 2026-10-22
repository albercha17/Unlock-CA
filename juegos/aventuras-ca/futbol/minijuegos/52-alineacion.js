// Carta 52 — El once del míster: cinco jugadores, cinco puestos y una nota de cada jugador en cada puesto (cartas 54 y 55). Hay que colocar a cada uno en un
// puesto distinto de modo que la suma de las notas sea la más alta posible; la regla, en la carta 59 (instancias_futbol.py, ALINEACION). Aro de la
// camiseta: D.aro.
import { openGame } from './ui.js';
import { estilo, opcion } from './comun.js';

const D = /*DATOS*/{"jugadores": ["Toni", "Beto", "Rafa", "Luis", "Nico"], "puestos": ["Portero", "Defensa", "Lateral", "Medio", "Delantero"], "notas": [[3, 9, 6, 2, 2], [4, 9, 7, 7, 2], [6, 9, 5, 8, 3], [5, 6, 3, 8, 7], [3, 7, 8, 6, 9]], "maximo": 39, "aro": 4}/*FIN*/;
const CORTO = ['POR', 'DEF', 'LAT', 'MED', 'DEL'];

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 52 — El once del míster', instr: 'Poned a cada jugador en un puesto distinto. Las notas están en las cartas 54 y 55; la regla, en la 59.', ...opts });
  estilo('fu-ali', '.ali-f{max-width:340px;margin:6px auto}.ali-f b{color:#f2c230;display:block;margin-bottom:4px;font:800 .9rem system-ui,Arial,sans-serif}.ali-f .fu-btns{margin:2px 0;gap:4px}.ali-f .fu-opc{min-width:52px;padding:0 6px}');
  const eleccion = D.jugadores.map(() => -1);
  let resuelto = false;
  const filas = D.jugadores.map((nombre, i) => {
    const f = document.createElement('div');
    f.className = 'ali-f';
    f.dataset.i = String(i);
    const t = document.createElement('b');
    t.textContent = nombre;
    const fila = document.createElement('div');
    fila.className = 'fu-btns';
    const bs = D.puestos.map((_, p) => {
      const b = opcion(CORTO[p], () => { if (resuelto) return; eleccion[i] = p; ui.say(''); pintar(); });
      b.dataset.i = String(i);
      b.dataset.p = String(p);
      b.setAttribute('aria-label', nombre + ' de ' + D.puestos[p]);
      fila.appendChild(b);
      return b;
    });
    f.append(t, fila);
    ui.body.appendChild(f);
    return bs;
  });
  function pintar() { filas.forEach((bs, i) => bs.forEach((b, p) => b.classList.toggle('sel', eleccion[i] === p))); }
  ui.button('Presentar el once', 'primary', () => {
    if (resuelto) return;
    if (eleccion.some(e => e < 0)) { ui.say('Falta poner a algún jugador.', 'bad'); return; }
    if (new Set(eleccion).size < eleccion.length) { ui.say('Hay dos jugadores en el mismo puesto y un puesto vacío.', 'bad'); return; }
    const suma = eleccion.reduce((a, p, i) => a + D.notas[i][p], 0);
    if (suma !== D.maximo) { ui.say('Suman ' + suma + ' puntos, pero el míster está seguro de que hay un once que suma más.', 'bad'); return; }
    resuelto = true;
    ui.say('Suman ' + suma + ' puntos: es el once perfecto. Aro de la camiseta: ' + D.aro + '. Coged la carta 44.', 'ok');
  });
  ui.button('Borrar todo', 'ghost', () => { if (!resuelto) { eleccion.fill(-1); ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
