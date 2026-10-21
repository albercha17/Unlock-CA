// Carta 64 — El friso de azulejos: falta un azulejo en el friso de la sala del trono (cartas 66 y 67, dos mitades). Cada azulejo lleva una
// figura, un color y un tamaño, y el friso sigue una regla para cada cosa. Solución única (instancias_egipto.py, FRISO).
import { openGame } from './ui.js';
import { estilo, guardarSello, figuraSVG } from './nilo.js';

const D = /*DATOS*/{"opciones": [{"fig": 1, "color": 1, "tam": 2}, {"fig": 1, "color": 2, "tam": 2}, {"fig": 1, "color": 0, "tam": 2}, {"fig": 2, "color": 0, "tam": 2}, {"fig": 1, "color": 0, "tam": 1}, {"fig": 1, "color": 0, "tam": 0}], "solucion": 2, "figuras": {"anj": [{"t": "c", "c": [50, 30], "r": 20, "w": 9}, {"t": "l", "p": [[50, 50], [50, 94]], "w": 10}, {"t": "l", "p": [[26, 66], [74, 66]], "w": 10}], "ojo": [{"t": "p", "p": [[8, 50], [26, 34], [50, 28], [74, 34], [92, 50], [74, 62], [50, 68], [26, 62]]}, {"t": "c", "c": [50, 48], "r": 11, "f": "fondo"}, {"t": "l", "p": [[50, 68], [42, 90], [60, 90]], "w": 7}], "escarabajo": [{"t": "p", "p": [[76.0, 56.0], [75.3, 63.1], [73.4, 69.9], [70.3, 76.0], [66.2, 81.0], [61.3, 84.8], [55.8, 87.2], [50.0, 88.0], [44.2, 87.2], [38.7, 84.8], [33.8, 81.0], [29.7, 76.0], [26.6, 69.9], [24.7, 63.1], [24.0, 56.0], [24.7, 48.9], [26.6, 42.1], [29.7, 36.0], [33.8, 31.0], [38.7, 27.2], [44.2, 24.8], [50.0, 24.0], [55.8, 24.8], [61.3, 27.2], [66.2, 31.0], [70.3, 36.0], [73.4, 42.1], [75.3, 48.9]]}, {"t": "c", "c": [50, 20], "r": 12}, {"t": "l", "p": [[50, 30], [50, 86]], "w": 4, "f": "fondo"}, {"t": "l", "p": [[28, 44], [10, 36]], "w": 6}, {"t": "l", "p": [[24, 62], [8, 64]], "w": 6}, {"t": "l", "p": [[28, 80], [12, 92]], "w": 6}, {"t": "l", "p": [[72, 44], [90, 36]], "w": 6}, {"t": "l", "p": [[76, 62], [92, 64]], "w": 6}, {"t": "l", "p": [[72, 80], [88, 92]], "w": 6}]}, "colores": ["terracota", "turquesa", "oro"]}/*FIN*/;
const COL = { terracota: '#be5a37', turquesa: '#329696', oro: '#dcaa32' };

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 64 — El friso de azulejos', instr: 'Al friso de la sala del trono le falta un azulejo. Elegid, entre estos seis, el que lo completa, y pulsad «Colocar».', ...opts });
  estilo('eg-azu', `.azu-op{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;max-width:330px;margin:10px auto}.azu-t{aspect-ratio:1;border-radius:8px;border:3px solid #6d5a36;background:#f6e7bf;cursor:pointer;display:flex;align-items:center;justify-content:center;padding:0}.azu-t.sel{border-color:#ffd36a;outline:3px solid #ffd36a}`);
  const g = document.createElement('div'); g.className = 'azu-op';
  let sel = null, resuelto = false;
  D.opciones.forEach((o, i) => {
    const b = document.createElement('button'); b.type = 'button'; b.className = 'azu-t'; b.dataset.i = String(i);
    b.setAttribute('aria-label', 'Azulejo ' + (i + 1));
    const nombres = ['anj', 'ojo', 'escarabajo'];
    b.appendChild(figuraSVG(D.figuras[nombres[o.fig]], COL[D.colores[o.color]], '#f6e7bf', 34 + o.tam * 18));
    b.addEventListener('click', () => { if (resuelto) return; sel = i; g.querySelectorAll('.azu-t').forEach(x => x.classList.toggle('sel', x === b)); ui.say(''); });
    g.appendChild(b);
  });
  ui.body.appendChild(g);
  ui.button('Colocar', 'primary', () => {
    if (resuelto) return;
    if (sel === null) { ui.say('Elegid un azulejo.', 'bad'); return; }
    if (sel === D.solucion) {
      resuelto = true; guardarSello('64');
      ui.say('El azulejo encaja y el friso entero se ilumina: una losa del suelo se levanta y deja ver un hueco con un brillo dorado. Coged la carta 62.', 'ok');
    } else ui.say('Ese azulejo rompe alguna regla del friso: mirad cómo cambian figura, color y tamaño de una fila a otra y de una columna a otra (cartas 66 y 67).', 'bad');
  });
  return { close: ui.close };
}
