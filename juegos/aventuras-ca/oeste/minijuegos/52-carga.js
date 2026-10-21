// Carta 52 — La carga del carro (mochila): elegir qué cosas cargar, una vez cada una, para llevar el mayor valor sin pasar el peso que aguanta el eje.
// Los pesos, en la carta 54; los valores, en la 55; lo que aguanta el carro, en la 59. Solución única (instancias_oeste.py, MOCHILA; ni «lo más valioso
// primero» ni «lo mejor por peso» dan el máximo). Coordenada de Polibio: D.coord.
import { openGame } from './ui.js';
import { estilo, COLORES } from './comun.js';

const D = /*DATOS*/{"articulos": ["barril de whisky", "saco de harina", "caja de herramientas", "fardo de pieles", "cajón de balas", "rollo de alambre", "bidón de petróleo", "baúl de plata"], "pesos": [10, 9, 14, 11, 8, 12, 8, 8], "valores": [38, 20, 58, 35, 55, 57, 39, 51], "capacidad": 38, "optimo": 203, "coord": "35"}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 52 — La carga del carro', instr: 'Tocad las cosas que queréis cargar en el carro, una vez cada una. Los pesos, los valores y lo que aguanta el eje están en las cartas 54, 55 y 59.', ...opts });
  estilo('oe-car', `.car-lista{display:grid;gap:6px;max-width:340px;margin:8px auto}.car-art{display:flex;align-items:center;gap:10px;min-height:46px;border-radius:8px;border:3px solid #3a2412;background:#e6c88c;color:#3a2412;font:700 .95rem Georgia,serif;padding:4px 10px;cursor:pointer;text-align:left}.car-art i{width:24px;height:24px;border-radius:4px;border:2px solid #3a2412;flex:none}.car-art[data-v="1"]{background:#b03a2e;color:#fff;border-color:#f5d48a}`);
  const sel = D.articulos.map(() => 0);
  let resuelto = false;
  const lista = document.createElement('div');
  lista.className = 'car-lista';
  lista.setAttribute('aria-label', 'Cosas del almacén');
  const botones = D.articulos.map((nombre, i) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'car-art';
    b.dataset.i = String(i);
    b.innerHTML = '<i style="background:' + COLORES[i] + '"></i><span>' + nombre + '</span>';
    b.addEventListener('click', () => { if (resuelto) return; sel[i] ^= 1; ui.say(''); pintar(); });
    lista.appendChild(b);
    return b;
  });
  const pie = document.createElement('div');
  pie.className = 'oe-pie';
  ui.body.append(lista, pie);
  function pintar() {
    botones.forEach((b, i) => { b.dataset.v = String(sel[i]); });
    pie.textContent = 'Cosas cargadas: ' + sel.reduce((a, b) => a + b, 0);
  }
  ui.button('Cargar el carro', 'primary', () => {
    if (resuelto) return;
    if (!sel.some(v => v)) { ui.say('El carro está vacío.', 'bad'); return; }
    const peso = sel.reduce((a, v, i) => a + v * D.pesos[i], 0);
    const valor = sel.reduce((a, v, i) => a + v * D.valores[i], 0);
    if (peso > D.capacidad) { ui.say('El eje cruje y se rompe: os habéis pasado de peso (carta 59).', 'bad'); return; }
    if (valor < D.optimo) { ui.say('El carro aguanta, pero se puede llevar una cartera más gorda sin romper nada.', 'bad'); return; }
    resuelto = true;
    ui.say('El carro sale cargado hasta el límite y con la mayor ganancia posible. Coordenada de Polibio: ' + D.coord + '. Coged la carta 44.', 'ok');
  });
  ui.button('Descargar todo', 'ghost', () => { if (!resuelto) { sel.fill(0); ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
