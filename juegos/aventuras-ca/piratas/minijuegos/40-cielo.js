// Carta 40 — La tapa del cofre: la tapa es un cielo de treinta y seis tachuelas numeradas (cartas 41 y 43, dos mitades); la Calavera de la carta celeste
// (carta 45) aparece una sola vez, girada y más pequeña. Hay que tocar los números de sus seis estrellas (instancias_piratas.py, CIELO).
// Distancia de las estrellas: D.distancia.
import { openGame } from './ui.js';
import { estilo, opcion } from './comun.js';

const D = /*DATOS*/{"estrellas": [[948, 670], [991, 446], [671, 440], [112, 172], [1049, 179], [338, 391], [1172, 387], [1064, 610], [527, 503], [848, 593], [314, 248], [808, 651], [479, 246], [240, 256], [898, 327], [102, 704], [406, 273], [259, 475], [572, 270], [817, 238], [458, 702], [270, 324], [493, 582], [54, 606], [417, 358], [1089, 344], [522, 374], [1065, 716], [1189, 252], [1017, 538], [139, 465], [1116, 552], [514, 162], [430, 453], [395, 664], [855, 753]], "solucion": [6, 11, 14, 17, 22, 25], "distancia": 2}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 40 — La tapa del cofre', instr: 'Tocad los números de las seis estrellas que forman la Calavera de la carta celeste (carta 45), que en el cielo de la tapa (cartas 41 y 43) aparece girada y más pequeña.', ...opts });
  estilo('pi-cie', '.cie-g{display:grid;grid-template-columns:repeat(6,1fr);gap:5px;max-width:340px;margin:8px auto}.cie-g button{min-height:42px;padding:0}');
  const sel = new Set();
  let resuelto = false;
  const g = document.createElement('div');
  g.className = 'cie-g';
  const bs = D.estrellas.map((_, i) => {
    const b = opcion(String(i + 1), () => {
      if (resuelto) return;
      if (sel.has(i + 1)) sel.delete(i + 1); else sel.add(i + 1);
      ui.say('');
      pintar();
    });
    b.dataset.n = String(i + 1);
    b.setAttribute('aria-label', 'Estrella ' + (i + 1));
    g.appendChild(b);
    return b;
  });
  const cuenta = document.createElement('div');
  cuenta.className = 'pi-pie';
  ui.body.append(g, cuenta);
  function pintar() {
    bs.forEach((b, i) => b.classList.toggle('sel', sel.has(i + 1)));
    cuenta.textContent = 'Estrellas elegidas: ' + sel.size;
  }
  ui.button('Abrir el cofre', 'primary', () => {
    if (resuelto) return;
    if (sel.size !== D.solucion.length) { ui.say('La Calavera tiene seis estrellas, ni una más ni una menos.', 'bad'); return; }
    if (!D.solucion.every(n => sel.has(n))) { ui.say('La tapa no cede: esas seis estrellas no forman la Calavera. Comparad la forma con la carta celeste (carta 45), girándola.', 'bad'); return; }
    resuelto = true;
    ui.say('Las seis tachuelas se hunden a la vez con un clic y la tapa se levanta sola. Distancia de las estrellas: ' + D.distancia + (D.distancia === 1 ? ' casilla' : ' casillas') + '. Coged la carta 30.', 'ok');
  });
  ui.button('Quitar todas', '', () => { if (!resuelto) { sel.clear(); ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
