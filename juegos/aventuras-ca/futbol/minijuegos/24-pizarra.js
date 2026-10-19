// Carta 24 — La pizarra: colocar a Los Rayos (1-2-2-1) con las pistas de las cartas 30 y 31.
// Solución: portero 1; defensa izquierda 6 y derecha 2; medio izquierda 11 y derecha 5; delantero 8.
import { openGame } from './ui.js';

const DORSALES = [1, 2, 5, 6, 8, 11];
const SOLUCION = { P: 1, DI: 6, DD: 2, MI: 11, MD: 5, DEL: 8 };
const NOMBRE = { DEL: 'Delantero', MI: 'Medio izquierda', MD: 'Medio derecha', DI: 'Defensa izquierda', DD: 'Defensa derecha', P: 'Portero' };
const FILAS = [['DEL'], ['MI', 'MD'], ['DI', 'DD'], ['P']];

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 24 — La pizarra',
    instr: 'Toca una ficha y luego el puesto donde juega. Toca un puesto ocupado para quitar la ficha. Izquierda y derecha, mirando hacia la portería rival.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .fut-campo{display:flex;flex-direction:column;gap:12px;max-width:300px;margin:4px auto 10px;padding:12px;border-radius:10px;border:3px solid #fff;background:linear-gradient(180deg,#2a6a3a,#1c4a2a)}
    .fut-fila{display:flex;justify-content:space-around}
    .fut-puesto{width:92px;min-height:62px;border-radius:10px;border:2px dashed #cfe8d0;background:rgba(0,0,0,.25);color:#fff;font:600 .68rem system-ui,sans-serif;padding:4px;cursor:pointer;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px}
    .fut-puesto b{font:800 1.5rem Impact,"Arial Black",sans-serif;color:#f2c230}
    .fut-puesto.lleno{border-style:solid;background:rgba(242,194,48,.18)}
    .fut-campo.ok .fut-puesto{border-color:#9be58a}
    .fut-banquillo{display:flex;gap:5px;justify-content:center;flex-wrap:wrap;margin:0 auto 10px;max-width:320px}
    .fut-ficha{width:42px;height:42px;border-radius:50%;border:3px solid #f7f2e6;background:#c0282c;color:#fff;font:800 1.1rem Impact,"Arial Black",sans-serif;cursor:pointer}
    .fut-ficha.sel{border-color:#f2c230;box-shadow:0 0 0 3px #f2c230}
    .fut-ficha:disabled{opacity:.25;cursor:default}
  `;
  ui.body.appendChild(style);

  const campo = document.createElement('div');
  campo.className = 'fut-campo';
  const banquillo = document.createElement('div');
  banquillo.className = 'fut-banquillo';
  ui.body.appendChild(campo);
  ui.body.appendChild(banquillo);

  const puesto = { P: null, DI: null, DD: null, MI: null, MD: null, DEL: null };
  let elegida = null;
  let resuelto = false;

  function pintar() {
    campo.className = 'fut-campo' + (resuelto ? ' ok' : '');
    campo.innerHTML = '';
    FILAS.forEach(fila => {
      const f = document.createElement('div');
      f.className = 'fut-fila';
      fila.forEach(s => {
        const b = document.createElement('button');
        b.type = 'button';
        b.className = 'fut-puesto' + (puesto[s] ? ' lleno' : '');
        b.dataset.s = s;
        b.dataset.d = puesto[s] ? String(puesto[s]) : '';
        b.setAttribute('aria-label', NOMBRE[s] + ': ' + (puesto[s] || 'vacío'));
        b.innerHTML = (puesto[s] ? '<b>' + puesto[s] + '</b>' : '') + '<span>' + NOMBRE[s] + '</span>';
        b.addEventListener('click', () => {
          if (resuelto) return;
          if (puesto[s]) { puesto[s] = null; elegida = null; }
          else if (elegida !== null) { puesto[s] = elegida; elegida = null; }
          ui.say('');
          pintar();
        });
        f.appendChild(b);
      });
      campo.appendChild(f);
    });
    banquillo.innerHTML = '';
    DORSALES.forEach(d => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'fut-ficha' + (elegida === d ? ' sel' : '');
      b.dataset.d = String(d);
      b.textContent = String(d);
      b.setAttribute('aria-label', 'Ficha del dorsal ' + d);
      b.disabled = Object.values(puesto).includes(d);
      b.addEventListener('click', () => { if (!resuelto) { elegida = d; ui.say(''); pintar(); } });
      banquillo.appendChild(b);
    });
  }

  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    if (Object.values(puesto).some(v => v === null)) { ui.say('Faltan jugadores por colocar: hay puestos vacíos.', 'bad'); return; }
    const bien = Object.keys(SOLUCION).filter(s => puesto[s] === SOLUCION[s]).length;
    if (bien === 6) {
      resuelto = true;
      pintar();
      ui.say('¡Esa es la alineación de Los Rayos! Don Remigio sonríe: «Ahora sé cómo jugarles». Os lleva a la sala del VAR. Coged la carta 28.', 'ok');
    } else {
      ui.say('Todavía no es la alineación del rival: hay ' + bien + ' de 6 jugadores bien colocados. Repasad las pistas de las dos cartas.', 'bad');
    }
  });
  ui.button('Vaciar', '', () => { if (!resuelto) { Object.keys(puesto).forEach(s => { puesto[s] = null; }); elegida = null; ui.say(''); pintar(); } });

  pintar();
  return { close: ui.close };
}
