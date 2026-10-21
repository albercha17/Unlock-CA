// Carta 46 — La cuenta de cifras: llegar al objetivo de la trayectoria (carta 39) con las piezas de la carta 37 y las cuatro operaciones; la norma, en la 33.
// En la app solo se opera: tocad una pieza, una operación y otra pieza. Vale cualquier cuenta correcta (instancias_marte.py, CIFRAS).
import { openGame } from './ui.js';
import { estilo } from './cupula.js';

const D = /*DATOS*/{"numeros": [1, 2, 3, 9, 25, 30], "objetivo": 894}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 46 — La cuenta de cifras', instr: 'Tocad una pieza, luego una operación y luego otra pieza: las dos se juntan en una nueva. El objetivo y la norma, en las cartas 37, 39 y 33.', ...opts });
  estilo('mr-cue', `.cue-piezas{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:10px 0;min-height:60px}.cue-p{min-width:54px;height:54px;border-radius:10px;border:3px solid #ff8a50;background:#4a2a1c;color:#ffe6d6;font:800 1.2rem Georgia,serif;cursor:pointer}.cue-p.sel{background:#ff8a50;color:#2a120c}.cue-ops{display:flex;gap:8px;justify-content:center;margin:8px 0}.cue-ops button{width:48px;height:44px;border-radius:10px;border:2px solid #ffe6d6;background:#7a4430;color:#ffe6d6;font:800 1.3rem system-ui;cursor:pointer}.cue-ops button.sel{background:#ffe6d6;color:#2a120c}.cue-hist{text-align:center;color:#ffe6d6;font:600 .8rem system-ui;margin:4px 0;min-height:1.2em}`);
  const piezas = document.createElement('div'); piezas.className = 'cue-piezas';
  const ops = document.createElement('div'); ops.className = 'cue-ops';
  const hist = document.createElement('div'); hist.className = 'cue-hist';
  ui.body.append(piezas, ops, hist);
  let lista = D.numeros.slice(), pasos = [], a = null, op = null, resuelto = false;
  const hechos = [];
  function pintar() {
    piezas.innerHTML = '';
    lista.forEach((v, i) => {
      const b = document.createElement('button'); b.type = 'button'; b.className = 'cue-p' + (a === i ? ' sel' : ''); b.dataset.i = String(i); b.dataset.v = String(v); b.textContent = String(v);
      b.addEventListener('click', () => tocar(i)); piezas.appendChild(b);
    });
    ops.querySelectorAll('button').forEach(b => b.classList.toggle('sel', b.dataset.o === op));
    hist.textContent = pasos.join('   ');
    piezas.dataset.lista = lista.join(',');
  }
  function tocar(i) {
    if (resuelto) return;
    if (a === null) { a = i; pintar(); return; }
    if (a === i) { a = null; op = null; pintar(); return; }
    if (!op) { a = i; pintar(); return; }
    const x = lista[a], y = lista[i];
    let r;
    if (op === '+') r = x + y; else if (op === '×') r = x * y;
    else if (op === '−') { if (x - y <= 0) { ui.say('Los resultados han de ser mayores que cero (carta 33).', 'bad'); a = null; op = null; pintar(); return; } r = x - y; }
    else { if (y === 0 || x % y !== 0) { ui.say('La división tiene que salir exacta (carta 33).', 'bad'); a = null; op = null; pintar(); return; } r = x / y; }
    hechos.push({ lista: lista.slice(), pasos: pasos.slice() });
    pasos.push(x + ' ' + op + ' ' + y + ' = ' + r);
    lista = lista.filter((_, k) => k !== a && k !== i).concat([r]);
    a = null; op = null; ui.say('');
    pintar();
    if (r === D.objetivo) { resuelto = true; ui.say('¡' + D.objetivo + '! La trayectoria queda calculada y el cohete de rescate puede despegar. Coged la carta 56.', 'ok'); }
  }
  ['+', '−', '×', '÷'].forEach(o => {
    const b = document.createElement('button'); b.type = 'button'; b.dataset.o = o; b.textContent = o; b.setAttribute('aria-label', 'Operación ' + o);
    b.addEventListener('click', () => { if (!resuelto && a !== null) { op = op === o ? null : o; pintar(); } });
    ops.appendChild(b);
  });
  ui.button('Deshacer', 'ghost', () => { if (!resuelto && hechos.length) { const h = hechos.pop(); lista = h.lista; pasos = h.pasos; a = null; op = null; ui.say(''); pintar(); } });
  ui.button('Empezar de nuevo', 'ghost', () => { if (!resuelto) { lista = D.numeros.slice(); pasos = []; hechos.length = 0; a = null; op = null; ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
