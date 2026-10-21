// Carta 59 — El calendario de piedra: clavar la clavija en el día del acertijo de Plinio (carta 65), contado a la romana como enseña el
// ejemplo del calendario (cartas 61 y 63).
import { openGame } from './ui.js';

const D = /*DATOS*/{"dia": 24}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 59 — El calendario de piedra', instr: 'Tocad un día de agosto para clavar la clavija y entregad el calendario al sacerdote.', ...opts });
  const style = document.createElement('style');
  style.textContent = `
    .pom-cal{display:grid;grid-template-columns:repeat(7,1fr);gap:4px;max-width:320px;margin:6px auto;padding:10px;border-radius:8px;background:#9a948a}
    .pom-dia{aspect-ratio:1;border-radius:4px;border:2px solid #5a564e;background:#d4d0c4;cursor:pointer;font:700 .85rem Georgia,serif;color:#2a2a26;padding:0}
    .pom-dia.sel{background:#c8a050;color:#fff}`;
  ui.body.appendChild(style);
  const cal = document.createElement('div'); cal.className = 'pom-cal'; ui.body.appendChild(cal);
  let dia = null, resuelto = false;
  for (let d = 1; d <= 31; d++) {
    const b = document.createElement('button'); b.type = 'button'; b.className = 'pom-dia'; b.dataset.d = String(d); b.textContent = String(d);
    b.addEventListener('click', () => { if (resuelto) return; dia = d; cal.querySelectorAll('.pom-dia').forEach(x => x.classList.toggle('sel', x === b)); ui.say(''); });
    cal.appendChild(b);
  }
  ui.button('Entregar al sacerdote', 'primary', () => {
    if (resuelto) return;
    if (dia === null) { ui.say('Clavad la clavija en algún día.', 'bad'); return; }
    if (dia === D.dia) { resuelto = true; ui.say('El sacerdote asiente: «Ese es el día». Os da la llave de la puerta del mar... y en ese momento el monte revienta. Coged la carta 64.', 'ok'); }
    else ui.say('El sacerdote frunce el ceño: ese no es el día. Los romanos cuentan hacia atrás y de una forma especial (cartas 61, 63 y 65).', 'bad');
  });
  return { close: ui.close };
}
