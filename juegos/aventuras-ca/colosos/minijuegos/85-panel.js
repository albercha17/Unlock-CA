// Carta 85 — El panel del viajero (metapuzle): cinco puzles dejaron una marca de dos cifras (fila y columna de la inscripción de la cámara);
// leídas en el orden de la placa de los cinco dibujos dan la palabra (herramientas/instancias_colosos.py, meta).
import { openGame } from './ui.js';
import { estilo } from './comun.js';

const D = /*DATOS*/{"palabra": "HOGAR"}/*FIN*/;

estilo('co-panel', `
  .co-casillas{display:flex;gap:6px;justify-content:center;margin:8px 0 12px}
  .co-casillas span{width:44px;height:52px;border-radius:8px;border:2px solid #e0a640;background:rgba(20,14,8,.6);color:#ffd27a;
    display:flex;align-items:center;justify-content:center;font:800 1.6rem 'Cinzel',Georgia,serif}
  .co-teclas{display:grid;grid-template-columns:repeat(7,1fr);gap:5px;max-width:340px;margin:0 auto}
  .co-teclas .far-key{min-height:42px;padding:0;font-size:1rem}
`);

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 85 — El panel del viajero',
    instr: 'Escribid la palabra de cinco letras que esconde la inscripción y pulsad «Encender».',
    ...opts
  });
  const n = D.palabra.length;
  let txt = '';
  const casillas = document.createElement('div');
  casillas.className = 'co-casillas';
  const teclas = document.createElement('div');
  teclas.className = 'co-teclas';
  'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'.split('').forEach(l => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'far-key';
    b.textContent = l;
    b.addEventListener('click', () => { if (txt.length < n) { txt += l; pintar(); } });
    teclas.appendChild(b);
  });
  ui.body.append(casillas, teclas);

  function pintar() {
    casillas.innerHTML = '';
    for (let k = 0; k < n; k++) {
      const s = document.createElement('span');
      s.textContent = txt[k] || '';
      casillas.appendChild(s);
    }
  }
  ui.button('Borrar', 'ghost', () => { txt = txt.slice(0, -1); pintar(); });
  ui.button('Encender', 'primary', () => {
    if (txt.length < n) { ui.say('Faltan letras: son ' + n + '.', ''); return; }
    if (txt === D.palabra) {
      ui.say('La flor de cinco pétalos se ilumina, los anillos giran y el Cronoportal os abre el camino de vuelta. Coged la carta 99.', 'ok');
      teclas.querySelectorAll('button').forEach(b => { b.disabled = true; });
    } else {
      ui.say('El panel parpadea en rojo. Revisad las marcas y el orden de los dibujos.', 'bad');
      txt = '';
      pintar();
    }
  });
  pintar();
  return { close: ui.close };
}
