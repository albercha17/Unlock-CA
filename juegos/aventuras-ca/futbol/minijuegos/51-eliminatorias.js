// Carta 51 — El cuadro de la Copa: ocho equipos, cuartos, semifinales y final. Con los titulares de prensa (carta 26) hay que reconstruir quién ganó cada
// partido; el cuadro vacío está en las cartas 61 y 63 (dos mitades). instancias_futbol.py, ELIMINATORIAS (solución única).
import { openGame } from './ui.js';
import { estilo, opcion } from './comun.js';

const D = /*DATOS*/{"equipos": ["Estrella", "Rayos", "Halcones", "Tigres", "Delfines", "Lobos", "Osos", "Cóndores"], "bits": [0, 0, 0, 1, 0, 0, 1]}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 51 — El cuadro de la Copa', instr: 'En cada partido, tocad al equipo que pasa. Los titulares están en la carta 26 y el cuadro, en las cartas 61 y 63.', ...opts });
  estilo('fu-eli', '.eli-r{max-width:340px;margin:8px auto}.eli-r h4{margin:6px 0 2px;color:#f2c230;font:800 .85rem system-ui,Arial,sans-serif}.eli-p{display:flex;gap:6px;margin:4px 0}.eli-p button{flex:1;min-height:44px;font-size:.85rem}');
  // partidos: 0-3 cuartos, 4-5 semifinales, 6 final; gana[i] = equipo que pasa (o null)
  const gana = Array(7).fill(null);
  let resuelto = false;
  const equiposDe = i => i < 4 ? [2 * i, 2 * i + 1] : i < 6 ? [gana[2 * (i - 4)], gana[2 * (i - 4) + 1]] : [gana[4], gana[5]];
  const raiz = document.createElement('div');
  ui.body.appendChild(raiz);
  function pintar() {
    raiz.innerHTML = '';
    const titulos = ['Cuartos de final', 'Semifinales', 'Final'];
    const grupos = [[0, 1, 2, 3], [4, 5], [6]];
    grupos.forEach((ps, g) => {
      const caja = document.createElement('div');
      caja.className = 'eli-r';
      const h = document.createElement('h4');
      h.textContent = titulos[g];
      caja.appendChild(h);
      ps.forEach(i => {
        const fila = document.createElement('div');
        fila.className = 'eli-p';
        fila.dataset.i = String(i);
        equiposDe(i).forEach(t => {
          const b = opcion(t === null ? '—' : D.equipos[t], () => {
            if (resuelto || t === null) return;
            gana[i] = t;
            for (let j = i + 1; j < 7; j++) if (gana[j] !== null && !equiposDe(j).includes(gana[j])) gana[j] = null;
            ui.say('');
            pintar();
          });
          b.dataset.t = t === null ? '' : String(t);
          if (t !== null && gana[i] === t) b.classList.add('sel');
          fila.appendChild(b);
        });
        caja.appendChild(fila);
      });
      raiz.appendChild(caja);
    });
  }
  function correcto() {
    const sol = Array(7).fill(null);
    for (let i = 0; i < 7; i++) {
      const par = i < 4 ? [2 * i, 2 * i + 1] : i < 6 ? [sol[2 * (i - 4)], sol[2 * (i - 4) + 1]] : [sol[4], sol[5]];
      sol[i] = par[D.bits[i]];
    }
    return sol;
  }
  ui.button('Cantar el cuadro', 'primary', () => {
    if (resuelto) return;
    if (gana.some(g => g === null)) { ui.say('Faltan partidos por decidir.', 'bad'); return; }
    const sol = correcto();
    if (gana.some((g, i) => g !== sol[i])) { ui.say('El cuadro no cuadra con los titulares de prensa: algún resultado es imposible.', 'bad'); return; }
    resuelto = true;
    ui.say('Todos los titulares encajan: el campeón es ' + D.equipos[sol[6]] + '. Coged la carta 58.', 'ok');
  });
  ui.button('Borrar todo', 'ghost', () => { if (!resuelto) { gana.fill(null); ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
