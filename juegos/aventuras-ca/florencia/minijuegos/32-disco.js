// Carta 32 — Disco de Alberti: disco de cifrado con dos anillos de letras.
// La nota de Salaì (carta 28) dice cómo colocarlo: la A de fuera sobre la F de dentro (desplazamiento 5).
// El pergamino (carta 35) es: JQ QJTS LZFWIF XZ HTWFETS = EL LEON GUARDA SU CORAZON. Palabra clave: LEON.
import { openGame } from './ui.js';

const ALF = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
const PALABRA = 'LEON';
const NS = 'http://www.w3.org/2000/svg';

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 32 — Disco de Alberti',
    instr: 'Coloca el disco como indica la nota de Salaì, descifra el pergamino y escribe el nombre del guardián del taller.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .far-disco{display:block;margin:0 auto 6px;max-width:300px;width:100%}
    .far-d-img{mix-blend-mode:screen}
    
    .far-d-letra{cursor:pointer}
    .far-d-letra text{font-family:Georgia,"Times New Roman",serif;font-weight:700;pointer-events:none}
    .far-d-letra.sel circle{fill:#ffd27a}
    .far-d-letra.sel text{fill:#2a1600}
    .far-par{text-align:center;font-weight:700;color:#ffd27a;margin:2px 0 8px;min-height:1.4em}
    .far-tabla2{display:grid;grid-template-columns:auto repeat(13,1fr);gap:1px 2px;font:700 .72rem/1.35 Georgia,serif;text-align:center;margin:0 0 10px;background:#2a1a0c;border:1px solid #6b4a1e;border-radius:8px;padding:6px 4px;color:#e8d9b0}
    .far-tabla2 .et{color:#9fb4c8;font:600 .62rem system-ui,sans-serif;text-align:left;padding-right:4px}
    .far-tabla2 .in{color:#ffd27a}
  `;
  ui.body.appendChild(style);

  let giro = 0;          // la letra de dentro bajo la A de fuera es ALF[giro]
  let seleccionada = null; // letra de dentro elegida, a la espera de una de fuera
  let entered = '';
  let resuelto = false;

  const svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('viewBox', '0 0 300 300');
  svg.classList.add('far-disco');
  const par = document.createElement('div');
  par.className = 'far-par';
  const tabla = document.createElement('div');
  tabla.className = 'far-tabla2';
  const display = document.createElement('div');
  display.className = 'far-display';
  const kb = document.createElement('div');
  kb.className = 'far-keyboard';
  ui.body.append(svg, par, tabla, display, kb);

  function el(tag, attrs, texto) {
    const e = document.createElementNS(NS, tag);
    Object.keys(attrs).forEach(k => e.setAttribute(k, attrs[k]));
    if (texto !== undefined) e.textContent = texto;
    return e;
  }

  function pos(i, radio) {
    const a = (i * 360 / 26 - 90) * Math.PI / 180;
    return [150 + radio * Math.cos(a), 150 + radio * Math.sin(a)];
  }

  function letra(lado, l, i, radio, color, fondo) {
    const [x, y] = pos(i, radio);
    const g = el('g', { class: 'far-d-letra far-d-' + lado + (lado === 'in' && seleccionada === l ? ' sel' : ''), 'data-l': l, 'data-lado': lado });
    g.appendChild(el('circle', { cx: x, cy: y, r: 11.5, fill: fondo }));
    g.appendChild(el('text', { x, y: y + 5, 'text-anchor': 'middle', 'font-size': 15, fill: color }, l));
    g.addEventListener('click', () => pulsar(lado, l));
    return g;
  }

  function pintarDisco() {
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    svg.appendChild(el('image', { href: './img/ui/disco.jpg', x: 2, y: 2, width: 296, height: 296, class: 'far-d-img' }));
    // bandas oscuras para que se lean las letras sobre el relieve del bronce
    svg.appendChild(el('circle', { cx: 150, cy: 150, r: 129, fill: 'none', stroke: 'rgba(12,7,2,.7)', 'stroke-width': 25 }));
    svg.appendChild(el('circle', { cx: 150, cy: 150, r: 96, fill: 'none', stroke: 'rgba(12,7,2,.7)', 'stroke-width': 25 }));
    for (let i = 0; i < 26; i++) {
      svg.appendChild(letra('out', ALF[i], i, 129, '#f4e9c8', 'rgba(0,0,0,.25)'));
      // la letra de dentro que queda frente a la de fuera i
      svg.appendChild(letra('in', ALF[(i + giro) % 26], i, 96, '#ffd27a', 'rgba(255,210,122,.12)'));
    }
    // marca de la A de fuera
    svg.appendChild(el('path', { d: 'M150 6 L144 -2 L156 -2 Z', fill: '#ffd27a' }));
  }

  function pintarTabla() {
    tabla.innerHTML = '';
    [[0, 13], [13, 26]].forEach(([a, b]) => {
      const e1 = document.createElement('div'); e1.className = 'et'; e1.textContent = 'fuera';
      tabla.appendChild(e1);
      for (let i = a; i < b; i++) { const c = document.createElement('div'); c.textContent = ALF[i]; tabla.appendChild(c); }
      const e2 = document.createElement('div'); e2.className = 'et'; e2.textContent = 'dentro';
      tabla.appendChild(e2);
      for (let i = a; i < b; i++) { const c = document.createElement('div'); c.className = 'in'; c.textContent = ALF[(i + giro) % 26]; tabla.appendChild(c); }
    });
  }

  function pintar() {
    pintarDisco();
    pintarTabla();
    par.textContent = 'La A de fuera está sobre la ' + ALF[giro] + ' de dentro.' + (seleccionada ? '  Elige ahora una letra de fuera para la ' + seleccionada + '.' : '');
    par.dataset.giro = String(giro);
  }

  function pulsar(lado, l) {
    if (resuelto) return;
    if (lado === 'in') {
      seleccionada = seleccionada === l ? null : l;
    } else if (seleccionada) {
      // dejar la letra de dentro elegida justo bajo la letra de fuera pulsada
      giro = ((ALF.indexOf(seleccionada) - ALF.indexOf(l)) % 26 + 26) % 26;
      seleccionada = null;
    }
    pintar();
  }

  ui.button('◀ Girar', 'ghost', () => { if (!resuelto) { giro = (giro + 25) % 26; seleccionada = null; pintar(); } });
  ui.button('Girar ▶', 'ghost', () => { if (!resuelto) { giro = (giro + 1) % 26; seleccionada = null; pintar(); } });

  const render = () => { display.textContent = entered === '' ? '—' : entered; };
  ALF.split('').forEach(l => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'far-key';
    b.textContent = l;
    b.addEventListener('click', () => { if (!resuelto && entered.length < 10) { entered += l; render(); } });
    kb.appendChild(b);
  });

  ui.button('Borrar', 'ghost', () => { if (!resuelto) { entered = entered.slice(0, -1); render(); } });
  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    if (entered === PALABRA) {
      resuelto = true;
      ui.say('«El león guarda su corazón». Al decir su nombre, una trampilla se abre bajo la ventana y asoma un león mecánico. Coged la carta 36.', 'ok');
      kb.querySelectorAll('button').forEach(b => { b.disabled = true; });
    } else {
      ui.say('Esa palabra no abre nada. Revisad cómo está colocado el disco y descifrad el pergamino letra a letra.', 'bad');
    }
  });

  pintar();
  render();
  return { close: ui.close };
}
