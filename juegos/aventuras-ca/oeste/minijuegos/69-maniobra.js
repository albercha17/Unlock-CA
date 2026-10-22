// Carta 69 — La maniobra de vagones: siete vagones de colores esperan en fila; hay un apartadero ciego (el último que entra es el primero que sale) y el
// tren tiene que salir ordenado del más ligero al más pesado. Los pesos de cada color, en la carta 70; la regla, en la 71. Vale cualquier maniobra
// (instancias_oeste.py, VAGONES). Coordenada de Polibio: D.coord.
import { openGame } from './ui.js';
import { estilo, COLORES } from './comun.js';

const D = /*DATOS*/{"pesos": [1, 5, 3, 2, 4, 6, 7], "coord": "34"}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 69 — La maniobra de vagones', instr: 'Pasad vagones de la fila al apartadero y del apartadero a la salida, de uno en uno. Los pesos de cada color están en la carta 70; la regla, en la 71.', ...opts });
  estilo('oe-man', `
    .man-via{display:flex;align-items:center;gap:6px;min-height:50px;margin:6px 0;padding:6px;border-radius:8px;background:#3a2412;border:2px solid #8a5a2a}
    .man-via b{color:#f5d48a;font:700 .75rem Georgia,serif;min-width:74px}
    .man-v{width:34px;height:34px;border-radius:5px;border:3px solid #1c0f06;flex:none}`);
  let cola, pila, salida, resuelto = false;
  function empezar() { cola = D.pesos.map((_, i) => i); pila = []; salida = []; }
  empezar();
  const vias = ['Fila de entrada', 'Apartadero', 'Salida'].map(t => {
    const v = document.createElement('div');
    v.className = 'man-via';
    v.innerHTML = '<b>' + t + '</b>';
    ui.body.appendChild(v);
    return v;
  });
  const btns = document.createElement('div');
  btns.className = 'oe-btns';
  ui.body.appendChild(btns);
  function pintar() {
    [cola, pila, salida].forEach((lista, k) => {
      const v = vias[k];
      v.querySelectorAll('.man-v').forEach(e => e.remove());
      lista.forEach(i => {
        const e = document.createElement('span');
        e.className = 'man-v';
        e.style.background = COLORES[i];
        e.dataset.i = String(i);
        e.setAttribute('aria-label', 'Vagón de color ' + (i + 1));
        v.appendChild(e);
      });
      v.dataset.n = String(lista.length);
    });
  }
  function entrar() {
    if (resuelto) return;
    if (!cola.length) { ui.say('No quedan vagones en la fila de entrada.', 'bad'); return; }
    pila.push(cola.shift());
    ui.say('');
    pintar();
  }
  function sacar() {
    if (resuelto) return;
    if (!pila.length) { ui.say('El apartadero está vacío.', 'bad'); return; }
    salida.push(pila.pop());
    ui.say('');
    pintar();
    if (salida.length === D.pesos.length) {
      const ok = salida.every((v, k) => k === 0 || D.pesos[salida[k - 1]] < D.pesos[v]);
      if (ok) {
        resuelto = true;
        ui.say('El tren sale ordenado, del más ligero al más pesado, y el jefe de estación saca el reloj. Coordenada de Polibio: ' + D.coord + '. Coged la carta 80.', 'ok');
      } else {
        ui.say('El tren sale desordenado: hay un vagón pesado delante de uno más ligero (cartas 70 y 71). Se vuelve a empezar.', 'bad');
        empezar();
        pintar();
      }
    }
  }
  [['Entrar al apartadero', 'man-e', entrar], ['Sacar del apartadero', 'man-s', sacar]].forEach(([t, cl, fn]) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = cl;
    b.textContent = t;
    b.addEventListener('click', fn);
    btns.appendChild(b);
  });
  ui.button('Empezar de nuevo', 'ghost', () => { if (!resuelto) { empezar(); ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
