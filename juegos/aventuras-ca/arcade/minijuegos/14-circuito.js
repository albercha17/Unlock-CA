// Carta 14 — El circuito de la placa: seis interruptores (A a F) y siete puertas lógicas; hay que dejar la lámpara X encendida y la Y apagada.
// El esquema, solo en la carta 16. Solución única comprobada por herramientas/instancias_arcade.py. Byte de la máquina: el de D.dato.
import { openGame } from './ui.js';
import { estilo } from './maquina.js';

const D = /*DATOS*/{"puertas": [["P1", "NOR", "A", "B"], ["P2", "NAND", "C", "D"], ["P3", "OR", "E", "F"], ["P4", "XOR", "P2", "P3"], ["P5", "AND", "P1", "P2"], ["P6", "NOR", "P4", "P5"], ["P7", "NOR", "P4", "P1"]], "salidas": {"X": "P6", "Y": "P7"}, "solucion": [0, 0, 1, 1, 0, 0], "dato": 6}/*FIN*/;
const OPS = { AND: (a, b) => a & b, OR: (a, b) => a | b, XOR: (a, b) => a ^ b, NAND: (a, b) => 1 - (a & b), NOR: (a, b) => 1 - (a | b) };

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 14 — El circuito de la placa', instr: 'Poned cada interruptor arriba (1) o abajo (0) y probad la placa. Las lámparas tienen que quedar como dice el esquema de la carta 16.', ...opts });
  estilo('ar-cir', `
    .cir-fila{display:grid;grid-template-columns:repeat(6,1fr);gap:8px;max-width:340px;margin:8px auto}
    .cir-sw{border-radius:10px;border:3px solid #00e2ff;background:#1c0a30;color:#8ffcff;padding:8px 0 6px;cursor:pointer;font:700 1.1rem ui-monospace,monospace}
    .cir-sw small{display:block;font-size:.65rem;color:#ffd6f6;margin-bottom:4px}
    .cir-sw[data-v="1"]{background:#00e2ff;color:#04141a}
    .cir-sw[data-v="1"] small{color:#04141a}
  `);
  const estado = [1, 1, 1, 1, 1, 1];
  let resuelto = false;
  const fila = document.createElement('div');
  fila.className = 'cir-fila';
  const sw = 'ABCDEF'.split('').map((l, i) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'cir-sw';
    b.dataset.i = String(i);
    b.innerHTML = '<small>' + l + '</small><span></span>';
    b.setAttribute('aria-label', 'Interruptor ' + l);
    b.addEventListener('click', () => { if (resuelto) return; estado[i] ^= 1; ui.say(''); pintar(); });
    fila.appendChild(b);
    return b;
  });
  function pintar() { sw.forEach((b, i) => { b.dataset.v = String(estado[i]); b.lastChild.textContent = String(estado[i]); }); }
  ui.body.appendChild(fila);
  const nota = document.createElement('div');
  nota.className = 'ar-pie';
  nota.textContent = 'Lámparas X e Y: se miran al probar.';
  ui.body.appendChild(nota);
  function evaluar() {
    const v = {};
    'ABCDEF'.split('').forEach((l, i) => { v[l] = estado[i]; });
    D.puertas.forEach(([n, op, a, b]) => { v[n] = OPS[op](v[a], v[b]); });
    return { X: v[D.salidas.X], Y: v[D.salidas.Y] };
  }
  ui.button('Probar la placa', 'primary', () => {
    if (resuelto) return;
    const r = evaluar();
    if (r.X === 1 && r.Y === 0) {
      resuelto = true;
      ui.say('La lámpara X se enciende y la Y se apaga: la placa responde. Byte de la máquina: ' + D.dato + '. Coged la carta 24.', 'ok');
    } else if (r.X === 0 && r.Y === 0) ui.say('Las dos lámparas están apagadas: la placa no da señal (esquema de la carta 16).', 'bad');
    else if (r.X === 1) ui.say('Se enciende X, pero también Y: tiene que quedar apagada (carta 16).', 'bad');
    else ui.say('Se enciende solo la lámpara Y: justo al revés de lo que pide el esquema (carta 16).', 'bad');
  });
  ui.button('Todo abajo', 'ghost', () => { if (!resuelto) { estado.fill(0); ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
