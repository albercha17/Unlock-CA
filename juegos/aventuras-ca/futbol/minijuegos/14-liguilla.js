// Carta 14 — La liguilla del club: cuatro equipos jugaron todos contra todos; la clasificación y tres resultados están en la carta 16. Hay que escribir los
// cuatro marcadores que faltan (instancias_futbol.py, LIGUILLA, solución única). Aro de la tabla: D.aro.
import { openGame } from './ui.js';
import { contador } from './comun.js';

const D = /*DATOS*/{"equipos": ["Estrella", "Rayos", "Halcones", "Tigres"], "partidos": [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]], "desconocidos": [1, 2, 3, 4], "resultados": [[1, 4], [0, 2], [0, 3], [3, 3], [3, 1], [0, 3]], "aro": 7}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 14 — La liguilla del club', instr: 'Escribid los marcadores de los partidos que faltan para que cuadre la clasificación. La clasificación y los resultados conocidos están en la carta 16.', ...opts });
  const cont = D.desconocidos.map(i => {
    const [a, b] = D.partidos[i];
    const caja = document.createElement('div');
    caja.className = 'fu-fila';
    caja.dataset.i = String(i);
    const t = document.createElement('b');
    t.textContent = D.equipos[a] + ' – ' + D.equipos[b];
    const x = contador(D.equipos[a], 0, 9, 0, 'l' + i + 'a');
    const y = contador(D.equipos[b], 0, 9, 0, 'l' + i + 'b');
    caja.append(t, x.el, y.el);
    ui.body.appendChild(caja);
    return { i, x, y };
  });
  let resuelto = false;
  ui.button('Entregar la tabla', 'primary', () => {
    if (resuelto) return;
    const malos = cont.filter(c => c.x.valor() !== D.resultados[c.i][0] || c.y.valor() !== D.resultados[c.i][1]).length;
    if (malos) { ui.say('La clasificación no sale: algún marcador no cuadra con los puntos y los goles de la tabla.', 'bad'); return; }
    resuelto = true;
    ui.say('La tabla cuadra al milímetro. Aro de la tabla: ' + D.aro + '. Coged la carta 24.', 'ok');
  });
  return { close: ui.close };
}
