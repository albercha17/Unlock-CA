// Carta 20 — El aparcamiento de naves (Rush Hour): sacar la nave roja (la 1) por la puerta de la derecha moviendo las demás, que solo avanzan y
// retroceden por donde apuntan. El tablero, en las cartas 19 y 21 (dos mitades); el acertijo, en la 18. Vale cualquier solución.
import { openGame } from './ui.js';
import { estilo, NEON } from './maquina.js';

const D = /*DATOS*/{"n": 6, "naves": [[2, 2, 2, true], [5, 3, 3, true], [4, 1, 2, false], [0, 3, 3, true], [1, 4, 2, true], [3, 1, 3, true], [2, 4, 3, false]], "minimo": 18}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 20 — El aparcamiento de naves', instr: 'Tocad una nave y movedla una casilla con las flechas. Solo se mueven por donde apuntan. Sacad la nave 1 por la puerta de la derecha. El tablero y el acertijo están en las cartas 18, 19 y 21.', ...opts });
  const L = 52;
  estilo('ar-ata', `
    .ata-tab{position:relative;margin:8px auto;border-radius:8px;background:#0a0418;border:2px solid #2ee67a;touch-action:manipulation}
    .ata-pieza{position:absolute;border-radius:7px;border:3px solid #f0f0ff;cursor:pointer;color:#10081c;font:800 1.1rem ui-monospace,monospace;display:flex;align-items:center;justify-content:center;transition:left .12s,top .12s;padding:0}
    .ata-pieza.sel{outline:3px solid #ffde46;box-shadow:0 0 12px #ffde46}
    .ata-flechas{display:flex;justify-content:center;gap:10px;margin:6px 0}
    .ata-flechas button{min-width:64px;min-height:46px;border-radius:8px;border:2px solid #ff5ad8;background:linear-gradient(180deg,#3a1458,#1c0a30);color:#ffd6f6;font:700 1.3rem system-ui;cursor:pointer;box-shadow:0 3px 0 #0d0518}
  `);
  const N = D.n;
  const naves = D.naves.map(([f, c, largo, hor]) => ({ f, c, largo, hor }));
  let sel = -1, mov = 0, resuelto = false;
  const tab = document.createElement('div');
  tab.className = 'ata-tab';
  tab.style.width = tab.style.height = (N * L) + 'px';
  const piezas = naves.map((n, i) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'ata-pieza';
    b.dataset.i = String(i);
    b.textContent = String(i + 1);
    b.style.background = i === 0 ? NEON[0] : NEON[(i % 7) + 1];
    b.style.width = (n.hor ? n.largo * L : L) - 6 + 'px';
    b.style.height = (n.hor ? L : n.largo * L) - 6 + 'px';
    b.setAttribute('aria-label', 'Nave ' + (i + 1));
    b.addEventListener('click', () => { if (resuelto) return; sel = i; pintar(); });
    tab.appendChild(b);
    return b;
  });
  const info = document.createElement('div');
  info.className = 'ar-pie';
  const flechas = document.createElement('div');
  flechas.className = 'ata-flechas';
  const menos = document.createElement('button'); menos.type = 'button'; menos.className = 'ata-menos'; menos.textContent = '◀ ▲';
  const mas = document.createElement('button'); mas.type = 'button'; mas.className = 'ata-mas'; mas.textContent = '▶ ▼';
  flechas.append(menos, mas);
  ui.body.append(tab, flechas, info);

  function libre(f, c, salvo) {
    if (f < 0 || c < 0 || f >= N || c >= N) return false;
    return !naves.some((n, i) => {
      if (i === salvo) return false;
      for (let k = 0; k < n.largo; k++) if ((n.hor ? n.f : n.f + k) === f && (n.hor ? n.c + k : n.c) === c) return true;
      return false;
    });
  }
  function mover(d) {
    if (resuelto) return;
    if (sel < 0) { ui.say('Tocad primero una nave.', 'bad'); return; }
    const n = naves[sel];
    const nf = n.hor ? n.f : n.f + d, nc = n.hor ? n.c + d : n.c;
    // la casilla que pasa a ocupar la nave: delante si avanza, detrás si retrocede
    const cf = n.hor ? n.f : (d > 0 ? n.f + n.largo : n.f - 1);
    const cc = n.hor ? (d > 0 ? n.c + n.largo : n.c - 1) : n.c;
    if (!libre(cf, cc, sel)) {
      ui.say('La nave ' + (sel + 1) + ' no puede moverse en ese sentido: hay otra nave o el borde.', 'bad');
      return;
    }
    n.f = nf; n.c = nc; mov++;
    ui.say('');
    pintar();
    if (sel === 0 && n.c + n.largo === N) terminar();
  }
  function terminar() {
    resuelto = true;
    ui.say('La nave 1 sale por la puerta y el aparcamiento se despeja en ' + mov + ' movimientos. Coged la carta 28.', 'ok');
  }
  function pintar() {
    naves.forEach((n, i) => {
      piezas[i].style.left = (n.c * L + 3) + 'px';
      piezas[i].style.top = (n.f * L + 3) + 'px';
      piezas[i].classList.toggle('sel', i === sel);
    });
    info.textContent = 'Movimientos: ' + mov + (sel >= 0 ? ' · nave elegida: ' + (sel + 1) : '');
    tab.dataset.mov = String(mov);
  }
  menos.addEventListener('click', () => mover(-1));
  mas.addEventListener('click', () => mover(1));
  ui.button('Empezar de nuevo', 'ghost', () => {
    if (resuelto) return;
    D.naves.forEach(([f, c], i) => { naves[i].f = f; naves[i].c = c; });
    mov = 0; sel = -1; ui.say(''); pintar();
  });
  pintar();
  return { close: ui.close };
}
