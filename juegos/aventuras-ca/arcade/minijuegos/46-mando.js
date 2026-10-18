// Carta 46 — El mando de la marquesina: pulsar, en orden, los botones del cartel con la luz amarilla encendida (cartas 40, 41 y 42 en fila).
// Solución: arriba, arriba, abajo, izquierda, A, B.
import { openGame } from './ui.js';

const NOMBRES = { arriba: 'Arriba', abajo: 'Abajo', izquierda: 'Izquierda', derecha: 'Derecha', a: 'A', b: 'B' };
const GIRO = { arriba: 0, derecha: 90, abajo: 180, izquierda: 270 };
const SOLUCION = ['arriba', 'arriba', 'abajo', 'izquierda', 'a', 'b'];

function icono(k) {
  if (k === 'a' || k === 'b') {
    return '<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="16" fill="currentColor"/><text x="20" y="27" text-anchor="middle" font-size="20" font-weight="800" fill="#1c0a30">' + NOMBRES[k] + '</text></svg>';
  }
  return '<svg viewBox="0 0 40 40" aria-hidden="true" fill="currentColor" style="transform:rotate(' + GIRO[k] + 'deg)"><polygon points="20,4 34,20 25,20 25,36 15,36 15,20 6,20"/></svg>';
}

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 46 — El mando de la marquesina',
    instr: 'Pulsa, en orden, solo los botones del cartel que tienen la luz amarilla encendida. Toca una casilla llena para vaciarla desde ahí.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .arc-secuencia{display:flex;gap:6px;justify-content:center;margin:4px 0 14px}
    .arc-paso{width:46px;height:46px;border-radius:8px;border:2px dashed #ff5ad8;background:rgba(10,4,24,.75);color:#ffe6fa;padding:6px;cursor:pointer;box-shadow:inset 0 0 12px rgba(0,0,0,.7)}
    .arc-paso svg{width:100%;height:100%}
    .arc-paso.lleno{border-style:solid;background:rgba(90,30,120,.55)}
    .arc-paso.ok{border-color:#9dffb0;color:#9dffb0}
    .arc-mando{display:flex;gap:22px;align-items:center;justify-content:center;margin:0 auto 12px}
    .arc-cruceta{display:grid;grid-template-columns:repeat(3,56px);grid-template-rows:repeat(3,56px);gap:6px}
    .arc-boton{border-radius:12px;border:2px solid #ff5ad8;background:linear-gradient(180deg,#5a2a8a,#2a1048);color:#ffe6fa;padding:8px;cursor:pointer;box-shadow:0 3px 0 #0d0518}
    .arc-boton:active{transform:translateY(2px);box-shadow:0 1px 0 #0d0518}
    .arc-boton svg{width:100%;height:100%}
    .arc-boton[data-k="arriba"]{grid-column:2;grid-row:1}
    .arc-boton[data-k="izquierda"]{grid-column:1;grid-row:2}
    .arc-boton[data-k="derecha"]{grid-column:3;grid-row:2}
    .arc-boton[data-k="abajo"]{grid-column:2;grid-row:3}
    .arc-ab{display:flex;gap:12px}
    .arc-ab .arc-boton{width:60px;height:60px;border-radius:50%;padding:6px}
  `;
  ui.body.appendChild(style);

  const secuencia = document.createElement('div');
  secuencia.className = 'arc-secuencia';
  const mando = document.createElement('div');
  mando.className = 'arc-mando';
  const cruceta = document.createElement('div');
  cruceta.className = 'arc-cruceta';
  const ab = document.createElement('div');
  ab.className = 'arc-ab';
  mando.appendChild(cruceta);
  mando.appendChild(ab);
  ui.body.appendChild(secuencia);
  ui.body.appendChild(mando);

  let puestas = [];
  let resuelto = false;

  function pintar() {
    secuencia.innerHTML = '';
    for (let i = 0; i < SOLUCION.length; i++) {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'arc-paso' + (puestas[i] ? ' lleno' : '') + (resuelto ? ' ok' : '');
      b.dataset.i = String(i);
      b.dataset.k = puestas[i] || '';
      b.setAttribute('aria-label', 'Paso ' + (i + 1) + ': ' + (puestas[i] ? NOMBRES[puestas[i]] : 'vacío'));
      b.innerHTML = puestas[i] ? icono(puestas[i]) : '';
      b.addEventListener('click', () => {
        if (resuelto || !puestas[i]) return;
        puestas = puestas.slice(0, i);
        ui.say('');
        pintar();
      });
      secuencia.appendChild(b);
    }
  }

  Object.keys(NOMBRES).forEach(k => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'arc-boton';
    b.dataset.k = k;
    b.setAttribute('aria-label', 'Botón ' + NOMBRES[k]);
    b.innerHTML = icono(k);
    b.addEventListener('click', () => {
      if (resuelto || puestas.length >= SOLUCION.length) return;
      puestas.push(k);
      ui.say('');
      pintar();
    });
    (k === 'a' || k === 'b' ? ab : cruceta).appendChild(b);
  });

  ui.button('Probar', 'primary', () => {
    if (resuelto) return;
    if (puestas.length < SOLUCION.length) { ui.say('Faltan botones por pulsar.', 'bad'); return; }
    if (puestas.every((k, i) => k === SOLUCION[i])) {
      resuelto = true;
      pintar();
      ui.say('¡CÓDIGO CORRECTO! Todas las bombillas del cartel parpadean a la vez y un panel se abre en la pared. Coged la carta 44.', 'ok');
    } else {
      ui.say('El cartel no responde. Juntad las tres piezas y fijaos solo en los botones con la luz amarilla encendida encima; se leen de izquierda a derecha.', 'bad');
    }
  });
  ui.button('Vaciar', '', () => { if (!resuelto) { puestas = []; ui.say(''); pintar(); } });

  pintar();
  return { close: ui.close };
}
