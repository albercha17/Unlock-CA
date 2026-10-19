// Carta 46 — El mando de la linterna: recorrer a ciegas el laberinto del yate (plano en la carta 40). Los muros no se ven; solo se nota al chocar.
// Instancia (herramientas/instancias_espia.py): laberinto perfecto de 7 x 7, entrada arriba a la izquierda y salida abajo a la derecha.
import { openGame } from './ui.js';

const N = 7;
// pasillos abiertos entre casillas vecinas, «fc-fc» (fila y columna de cada casilla)
const ABIERTOS = new Set(('00-01 01-02 02-12 03-04 03-13 04-05 05-15 06-16 10-20 11-12 11-21 13-23 14-24 15-16 16-26 20-21 20-30 22-23 23-33 24-34 25-26 25-35 30-31 31-32 32-42 33-43 34-35 35-45 36-46 40-41 40-50 42-52 43-44 43-53 44-54 45-46 46-56 50-51 50-60 51-61 52-62 54-64 55-65 56-66 61-62 62-63 63-64 65-66').split(' '));

function hayPasillo(f, c, f2, c2) {
  const a = '' + f + c, b = '' + f2 + c2;
  return ABIERTOS.has(a + '-' + b) || ABIERTOS.has(b + '-' + a);
}

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 46 — El mando de la linterna',
    instr: 'Muévete con las flechas por los pasillos a oscuras, hasta la salida (abajo a la derecha). Los muros no se ven: usa el plano.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .esp-yate{display:grid;grid-template-columns:repeat(7,1fr);gap:2px;max-width:322px;margin:4px auto 6px;padding:6px;border-radius:10px;border:2px solid #7fe8f0;background:#05090c}
    .esp-cel{position:relative;aspect-ratio:1;border-radius:3px;background:#0b141a}
    .esp-cel.visto{background:#12303a}
    .esp-cel.salida{background:#3a1424}
    .esp-agente{position:absolute;inset:18%;border-radius:50%;background:#ff6fa8;border:2px solid #fff;box-shadow:0 0 12px #ff6fa8}
    .esp-cel.choque{box-shadow:inset 0 0 0 3px #ff4a4a}
    .esp-golpes{text-align:center;color:#7fe8f0;font:600 .85rem system-ui,sans-serif;margin:0 0 8px}
  `;
  ui.body.appendChild(style);

  const yate = document.createElement('div');
  yate.className = 'esp-yate';
  const info = document.createElement('p');
  info.className = 'esp-golpes';
  ui.body.appendChild(yate);
  ui.body.appendChild(info);

  let f = 0, c = 0, golpes = 0, choque = null;
  const vistos = new Set(['00']);
  let resuelto = false;

  function pintar() {
    yate.innerHTML = '';
    for (let i = 0; i < N; i++) {
      for (let j = 0; j < N; j++) {
        const d = document.createElement('div');
        d.className = 'esp-cel' + (vistos.has('' + i + j) ? ' visto' : '') + (i === N - 1 && j === N - 1 ? ' salida' : '') + (choque && choque[0] === i && choque[1] === j ? ' choque' : '');
        d.dataset.f = String(i);
        d.dataset.c = String(j);
        if (i === f && j === c) {
          const a = document.createElement('div');
          a.className = 'esp-agente';
          a.setAttribute('aria-label', 'Vosotros');
          d.appendChild(a);
        }
        yate.appendChild(d);
      }
    }
    info.textContent = 'Choques con un muro: ' + golpes;
  }

  function mover(df, dc) {
    if (resuelto) return;
    const f2 = f + df, c2 = c + dc;
    if (f2 < 0 || c2 < 0 || f2 >= N || c2 >= N || !hayPasillo(f, c, f2, c2)) {
      golpes++;
      choque = [f, c];
      pintar();
      ui.say('¡Pum! Os habéis dado contra un muro. Mirad el plano del yate (carta 40) y probad otro camino.', 'bad');
      return;
    }
    f = f2; c = c2; choque = null;
    vistos.add('' + f + c);
    pintar();
    if (f === N - 1 && c === N - 1) {
      resuelto = true;
      ui.say('La puerta del final del pasillo cede: es la sala de máquinas del yate. Coged la carta 44.', 'ok');
    } else {
      ui.say('');
    }
  }

  ui.button('Arriba', 'primary', () => mover(-1, 0));
  ui.button('Izquierda', '', () => mover(0, -1));
  ui.button('Derecha', '', () => mover(0, 1));
  ui.button('Abajo', '', () => mover(1, 0));

  pintar();
  return { close: ui.close };
}
