// Carta 20 — La convocatoria: el míster necesita a dos jugadores de la plantilla y los describe en un acertijo (carta 18). Los seis cromos tienen dos caras:
// por delante, dorsal y nombre; por detrás, la ficha (cartas 19 y 21, con «Dar la vuelta»). Hay que elegir sus dos camisetas (instancias_futbol.py, CROMOS).
import { openGame } from './ui.js';
import { estilo, opcion } from './comun.js';

const D = /*DATOS*/{"jugadores": [{"dorsal": 7, "nombre": "Rafa Gol"}, {"dorsal": 6, "nombre": "Toni Roca"}, {"dorsal": 4, "nombre": "Luis Muro"}, {"dorsal": 8, "nombre": "Mario Eje"}, {"dorsal": 2, "nombre": "Paco Guante"}, {"dorsal": 9, "nombre": "Beto Pase"}], "solucion": [4, 6]}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 20 — La convocatoria', instr: 'Elegid las dos camisetas que pide el míster. Su acertijo está en la carta 18 y las fichas de los jugadores, por detrás de los cromos (cartas 19 y 21).', ...opts });
  estilo('fu-conv', '.conv-g{display:grid;grid-template-columns:1fr 1fr;gap:8px;max-width:340px;margin:8px auto}.conv-g button{min-height:56px}');
  const sel = new Set();
  let resuelto = false;
  const cuadro = document.createElement('div');
  cuadro.className = 'conv-g';
  const botones = D.jugadores.map(j => {
    const b = opcion(j.dorsal + ' · ' + j.nombre, () => {
      if (resuelto) return;
      if (sel.has(j.dorsal)) sel.delete(j.dorsal); else sel.add(j.dorsal);
      ui.say('');
      pintar();
    });
    b.dataset.d = String(j.dorsal);
    cuadro.appendChild(b);
    return b;
  });
  ui.body.appendChild(cuadro);
  function pintar() { botones.forEach(b => b.classList.toggle('sel', sel.has(Number(b.dataset.d)))); }
  ui.button('Presentar la lista', 'primary', () => {
    if (resuelto) return;
    if (sel.size !== 2) { ui.say('El míster pide exactamente dos camisetas.', 'bad'); return; }
    const v = [...sel].sort((a, b) => a - b);
    if (v[0] !== D.solucion[0] || v[1] !== D.solucion[1]) { ui.say('El míster niega con la cabeza: esos no son los dos que describe su acertijo.', 'bad'); return; }
    resuelto = true;
    ui.say('«Esos mismos», sonríe el míster, y os da una carta por el favor. Coged la carta 28.', 'ok');
  });
  ui.button('Borrar la lista', 'ghost', () => { if (!resuelto) { sel.clear(); ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
