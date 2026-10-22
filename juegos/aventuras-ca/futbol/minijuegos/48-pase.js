// Carta 48 — El pase en cadena: siete jugadores en un campo de entrenamiento; el balón va recto de uno a otro y lo corta cualquier rival o compañero que
// esté justo en su camino. Hay que salir del portero (P) y acabar en el delantero (Z) pasando por todos una sola vez. El campo está en las cartas 42 y 49
// (dos mitades) y la regla, en la 53 (instancias_futbol.py, PASE).
import { openGame } from './ui.js';
import { estilo } from './comun.js';

const D = /*DATOS*/{"jugadores": [[2, 4], [13, 4], [6, 4], [3, 8], [11, 4], [2, 0], [12, 4]], "rivales": [[9, 5], [8, 6], [4, 4], [3, 4], [5, 4], [4, 2]], "etiquetas": ["P", "A", "B", "C", "D", "E", "Z"]}/*FIN*/;

function mcd(a, b) { return b ? mcd(b, a % b) : Math.abs(a); }

// ¿Corta algo el pase de p a q? Un rival o un compañero justo en un punto entero del camino.
function cortado(p, q) {
  const dx = q[0] - p[0], dy = q[1] - p[1], g = mcd(dx, dy);
  if (g < 2) return false;
  const ocupados = new Set(D.rivales.concat(D.jugadores).map(u => u[0] + ',' + u[1]));
  for (let k = 1; k < g; k++) if (ocupados.has((p[0] + k * dx / g) + ',' + (p[1] + k * dy / g))) return true;
  return false;
}

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 48 — El pase en cadena', instr: 'Tocad a los jugadores en el orden de los pases: desde el portero (P) hasta el delantero (Z), por todos los demás una vez. El campo está en las cartas 42 y 49; la regla, en la 53.', ...opts });
  estilo('fu-pase', '.pas-lin{min-height:2.4em}');
  let cadena = [], resuelto = false;
  const fila = document.createElement('div');
  fila.className = 'fu-btns';
  const botones = D.etiquetas.map((t, k) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.dataset.k = t;
    b.textContent = t;
    b.setAttribute('aria-label', 'Jugador ' + t);
    b.addEventListener('click', () => { if (resuelto) return; cadena.push(k); ui.say(''); pintar(); });
    fila.appendChild(b);
    return b;
  });
  const linea = document.createElement('div');
  linea.className = 'fu-pie pas-lin';
  ui.body.append(fila, linea);
  function pintar() {
    linea.textContent = cadena.length ? 'Pases: ' + cadena.map(k => D.etiquetas[k]).join(' → ') : 'Pases: (ninguno)';
    botones.forEach((b, k) => b.classList.toggle('sel', cadena[cadena.length - 1] === k));
  }
  ui.button('Sacar de puerta', 'primary', () => {
    if (resuelto) return;
    const n = D.jugadores.length;
    if (cadena.length < 2) { ui.say('Marcad primero los pases.', 'bad'); return; }
    if (cadena[0] !== 0) { ui.say('La jugada tiene que empezar en el portero (P).', 'bad'); return; }
    for (let i = 1; i < cadena.length; i++) {
      if (cortado(D.jugadores[cadena[i - 1]], D.jugadores[cadena[i]])) {
        ui.say('El pase de ' + D.etiquetas[cadena[i - 1]] + ' a ' + D.etiquetas[cadena[i]] + ' lo corta alguien que está en su camino.', 'bad');
        return;
      }
    }
    if (new Set(cadena).size < cadena.length) { ui.say('Algún jugador toca el balón dos veces: cada uno, una sola.', 'bad'); return; }
    if (cadena[cadena.length - 1] !== n - 1) { ui.say('La jugada tiene que acabar en el delantero (Z).', 'bad'); return; }
    if (cadena.length !== n) { ui.say('Faltan jugadores por tocar el balón.', 'bad'); return; }
    resuelto = true;
    ui.say('La jugada sale redonda y el delantero marca. La pizarra se mueve y deja ver un papel. Coged la carta 36.', 'ok');
  });
  ui.button('Quitar el último', 'ghost', () => { if (!resuelto) { cadena.pop(); ui.say(''); pintar(); } });
  ui.button('Empezar de nuevo', 'ghost', () => { if (!resuelto) { cadena = []; ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
