// Carta 20 — La terminal de la placa: escribir la palabra que forman los componentes del cable, de la pila al chip (cartas 14 a 19 juntas).
// Solución: PIXEL.
import { openGame } from './ui.js';

const SOLUCION = 'PIXEL';

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 20 — La terminal de la placa',
    instr: 'Escribe la palabra que forman las letras de los componentes del cable, de la pila al chip.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .arc-pantalla{display:flex;gap:8px;justify-content:center;margin:4px 0 14px;padding:12px;border-radius:10px;border:2px solid #2ee67a;background:#04140a;box-shadow:inset 0 0 18px rgba(46,230,122,.35)}
    .arc-letra{width:40px;height:52px;border-bottom:3px solid #2ee67a;color:#7dffae;font:700 2rem/52px "Courier New",monospace;text-align:center}
    .arc-teclado{display:grid;grid-template-columns:repeat(7,1fr);gap:6px;max-width:330px;margin:0 auto 12px}
    .arc-tecla{aspect-ratio:1;min-height:42px;border-radius:8px;border:2px solid #ff5ad8;background:linear-gradient(180deg,#3a1458,#1c0a30);color:#ffd6f6;font:700 1.05rem system-ui,sans-serif;cursor:pointer;box-shadow:0 3px 0 #0d0518}
    .arc-tecla:active{transform:translateY(2px);box-shadow:0 1px 0 #0d0518}
  `;
  ui.body.appendChild(style);

  const pantalla = document.createElement('div');
  pantalla.className = 'arc-pantalla';
  const teclado = document.createElement('div');
  teclado.className = 'arc-teclado';
  ui.body.appendChild(pantalla);
  ui.body.appendChild(teclado);

  let texto = '';
  let resuelto = false;

  function pintar() {
    pantalla.innerHTML = '';
    for (let i = 0; i < SOLUCION.length; i++) {
      const s = document.createElement('div');
      s.className = 'arc-letra';
      s.dataset.i = String(i);
      s.textContent = texto[i] || '';
      pantalla.appendChild(s);
    }
  }

  'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('').forEach(l => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'arc-tecla';
    b.dataset.k = l;
    b.textContent = l;
    b.setAttribute('aria-label', 'Letra ' + l);
    b.addEventListener('click', () => {
      if (resuelto || texto.length >= SOLUCION.length) return;
      texto += l;
      ui.say('');
      pintar();
    });
    teclado.appendChild(b);
  });

  ui.button('Enviar', 'primary', () => {
    if (resuelto) return;
    if (texto.length < SOLUCION.length) { ui.say('Faltan letras: la palabra tiene cinco.', 'bad'); return; }
    if (texto === SOLUCION) {
      resuelto = true;
      pantalla.style.borderColor = '#9dffb0';
      ui.say('ACCESO CONCEDIDO. Una chispa recorre el cable de cobre desde la pila hasta el chip y todo el circuito se enciende. Coged la carta 26.', 'ok');
    } else {
      ui.say('ERROR: la terminal no reconoce esa palabra. Seguid el cable desde la pila hasta el chip, letra a letra, sin entrar en los ramales que acaban en un punto apagado.', 'bad');
    }
  });
  ui.button('Borrar', '', () => { if (!resuelto) { texto = texto.slice(0, -1); ui.say(''); pintar(); } });

  pintar();
  return { close: ui.close };
}
