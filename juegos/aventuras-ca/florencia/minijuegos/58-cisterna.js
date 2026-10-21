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
    .far-j-vaso{position:relative}
    .far-j-vaso img{position:relative;z-index:2;display:block;width:100%;height:100%;object-fit:fill;mix-blend-mode:screen}
    .far-j-agua{position:absolute;left:9%;right:9%;bottom:7%;z-index:1;border-radius:0 0 10px 10px;background:linear-gradient(180deg,#7cc8ff,#2a7fd0 70%,#1b5aa0);box-shadow:0 0 14px rgba(95,183,255,.55);transition:height .55s cubic-bezier(.3,1.3,.5,1)}
    .far-j-marcas{position:absolute;left:9%;right:9%;bottom:7%;z-index:3;pointer-events:none}
    .far-j-marcas i{position:absolute;left:0;right:0;border-top:1px dashed rgba(255,255,255,.35)}
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
      vaso.style.width = (k === 'pequena' ? 118 : 96) + 'px';
      vaso.style.height = (k === 'pequena' ? 106 : 200) + 'px';
      // el agua ocupa el 86 % útil del vaso: cada medida es una fracción igual
      const util = 86;
      const agua = document.createElement('div');
      agua.className = 'far-j-agua';
      agua.dataset.nivel = String(nivel[k]);
      agua.style.height = (nivel[k] / CAP[k] * util) + '%';
      const marcas = document.createElement('div');
      marcas.className = 'far-j-marcas';
      marcas.style.height = util + '%';
      for (let i = 1; i < CAP[k]; i++) { const m = document.createElement('i'); m.style.bottom = (i / CAP[k] * 100) + '%'; marcas.appendChild(m); }
      vaso.innerHTML = '<img alt="" src="./img/ui/vasos/' + (k === 'pequena' ? 'vaso3' : 'vaso5') + '.jpg">';
      vaso.append(agua, marcas);
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
      ui.say('La jarra grande guarda justo cuatro medidas. La compuerta cede con un crujido y aparece una escalera de caracol... atascada de cajas. Coged la carta 44.', 'ok');
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
