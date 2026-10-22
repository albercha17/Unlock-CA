// Carta 40 — La sala del VAR: seis jugadas de entrenamiento dibujadas desde arriba (cartas 41 y 43); el reglamento del fuera de juego, en la carta 45.
// Hay que decidir cada jugada: válida o fuera de juego (instancias_futbol.py, VAR). Aro de la bandera: D.aro.
import { openGame } from './ui.js';
import { estilo } from './comun.js';

const D = /*DATOS*/{"fuera": [true, false, true, false, false, false], "aro": 11}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 40 — La sala del VAR', instr: 'Decidid cada jugada: ¿válida o fuera de juego? Las jugadas están en las cartas 41 y 43; el reglamento, en la 45.', ...opts });
  estilo('fu-var', '.var-f{display:flex;align-items:center;gap:8px;max-width:340px;margin:6px auto}.var-f b{min-width:84px;color:#f2c230;font:800 .9rem system-ui,Arial,sans-serif}.var-f button{flex:1;min-height:44px}');
  const voto = D.fuera.map(() => null);
  let resuelto = false;
  const filas = D.fuera.map((_, i) => {
    const f = document.createElement('div');
    f.className = 'var-f';
    f.dataset.i = String(i);
    const t = document.createElement('b');
    t.textContent = 'Jugada ' + 'ABCDEF'[i];
    const mk = (txt, val) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'fu-opc';
      b.dataset.v = val ? 'fuera' : 'valida';
      b.textContent = txt;
      b.addEventListener('click', () => { if (resuelto) return; voto[i] = val; ui.say(''); pintar(); });
      return b;
    };
    const a = mk('Válida', false), b = mk('Fuera de juego', true);
    f.append(t, a, b);
    ui.body.appendChild(f);
    return [a, b];
  });
  function pintar() { filas.forEach(([a, b], i) => { a.classList.toggle('sel', voto[i] === false); b.classList.toggle('sel', voto[i] === true); }); }
  ui.button('Pitar', 'primary', () => {
    if (resuelto) return;
    if (voto.some(v => v === null)) { ui.say('Falta decidir alguna jugada.', 'bad'); return; }
    if (voto.some((v, i) => v !== D.fuera[i])) { ui.say('El árbitro de campo no está de acuerdo con alguna de vuestras decisiones.', 'bad'); return; }
    resuelto = true;
    ui.say('Las seis decisiones coinciden con el libro del árbitro. Aro de la bandera: ' + D.aro + '. Coged la carta 30.', 'ok');
  });
  ui.button('Borrar', 'ghost', () => { if (!resuelto) { voto.fill(null); ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
