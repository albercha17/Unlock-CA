// Carta 20 — La persecución por Montecarlo: el camino más rápido del Casino (A) al Puerto (I) por unas calles con minutos, sin pasar por las glorietas que
// corta el desfile. El acertijo, en la carta 18 y el plano, en las cartas 19 y 21 (dos mitades). Aquí solo se marcan las glorietas, sin calles ni minutos
// (instancias_espia.py, RUTA).
import { openGame } from './ui.js';

const D = /*DATOS*/{"nodos": ["A", "B", "C", "D", "E", "F", "G", "H", "I"], "aristas": [[0, 1, 4], [0, 3, 8], [1, 2, 6], [1, 4, 9], [2, 5, 9], [3, 4, 4], [3, 6, 5], [4, 5, 2], [4, 7, 7], [5, 8, 4], [6, 7, 5], [7, 8, 5]], "cerrados": [1, 5], "mejor": 23}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 20 — La persecución', instr: 'Marcad en orden las glorietas del camino, desde el Casino (A) hasta el Puerto (I). El acertijo está en la carta 18 y el plano, en las cartas 19 y 21.', ...opts });
  let ruta = [], resuelto = false;
  const mapa = new Map();
  D.aristas.forEach(([a, b, w]) => { mapa.set(a + '-' + b, w); mapa.set(b + '-' + a, w); });
  const cuadro = document.createElement('div');
  cuadro.className = 'es-rejilla';
  cuadro.style.gridTemplateColumns = 'repeat(3,1fr)';
  const botones = D.nodos.map((n, k) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'es-cel es-nodo';
    b.dataset.n = n;
    b.textContent = n;
    b.setAttribute('aria-label', 'Glorieta ' + n);
    b.addEventListener('click', () => { if (resuelto) return; ruta.push(k); ui.say(''); pintar(); });
    cuadro.appendChild(b);
    return b;
  });
  const linea = document.createElement('div');
  linea.className = 'es-pie';
  ui.body.append(cuadro, linea);
  function pintar() {
    linea.textContent = ruta.length ? 'Camino: ' + ruta.map(k => D.nodos[k]).join(' → ') : 'Camino: (vacío)';
    botones.forEach((b, k) => b.classList.toggle('sel', ruta[ruta.length - 1] === k));
  }
  ui.button('Salir de caza', 'primary', () => {
    if (resuelto) return;
    if (ruta.length < 2) { ui.say('Marcad primero el camino, desde la A.', 'bad'); return; }
    if (ruta[0] !== 0) { ui.say('El camino tiene que empezar en el Casino (A).', 'bad'); return; }
    let total = 0;
    for (let i = 1; i < ruta.length; i++) {
      const w = mapa.get(ruta[i - 1] + '-' + ruta[i]);
      if (w === undefined) { ui.say('Entre ' + D.nodos[ruta[i - 1]] + ' y ' + D.nodos[ruta[i]] + ' no hay calle: el coche se queda parado.', 'bad'); return; }
      total += w;
    }
    if (ruta.some(k => D.cerrados.includes(k))) { ui.say('Ese camino pasa por una glorieta cortada por el desfile: la policía os para.', 'bad'); return; }
    if (ruta[ruta.length - 1] !== D.nodos.length - 1) { ui.say('El camino no llega al Puerto (I).', 'bad'); return; }
    if (total !== D.mejor) { ui.say('Llegáis en ' + total + ' minutos, pero hay un camino más rápido: el yate sale antes.', 'bad'); return; }
    resuelto = true;
    ui.say('Llegáis al Puerto en ' + total + ' minutos, justo a tiempo. Coged la carta 28.', 'ok');
  });
  ui.button('Quitar la última', 'ghost', () => { if (!resuelto) { ruta.pop(); ui.say(''); pintar(); } });
  ui.button('Empezar de nuevo', 'ghost', () => { if (!resuelto) { ruta = []; ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
