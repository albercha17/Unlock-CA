// Carta 58 — Cisterna: dos jarras (3 y 5 medidas) y un grifo. Hay que dejar justo 4 medidas en la jarra grande (nota, carta 60).
// Solución mínima (6 pasos): llenar la grande; verter en la pequeña; vaciar la pequeña; verter en la pequeña; llenar la grande; verter en la pequeña.
import { openGame } from './ui.js';

const CAP = { pequena: 3, grande: 5 };
const OBJETIVO = 4;

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 58 — Cisterna',
    instr: 'Llena, vacía o vierte una jarra en otra hasta dejar la cantidad que pide la nota en la jarra grande.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .far-j-jarras{display:flex;gap:26px;justify-content:center;align-items:flex-end;margin:6px 0 12px}
    .far-j-jarra{display:flex;flex-direction:column;align-items:center;gap:6px;font-weight:700;color:#e8d9b0}
    .far-j-vaso{display:flex;flex-direction:column-reverse;gap:3px;padding:6px;border:3px solid #8a5a2a;border-top:none;border-radius:0 0 22px 22px;background:#1b1209}
    .far-j-medida{width:62px;height:30px;border-radius:5px;background:rgba(255,255,255,.07)}
    .far-j-medida.llena{background:linear-gradient(180deg,#5fb7ff,#2a7fd0)}
    .far-j-pasos{text-align:center;color:#9fb4c8;font-size:.85rem;margin-bottom:8px}
    .far-j-acciones{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:6px}
  `;
  ui.body.appendChild(style);

  const jarras = document.createElement('div');
  jarras.className = 'far-j-jarras';
  const pasos = document.createElement('div');
  pasos.className = 'far-j-pasos';
  const acciones = document.createElement('div');
  acciones.className = 'far-j-acciones';
  ui.body.append(jarras, pasos, acciones);

  let nivel = { pequena: 0, grande: 0 };
  let n = 0;
  let resuelto = false;

  function pintar() {
    jarras.innerHTML = '';
    ['pequena', 'grande'].forEach(k => {
      const col = document.createElement('div');
      col.className = 'far-j-jarra';
      col.dataset.jarra = k;
      const vaso = document.createElement('div');
      vaso.className = 'far-j-vaso';
      for (let i = 0; i < CAP[k]; i++) {
        const m = document.createElement('div');
        m.className = 'far-j-medida' + (i < nivel[k] ? ' llena' : '');
        vaso.appendChild(m);
      }
      const t = document.createElement('div');
      t.className = 'far-j-texto';
      t.textContent = (k === 'pequena' ? 'Pequeña' : 'Grande') + ' (' + CAP[k] + '): ' + nivel[k];
      col.append(vaso, t);
      jarras.appendChild(col);
    });
    pasos.textContent = 'Movimientos: ' + n;
  }

  function accion(f) {
    if (resuelto) return;
    f();
    n++;
    pintar();
    if (nivel.grande === OBJETIVO) {
      resuelto = true;
      ui.say('La jarra grande guarda justo cuatro medidas. La compuerta cede con un crujido y aparece una escalera de caracol hacia la azotea. Coged la carta 74.', 'ok');
      acciones.querySelectorAll('button').forEach(b => { b.disabled = true; });
    } else {
      ui.say('');
    }
  }

  const verter = (de, a) => () => {
    const t = Math.min(nivel[de], CAP[a] - nivel[a]);
    nivel[de] -= t;
    nivel[a] += t;
  };

  [
    ['Llenar pequeña', () => { nivel.pequena = CAP.pequena; }],
    ['Llenar grande', () => { nivel.grande = CAP.grande; }],
    ['Vaciar pequeña', () => { nivel.pequena = 0; }],
    ['Vaciar grande', () => { nivel.grande = 0; }],
    ['Verter pequeña → grande', verter('pequena', 'grande')],
    ['Verter grande → pequeña', verter('grande', 'pequena')]
  ].forEach(([txt, f]) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'far-btn ghost';
    b.textContent = txt;
    b.addEventListener('click', () => accion(f));
    acciones.appendChild(b);
  });

  ui.button('Empezar de nuevo', 'ghost', () => {
    if (resuelto) return;
    nivel = { pequena: 0, grande: 0 };
    n = 0;
    ui.say('');
    pintar();
  });

  pintar();
  return { close: ui.close };
}
