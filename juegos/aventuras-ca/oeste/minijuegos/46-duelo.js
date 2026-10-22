// Carta 46 — El duelo en corro (problema de Josefo): diecisiete pistoleros en corro, numerados desde el sombrero rojo; cae cada cuarto y la cuenta sigue
// desde el siguiente. Hay que sentarse en el asiento del último que queda en pie. El corro, en la carta 37; la regla, en las cartas 39 y 33.
// instancias_oeste.py, JOSEFO.
import { openGame } from './ui.js';
import { estilo } from './comun.js';

const D = /*DATOS*/{"n": 17, "sobrevive": 5, "caen": [4, 8, 12, 16, 3, 9, 14, 2, 10, 17, 7, 1, 13, 11, 15, 6]}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 46 — El duelo en corro', instr: 'Elegid el asiento donde queréis sentaros para ser el último que queda en pie. El corro está en la carta 37 y la regla de la cuenta, en las cartas 39 y 33.', ...opts });
  estilo('oe-due', `.due-corro{position:relative;width:min(84vw,320px);height:min(84vw,320px);margin:10px auto;border-radius:50%;background:radial-gradient(#6b4a2a 0 38%,transparent 39%)}.due-as{position:absolute;width:34px;height:34px;margin:-17px;border-radius:50%;border:3px solid #3a2412;background:#e6c88c;color:#3a2412;font:800 .8rem Georgia,serif;cursor:pointer;padding:0}.due-as.sel{background:#b03a2e;color:#fff;border-color:#f5d48a}`);
  let sel = 0, resuelto = false;
  const corro = document.createElement('div');
  corro.className = 'due-corro';
  const botones = [];
  for (let k = 0; k < D.n; k++) {
    const ang = -Math.PI / 2 + (2 * Math.PI * k) / D.n;
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'due-as';
    b.dataset.s = String(k + 1);
    b.textContent = String(k + 1);
    b.style.left = (50 + 42 * Math.cos(ang)) + '%';
    b.style.top = (50 + 42 * Math.sin(ang)) + '%';
    b.setAttribute('aria-label', 'Asiento ' + (k + 1));
    b.addEventListener('click', () => { if (resuelto) return; sel = k + 1; ui.say(''); pintar(); });
    corro.appendChild(b);
    botones.push(b);
  }
  ui.body.appendChild(corro);
  function pintar() { botones.forEach((b, k) => b.classList.toggle('sel', sel === k + 1)); }
  ui.button('Sentarse', 'primary', () => {
    if (resuelto) return;
    if (!sel) { ui.say('Elegid primero un asiento.', 'bad'); return; }
    if (sel !== D.sobrevive) {
      const ronda = D.caen.indexOf(sel) + 1;
      ui.say('Os sentáis en el ' + sel + ' y caéis en el disparo número ' + ronda + '. Otro asiento.', 'bad');
      return;
    }
    resuelto = true;
    ui.say('Sois el último en pie: el juez os da el botín y una llave. Coged la carta 56.', 'ok');
  });
  pintar();
  return { close: ui.close };
}
