// Carta 20 — Excavación: marcar dónde hay huesos enterrados (tipo buscaminas), con las notas de excavación (carta 18).
// Hay 7 huesos. Cada casilla con número no esconde hueso y el número cuenta los huesos de sus 8 vecinas.
// Solución: B2, C4, D1, D5, E2, E3 y F5 (única).
import { openGame } from './ui.js';

const COLS = 6, ROWS = 5, TOTAL = 7;
const LETRAS = 'ABCDEF';
// casillas con número (columna,fila) -> huesos vecinos
const PISTAS = { '4,0': 2, '0,1': 1, '3,1': 3, '1,2': 2, '2,2': 2, '5,2': 2, '1,3': 1, '4,3': 3, '0,4': 0, '1,4': 1, '4,4': 2 };

function vecinas(c, r) {
  const v = [];
  for (let dr = -1; dr <= 1; dr++) {
    for (let dc = -1; dc <= 1; dc++) {
      if ((dc || dr) && c + dc >= 0 && c + dc < COLS && r + dr >= 0 && r + dr < ROWS) v.push((c + dc) + ',' + (r + dr));
    }
  }
  return v;
}

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 20 — Excavación',
    instr: 'Toca las casillas donde crees que hay un hueso enterrado. Toca otra vez para quitar la marca.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .exc-ext{display:grid;grid-template-columns:18px 1fr;grid-template-rows:18px auto;max-width:350px;margin:0 auto 8px;font-size:.78rem;color:#e6cfa0}
    .exc-letras,.exc-nums{display:grid;align-items:center;justify-items:center}
    .exc-letras{grid-column:2;grid-template-columns:repeat(${COLS},1fr)}
    .exc-nums{grid-row:2;grid-template-rows:repeat(${ROWS},1fr)}
    .exc-malla{grid-column:2;grid-row:2;display:grid;grid-template-columns:repeat(${COLS},1fr);gap:3px;padding:6px;border-radius:10px;border:3px solid #5b3a18;background:#2a1a0a;box-shadow:inset 0 0 18px rgba(0,0,0,.75)}
    .exc-cell{position:relative;aspect-ratio:1;padding:0;border:0;border-radius:5px;overflow:hidden;cursor:pointer;font:800 1.2rem Georgia,serif;color:#3a240c;background:url(./img/ui/tierra.jpg) center/cover;box-shadow:inset 0 0 8px rgba(0,0,0,.55)}
    .exc-cell.pista{background:url(./img/ui/suelo-limpio.jpg) center/cover;cursor:default;box-shadow:inset 0 0 6px rgba(120,80,30,.55)}
    .exc-cell img{position:absolute;inset:8%;width:84%;height:84%;object-fit:contain;mix-blend-mode:screen;pointer-events:none;filter:drop-shadow(0 0 5px rgba(255,235,170,.6))}
    .exc-cell:not(.pista):active{filter:brightness(1.2)}
    .exc-cont{color:#e6cfa0;font-size:.85rem;margin-bottom:4px}
  `;
  ui.body.appendChild(style);

  const ext = document.createElement('div');
  ext.className = 'exc-ext';
  const letras = document.createElement('div');
  letras.className = 'exc-letras';
  for (let c = 0; c < COLS; c++) { const s = document.createElement('span'); s.textContent = LETRAS[c]; letras.appendChild(s); }
  const nums = document.createElement('div');
  nums.className = 'exc-nums';
  for (let r = 0; r < ROWS; r++) { const s = document.createElement('span'); s.textContent = String(r + 1); nums.appendChild(s); }
  const malla = document.createElement('div');
  malla.className = 'exc-malla';
  ext.append(letras, nums, malla);
  const cont = document.createElement('div');
  cont.className = 'exc-cont';
  ui.body.append(ext, cont);

  const marcas = new Set();
  let resuelto = false;
  const celdas = {};

  for (let r = 0; r < ROWS; r++) {
    for (let c = 0; c < COLS; c++) {
      const k = c + ',' + r;
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'exc-cell' + (k in PISTAS ? ' pista' : '');
      b.dataset.c = k;
      b.setAttribute('aria-label', 'Casilla ' + LETRAS[c] + (r + 1) + (k in PISTAS ? ', número ' + PISTAS[k] : ''));
      if (k in PISTAS) {
        b.textContent = String(PISTAS[k]);
        b.disabled = true;
      } else {
        b.addEventListener('click', () => {
          if (resuelto) return;
          if (marcas.has(k)) marcas.delete(k); else marcas.add(k);
          ui.say('');
          pintar();
        });
      }
      celdas[k] = b;
      malla.appendChild(b);
    }
  }

  function pintar() {
    Object.keys(celdas).forEach(k => {
      const b = celdas[k];
      const img = b.querySelector('img');
      if (marcas.has(k) && !img) {
        const i = document.createElement('img');
        i.alt = 'Hueso';
        i.src = './img/ui/hueso.jpg';
        b.appendChild(i);
      } else if (!marcas.has(k) && img) {
        img.remove();
      }
      b.dataset.marca = marcas.has(k) ? '1' : '0';
    });
    cont.textContent = 'Huesos marcados: ' + marcas.size + ' de ' + TOTAL;
  }

  ui.button('Quitar todas', 'ghost', () => { if (!resuelto) { marcas.clear(); ui.say(''); pintar(); } });
  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    if (marcas.size !== TOTAL) { ui.say('Las notas hablan de siete huesos y has marcado ' + marcas.size + '.', 'bad'); return; }
    const ok = Object.keys(PISTAS).every(k => {
      const [c, r] = k.split(',').map(Number);
      return vecinas(c, r).filter(v => marcas.has(v)).length === PISTAS[k];
    });
    if (ok) {
      resuelto = true;
      ui.say('¡Todo encaja! Al apartar la tierra aparece el esqueleto parcial de un anquilosaurio y, a su lado, el equipo enterrado de Ibarra. Coged la carta 28.', 'ok');
    } else {
      ui.say('Algún número no cuadra con los huesos que habéis marcado a su alrededor. Contad los de las ocho casillas vecinas.', 'bad');
    }
  });

  pintar();
  return { close: ui.close };
}
