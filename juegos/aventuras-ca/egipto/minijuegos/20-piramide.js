// Carta 20 — La pirámide del escriba: poner el peso de las cinco piedras de la base. La pirámide con las piedras que ya tienen su peso
// está en las cartas 19 y 21 (dos mitades) y el acertijo del cantero, en la 18. Solución única (instancias_egipto.py, PIRAMIDE).
import { openGame } from './ui.js';
import { estilo, guardarSello } from './nilo.js';

const D = /*DATOS*/{"n": 5, "filas": [[4, 3, 9, 7, 1], [7, 12, 16, 8], [19, 28, 24], [47, 52], [99]], "dados": [[1, 0], [1, 2], [3, 1], [4, 0]], "solucion": [4, 3, 9, 7, 1]}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 20 — La pirámide del escriba', instr: 'Escribid el peso de las cinco piedras de la base de la pirámide (de izquierda a derecha). El resto de la pirámide, en las cartas 18, 19 y 21.', ...opts });
  estilo('eg-pira', `.pir-base{display:flex;gap:6px;justify-content:center;margin:14px 0}.pir-base input{width:52px;height:52px;text-align:center;border-radius:8px;border:2px solid #d9a441;background:#f6e7bf;color:#2a1f0c;font:800 1.3rem Georgia,serif}`);
  const fila = document.createElement('div'); fila.className = 'pir-base';
  const ins = [];
  for (let i = 0; i < D.n; i++) {
    const e = document.createElement('input'); e.type = 'number'; e.min = '0'; e.max = '99'; e.inputMode = 'numeric'; e.dataset.i = String(i);
    e.setAttribute('aria-label', 'Piedra ' + (i + 1) + ' de la base');
    e.addEventListener('input', () => ui.say(''));
    ins.push(e); fila.appendChild(e);
  }
  ui.body.appendChild(fila);
  let resuelto = false;
  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    const v = ins.map(e => e.value === '' ? null : Number(e.value));
    if (v.includes(null)) { ui.say('Faltan piedras por pesar.', 'bad'); return; }
    if (v.every((x, i) => x === D.solucion[i])) {
      resuelto = true; guardarSello('20');
      ui.say('Las piedras encajan y el muro se desliza hacia un lado, dejando ver una cámara. Coged la carta 28.', 'ok');
    } else ui.say('Con esos pesos, las piedras de arriba no coinciden con las que ya están escritas (cartas 19 y 21).', 'bad');
  });
  return { close: ui.close };
}
