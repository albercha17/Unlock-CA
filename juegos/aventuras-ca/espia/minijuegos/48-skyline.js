// Carta 48 — El panel del skyline: rascacielos 4 x 4. Las pistas del borde están repartidas en las cartas 52 (arriba e izquierda) y 53 (abajo y derecha).
// Instancia (herramientas/instancias_espia.py): solución única. De arriba abajo: 4 3 1 2 / 2 1 4 3 / 3 4 2 1 / 1 2 3 4.
import { openGame } from './ui.js';

const SOLUCION = [[4, 3, 1, 2], [2, 1, 4, 3], [3, 4, 2, 1], [1, 2, 3, 4]];

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 48 — El panel del skyline',
    instr: 'Toca una casilla para ir cambiando la altura del edificio (1 a 4). Usa las pistas de las cartas 52 y 53.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .esp-skyline{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;max-width:260px;margin:6px auto 12px;padding:10px;border-radius:10px;border:2px solid #7fe8f0;background:#05090c}
    .esp-edificio{position:relative;aspect-ratio:1;border-radius:6px;border:2px solid #2a5a66;background:#0b1a20;color:#e8fbff;font:800 1.6rem system-ui,sans-serif;cursor:pointer;padding:0;overflow:hidden}
    .esp-edificio i{position:absolute;left:12%;right:12%;bottom:0;background:linear-gradient(180deg,#7fe8f0,#2a8a9a);border-radius:3px 3px 0 0;opacity:.35}
    .esp-edificio b{position:relative}
    .esp-skyline.ok .esp-edificio{border-color:#6dffa8}
  `;
  ui.body.appendChild(style);

  const rejilla = document.createElement('div');
  rejilla.className = 'esp-skyline';
  ui.body.appendChild(rejilla);

  const h = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]];
  let resuelto = false;

  function pintar() {
    rejilla.className = 'esp-skyline' + (resuelto ? ' ok' : '');
    rejilla.innerHTML = '';
    for (let f = 0; f < 4; f++) {
      for (let c = 0; c < 4; c++) {
        const b = document.createElement('button');
        b.type = 'button';
        b.className = 'esp-edificio';
        b.dataset.f = String(f);
        b.dataset.c = String(c);
        b.dataset.h = String(h[f][c]);
        b.setAttribute('aria-label', 'Fila ' + (f + 1) + ', columna ' + (c + 1) + ': altura ' + (h[f][c] || 'vacía'));
        b.innerHTML = '<i style="height:' + h[f][c] * 25 + '%"></i><b>' + (h[f][c] || '') + '</b>';
        b.addEventListener('click', () => { if (!resuelto) { h[f][c] = (h[f][c] + 1) % 5; ui.say(''); pintar(); } });
        rejilla.appendChild(b);
      }
    }
  }

  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    if (h.some(fila => fila.some(x => x === 0))) { ui.say('Faltan edificios: hay casillas sin altura.', 'bad'); return; }
    for (let i = 0; i < 4; i++) {
      const fila = new Set(h[i]), col = new Set(h.map(r => r[i]));
      if (fila.size < 4 || col.size < 4) { ui.say('Hay alturas repetidas en alguna fila o columna: cada una debe tener 1, 2, 3 y 4.', 'bad'); return; }
    }
    if (h.every((fila, f) => fila.every((x, c) => x === SOLUCION[f][c]))) {
      resuelto = true;
      pintar();
      ui.say('El perfil encaja con todas las pistas: el panel marca la torre del Dr. Noche con un círculo rojo. Coged la carta 58.', 'ok');
    } else {
      ui.say('Las alturas no repiten, pero el perfil no cuadra con alguna pista del borde. Recordad: los edificios altos tapan a los bajos.', 'bad');
    }
  });
  ui.button('Vaciar', '', () => { if (!resuelto) { h.forEach(fila => fila.fill(0)); ui.say(''); pintar(); } });

  pintar();
  return { close: ui.close };
}
