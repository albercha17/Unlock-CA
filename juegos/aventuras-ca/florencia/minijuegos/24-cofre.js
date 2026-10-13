// Carta 24 — Cofre del maestro: teclado de 4 cifras. Código: 2759 (cuaderno en espejo, carta 26).
import { openGame } from './ui.js';

const CODE = '2759';

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 24 — Cofre del maestro',
    instr: 'Pon las cuatro cifras de la combinación en las ruedas del cofre.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .far-ruedas{display:flex;gap:10px;justify-content:center;margin-bottom:14px;background:#2a1a0c;border:3px solid #8a5a2a;border-radius:12px;padding:12px 8px}
    .far-rueda{width:54px;height:72px;border-radius:8px;background:linear-gradient(180deg,#d9b46a,#a87a35 50%,#d9b46a);border:2px solid #5a3a14;color:#2a1600;font-size:2.2rem;font-weight:800;display:flex;align-items:center;justify-content:center;box-shadow:inset 0 0 8px rgba(0,0,0,.35)}
  `;
  ui.body.appendChild(style);

  const ruedas = document.createElement('div');
  ruedas.className = 'far-ruedas';
  const celdas = [0, 1, 2, 3].map(() => {
    const r = document.createElement('div');
    r.className = 'far-rueda';
    ruedas.appendChild(r);
    return r;
  });
  const pad = document.createElement('div');
  pad.className = 'far-keypad';
  ui.body.append(ruedas, pad);

  let entered = '';
  let resuelto = false;
  const render = () => { celdas.forEach((c, i) => { c.textContent = entered[i] || '·'; }); };

  ['1', '2', '3', '4', '5', '6', '7', '8', '9', '⌫', '0', '✓'].forEach(k => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'far-key';
    b.textContent = k;
    b.addEventListener('click', () => {
      if (resuelto) return;
      if (k === '⌫') { entered = entered.slice(0, -1); render(); return; }
      if (k === '✓') { check(); return; }
      if (entered.length < 4) { entered += k; render(); }
    });
    pad.appendChild(b);
  });

  function check() {
    if (entered === CODE) {
      resuelto = true;
      ui.say('Las cuatro ruedas encajan y la tapa se abre con un chasquido. Dentro hay un disco de cobre y un pergamino. Coged la carta 30.', 'ok');
      pad.querySelectorAll('button').forEach(b => { b.disabled = true; });
    } else {
      ui.say('El cofre no se abre. Leed con calma el cuaderno de Leonardo: está escrito al revés.', 'bad');
      entered = '';
      render();
    }
  }

  render();
  return { close: ui.close };
}
