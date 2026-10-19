// Carta 24 — El teletipo: escribir la palabra que se lee por las ventanas de la rejilla (carta 30) puesta sobre la carta de letras (31), de arriba abajo.
// Solución: NEPTUNO.
import { openGame } from './ui.js';

const SOLUCION = 'NEPTUNO';
const FILAS = ['QWERTYUIOP', 'ASDFGHJKLÑ', 'ZXCVBNM'];

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 24 — El teletipo',
    instr: 'Escribe la palabra que se lee por las ventanas de la rejilla, de arriba abajo, y pulsa Enviar.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .esp-cinta{min-height:58px;margin:6px 0 14px;padding:10px 12px;background:#f4efe0;color:#1a1a1a;font:700 1.6rem "Courier New",monospace;letter-spacing:.28em;text-align:center;border-radius:2px;box-shadow:0 3px 0 #b8b098,inset 0 0 10px rgba(0,0,0,.12);border-left:6px dotted #8a8470;border-right:6px dotted #8a8470}
    .esp-fila{display:flex;gap:4px;justify-content:center;margin-bottom:5px}
    .esp-letra{width:30px;height:38px;border-radius:50%;border:2px solid #c0c8d0;background:linear-gradient(180deg,#3a4046,#1a1e22);color:#f0f4f8;font:700 .95rem "Courier New",monospace;cursor:pointer;box-shadow:0 2px 0 #0a0c0e;padding:0}
    .esp-letra:active{transform:translateY(2px);box-shadow:none}
    .esp-cinta.ok{background:#dff5e4;border-color:#46a46a}
  `;
  ui.body.appendChild(style);

  const cinta = document.createElement('div');
  cinta.className = 'esp-cinta';
  ui.body.appendChild(cinta);
  const teclas = document.createElement('div');
  ui.body.appendChild(teclas);

  let texto = '';
  let resuelto = false;

  function pintar() {
    cinta.textContent = texto || ' ';
    cinta.dataset.t = texto;
    cinta.className = 'esp-cinta' + (resuelto ? ' ok' : '');
  }

  FILAS.forEach(f => {
    const fila = document.createElement('div');
    fila.className = 'esp-fila';
    f.split('').forEach(l => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'esp-letra';
      b.dataset.k = l;
      b.textContent = l;
      b.setAttribute('aria-label', 'Tecla ' + l);
      b.addEventListener('click', () => {
        if (resuelto || texto.length >= SOLUCION.length) return;
        texto += l;
        ui.say('');
        pintar();
      });
      fila.appendChild(b);
    });
    teclas.appendChild(fila);
  });

  ui.button('Enviar', 'primary', () => {
    if (resuelto) return;
    if (texto.length < SOLUCION.length) { ui.say('Faltan letras: la palabra tiene siete.', 'bad'); return; }
    if (texto === SOLUCION) {
      resuelto = true;
      pintar();
      ui.say('El teletipo imprime: «NEPTUNO», el nombre del yate del Dr. Noche y la contraseña de su pasarela. Coged la carta 28.', 'ok');
    } else {
      ui.say('El teletipo escupe una cinta sin sentido. Poned la carta negra con ventanas sobre la de letras, con los marcos alineados, y leed las letras que se ven, de arriba abajo.', 'bad');
    }
  });
  ui.button('Borrar', '', () => { if (!resuelto) { texto = texto.slice(0, -1); ui.say(''); pintar(); } });

  pintar();
  return { close: ui.close };
}
