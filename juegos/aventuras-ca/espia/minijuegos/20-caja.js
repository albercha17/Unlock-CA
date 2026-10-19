// Carta 20 — La caja de seguridad: teclado de tres cifras; el número es el que se ve al superponer las hojas transparentes (cartas 14 y 15).
// Solución: 729.
import { openGame } from './ui.js';

const SOLUCION = '729';

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 20 — La caja de seguridad',
    instr: 'Escribe el número de tres cifras que se ve al superponer las dos hojas transparentes y pulsa Abrir.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .esp-pantalla{display:flex;gap:10px;justify-content:center;margin:6px 0 14px;padding:12px;border-radius:10px;border:3px solid #9aa4ad;background:linear-gradient(180deg,#1a2128,#0c1014);box-shadow:inset 0 0 14px rgba(0,0,0,.8)}
    .esp-cifra{width:46px;height:60px;border-radius:6px;background:#0c2a1a;border:2px solid #2d6a4a;color:#6dffa8;font:700 2.2rem "Courier New",monospace;text-align:center;line-height:60px}
    .esp-teclado{display:grid;grid-template-columns:repeat(3,64px);gap:8px;justify-content:center;margin:0 auto 12px}
    .esp-tecla{height:52px;border-radius:8px;border:2px solid #c0c8d0;background:linear-gradient(180deg,#e4e8ec,#9aa4ad);color:#10161c;font:800 1.3rem system-ui,sans-serif;cursor:pointer;box-shadow:0 3px 0 #4a525a}
    .esp-tecla:active{transform:translateY(2px);box-shadow:0 1px 0 #4a525a}
  `;
  ui.body.appendChild(style);

  const pantalla = document.createElement('div');
  pantalla.className = 'esp-pantalla';
  const teclado = document.createElement('div');
  teclado.className = 'esp-teclado';
  ui.body.appendChild(pantalla);
  ui.body.appendChild(teclado);

  let texto = '';
  let resuelto = false;

  function pintar() {
    pantalla.innerHTML = '';
    for (let i = 0; i < SOLUCION.length; i++) {
      const c = document.createElement('div');
      c.className = 'esp-cifra';
      c.dataset.i = String(i);
      c.textContent = texto[i] || '';
      pantalla.appendChild(c);
    }
  }

  '1234567890'.split('').forEach(k => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'esp-tecla';
    b.dataset.k = k;
    b.textContent = k;
    b.setAttribute('aria-label', 'Cifra ' + k);
    b.addEventListener('click', () => {
      if (resuelto || texto.length >= SOLUCION.length) return;
      texto += k;
      ui.say('');
      pintar();
    });
    teclado.appendChild(b);
  });

  ui.button('Abrir', 'primary', () => {
    if (resuelto) return;
    if (texto.length < SOLUCION.length) { ui.say('Faltan cifras: el número tiene tres.', 'bad'); return; }
    if (texto === SOLUCION) {
      resuelto = true;
      pantalla.style.borderColor = '#6dffa8';
      ui.say('Clic. La caja de seguridad se abre: dentro hay una carta negra con ventanas, una carta de letras y una nota de la Agente Zorro. Coged la carta 26.', 'ok');
    } else {
      ui.say('La luz roja parpadea: no es ese. Superponed las dos hojas con los marcos bien alineados y leed el número que aparece en negro sobre el ruido.', 'bad');
    }
  });
  ui.button('Borrar', '', () => { if (!resuelto) { texto = texto.slice(0, -1); ui.say(''); pintar(); } });

  pintar();
  return { close: ui.close };
}
