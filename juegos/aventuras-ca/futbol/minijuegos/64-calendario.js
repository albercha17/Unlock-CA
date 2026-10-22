// Carta 64 — El calendario de la liga: ocho equipos que se cruzan por el método del círculo (carta 67); en la carta 66 están los cruces de la jornada 1.
// Hay que escribir los cuatro cruces de la jornada D.jornada (instancias_futbol.py, CALENDARIO).
import { openGame } from './ui.js';
import { estilo, opcion } from './comun.js';

const D = /*DATOS*/{"clubes": ["Estrella", "Rayos", "Halcones", "Tigres", "Delfines", "Lobos", "Osos", "Cóndores"], "solucion": [[1, 4], [7, 5], [0, 6], [2, 3]], "jornada": 5}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 64 — El calendario de la liga', instr: 'Formad los cuatro cruces de la jornada ' + D.jornada + ': tocad un equipo y luego su rival. Los cruces de la jornada 1 están en la carta 66 y el método, en la 67.', ...opts });
  estilo('fu-cal', '.cal-g{display:grid;grid-template-columns:1fr 1fr;gap:6px;max-width:340px;margin:8px auto}.cal-g button{min-height:48px}.cal-g button.usado{opacity:.45}');
  let pares = [], pend = null, resuelto = false;
  const rejilla = document.createElement('div');
  rejilla.className = 'cal-g';
  const lista = document.createElement('div');
  lista.className = 'fu-pie';
  const botones = D.clubes.map((c, k) => {
    const b = opcion(c, () => {
      if (resuelto) return;
      if (pares.some(p => p.includes(k))) { ui.say('Ese equipo ya tiene rival en esta jornada.', 'bad'); return; }
      if (pend === null) pend = k;
      else if (pend === k) pend = null;
      else { pares.push([pend, k]); pend = null; ui.say(''); }
      pintar();
    });
    b.dataset.k = String(k);
    rejilla.appendChild(b);
    return b;
  });
  ui.body.append(rejilla, lista);
  function pintar() {
    botones.forEach((b, k) => { b.classList.toggle('sel', pend === k); b.classList.toggle('usado', pares.some(p => p.includes(k))); });
    lista.textContent = pares.length ? pares.map(p => D.clubes[p[0]] + ' – ' + D.clubes[p[1]]).join(' · ') : 'Cruces: (ninguno)';
  }
  ui.button('Sortear la jornada', 'primary', () => {
    if (resuelto) return;
    if (pares.length < 4) { ui.say('Faltan cruces: son cuatro partidos.', 'bad'); return; }
    const clave = ps => ps.map(p => p.slice().sort((a, b) => a - b).join('-')).sort().join('|');
    if (clave(pares) !== clave(D.solucion)) { ui.say('Los cruces no coinciden con los de la jornada ' + D.jornada + ' del secretario de la liga.', 'bad'); return; }
    resuelto = true;
    ui.say('Los cuatro cruces son los de la jornada ' + D.jornada + ': el secretario abre la vitrina. Coged la carta 62.', 'ok');
  });
  ui.button('Quitar el último', 'ghost', () => { if (!resuelto) { pares.pop(); pend = null; ui.say(''); pintar(); } });
  ui.button('Empezar de nuevo', 'ghost', () => { if (!resuelto) { pares = []; pend = null; ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
