// Carta 51 — La sucesión: decir quién hereda la corona de Piedra Negra aplicando las leyes del reino (carta 26) al árbol del rey Aerion (cartas 61 y 63,
// dos mitades). Solución: Daemon (instancias_trono.py, SUCESION).
import { openGame } from './ui.js';
import { estilo } from './reino.js';

const D = /*DATOS*/{"opciones": ["Rhaena", "Daemon", "Maegor", "Aemon", "Daenys", "Jaena"], "solucion": "Daemon"}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 51 — La sucesión', instr: 'El rey Aerion ha muerto. Elegid quién hereda la corona según las leyes del reino (carta 26) y el árbol de la familia (cartas 61 y 63).', ...opts });
  estilo('tr-suc', `.suc-op{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;max-width:300px;margin:14px auto}.suc-b{padding:14px 6px;border-radius:12px;border:3px solid #6d8aa6;background:#2c3a4a;color:#e6f1fb;font:800 1.1rem Georgia,serif;cursor:pointer}.suc-b.sel{border-color:#8fc7ee;background:#3a5a78}`);
  const g = document.createElement('div'); g.className = 'suc-op';
  let sel = null, resuelto = false;
  D.opciones.forEach(n => {
    const b = document.createElement('button'); b.type = 'button'; b.className = 'suc-b'; b.dataset.n = n; b.textContent = n;
    b.addEventListener('click', () => { if (resuelto) return; sel = n; g.querySelectorAll('.suc-b').forEach(x => x.classList.toggle('sel', x === b)); ui.say(''); });
    g.appendChild(b);
  });
  ui.body.appendChild(g);
  ui.button('Coronar', 'primary', () => {
    if (resuelto) return;
    if (!sel) { ui.say('Elegid a alguien.', 'bad'); return; }
    if (sel === D.solucion) {
      resuelto = true;
      ui.say('El consejo se pone en pie y aclama a ' + sel + ': las leyes lo dicen claro. El maestre os abre la cripta de los archivos. Coged la carta 58.', 'ok');
    } else ui.say('Las leyes no dicen eso: repasad quién queda tras apartar a quien no puede heredar y en qué línea (cartas 26, 61 y 63).', 'bad');
  });
  return { close: ui.close };
}
