// Carta 47 — Balanza de Maat: igualar el peso del corazón (17 deben, dato del papiro del juicio, carta 52).
import { openGame } from './ui.js';

const PESO_CORAZON = 17;
const PESAS = [3, 4, 6, 9, 11];
const IMG = './img/ui/';
const MUELLE = 'cubic-bezier(.3,1.5,.5,1)';

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 47 — Balanza de Maat',
    instr: 'Coloca pesas en el plato derecho hasta equilibrar el corazón. Toca una pesa para ponerla o quitarla.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .far-bal{position:relative;width:100%;max-width:330px;height:310px;margin:0 auto 10px;border-radius:10px;border:3px solid #6b5320;overflow:hidden;background:radial-gradient(ellipse at 50% 30%,rgba(255,210,122,.16),transparent 65%),linear-gradient(rgba(20,12,4,.72),rgba(20,12,4,.9)),url(${IMG}piedra.jpg) center/cover;box-shadow:inset 0 0 28px rgba(0,0,0,.8)}
    .far-bal img{position:absolute;display:block;mix-blend-mode:screen;pointer-events:none;object-fit:contain}
    .far-bal-pilar{left:50%;bottom:4px;height:255px;transform:translateX(-50%)}
    .far-bal-brazo{left:50%;top:52px;width:250px;margin-left:-125px;transition:transform .7s ${MUELLE}}
    .far-bal-plato{width:104px;transition:left .7s ${MUELLE},top .7s ${MUELLE}}
    .far-bal-corazon{width:50px;transition:left .7s ${MUELLE},top .7s ${MUELLE}}
    .far-bal-carga{position:absolute;display:flex;gap:2px;align-items:flex-end;justify-content:center;width:100px;transition:left .7s ${MUELLE},top .7s ${MUELLE}}
    .far-bal-carga img{position:static;width:30px}
    .far-bal-ok{position:absolute;left:0;right:0;top:6px;text-align:center;color:#9dffb0;font-weight:700;font-size:.85rem;letter-spacing:.12em;text-shadow:0 0 8px #3fbf6a;opacity:0;transition:opacity .4s}
    .far-bal-ok.si{opacity:1}
    .far-pesa{position:relative;width:60px;height:68px;border:0;padding:0;background:url(${IMG}balanza-b/pesa.jpg) center/contain no-repeat,#000;background-blend-mode:screen;color:#fff;font:700 1.05rem system-ui,sans-serif;text-shadow:0 1px 3px #000,0 0 6px #000;cursor:pointer;border-radius:8px;filter:brightness(.8) saturate(.8);transition:transform .15s,filter .15s}
    .far-pesa.puesta{filter:none;transform:translateY(-4px);box-shadow:0 0 0 2px #ffd27a,0 0 14px rgba(255,210,122,.6)}
    .far-pesa:disabled{cursor:default}
  `;
  ui.body.appendChild(style);

  const bal = document.createElement('div');
  bal.className = 'far-bal';
  const mk = (clase, src) => {
    const im = document.createElement('img');
    im.className = clase;
    im.alt = '';
    im.src = IMG + src;
    bal.appendChild(im);
    return im;
  };
  mk('far-bal-pilar', 'balanza-a/pilar.jpg');
  const brazo = mk('far-bal-brazo', 'balanza-a/brazo.jpg');
  const platoI = mk('far-bal-plato', 'balanza-a/plato.jpg');
  const platoD = mk('far-bal-plato', 'balanza-a/plato.jpg');
  const corazon = mk('far-bal-corazon', 'balanza-b/corazon.jpg');
  const carga = document.createElement('div');
  carga.className = 'far-bal-carga';
  const ok = document.createElement('div');
  ok.className = 'far-bal-ok';
  ok.textContent = 'EQUILIBRIO';
  bal.append(carga, ok);
  const kg = document.createElement('div');
  kg.style.cssText = 'display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-bottom:8px';
  ui.body.append(bal, kg);

  const elegidas = new Set();
  let resuelto = false;
  function total() { return [...elegidas].reduce((a, b) => a + b, 0); }

  function pintar() {
    const w = bal.clientWidth || 330;
    const diff = total() - PESO_CORAZON;
    const ang = diff === 0 ? 0 : Math.max(-9, Math.min(9, diff * 2.2));
    const rad = ang * Math.PI / 180;
    const px = w / 2;
    const py = 52 + (brazo.clientHeight || 40) / 2;
    const L = 110;
    const izq = [px - L * Math.cos(rad), py - L * Math.sin(rad)];
    const der = [px + L * Math.cos(rad), py + L * Math.sin(rad)];
    brazo.style.transform = `rotate(${ang}deg)`;
    const pon = (el, p, dx, dy) => { el.style.left = (p[0] - dx) + 'px'; el.style.top = (p[1] + dy) + 'px'; };
    pon(platoI, izq, 52, 4);
    pon(platoD, der, 52, 4);
    pon(corazon, izq, 25, 80);
    pon(carga, der, 50, 98);
    carga.innerHTML = '';
    [...elegidas].sort((a, b) => a - b).forEach(p => {
      const im = document.createElement('img');
      im.alt = '';
      im.src = IMG + 'balanza-b/pesa.jpg';
      im.style.height = (16 + p * 1.4) + 'px';
      carga.appendChild(im);
    });
    ok.classList.toggle('si', diff === 0 && elegidas.size > 0);
  }

  PESAS.forEach(p => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'far-pesa';
    b.textContent = p;
    b.addEventListener('click', () => {
      if (resuelto) return;
      if (elegidas.has(p)) { elegidas.delete(p); b.classList.remove('puesta'); } else { elegidas.add(p); b.classList.add('puesta'); }
      ui.say('');
      pintar();
      if (total() === PESO_CORAZON) {
        resuelto = true;
        ui.say('¡Equilibrio perfecto! Maat aprueba el corazón y la puerta de la sala se abre. Coged la carta 63.', 'ok');
        kg.querySelectorAll('button').forEach(x => { x.disabled = true; });
      }
    });
    kg.appendChild(b);
  });

  pintar();
  brazo.addEventListener('load', pintar);
  return { close: ui.close };
}
