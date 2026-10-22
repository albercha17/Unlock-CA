// Carta 72 — El montacargas: elegir, entre los cuatro aparejos del almacén (carta 75), el que alza la carga con lo que aguanta la mano y gasta la menor
// cuerda (peso y esfuerzo, en la carta 79). Un aparejo con n cuerdas sosteniendo el peso divide el esfuerzo entre n. Solución en instancias_florencia.py
// (POLEAS). Letra de la clave: O.
import { openGame } from './ui.js';
import { estilo } from './taller.js';

const D = /*DATOS*/{"sistemas": [4, 2, 5, 3], "solucion": 0, "letra": "O"}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 72 — El montacargas', instr: 'Elegid el aparejo (1 a 4) que alza la carga con lo que aguanta la mano y gasta la menor cuerda. Los aparejos, en la carta 75; la carga y la mano, en la 79.', ...opts });
  estilo('fl-pol', `.pol-op{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;max-width:320px;margin:14px auto}.pol-b{aspect-ratio:1;border-radius:12px;border:3px solid #6d5a36;background:#4d3c20;color:#f6e7bf;font:800 1.6rem Georgia,serif;cursor:pointer}.pol-b.sel{border-color:#ffd36a;background:#7a5f26}`);
  const g = document.createElement('div'); g.className = 'pol-op';
  let sel = null, resuelto = false;
  D.sistemas.forEach((_, i) => {
    const b = document.createElement('button'); b.type = 'button'; b.className = 'pol-b'; b.dataset.i = String(i); b.textContent = String(i + 1); b.setAttribute('aria-label', 'Aparejo ' + (i + 1));
    b.addEventListener('click', () => { if (resuelto) return; sel = i; g.querySelectorAll('.pol-b').forEach(x => x.classList.toggle('sel', x === b)); ui.say(''); });
    g.appendChild(b);
  });
  ui.body.appendChild(g);
  ui.button('Alzar la carga', 'primary', () => {
    if (resuelto) return;
    if (sel === null) { ui.say('Elegid un aparejo.', 'bad'); return; }
    if (sel === D.solucion) {
      resuelto = true;
      ui.say('La carga sube con un tirón firme y sin romper la cuerda: el montacargas lleva hasta el archivo. Letra de la clave: ' + D.letra + '. Coged la carta 82.', 'ok');
    } else ui.say('Con ese aparejo la mano no puede, o se gasta más cuerda de la necesaria (cartas 75 y 79).', 'bad');
  });
  return { close: ui.close };
}
