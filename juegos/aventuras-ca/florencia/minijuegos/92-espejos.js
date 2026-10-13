// Carta 92 — Rayo del amanecer: colocar la lente en uno de los tres atriles y tres espejos de modo que el rayo
// que entra por el lucernario (sobre la columna A) atraviese la lente y llegue al Cronoportal (A3).
// El plano (carta 94) dice: lente en el atril de la columna B, fila 3.
// Solución única: lente en B3; espejos \ en A2, \ en C2 y / en C3.
import { openGame } from './ui.js';

const NS = 'http://www.w3.org/2000/svg';
const COLS = 6, FILAS = 5, CELL = 52, MARGEN = 26;
const SOL_COL = 0;
const PORTAL = '0,2';
const ATRILES = ['3,4', '1,2', '4,2'];
const OBSTACULOS = ['2,0', '3,1', '3,3', '4,3', '4,4'];
const LETRAS = 'ABCDEF';
const MAX_ESPEJOS = 3;
const DIRS = { N: [0, -1], S: [0, 1], E: [1, 0], O: [-1, 0] };
const REFL = { '/': { E: 'N', N: 'E', O: 'S', S: 'O' }, '\\': { E: 'S', S: 'E', O: 'N', N: 'O' } };
const nombre = k => { const [x, y] = k.split(',').map(Number); return LETRAS[x] + (y + 1); };

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 92 — Rayo del amanecer',
    instr: 'Coloca la lente en un atril y tres espejos para llevar el rayo del lucernario hasta el Cronoportal. Toca un espejo ya puesto para girarlo o quitarlo.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .far-e-svg{display:block;width:100%;background:linear-gradient(rgba(14,8,3,.74),rgba(14,8,3,.88)),url(./img/ui/suelo.jpg) center/cover;border:2px solid #6b4a1e;border-radius:12px}
    .far-e-img{mix-blend-mode:screen}
    .far-e-cell{cursor:pointer}
    .far-e-tools{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:10px 0 6px}
    .far-e-tool{padding:10px 4px;border-radius:9px;border:2px solid rgba(255,255,255,.14);background:rgba(255,255,255,.06);color:#fff;font-weight:700;font-size:.85rem;cursor:pointer;font-family:inherit}
    .far-e-tool.sel{border-color:#ffd27a;color:#ffd27a;background:rgba(255,210,122,.16)}
    .far-e-info{color:#9fb4c8;font-size:.82rem;text-align:center;min-height:1.2em}
  `;
  ui.body.appendChild(style);

  const svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('viewBox', `${-MARGEN} ${-MARGEN - 8} ${COLS * CELL + 2 * MARGEN} ${FILAS * CELL + 2 * MARGEN + 8}`);
  svg.classList.add('far-e-svg');
  const tools = document.createElement('div');
  tools.className = 'far-e-tools';
  const info = document.createElement('div');
  info.className = 'far-e-info';
  ui.body.append(svg, tools, info);

  let herramienta = 'lente';
  let lente = null;                // clave "x,y" del atril con la lente
  const espejos = {};              // "x,y" -> '/' | '\\'
  let resuelto = false;

  function el(tag, attrs, texto) {
    const e = document.createElementNS(NS, tag);
    Object.keys(attrs).forEach(k => e.setAttribute(k, attrs[k]));
    if (texto !== undefined) e.textContent = texto;
    svg.appendChild(e);
    return e;
  }

  // Recorre el rayo desde el lucernario. Devuelve la lista de puntos, si llegó al portal y si pasó por la lente.
  function trazar() {
    let x = SOL_COL, y = 0, d = 'S';
    const puntos = [[x * CELL + CELL / 2, -MARGEN + 4]];
    let pasoLente = false, llega = false, fin = null;
    const visto = new Set();
    while (x >= 0 && x < COLS && y >= 0 && y < FILAS) {
      const k = x + ',' + y;
      const marca = k + d;
      if (visto.has(marca)) { fin = 'bucle'; break; }
      visto.add(marca);
      const cx = x * CELL + CELL / 2, cy = y * CELL + CELL / 2;
      if (OBSTACULOS.includes(k)) { puntos.push([cx, cy]); fin = 'obstaculo:' + k; break; }
      if (k === lente) pasoLente = true;
      if (k === PORTAL) { puntos.push([cx, cy]); llega = true; break; }
      if (espejos[k]) { puntos.push([cx, cy]); d = REFL[espejos[k]][d]; }
      x += DIRS[d][0]; y += DIRS[d][1];
    }
    if (!llega && fin === null) {
      // salió de la rejilla
      const [px, py] = [Math.max(-MARGEN + 4, Math.min(COLS * CELL + MARGEN - 4, x * CELL + CELL / 2)), Math.max(-MARGEN + 4, Math.min(FILAS * CELL + MARGEN - 4, y * CELL + CELL / 2))];
      puntos.push([px, py]);
      fin = 'borde';
    }
    return { puntos, llega, pasoLente, fin };
  }

  function pintar() {
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    svg.insertAdjacentHTML('beforeend', '<defs><linearGradient id="far-luna-g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".5" stop-color="#bcd4e6"/><stop offset="1" stop-color="#6d8aa3"/></linearGradient><radialGradient id="far-lente-g"><stop offset="0" stop-color="rgba(220,245,255,.5)"/><stop offset="1" stop-color="rgba(120,180,220,.22)"/></radialGradient></defs>');
    for (let c = 0; c < COLS; c++) el('text', { x: c * CELL + CELL / 2, y: -10, 'text-anchor': 'middle', 'font-size': 12, fill: '#e8d9b0', 'font-family': 'system-ui,sans-serif' }, LETRAS[c]);
    for (let r = 0; r < FILAS; r++) el('text', { x: -10, y: r * CELL + CELL / 2 + 4, 'text-anchor': 'middle', 'font-size': 12, fill: '#e8d9b0', 'font-family': 'system-ui,sans-serif' }, String(r + 1));
    for (let r = 0; r < FILAS; r++) {
      for (let c = 0; c < COLS; c++) {
        const k = c + ',' + r;
        const g = el('g', { class: 'far-e-cell', 'data-c': k });
        const rect = document.createElementNS(NS, 'rect');
        [['x', c * CELL + 1.5], ['y', r * CELL + 1.5], ['width', CELL - 3], ['height', CELL - 3], ['rx', 5], ['fill', 'rgba(0,0,0,.32)'], ['stroke', 'rgba(255,230,170,.08)']].forEach(([a, v]) => rect.setAttribute(a, v));
        g.appendChild(rect);
        svg.appendChild(g);
        g.addEventListener('click', () => pulsar(k));
      }
    }
    // elementos fijos
    OBSTACULOS.forEach(k => {
      const [x, y] = k.split(',').map(Number);
      el('image', { href: './img/ui/taller/columna.jpg', x: x * CELL + 5, y: y * CELL + 5, width: CELL - 10, height: CELL - 10, class: 'far-e-img', 'pointer-events': 'none' });
    });
    ATRILES.forEach(k => {
      const [x, y] = k.split(',').map(Number);
      el('image', { href: './img/ui/taller/atril.jpg', x: x * CELL + 3, y: y * CELL + 3, width: CELL - 6, height: CELL - 6, class: 'far-e-img', 'pointer-events': 'none' });
      if (k === lente) {
        el('circle', { cx: x * CELL + CELL / 2, cy: y * CELL + CELL / 2 - 1, r: 15, fill: 'url(#far-lente-g)', stroke: 'rgba(235,250,255,.9)', 'stroke-width': 2, 'pointer-events': 'none' });
        el('path', { d: `M${x * CELL + CELL / 2 - 9} ${y * CELL + CELL / 2 - 6} a11 11 0 0 1 9 -6`, fill: 'none', stroke: 'rgba(255,255,255,.9)', 'stroke-width': 2.2, 'stroke-linecap': 'round', 'pointer-events': 'none' });
      }
    });
    const [px, py] = PORTAL.split(',').map(Number);
    el('image', { href: './img/ui/taller/portal.jpg', x: px * CELL + 2, y: py * CELL + 2, width: CELL - 4, height: CELL - 4, class: 'far-e-img', 'pointer-events': 'none' });
    el('image', { href: './img/ui/taller/claraboya.jpg', x: SOL_COL * CELL + CELL / 2 - 17, y: -MARGEN - 8, width: 34, height: 34, class: 'far-e-img', 'pointer-events': 'none' });
    // espejos
    Object.keys(espejos).forEach(k => {
      const [x, y] = k.split(',').map(Number);
      const cx = x * CELL + CELL / 2, cy = y * CELL + CELL / 2;
      const g = el('g', { transform: `translate(${cx} ${cy}) rotate(${espejos[k] === '/' ? -45 : 45})`, 'pointer-events': 'none' });
      const marco = el('rect', { x: -21, y: -5.5, width: 42, height: 11, rx: 3, fill: '#8a6420', stroke: '#e3b34f', 'stroke-width': 1.5 });
      const luna = el('rect', { x: -18, y: -3, width: 36, height: 6, rx: 1.5, fill: 'url(#far-luna-g)', class: 'far-e-espejo', 'data-c': k, 'data-o': espejos[k] });
      [marco, luna].forEach(n => g.appendChild(n));
    });
    // rayo
    const t = trazar();
    const pts = t.puntos.map(p => p.join(',')).join(' ');
    el('polyline', { points: pts, fill: 'none', stroke: 'rgba(255,210,100,.35)', 'stroke-width': 9, 'stroke-linejoin': 'round', 'pointer-events': 'none' });
    el('polyline', { points: pts, fill: 'none', stroke: '#fff1b0', 'stroke-width': 3, 'stroke-linejoin': 'round', 'pointer-events': 'none' });
    // herramientas
    tools.innerHTML = '';
    [['lente', 'Lente'], ['espejo', 'Espejo (' + (MAX_ESPEJOS - Object.keys(espejos).length) + ')'], ['quitar', 'Quitar']].forEach(([id, txt]) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'far-e-tool' + (herramienta === id ? ' sel' : '');
      b.dataset.tool = id;
      b.textContent = txt;
      b.addEventListener('click', () => { herramienta = id; pintar(); });
      tools.appendChild(b);
    });
    info.textContent = lente ? 'Lente en ' + nombre(lente) + ' · Espejos: ' + (Object.keys(espejos).map(k => nombre(k) + ' ' + espejos[k]).join(', ') || 'ninguno') : 'Aún no hay lente colocada.';
  }

  function pulsar(k) {
    if (resuelto) return;
    ui.say('');
    if (herramienta === 'lente') {
      if (!ATRILES.includes(k)) { ui.say('La lente solo cabe en un atril (los círculos de puntos).', 'bad'); return; }
      lente = k;
    } else if (herramienta === 'quitar') {
      if (k === lente) lente = null;
      delete espejos[k];
    } else {
      if (OBSTACULOS.includes(k) || ATRILES.includes(k) || k === PORTAL) { ui.say('Ahí no se puede poner un espejo.', 'bad'); return; }
      if (espejos[k] === '/') espejos[k] = '\\';
      else if (espejos[k] === '\\') delete espejos[k];
      else {
        if (Object.keys(espejos).length >= MAX_ESPEJOS) { ui.say('Solo tenéis tres espejos: quitad uno antes.', 'bad'); return; }
        espejos[k] = '/';
      }
    }
    pintar();
  }

  ui.button('Probar', 'primary', () => {
    if (resuelto) return;
    if (!lente) { ui.say('Falta la lente: colócala en uno de los atriles.', 'bad'); return; }
    const t = trazar();
    if (t.llega && t.pasoLente) {
      resuelto = true;
      ui.say('El rayo atraviesa la lente, se concentra y llega al Cronoportal, que despierta con un destello dorado. ¡El portal de vuelta se abre! Coged la carta 99.', 'ok');
    } else if (t.llega) {
      ui.say('El rayo llega al Cronoportal, pero sin pasar por la lente: la luz no se concentra y no basta.', 'bad');
    } else if (t.fin && t.fin.startsWith('obstaculo')) {
      ui.say('El rayo se detiene contra una columna en ' + nombre(t.fin.split(':')[1]) + '.', 'bad');
    } else if (t.fin === 'bucle') {
      ui.say('El rayo da vueltas sin llegar a ninguna parte.', 'bad');
    } else {
      ui.say('El rayo se pierde fuera del taller. Probad otra colocación.', 'bad');
    }
  });

  pintar();
  return { close: ui.close };
}
