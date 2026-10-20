// Carta 46 — La torre de bloques: construir en una base de 3 x 3 la torre de las instrucciones (vistas de frente y de lado en la carta 30;
// desde arriba y total de bloques en la carta 31). Solución única comprobada en herramientas/instancias_juguetes.py.
import { openGame } from './ui.js';

const T = /*DATOS*/{"alturas": [[3, 0, 1], [2, 1, 1], [2, 1, 1]], "bloques": 12}/*FIN*/;
const FILAS = ['delante', 'en medio', 'detrás'];
const COLOR = ['#f6c42a', '#ee8028', '#d63430'];

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 46 — La torre de bloques',
    instr: 'Toca una casilla para ponerle un bloque más (hasta 3; uno más y se queda vacía). La fila de abajo es la de delante. Construid la torre de las instrucciones.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .jug-base{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;width:min(78vw,280px);margin:4px auto 4px;padding:8px;border-radius:12px;background:#7a5030;border:4px solid #4a2e18}
    .jug-casilla{position:relative;aspect-ratio:1;border:0;border-radius:8px;background:#c89a66;cursor:pointer;display:flex;flex-direction:column-reverse;align-items:center;justify-content:flex-start;padding:6px 0;gap:3px}
    .jug-bloque{width:68%;height:18%;border-radius:4px;border:2px solid rgba(0,0,0,.45);box-shadow:inset 0 3px 0 rgba(255,255,255,.4)}
    .jug-casilla b{position:absolute;right:6px;top:4px;font:700 .9rem 'Fredoka',system-ui;color:#2a1a0a}
    .jug-base.ok{border-color:#7be495;box-shadow:0 0 24px rgba(123,228,149,.6)}
    .jug-etq{text-align:center;font:700 .75rem system-ui,sans-serif;letter-spacing:.15em;color:#ffcc33;margin:0}
    .jug-total{text-align:center;color:#fff;font:600 .9rem 'Fredoka',system-ui;margin:4px 0 0}
  `;
  ui.body.appendChild(style);

  const arriba = document.createElement('p');
  arriba.className = 'jug-etq';
  arriba.textContent = 'DETRÁS';
  const base = document.createElement('div');
  base.className = 'jug-base';
  const abajo = document.createElement('p');
  abajo.className = 'jug-etq';
  abajo.textContent = 'DELANTE';
  const total = document.createElement('p');
  total.className = 'jug-total';
  ui.body.appendChild(arriba);
  ui.body.appendChild(base);
  ui.body.appendChild(abajo);
  ui.body.appendChild(total);

  const h = [[0, 0, 0], [0, 0, 0], [0, 0, 0]];
  let resuelto = false;

  function pintar() {
    base.className = 'jug-base' + (resuelto ? ' ok' : '');
    base.innerHTML = '';
    for (let f = 2; f >= 0; f--) {
      for (let c = 0; c < 3; c++) {
        const b = document.createElement('button');
        b.type = 'button';
        b.className = 'jug-casilla';
        b.dataset.f = String(f);
        b.dataset.c = String(c);
        b.setAttribute('aria-label', 'Casilla ' + FILAS[f] + ', columna ' + (c + 1) + ': ' + h[f][c] + ' bloques');
        for (let k = 0; k < h[f][c]; k++) {
          const q = document.createElement('i');
          q.className = 'jug-bloque';
          q.style.background = COLOR[k];
          b.appendChild(q);
        }
        const n = document.createElement('b');
        n.textContent = String(h[f][c]);
        b.appendChild(n);
        b.addEventListener('click', () => { if (!resuelto) { h[f][c] = (h[f][c] + 1) % 4; ui.say(''); pintar(); } });
        base.appendChild(b);
      }
    }
    total.textContent = 'Bloques puestos: ' + h.flat().reduce((a, b) => a + b, 0);
  }

  const vistas = m => ({
    frente: [0, 1, 2].map(c => Math.max(...[0, 1, 2].map(f => m[f][c]))),
    lado: [0, 1, 2].map(f => Math.max(...m[f])),
    arriba: m.map(fila => fila.map(x => (x ? 1 : 0)).join('')).join('|')
  });

  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    const n = h.flat().reduce((a, b) => a + b, 0);
    if (n !== T.bloques) { ui.say('La torre lleva ' + T.bloques + ' bloques y habéis puesto ' + n + '. Mirad la carta 31.', 'bad'); return; }
    if (h.every((fila, f) => fila.every((x, c) => x === T.alturas[f][c]))) {
      resuelto = true;
      pintar();
      ui.say('¡La torre de Leo, idéntica a las instrucciones! Llega justo al borde de la cama y trepáis por ella. Coged la carta 44.', 'ok');
      return;
    }
    const a = vistas(h), b = vistas(T.alturas);
    const mal = [];
    if (a.frente.join() !== b.frente.join()) mal.push('de frente');
    if (a.lado.join() !== b.lado.join()) mal.push('desde la derecha');
    if (a.arriba !== b.arriba) mal.push('desde arriba');
    ui.say('Así no se ve como en las instrucciones' + (mal.length ? ' (falla la vista ' + mal.join(' y la vista ') + ')' : '') + '. Repasad las cartas 30 y 31.', 'bad');
  });
  ui.button('Vaciar', '', () => { if (!resuelto) { h.forEach(f => f.fill(0)); ui.say(''); pintar(); } });

  pintar();
  return { close: ui.close };
}
