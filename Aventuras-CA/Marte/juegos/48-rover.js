// Carta 48 — Rover: programar una ruta (↑ ↓ ← →) desde A5 hasta la baliza (F2, dato de la carta 57).
// No se muestra dónde está la baliza: solo el mapa con las rocas.
import { openGame } from './ui.js';

const COLS = 7, ROWS = 5, CELL = 50;
const INICIO = { c: 0, r: 4 };
const META = { c: 5, r: 1 };
const ROCAS = ['1,1', '3,1', '3,2', '1,3', '5,3', '4,4'];
const DIR = { '↑': [0, -1], '↓': [0, 1], '←': [-1, 0], '→': [1, 0] };
const NS = 'http://www.w3.org/2000/svg';
const LETRAS = 'ABCDEFG';
const MAX = 24;

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 48 — Rover de superficie',
    instr: 'Programa la ruta del rover con las flechas y pulsa Ejecutar. Las rocas lo bloquean.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .far-prog{min-height:34px;display:flex;flex-wrap:wrap;gap:4px;justify-content:center;margin:8px 0;font-size:1.3rem;color:#ffd27a}
    .far-prog span{background:#1c2a36;border:1px solid #34495e;border-radius:6px;padding:0 8px}
    .far-flechas{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:8px}
  `;
  ui.body.appendChild(style);

  const svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('viewBox', `-20 -20 ${COLS * CELL + 40} ${ROWS * CELL + 40}`);
  svg.setAttribute('width', '100%');
  svg.style.background = '#2a120c';
  svg.style.borderRadius = '10px';
  const prog = document.createElement('div');
  prog.className = 'far-prog';
  const flechas = document.createElement('div');
  flechas.className = 'far-flechas';
  ui.body.append(svg, prog, flechas);

  let programa = [];
  let pos = { ...INICIO };
  let ocupado = false;
  let resuelto = false;
  let vivo = true;
  ui.onClose(() => { vivo = false; });

  function el(tag, attrs, texto) {
    const e = document.createElementNS(NS, tag);
    Object.keys(attrs).forEach(k => e.setAttribute(k, attrs[k]));
    if (texto !== undefined) e.textContent = texto;
    svg.appendChild(e);
    return e;
  }

  function mapa() {
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    for (let c = 0; c < COLS; c++) {
      el('text', { x: c * CELL + CELL / 2, y: -6, 'text-anchor': 'middle', 'font-size': 13, fill: '#e8b49a', 'font-family': 'system-ui,sans-serif' }, LETRAS[c]);
    }
    for (let r = 0; r < ROWS; r++) {
      el('text', { x: -8, y: r * CELL + CELL / 2 + 5, 'text-anchor': 'middle', 'font-size': 13, fill: '#e8b49a', 'font-family': 'system-ui,sans-serif' }, String(r + 1));
      for (let c = 0; c < COLS; c++) {
        el('rect', { x: c * CELL + 1.5, y: r * CELL + 1.5, width: CELL - 3, height: CELL - 3, rx: 5, fill: '#4a2214' });
        if (ROCAS.includes(c + ',' + r)) {
          el('text', { x: c * CELL + CELL / 2, y: r * CELL + CELL / 2 + 9, 'text-anchor': 'middle', 'font-size': 26 }, '🪨');
        }
      }
    }
    el('text', { x: pos.c * CELL + CELL / 2, y: pos.r * CELL + CELL / 2 + 9, 'text-anchor': 'middle', 'font-size': 26 }, '🤖');
  }

  function pintarPrograma() {
    prog.innerHTML = '';
    programa.forEach(f => {
      const s = document.createElement('span');
      s.textContent = f;
      prog.appendChild(s);
    });
  }

  async function ejecutar() {
    if (ocupado || resuelto || !programa.length) return;
    ocupado = true;
    pos = { ...INICIO };
    mapa();
    for (const f of programa) {
      await new Promise(r => setTimeout(r, 220));
      if (!vivo) return;
      const nc = pos.c + DIR[f][0], nr = pos.r + DIR[f][1];
      if (nc < 0 || nc >= COLS || nr < 0 || nr >= ROWS) { ui.say('El rover llega al borde del mapa y se detiene.', 'bad'); break; }
      if (ROCAS.includes(nc + ',' + nr)) { ui.say('El rover choca con una roca y se atasca. Vuelve al inicio.', 'bad'); pos = { ...INICIO }; mapa(); ocupado = false; return; }
      pos = { c: nc, r: nr };
      mapa();
    }
    if (pos.c === META.c && pos.r === META.r) {
      resuelto = true;
      ui.say('¡El rover llega a la baliza! Desde ahí se ve el anexo del reactor. Coged la carta 79.', 'ok');
    } else {
      if (!document.querySelector('.far-feedback.bad')?.textContent) ui.say('El rover se detiene en ' + LETRAS[pos.c] + (pos.r + 1) + ', lejos de la baliza.', 'bad');
      pos = { ...INICIO };
      mapa();
    }
    ocupado = false;
  }

  ['↑', '↓', '←', '→'].forEach(f => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'far-key';
    b.textContent = f;
    b.setAttribute('aria-label', 'Añadir ' + f);
    b.addEventListener('click', () => {
      if (ocupado || resuelto || programa.length >= MAX) return;
      programa.push(f);
      ui.say('');
      pintarPrograma();
    });
    flechas.appendChild(b);
  });

  ui.button('Borrar último', 'ghost', () => { if (!ocupado && !resuelto) { programa.pop(); pintarPrograma(); } });
  ui.button('Reiniciar', 'ghost', () => { if (!ocupado && !resuelto) { programa = []; ui.say(''); pintarPrograma(); pos = { ...INICIO }; mapa(); } });
  ui.button('Ejecutar', 'primary', ejecutar);

  mapa();
  pintarPrograma();
  return { close: ui.close };
}
