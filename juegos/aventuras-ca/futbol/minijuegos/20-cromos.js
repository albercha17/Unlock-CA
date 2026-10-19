// Carta 20 — La convocatoria: elegir el dorsal del jugador que describe el míster (zurdo, de entre 1,75 m y 1,80 m, que no es defensa). Las fichas están en los reversos de los cromos (cartas 14 a 19).
// Solución: el dorsal 10 (Beto Pase).
import { openGame } from './ui.js';

const DORSALES = [1, 3, 4, 7, 9, 10];
const SOLUCION = 10;

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 20 — La convocatoria',
    instr: 'El míster busca a un jugador ZURDO, de MÁS de 1,75 m y MENOS de 1,80 m, que NO juega de defensa. Elige su dorsal: las fichas están por detrás de los cromos.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .fut-camisetas{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;max-width:320px;margin:6px auto 14px}
    .fut-dorsal{position:relative;aspect-ratio:1;border-radius:10px;border:3px solid #f5f0e0;background:repeating-linear-gradient(90deg,#c0282c 0 14px,#f7f2e6 14px 28px);color:#14231a;font:800 2rem Impact,"Arial Black",sans-serif;cursor:pointer;box-shadow:0 3px 0 #4a1010}
    .fut-dorsal span{display:block;background:rgba(247,242,230,.9);border-radius:6px;padding:0 8px;margin:0 auto;width:max-content}
    .fut-dorsal.sel{border-color:#f2c230;box-shadow:0 0 0 4px #f2c230,0 3px 0 #4a1010}
    .fut-camisetas.ok .fut-dorsal.sel{border-color:#46c46a;box-shadow:0 0 0 4px #46c46a}
  `;
  ui.body.appendChild(style);

  const rejilla = document.createElement('div');
  rejilla.className = 'fut-camisetas';
  ui.body.appendChild(rejilla);

  let elegido = null;
  let resuelto = false;

  function pintar() {
    rejilla.className = 'fut-camisetas' + (resuelto ? ' ok' : '');
    rejilla.innerHTML = '';
    DORSALES.forEach(d => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'fut-dorsal' + (elegido === d ? ' sel' : '');
      b.dataset.d = String(d);
      b.setAttribute('aria-label', 'Dorsal ' + d);
      b.innerHTML = '<span>' + d + '</span>';
      b.addEventListener('click', () => { if (!resuelto) { elegido = d; ui.say(''); pintar(); } });
      rejilla.appendChild(b);
    });
  }

  ui.button('Convocar', 'primary', () => {
    if (resuelto) return;
    if (elegido === null) { ui.say('Elegid primero un dorsal.', 'bad'); return; }
    if (elegido === SOLUCION) {
      resuelto = true;
      pintar();
      ui.say('«¡Ese es! Beto Pase, el centrocampista zurdo», exclama Don Remigio, y lo apunta en su hoja con un lápiz mordido. Os lleva a su pizarra táctica. Coged la carta 26.', 'ok');
    } else {
      ui.say('Don Remigio niega con la cabeza: ese no es. Dad la vuelta a los cromos y comprobad en cada ficha el pie, la altura y la posición: tienen que cumplirse las tres cosas a la vez.', 'bad');
    }
  });

  pintar();
  return { close: ui.close };
}
