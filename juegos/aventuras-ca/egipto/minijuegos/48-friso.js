// Carta 48 — El friso de los animales: el guardián solo deja pasar si le contáis cuántos animales de cada clase miran hacia donde nace el sol
// (a la derecha). El friso son las cartas 42 y 49 (dos mitades); la cerradura del guardián, la carta 53. Solución: 4, 6, 3 y 5.
import { openGame } from './ui.js';
import { guardarSello, contador, figuraSVG } from './nilo.js';

const D = /*DATOS*/{"animales": ["ibis", "cobra", "chacal", "halcon"], "solucion": [4, 6, 3, 5], "figuras": {"ibis": [{"t": "p", "p": [[64.0, 56.0], [63.4, 59.8], [61.6, 63.4], [58.8, 66.6], [55.0, 69.3], [50.4, 71.3], [45.3, 72.6], [40.0, 73.0], [34.7, 72.6], [29.6, 71.3], [25.0, 69.3], [21.2, 66.6], [18.4, 63.4], [16.6, 59.8], [16.0, 56.0], [16.6, 52.2], [18.4, 48.6], [21.2, 45.4], [25.0, 42.7], [29.6, 40.7], [34.7, 39.4], [40.0, 39.0], [45.3, 39.4], [50.4, 40.7], [55.0, 42.7], [58.8, 45.4], [61.6, 48.6], [63.4, 52.2]]}, {"t": "l", "p": [[56, 50], [66, 28], [70, 22]], "w": 7}, {"t": "c", "c": [72, 20], "r": 8}, {"t": "l", "p": [[78, 20], [96, 28], [92, 34]], "w": 4}, {"t": "l", "p": [[38, 72], [36, 92]], "w": 4}, {"t": "l", "p": [[46, 72], [48, 92]], "w": 4}, {"t": "l", "p": [[18, 54], [4, 64]], "w": 7}], "cobra": [{"t": "p", "p": [[18, 94], [30, 70], [46, 78], [58, 56], [48, 34], [54, 16], [66, 16], [72, 34], [66, 58], [78, 80], [92, 94]]}, {"t": "p", "p": [[36, 16], [54, 16], [48, 4]]}, {"t": "c", "c": [62, 10], "r": 7}, {"t": "l", "p": [[66, 10], [78, 12]], "w": 3}], "chacal": [{"t": "p", "p": [[62.0, 58.0], [61.3, 61.1], [59.4, 64.1], [56.3, 66.7], [52.2, 68.9], [47.3, 70.6], [41.8, 71.6], [36.0, 72.0], [30.2, 71.6], [24.7, 70.6], [19.8, 68.9], [15.7, 66.7], [12.6, 64.1], [10.7, 61.1], [10.0, 58.0], [10.7, 54.9], [12.6, 51.9], [15.7, 49.3], [19.8, 47.1], [24.7, 45.4], [30.2, 44.4], [36.0, 44.0], [41.8, 44.4], [47.3, 45.4], [52.2, 47.1], [56.3, 49.3], [59.4, 51.9], [61.3, 54.9]]}, {"t": "l", "p": [[18, 66], [14, 92]], "w": 6}, {"t": "l", "p": [[30, 68], [30, 92]], "w": 6}, {"t": "l", "p": [[46, 68], [48, 92]], "w": 6}, {"t": "l", "p": [[58, 62], [64, 92]], "w": 6}, {"t": "p", "p": [[56, 50], [66, 30], [88, 40], [96, 46], [90, 52], [70, 54]]}, {"t": "p", "p": [[62, 32], [64, 4], [74, 30]]}, {"t": "p", "p": [[74, 32], [80, 8], [84, 36]]}, {"t": "l", "p": [[10, 56], [2, 40]], "w": 5}], "halcon": [{"t": "p", "p": [[68.0, 62.0], [67.4, 67.8], [65.8, 73.3], [63.2, 78.2], [59.7, 82.3], [55.5, 85.4], [50.9, 87.3], [46.0, 88.0], [41.1, 87.3], [36.5, 85.4], [32.3, 82.3], [28.8, 78.2], [26.2, 73.3], [24.6, 67.8], [24.0, 62.0], [24.6, 56.2], [26.2, 50.7], [28.8, 45.8], [32.3, 41.7], [36.5, 38.6], [41.1, 36.7], [46.0, 36.0], [50.9, 36.7], [55.5, 38.6], [59.7, 41.7], [63.2, 45.8], [65.8, 50.7], [67.4, 56.2]]}, {"t": "c", "c": [58, 28], "r": 12}, {"t": "p", "p": [[66, 26], [86, 32], [66, 40]]}, {"t": "p", "p": [[34, 50], [10, 28], [8, 62], [30, 76]]}, {"t": "l", "p": [[40, 86], [40, 98]], "w": 5}, {"t": "l", "p": [[52, 86], [54, 98]], "w": 5}]}}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 48 — El friso de los animales', instr: 'Decidle al guardián cuántos animales de cada clase hay mirando hacia el sol naciente. Pone un número por cada animal de su cerradura.', ...opts });
  const cs = D.animales.map(a => {
    const c = contador('', 20, () => ui.say(''), a, figuraSVG(D.figuras[a], '#f6e7bf', '#4d3c20', 46));
    ui.body.appendChild(c.el);
    return c;
  });
  let resuelto = false;
  ui.button('Responder', 'primary', () => {
    if (resuelto) return;
    const v = cs.map(c => c.valor());
    const ok = v.map((x, i) => x === D.solucion[i]).filter(Boolean).length;
    if (ok === D.animales.length) {
      resuelto = true; guardarSello('48');
      ui.say('El guardián de piedra asiente despacio y se aparta de la puerta. Coged la carta 36.', 'ok');
    } else ui.say('El guardián niega con la cabeza: ' + (ok === 0 ? 'ninguna cuenta es correcta' : 'alguna cuenta es correcta, pero no todas') + '. Mirad bien hacia dónde miran (cartas 42, 49 y 53).', 'bad');
  });
  return { close: ui.close };
}
