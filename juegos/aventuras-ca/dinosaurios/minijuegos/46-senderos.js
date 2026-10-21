// Carta 46 — La ruta de la manada: seguir a los edmontosaurios desde la Roca Alta por TODOS los senderos del valle, sin repetir ninguno
// (camino de Euler; la costumbre, en la carta 33). Los senderos solo están en el mapa (cartas 37 y 39): la app enseña los claros sueltos
// y dibuja solo los senderos ya recorridos. Vale cualquier recorrido correcto (instancias_dinosaurios.py, SENDEROS).
import { openGame } from './ui.js';
import { estilo } from './valle.js';

const D = /*DATOS*/{"claros": {"N": "Nidos", "H": "Helechal", "L": "Lago", "C": "Cascada", "V": "Volcán", "P": "Pinar", "R": "Roca Alta"}, "senderos": [["N", "H"], ["N", "L"], ["H", "L"], ["H", "C"], ["L", "C"], ["L", "V"], ["C", "P"], ["V", "P"], ["P", "R"], ["C", "R"], ["V", "R"], ["H", "V"]], "impares": ["P", "R"]}/*FIN*/;
const POS = { N: [12, 30], H: [32, 18], L: [30, 62], C: [55, 40], V: [55, 82], P: [80, 62], R: [86, 22] };

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 46 — La ruta de la manada', instr: 'Tocad los claros en el orden en que los pisa la manada, desde la Roca Alta. Si os equivocáis de sendero, la manada se dispersa y hay que volver a empezar.', ...opts });
  estilo('dn-sende', `
    .sen-mapa{position:relative;width:min(88vw,330px);aspect-ratio:1.1;margin:6px auto;border-radius:10px;background:#5f7a3e}
    .sen-mapa svg{position:absolute;inset:0;width:100%;height:100%}
    .sen-claro{position:absolute;width:56px;height:40px;margin:-20px -28px;border-radius:50%;border:3px solid #f2ffd6;background:#2f4a1e;color:#f2ffd6;font:700 .55rem system-ui;cursor:pointer;padding:0}
    .sen-claro.aqui{background:#b5e35b;color:#1a2a0c}`);
  const mapa = document.createElement('div'); mapa.className = 'sen-mapa';
  ui.body.appendChild(mapa);
  const pie = document.createElement('p'); pie.className = 'dn-pie'; ui.body.appendChild(pie);
  const sendero = (a, b) => D.senderos.findIndex(([x, y]) => (x === a && y === b) || (x === b && y === a));
  let ruta = ['R'], usados = new Set(), resuelto = false;
  function pintar() {
    const lin = ruta.slice(1).map((n, i) => { const a = POS[ruta[i]], b = POS[n]; return '<line x1="' + a[0] + '" y1="' + a[1] / 1.1 + '" x2="' + b[0] + '" y2="' + b[1] / 1.1 + '" stroke="#e8d8a8" stroke-width="2.4" stroke-linecap="round"/>'; }).join('');
    mapa.innerHTML = '<svg viewBox="0 0 100 91" aria-hidden="true">' + lin + '</svg>';
    Object.keys(POS).forEach(k => {
      const b = document.createElement('button'); b.type = 'button'; b.className = 'sen-claro' + (k === ruta[ruta.length - 1] ? ' aqui' : ''); b.dataset.k = k;
      b.textContent = D.claros[k]; b.style.left = POS[k][0] + '%'; b.style.top = POS[k][1] + '%';
      b.addEventListener('click', () => pisar(k));
      mapa.appendChild(b);
    });
    mapa.dataset.ruta = ruta.join('');
    pie.textContent = 'Senderos recorridos: ' + usados.size + ' de ' + D.senderos.length;
  }
  function pisar(k) {
    if (resuelto) return;
    const desde = ruta[ruta.length - 1];
    const i = sendero(desde, k);
    if (i < 0) { ui.say('No hay ningún sendero directo de ' + D.claros[desde] + ' a ' + D.claros[k] + ' (mapa, cartas 37 y 39).', 'bad'); return; }
    if (usados.has(i)) { ui.say('La manada nunca pisa dos veces el mismo sendero (carta 33). Se dispersa y vuelve a la Roca Alta.', 'bad'); ruta = ['R']; usados = new Set(); pintar(); return; }
    usados.add(i); ruta.push(k); ui.say(''); pintar();
    if (usados.size === D.senderos.length) {
      resuelto = true;
      ui.say('¡La manada llega a su dormidero en ' + D.claros[k] + '! Junto a los huesos de un viejo edmontosaurio brilla una batería de la doctora. Coged la carta 56.', 'ok');
      return;
    }
    const quedan = D.senderos.some(([a, b], j) => !usados.has(j) && (a === k || b === k));
    if (!quedan) { ui.say('Desde ' + D.claros[k] + ' ya no quedan senderos sin pisar, y faltan otros: la manada se dispersa. Volved a empezar.', 'bad'); ruta = ['R']; usados = new Set(); pintar(); }
  }
  ui.button('Volver a la Roca Alta', '', () => { if (!resuelto) { ruta = ['R']; usados = new Set(); ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
