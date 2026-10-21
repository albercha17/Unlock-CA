// Carta 46 — La balanza romana: el cofre cuelga a una muesca del eje; el contrapeso se mueve por las muescas del brazo. Equilibrio:
// peso del cofre × 1 = contrapeso × muesca. Los pesos salen de las pesadas (carta 43) y el recibo (carta 45).
import { openGame } from './ui.js';

const D = /*DATOS*/{"muesca": 10}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 46 — La balanza romana', instr: 'Moved el contrapeso por las muescas del brazo y soltad la balanza. Si queda en equilibrio, el pestillo del cofre se suelta.', ...opts });
  const style = document.createElement('style');
  style.textContent = `
    .pom-brazo{position:relative;height:70px;max-width:330px;margin:20px auto 6px;border-bottom:8px solid #8a6a3a}
    .pom-muesca{position:absolute;bottom:-26px;width:22px;margin-left:-11px;text-align:center;font:700 .7rem Georgia,serif;color:#f6e4b8}
    .pom-pondus{position:absolute;bottom:-4px;width:34px;height:40px;margin-left:-17px;border-radius:50% 50% 8px 8px;background:radial-gradient(circle at 40% 30%,#e8c870,#8a6a2a);transition:left .2s}
    .pom-cofre{position:absolute;left:0;bottom:-46px;width:40px;height:34px;background:#6a4a2a;border:2px solid #3a2410}
    .pom-giro{display:flex;gap:10px;justify-content:center;margin-top:44px}
    .pom-giro button{padding:10px 18px;border-radius:8px;border:2px solid #c8a050;background:#2a1a10;color:#f6e4b8;font:800 1.1rem system-ui;cursor:pointer}`;
  ui.body.appendChild(style);
  const brazo = document.createElement('div'); brazo.className = 'pom-brazo';
  brazo.innerHTML = '<div class="pom-cofre"></div>';
  for (let m = 1; m <= 12; m++) { const s = document.createElement('span'); s.className = 'pom-muesca'; s.style.left = (8 + m * 7.4) + '%'; s.textContent = String(m); brazo.appendChild(s); }
  const pondus = document.createElement('i'); pondus.className = 'pom-pondus'; brazo.appendChild(pondus);
  const giro = document.createElement('div'); giro.className = 'pom-giro';
  ui.body.append(brazo, giro);
  let muesca = 1, resuelto = false;
  const pintar = () => { pondus.style.left = (8 + muesca * 7.4) + '%'; brazo.dataset.m = String(muesca); };
  [['◀', -1], ['▶', 1]].forEach(([t, d]) => {
    const b = document.createElement('button'); b.type = 'button'; b.textContent = t; b.dataset.d = String(d);
    b.addEventListener('click', () => { if (!resuelto) { muesca = Math.min(12, Math.max(1, muesca + d)); ui.say(''); pintar(); } });
    giro.appendChild(b);
  });
  ui.button('Soltar la balanza', 'primary', () => {
    if (resuelto) return;
    if (muesca === D.muesca) { resuelto = true; ui.say('El brazo queda quieto, perfectamente horizontal, y el pestillo del cofre salta. Dentro hay una lámpara de aceite. Coged la carta 56.', 'ok'); }
    else ui.say('El brazo se inclina y se queda torcido. Calculad bien lo que pesa el cofre (cartas 43 y 45).', 'bad');
  });
  pintar();
  return { close: ui.close };
}
