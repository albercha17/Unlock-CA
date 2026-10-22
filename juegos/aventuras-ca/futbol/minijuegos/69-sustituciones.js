// Carta 69 — Los cambios del míster: ocho jugadores en ocho puestos; el míster da tres órdenes de cambios (ciclos y un intercambio) y las repite tres veces.
// Hay que decir qué dorsal acaba en cada puesto. La alineación inicial, en la carta 70; las órdenes, en la 71 (instancias_futbol.py, SUSTITUCIONES).
// Aro de las flechas: D.aro.
import { openGame } from './ui.js';
import { estilo, opcion } from './comun.js';

const D = /*DATOS*/{"dorsales": [10, 2, 9, 1, 4, 6, 11, 5], "final": [10, 2, 1, 9, 11, 5, 4, 6], "aro": 9}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 69 — Los cambios del míster', instr: 'Elegid un puesto y tocad el dorsal que acaba en él después de todos los cambios. La alineación inicial está en la carta 70 y las órdenes, en la 71.', ...opts });
  estilo('fu-sus', '.sus-p{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;max-width:340px;margin:8px auto}.sus-p button{min-height:52px;font-size:1rem}.sus-d{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;max-width:340px;margin:8px auto}');
  const n = D.dorsales.length;
  const pon = Array(n).fill(null);
  let sel = null, resuelto = false;
  const puestos = document.createElement('div');
  puestos.className = 'sus-p';
  const pb = Array.from({ length: n }, (_, k) => {
    const b = opcion('', () => { if (resuelto) return; sel = k; ui.say(''); pintar(); });
    b.dataset.p = String(k + 1);
    b.setAttribute('aria-label', 'Puesto ' + (k + 1));
    puestos.appendChild(b);
    return b;
  });
  const dors = document.createElement('div');
  dors.className = 'sus-d';
  D.dorsales.slice().sort((a, b) => a - b).forEach(d => {
    const b = opcion(String(d), () => {
      if (resuelto) return;
      if (sel === null) { ui.say('Elegid primero un puesto.', 'bad'); return; }
      const antes = pon.indexOf(d);
      if (antes >= 0) pon[antes] = null;
      pon[sel] = d;
      ui.say('');
      pintar();
    });
    b.dataset.d = String(d);
    dors.appendChild(b);
  });
  ui.body.append(puestos, dors);
  function pintar() { pb.forEach((b, k) => { b.textContent = (k + 1) + ': ' + (pon[k] === null ? '?' : pon[k]); b.classList.toggle('sel', sel === k); b.dataset.v = pon[k] === null ? '' : String(pon[k]); }); }
  ui.button('Presentar la alineación', 'primary', () => {
    if (resuelto) return;
    if (pon.some(v => v === null)) { ui.say('Falta algún puesto.', 'bad'); return; }
    if (pon.some((v, k) => v !== D.final[k])) { ui.say('Esa no es la alineación tras los cambios: rehaced las órdenes del míster paso a paso.', 'bad'); return; }
    resuelto = true;
    ui.say('Esa es la alineación tras todos los cambios. Aro de las flechas: ' + D.aro + '. Coged la carta 80.', 'ok');
  });
  ui.button('Vaciar', 'ghost', () => { if (!resuelto) { pon.fill(null); ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
