// Carta 46 — La suma del escriba: seis signos esconden cifras distintas de una suma (carta 37). Dos notas del escriba (cartas 39 y 33)
// dejan una sola solución. La primera cifra de cada número no es cero. Solución en instancias_egipto.py (CRIPTO).
import { openGame } from './ui.js';
import { guardarSello, contador, figuraSVG } from './nilo.js';

const D = /*DATOS*/{"suma": ["CDC", "EAA", "CBBF"], "signos": {"A": "sol", "B": "loto", "C": "agua", "D": "pluma", "E": "corona", "F": "cetro"}, "solucion": {"A": 4, "B": 0, "C": 1, "D": 6, "E": 8, "F": 5}, "figuras": {"sol": [{"t": "c", "c": [50, 50], "r": 30, "w": 8}, {"t": "c", "c": [50, 50], "r": 7}], "loto": [{"t": "p", "p": [[50, 14], [62, 52], [50, 74], [38, 52]]}, {"t": "p", "p": [[30, 30], [46, 54], [40, 74], [20, 56]]}, {"t": "p", "p": [[70, 30], [54, 54], [60, 74], [80, 56]]}, {"t": "l", "p": [[50, 74], [50, 96]], "w": 6}], "agua": [{"t": "l", "p": [[8, 30], [26, 20], [44, 30], [62, 20], [80, 30], [94, 22]], "w": 7}, {"t": "l", "p": [[8, 56], [26, 46], [44, 56], [62, 46], [80, 56], [94, 48]], "w": 7}, {"t": "l", "p": [[8, 82], [26, 72], [44, 82], [62, 72], [80, 82], [94, 74]], "w": 7}], "pluma": [{"t": "p", "p": [[65.0, 44.0], [64.6, 52.5], [63.5, 60.5], [61.7, 67.7], [59.4, 73.7], [56.5, 78.2], [53.3, 81.0], [50.0, 82.0], [46.7, 81.0], [43.5, 78.2], [40.6, 73.7], [38.3, 67.7], [36.5, 60.5], [35.4, 52.5], [35.0, 44.0], [35.4, 35.5], [36.5, 27.5], [38.3, 20.3], [40.6, 14.3], [43.5, 9.8], [46.7, 7.0], [50.0, 6.0], [53.3, 7.0], [56.5, 9.8], [59.4, 14.3], [61.7, 20.3], [63.5, 27.5], [64.6, 35.5]]}, {"t": "l", "p": [[50, 10], [50, 96]], "w": 5, "f": "fondo"}], "corona": [{"t": "p", "p": [[30, 90], [38, 30], [50, 6], [62, 30], [70, 90]]}, {"t": "c", "c": [50, 50], "r": 8, "f": "fondo"}], "cetro": [{"t": "l", "p": [[50, 94], [50, 20]], "w": 9}, {"t": "p", "p": [[34, 8], [66, 8], [58, 28], [42, 28]]}]}}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 46 — La suma del escriba', instr: 'Poned una cifra (de 0 a 9) a cada signo, sin repetir ninguna, para que la suma de la carta 37 sea cierta y cumpla las notas del escriba (cartas 39 y 33).', ...opts });
  const letras = Object.keys(D.signos);
  const cs = {};
  letras.forEach(l => {
    const c = contador('', 9, () => ui.say(''), l, figuraSVG(D.figuras[D.signos[l]], '#f6e7bf', '#4d3c20', 44));
    cs[l] = c; ui.body.appendChild(c.el);
  });
  let resuelto = false;
  const num = p => Number([...p].map(ch => cs[ch].valor()).join(''));
  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    const v = letras.map(l => cs[l].valor());
    if (new Set(v).size < v.length) { ui.say('Cada signo es una cifra distinta: hay cifras repetidas.', 'bad'); return; }
    if (D.suma.some(p => cs[p[0]].valor() === 0)) { ui.say('El primer signo de un número no puede ser el cero.', 'bad'); return; }
    if (num(D.suma[0]) + num(D.suma[1]) !== num(D.suma[2])) { ui.say('Con esas cifras la suma no es cierta (carta 37).', 'bad'); return; }
    if (letras.every(l => cs[l].valor() === D.solucion[l])) {
      resuelto = true; guardarSello('46');
      ui.say('La suma es cierta y cumple lo que anotó el escriba: la tapa del cofre se abre con un clic. Coged la carta 56.', 'ok');
    } else ui.say('La suma es cierta, pero no cumple lo que anotó el escriba en los márgenes (cartas 39 y 33).', 'bad');
  });
  return { close: ui.close };
}
