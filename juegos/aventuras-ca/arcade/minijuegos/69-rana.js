// Carta 69 — La rana de la autopista (Frogger por turnos): programar de antemano los pasos de la rana (U arriba, L izquierda, R derecha, W esperar)
// para cruzar cinco carriles sin que la atropellen. Los coches no se ven: su posición al empezar está en la carta 70 y sus velocidades en la 71.
// En cada turno la rana se mueve primero y después avanzan los coches; solo cuenta dónde están al acabar el turno. Vale cualquier ruta correcta.
// Byte de la máquina: el de D.dato (instancias_arcade.py, RANA).
import { openGame } from './ui.js';
import { estilo } from './maquina.js';

const D = /*DATOS*/{"ancho": 8, "carriles": [{"vel": 1, "dir": 1, "coches": [0, 4, 5]}, {"vel": 2, "dir": -1, "coches": [0, 5, 7]}, {"vel": 2, "dir": -1, "coches": [0, 1, 5]}, {"vel": 1, "dir": 1, "coches": [0, 6]}, {"vel": 1, "dir": 1, "coches": [2, 3]}], "inicio": [6, 4], "dato": 12}/*FIN*/;
const MOV = { U: [-1, 0], L: [0, -1], R: [0, 1], W: [0, 0] };

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 69 — La rana de la autopista', instr: 'Programad los pasos de la rana: arriba (U), izquierda (L), derecha (R) o esperar (W). Luego pulsad Ejecutar. El tráfico está en las cartas 70 y 71: no se ve aquí.', ...opts });
  estilo('ar-rana', `
    .rana-prog{display:flex;flex-wrap:wrap;gap:4px;justify-content:center;min-height:44px;margin:6px 0;padding:8px;border-radius:10px;border:2px solid #2ee67a;background:#04140a}
    .rana-paso{width:30px;height:34px;border-radius:6px;background:#12301e;color:#7dffae;font:700 1rem ui-monospace,monospace;display:flex;align-items:center;justify-content:center}
    .rana-tab{display:grid;gap:2px;width:min(84vw,330px);margin:8px auto}
    .rana-c{aspect-ratio:1;border-radius:3px;background:#1e1040}
    .rana-c.meta{background:#1d5a34}.rana-c.rana{background:#5aff96;box-shadow:0 0 8px #5aff96}.rana-c.coche{background:#ff505a}
  `);
  const prog = [];
  let resuelto = false;
  const filas = D.carriles.length + 2;
  const caja = document.createElement('div');
  caja.className = 'rana-prog';
  const tab = document.createElement('div');
  tab.className = 'rana-tab';
  tab.style.gridTemplateColumns = 'repeat(' + D.ancho + ',1fr)';
  const btns = document.createElement('div');
  btns.className = 'ar-btns';
  tab.setAttribute('aria-label', 'La autopista y la rana');
  ui.body.append(tab, caja, btns);
  [['U', '↑ U'], ['L', '← L'], ['R', '→ R'], ['W', '⏸ W']].forEach(([m, t]) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'rana-b';
    b.dataset.m = m;
    b.textContent = t;
    b.addEventListener('click', () => { if (resuelto || prog.length >= 24) return; prog.push(m); ui.say(''); pintar(); });
    btns.appendChild(b);
  });
  function ocupado(carril, col, t) {
    const L = D.carriles[carril];
    return L.coches.some(p => (((p + L.dir * L.vel * t) % D.ancho) + D.ancho) % D.ancho === col);
  }
  function pintar(pos, coches) {
    caja.innerHTML = '';
    prog.forEach(m => { const s = document.createElement('span'); s.className = 'rana-paso'; s.textContent = m; caja.appendChild(s); });
    caja.dataset.prog = prog.join('');
    tab.innerHTML = '';
    const p = pos || D.inicio;
    for (let f = 0; f < filas; f++) for (let c = 0; c < D.ancho; c++) {
      const e = document.createElement('div');
      e.className = 'rana-c' + (f === 0 ? ' meta' : '') + (p[0] === f && p[1] === c ? ' rana' : '') + (coches && f >= 1 && f <= D.carriles.length && ocupado(f - 1, c, coches) ? ' coche' : '');
      tab.appendChild(e);
    }
  }
  function ejecutar() {
    if (resuelto) return;
    if (!prog.length) { ui.say('El programa está vacío: añadid pasos.', 'bad'); return; }
    let f = D.inicio[0], c = D.inicio[1];
    for (let t = 0; t < prog.length; t++) {
      const [df, dc] = MOV[prog[t]];
      f += df; c += dc;
      if (c < 0 || c >= D.ancho) { pintar([f, Math.max(0, Math.min(D.ancho - 1, c))]); ui.say('En el turno ' + (t + 1) + ' la rana se cae por el borde de la autopista.', 'bad'); return; }
      if (f >= 1 && f <= D.carriles.length && ocupado(f - 1, c, t + 1)) {
        pintar([f, c], t + 1);
        ui.say('En el turno ' + (t + 1) + ' la rana acaba en una casilla donde hay un coche. ¡Atropellada!', 'bad');
        return;
      }
      if (f === 0) {
        pintar([0, c]);
        if (t + 1 < prog.length) { ui.say('La rana ya había llegado a la meta en el turno ' + (t + 1) + ': sobran pasos.', 'bad'); return; }
        resuelto = true;
        ui.say('La rana llega sana y salva a la meta en ' + prog.length + ' turnos. Byte de la máquina: ' + D.dato + '. Coged la carta 80.', 'ok');
        return;
      }
    }
    pintar([f, c]);
    ui.say('El programa acaba y la rana se queda a ' + f + (f === 1 ? ' fila' : ' filas') + ' de la meta.', 'bad');
  }
  ui.button('Ejecutar', 'primary', ejecutar);
  ui.button('Quitar el último', 'ghost', () => { if (!resuelto && prog.length) { prog.pop(); ui.say(''); pintar(); } });
  ui.button('Borrar todo', 'ghost', () => { if (!resuelto) { prog.length = 0; ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
