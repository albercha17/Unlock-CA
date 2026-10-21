// Carta 51 — Las cuatro hadas: las de ala azul siempre dicen la verdad y las de ala roja siempre mienten.
// Frases: Brisa en la carta 26 (chismes de Doña Hogaza), Lila en la 61, Nube en la 63 y Dalia aquí (en la app). Solución única (comprobada con generadores_puzles.caballeros(4, 13)):
// Brisa y Dalia de ala azul; Lila y Nube de ala roja. Letra del libro: I.
import { openGame } from './ui.js';
import { guardarLetra, estilo, conImagen } from './libro.js';

const LETRA = 'I';
const HADAS = [
  { n: 'Brisa', real: 'azul', frase: null },
  { n: 'Lila', real: 'roja', frase: null },
  { n: 'Nube', real: 'roja', frase: null },
  { n: 'Dalia', real: 'azul', frase: '«Al menos una de Brisa y Nube es de ala azul.»' }
];

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 51 — Las cuatro hadas',
    instr: 'Marca el ala de cada hada tocándola: sin marca, azul (dice siempre la verdad) o roja (miente siempre). Lo que dijeron Brisa, Lila y Nube está en las cartas 26, 61 y 63; lo de Dalia, aquí.',
    ...opts
  });
  estilo('cu-hadas-estilo', `
    .had-fila{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin-bottom:8px}
    .had-hada{position:relative;min-height:132px;border-radius:14px;border:2px solid rgba(255,224,138,.4);background:rgba(255,255,255,.07);color:#fff;font:700 .95rem inherit;font-family:inherit;padding:8px 6px 6px;cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:4px;text-align:center}
    .had-hada[data-m="azul"]{border-color:#6fb6ff;background:rgba(90,160,255,.2)}
    .had-hada[data-m="roja"]{border-color:#ff7c8f;background:repeating-linear-gradient(45deg,rgba(255,110,130,.2) 0 8px,rgba(255,110,130,.08) 8px 16px)}
    .had-cuerpo{position:relative;width:62px;height:56px}
    .had-ala{position:absolute;top:6px;width:30px;height:40px;border-radius:60% 40% 60% 40%;background:rgba(255,255,255,.35);border:2px solid rgba(255,255,255,.5)}
    .had-ala.l{left:0;transform:rotate(-18deg)}.had-ala.r{right:0;transform:scaleX(-1) rotate(-18deg)}
    .had-hada[data-m="azul"] .had-ala{background:rgba(90,160,255,.75);border-color:#cfe6ff}
    .had-hada[data-m="roja"] .had-ala{background:rgba(255,100,120,.75);border-color:#ffd0d6}
    .had-cara{position:absolute;left:19px;top:14px;width:24px;height:24px;border-radius:50%;background:#ffd9b8;border:2px solid rgba(0,0,0,.3)}
    .had-cara::before,.had-cara::after{content:"";position:absolute;top:9px;width:4px;height:4px;border-radius:50%;background:#2a1450}
    .had-cara::before{left:5px}.had-cara::after{right:5px}
    .had-estado{font-size:.78rem;min-height:1.1em;letter-spacing:.03em}
    .had-globo{font-weight:600;font-size:.76rem;line-height:1.25;background:rgba(255,255,255,.14);border-radius:10px;padding:5px 7px;margin-top:2px}
    .had-img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.5;pointer-events:none}
  `);

  const fila = document.createElement('div');
  fila.className = 'had-fila';
  ui.body.appendChild(fila);
  const marcas = {};
  let resuelto = false;
  const nodos = [];

  HADAS.forEach((h, i) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'had-hada';
    b.dataset.n = String(i);
    b.dataset.m = '';
    b.innerHTML = '<span class="had-cuerpo"><i class="had-ala l"></i><i class="had-ala r"></i><i class="had-cara"></i></span><span>' + h.n + '</span><span class="had-estado"></span>' +
      (h.frase ? '<span class="had-globo">' + h.frase + '</span>' : '<span class="had-globo">Su frase está en una carta.</span>');
    b.addEventListener('click', () => {
      if (resuelto) return;
      const orden = ['', 'azul', 'roja'];
      marcas[i] = orden[(orden.indexOf(marcas[i] || '') + 1) % 3];
      ui.say('');
      pintar();
    });
    fila.appendChild(b);
    nodos.push(b);
    conImagen(b, 'hadas/' + h.n.toLowerCase() + '.jpg', { clase: 'had-img', mezcla: 'screen' });
  });

  function pintar() {
    nodos.forEach((b, i) => {
      const m = marcas[i] || '';
      b.dataset.m = m;
      b.querySelector('.had-estado').textContent = m === 'azul' ? 'Ala azul: dice la verdad' : m === 'roja' ? 'Ala roja: miente' : 'Sin marcar';
      b.setAttribute('aria-label', HADAS[i].n + ': ' + (m === 'azul' ? 'ala azul' : m === 'roja' ? 'ala roja' : 'sin marcar'));
    });
  }

  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    const sin = HADAS.filter((_, i) => !marcas[i]).length;
    if (sin) { ui.say('Faltan ' + sin + ' hada' + (sin > 1 ? 's' : '') + ' por marcar.', 'bad'); return; }
    const mal = HADAS.filter((h, i) => marcas[i] !== h.real).length;
    if (!mal) {
      resuelto = true;
      guardarLetra('51', LETRA);
      ui.say('¡Eso es! Lila y Nube mienten y Brisa y Dalia dicen la verdad. Las hadas de ala azul os cuentan su secreto. Coged la carta 58. Letra del libro: ' + LETRA + '.', 'ok');
    } else {
      ui.say('Alguna frase no cuadra con esa marca: si un hada es de ala azul su frase debe ser verdad, y si es de ala roja, mentira. Revisad cada una.', 'bad');
    }
  });
  ui.button('Quitar marcas', 'ghost', () => { if (!resuelto) { Object.keys(marcas).forEach((k) => delete marcas[k]); ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
