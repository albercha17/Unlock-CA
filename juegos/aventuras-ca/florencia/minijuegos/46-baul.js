// Carta 46 — El baúl de viaje: encajar las cuatro cajas de Leonardo (formas en las cartas 47 a 50) en un baúl de 5 x 4 sin huecos.
// Las cajas se pueden girar, no voltear. Vale cualquier encaje que llene el baúl (herramientas/instancias_ampliacion.py los cuenta).
import { openGame } from './ui.js';

const B = /*DATOS*/{"ancho": 5, "alto": 4, "piezas": {"ornitoptero": [[0, 0], [1, 0], [2, 0], [3, 0], [1, 1]], "leon": [[1, 0], [1, 1], [1, 2], [0, 2], [1, 3]], "laud": [[0, 0], [0, 1], [1, 1], [0, 2]], "carro": [[1, 0], [2, 0], [1, 1], [0, 2], [1, 2], [2, 2]]}}/*FIN*/;
const NOMBRE = { ornitoptero: 'Ornitóptero', leon: 'León mecánico', laud: 'Laúd de plata', carro: 'Carro blindado' };
const COLOR = { ornitoptero: '#ba783c', leon: '#c8a03c', laud: '#965a78', carro: '#5a785a' };

function girar(celdas, veces) {
  let p = celdas.map(([x, y]) => [x, y]);
  for (let i = 0; i < veces; i++) p = p.map(([x, y]) => [y, -x]);
  const mx = Math.min(...p.map(c => c[0])), my = Math.min(...p.map(c => c[1]));
  return p.map(([x, y]) => [x - mx, y - my]);
}

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 46 — El baúl de viaje',
    instr: 'Elegid una caja, giradla si hace falta y tocad la casilla del baúl donde va su esquina de arriba a la izquierda. Tocad una caja ya puesta para sacarla. Las formas están en las cartas 47 a 50.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .flo-baul{display:grid;gap:3px;width:min(84vw,310px);margin:6px auto;padding:8px;border-radius:8px;background:#4a2e16;border:5px solid #b8862e}
    .flo-celda{aspect-ratio:1;border:0;border-radius:3px;background:#7a5634;cursor:pointer;padding:0}
    .flo-baul.ok{border-color:#7be495}
    .flo-cajas{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin:6px 0}
    .flo-caja{padding:8px 10px;border-radius:8px;border:2px solid #e8c878;background:#3a2414;color:#f6e4b8;font:600 .8rem Georgia,serif;cursor:pointer}
    .flo-caja.sel{background:#8a5a20;box-shadow:0 0 0 2px #fff}
    .flo-caja:disabled{opacity:.3}
    .flo-giro{text-align:center;color:#f6e4b8;font:600 .8rem system-ui;margin:0}
  `;
  ui.body.appendChild(style);
  const baul = document.createElement('div');
  baul.className = 'flo-baul';
  baul.style.gridTemplateColumns = 'repeat(' + B.ancho + ',1fr)';
  const cajas = document.createElement('div');
  cajas.className = 'flo-cajas';
  const giroTxt = document.createElement('p');
  giroTxt.className = 'flo-giro';
  ui.body.appendChild(cajas);
  ui.body.appendChild(giroTxt);
  ui.body.appendChild(baul);

  const puestas = {};          // nombre -> lista de celdas "x,y"
  let elegida = null, giro = 0, resuelto = false;
  const dueño = () => { const d = {}; Object.entries(puestas).forEach(([n, cs]) => cs.forEach(c => { d[c] = n; })); return d; };

  function pintar() {
    const d = dueño();
    baul.innerHTML = '';
    baul.classList.toggle('ok', resuelto);
    for (let y = 0; y < B.alto; y++) {
      for (let x = 0; x < B.ancho; x++) {
        const b = document.createElement('button');
        b.type = 'button';
        b.className = 'flo-celda';
        b.dataset.x = String(x);
        b.dataset.y = String(y);
        const n = d[x + ',' + y];
        if (n) b.style.background = COLOR[n];
        b.setAttribute('aria-label', 'Casilla ' + (x + 1) + ',' + (y + 1) + (n ? ': ' + NOMBRE[n] : ''));
        b.addEventListener('click', () => tocar(x, y));
        baul.appendChild(b);
      }
    }
    cajas.innerHTML = '';
    Object.keys(B.piezas).forEach(n => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'flo-caja' + (elegida === n ? ' sel' : '');
      b.dataset.p = n;
      b.textContent = NOMBRE[n];
      b.disabled = !!puestas[n];
      b.addEventListener('click', () => { if (!resuelto) { elegida = n; ui.say(''); pintar(); } });
      cajas.appendChild(b);
    });
    giroTxt.textContent = elegida ? NOMBRE[elegida] + ' · girada ' + giro * 90 + '°' : 'Elegid una caja';
  }

  function tocar(x, y) {
    if (resuelto) return;
    const d = dueño();
    if (d[x + ',' + y]) { delete puestas[d[x + ',' + y]]; ui.say(''); pintar(); return; }
    if (!elegida) { ui.say('Elegid primero una caja.', 'bad'); return; }
    const celdas = girar(B.piezas[elegida], giro).map(([cx, cy]) => [cx + x, cy + y]);
    if (celdas.some(([cx, cy]) => cx >= B.ancho || cy >= B.alto || d[cx + ',' + cy])) { ui.say('Ahí no cabe: se sale del baúl o choca con otra caja.', 'bad'); return; }
    puestas[elegida] = celdas.map(([cx, cy]) => cx + ',' + cy);
    elegida = null; giro = 0;
    ui.say('');
    pintar();
    if (Object.keys(puestas).length === Object.keys(B.piezas).length) {
      resuelto = true;
      pintar();
      ui.say('¡Las cuatro cajas encajan sin un hueco! Cerráis el baúl y la escalera queda libre hasta la azotea. Coged la carta 74.', 'ok');
    }
  }

  ui.button('Girar la caja', '', () => { if (!resuelto && elegida) { giro = (giro + 1) % 4; pintar(); } });
  ui.button('Vaciar el baúl', '', () => { if (!resuelto) { Object.keys(puestas).forEach(k => delete puestas[k]); ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
