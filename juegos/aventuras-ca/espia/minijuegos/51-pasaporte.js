// Carta 51 — Los pasaportes falsos: en la zona de lectura mecánica de cada pasaporte falta el dígito de control del número del documento (un «?»). Hay que
// calcularlo con la regla del aduanero (pesos 7-3-1). Los pasaportes, en las cartas 61 y 63 (dos mitades); la regla, en la 26 (instancias_espia.py, PASAPORTES).
// Pulsaciones del teléfono rojo: D.pulsa.
import { openGame } from './ui.js';
import { teclado } from './comun.js';

const D = /*DATOS*/{"digitos": [4, 1, 5], "pulsa": "2"}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 51 — Los pasaportes falsos', instr: 'Para cada pasaporte, elegid su fila y tocad el dígito de control que falta (0 a 9). Los pasaportes están en las cartas 61 y 63 y la regla, en la 26.', ...opts });
  const vals = D.digitos.map(() => null);
  let fila = 0, resuelto = false;
  const filas = document.createElement('div');
  filas.className = 'es-btns';
  const botones = D.digitos.map((_, i) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'pas-f';
    b.dataset.i = String(i);
    b.addEventListener('click', () => { if (!resuelto) { fila = i; ui.say(''); pintar(); } });
    filas.appendChild(b);
    return b;
  });
  const nums = teclado(0, 9, d => {
    if (resuelto) return;
    vals[fila] = d;
    ui.say('');
    pintar();
  });
  ui.body.append(filas, nums);
  function pintar() {
    botones.forEach((b, i) => {
      b.textContent = 'Pasaporte ' + (i + 1) + ': ' + (vals[i] === null ? '?' : vals[i]);
      b.classList.toggle('sel', i === fila);
      b.dataset.v = vals[i] === null ? '' : String(vals[i]);
    });
  }
  ui.button('Sellar los pasaportes', 'primary', () => {
    if (resuelto) return;
    if (vals.some(v => v === null)) { ui.say('Falta algún dígito de control.', 'bad'); return; }
    const malos = vals.filter((v, i) => v !== D.digitos[i]).length;
    if (malos) { ui.say('El aduanero levanta el sello: ' + malos + (malos === 1 ? ' dígito no coincide' : ' dígitos no coinciden') + ' con el control.', 'bad'); return; }
    resuelto = true;
    ui.say('Los pasaportes pasan la aduana. Teléfono rojo: pulsad ' + D.pulsa + '. Coged la carta 58.', 'ok');
  });
  ui.button('Vaciar', 'ghost', () => { if (!resuelto) { vals.fill(null); ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
