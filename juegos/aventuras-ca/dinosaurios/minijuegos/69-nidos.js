// Carta 69 — Huevos y nidos (torres de Hanói): pasar cuatro huevos del nido de ramas al de plumas (carta 70).
// Un huevo solo puede apoyarse en un nido vacío o sobre un huevo más grande. Mínimo: quince movimientos.
import { openGame } from './ui.js';

const NIDOS = [
  { k: 'ramas', nombre: 'Nido de ramas' },
  { k: 'piedras', nombre: 'Nido de piedras' },
  { k: 'plumas', nombre: 'Nido de plumas' }
];
const ANCHO = { 1: 22, 2: 30, 3: 38, 4: 46 };   // tamaño del huevo (1 = el más pequeño)
const IMG = './img/ui/';

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 69 — Huevos y nidos',
    instr: 'Pasa los huevos de uno en uno. Toca un nido para coger su huevo de arriba y toca otro nido para dejarlo. Nunca un huevo grande sobre uno más pequeño.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .nid-cueva{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;max-width:350px;margin:0 auto 8px;padding:10px 8px;border-radius:12px;border:3px solid #2a1a10;background:linear-gradient(rgba(30,10,2,.35),rgba(30,10,2,.6)),url(${IMG}roca-cueva.jpg) center/cover;box-shadow:inset 0 0 28px rgba(0,0,0,.8)}
    .nid-nido{position:relative;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;height:232px;padding:0;border:2px solid transparent;border-radius:10px;background:none;cursor:pointer;color:#fff}
    .nid-nido.sel{border-color:#ffd27a;background:rgba(255,210,122,.08)}
    .nid-pila{display:flex;flex-direction:column;align-items:center;margin-bottom:-22px}
    .nid-pila img{display:block;height:auto;mix-blend-mode:screen;margin-top:-8px;filter:drop-shadow(0 3px 3px rgba(0,0,0,.6));transition:transform .2s}
    .nid-pila img:first-child{margin-top:0}
    .nid-nido.sel .nid-pila img:first-child{transform:translateY(-14px)}
    .nid-base{display:block;width:100%;height:auto;mix-blend-mode:screen;pointer-events:none}
    .nid-info{color:#f0d8b8;font-size:.85rem;margin-bottom:4px}
  `;
  ui.body.appendChild(style);

  const cueva = document.createElement('div');
  cueva.className = 'nid-cueva';
  const info = document.createElement('div');
  info.className = 'nid-info';
  ui.body.append(cueva, info);

  let pilas = [[4, 3, 2, 1], [], []];   // de abajo arriba
  let sel = null;
  let mov = 0;
  let resuelto = false;

  function pintar() {
    cueva.innerHTML = '';
    NIDOS.forEach((n, i) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'nid-nido' + (sel === i ? ' sel' : '');
      b.dataset.n = n.k;
      b.dataset.huevos = String(pilas[i].length);
      b.setAttribute('aria-label', n.nombre + ', ' + pilas[i].length + ' huevos');
      const pila = document.createElement('div');
      pila.className = 'nid-pila';
      // arriba del todo el más pequeño: el orden de pintado es de arriba abajo
      pilas[i].slice().reverse().forEach(h => {
        const im = document.createElement('img');
        im.alt = '';
        im.src = IMG + 'huevos/h' + h + '.jpg';
        im.style.width = ANCHO[h] + 'px';
        pila.appendChild(im);
      });
      b.appendChild(pila);
      b.insertAdjacentHTML('beforeend', '<img class="nid-base" alt="" src="' + IMG + 'nidos/' + n.k + '.jpg">');
      b.addEventListener('click', () => pulsar(i));
      cueva.appendChild(b);
    });
    info.textContent = 'Movimientos: ' + mov;
  }

  function pulsar(i) {
    if (resuelto) return;
    ui.say('');
    if (sel === null) {
      if (!pilas[i].length) { ui.say('Ese nido está vacío.', 'bad'); return; }
      sel = i;
    } else if (sel === i) {
      sel = null;
    } else {
      const h = pilas[sel][pilas[sel].length - 1];
      const dest = pilas[i];
      if (dest.length && dest[dest.length - 1] < h) {
        ui.say('Un huevo grande aplastaría al pequeño. Ahí no.', 'bad');
        sel = null;
      } else {
        pilas[sel].pop();
        dest.push(h);
        sel = null;
        mov++;
        if (pilas[2].length === 4) {
          resuelto = true;
          pintar();
          ui.say('¡Los cuatro huevos están a salvo en el nido de plumas! Donde estaban queda a la vista un hueco de roca caliente. Coged la carta 80.', 'ok');
          return;
        }
      }
    }
    pintar();
  }

  ui.button('Empezar de nuevo', 'ghost', () => {
    if (resuelto) return;
    pilas = [[4, 3, 2, 1], [], []];
    sel = null; mov = 0;
    ui.say('');
    pintar();
  });

  pintar();
  return { close: ui.close };
}
