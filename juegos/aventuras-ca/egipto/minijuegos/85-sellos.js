// Carta 85 — La consola del Cronoportal (metapuzle): cada puzle resuelto dejó un sello con su signo (pan, tierra, agua, ibis, ojo, pluma, loto,
// cetro, escarabajo y corona). Para despertar al aparato hay que tocar cinco sellos en el orden de los acertijos de las cartas 86 y 87.
// Orden: agua, tierra, pan, ojo, escarabajo (instancias_egipto.py, SELLOS y ORDEN_SELLOS).
import { openGame } from './ui.js';
import { estilo, figuraSVG, sellosGuardados } from './nilo.js';

const D = /*DATOS*/{"sellos": {"14": "pan", "20": "tierra", "40": "agua", "48": "ibis", "52": "ojo", "46": "pluma", "51": "loto", "69": "cetro", "64": "escarabajo", "72": "corona"}, "orden": ["40", "20", "14", "52", "64"], "figuras": {"anj": [{"t": "c", "c": [50, 30], "r": 20, "w": 9}, {"t": "l", "p": [[50, 50], [50, 94]], "w": 10}, {"t": "l", "p": [[26, 66], [74, 66]], "w": 10}], "ojo": [{"t": "p", "p": [[8, 50], [26, 34], [50, 28], [74, 34], [92, 50], [74, 62], [50, 68], [26, 62]]}, {"t": "c", "c": [50, 48], "r": 11, "f": "fondo"}, {"t": "l", "p": [[50, 68], [42, 90], [60, 90]], "w": 7}], "escarabajo": [{"t": "p", "p": [[76.0, 56.0], [75.3, 63.1], [73.4, 69.9], [70.3, 76.0], [66.2, 81.0], [61.3, 84.8], [55.8, 87.2], [50.0, 88.0], [44.2, 87.2], [38.7, 84.8], [33.8, 81.0], [29.7, 76.0], [26.6, 69.9], [24.7, 63.1], [24.0, 56.0], [24.7, 48.9], [26.6, 42.1], [29.7, 36.0], [33.8, 31.0], [38.7, 27.2], [44.2, 24.8], [50.0, 24.0], [55.8, 24.8], [61.3, 27.2], [66.2, 31.0], [70.3, 36.0], [73.4, 42.1], [75.3, 48.9]]}, {"t": "c", "c": [50, 20], "r": 12}, {"t": "l", "p": [[50, 30], [50, 86]], "w": 4, "f": "fondo"}, {"t": "l", "p": [[28, 44], [10, 36]], "w": 6}, {"t": "l", "p": [[24, 62], [8, 64]], "w": 6}, {"t": "l", "p": [[28, 80], [12, 92]], "w": 6}, {"t": "l", "p": [[72, 44], [90, 36]], "w": 6}, {"t": "l", "p": [[76, 62], [92, 64]], "w": 6}, {"t": "l", "p": [[72, 80], [88, 92]], "w": 6}], "ibis": [{"t": "p", "p": [[64.0, 56.0], [63.4, 59.8], [61.6, 63.4], [58.8, 66.6], [55.0, 69.3], [50.4, 71.3], [45.3, 72.6], [40.0, 73.0], [34.7, 72.6], [29.6, 71.3], [25.0, 69.3], [21.2, 66.6], [18.4, 63.4], [16.6, 59.8], [16.0, 56.0], [16.6, 52.2], [18.4, 48.6], [21.2, 45.4], [25.0, 42.7], [29.6, 40.7], [34.7, 39.4], [40.0, 39.0], [45.3, 39.4], [50.4, 40.7], [55.0, 42.7], [58.8, 45.4], [61.6, 48.6], [63.4, 52.2]]}, {"t": "l", "p": [[56, 50], [66, 28], [70, 22]], "w": 7}, {"t": "c", "c": [72, 20], "r": 8}, {"t": "l", "p": [[78, 20], [96, 28], [92, 34]], "w": 4}, {"t": "l", "p": [[38, 72], [36, 92]], "w": 4}, {"t": "l", "p": [[46, 72], [48, 92]], "w": 4}, {"t": "l", "p": [[18, 54], [4, 64]], "w": 7}], "cobra": [{"t": "p", "p": [[18, 94], [30, 70], [46, 78], [58, 56], [48, 34], [54, 16], [66, 16], [72, 34], [66, 58], [78, 80], [92, 94]]}, {"t": "p", "p": [[36, 16], [54, 16], [48, 4]]}, {"t": "c", "c": [62, 10], "r": 7}, {"t": "l", "p": [[66, 10], [78, 12]], "w": 3}], "chacal": [{"t": "p", "p": [[62.0, 58.0], [61.3, 61.1], [59.4, 64.1], [56.3, 66.7], [52.2, 68.9], [47.3, 70.6], [41.8, 71.6], [36.0, 72.0], [30.2, 71.6], [24.7, 70.6], [19.8, 68.9], [15.7, 66.7], [12.6, 64.1], [10.7, 61.1], [10.0, 58.0], [10.7, 54.9], [12.6, 51.9], [15.7, 49.3], [19.8, 47.1], [24.7, 45.4], [30.2, 44.4], [36.0, 44.0], [41.8, 44.4], [47.3, 45.4], [52.2, 47.1], [56.3, 49.3], [59.4, 51.9], [61.3, 54.9]]}, {"t": "l", "p": [[18, 66], [14, 92]], "w": 6}, {"t": "l", "p": [[30, 68], [30, 92]], "w": 6}, {"t": "l", "p": [[46, 68], [48, 92]], "w": 6}, {"t": "l", "p": [[58, 62], [64, 92]], "w": 6}, {"t": "p", "p": [[56, 50], [66, 30], [88, 40], [96, 46], [90, 52], [70, 54]]}, {"t": "p", "p": [[62, 32], [64, 4], [74, 30]]}, {"t": "p", "p": [[74, 32], [80, 8], [84, 36]]}, {"t": "l", "p": [[10, 56], [2, 40]], "w": 5}], "halcon": [{"t": "p", "p": [[68.0, 62.0], [67.4, 67.8], [65.8, 73.3], [63.2, 78.2], [59.7, 82.3], [55.5, 85.4], [50.9, 87.3], [46.0, 88.0], [41.1, 87.3], [36.5, 85.4], [32.3, 82.3], [28.8, 78.2], [26.2, 73.3], [24.6, 67.8], [24.0, 62.0], [24.6, 56.2], [26.2, 50.7], [28.8, 45.8], [32.3, 41.7], [36.5, 38.6], [41.1, 36.7], [46.0, 36.0], [50.9, 36.7], [55.5, 38.6], [59.7, 41.7], [63.2, 45.8], [65.8, 50.7], [67.4, 56.2]]}, {"t": "c", "c": [58, 28], "r": 12}, {"t": "p", "p": [[66, 26], [86, 32], [66, 40]]}, {"t": "p", "p": [[34, 50], [10, 28], [8, 62], [30, 76]]}, {"t": "l", "p": [[40, 86], [40, 98]], "w": 5}, {"t": "l", "p": [[52, 86], [54, 98]], "w": 5}], "sol": [{"t": "c", "c": [50, 50], "r": 30, "w": 8}, {"t": "c", "c": [50, 50], "r": 7}], "loto": [{"t": "p", "p": [[50, 14], [62, 52], [50, 74], [38, 52]]}, {"t": "p", "p": [[30, 30], [46, 54], [40, 74], [20, 56]]}, {"t": "p", "p": [[70, 30], [54, 54], [60, 74], [80, 56]]}, {"t": "l", "p": [[50, 74], [50, 96]], "w": 6}], "agua": [{"t": "l", "p": [[8, 30], [26, 20], [44, 30], [62, 20], [80, 30], [94, 22]], "w": 7}, {"t": "l", "p": [[8, 56], [26, 46], [44, 56], [62, 46], [80, 56], [94, 48]], "w": 7}, {"t": "l", "p": [[8, 82], [26, 72], [44, 82], [62, 72], [80, 82], [94, 74]], "w": 7}], "pluma": [{"t": "p", "p": [[65.0, 44.0], [64.6, 52.5], [63.5, 60.5], [61.7, 67.7], [59.4, 73.7], [56.5, 78.2], [53.3, 81.0], [50.0, 82.0], [46.7, 81.0], [43.5, 78.2], [40.6, 73.7], [38.3, 67.7], [36.5, 60.5], [35.4, 52.5], [35.0, 44.0], [35.4, 35.5], [36.5, 27.5], [38.3, 20.3], [40.6, 14.3], [43.5, 9.8], [46.7, 7.0], [50.0, 6.0], [53.3, 7.0], [56.5, 9.8], [59.4, 14.3], [61.7, 20.3], [63.5, 27.5], [64.6, 35.5]]}, {"t": "l", "p": [[50, 10], [50, 96]], "w": 5, "f": "fondo"}], "corona": [{"t": "p", "p": [[30, 90], [38, 30], [50, 6], [62, 30], [70, 90]]}, {"t": "c", "c": [50, 50], "r": 8, "f": "fondo"}], "cetro": [{"t": "l", "p": [[50, 94], [50, 20]], "w": 9}, {"t": "p", "p": [[34, 8], [66, 8], [58, 28], [42, 28]]}], "pan": [{"t": "p", "p": [[88.0, 62.0], [87.0, 66.9], [84.2, 71.5], [79.7, 75.7], [73.7, 79.2], [66.5, 81.8], [58.5, 83.4], [50.0, 84.0], [41.5, 83.4], [33.5, 81.8], [26.3, 79.2], [20.3, 75.7], [15.8, 71.5], [13.0, 66.9], [12.0, 62.0], [13.0, 57.1], [15.8, 52.5], [20.3, 48.3], [26.3, 44.8], [33.5, 42.2], [41.5, 40.6], [50.0, 40.0], [58.5, 40.6], [66.5, 42.2], [73.7, 44.8], [79.7, 48.3], [84.2, 52.5], [87.0, 57.1]]}, {"t": "l", "p": [[24, 56], [76, 56]], "w": 4, "f": "fondo"}], "tierra": [{"t": "p", "p": [[10, 70], [30, 30], [50, 62], [70, 24], [92, 70]]}]}}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 85 — La consola del Cronoportal', instr: 'Los sellos de los puzles resueltos están en el aparato. Tocad cinco, en el orden de los acertijos (cartas 86 y 87). Tocad un hueco para devolver un sello.', ...opts });
  estilo('eg-sel', `.sel-huecos{display:flex;gap:6px;justify-content:center;margin:8px 0}.sel-hueco{width:52px;height:52px;border-radius:10px;border:2px dashed #d9a441;background:rgba(0,0,0,.25);cursor:pointer;display:flex;align-items:center;justify-content:center;padding:0}.sel-sellos{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;max-width:340px;margin:10px auto}.sel-s{aspect-ratio:1;border-radius:50%;border:3px solid #d9a441;background:#4d3c20;cursor:pointer;display:flex;align-items:center;justify-content:center;padding:0}.sel-s.falta{opacity:.3;border-style:dashed}.sel-s.usado{opacity:.4}`);
  const huecos = document.createElement('div'); huecos.className = 'sel-huecos';
  const sellos = document.createElement('div'); sellos.className = 'sel-sellos';
  ui.body.append(huecos, sellos);
  const tengo = new Set(sellosGuardados());
  let orden = [], resuelto = false;
  const n = D.orden.length;
  function pintar() {
    huecos.innerHTML = '';
    for (let i = 0; i < n; i++) {
      const h = document.createElement('button'); h.type = 'button'; h.className = 'sel-hueco'; h.dataset.i = String(i);
      if (orden[i]) h.appendChild(figuraSVG(D.figuras[D.sellos[orden[i]]], '#f6e7bf', '#4d3c20', 36));
      h.addEventListener('click', () => { if (!resuelto && orden[i]) { orden.splice(i, 1); ui.say(''); pintar(); } });
      huecos.appendChild(h);
    }
    sellos.querySelectorAll('.sel-s').forEach(b => b.classList.toggle('usado', orden.includes(b.dataset.c)));
    huecos.dataset.orden = orden.join(',');
  }
  Object.keys(D.sellos).forEach(c => {
    const b = document.createElement('button'); b.type = 'button'; b.className = 'sel-s' + (tengo.has(c) ? '' : ' falta'); b.dataset.c = c;
    b.setAttribute('aria-label', 'Sello del puzle ' + c);
    b.appendChild(figuraSVG(D.figuras[D.sellos[c]], '#f6e7bf', '#4d3c20', 38));
    b.addEventListener('click', () => {
      if (resuelto || orden.includes(c) || orden.length >= n) return;
      if (!tengo.has(c)) { ui.say('Ese sello todavía no está en el aparato: resolved antes el puzle de la carta ' + c + '.', 'bad'); return; }
      orden.push(c); ui.say(''); pintar();
    });
    sellos.appendChild(b);
  });
  ui.button('Despertar al Cronoportal', 'primary', () => {
    if (resuelto) return;
    if (orden.length < n) { ui.say('Faltan sellos: son ' + n + '.', 'bad'); return; }
    if (orden.every((c, i) => c === D.orden[i])) {
      resuelto = true;
      ui.say('Los cinco sellos brillan uno tras otro y el Cronoportal despierta con un zumbido grave. Coged la carta 99.', 'ok');
    } else ui.say('El aparato se estremece pero no despierta: ese no es el orden de los acertijos (cartas 86 y 87).', 'bad');
  });
  ui.button('Quitar todos', 'ghost', () => { if (!resuelto) { orden = []; ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
