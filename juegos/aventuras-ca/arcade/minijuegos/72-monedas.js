// Carta 72 — Las monedas de la máquina: pagar justo el precio de la partida (carta 79) con el menor número de monedas posible. Los valores de las cuatro
// monedas, en la carta 75 (de la menor a la mayor). La máquina no da cambio. Solución única (instancias_arcade.py, MONEDAS: el método «la mayor que quepa»
// no da el mínimo).
import { openGame } from './ui.js';
import { estilo, contador } from './maquina.js';

const D = /*DATOS*/{"monedas": [1, 15, 16, 20], "precio": 34, "minimo": 4, "solucion": [2, 0, 2, 0]}/*FIN*/;
const NOM = ['la más pequeña', 'la segunda', 'la tercera', 'la mayor'];

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 72 — Las monedas de la máquina', instr: 'Elegid cuántas monedas de cada clase echáis. La máquina no da cambio: hay que pagar justo el precio de la carta 79, con las menos monedas posibles. Los valores están en la carta 75, de la menor a la mayor.', ...opts });
  estilo('ar-mon', `.mon-total{margin:6px auto;text-align:center;font:700 1rem ui-monospace,monospace;color:#ffde46}`);
  let resuelto = false;
  const cont = D.monedas.map((v, i) => contador('Moneda ' + NOM[i], 12, () => { ui.say(''); total(); }, String(v)));
  const tot = document.createElement('div');
  tot.className = 'mon-total';
  tot.setAttribute('aria-label', 'Monedas echadas');
  cont.forEach(c => ui.body.appendChild(c.el));
  ui.body.appendChild(tot);
  function datos() {
    const n = cont.map(c => c.valor());
    return { n, piezas: n.reduce((a, b) => a + b, 0), suma: n.reduce((a, b, i) => a + b * D.monedas[i], 0) };
  }
  function total() { const d = datos(); tot.textContent = 'Monedas echadas: ' + d.piezas; tot.dataset.piezas = String(d.piezas); }
  ui.button('Pagar', 'primary', () => {
    if (resuelto) return;
    const d = datos();
    if (!d.piezas) { ui.say('No habéis echado ninguna moneda.', 'bad'); return; }
    if (d.suma < D.precio) { ui.say('Falta dinero: la máquina sigue pidiendo (carta 79).', 'bad'); return; }
    if (d.suma > D.precio) { ui.say('Os pasáis: la máquina no da cambio y se traga lo que sobra (carta 79).', 'bad'); return; }
    if (d.piezas > D.minimo) { ui.say('Pagáis justo, pero la máquina protesta: se puede hacer con menos monedas.', 'bad'); return; }
    resuelto = true;
    ui.say('Pago justo y con las menos monedas posibles: ' + d.piezas + '. La máquina da una ficha de continuar. Coged la carta 82.', 'ok');
  });
  ui.button('Vaciar', 'ghost', () => { if (!resuelto) { cont.forEach(c => c.poner(0)); ui.say(''); total(); } });
  total();
  return { close: ui.close };
}
