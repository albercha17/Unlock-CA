// Carta 48 — El mensaje de la pantalla: ocho bytes en hexadecimal (carta 42), la tabla de caracteres (carta 49) y la regla de los bytes (carta 53).
// Se escribe la palabra que forman. Solución: D.claro (instancias_arcade.py, ASCII).
import { openGame } from './ui.js';
import { estilo } from './maquina.js';

const D = /*DATOS*/{"claro": "CONTINUE"}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 48 — El mensaje de la pantalla', instr: 'Descifrad los ocho bytes de la carta 42 con la tabla de la carta 49 y escribid el mensaje con las letras en orden. La regla está en la carta 53.', ...opts });
  estilo('ar-asc', `.asc-casillas{display:flex;gap:6px;justify-content:center;margin:6px 0 12px}.asc-casilla{width:34px;height:46px;border-bottom:3px solid #2ee67a;color:#7dffae;font:700 1.6rem/46px ui-monospace,monospace;text-align:center}.asc-teclado{display:grid;grid-template-columns:repeat(7,1fr);gap:6px;max-width:330px;margin:0 auto 10px}.asc-teclado button{aspect-ratio:1;min-height:40px;border-radius:8px;border:2px solid #ff5ad8;background:linear-gradient(180deg,#3a1458,#1c0a30);color:#ffd6f6;font:700 1rem system-ui;cursor:pointer;box-shadow:0 3px 0 #0d0518}`);
  let texto = '', resuelto = false;
  const casillas = document.createElement('div');
  casillas.className = 'asc-casillas';
  const teclado = document.createElement('div');
  teclado.className = 'asc-teclado';
  ui.body.append(casillas, teclado);
  function pintar() {
    casillas.innerHTML = '';
    for (let i = 0; i < D.claro.length; i++) {
      const s = document.createElement('div');
      s.className = 'asc-casilla';
      s.dataset.i = String(i);
      s.textContent = texto[i] || '';
      casillas.appendChild(s);
    }
    casillas.dataset.texto = texto;
  }
  'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('').forEach(l => {
    const b = document.createElement('button');
    b.type = 'button';
    b.dataset.k = l;
    b.textContent = l;
    b.setAttribute('aria-label', 'Letra ' + l);
    b.addEventListener('click', () => { if (resuelto || texto.length >= D.claro.length) return; texto += l; ui.say(''); pintar(); });
    teclado.appendChild(b);
  });
  ui.button('Borrar una', 'ghost', () => { if (!resuelto) { texto = texto.slice(0, -1); ui.say(''); pintar(); } });
  ui.button('Enviar', 'primary', () => {
    if (resuelto) return;
    if (texto.length < D.claro.length) { ui.say('El mensaje tiene ocho letras, una por byte.', 'bad'); return; }
    if (texto !== D.claro) {
      const bien = texto.split('').filter((c, i) => c === D.claro[i]).length;
      ui.say('La pantalla se llena de basura: ' + bien + ' de las 8 letras están en su sitio.', 'bad');
      return;
    }
    resuelto = true;
    ui.say('La pantalla parpadea y muestra «' + D.claro + '»: la cuenta atrás se detiene. Coged la carta 36.', 'ok');
  });
  pintar();
  return { close: ui.close };
}
