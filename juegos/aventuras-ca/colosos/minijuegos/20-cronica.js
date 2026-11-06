// Carta 20 — La crónica: ordenar seis sucesos de Altamuralla con las pistas de la nota del archivero y de la crónica partida.
// Solución única (herramientas/instancias_colosos.py, cronica).
import { openGame } from './ui.js';
import { boton } from './comun.js';

const D = /*DATOS*/{"sucesos": ["La primera piedra", "El primer coloso", "El gran incendio", "La campana mayor", "La llegada de la doctora", "El elevador"], "solucion": [2, 4, 3, 5, 1, 0], "marca": "75"}/*FIN*/;
const ICONOS = ['🧱', '⛰️', '🔥', '🔔', '⚗️', '⛓️'];

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 20 — La crónica',
    instr: 'Tocad los sucesos en el orden en que ocurrieron, del más antiguo al más reciente.',
    ...opts
  });
  const orden = [];
  const lista = document.createElement('div');
  lista.className = 'co-lista';
  const btns = document.createElement('div');
  btns.className = 'co-btns';
  const botones = D.sucesos.map((s, i) => {
    const b = boton(ICONOS[i] + ' ' + s, () => {
      if (orden.length >= 6 || orden.includes(i)) return;
      orden.push(i);
      pintar();
    });
    b.dataset.suceso = i;
    btns.appendChild(b);
    return b;
  });
  ui.body.append(btns, lista);

  function pintar() {
    lista.innerHTML = '';
    for (let k = 0; k < 6; k++) {
      const p = document.createElement('div');
      p.className = 'co-paso';
      p.textContent = (k + 1) + '.º ' + (orden[k] !== undefined ? ICONOS[orden[k]] + ' ' + D.sucesos[orden[k]] : '—');
      lista.appendChild(p);
    }
    botones.forEach((b, i) => { b.disabled = orden.includes(i); });
  }

  ui.button('Borrar', 'ghost', () => { orden.length = 0; pintar(); ui.say('', ''); });
  ui.button('Comprobar', 'primary', () => {
    if (orden.length < 6) { ui.say('Faltan sucesos por colocar: son seis.', ''); return; }
    if (orden.every((s, k) => s === D.solucion[k])) {
      ui.say('El archivero aplaude con lágrimas en los ojos: ¡su crónica, en orden! Marca de la crónica: ' + D.marca + '. Coged la carta 28.', 'ok');
      botones.forEach(b => { b.disabled = true; });
    } else {
      ui.say('El archivero niega con la cabeza: alguna pista no se cumple.', 'bad');
      orden.length = 0;
      pintar();
    }
  });
  pintar();
  return { close: ui.close };
}
