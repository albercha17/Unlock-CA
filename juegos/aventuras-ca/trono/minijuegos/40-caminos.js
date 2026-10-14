// Carta 40 — Caminos entre castillos (puentes / hashi): unir ocho castillos con caminos de uno o dos tramos, sin cruces, todos conectados.
// Los castillos E y G no muestran su número: lo da la crónica del maestre (carta 42). Solución única comprobada por herramientas/instancias_trono.py.
import { openGame } from './ui.js';
import { guardarPalabra, estilo, conImagen, texturaSi } from './comun.js';

const N = 7;
const PALABRA = 'VENCERÁ';
// letra, fila, columna, caminos que salen, ¿oculto?
const CASTILLOS = [
  ['A', 1, 1, 2, false], ['B', 1, 3, 2, false], ['C', 1, 4, 2, false], ['D', 1, 6, 1, false],
  ['E', 2, 1, 3, true], ['F', 6, 0, 1, false], ['G', 6, 1, 4, true], ['H', 6, 2, 1, false]
];

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 40 — Caminos entre castillos',
    instr: 'Tocad un castillo y luego otro en línea recta para tender un camino; tocad otra vez para un camino doble y otra para quitarlo. El número dice cuántos caminos salen del castillo.',
    ...opts
  });
  texturaSi(ui, 'mapa.jpg', { opacidad: 0.3, mezcla: 'screen' });

  estilo(ui.body, `
    .cam-mapa{position:relative;width:min(340px,86vw);aspect-ratio:1;margin:0 auto 6px;border-radius:10px;border:3px solid #5d7a90;background:radial-gradient(circle at 50% 40%,#1d2a36,#0c131b);touch-action:manipulation;overflow:hidden}
    .cam-mapa svg{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
    .cam-isla{position:absolute;width:15.5%;aspect-ratio:1;transform:translate(-50%,-50%);border-radius:30% 30% 12% 12%;border:2px solid #9fb8cc;background:linear-gradient(#586573,#2f3944);color:#f3f8fc;font:800 1.05rem Georgia,serif;padding:0;cursor:pointer;display:flex;flex-direction:column;align-items:center;justify-content:center;line-height:1;touch-action:manipulation}
    .cam-isla small{font:600 .6rem Poppins,sans-serif;opacity:.8}
    .cam-isla.img{background-image:var(--img);background-size:cover}
    .cam-isla.sel{box-shadow:0 0 0 3px #8fc7ee,0 0 16px #8fc7ee}
    .cam-isla.ok{border-color:#7dffb0;color:#c8ffd8}
    .cam-isla.mal{border-color:#ff9d9d;color:#ffd0d0}
    .cam-isla.oculto{border-style:dashed}
    .cam-nota{font-size:.78rem;color:#a9bccb;margin:2px 0 4px}
  `);

  const mapa = document.createElement('div');
  mapa.className = 'cam-mapa';
  const NS = 'http://www.w3.org/2000/svg';
  const svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('viewBox', '0 0 ' + N + ' ' + N);
  mapa.appendChild(svg);
  const nota = document.createElement('div');
  nota.className = 'cam-nota';
  nota.textContent = 'Los castillos E y G no muestran su número: está en la crónica del maestre.';
  ui.body.append(mapa, nota);

  const islas = CASTILLOS.map(([l, r, c, n, oc]) => ({ l, r, c, n, oc, k: r + ',' + c }));
  const puentes = {};
  let sel = null;
  let resuelto = false;
  const btn = {};

  islas.forEach(i => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'cam-isla' + (i.oc ? ' oculto' : '');
    b.dataset.k = i.k;
    b.dataset.letra = i.l;
    b.innerHTML = i.l + '<small>' + (i.oc ? '?' : i.n) + '</small>';
    b.setAttribute('aria-label', 'Castillo ' + i.l + ', ' + (i.oc ? 'número desconocido' : i.n + ' caminos') + ', fila ' + (i.r + 1) + ' columna ' + (i.c + 1));
    b.style.left = ((i.c + 0.5) / N * 100) + '%';
    b.style.top = ((i.r + 0.5) / N * 100) + '%';
    b.addEventListener('click', () => tocar(i));
    mapa.appendChild(b);
    btn[i.k] = b;
    conImagen(b, 'castillo.jpg');
  });

  const clave = (a, b) => [a.k, b.k].sort().join('|');
  const porK = (k) => islas.find(x => x.k === k);
  function entre(a, b) {
    return islas.some(x => x !== a && x !== b && ((a.r === b.r && x.r === a.r && x.c > Math.min(a.c, b.c) && x.c < Math.max(a.c, b.c)) ||
      (a.c === b.c && x.c === a.c && x.r > Math.min(a.r, b.r) && x.r < Math.max(a.r, b.r))));
  }
  function cruza(a, b) {
    return Object.keys(puentes).some(kk => {
      if (!puentes[kk] || kk === clave(a, b)) return false;
      const [p, q] = kk.split('|').map(porK);
      const h1 = a.r === b.r, h2 = p.r === q.r;
      if (h1 === h2) return false;
      const [h, v] = h1 ? [[a, b], [p, q]] : [[p, q], [a, b]];
      const fy = h[0].r, x1 = Math.min(h[0].c, h[1].c), x2 = Math.max(h[0].c, h[1].c);
      const fx = v[0].c, y1 = Math.min(v[0].r, v[1].r), y2 = Math.max(v[0].r, v[1].r);
      return x1 < fx && fx < x2 && y1 < fy && fy < y2;
    });
  }
  function grado(i) { return Object.keys(puentes).reduce((s, kk) => s + (kk.split('|').includes(i.k) ? puentes[kk] : 0), 0); }

  function tocar(i) {
    if (resuelto) return;
    if (!sel) sel = i;
    else if (sel === i) sel = null;
    else {
      const a = sel, b = i;
      sel = null;
      if (!(a.r === b.r || a.c === b.c) || entre(a, b)) {
        ui.say('Solo se pueden unir castillos en línea recta y sin otro castillo entre medias.', 'bad');
      } else {
        const kk = clave(a, b);
        const nuevo = ((puentes[kk] || 0) + 1) % 3;
        if (nuevo && cruza(a, b)) ui.say('Ese camino cruzaría otro.', 'bad');
        else { puentes[kk] = nuevo; ui.say(''); }
      }
    }
    pintar();
    if (todoCuadra().ok) terminar();
  }

  function conectados() {
    const vistos = new Set([islas[0].k]);
    let cambio = true;
    while (cambio) {
      cambio = false;
      Object.keys(puentes).forEach(kk => {
        if (!puentes[kk]) return;
        const [a, b] = kk.split('|');
        if (vistos.has(a) !== vistos.has(b)) { vistos.add(a); vistos.add(b); cambio = true; }
      });
    }
    return vistos.size === islas.length;
  }
  function todoCuadra() {
    const visibles = islas.filter(i => !i.oc).every(i => grado(i) === i.n);
    const ocultos = islas.filter(i => i.oc).every(i => grado(i) === i.n);
    return { visibles, ocultos, conexo: conectados(), ok: visibles && ocultos && conectados() };
  }

  function pintar() {
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    Object.keys(puentes).forEach(kk => {
      const v = puentes[kk];
      if (!v) return;
      const [p, q] = kk.split('|').map(porK);
      for (let j = 0; j < v; j++) {
        const off = v === 1 ? 0 : (j === 0 ? -0.07 : 0.07);
        const l = document.createElementNS(NS, 'line');
        const horiz = p.r === q.r;
        l.setAttribute('x1', p.c + 0.5 + (horiz ? 0 : off)); l.setAttribute('y1', p.r + 0.5 + (horiz ? off : 0));
        l.setAttribute('x2', q.c + 0.5 + (horiz ? 0 : off)); l.setAttribute('y2', q.r + 0.5 + (horiz ? off : 0));
        l.setAttribute('stroke', '#d9c79a'); l.setAttribute('stroke-width', '0.08'); l.setAttribute('stroke-linecap', 'round');
        svg.appendChild(l);
      }
    });
    islas.forEach(i => {
      const g = grado(i);
      btn[i.k].classList.toggle('sel', sel === i);
      btn[i.k].classList.toggle('ok', !i.oc && g === i.n);
      btn[i.k].classList.toggle('mal', !i.oc && g > i.n);
      btn[i.k].dataset.grado = String(g);
    });
  }

  function terminar() {
    if (resuelto) return;
    resuelto = true;
    guardarPalabra('40', PALABRA);
    ui.say('¡Todos los castillos están unidos! El mapa se ilumina y muestra la ruta hasta el salón del consejo. Palabra de la profecía: «' + PALABRA + '». Anotadla. Coged la carta 44.', 'ok');
  }

  ui.button('Quitar caminos', 'ghost', () => { if (!resuelto) { Object.keys(puentes).forEach(k => delete puentes[k]); sel = null; ui.say(''); pintar(); } });
  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    const t = todoCuadra();
    if (t.ok) { terminar(); return; }
    if (!t.visibles) ui.say('Algún castillo tiene más o menos caminos de los que indica su número.', 'bad');
    else if (!t.conexo) ui.say('Los números cuadran, pero hay castillos que no están conectados con los demás.', 'bad');
    else ui.say('Los castillos con número están bien, pero E o G no tienen los caminos que anota la crónica del maestre (carta 42).', 'bad');
  });

  pintar();
  return { close: ui.close };
}
