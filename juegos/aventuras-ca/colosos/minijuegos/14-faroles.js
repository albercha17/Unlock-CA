// Carta 14 — Los faroles del camino de ronda: Akari 7 x 7. La app enseña las torres sin número; los números están en el plano de las torres.
// Solución única (herramientas/instancias_colosos.py, faroles).
import { openGame } from './ui.js';
import { rejilla, tamCasilla } from './comun.js';

const D = /*DATOS*/{"n": 7, "muros": [[0, 0], [0, 1], [0, 3], [1, 5], [2, 2], [2, 4], [4, 2], [4, 4], [5, 1], [6, 3], [6, 5], [6, 6]], "solucion": [[0, 2], [0, 5], [1, 0], [2, 3], [3, 6], [4, 1], [4, 5], [5, 4], [6, 1]], "marca": "79"}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 14 — Los faroles del camino de ronda',
    instr: 'Tocad las losas para poner o quitar faroles. Todo el camino tiene que quedar iluminado, sin dos faroles que se vean, y cada torre con su número de faroles pegados.',
    ...opts
  });
  const n = D.n;
  const muro = new Set(D.muros.map(([f, c]) => f + ',' + c));
  const faroles = new Set();
  const { el, celdas } = rejilla(n, (f, c, b) => {
    if (muro.has(f + ',' + c)) { b.classList.add('muro'); b.disabled = true; return; }
    b.addEventListener('click', () => {
      const k = f + ',' + c;
      if (faroles.has(k)) faroles.delete(k); else faroles.add(k);
      pintar();
    });
  }, tamCasilla(n));
  const pie = document.createElement('div');
  pie.className = 'co-pie';
  ui.body.append(el, pie);

  function vista(f, c) {
    const out = [];
    [[-1, 0], [1, 0], [0, -1], [0, 1]].forEach(([a, b]) => {
      let y = f + a, x = c + b;
      while (y >= 0 && y < n && x >= 0 && x < n && !muro.has(y + ',' + x)) { out.push(y + ',' + x); y += a; x += b; }
    });
    return out;
  }
  function iluminadas() {
    const s = new Set();
    faroles.forEach(k => { s.add(k); const [f, c] = k.split(',').map(Number); vista(f, c).forEach(v => s.add(v)); });
    return s;
  }
  function pintar() {
    const lit = iluminadas();
    for (let f = 0; f < n; f++) for (let c = 0; c < n; c++) {
      const k = f + ',' + c;
      if (muro.has(k)) continue;
      const b = celdas[f][c];
      b.classList.toggle('farol', faroles.has(k));
      b.classList.toggle('luz', lit.has(k) && !faroles.has(k));
      b.textContent = faroles.has(k) ? '🏮' : '';
    }
    pie.textContent = `Faroles: ${faroles.size}`;
  }

  ui.button('Encender', 'primary', () => {
    const lit = iluminadas();
    const oscuras = [];
    for (let f = 0; f < n; f++) for (let c = 0; c < n; c++) if (!muro.has(f + ',' + c) && !lit.has(f + ',' + c)) oscuras.push(1);
    const seVen = [...faroles].some(k => { const [f, c] = k.split(',').map(Number); return vista(f, c).some(v => faroles.has(v)); });
    const sol = new Set(D.solucion.map(([f, c]) => f + ',' + c));
    const bien = faroles.size === sol.size && [...faroles].every(k => sol.has(k));
    if (bien) {
      ui.say('¡El camino de ronda brilla entero, como un collar de luces! Marca de los faroles: ' + D.marca + '. Coged la carta 24.', 'ok');
      celdas.flat().forEach(b => { b.disabled = true; });
    } else if (oscuras.length) {
      ui.say('Aún quedan losas a oscuras: un coloso podría acercarse por ahí.', 'bad');
    } else if (seVen) {
      ui.say('Dos faroles se ven de frente y se deslumbran. Así no.', 'bad');
    } else {
      ui.say('Todo iluminado... pero alguna torre no tiene los faroles que dice el plano.', 'bad');
    }
  });
  ui.button('Apagar todo', 'ghost', () => { faroles.clear(); pintar(); ui.say('', ''); });
  pintar();
  return { close: ui.close };
}
