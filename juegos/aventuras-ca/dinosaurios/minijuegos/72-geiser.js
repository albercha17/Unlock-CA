// Carta 72 — Válvulas del géiser: tres válvulas (0 a 6) y tres manómetros. Presiones: 2A+B, B+C y A+2C.
// Presión segura (carta 76): 7, 5 y 11. Solución única: A=3, B=1, C=4.
import { openGame } from './ui.js';

const MAX = 6;
const OBJETIVO = [7, 5, 11];
const LECTURA = (a, b, c) => [2 * a + b, b + c, a + 2 * c];
const ESCALA = 20;
const IMG = './img/ui/';

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 72 — Válvulas del géiser',
    instr: 'Gira las tres válvulas con + y −. Cada manómetro mide una mezcla distinta de ellas. Deja la presión segura en los tres.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .gei-panel{max-width:350px;margin:0 auto 8px;padding:10px 8px;border-radius:12px;border:3px solid #2a1a10;background:linear-gradient(rgba(30,10,2,.4),rgba(30,10,2,.65)),url(${IMG}roca-cueva.jpg) center/cover;box-shadow:inset 0 0 28px rgba(0,0,0,.8)}
    .gei-fila{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:10px}
    .gei-manometro{position:relative;aspect-ratio:1}
    .gei-manometro img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;mix-blend-mode:screen}
    .gei-aguja{position:absolute;left:50%;top:50%;width:3px;height:36%;margin-left:-1.5px;background:linear-gradient(180deg,#ff4a3a,#7a1008);border-radius:2px;transform-origin:50% 100%;transform:translateY(-100%) rotate(-135deg);transition:transform .5s cubic-bezier(.3,1.4,.5,1);box-shadow:0 0 5px rgba(255,80,60,.8)}
    .gei-eje{position:absolute;left:50%;top:50%;width:12px;height:12px;margin:-6px 0 0 -6px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#e7c27a,#6a4a14)}
    .gei-lec{position:absolute;left:0;right:0;bottom:12%;text-align:center;font:800 .95rem Georgia,serif;color:#2a1600;text-shadow:0 1px 0 rgba(255,255,255,.4)}
    .gei-valv{display:flex;flex-direction:column;align-items:center;gap:4px}
    .gei-rueda{position:relative;width:100%;aspect-ratio:1}
    .gei-rueda img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;mix-blend-mode:screen;transition:transform .35s ease}
    .gei-rueda b{position:absolute;left:0;right:0;top:50%;transform:translateY(-50%);text-align:center;font:800 1.2rem Georgia,serif;color:#fff;text-shadow:0 0 6px #000,0 0 3px #000}
    .gei-mandos{display:flex;gap:6px}
    .gei-mandos button{width:36px;height:34px;border-radius:8px;border:1px solid rgba(181,227,91,.6);background:linear-gradient(180deg,#6f8d45,#3d5a24);color:#f2ffd6;font:800 1.2rem system-ui,sans-serif;cursor:pointer}
    .gei-mandos button:disabled{opacity:.4;cursor:default}
  `;
  ui.body.appendChild(style);

  const panel = document.createElement('div');
  panel.className = 'gei-panel';
  const filaM = document.createElement('div');
  filaM.className = 'gei-fila';
  const filaV = document.createElement('div');
  filaV.className = 'gei-fila';
  panel.append(filaM, filaV);
  ui.body.appendChild(panel);

  const val = [0, 0, 0];
  let resuelto = false;
  const agujas = [], lecs = [], ruedas = [], numeros = [], menos = [], mas = [];

  for (let i = 0; i < 3; i++) {
    const m = document.createElement('div');
    m.className = 'gei-manometro';
    m.dataset.m = String(i);
    m.innerHTML = '<img alt="" src="' + IMG + 'manometro.jpg"><div class="gei-aguja"></div><div class="gei-eje"></div><div class="gei-lec">0</div>';
    agujas.push(m.querySelector('.gei-aguja'));
    lecs.push(m.querySelector('.gei-lec'));
    filaM.appendChild(m);

    const v = document.createElement('div');
    v.className = 'gei-valv';
    v.dataset.v = String(i);
    v.innerHTML = '<div class="gei-rueda"><img alt="" src="' + IMG + 'valvula.jpg"><b>0</b></div><div class="gei-mandos"><button type="button" class="gei-menos" aria-label="Válvula ' + (i + 1) + ' menos">−</button><button type="button" class="gei-mas" aria-label="Válvula ' + (i + 1) + ' más">+</button></div>';
    ruedas.push(v.querySelector('.gei-rueda img'));
    numeros.push(v.querySelector('.gei-rueda b'));
    menos.push(v.querySelector('.gei-menos'));
    mas.push(v.querySelector('.gei-mas'));
    menos[i].addEventListener('click', () => { if (!resuelto && val[i] > 0) { val[i]--; ui.say(''); pintar(); } });
    mas[i].addEventListener('click', () => { if (!resuelto && val[i] < MAX) { val[i]++; ui.say(''); pintar(); } });
    filaV.appendChild(v);
  }

  function pintar() {
    const lec = LECTURA(...val);
    for (let i = 0; i < 3; i++) {
      agujas[i].style.transform = 'translateY(-100%) rotate(' + (-135 + Math.min(lec[i], ESCALA) / ESCALA * 270) + 'deg)';
      lecs[i].textContent = String(lec[i]);
      ruedas[i].style.transform = 'rotate(' + (val[i] * 60) + 'deg)';
      numeros[i].textContent = String(val[i]);
      menos[i].disabled = val[i] === 0;
      mas[i].disabled = val[i] === MAX;
    }
  }

  ui.button('Comprobar presión', 'primary', () => {
    if (resuelto) return;
    const lec = LECTURA(...val);
    if (lec.every((x, i) => x === OBJETIVO[i])) {
      resuelto = true;
      ui.say('Los tres manómetros marcan la presión segura y el géiser se calma con un largo suspiro de vapor. El núcleo queda al alcance. Coged la carta 82.', 'ok');
    } else {
      ui.say('Los manómetros no marcan la presión segura. Fijaos en cómo cambia cada uno al mover una sola válvula.', 'bad');
    }
  });

  pintar();
  return { close: ui.close };
}
