// Carta 14 — Los cubos de Leo: cuatro cubos en 2 x 2; cada cara lleva un cuarto de un dibujo. Tocando un cubo se gira a la cara
// siguiente. Hay que formar el dibujo de la tapa de la caja (carta 16). Caras de herramientas/instancias_juguetes.py (CUBOS). Nota de la nana: C.nota.
import { openGame } from './ui.js';

const C = /*DATOS*/{"dibujos": ["perro", "barco", "casa", "sol", "cohete", "arbol"], "caras": [["cohete", "perro", "casa", "barco", "sol", "arbol"], ["perro", "barco", "casa", "arbol", "sol", "cohete"], ["cohete", "sol", "perro", "barco", "arbol", "casa"], ["casa", "perro", "sol", "barco", "arbol", "cohete"]], "objetivo": "perro", "inicial": [4, 2, 3, 3], "nota": "MI"}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 14 — Los cubos de Leo',
    instr: 'Tocad un cubo para girarlo y ver otra cara. Formad entre los cuatro el dibujo de la tapa de la caja (carta 16).',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .jug-cubos{display:grid;grid-template-columns:1fr 1fr;gap:6px;width:min(72vw,260px);margin:8px auto;padding:8px;border-radius:12px;background:#8a5a30;border:4px solid #ffcc33}
    .jug-cubo{aspect-ratio:1;border:3px solid #4a2a10;border-radius:8px;padding:0;cursor:pointer;background:#fff center / cover no-repeat;transition:transform .2s}
    .jug-cubo.gira{transform:rotateY(90deg)}
    .jug-cubos.ok{border-color:#7be495;box-shadow:0 0 24px rgba(123,228,149,.6)}
    @media (prefers-reduced-motion:reduce){.jug-cubo{transition:none}}
  `;
  ui.body.appendChild(style);
  const caja = document.createElement('div');
  caja.className = 'jug-cubos';
  ui.body.appendChild(caja);

  const cara = C.inicial.slice();
  let resuelto = false;
  const cubos = [0, 1, 2, 3].map(i => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'jug-cubo';
    b.dataset.i = String(i);
    b.addEventListener('click', () => {
      if (resuelto) return;
      cara[i] = (cara[i] + 1) % C.caras[i].length;
      b.classList.add('gira');
      setTimeout(() => { b.classList.remove('gira'); pintar(); }, 160);
      ui.say('');
      comprobar();
    });
    caja.appendChild(b);
    return b;
  });

  function pintar() {
    cubos.forEach((b, i) => {
      const d = C.caras[i][cara[i]];
      b.style.backgroundImage = "url('./img/ui/cubo-" + d + '-' + i + ".png')";
      b.dataset.d = d;
      b.setAttribute('aria-label', 'Cubo ' + (i + 1) + ': trozo de ' + d);
    });
  }
  function comprobar() {
    if (cara.every((c, i) => C.caras[i][c] === C.objetivo)) {
      resuelto = true;
      setTimeout(() => {
        pintar();
        caja.classList.add('ok');
        ui.say('¡Guau! Aparece Trufo entero y el baúl se abre con un clic. Dentro hay un collar de cuentas roto y una nota de la mamá de Leo. Nota de los cubos: ' + C.nota + '. Coged la carta 24.', 'ok');
      }, 200);
    }
  }
  pintar();
  return { close: ui.close };
}
