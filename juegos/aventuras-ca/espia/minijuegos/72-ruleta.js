// Carta 72 — La martingala: el Dr. Noche empieza con unas fichas y apuesta siempre al rojo siguiendo un sistema; los giros están en la carta 75 y el sistema,
// en la 79. Hay que decir cuántas fichas le quedan tras el último giro (instancias_espia.py, RULETA).
import { openGame } from './ui.js';
import { contador } from './comun.js';

const D = /*DATOS*/{"final": 115}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 72 — La martingala', instr: 'Decid cuántas fichas quedan en el banco tras el último giro. Los giros están en la carta 75 y el sistema de apuestas, en la 79.', ...opts });
  const fichas = contador('Fichas en el banco', 0, 400, 100, 'fichas');
  ui.body.appendChild(fichas.el);
  // pasos de 1 en 1 serían eternos: botones de salto
  const saltos = document.createElement('div');
  saltos.className = 'es-btns';
  [[-10, '−10'], [10, '+10']].forEach(([d, t]) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.dataset.d = String(d);
    b.textContent = t;
    b.addEventListener('click', () => { for (let i = 0; i < Math.abs(d); i++) fichas.el.querySelector('button[data-d="' + (d < 0 ? '-1' : '1') + '"]').click(); });
    saltos.appendChild(b);
  });
  ui.body.appendChild(saltos);
  let resuelto = false;
  ui.button('Contar el banco', 'primary', () => {
    if (resuelto) return;
    const v = fichas.valor();
    if (v !== D.final) { ui.say('El crupier cuenta el banco y no sale ' + v + ': revisad giro a giro lo que se apuesta y lo que se cobra.', 'bad'); return; }
    resuelto = true;
    ui.say('El banco queda en ' + v + ' fichas: la caja del Dr. Noche cede. Coged la carta 82.', 'ok');
  });
  return { close: ui.close };
}
