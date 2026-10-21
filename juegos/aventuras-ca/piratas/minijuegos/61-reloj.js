// Carta 61 — El reloj de bitácora: ponerlo a la hora del diario de la capitana (carta 67), pasando la guardia y las campanadas a horas
// con los cuadros de las cartas 63 y 65. Hora de herramientas/instancias_ampliacion.py.
import { openGame } from './ui.js';

const R = /*DATOS*/{"hora": [14, 30]}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 61 — El reloj de bitácora',
    instr: 'Adelantad o atrasad el reloj de media en media hora (es de 24 horas) hasta la hora del diario de la capitana y pulsad «Esta es la hora».',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .pir-esfera{position:relative;width:min(70vw,240px);aspect-ratio:1;margin:6px auto;border-radius:50%;
      background:radial-gradient(circle,#f6ead0 0 62%,#c89a3a 63% 67%,#6a4a1a 68% 72%,transparent 73%)}
    .pir-esfera span{position:absolute;transform:translate(-50%,-50%);font:700 .72rem Georgia,serif;color:#3a2410}
    .pir-aguja{position:absolute;left:50%;bottom:50%;transform-origin:50% 100%;border-radius:4px}
    .pir-aguja.h{width:8px;margin-left:-4px;height:30%;background:#3a2410}
    .pir-aguja.m{width:4px;margin-left:-2px;height:40%;background:#9a2a1a}
    .pir-centro{position:absolute;left:50%;top:50%;width:14px;height:14px;margin:-7px;border-radius:50%;background:#c89a3a}
    .pir-digital{text-align:center;font:800 1.6rem Georgia,serif;color:#f6e4b8;margin:4px 0 8px}
    .pir-mandos{display:flex;gap:8px;justify-content:center}
    .pir-mandos button{padding:10px 14px;border-radius:8px;border:2px solid #e8b84a;background:#173a46;color:#f6e7b8;font:700 .9rem system-ui;cursor:pointer}
  `;
  ui.body.appendChild(style);
  const esfera = document.createElement('div');
  esfera.className = 'pir-esfera';
  for (let h = 0; h < 24; h += 2) {
    const a = h / 24 * 2 * Math.PI - Math.PI / 2;
    const s = document.createElement('span');
    s.textContent = String(h);
    s.style.left = (50 + 52 * Math.cos(a)) + '%';
    s.style.top = (50 + 52 * Math.sin(a)) + '%';
    esfera.appendChild(s);
  }
  const ah = document.createElement('i'); ah.className = 'pir-aguja h';
  const am = document.createElement('i'); am.className = 'pir-aguja m';
  const ce = document.createElement('i'); ce.className = 'pir-centro';
  esfera.append(ah, am, ce);
  const dig = document.createElement('p');
  dig.className = 'pir-digital';
  const mandos = document.createElement('div');
  mandos.className = 'pir-mandos';
  ui.body.append(esfera, dig, mandos);

  let medias = 0, resuelto = false;      // medias horas desde las 00:00
  function pintar() {
    const h = Math.floor(medias / 2), m = (medias % 2) * 30;
    ah.style.transform = 'rotate(' + (medias / 48 * 360) + 'deg)';
    am.style.transform = 'rotate(' + (m / 60 * 360) + 'deg)';
    dig.textContent = String(h).padStart(2, '0') + ':' + String(m).padStart(2, '0');
    dig.dataset.h = String(h);
    dig.dataset.m = String(m);
  }
  [['−2 h', -4], ['−½ h', -1], ['+½ h', 1], ['+2 h', 4]].forEach(([t, d]) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.textContent = t;
    b.dataset.d = String(d);
    b.addEventListener('click', () => { if (!resuelto) { medias = (medias + d + 48) % 48; ui.say(''); pintar(); } });
    mandos.appendChild(b);
  });

  ui.button('Esta es la hora', 'primary', () => {
    if (resuelto) return;
    if (medias === R.hora[0] * 2 + R.hora[1] / 30) {
      resuelto = true;
      ui.say('¡Justo a tiempo! La marea baja, aparece un canal entre los arrecifes y La Gaviota se cuela hasta la playa. Coged la carta 58.', 'ok');
    } else {
      ui.say('A esa hora el mar rompe sobre las rocas: no se puede pasar. Mirad la guardia y las campanadas del diario (carta 67) con los cuadros (cartas 63 y 65).', 'bad');
    }
  });
  pintar();
  return { close: ui.close };
}
