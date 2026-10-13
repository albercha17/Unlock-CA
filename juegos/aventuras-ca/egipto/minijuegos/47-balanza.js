// Carta 47 — Balanza de Maat: igualar el peso del corazón (17 deben, dato del papiro del juicio, carta 52).
import { openGame } from './ui.js';

const PESO_CORAZON = 17;
const PESAS = [3, 4, 6, 9, 11];
const NS = 'http://www.w3.org/2000/svg';

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 47 — Balanza de Maat',
    instr: 'Coloca pesas en el plato derecho hasta equilibrar el corazón. Toca una pesa para ponerla o quitarla.',
    ...opts
  });

  const svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('viewBox', '0 0 300 200');
  svg.setAttribute('width', '100%');
  svg.style.background = '#1d1508';
  svg.style.borderRadius = '10px';
  svg.style.marginBottom = '10px';
  const kg = document.createElement('div');
  kg.style.cssText = 'display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-bottom:8px';
  ui.body.append(svg, kg);

  const elegidas = new Set();
  let resuelto = false;

  function el(tag, attrs, parent) {
    const e = document.createElementNS(NS, tag);
    Object.keys(attrs).forEach(k => e.setAttribute(k, attrs[k]));
    (parent || svg).appendChild(e);
    return e;
  }

  function total() { return [...elegidas].reduce((a, b) => a + b, 0); }

  function pintar() {
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    const diff = total() - PESO_CORAZON;
    const ang = diff === 0 ? 0 : Math.max(-14, Math.min(14, diff * 3));
    const rad = ang * Math.PI / 180;
    const px = 150, py = 40, L = 100;
    const izq = [px - L * Math.cos(rad), py - L * Math.sin(rad)];
    const der = [px + L * Math.cos(rad), py + L * Math.sin(rad)];

    el('rect', { x: 144, y: 40, width: 12, height: 130, fill: '#b8893b' });
    el('rect', { x: 100, y: 168, width: 100, height: 12, rx: 4, fill: '#8a6a2a' });
    el('line', { x1: izq[0], y1: izq[1], x2: der[0], y2: der[1], stroke: '#e0b04a', 'stroke-width': 7, 'stroke-linecap': 'round' });
    el('circle', { cx: px, cy: py, r: 9, fill: '#e0b04a' });

    [[izq, '❤️'], [der, elegidas.size ? [...elegidas].sort((a, b) => a - b).join('+') : '']].forEach(([p, txt], i) => {
      el('line', { x1: p[0], y1: p[1], x2: p[0] - 34, y2: p[1] + 62, stroke: '#b8893b', 'stroke-width': 2 });
      el('line', { x1: p[0], y1: p[1], x2: p[0] + 34, y2: p[1] + 62, stroke: '#b8893b', 'stroke-width': 2 });
      el('path', { d: `M${p[0] - 40} ${p[1] + 62} h80 q-8 16 -40 16 q-32 0 -40 -16 z`, fill: '#e0b04a' });
      const t = el('text', { x: p[0], y: p[1] + 56, 'text-anchor': 'middle', 'font-size': i === 0 ? 24 : 15, fill: '#fff', 'font-family': 'system-ui,sans-serif', 'font-weight': 700 });
      t.textContent = txt;
    });
    if (diff === 0 && elegidas.size) {
      const t = el('text', { x: 150, y: 22, 'text-anchor': 'middle', 'font-size': 14, fill: '#9dffb0', 'font-family': 'system-ui,sans-serif', 'font-weight': 700 });
      t.textContent = 'EQUILIBRIO';
    }
  }

  PESAS.forEach(p => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'far-key';
    b.style.minWidth = '56px';
    b.textContent = p;
    b.addEventListener('click', () => {
      if (resuelto) return;
      if (elegidas.has(p)) { elegidas.delete(p); b.style.outline = ''; } else { elegidas.add(p); b.style.outline = '2px solid #ffd27a'; }
      ui.say('');
      pintar();
      if (total() === PESO_CORAZON) {
        resuelto = true;
        ui.say('¡Equilibrio perfecto! Maat aprueba el corazón y la puerta de la sala se abre. Coged la carta 63.', 'ok');
        kg.querySelectorAll('button').forEach(x => { x.disabled = true; });
      }
    });
    kg.appendChild(b);
  });

  pintar();
  return { close: ui.close };
}
