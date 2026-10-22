// Carta 72 — Cavar en la gruta: el suelo de arena de la gruta repite la cuadrícula del mapa de la isla (carta 75), pero se entra por el este, así que se ve
// girado (carta 79: el norte queda a la derecha). Hay que cavar en la casilla de la X del mapa PLEGADO por los dos lados. Desplegado, el mapa tiene más filas y
// columnas que el suelo y la X cae en otro sitio. Datos de herramientas/instancias_piratas.py. Distancia de la gruta: R.distancia.
import { openGame } from './ui.js';

const R = /*DATOS*/{"cols": 6, "filas": 8, "inicio": [0, 1], "celdas": [[0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [4, 2], [4, 3], [4, 4], [4, 5], [3, 5], [2, 5], [2, 6]], "distancia": 2}/*FIN*/;

export function startMinigame(opts = {}) {
  // en pantalla: entrando por el este, el oeste queda arriba y el norte a la derecha
  const ancho = R.filas, alto = R.cols;
  const aPantalla = (c, f) => [R.filas - 1 - f, c];
  const x = R.celdas[R.celdas.length - 1];
  const tesoro = aPantalla(x[0], x[1]);
  const palmera = aPantalla(R.inicio[0], R.inicio[1]);

  const ui = openGame({
    title: 'Carta 72 — Cavar en la gruta',
    instr: 'El suelo de la gruta repite la cuadrícula del mapa, pero entráis por el este: lo veis girado, con el norte a la derecha (carta 79). La palmera de piedra marca la palmera del mapa (carta 75). Tocad la casilla donde hay que cavar.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .pir-gruta{position:relative;display:grid;grid-template-columns:repeat(${ancho},1fr);gap:2px;width:min(88vw,330px);margin:20px auto 6px;padding:5px;border-radius:10px;
      background:#3a2a18;border:3px solid #6a4a2a;box-shadow:inset 0 0 30px rgba(0,0,0,.7)}
    .pir-arena{position:relative;aspect-ratio:1;border:0;border-radius:3px;padding:0;cursor:pointer;background:radial-gradient(circle at 40% 35%,#e6cc90,#c8a464 70%)}
    .pir-arena.palmera{cursor:default;background:radial-gradient(circle,#8a8274,#5a544a)}
    .pir-arena.palmera::after{content:'';position:absolute;inset:14%;background:url('./img/ui/palmera.png') center / contain no-repeat}
    .pir-arena.hoyo{background:radial-gradient(circle,#5a3a1a 0 38%,#c8a464 42%)}
    .pir-arena.tesoro{background:radial-gradient(circle,#fff0a0,#e8b84a 45%,#8a5a14);box-shadow:0 0 16px #ffd27a}
    .pir-rosa-g{position:absolute;right:-6px;top:-22px;font:700 .8rem system-ui,sans-serif;color:#f6e7b8}
    .pir-entrada{text-align:center;font:700 .75rem system-ui,sans-serif;letter-spacing:.2em;color:#e8b84a;margin:0}
  `;
  ui.body.appendChild(style);

  const gruta = document.createElement('div');
  gruta.className = 'pir-gruta';
  gruta.innerHTML = '<span class="pir-rosa-g">NORTE ▶</span>';
  const entrada = document.createElement('p');
  entrada.className = 'pir-entrada';
  entrada.textContent = 'ENTRADA (ESTE)';
  ui.body.appendChild(gruta);
  ui.body.appendChild(entrada);

  let resuelto = false;
  for (let y = 0; y < alto; y++) {
    for (let xx = 0; xx < ancho; xx++) {
      const b = document.createElement('button');
      b.type = 'button';
      b.dataset.x = String(xx);
      b.dataset.y = String(y);
      const esPalmera = xx === palmera[0] && y === palmera[1];
      b.className = 'pir-arena' + (esPalmera ? ' palmera' : '');
      b.setAttribute('aria-label', esPalmera ? 'Palmera de piedra' : 'Arena, fila ' + (y + 1) + ', columna ' + (xx + 1));
      if (!esPalmera) b.addEventListener('click', () => {
        if (resuelto) return;
        if (xx === tesoro[0] && y === tesoro[1]) {
          resuelto = true;
          b.classList.add('tesoro');
          ui.say('¡La pala choca con madera! Bajo la arena hay una trampilla con argollas de hierro. Al levantarla, brilla el oro: el tesoro del capitán Calavera. Distancia de la gruta: ' + R.distancia + (R.distancia === 1 ? ' casilla' : ' casillas') + '. Coged la carta 82.', 'ok');
        } else {
          b.classList.add('hoyo');
          ui.say('Solo arena y conchas. Recordad: el mapa se pliega por los dos lados y aquí lo veis girado, con el norte a la derecha.', 'bad');
        }
      });
      gruta.appendChild(b);
    }
  }
  return { close: ui.close };
}
