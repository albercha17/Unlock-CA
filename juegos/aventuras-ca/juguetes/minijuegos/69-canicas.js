// Carta 69 — La pista de canicas: colocar los tres balancines para que la tercera canica (el cristal) caiga en el tarro. Cada balancín
// manda la canica al lado al que apunta y cambia de lado cuando ella pasa (instrucciones, carta 70). Una sola posición válida (instancias_juguetes.py).
import { openGame } from './ui.js';

const P = /*DATOS*/{"tarro": "C", "solucion": {"b1": "der", "b2": "der", "b3": "der"}, "canicas": 3}/*FIN*/;
const SALIDA = { 'b2,izq': 'A', 'b2,der': 'B', 'b3,izq': 'C', 'b3,der': 'D' };
const XY = { entrada: [150, 14], b1: [150, 70], b2: [90, 140], b3: [210, 140], A: [60, 214], B: [120, 214], C: [180, 214], D: [240, 214] };

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 69 — La pista de canicas',
    instr: 'Toca los balancines para colocarlos y suelta las canicas. Caen de una en una y cada balancín cambia de lado al pasar una. El cristal es la tercera: tiene que caer en el tarro.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .jug-pista{position:relative;width:min(88vw,320px);aspect-ratio:300 / 240;margin:4px auto 8px;border-radius:10px;background:#e8d2a0;border:5px solid #8a5c30}
    .jug-pista svg{position:absolute;inset:0;width:100%;height:100%}
    .jug-bal{position:absolute;width:15%;aspect-ratio:1;margin:-7.5% 0 0 -7.5%;border-radius:50%;border:3px solid #6a4022;background:#fff4dc;padding:0;cursor:pointer}
    .jug-bal i{position:absolute;left:50%;top:50%;width:12%;height:62%;margin-left:-6%;background:#ee8028;border:2px solid #3a2010;border-radius:3px;transform-origin:50% 0;transition:transform .25s}
    .jug-bal[data-lado=izq] i{transform:rotate(40deg)}
    .jug-bal[data-lado=der] i{transform:rotate(-40deg)}
    .jug-bal b{position:absolute;right:-14px;top:-10px;font:700 .8rem system-ui;color:#3a2010}
    .jug-canica{position:absolute;width:5%;aspect-ratio:1;margin:-2.5% 0 0 -2.5%;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff,#6ab0ff 40%,#2050a0);transition:left .32s linear,top .32s linear}
    .jug-canica.cristal{background:radial-gradient(circle at 35% 30%,#fff,#ff6a6a 40%,#a01020);box-shadow:0 0 8px #ff4040}
  `;
  ui.body.appendChild(style);

  const pista = document.createElement('div');
  pista.className = 'jug-pista';
  const pct = ([x, y]) => [x / 300 * 100, y / 240 * 100];
  const lin = (a, b) => '<line x1="' + XY[a][0] + '" y1="' + XY[a][1] + '" x2="' + XY[b][0] + '" y2="' + XY[b][1] + '" stroke="#b49064" stroke-width="9" stroke-linecap="round"/>';
  pista.innerHTML = '<svg viewBox="0 0 300 240" aria-hidden="true">' + [['entrada', 'b1'], ['b1', 'b2'], ['b1', 'b3'], ['b2', 'A'], ['b2', 'B'], ['b3', 'C'], ['b3', 'D']].map(([a, b]) => lin(a, b)).join('') +
    ['A', 'B', 'C', 'D'].map(s => '<text x="' + XY[s][0] + '" y="236" text-anchor="middle" font-size="14" font-weight="700" fill="#3a2010">' + s + '</text>').join('') +
    '<path d="M' + (XY[P.tarro][0] - 16) + ' 204 L' + (XY[P.tarro][0] + 16) + ' 204 L' + (XY[P.tarro][0] + 13) + ' 224 L' + (XY[P.tarro][0] - 13) + ' 224 Z" fill="rgba(170,220,240,.8)" stroke="#3a7a90" stroke-width="2"/></svg>';
  ui.body.appendChild(pista);

  const lado = { b1: 'izq', b2: 'izq', b3: 'izq' };
  let ocupado = false, resuelto = false;
  const botones = {};
  ['b1', 'b2', 'b3'].forEach((b, i) => {
    const el = document.createElement('button');
    el.type = 'button';
    el.className = 'jug-bal';
    el.dataset.b = b;
    const [x, y] = pct(XY[b]);
    el.style.left = x + '%';
    el.style.top = y + '%';
    el.innerHTML = '<i></i><b>' + (i + 1) + '</b>';
    el.addEventListener('click', () => {
      if (ocupado || resuelto) return;
      lado[b] = lado[b] === 'izq' ? 'der' : 'izq';
      ui.say('');
      pintar();
    });
    botones[b] = el;
    pista.appendChild(el);
  });

  function pintar(est = lado) {
    Object.keys(botones).forEach(b => {
      botones[b].dataset.lado = est[b];
      botones[b].setAttribute('aria-label', 'Balancín ' + b.slice(1) + ': apunta a la ' + (est[b] === 'izq' ? 'izquierda' : 'derecha'));
    });
  }

  const espera = ms => new Promise(r => setTimeout(r, ms));

  async function soltar() {
    if (ocupado || resuelto) return;
    ocupado = true;
    ui.say('');
    const est = { ...lado };
    let ultima = null;
    for (let n = 0; n < P.canicas; n++) {
      const c = document.createElement('i');
      c.className = 'jug-canica' + (n === P.canicas - 1 ? ' cristal' : '');
      const mover = p => { const [x, y] = pct(XY[p]); c.style.left = x + '%'; c.style.top = y + '%'; };
      mover('entrada');
      pista.appendChild(c);
      await espera(60);
      mover('b1');
      await espera(340);
      const l1 = est.b1;
      est.b1 = l1 === 'izq' ? 'der' : 'izq';
      const b = l1 === 'izq' ? 'b2' : 'b3';
      pintar(est);
      mover(b);
      await espera(340);
      const l2 = est[b];
      est[b] = l2 === 'izq' ? 'der' : 'izq';
      pintar(est);
      ultima = SALIDA[b + ',' + l2];
      mover(ultima);
      await espera(380);
      c.remove();
    }
    pintar();
    ocupado = false;
    if (ultima === P.tarro) {
      resuelto = true;
      ui.say('¡Clinc! El cristal cae justo en el tarro de canicas, sano y salvo. Los juguetes lo celebran en voz bajita para no despertar a Leo. Coged la carta 82.', 'ok');
    } else {
      ui.say('El cristal ha caído por la salida ' + ultima + ' y no en el tarro. Los juguetes lo devuelven a la rampa: seguid las tres canicas con las instrucciones (carta 70).', 'bad');
    }
  }

  ui.button('Soltar las canicas', 'primary', soltar);
  pintar();
  return { close: ui.close };
}
