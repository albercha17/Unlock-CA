// Carta 95 — Consola del Cronoportal: tocar los cristales en el orden del guardián (carta 44) con los colores del papiro (carta 15).
// Orden: Nilo (azul), Sol (amarillo), Sangre (rojo), Papiro (verde), Sol (amarillo).
import { openGame } from './ui.js';

const COLORES = {
  amarillo: '#f2c94c',
  azul: '#2f80ed',
  verde: '#27ae60',
  rojo: '#eb5757'
};
const SECUENCIA = ['azul', 'amarillo', 'rojo', 'verde', 'amarillo'];

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 95 — Consola del Cronoportal',
    instr: 'Toca los cuatro cristales en el orden correcto para despertar el Ojo.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .far-cristales{display:grid;grid-template-columns:repeat(2,96px);gap:14px;justify-content:center;margin:6px 0 14px}
    .far-cristal{width:96px;height:96px;border-radius:50%;border:4px solid rgba(255,255,255,.35);cursor:pointer;box-shadow:0 6px 18px rgba(0,0,0,.5);transition:transform .1s,filter .1s}
    .far-cristal:active,.far-cristal.on{transform:scale(.94);filter:brightness(1.5)}
    .far-cristal:disabled{opacity:.5;cursor:not-allowed}
    .far-puntos{display:flex;gap:8px;justify-content:center;margin-bottom:6px}
    .far-puntos i{width:14px;height:14px;border-radius:50%;background:#3a4a5c}
    .far-puntos i.hecho{background:#ffd27a}
  `;
  ui.body.appendChild(style);

  const puntos = document.createElement('div');
  puntos.className = 'far-puntos';
  SECUENCIA.forEach(() => puntos.appendChild(document.createElement('i')));
  const grid = document.createElement('div');
  grid.className = 'far-cristales';
  ui.body.append(puntos, grid);

  let pos = 0;
  let resuelto = false;

  function pintarPuntos() {
    [...puntos.children].forEach((p, i) => p.classList.toggle('hecho', i < pos));
  }

  Object.keys(COLORES).forEach(nombre => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'far-cristal';
    b.style.background = COLORES[nombre];
    b.setAttribute('aria-label', 'Cristal ' + nombre);
    b.dataset.color = nombre;
    b.addEventListener('click', () => {
      if (resuelto) return;
      b.classList.add('on');
      setTimeout(() => b.classList.remove('on'), 150);
      if (nombre === SECUENCIA[pos]) {
        pos++;
        pintarPuntos();
        if (pos === SECUENCIA.length) {
          resuelto = true;
          ui.say('¡El Ojo de Horus brilla y el Cronoportal se enciende! Coged la carta 99.', 'ok');
          grid.querySelectorAll('button').forEach(x => { x.disabled = true; });
        } else {
          ui.say('');
        }
      } else {
        pos = 0;
        pintarPuntos();
        ui.say('El cristal se apaga. Empezad de nuevo.', 'bad');
      }
    });
    grid.appendChild(b);
  });

  pintarPuntos();
  return { close: ui.close };
}
