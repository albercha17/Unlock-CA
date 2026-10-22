// Carta 85 — La válvula de la locomotora: cinco coordenadas de Polibio, las que dejaron otros cinco puzles (orden en la carta 86), dan una palabra con el
// cuadrado de la carta 87. Se escribe la palabra. Solución: D.palabra (instancias_oeste.py, POLIBIO).
import { openGame } from './ui.js';
import { estilo } from './comun.js';

const D = /*DATOS*/{"palabra": "VAPOR"}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 85 — La válvula de la locomotora', instr: 'Escribid la palabra que forman las cinco coordenadas que anotasteis, con el cuadrado de la carta 87. El orden de las coordenadas, en la 86.', ...opts });
  estilo('oe-pol', `.pol-casillas{display:flex;gap:8px;justify-content:center;margin:8px 0 12px}.pol-casilla{width:44px;height:54px;border-bottom:4px solid #e0a040;color:#f5d48a;font:800 2rem/54px Georgia,serif;text-align:center}.pol-teclado{display:grid;grid-template-columns:repeat(7,1fr);gap:6px;max-width:330px;margin:0 auto 10px}.pol-teclado button{aspect-ratio:1;min-height:40px;border-radius:8px;border:2px solid #e0a040;background:linear-gradient(180deg,#8a5a2a,#4a2c14);color:#f5d48a;font:700 1rem Georgia,serif;cursor:pointer;box-shadow:0 3px 0 #2a1608;padding:0}`);
  let texto = '', resuelto = false;
  const casillas = document.createElement('div');
  casillas.className = 'pol-casillas';
  const teclado = document.createElement('div');
  teclado.className = 'pol-teclado';
  ui.body.append(casillas, teclado);
  function pintar() {
    casillas.innerHTML = '';
    for (let i = 0; i < D.palabra.length; i++) {
      const s = document.createElement('div');
      s.className = 'pol-casilla';
      s.dataset.i = String(i);
      s.textContent = texto[i] || '';
      casillas.appendChild(s);
    }
    casillas.dataset.texto = texto;
  }
  'ABCDEFGHIKLMNOPQRSTUVWXYZ'.split('').forEach(l => {
    const b = document.createElement('button');
    b.type = 'button';
    b.dataset.k = l;
    b.textContent = l;
    b.setAttribute('aria-label', 'Letra ' + l);
    b.addEventListener('click', () => { if (resuelto || texto.length >= D.palabra.length) return; texto += l; ui.say(''); pintar(); });
    teclado.appendChild(b);
  });
  ui.button('Borrar una', 'ghost', () => { if (!resuelto) { texto = texto.slice(0, -1); ui.say(''); pintar(); } });
  ui.button('Abrir la válvula', 'primary', () => {
    if (resuelto) return;
    if (texto.length < D.palabra.length) { ui.say('La palabra tiene ' + D.palabra.length + ' letras, una por coordenada.', 'bad'); return; }
    if (texto !== D.palabra) {
      const bien = texto.split('').filter((c, i) => c === D.palabra[i]).length;
      ui.say('La válvula no cede: ' + bien + ' de las ' + D.palabra.length + ' letras están en su sitio.', 'bad');
      return;
    }
    resuelto = true;
    ui.say('La válvula gira, el vapor escapa en una nube y la locomotora arranca. Coged la carta 99.', 'ok');
  });
  pintar();
  return { close: ui.close };
}
