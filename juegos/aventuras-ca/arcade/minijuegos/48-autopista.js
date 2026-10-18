// Carta 48 — El panel de la autopista: cruzar cuatro carriles por turnos sin chocar. El sentido y la velocidad de cada carril están en el tablero de tráfico (carta 52).
// Reglas: en cada turno os movéis (arriba, izquierda, derecha o esperar) y DESPUÉS se mueven los coches casilla a casilla; si un coche pasa por vuestra casilla, os atropella.
// Instancia (herramientas/instancias_arcade.py): solución de 9 pasos: izquierda, derecha, arriba, arriba, derecha, esperar, arriba, arriba, arriba.
import { openGame } from './ui.js';

const ANCHO = 7;
const FILAS = 6;                      // fila 0 = meta, filas 1..4 = carriles, fila 5 = salida
const SALIDA = { f: 5, c: 3 };
const CARRILES = [
  { dir: -1, vel: 1, coches: [1, 3, 6] },
  { dir: -1, vel: 2, coches: [0, 6] },
  { dir: 1, vel: 1, coches: [1, 2] },
  { dir: -1, vel: 2, coches: [4, 6] }
];

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 48 — El panel de la autopista',
    instr: 'Cruza la autopista hasta la meta (arriba). Tú te mueves primero y después se mueven los coches según el tablero de tráfico.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .arc-via{display:grid;grid-template-columns:repeat(7,1fr);gap:2px;max-width:322px;margin:4px auto 8px;padding:6px;border-radius:10px;border:2px solid #ffe23c;background:#07040f}
    .arc-celda{position:relative;aspect-ratio:1;border-radius:3px;background:#12122e}
    .arc-celda.meta{background:#0c3a22}
    .arc-celda.salida{background:#3a1458}
    .arc-celda.carril{background:#16163a}
    .arc-coche{position:absolute;inset:18% 8%;border-radius:4px;background:linear-gradient(180deg,#ff5ad8,#b0208c);box-shadow:0 0 6px #ff5ad8}
    .arc-rana{position:absolute;inset:12%;border-radius:50%;background:#46ff82;border:2px solid #fff;box-shadow:0 0 8px #46ff82}
    .arc-rana::before,.arc-rana::after{content:"";position:absolute;top:22%;width:20%;height:20%;border-radius:50%;background:#07040f}
    .arc-rana::before{left:22%}.arc-rana::after{right:22%}
    .arc-turno{text-align:center;color:#8ffcff;font:600 .85rem system-ui,sans-serif;margin:0 0 8px}
  `;
  ui.body.appendChild(style);

  const via = document.createElement('div');
  via.className = 'arc-via';
  const info = document.createElement('p');
  info.className = 'arc-turno';
  ui.body.appendChild(via);
  ui.body.appendChild(info);

  let est;
  let resuelto = false;
  function reiniciar() { est = { f: SALIDA.f, c: SALIDA.c, coches: CARRILES.map(l => l.coches.slice()), turno: 0 }; }

  function pintar() {
    via.innerHTML = '';
    for (let f = 0; f < FILAS; f++) {
      for (let c = 0; c < ANCHO; c++) {
        const d = document.createElement('div');
        d.className = 'arc-celda ' + (f === 0 ? 'meta' : f === FILAS - 1 ? 'salida' : 'carril');
        d.dataset.f = String(f);
        d.dataset.c = String(c);
        if (f >= 1 && f <= 4 && est.coches[f - 1].includes(c)) {
          const k = document.createElement('div');
          k.className = 'arc-coche';
          k.setAttribute('aria-label', 'Coche');
          d.appendChild(k);
        }
        if (est.f === f && est.c === c) {
          const r = document.createElement('div');
          r.className = 'arc-rana';
          r.setAttribute('aria-label', 'Vosotros');
          d.appendChild(r);
        }
        via.appendChild(d);
      }
    }
    info.textContent = 'Turno ' + est.turno + ' · fila ' + (FILAS - 1 - est.f) + ' de ' + (FILAS - 1);
  }

  // devuelve 'pared' (movimiento imposible, no gasta turno), 'choque', 'ok' o 'meta'
  function paso(mov) {
    let f = est.f, c = est.c;
    if (mov === 'arriba') f--;
    else if (mov === 'izquierda') c--;
    else if (mov === 'derecha') c++;
    if (f < 0 || c < 0 || c >= ANCHO) return 'pared';
    if (f >= 1 && f <= 4 && est.coches[f - 1].includes(c)) return 'choque';
    const nuevos = [];
    let choque = false;
    CARRILES.forEach((l, i) => {
      const nc = [];
      est.coches[i].forEach(x => {
        let y = x;
        for (let k = 0; k < l.vel; k++) {
          y = ((y + l.dir) % ANCHO + ANCHO) % ANCHO;
          if (f === i + 1 && y === c) choque = true;
        }
        nc.push(y);
      });
      nuevos.push(nc);
    });
    if (choque) return 'choque';
    est.f = f; est.c = c; est.coches = nuevos; est.turno++;
    return f === 0 ? 'meta' : 'ok';
  }

  function mover(mov) {
    if (resuelto) return;
    const r = paso(mov);
    if (r === 'pared') { ui.say('No podéis salir de la carretera.', 'bad'); return; }
    if (r === 'choque') {
      reiniciar();
      pintar();
      ui.say('¡Un coche os ha atropellado! Volvéis a la salida. Mirad el tablero de tráfico: dice hacia dónde va cada carril y a qué velocidad.', 'bad');
      return;
    }
    pintar();
    if (r === 'meta') {
      resuelto = true;
      ui.say('¡Meta! Habéis cruzado los cuatro carriles sin un rasguño y la barrera del otro lado se levanta. Coged la carta 58.', 'ok');
    } else {
      ui.say('');
    }
  }

  ui.button('Arriba', 'primary', () => mover('arriba'));
  ui.button('Izquierda', '', () => mover('izquierda'));
  ui.button('Derecha', '', () => mover('derecha'));
  ui.button('Esperar', '', () => mover('quieto'));
  ui.button('Reiniciar', '', () => { if (!resuelto) { reiniciar(); pintar(); ui.say(''); } });

  reiniciar();
  pintar();
  return { close: ui.close };
}
