// Carta 51 — Las torres de vigía: levantar el menor número de torres para que cada plaza de la ciudad esté vigilada. Una torre vigila su plaza y las que
// tienen calle directa con ella. El plano de las plazas, en las cartas 61 y 63 (dos mitades); el cuaderno de Leonardo, en la 26. Las calles no se
// ven en la app. Vale cualquier conjunto del tamaño mínimo que vigile todas (instancias_florencia.py, VIGILANTES).
import { openGame } from './ui.js';
import { estilo } from './taller.js';

const D = /*DATOS*/{"n": 9, "aristas": [[1, 2], [1, 3], [1, 5], [3, 4], [3, 6], [3, 7], [4, 5], [4, 6], [4, 7], [4, 8], [5, 8], [6, 7], [7, 8]], "minimo": 3}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 51 — Las torres de vigía', instr: 'Tocad las plazas donde queréis levantar una torre (otra vez para quitarla). Todas las plazas deben quedar vigiladas con las menos torres posibles. El plano, en las cartas 61, 63 y 26.', ...opts });
  estilo('fl-vig', `.vig-pl{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;max-width:300px;margin:12px auto}.vig-p{aspect-ratio:1;border-radius:50%;border:3px solid #6d5a36;background:#4d3c20;color:#f6e7bf;font:800 1.3rem Georgia,serif;cursor:pointer}.vig-p.on{background:#d9a441;color:#2a1f0c;border-color:#ffd36a}`);
  const g = document.createElement('div'); g.className = 'vig-pl';
  ui.body.appendChild(g);
  const on = new Set();
  let resuelto = false;
  for (let i = 0; i < D.n; i++) {
    const b = document.createElement('button'); b.type = 'button'; b.className = 'vig-p'; b.dataset.i = String(i); b.textContent = String(i + 1);
    b.setAttribute('aria-label', 'Plaza ' + (i + 1));
    b.addEventListener('click', () => { if (resuelto) return; on.has(i) ? on.delete(i) : on.add(i); b.classList.toggle('on', on.has(i)); ui.say(''); g.dataset.torres = [...on].sort().join(','); });
    g.appendChild(b);
  }
  ui.button('Avisar al Gonfaloniere', 'primary', () => {
    if (resuelto) return;
    if (!on.size) { ui.say('Levantad alguna torre.', 'bad'); return; }
    const vigilada = new Set(on);
    D.aristas.forEach(([a, b]) => { if (on.has(a)) vigilada.add(b); if (on.has(b)) vigilada.add(a); });
    const sin = D.n - vigilada.size;
    if (sin > 0) { ui.say('Quedan ' + sin + ' plaza' + (sin > 1 ? 's' : '') + ' fuera de vista (plano, cartas 61 y 63).', 'bad'); return; }
    if (on.size > D.minimo) { ui.say('Toda la ciudad está vigilada, pero el Gonfaloniere dice que se puede hacer con menos torres (carta 26).', 'bad'); return; }
    resuelto = true;
    ui.say('Toda Florencia queda a la vista con el mínimo de torres y el Gonfaloniere firma el permiso. Coged la carta 58.', 'ok');
  });
  return { close: ui.close };
}
