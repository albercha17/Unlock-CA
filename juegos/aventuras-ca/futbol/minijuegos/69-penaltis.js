// Carta 69 — La tanda de penaltis: marcar cinco penaltis contra un portero con manías (informe del entrenador, carta 70) chutando al menos una vez al centro.
// El portero se lanza a la izquierda en el primero y, en los demás, al lado al que chutó el delantero en el penalti anterior (si fue al centro, se queda en el centro).
// Es gol si el delantero chuta a un lado distinto de aquel al que se lanza.
import { openGame } from './ui.js';

const TOTAL = 5;
const LADOS = { izquierda: 'Izquierda', centro: 'Centro', derecha: 'Derecha' };

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 69 — La tanda de penaltis',
    instr: 'Elige hacia dónde chutar cada penalti. El portero decide según el informe del entrenador. Hay que marcar los cinco y chutar al menos una vez al centro.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .fut-porteria{display:grid;grid-template-columns:repeat(3,1fr);max-width:300px;margin:6px auto 8px;border:4px solid #f4f0e0;border-bottom-width:6px;background:repeating-linear-gradient(45deg,#2a3a30 0 6px,#1c2a22 6px 12px)}
    .fut-zona{height:70px;display:flex;align-items:center;justify-content:center;font:800 .8rem system-ui,sans-serif;color:#cfd8c8;border-left:2px solid #f4f0e0}
    .fut-zona:first-child{border-left:0}
    .fut-zona.gol{background:rgba(70,196,106,.55);color:#fff}
    .fut-zona.parada{background:rgba(224,68,58,.55);color:#fff}
    .fut-balones{display:flex;gap:8px;justify-content:center;margin:0 0 10px}
    .fut-balon{width:30px;height:30px;border-radius:50%;border:3px solid #f4f0e0;background:#1a2a20}
    .fut-balon.gol{background:#46c46a}
    .fut-tiro{display:flex;gap:8px;justify-content:center;margin-bottom:8px}
    .fut-tiro button{flex:1;max-width:100px;padding:12px 6px;border-radius:8px;border:2px solid #f2c230;background:#1f3a28;color:#f2c230;font:800 .9rem system-ui,sans-serif;cursor:pointer}
  `;
  ui.body.appendChild(style);

  const porteria = document.createElement('div');
  porteria.className = 'fut-porteria';
  const balones = document.createElement('div');
  balones.className = 'fut-balones';
  const tiro = document.createElement('div');
  tiro.className = 'fut-tiro';
  ui.body.appendChild(porteria);
  ui.body.appendChild(balones);
  ui.body.appendChild(tiro);

  let tiros = [];
  let ultimo = null;           // { tiro, salto }
  let resuelto = false;

  function pintar() {
    porteria.innerHTML = '';
    Object.keys(LADOS).forEach(l => {
      const z = document.createElement('div');
      z.className = 'fut-zona' + (ultimo && ultimo.tiro === l ? (ultimo.gol ? ' gol' : '') : '') + (ultimo && ultimo.salto === l && !ultimo.gol ? ' parada' : '');
      z.dataset.z = l;
      z.textContent = ultimo ? (ultimo.salto === l ? 'PORTERO' : ultimo.tiro === l ? 'BALÓN' : '') : LADOS[l];
      porteria.appendChild(z);
    });
    balones.innerHTML = '';
    for (let i = 0; i < TOTAL; i++) {
      const b = document.createElement('div');
      b.className = 'fut-balon' + (i < tiros.length ? ' gol' : '');
      balones.appendChild(b);
    }
  }

  function chutar(l) {
    if (resuelto) return;
    const salto = tiros.length === 0 ? 'izquierda' : tiros[tiros.length - 1];
    const gol = l !== salto;
    ultimo = { tiro: l, salto, gol };
    if (!gol) {
      tiros = [];
      pintar();
      ui.say('¡Paradón! El portero se había lanzado justo ahí (a ' + LADOS[salto].toLowerCase() + '). Se repite la tanda desde el primer penalti: repasad el informe del entrenador.', 'bad');
      return;
    }
    tiros.push(l);
    pintar();
    if (tiros.length < TOTAL) { ui.say('¡GOOOL! Penalti ' + tiros.length + ' de ' + TOTAL + '. El portero se lanzó a ' + LADOS[salto].toLowerCase() + '.', ''); return; }
    if (!tiros.includes('centro')) {
      tiros = [];
      pintar();
      ui.say('Cinco goles, pero no habéis chutado ni una vez al centro. Se repite la tanda: el entrenador quiere ver un penalti por el centro.', 'bad');
      return;
    }
    resuelto = true;
    ui.say('¡Cinco de cinco! El estadio estalla y el Estrella gana la final por penaltis. En la ceremonia, Don Remigio levanta la Copa de cristal. Coged la carta 82.', 'ok');
  }

  Object.keys(LADOS).forEach(l => {
    const b = document.createElement('button');
    b.type = 'button';
    b.dataset.l = l;
    b.textContent = LADOS[l];
    b.setAttribute('aria-label', 'Chutar a la ' + LADOS[l].toLowerCase());
    b.addEventListener('click', () => chutar(l));
    tiro.appendChild(b);
  });

  pintar();
  return { close: ui.close };
}
