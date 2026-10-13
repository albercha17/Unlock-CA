// Carta 66 — Ornitóptero: elegir ala, tela y lastre. Las tres notas (cartas 68, 70 y 71) descartan combinaciones.
// Solución única: ala LARGA, tela de SEDA, lastre de 2 sacos.
//   68: ala corta no levanta · con ala media siempre 2 sacos · ala larga no admite 3 sacos
//   70: con un solo saco cae de lado
//   71: 2 sacos + cuero vuelca · lino + 2 sacos se arruga · ala media + seda sin fuerza
import { openGame } from './ui.js';

const NS = 'http://www.w3.org/2000/svg';
const GRUPOS = [
  { id: 'ala', titulo: 'Ala', opciones: [['corta', 'Corta'], ['media', 'Media'], ['larga', 'Larga']] },
  { id: 'tela', titulo: 'Tela', opciones: [['lino', 'Lino'], ['seda', 'Seda'], ['cuero', 'Cuero']] },
  { id: 'lastre', titulo: 'Lastre', opciones: [['1', '1 saco'], ['2', '2 sacos'], ['3', '3 sacos']] }
];
const SOLUCION = { ala: 'larga', tela: 'seda', lastre: '2' };
const ENVERGADURA = { corta: 46, media: 78, larga: 112 };
const AX = 140;  // centro del ornitoptero
const COLOR_TELA = { lino: '#e8dcc0', seda: '#d9566f', cuero: '#8a5a2a' };

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 66 — Ornitóptero',
    instr: 'Prepara el ornitóptero con ala, tela y lastre según las notas de Leonardo y Salaì. Solo una combinación vuela.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .far-o-svg{display:block;width:100%;background:linear-gradient(180deg,#1d2a3a,#3a2a1c 78%);border:2px solid #6b4a1e;border-radius:12px;margin-bottom:10px}
    .far-o-ave{transition:transform 1.2s ease-in,opacity .3s}
    .far-o-ave.vuela{transform:translate(70px,-46px) rotate(-8deg)}
    .far-o-ave.cae{transform:translate(18px,16px) rotate(24deg)}
    .far-o-grupo{display:flex;align-items:center;gap:8px;margin-bottom:8px}
    .far-o-grupo b{width:58px;color:#ffd27a;font-size:.9rem}
    .far-o-opts{display:flex;gap:6px;flex:1}
    .far-o-opt{flex:1;padding:9px 4px;border-radius:9px;border:2px solid rgba(255,255,255,.14);background:rgba(255,255,255,.06);color:#fff;font-weight:700;font-size:.88rem;cursor:pointer;font-family:inherit}
    .far-o-opt.sel{border-color:#ffd27a;background:rgba(255,210,122,.18);color:#ffd27a}
    .far-o-intentos{color:#9fb4c8;font-size:.82rem;text-align:center;margin:4px 0}
  `;
  ui.body.appendChild(style);

  const svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('viewBox', '0 0 300 150');
  svg.classList.add('far-o-svg');
  const grupos = document.createElement('div');
  const intentosEl = document.createElement('div');
  intentosEl.className = 'far-o-intentos';
  ui.body.append(svg, grupos, intentosEl);

  const eleccion = { ala: null, tela: null, lastre: null };
  let intentos = 0;
  let resuelto = false;
  let estadoVuelo = '';

  function el(tag, attrs) {
    const e = document.createElementNS(NS, tag);
    Object.keys(attrs).forEach(k => e.setAttribute(k, attrs[k]));
    return e;
  }

  function pintarAve() {
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    svg.appendChild(el('rect', { x: 0, y: 128, width: 300, height: 22, fill: '#2a1a0c' }));
    svg.appendChild(el('polygon', { points: '6,128 120,128 120,119 6,125', fill: '#5a3a1a' }));  // rampa
    const ave = el('g', { class: 'far-o-ave ' + estadoVuelo, 'data-estado': estadoVuelo });
    const env = ENVERGADURA[eleccion.ala] || 62;
    const col = COLOR_TELA[eleccion.tela] || '#b9a98a';
    [-1, 1].forEach(lado => {
      ave.appendChild(el('polygon', { points: `${AX},100 ${AX + lado * env},${86} ${AX + lado * env * 0.9},${112} ${AX},108`, fill: col, stroke: '#3a2208', 'stroke-width': 2 }));
      ave.appendChild(el('line', { x1: AX, y1: 102, x2: AX + lado * env, y2: 90, stroke: '#3a2208', 'stroke-width': 3 }));
    });
    ave.appendChild(el('ellipse', { cx: AX, cy: 106, rx: 20, ry: 9, fill: '#8a5a2a', stroke: '#3a2208', 'stroke-width': 2 }));
    ave.appendChild(el('circle', { cx: AX, cy: 100, r: 5, fill: '#e8d9b0' }));
    const sacos = Number(eleccion.lastre) || 0;
    for (let i = 0; i < sacos; i++) {
      ave.appendChild(el('line', { x1: AX - 10 + i * 10, y1: 114, x2: AX - 10 + i * 10, y2: 120, stroke: '#3a2208', 'stroke-width': 1.5 }));
      ave.appendChild(el('circle', { cx: AX - 10 + i * 10, cy: 124, r: 5, fill: '#b8893b', stroke: '#3a2208', 'stroke-width': 1.5 }));
    }
    svg.appendChild(ave);
    // palanca del lucernario
    svg.appendChild(el('line', { x1: 286, y1: 40, x2: 286, y2: 128, stroke: '#6b4a1e', 'stroke-width': 4 }));
    svg.appendChild(el('circle', { cx: 286, cy: 40, r: 7, fill: '#ffd27a', stroke: '#3a2208', 'stroke-width': 2 }));
  }

  function pintarGrupos() {
    grupos.innerHTML = '';
    GRUPOS.forEach(g => {
      const fila = document.createElement('div');
      fila.className = 'far-o-grupo';
      const t = document.createElement('b');
      t.textContent = g.titulo;
      const opts = document.createElement('div');
      opts.className = 'far-o-opts';
      g.opciones.forEach(([v, txt]) => {
        const b = document.createElement('button');
        b.type = 'button';
        b.className = 'far-o-opt' + (eleccion[g.id] === v ? ' sel' : '');
        b.dataset.g = g.id;
        b.dataset.v = v;
        b.textContent = txt;
        b.addEventListener('click', () => {
          if (resuelto) return;
          eleccion[g.id] = v;
          estadoVuelo = '';
          ui.say('');
          pintarGrupos();
          pintarAve();
        });
        opts.appendChild(b);
      });
      fila.append(t, opts);
      grupos.appendChild(fila);
    });
    intentosEl.textContent = 'Intentos de vuelo: ' + intentos;
  }

  const vuela = () => GRUPOS.every(g => eleccion[g.id] === SOLUCION[g.id]);

  ui.button('Probar vuelo', 'primary', () => {
    if (resuelto) return;
    if (!eleccion.ala || !eleccion.tela || !eleccion.lastre) { ui.say('Elige un ala, una tela y un lastre antes de probar.', 'bad'); return; }
    intentos++;
    if (vuela()) {
      resuelto = true;
      estadoVuelo = 'vuela';
      pintarAve();
      pintarGrupos();
      ui.say('¡Vuela! El ornitóptero se eleva por la rampa y su ala golpea la palanca: el lucernario del tejado se abre y entra el primer rayo del amanecer. Coged la carta 90.', 'ok');
    } else {
      estadoVuelo = 'cae';
      pintarAve();
      pintarGrupos();
      ui.say('El ornitóptero no consigue despegar y se desploma. Releed las tres notas: cada frase descarta combinaciones.', 'bad');
    }
  });

  pintarGrupos();
  pintarAve();
  return { close: ui.close };
}
