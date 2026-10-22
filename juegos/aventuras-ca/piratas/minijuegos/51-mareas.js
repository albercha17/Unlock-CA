// Carta 51 — Las mareas: La Gaviota tiene que cruzar tres barras de arena, una al salir, otra dos horas después y otra cinco horas después de salir
// (carta 26). El agua sobre cada barra es la altura de la marea (tabla de las cartas 61 y 63, dos mitades) más el fondo propio de la barra.
// Hay que elegir la hora de salida (instancias_piratas.py, MAREAS, solución única).
import { openGame } from './ui.js';
import { estilo, opcion } from './comun.js';

const D = /*DATOS*/{"salida": 4, "alturas": [5, 8, 14, 22, 31, 37, 39, 37, 31, 23, 15, 8, 5, 6, 11, 19, 27, 35, 39, 38, 34, 27, 18, 11], "calado": 32, "barras": [{"fondo": 2, "tras": 0}, {"fondo": 5, "tras": 2}, {"fondo": 9, "tras": 5}]}/*FIN*/;
const NOMBRES = ['la Barra del Cangrejo', 'la Barra del Faro', 'la Barra Seca'];

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 51 — Las mareas', instr: 'Elegid la hora de salida de La Gaviota para que pase las tres barras con agua suficiente. El calado y las barras están en la carta 26 y la tabla de la marea, en las cartas 61 y 63.', ...opts });
  estilo('pi-mar', '.mar-g{display:grid;grid-template-columns:repeat(6,1fr);gap:5px;max-width:340px;margin:8px auto}.mar-g button{min-height:44px;padding:0}');
  let hora = null, resuelto = false;
  const g = document.createElement('div');
  g.className = 'mar-g';
  const bs = Array.from({ length: 24 - 5 }, (_, t) => {
    const b = opcion(String(t).padStart(2, '0') + ':00', () => { if (resuelto) return; hora = t; ui.say(''); pintar(); });
    b.dataset.h = String(t);
    g.appendChild(b);
    return b;
  });
  ui.body.appendChild(g);
  function pintar() { bs.forEach((b, t) => b.classList.toggle('sel', hora === t)); }
  ui.button('Zarpar', 'primary', () => {
    if (resuelto) return;
    if (hora === null) { ui.say('Elegid primero la hora de salida.', 'bad'); return; }
    for (let i = 0; i < D.barras.length; i++) {
      const b = D.barras[i];
      if (D.alturas[hora + b.tras] + b.fondo < D.calado) {
        ui.say('La Gaviota embarranca en ' + NOMBRES[i] + ': a esa hora no hay agua bastante. Probad otra hora de salida.', 'bad');
        return;
      }
    }
    if (hora !== D.salida) { ui.say('Cruza las tres barras, pero otra salida era posible y el pirata de guardia sospecha de vuestro cálculo.', 'bad'); return; }
    resuelto = true;
    ui.say('La Gaviota cruza las tres barras con el agua justa y llega a mar abierto. La capitana Bruma suspira de alivio. Coged la carta 58.', 'ok');
  });
  pintar();
  return { close: ui.close };
}
