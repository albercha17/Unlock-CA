// Carta 14 — El granero cerrado: la puerta se abre diciendo cuántos sacos hay en el montón (la falsa posición del papiro Rhind).
// El grabado de la carta 16 dibuja «un montón, su mitad y su cuarto» sumando 28 sacos. Solución: 16 (instancias_egipto.py, MONTON).
import { openGame } from './ui.js';
import { guardarSello, contador } from './nilo.js';

const D = /*DATOS*/{"fracciones": [[1, 1], [1, 2], [1, 4]], "total": 28, "solucion": 16}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 14 — El granero cerrado', instr: 'La puerta del granero solo se abre si decís cuántos sacos tiene el montón. Lo que dice el grabado, en la carta 16.', ...opts });
  const c = contador('Sacos', 99, () => ui.say(''), 'sacos');
  ui.body.appendChild(c.el);
  let resuelto = false;
  ui.button('Abrir la puerta', 'primary', () => {
    if (resuelto) return;
    const v = c.valor();
    if (v === D.solucion) {
      resuelto = true; guardarSello('14');
      ui.say('El cerrojo gira y la puerta del granero se abre con un crujido de siglos. Coged la carta 24.', 'ok');
    } else ui.say('La puerta no se mueve: ' + v + ' sacos no cuadran con lo grabado (carta 16).', 'bad');
  });
  return { close: ui.close };
}
