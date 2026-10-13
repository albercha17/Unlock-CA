// Carta 95 — Panel de arranque: ordenar 5 pasos. El orden sale del cuaderno (carta 15).
import { openGame } from './ui.js';

const ORDER = [
  'Abrir la válvula del aceite',
  'Cebar la mecha',
  'Girar el engranaje',
  'Encender el piloto',
  'Soltar el freno de la lente'
];

const ICONO = {
  'Abrir la válvula del aceite': '🛢️',
  'Cebar la mecha': '🕯️',
  'Girar el engranaje': '⚙️',
  'Encender el piloto': '🔥',
  'Soltar el freno de la lente': '🔓'
};

function shuffle(a) {
  const r = a.slice();
  for (let i = r.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [r[i], r[j]] = [r[j], r[i]];
  }
  return r;
}

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 95 — Panel de arranque',
    instr: 'Toca los pasos en el orden en que hay que hacerlos. Toca uno colocado para quitarlo.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .far-seq{display:flex;flex-direction:column;gap:8px;margin-bottom:12px;text-align:left}
    .far-step{display:flex;gap:10px;align-items:center;width:100%;padding:11px 12px;border-radius:10px;border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.05);color:#fff;font:inherit;font-size:.92rem;cursor:pointer;text-align:left}
    .far-step:hover{background:rgba(255,255,255,.1)}
    .far-step .n{flex:0 0 26px;height:26px;border-radius:50%;background:#26323f;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:.8rem}
    .far-step .ico{font-size:1.3rem;filter:grayscale(.6);transition:filter .2s}
    .far-step.placed .ico{filter:none}
    .far-step.placed .n{background:#ffd27a;color:#2a1600}
    .far-step.placed{border-color:#ffd27a}
  `;
  ui.body.appendChild(style);
  const list = document.createElement('div');
  list.className = 'far-seq';
  ui.body.appendChild(list);

  const steps = shuffle(ORDER);
  let chosen = [];
  let done = false;

  function render() {
    list.innerHTML = '';
    steps.forEach(text => {
      const idx = chosen.indexOf(text);
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'far-step' + (idx >= 0 ? ' placed' : '');
      const n = document.createElement('span');
      n.className = 'n';
      n.textContent = idx >= 0 ? String(idx + 1) : '·';
      const ico = document.createElement('span');
      ico.className = 'ico';
      ico.textContent = ICONO[text] || '';
      ico.setAttribute('aria-hidden', 'true');
      const t = document.createElement('span');
      t.textContent = text;
      b.append(n, ico, t);
      b.addEventListener('click', () => {
        if (done) return;
        if (idx >= 0) chosen.splice(idx, 1); else chosen.push(text);
        ui.say('');
        render();
      });
      list.appendChild(b);
    });
  }

  ui.button('Reiniciar', 'ghost', () => { if (!done) { chosen = []; ui.say(''); render(); } });
  ui.button('Arrancar', 'primary', () => {
    if (done) return;
    if (chosen.length < ORDER.length) { ui.say('Colocad los cinco pasos.', 'bad'); return; }
    const right = chosen.filter((t, i) => t === ORDER[i]).length;
    if (right === ORDER.length) {
      done = true;
      ui.say('¡La lámpara se enciende y la lente empieza a girar! Coged la carta 99.', 'ok');
    } else {
      ui.say(`${right} de 5 pasos están en su sitio. Revisad el cuaderno.`, 'bad');
    }
  });

  render();
  return { close: ui.close };
}
