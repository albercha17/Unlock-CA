// Carta 46 — El veredicto del VAR: decidir si cada una de las cuatro jugadas (cartas 40 y 41) es gol válido o fuera de juego (reglamento en la carta 42).
// Solución: A fuera de juego, B válido, C válido, D fuera de juego.
import { openGame } from './ui.js';

const JUGADAS = ['A', 'B', 'C', 'D'];
const SOLUCION = ['fuera', 'valido', 'valido', 'fuera'];
const TEXTO = { '': 'Sin decidir', valido: 'Gol válido', fuera: 'Fuera de juego' };

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 46 — El veredicto del VAR',
    instr: 'Toca cada jugada para marcarla como gol válido o fuera de juego, según el reglamento. Cuando las cuatro estén decididas, pulsa Confirmar.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .fut-jugadas{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;max-width:320px;margin:6px auto 14px}
    .fut-jugada{padding:16px 8px;border-radius:10px;border:3px solid #cfd8c8;background:#1a2a20;color:#f4f0e0;font:700 .85rem system-ui,sans-serif;cursor:pointer;display:flex;flex-direction:column;gap:6px;align-items:center}
    .fut-jugada b{font:800 2rem Impact,"Arial Black",sans-serif}
    .fut-jugada.valido{border-color:#46c46a;background:#143a22}
    .fut-jugada.fuera{border-color:#e0443a;background:#3a1612}
    .fut-jugadas.ok .fut-jugada{box-shadow:0 0 8px #9be58a}
  `;
  ui.body.appendChild(style);

  const caja = document.createElement('div');
  caja.className = 'fut-jugadas';
  ui.body.appendChild(caja);

  const decision = ['', '', '', ''];
  let resuelto = false;

  function pintar() {
    caja.className = 'fut-jugadas' + (resuelto ? ' ok' : '');
    caja.innerHTML = '';
    JUGADAS.forEach((n, i) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'fut-jugada ' + decision[i];
      b.dataset.j = String(i);
      b.dataset.v = decision[i];
      b.setAttribute('aria-label', 'Jugada ' + n + ': ' + TEXTO[decision[i]]);
      b.innerHTML = '<b>' + n + '</b><span>' + TEXTO[decision[i]] + '</span>';
      b.addEventListener('click', () => {
        if (resuelto) return;
        decision[i] = decision[i] === '' ? 'valido' : decision[i] === 'valido' ? 'fuera' : '';
        ui.say('');
        pintar();
      });
      caja.appendChild(b);
    });
  }

  ui.button('Confirmar', 'primary', () => {
    if (resuelto) return;
    if (decision.some(d => d === '')) { ui.say('Faltan jugadas por decidir.', 'bad'); return; }
    if (decision.every((d, i) => d === SOLUCION[i])) {
      resuelto = true;
      pintar();
      ui.say('El árbitro asiente: «Cuatro de cuatro. Con vosotros no hacemos falta ni los jueces de línea». Os deja pasar al banquillo. Coged la carta 44.', 'ok');
    } else {
      ui.say('Alguna decisión no es correcta. Repasad el reglamento (carta 42): quien recibe tiene que estar más cerca de la portería que el penúltimo defensor Y que el balón.', 'bad');
    }
  });
  ui.button('Vaciar', '', () => { if (!resuelto) { decision.fill(''); ui.say(''); pintar(); } });

  pintar();
  return { close: ui.close };
}
