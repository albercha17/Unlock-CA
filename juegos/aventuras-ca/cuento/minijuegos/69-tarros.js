// Carta 69 — Tarros de colores: cinco tarros con capas de pintura mezcladas (rosa, dorado y turquesa). Se vierte la capa de arriba de un tarro
// sobre otro si es del mismo color o si el otro está vacío. Hay que dejar cada color en un tarro, en el orden del tapiz (carta 70) y la nota de la cocinera (71)
// y los dos últimos vacíos. 11 movimientos mínimos (BFS en herramientas/instancias_cuento.py).
// Cada color lleva además una forma (círculo, estrella, rombo) para no depender solo del color. Letra del libro: E.
import { openGame } from './ui.js';
import { guardarLetra, estilo, conImagen } from './libro.js';

const LETRA = 'E';
const CAP = 4;
const COLORES = [
  { n: 'rosa', c: '#ff7eb6', forma: 'circulo' },
  { n: 'dorado', c: '#ffcf3a', forma: 'estrella' },
  { n: 'turquesa', c: '#2fd1c5', forma: 'rombo' }
];
const INICIAL = [[0, 1, 2, 0], [1, 2, 1, 1], [0, 2, 2, 0], [], []];
const ORDEN = [1, 2, 0];

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 69 — Tarros de colores',
    instr: 'Toca un tarro y luego otro para verter la capa de arriba. Solo se puede verter sobre un tarro vacío o sobre una capa del mismo color. Dejad los colores como dicen las cartas 70 y 71.',
    ...opts
  });
  estilo('cu-tarros-estilo', `
    .tar-fila{position:relative;display:flex;gap:8px;justify-content:center;align-items:flex-end;margin:6px 0 10px}
    .tar-tubo{position:relative;width:54px;height:${CAP * 34 + 16}px;padding:6px 4px;border-radius:8px 8px 18px 18px;border:3px solid rgba(255,255,255,.55);background:rgba(255,255,255,.07);display:flex;flex-direction:column-reverse;gap:2px;cursor:pointer;box-shadow:inset 0 0 12px rgba(255,255,255,.1);min-width:0}
    .tar-tubo.sel{border-color:#ffe08a;box-shadow:0 0 16px rgba(255,224,138,.75),inset 0 0 12px rgba(255,224,138,.25);transform:translateY(-8px)}
    .tar-capa{position:relative;height:30px;border-radius:6px;background:var(--c);border:1px solid rgba(0,0,0,.3);box-shadow:inset 0 3px 6px rgba(255,255,255,.35)}
    .tar-capa::after{content:"";position:absolute;left:50%;top:50%;width:14px;height:14px;transform:translate(-50%,-50%);background:rgba(40,16,70,.65)}
    .tar-capa.circulo::after{border-radius:50%}
    .tar-capa.estrella::after{clip-path:polygon(50% 0,61% 35%,98% 35%,68% 57%,79% 91%,50% 70%,21% 91%,32% 57%,2% 35%,39% 35%)}
    .tar-capa.rombo::after{clip-path:polygon(50% 0,100% 50%,50% 100%,0 50%)}
    .tar-num{position:absolute;bottom:-20px;left:0;right:0;text-align:center;font-size:.75rem;color:#ffe08a}
    .tar-info{font-size:.85rem;color:#d8e2ee;margin:14px 0 2px}
    .tar-img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.4;pointer-events:none;border-radius:8px}
  `);

  const fila = document.createElement('div');
  fila.className = 'tar-fila';
  const info = document.createElement('div');
  info.className = 'tar-info';
  ui.body.append(fila, info);

  let tubos, sel, movs, historial;
  let resuelto = false;

  function pintar() {
    fila.replaceChildren();
    tubos.forEach((t, i) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'tar-tubo' + (sel === i ? ' sel' : '');
      b.dataset.i = String(i);
      b.setAttribute('aria-label', 'Tarro ' + (i + 1) + (t.length ? ': ' + t.map((c) => COLORES[c].n).join(', ') + ' (de abajo arriba)' : ': vacío') + (sel === i ? ', elegido' : ''));
      t.forEach((c) => {
        const k = document.createElement('div');
        k.className = 'tar-capa ' + COLORES[c].forma;
        k.dataset.c = String(c);
        k.style.setProperty('--c', COLORES[c].c);
        b.appendChild(k);
      });
      const n = document.createElement('span');
      n.className = 'tar-num';
      n.textContent = String(i + 1);
      b.appendChild(n);
      b.addEventListener('click', () => tocar(i));
      fila.appendChild(b);
    });
    info.textContent = 'Movimientos: ' + movs;
  }

  function verter(a, b) {
    const ta = tubos[a], tb = tubos[b];
    if (!ta.length) { ui.say('El tarro ' + (a + 1) + ' está vacío: no hay nada que verter.', 'bad'); return false; }
    if (tb.length >= CAP) { ui.say('El tarro ' + (b + 1) + ' está lleno.', 'bad'); return false; }
    if (tb.length && tb[tb.length - 1] !== ta[ta.length - 1]) { ui.say('No se puede verter ' + COLORES[ta[ta.length - 1]].n + ' sobre ' + COLORES[tb[tb.length - 1]].n + ': las capas de arriba deben ser del mismo color.', 'bad'); return false; }
    let k = 1;
    while (k < ta.length && ta[ta.length - 1 - k] === ta[ta.length - 1]) k++;
    k = Math.min(k, CAP - tb.length);
    historial.push(JSON.stringify(tubos));
    const mover = ta.splice(ta.length - k, k);
    tb.push(...mover);
    movs++;
    return true;
  }

  function tocar(i) {
    if (resuelto) return;
    if (sel === null) {
      if (!tubos[i].length) { ui.say('Ese tarro está vacío.', ''); return; }
      sel = i; ui.say(''); pintar(); return;
    }
    if (sel === i) { sel = null; pintar(); return; }
    const a = sel;
    sel = null;
    if (verter(a, i)) ui.say('');
    pintar();
    comprobar();
  }

  function comprobar() {
    const ok = ORDEN.every((c, i) => tubos[i].length === CAP && tubos[i].every((x) => x === c)) && tubos[3].length === 0 && tubos[4].length === 0;
    if (ok) {
      resuelto = true;
      guardarLetra('69', LETRA);
      ui.say('¡Los colores vuelven al cuento en el orden de la Cocinera: dorado, turquesa y rosa! El castillo recobra su color. Coged la carta 80. Letra del libro: ' + LETRA + '.', 'ok');
      return;
    }
    // todos los tarros de un solo color pero en otro orden: aviso con razón
    const entero = tubos.every((t) => t.length === 0 || (t.length === CAP && new Set(t).size === 1));
    if (entero) ui.say('Cada color está en su tarro, pero no como quiere la Cocinera Real (cartas 70 y 71).', 'bad');
  }

  function inicio() { tubos = INICIAL.map((t) => t.slice()); sel = null; movs = 0; historial = []; resuelto = false; ui.say(''); pintar(); }
  ui.button('Deshacer', 'ghost', () => { if (!resuelto && historial.length) { tubos = JSON.parse(historial.pop()); movs = Math.max(0, movs - 1); sel = null; ui.say(''); pintar(); } });
  ui.button('Empezar de nuevo', 'ghost', inicio);
  conImagen(fila, 'tarros.jpg', { clase: 'tar-img', mezcla: 'screen' });
  inicio();
  return { close: ui.close };
}
