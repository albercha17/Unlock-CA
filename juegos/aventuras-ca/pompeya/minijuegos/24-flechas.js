// Carta 24 — La verja del peristilo: cuatro flechas en el orden de las estatuas del fresco (cartas 30 a 33 juntas).
// Solución: abajo, abajo, derecha, arriba.
import { openGame } from './ui.js';

const DIRS = {
  arriba: ['Arriba', '0'],
  derecha: ['Derecha', '90'],
  abajo: ['Abajo', '180'],
  izquierda: ['Izquierda', '270']
};
const SOLUCION = ['abajo', 'abajo', 'derecha', 'arriba'];

function flecha(k) {
  return '<svg viewBox="0 0 40 40" aria-hidden="true" fill="currentColor" style="transform:rotate(' + DIRS[k][1] + 'deg)"><polygon points="20,4 34,20 25,20 25,36 15,36 15,20 6,20"/></svg>';
}

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 24 — La verja del peristilo',
    instr: 'Pulsa las flechas en orden para abrir la verja. Toca una casilla llena para vaciarla desde ahí.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .pom-secuencia{display:flex;gap:10px;justify-content:center;margin:4px 0 14px}
    .pom-paso{width:58px;height:58px;border-radius:10px;border:2px dashed #7e8a98;background:rgba(14,18,26,.7);color:#dfe8f2;display:flex;align-items:center;justify-content:center;padding:8px;cursor:pointer;box-shadow:inset 0 0 14px rgba(0,0,0,.7)}
    .pom-paso svg{width:100%;height:100%}
    .pom-paso.lleno{border-style:solid;background:rgba(70,84,100,.55)}
    .pom-paso.ok{border-color:#9dffb0;color:#9dffb0}
    .pom-cruceta{display:grid;grid-template-columns:repeat(3,64px);grid-template-rows:repeat(3,64px);gap:8px;justify-content:center;margin:0 auto 12px}
    .pom-flecha{border-radius:12px;border:2px solid #aab6c4;background:linear-gradient(180deg,#6e7a88,#363f4a);color:#f2f7fc;padding:10px;cursor:pointer;box-shadow:0 3px 0 #161b22}
    .pom-flecha:active{transform:translateY(2px);box-shadow:0 1px 0 #161b22}
    .pom-flecha svg{width:100%;height:100%}
    .pom-flecha[data-k="arriba"]{grid-column:2;grid-row:1}
    .pom-flecha[data-k="izquierda"]{grid-column:1;grid-row:2}
    .pom-flecha[data-k="derecha"]{grid-column:3;grid-row:2}
    .pom-flecha[data-k="abajo"]{grid-column:2;grid-row:3}
  `;
  ui.body.appendChild(style);

  const secuencia = document.createElement('div');
  secuencia.className = 'pom-secuencia';
  const cruceta = document.createElement('div');
  cruceta.className = 'pom-cruceta';
  ui.body.appendChild(secuencia);
  ui.body.appendChild(cruceta);

  let puestas = [];
  let resuelto = false;

  function pintar() {
    secuencia.innerHTML = '';
    for (let i = 0; i < SOLUCION.length; i++) {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'pom-paso' + (puestas[i] ? ' lleno' : '') + (resuelto ? ' ok' : '');
      b.dataset.i = String(i);
      b.dataset.k = puestas[i] || '';
      b.setAttribute('aria-label', 'Paso ' + (i + 1) + ': ' + (puestas[i] ? DIRS[puestas[i]][0] : 'vacío'));
      b.innerHTML = puestas[i] ? flecha(puestas[i]) : '';
      b.addEventListener('click', () => {
        if (resuelto || !puestas[i]) return;
        puestas = puestas.slice(0, i);
        ui.say('');
        pintar();
      });
      secuencia.appendChild(b);
    }
  }

  Object.keys(DIRS).forEach(k => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'pom-flecha';
    b.dataset.k = k;
    b.setAttribute('aria-label', DIRS[k][0]);
    b.innerHTML = flecha(k);
    b.addEventListener('click', () => {
      if (resuelto || puestas.length >= SOLUCION.length) return;
      puestas.push(k);
      ui.say('');
      pintar();
    });
    cruceta.appendChild(b);
  });

  ui.button('Probar', 'primary', () => {
    if (resuelto) return;
    if (puestas.length < SOLUCION.length) { ui.say('Faltan flechas por poner.', 'bad'); return; }
    if (puestas.every((k, i) => k === SOLUCION[i])) {
      resuelto = true;
      pintar();
      ui.say('Los cerrojos chasquean uno tras otro y la verja de hierro se abre hacia el jardín. Coged la carta 28.', 'ok');
    } else {
      ui.say('La verja no se mueve. Mirad el fresco entero: empezad por la estatua de la antorcha y seguid el sentido de las agujas del reloj.', 'bad');
    }
  });
  ui.button('Vaciar', '', () => { if (!resuelto) { puestas = []; ui.say(''); pintar(); } });

  pintar();
  return { close: ui.close };
}
