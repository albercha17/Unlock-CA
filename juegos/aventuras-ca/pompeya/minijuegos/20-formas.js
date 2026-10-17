// Carta 20 — La puerta del tablinum: poner cuatro figuras en el orden del camino del mosaico del atrio (cartas 14 a 17 juntas).
// Solución: triángulo, estrella, círculo, cruz.
import { openGame } from './ui.js';

const FORMAS = {
  circulo: ['Círculo', '<circle cx="20" cy="20" r="14"/>'],
  triangulo: ['Triángulo', '<polygon points="20,5 35,33 5,33"/>'],
  cuadrado: ['Cuadrado', '<rect x="7" y="7" width="26" height="26"/>'],
  rombo: ['Rombo', '<polygon points="20,4 35,20 20,36 5,20"/>'],
  estrella: ['Estrella', '<polygon points="20,4 24.5,15 36,15.5 27,23 30,35 20,28 10,35 13,23 4,15.5 15.5,15"/>'],
  cruz: ['Cruz', '<polygon points="15,5 25,5 25,15 35,15 35,25 25,25 25,35 15,35 15,25 5,25 5,15 15,15"/>']
};
const SOLUCION = ['triangulo', 'estrella', 'circulo', 'cruz'];

function svg(k) {
  return '<svg viewBox="0 0 40 40" aria-hidden="true" fill="currentColor">' + FORMAS[k][1] + '</svg>';
}

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 20 — La puerta del tablinum',
    instr: 'Toca las figuras para llenar los cuatro huecos, en orden. Toca un hueco lleno para vaciarlo.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .pom-huecos{display:flex;gap:10px;justify-content:center;margin:4px 0 14px}
    .pom-hueco{width:62px;height:62px;border-radius:10px;border:2px dashed #b8793c;background:rgba(40,16,6,.65);color:#f5c08a;display:flex;align-items:center;justify-content:center;padding:6px;cursor:pointer;box-shadow:inset 0 0 14px rgba(0,0,0,.7)}
    .pom-hueco svg{width:100%;height:100%}
    .pom-hueco.lleno{border-style:solid;background:rgba(120,60,24,.55)}
    .pom-hueco.ok{border-color:#9dffb0;color:#9dffb0}
    .pom-paneles{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;max-width:300px;margin:0 auto 12px}
    .pom-forma{aspect-ratio:1;border-radius:10px;border:2px solid #b8793c;background:linear-gradient(180deg,#8a5a2c,#4a2c14);color:#ffe2bd;padding:8px;cursor:pointer;box-shadow:0 3px 0 #2a1608}
    .pom-forma:active{transform:translateY(2px);box-shadow:0 1px 0 #2a1608}
    .pom-forma svg{width:100%;height:100%}
  `;
  ui.body.appendChild(style);

  const huecos = document.createElement('div');
  huecos.className = 'pom-huecos';
  const paneles = document.createElement('div');
  paneles.className = 'pom-paneles';
  ui.body.appendChild(huecos);
  ui.body.appendChild(paneles);

  let puestas = [];
  let resuelto = false;

  function pintar() {
    huecos.innerHTML = '';
    for (let i = 0; i < SOLUCION.length; i++) {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'pom-hueco' + (puestas[i] ? ' lleno' : '') + (resuelto ? ' ok' : '');
      b.dataset.i = String(i);
      b.dataset.k = puestas[i] || '';
      b.setAttribute('aria-label', 'Hueco ' + (i + 1) + ': ' + (puestas[i] ? FORMAS[puestas[i]][0] : 'vacío'));
      b.innerHTML = puestas[i] ? svg(puestas[i]) : '';
      b.addEventListener('click', () => {
        if (resuelto || !puestas[i]) return;
        puestas = puestas.slice(0, i);
        ui.say('');
        pintar();
      });
      huecos.appendChild(b);
    }
  }

  Object.keys(FORMAS).forEach(k => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'pom-forma';
    b.dataset.k = k;
    b.setAttribute('aria-label', FORMAS[k][0]);
    b.innerHTML = svg(k);
    b.addEventListener('click', () => {
      if (resuelto || puestas.length >= SOLUCION.length) return;
      puestas.push(k);
      ui.say('');
      pintar();
    });
    paneles.appendChild(b);
  });

  ui.button('Probar', 'primary', () => {
    if (resuelto) return;
    if (puestas.length < SOLUCION.length) { ui.say('Faltan figuras por poner.', 'bad'); return; }
    if (puestas.every((k, i) => k === SOLUCION[i])) {
      resuelto = true;
      pintar();
      ui.say('¡Clic! Las cuatro figuras se hunden en la madera y la puerta del tablinum se abre despacio. Coged la carta 26.', 'ok');
    } else {
      ui.say('La puerta no cede. Repasad el mosaico: seguid el camino desde la estrella de oro y fijaos solo en los medallones que toca.', 'bad');
    }
  });
  ui.button('Vaciar', '', () => { if (!resuelto) { puestas = []; ui.say(''); pintar(); } });

  pintar();
  return { close: ui.close };
}
