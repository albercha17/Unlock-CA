// Carta 51 — El collar de mamá: un collar de cien cuentas cuyos colores se repiten siempre igual. La nota de mamá (carta 26) hace dos preguntas: de qué
// color es la última cuenta y cuántas son azules; las primeras cuentas están dibujadas en las dos láminas (cartas 61 y 63). instancias_juguetes.py, COLLAR.
import { openGame } from './ui.js';
import { estilo, opcion } from './comun.js';

const D = /*DATOS*/{"colores": ["rojo", "azul", "verde", "amarillo", "morado"], "ultimo": "morado", "azules": 29}/*FIN*/;
const HEX = { rojo: '#d63430', azul: '#2c68c4', verde: '#3aa054', amarillo: '#f6c42a', morado: '#8a4cc4' };

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 51 — El collar de mamá', instr: 'Elegid el color de la última cuenta del collar de cien cuentas y escribid cuántas cuentas azules lleva. La nota de mamá está en la carta 26 y las primeras cuentas, en las cartas 61 y 63.', ...opts });
  estilo('ju-col', '.col-c{display:flex;gap:8px;justify-content:center;margin:8px 0}.col-c button{width:52px;height:52px;border-radius:50%;border:4px solid #1a2a5a;padding:0;cursor:pointer}.col-c button.sel{outline:4px solid #fff}');
  let color = null, resuelto = false;
  const fila = document.createElement('div');
  fila.className = 'col-c';
  const bs = D.colores.map(c => {
    const b = document.createElement('button');
    b.type = 'button';
    b.dataset.c = c;
    b.style.background = HEX[c];
    b.setAttribute('aria-label', 'Cuenta ' + c);
    b.addEventListener('click', () => { if (resuelto) return; color = c; ui.say(''); pintar(); });
    fila.appendChild(b);
    return b;
  });
  const etq = document.createElement('div');
  etq.className = 'ju-pie';
  etq.textContent = 'Cuentas azules en las cien';
  const entrada = document.createElement('input');
  entrada.type = 'number';
  entrada.min = '0';
  entrada.max = '100';
  entrada.value = '0';
  entrada.className = 'ju-in';
  entrada.setAttribute('aria-label', 'Cuentas azules');
  entrada.addEventListener('input', () => ui.say(''));
  ui.body.append(fila, etq, entrada);
  function pintar() { bs.forEach(b => b.classList.toggle('sel', b.dataset.c === color)); }
  ui.button('Enhebrar el collar', 'primary', () => {
    if (resuelto) return;
    if (!color) { ui.say('Elegid primero el color de la última cuenta.', 'bad'); return; }
    if (color !== D.ultimo) { ui.say('Esa no es la última cuenta: contad con cuidado cómo se repiten los colores hasta llegar a la cien.', 'bad'); return; }
    if (Number(entrada.value) !== D.azules) { ui.say('La última cuenta es buena, pero el número de cuentas azules no sale: contad las de cada vuelta del patrón.', 'bad'); return; }
    resuelto = true;
    ui.say('El collar queda completo, con las cien cuentas bien puestas, y la mamá de Leo lo cuelga del cabecero de la cama. Coged la carta 58.', 'ok');
  });
  pintar();
  return { close: ui.close };
}
