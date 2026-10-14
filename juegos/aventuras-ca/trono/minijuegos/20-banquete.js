// Carta 20 — Banquete de las casas: tabla lógica. Cuatro casas, cuatro asientos y cuatro regalos.
// Dos pistas están en la lista del senescal (carta 18) y cuatro las cuentan los criados en la pantalla. Solución única comprobada por
// herramientas/instancias_trono.py.
import { openGame } from './ui.js';
import { guardarPalabra, estilo, texturaSi } from './comun.js';

const CASAS = ['Lobo Gris', 'León Dorado', 'Halcón Plateado', 'Oso Pardo'];
const REGALOS = ['espada', 'copa', 'pieles', 'cuerno'];
// forma (no solo color) que acompaña a cada casa
const FORMAS = ['▲', '●', '◆', '■'];
const SOLUCION = [['León Dorado', 'copa'], ['Lobo Gris', 'pieles'], ['Oso Pardo', 'espada'], ['Halcón Plateado', 'cuerno']];
const PALABRA = 'SOLO';

// ac[i] = asiento (0..3) de la casa i; ar[j] = asiento del regalo j
const c = (x) => CASAS.indexOf(x);
const r = (x) => REGALOS.indexOf(x);
const CARTA = [
  { txt: 'El Halcón Plateado ocupa el último asiento.', ok: (ac) => ac[c('Halcón Plateado')] === 3 },
  { txt: 'Quien trae la espada no se sienta en ninguna de las dos puntas de la mesa.', ok: (ac, ar) => ar[r('espada')] === 1 || ar[r('espada')] === 2 }
];
const APP = [
  { txt: 'El cuerno lo trae la casa sentada justo a la derecha del Oso Pardo.', ok: (ac, ar) => ar[r('cuerno')] === ac[c('Oso Pardo')] + 1 },
  { txt: 'El Oso Pardo no trae las pieles.', ok: (ac, ar) => ar[r('pieles')] !== ac[c('Oso Pardo')] },
  { txt: 'El Lobo Gris se sienta más a la derecha que el León Dorado.', ok: (ac) => ac[c('Lobo Gris')] > ac[c('León Dorado')] },
  { txt: 'Las pieles no las trae ni el Halcón Plateado ni el León Dorado.', ok: (ac, ar) => ar[r('pieles')] !== ac[c('Halcón Plateado')] && ar[r('pieles')] !== ac[c('León Dorado')] }
];

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 20 — Banquete de las casas',
    instr: 'Cuatro casas se sientan a la mesa, de izquierda a derecha, y cada una trae un regalo. Tocad cada casilla para cambiar de casa o de regalo.',
    ...opts
  });
  texturaSi(ui, 'mesa.jpg', { opacidad: 0.3, mezcla: 'screen' });

  estilo(ui.body, `
    .ban-criados{margin:0 auto 10px;max-width:360px;padding:8px 10px;border-radius:8px;background:rgba(0,0,0,.32);border:1px solid rgba(159,184,204,.4);text-align:left;font-size:.82rem;line-height:1.35}
    .ban-criados b{display:block;margin-bottom:3px;color:#d6e8f5;font-size:.74rem;letter-spacing:.06em;text-transform:uppercase}
    .ban-criados li{margin:0 0 3px 16px}
    .ban-mesa{display:grid;gap:7px;max-width:360px;margin:0 auto 6px}
    .ban-fila{display:grid;grid-template-columns:62px 1fr 1fr;gap:6px;align-items:stretch;padding:6px;border-radius:8px;background:linear-gradient(#3a2c1f,#2a1f15);border:1px solid #6b5436;box-shadow:inset 0 1px 0 rgba(255,235,200,.12)}
    .ban-asiento{display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:.7rem;color:#e8d6b4;line-height:1.15}
    .ban-asiento strong{font-size:1.15rem;color:#ffe3a8}
    .ban-fila button{min-height:48px;padding:4px 6px;border-radius:8px;border:1px solid rgba(207,232,251,.55);background:rgba(8,14,22,.72);color:#eaf4fb;font:600 .85rem inherit;font-family:inherit;cursor:pointer;touch-action:manipulation;line-height:1.15}
    .ban-fila button.vacio{color:#8aa0b2;border-style:dashed}
    .ban-fila button.img{background-image:var(--img);background-size:cover}
    .ban-forma{margin-right:4px;color:#8fc7ee}
  `);

  const crit = document.createElement('div');
  crit.className = 'ban-criados';
  crit.innerHTML = '<b>Lo que cuentan los criados</b><ul></ul>';
  APP.forEach(p => { const li = document.createElement('li'); li.textContent = p.txt; crit.querySelector('ul').appendChild(li); });
  const mesa = document.createElement('div');
  mesa.className = 'ban-mesa';
  ui.body.append(crit, mesa);

  const casa = [-1, -1, -1, -1];
  const regalo = [-1, -1, -1, -1];
  let resuelto = false;
  const bC = [], bR = [];

  for (let s = 0; s < 4; s++) {
    const fila = document.createElement('div');
    fila.className = 'ban-fila';
    fila.innerHTML = '<div class="ban-asiento">Asiento<strong>' + (s + 1) + '</strong>' + (s === 0 ? 'izquierda' : s === 3 ? 'derecha' : '') + '</div>';
    const a = document.createElement('button');
    a.type = 'button';
    a.className = 'ban-casa vacio';
    a.dataset.s = String(s);
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'ban-regalo vacio';
    b.dataset.s = String(s);
    a.addEventListener('click', () => { if (!resuelto) { casa[s] = (casa[s] + 2) % 5 - 1; pintar(); } });
    b.addEventListener('click', () => { if (!resuelto) { regalo[s] = (regalo[s] + 2) % 5 - 1; pintar(); } });
    fila.append(a, b);
    mesa.appendChild(fila);
    bC.push(a);
    bR.push(b);
  }

  function pintar() {
    for (let s = 0; s < 4; s++) {
      const hc = casa[s] >= 0;
      bC[s].classList.toggle('vacio', !hc);
      bC[s].dataset.v = hc ? CASAS[casa[s]] : '';
      bC[s].innerHTML = hc ? '<span class="ban-forma" aria-hidden="true">' + FORMAS[casa[s]] + '</span>' + CASAS[casa[s]] : 'Casa ¿?';
      bC[s].setAttribute('aria-label', 'Asiento ' + (s + 1) + ', casa: ' + (hc ? CASAS[casa[s]] : 'sin elegir'));
      const hr = regalo[s] >= 0;
      bR[s].classList.toggle('vacio', !hr);
      bR[s].dataset.v = hr ? REGALOS[regalo[s]] : '';
      bR[s].textContent = hr ? REGALOS[regalo[s]][0].toUpperCase() + REGALOS[regalo[s]].slice(1) : 'Regalo ¿?';
      bR[s].setAttribute('aria-label', 'Asiento ' + (s + 1) + ', regalo: ' + (hr ? REGALOS[regalo[s]] : 'sin elegir'));
    }
  }
  pintar();

  ui.button('Vaciar la mesa', 'ghost', () => {
    if (resuelto) return;
    for (let i = 0; i < 4; i++) { casa[i] = -1; regalo[i] = -1; }
    ui.say('');
    pintar();
  });
  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    if (casa.includes(-1) || regalo.includes(-1)) { ui.say('Falta decidir alguna casa o algún regalo.', 'bad'); return; }
    if (new Set(casa).size < 4) { ui.say('Una casa no puede ocupar dos asientos: alguna se repite.', 'bad'); return; }
    if (new Set(regalo).size < 4) { ui.say('Cada casa trae un regalo distinto: alguno se repite.', 'bad'); return; }
    const ac = [0, 0, 0, 0], ar = [0, 0, 0, 0];
    for (let s = 0; s < 4; s++) { ac[casa[s]] = s; ar[regalo[s]] = s; }
    const mala = CARTA.find(p => !p.ok(ac, ar));
    if (mala) { ui.say('Algo no encaja con la lista del senescal (carta 18): «' + mala.txt + '»', 'bad'); return; }
    const mala2 = APP.find(p => !p.ok(ac, ar));
    if (mala2) { ui.say('Algo no encaja con lo que cuentan los criados: «' + mala2.txt + '»', 'bad'); return; }
    resuelto = true;
    guardarPalabra('20', PALABRA);
    ui.say('¡Todo encaja! El banquete se desarrolla en paz y los criados os dan lo que han encontrado. Palabra de la profecía: «' + PALABRA + '». Anotadla. Coged la carta 28.', 'ok');
  });

  return { close: ui.close, solucion: SOLUCION };
}
