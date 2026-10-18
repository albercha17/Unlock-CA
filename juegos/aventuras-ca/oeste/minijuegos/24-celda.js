// Carta 24 — La celda: señalar al bandido del cartel de «Se busca» (cartas 30, 31 y 32 en columna) comparándolo con el libro del sheriff (carta 36).
// Solución: Pete Cuchillo (sombrero de ala ancha, cicatriz a la izquierda del retrato y bigote de manillar).
import { openGame } from './ui.js';

const NOMBRES = ['Pete Cuchillo', 'Jack Botas', 'Slim Sombra', 'Doc Pólvora', 'La Zorra Roja', 'Tom Barro'];
const SOLUCION = 'Pete Cuchillo';

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 24 — La celda',
    instr: 'Elige el nombre del bandido del cartel de «Se busca» y pulsa Detener.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .oes-lista{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;max-width:340px;margin:6px auto 14px}
    .oes-nombre{padding:12px 8px;border-radius:8px;border:2px solid #b8742a;background:linear-gradient(180deg,#f0dcb0,#d4b27a);color:#2a1404;font:700 .95rem Georgia,serif;cursor:pointer;box-shadow:0 3px 0 #4a2c10}
    .oes-nombre.sel{border-color:#fff;background:linear-gradient(180deg,#ffd27a,#e0a040);box-shadow:0 0 12px #f0b860}
    .oes-lista.ok .oes-nombre.sel{background:linear-gradient(180deg,#9be8ae,#46c46a)}
  `;
  ui.body.appendChild(style);

  const lista = document.createElement('div');
  lista.className = 'oes-lista';
  ui.body.appendChild(lista);

  let elegido = null;
  let resuelto = false;

  function pintar() {
    lista.className = 'oes-lista' + (resuelto ? ' ok' : '');
    lista.innerHTML = '';
    NOMBRES.forEach((n, i) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'oes-nombre' + (elegido === n ? ' sel' : '');
      b.dataset.n = n;
      b.dataset.i = String(i);
      b.textContent = n;
      b.setAttribute('aria-label', 'Sospechoso ' + n);
      b.addEventListener('click', () => { if (!resuelto) { elegido = n; ui.say(''); pintar(); } });
      lista.appendChild(b);
    });
  }

  ui.button('Detener', 'primary', () => {
    if (resuelto) return;
    if (!elegido) { ui.say('Elegid primero un nombre de la lista.', 'bad'); return; }
    if (elegido === SOLUCION) {
      resuelto = true;
      pintar();
      ui.say('El prisionero baja la cabeza: «Está bien, me habéis pillado... Pete Cuchillo lo organizó todo, y la banda se esconde en la vieja mina del arroyo seco». Coged la carta 28.', 'ok');
    } else {
      ui.say('El prisionero sonríe: «Ese no es». Comparad el cartel con el libro del sheriff: el sombrero, la cicatriz y el bigote tienen que coincidir los tres.', 'bad');
    }
  });

  pintar();
  return { close: ui.close };
}
