// Carta 74 — La placa del anexo: cinco interruptores que alimentan, a través de puertas lógicas Y / O / NO, el motor de la puerta,
// la alarma y la ventilación (circuitos en las cartas 75, 76 y 78; leyenda y estado pedido en la carta 81). Una sola combinación
// (herramientas/instancias_ampliacion.py).
import { openGame } from './ui.js';

const C = /*DATOS*/{"interruptores": ["A", "B", "C", "D", "E"], "solucion": {"A": false, "B": false, "C": true, "D": true, "E": true}, "salidas": {"motor": ["Y", ["NO", ["O", ["in", "A"], ["in", "B"]]], ["in", "D"]], "alarma": ["Y", ["NO", ["O", ["in", "B"], ["in", "E"]]], ["NO", ["in", "B"]]], "ventilacion": ["O", ["O", ["in", "B"], ["in", "A"]], ["in", "C"]]}, "quiere": {"motor": true, "alarma": false, "ventilacion": true}}/*FIN*/;

function evaluar(n, v) {
  if (n[0] === 'in') return v[n[1]];
  if (n[0] === 'NO') return !evaluar(n[1], v);
  const a = evaluar(n[1], v), b = evaluar(n[2], v);
  return n[0] === 'Y' ? a && b : a || b;
}

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 74 — La placa del anexo',
    instr: 'Subid o bajad los cinco interruptores y pulsad «Conectar». La placa solo abre la puerta si el motor y la ventilación se encienden y la alarma no.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .mar-placa{display:flex;gap:10px;justify-content:center;margin:10px auto 14px;padding:14px 10px;max-width:320px;border-radius:10px;
      background:repeating-linear-gradient(0deg,#123,#123 10px,#14283a 10px,#14283a 20px);border:3px solid #6ee6f0}
    .mar-int{width:48px;height:96px;border-radius:10px;border:2px solid #6ee6f0;background:#0a1620;cursor:pointer;position:relative;padding:0}
    .mar-int i{position:absolute;left:8px;right:8px;height:38px;border-radius:6px;background:#3a4a56;transition:top .15s}
    .mar-int[data-on="1"] i{top:8px;background:#ffd84a;box-shadow:0 0 12px #ffd84a}
    .mar-int[data-on="0"] i{top:48px}
    .mar-int b{position:absolute;left:0;right:0;bottom:-24px;text-align:center;color:#bfefff;font:800 1rem system-ui,sans-serif}
  `;
  ui.body.appendChild(style);
  const placa = document.createElement('div');
  placa.className = 'mar-placa';
  ui.body.appendChild(placa);

  const v = {};
  let resuelto = false;
  C.interruptores.forEach(k => {
    v[k] = false;
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'mar-int';
    b.dataset.k = k;
    b.dataset.on = '0';
    b.innerHTML = '<i></i><b>' + k + '</b>';
    b.setAttribute('aria-label', 'Interruptor ' + k + ': apagado');
    b.addEventListener('click', () => {
      if (resuelto) return;
      v[k] = !v[k];
      b.dataset.on = v[k] ? '1' : '0';
      b.setAttribute('aria-label', 'Interruptor ' + k + ': ' + (v[k] ? 'encendido' : 'apagado'));
      ui.say('');
    });
    placa.appendChild(b);
  });

  ui.button('Conectar', 'primary', () => {
    if (resuelto) return;
    const mal = [];
    if (evaluar(C.salidas.motor, v) !== C.quiere.motor) mal.push('el motor no arranca');
    if (evaluar(C.salidas.alarma, v) !== C.quiere.alarma) mal.push('salta la alarma');
    if (evaluar(C.salidas.ventilacion, v) !== C.quiere.ventilacion) mal.push('la ventilación no se enciende');
    if (!mal.length) {
      resuelto = true;
      ui.say('El motor ronronea, el aire empieza a circular y la alarma sigue callada. La puerta interior del anexo se desliza. Coged la carta 83.', 'ok');
    } else {
      ui.say('La puerta no se mueve: ' + mal.join(' y ') + '. Seguid los cables de las cartas 75, 76 y 78.', 'bad');
    }
  });
  return { close: ui.close };
}
