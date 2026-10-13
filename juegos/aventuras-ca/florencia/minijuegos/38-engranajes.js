// Carta 38 — Mecanismo del león: montar una cadena de engranajes entre la manivela (A) y la cuerda (Z).
// Dos ruedas engranan si la distancia entre sus clavijas es exactamente la suma de sus radios.
// Objetivo (plano, carta 40): la cuerda gira igual de rápido que la manivela y en sentido contrario.
// Solución: pequeña (1) en D, mediana (2) en B y mediana (2) en Z (cadena A-D-B-Z).
// La otra cadena (A-D-Z con la grande en Z) hace girar la cuerda a la mitad de velocidad y en el mismo sentido.
import { openGame } from './ui.js';

const U = 26;
const NS = 'http://www.w3.org/2000/svg';
const PEGS = { A: [0, 0], B: [3, 3], D: [3, 0], Z: [7, 3] };
const NOMBRES = { A: 'la manivela', B: 'la clavija B', D: 'la clavija D', Z: 'la cuerda' };
const TAM = { 1: 'pequeña', 2: 'mediana', 4: 'grande' };
const IMG = { 1: 'pequena', 2: 'mediana', 4: 'grande' };
const BANDEJA = [1, 1, 2, 2, 4];
const EPS = 1e-6;

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 38 — Mecanismo del león',
    instr: 'Elige una rueda de la bandeja y toca una clavija para colocarla. Dos ruedas solo engranan si se tocan justo por los bordes.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    @keyframes far-giro{from{transform:rotate(0)}to{transform:rotate(360deg)}}
    .far-g-svg{display:block;width:100%;background:linear-gradient(rgba(14,8,3,.74),rgba(14,8,3,.88)),url(./img/ui/suelo.jpg) center/cover;border:2px solid #6b4a1e;border-radius:12px}
    .far-g-rueda-svg{mix-blend-mode:screen}
    .far-g-giro{transform-box:fill-box;transform-origin:center}
    .far-g-peg{cursor:pointer}
    .far-g-tray{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin:10px 0 4px}
    .far-g-rueda{width:62px;padding:6px 2px;border-radius:10px;border:2px solid #6b4a1e;background:linear-gradient(rgba(14,8,3,.7),rgba(14,8,3,.9)),url(./img/ui/suelo.jpg) center/cover;color:#fff;cursor:pointer;font:600 .7rem system-ui,sans-serif;display:flex;flex-direction:column;align-items:center;gap:3px}
    .far-g-rueda img{display:block;mix-blend-mode:screen;object-fit:contain}
    .far-g-rueda.sel{border-color:#ffd27a;box-shadow:0 0 10px rgba(255,210,122,.6)}
    .far-g-rueda:disabled{opacity:.3;cursor:not-allowed}
    .far-g-ayuda{color:#9fb4c8;font-size:.82rem;text-align:center;min-height:1.2em}
  `;
  ui.body.appendChild(style);

  const svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('viewBox', `${-3.2 * U} ${-3.4 * U} ${15 * U} ${10.8 * U}`);
  svg.classList.add('far-g-svg');
  const bandejaEl = document.createElement('div');
  bandejaEl.className = 'far-g-tray';
  const ayuda = document.createElement('div');
  ayuda.className = 'far-g-ayuda';
  ui.body.append(svg, bandejaEl, ayuda);

  let colocadas = {};            // clavija -> radio (A siempre está)
  let tray = BANDEJA.map((r, i) => ({ id: i, r, usada: false }));
  let seleccion = null;          // id de la rueda elegida de la bandeja
  let girando = null;            // resultado de la última simulación
  let resuelto = false;

  function el(tag, attrs, texto) {
    const e = document.createElementNS(NS, tag);
    Object.keys(attrs).forEach(k => e.setAttribute(k, attrs[k]));
    if (texto !== undefined) e.textContent = texto;
    return e;
  }

  const dist = (a, b) => Math.hypot(PEGS[a][0] - PEGS[b][0], PEGS[a][1] - PEGS[b][1]);
  const radioDe = p => (p === 'A' ? 2 : colocadas[p]);
  const todas = () => ['A', ...Object.keys(colocadas)];

  // Recorre las ruedas unidas a la manivela: sentido (+1 horario, -1 antihorario) y velocidad relativa.
  function simular() {
    const dir = { A: 1 };
    const vel = { A: 1 };
    const cola = ['A'];
    while (cola.length) {
      const a = cola.shift();
      todas().forEach(b => {
        if (dir[b] !== undefined) return;
        if (Math.abs(dist(a, b) - (radioDe(a) + radioDe(b))) < EPS) {
          dir[b] = -dir[a];
          vel[b] = vel[a] * radioDe(a) / radioDe(b);
          cola.push(b);
        }
      });
    }
    return { dir, vel };
  }

  function pintarRueda(peg, r, giro) {
    const [cx, cy] = [PEGS[peg][0] * U, PEGS[peg][1] * U];
    const R = r * U;
    const g = el('g', { transform: `translate(${cx} ${cy})`, 'data-peg': peg, class: 'far-g-rueda-svg' });
    const anim = el('g', { class: 'far-g-giro' });
    if (giro) {
      anim.style.animation = `far-giro ${(3 / giro.vel).toFixed(3)}s linear infinite`;
      anim.style.animationDirection = giro.dir === 1 ? 'normal' : 'reverse';
    }
    const W = 2 * R + 8;
    anim.appendChild(el('image', { href: './img/ui/engranajes/' + (peg === 'A' ? 'manivela' : IMG[r]) + '.jpg', x: -W / 2, y: -W / 2, width: W, height: W }));
    g.appendChild(anim);
    return g;
  }

  function pintar() {
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    // cuadricula suave para poder medir distancias
    for (let x = -3; x <= 11; x++) svg.appendChild(el('line', { x1: x * U, y1: -4.5 * U, x2: x * U, y2: 7.5 * U, stroke: 'rgba(255,255,255,.05)' }));
    for (let y = -4; y <= 7; y++) svg.appendChild(el('line', { x1: -3 * U, y1: y * U, x2: 11.5 * U, y2: y * U, stroke: 'rgba(255,255,255,.05)' }));
    // clavijas
    Object.keys(PEGS).forEach(p => {
      const [cx, cy] = [PEGS[p][0] * U, PEGS[p][1] * U];
      if (p === 'A') return;
      const g = el('g', { class: 'far-g-peg', 'data-peg': p, transform: `translate(${cx} ${cy})` });
      g.appendChild(el('circle', { r: 17, fill: 'transparent' }));
      g.appendChild(el('circle', { r: 11, fill: '#3a2208', stroke: '#e8d9b0', 'stroke-width': 2, 'stroke-dasharray': colocadas[p] ? '' : '3 3' }));
      g.appendChild(el('text', { y: 4, 'text-anchor': 'middle', 'font-size': 12, fill: '#fff', 'font-family': 'system-ui,sans-serif', 'font-weight': 700, 'pointer-events': 'none' }, p));
      g.addEventListener('click', () => pulsarClavija(p));
      svg.appendChild(g);
    });
    // ruedas colocadas (debajo de las clavijas para que se puedan seguir pulsando)
    const capa = el('g', { 'pointer-events': 'none' });
    capa.appendChild(pintarRueda('A', 2, girando && girando.dir.A !== undefined ? { dir: 1, vel: 1 } : null));
    Object.keys(colocadas).forEach(p => {
      const conectada = girando && girando.dir[p] !== undefined;
      capa.appendChild(pintarRueda(p, colocadas[p], conectada ? { dir: girando.dir[p], vel: girando.vel[p] } : null));
    });
    svg.insertBefore(capa, svg.querySelector('.far-g-peg'));
    // etiquetas
    [['A', 'Manivela', 0, -2 * U - 10], ['Z', 'Cuerda', 0, -4 * U + 4]].forEach(([p, txt, dx, dy]) => {
      const t = el('text', { x: PEGS[p][0] * U + dx, y: PEGS[p][1] * U + dy, 'text-anchor': 'middle', 'font-size': 13, fill: '#ffd27a', 'font-family': 'system-ui,sans-serif', 'font-weight': 700, 'pointer-events': 'none' }, txt);
      svg.appendChild(t);
    });
    // bandeja
    bandejaEl.innerHTML = '';
    tray.forEach(g => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'far-g-rueda' + (seleccion === g.id ? ' sel' : '');
      b.dataset.r = String(g.r);
      b.dataset.id = String(g.id);
      b.disabled = g.usada;
      b.setAttribute('aria-label', 'Rueda ' + TAM[g.r]);
      const lado = 18 + g.r * 7;
      b.innerHTML = '<img alt="" style="width:' + lado + 'px;height:' + lado + 'px" src="./img/ui/engranajes/' + IMG[g.r] + '.jpg">' + TAM[g.r];
      b.addEventListener('click', () => { if (!resuelto) { seleccion = seleccion === g.id ? null : g.id; ui.say(''); pintar(); } });
      bandejaEl.appendChild(b);
    });
    ayuda.textContent = seleccion === null ? 'Elige una rueda de la bandeja, o toca una rueda colocada para quitarla.' : 'Ahora toca una clavija vacía (B, D o Z).';
  }

  function pulsarClavija(p) {
    if (resuelto) return;
    girando = null;
    ui.say('');
    if (colocadas[p]) {
      // quitarla: vuelve a la bandeja
      const r = colocadas[p];
      const hueco = tray.find(g => g.usada && g.r === r);
      if (hueco) hueco.usada = false;
      delete colocadas[p];
      pintar();
      return;
    }
    if (seleccion === null) { ui.say('Primero elige una rueda de la bandeja.', 'bad'); return; }
    const g = tray.find(x => x.id === seleccion);
    // ¿se pisa con alguna?
    for (const q of todas()) {
      if (dist(p, q) < g.r + radioDe(q) - EPS) {
        ui.say('No cabe ahí: la rueda ' + TAM[g.r] + ' se pisa con ' + NOMBRES[q] + '.', 'bad');
        return;
      }
    }
    colocadas[p] = g.r;
    g.usada = true;
    seleccion = null;
    pintar();
  }

  function girar() {
    if (resuelto) return;
    if (!colocadas.Z) { ui.say('Falta la rueda de la cuerda: colócala en la clavija Z.', 'bad'); return; }
    const s = simular();
    girando = s;
    pintar();
    if (s.dir.Z === undefined) {
      ui.say('La manivela gira, pero la cuerda no se mueve: no hay una cadena de ruedas que se toquen justo por los bordes hasta ella.', 'bad');
      return;
    }
    const v = s.vel.Z;
    const vel = Math.abs(v - 1) < EPS ? 'igual de rápido' : (Math.abs(v - 2) < EPS ? 'el doble de rápido' : (Math.abs(v - 0.5) < EPS ? 'la mitad de rápido' : 'a otra velocidad'));
    const sent = s.dir.Z === -1 ? 'al revés' : 'en el mismo sentido';
    if (Math.abs(v - 1) < EPS && s.dir.Z === -1) {
      resuelto = true;
      ui.say('La cuerda gira igual de rápido que la manivela y al revés, como pide el plano. El mecanismo del león arranca y una esfera marca el número 9: es un modificador (+9). Sumadlo a la llave de cuerda (carta 42): 42 + 9 = 51. Coged la carta 51.', 'ok');
      return;
    }
    ui.say('La cuerda gira ' + vel + ' que la manivela y ' + sent + '. El plano pide otra cosa: probad otra cadena.', 'bad');
  }

  ui.button('Quitar todo', 'ghost', () => {
    if (resuelto) return;
    colocadas = {};
    tray = BANDEJA.map((r, i) => ({ id: i, r, usada: false }));
    seleccion = null;
    girando = null;
    ui.say('');
    pintar();
  });
  ui.button('Girar manivela', 'primary', girar);

  pintar();
  return { close: ui.close };
}
