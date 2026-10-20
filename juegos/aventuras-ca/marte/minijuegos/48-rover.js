// Carta 48 — Rover: programar una ruta (↑ ↓ ← →) desde A5 hasta la baliza (F2, dato de la carta 57).
// No se muestra dónde está la baliza: solo el mapa con las rocas.
import { openGame } from './ui.js';

const COLS = 7, ROWS = 5, CELL = 50;
const INICIO = { c: 0, r: 4 };
const META = { c: 5, r: 1 };
const ROCAS = ['1,1', '3,1', '3,2', '1,3', '5,3', '4,4'];
const DIR = { '↑': [0, -1], '↓': [0, 1], '←': [-1, 0], '→': [1, 0] };
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
    .mar-mapa-ext{display:grid;grid-template-columns:18px 1fr;grid-template-rows:18px auto;max-width:350px;margin:0 auto;font-size:.78rem;color:#e8b49a}
    .mar-letras,.mar-nums{display:grid;align-items:center;justify-items:center}
    .mar-letras{grid-column:2;grid-template-columns:repeat(${COLS},1fr)}
    .mar-nums{grid-row:2;grid-template-rows:repeat(${ROWS},1fr)}
    .mar-mapa{position:relative;grid-column:2;grid-row:2;aspect-ratio:${COLS}/${ROWS};border-radius:8px;border:2px solid #5b3a24;overflow:hidden;background:linear-gradient(rgba(12,5,2,.66),rgba(12,5,2,.66)),url(./img/ui/terreno.jpg) center/cover,#2a120c;box-shadow:inset 0 0 22px rgba(0,0,0,.65)}
    .mar-mapa::before{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(0,0,0,.28) 1px,transparent 1px),linear-gradient(90deg,rgba(0,0,0,.28) 1px,transparent 1px);background-size:calc(100%/${COLS}) calc(100%/${ROWS})}
    .mar-obj{position:absolute;width:calc(100%/${COLS});height:calc(100%/${ROWS});display:flex;align-items:center;justify-content:center}
    .mar-obj img{width:92%;height:92%;object-fit:contain;mix-blend-mode:screen;filter:drop-shadow(0 4px 4px rgba(0,0,0,.7))}
    .mar-rover{transition:left .2s linear,top .2s linear}
    .mar-rover img{transition:transform .15s}
    .mar-rover.choque{animation:mar-choque .3s}
    @keyframes mar-choque{25%{transform:translateX(-4px)}75%{transform:translateX(4px)}}
  `;
  ui.body.appendChild(style);

  const ext = document.createElement('div');
  ext.className = 'mar-mapa-ext';
  const letras = document.createElement('div');
  letras.className = 'mar-letras';
  for (let c = 0; c < COLS; c++) { const s = document.createElement('span'); s.textContent = LETRAS[c]; letras.appendChild(s); }
  const nums = document.createElement('div');
  nums.className = 'mar-nums';
  for (let r = 0; r < ROWS; r++) { const s = document.createElement('span'); s.textContent = String(r + 1); nums.appendChild(s); }
  const mapaEl = document.createElement('div');
  mapaEl.className = 'mar-mapa';
  ROCAS.forEach(k => {
    const [c, r] = k.split(',').map(Number);
    const o = document.createElement('div');
    o.className = 'mar-obj';
    o.style.left = (c * 100 / COLS) + '%';
    o.style.top = (r * 100 / ROWS) + '%';
    o.innerHTML = '<img alt="Roca" src="./img/ui/rover/roca.jpg">';
    mapaEl.appendChild(o);
  });
  const roverEl = document.createElement('div');
  roverEl.className = 'mar-obj mar-rover';
  roverEl.innerHTML = '<img alt="Rover" src="./img/ui/rover/rover.jpg">';
  mapaEl.appendChild(roverEl);
  ext.append(letras, nums, mapaEl);
  const prog = document.createElement('div');
  prog.className = 'far-prog';
  const flechas = document.createElement('div');
  flechas.className = 'far-flechas';
  ui.body.append(ext, prog, flechas);

  let programa = [];
  let pos = { ...INICIO };
  let rumbo = 0;
  let ocupado = false;
  let resuelto = false;
  let vivo = true;
  ui.onClose(() => { vivo = false; });

  const GIRO = { '↑': 0, '→': 90, '↓': 180, '←': 270 };
  function mapa(f) {
    if (f) {
      // gira por el camino corto
      const objetivo = GIRO[f];
      let d = ((objetivo - rumbo) % 360 + 540) % 360 - 180;
      rumbo += d;
    } else {
      rumbo = 0;
    }
    roverEl.style.left = (pos.c * 100 / COLS) + '%';
    roverEl.style.top = (pos.r * 100 / ROWS) + '%';
    roverEl.querySelector('img').style.transform = 'rotate(' + rumbo + 'deg)';
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
      if (ROCAS.includes(nc + ',' + nr)) {
        mapa(f);
        roverEl.classList.add('choque');
        ui.say('El rover choca con una roca y se atasca. Vuelve al inicio.', 'bad');
        await new Promise(r => setTimeout(r, 450));
        roverEl.classList.remove('choque');
        pos = { ...INICIO };
        mapa();
        ocupado = false;
        return;
      }
      pos = { c: nc, r: nr };
      mapa(f);
    }
    if (pos.c === META.c && pos.r === META.r) {
      resuelto = true;
      ui.say('¡El rover llega a la baliza! Desde ahí se ve la puerta del anexo del reactor. Coged la carta 72.', 'ok');
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
