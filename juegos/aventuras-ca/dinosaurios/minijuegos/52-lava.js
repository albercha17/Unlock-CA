// Carta 52 — La lava: poner UNA roca para que la lava, que baja siempre a la vecina más baja (carta 59), no llegue a los nidos.
// Las alturas solo están en las cartas 54 y 55; la app enseña la ladera sin números. Una sola casilla sirve (instancias_dinosaurios.py, LAVA).
import { openGame } from './ui.js';
import { estilo, rejilla, LETRAS } from './valle.js';

const D = /*DATOS*/{"n": 6, "alturas": [[207, 208, 189, 173, 231, 166], [202, 173, 166, 158, 157, 186], [154, 175, 129, 127, 180, 121], [142, 100, 103, 125, 89, 147], [102, 76, 70, 121, 87, 112], [56, 70, 40, 69, 74, 101]], "fuente": [1, 0], "nido": [2, 5], "camino": [[1, 0], [1, 1], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5]], "solucion": [2, 1]}/*FIN*/;
const V4 = [[0, -1], [1, 0], [0, 1], [-1, 0]];

function flujo(roca) {
  const n = D.n, alt = D.alturas;
  let [x, y] = D.fuente;
  const cam = [[x, y]];
  for (;;) {
    let mejor = null;
    for (const [dx, dy] of V4) {
      const a = x + dx, b = y + dy;
      if (a < 0 || b < 0 || a >= n || b >= n || (roca && roca[0] === a && roca[1] === b)) continue;
      if (!mejor || alt[b][a] < alt[mejor[1]][mejor[0]]) mejor = [a, b];
    }
    if (alt[mejor[1]][mejor[0]] >= alt[y][x]) return cam;
    [x, y] = mejor;
    cam.push([x, y]);
  }
}

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 52 — La lava', instr: 'El volcán va a escupir lava ladera abajo. Tocad la casilla donde Alberto empuja la roca (solo hay una) y pulsad «¡Que baje!».', ...opts });
  estilo('dn-lava', `
    .lav .dn-cel{background:#8a7a5a}
    .lav .dn-cel.fuente{background:#5a2a14}
    .lav .dn-cel.nido{background:radial-gradient(circle,#fff8e6 22%,#a87a3a 26%,#8a7a5a 55%)}
    .lav .dn-cel.roca{background:radial-gradient(circle,#9a9a92 40%,#4a4a44 70%)}
    .lav .dn-cel.lava{background:radial-gradient(circle,#ffd04a 20%,#e8501a 55%,#7a1a08)}`);
  let roca = null, resuelto = false, corriendo = false;
  const es = (c, p) => c && p && c[0] === p[0] && c[1] === p[1];
  const r = rejilla(D.n, (x, y) => {
    if (resuelto || corriendo || es([x, y], D.fuente) || es([x, y], D.nido)) return;
    roca = es(roca, [x, y]) ? null : [x, y];
    pintar([]);
    ui.say(roca ? 'La roca va en ' + LETRAS[x] + (y + 1) + '.' : '');
  }, true);
  r.el.classList.add('lav');
  ui.body.appendChild(r.el);
  function pintar(lava) {
    for (let y = 0; y < D.n; y++) for (let x = 0; x < D.n; x++) {
      const c = r.celda(x, y);
      c.className = 'dn-cel' + (es([x, y], D.fuente) ? ' fuente' : es([x, y], D.nido) ? ' nido' : '') + (es(roca, [x, y]) ? ' roca' : '');
      c.textContent = es([x, y], D.fuente) ? '🌋' : '';
    }
    lava.forEach(([x, y]) => r.celda(x, y).classList.add('lava'));
    r.el.dataset.roca = roca ? roca.join(',') : '';
  }
  ui.button('¡Que baje!', 'primary', () => {
    if (resuelto || corriendo) return;
    if (!roca) { ui.say('Primero colocad la roca.', 'bad'); return; }
    const cam = flujo(roca);
    const llega = cam.some(c => es(c, D.nido));
    corriendo = true;
    let i = 0;
    const paso = () => {
      pintar(cam.slice(0, ++i));
      if (i < cam.length) { setTimeout(paso, 120); return; }
      corriendo = false;
      if (!llega) {
        resuelto = true;
        ui.say('La lava choca con la roca, tuerce y se enfría lejos de los nidos. Las madres os miran agradecidas. Coged la carta 44.', 'ok');
      } else {
        ui.say('¡La lava llega a los nidos! Por suerte era solo el primer chorro. Alberto vuelve a por la roca: pensad dónde ponerla (cartas 54, 55 y 59).', 'bad');
        setTimeout(() => { if (!resuelto) { roca = null; pintar([]); } }, 900);
      }
    };
    paso();
  });
  pintar([]);
  return { close: ui.close };
}
