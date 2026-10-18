// Lector de páginas (no hay nada que resolver). No pausa el temporizador: leer también cuesta tiempo.
import { openGame } from './ui.js';

const STYLE_ID = 'far-lector-style';

function inyectarEstilo() {
  if (document.getElementById(STYLE_ID)) return;
  const s = document.createElement('style');
  s.id = STYLE_ID;
  s.textContent = `
    .far-hoja{border-radius:8px;padding:16px 16px 14px;text-align:left;min-height:260px}
    .far-hoja h4{margin:0 0 10px;font-size:1.05rem;font-style:italic;padding-bottom:6px;border-bottom:1px solid currentColor}
    .far-hoja p{margin:0 0 10px;font-size:.95rem;line-height:1.45}
    .far-hoja .pie{font-size:.82rem;font-style:italic;opacity:.85;margin-top:10px}
    .far-hoja.papiro{background:#e9d9a8;color:#3a2a10;font-family:Georgia,"Times New Roman",serif;box-shadow:inset 0 0 22px rgba(90,60,20,.3)}
    .far-hoja.terminal{background:#06140d;color:#7dffb0;font-family:"IBM Plex Mono",ui-monospace,Consolas,monospace;border:1px solid #1f5a3a;box-shadow:inset 0 0 18px rgba(40,255,140,.12)}
    .far-hoja.terminal h4{font-style:normal;text-transform:uppercase;letter-spacing:.05em;font-size:.9rem}
    .far-pag{margin-top:10px;color:#93a4b5;font-size:.85rem}
  `;
  document.head.appendChild(s);
}

export function abrirLector({ titulo, instr, paginas, tema, opts = {} }) {
  inyectarEstilo();
  const ui = openGame({ title: titulo, instr, onClose: opts.onClose });

  const hoja = document.createElement('div');
  hoja.className = 'far-hoja ' + tema;
  const pag = document.createElement('div');
  pag.className = 'far-pag';
  ui.body.append(hoja, pag);

  let i = 0;
  function pintar() {
    const p = paginas[i];
    hoja.innerHTML = '';
    const h = document.createElement('h4');
    h.textContent = p.titulo;
    hoja.appendChild(h);
    (p.texto || []).forEach(linea => {
      const el = document.createElement('p');
      el.textContent = linea;
      hoja.appendChild(el);
    });
    if (p.pie) {
      const el = document.createElement('p');
      el.className = 'pie';
      el.textContent = p.pie;
      hoja.appendChild(el);
    }
    pag.textContent = 'Página ' + (i + 1) + ' de ' + paginas.length;
    ant.disabled = i === 0;
    sig.disabled = i === paginas.length - 1;
  }

  const ant = ui.button('← Anterior', 'ghost', () => { if (i > 0) { i--; pintar(); } });
  const sig = ui.button('Siguiente →', 'primary', () => { if (i < paginas.length - 1) { i++; pintar(); } });

  function onKey(e) {
    if (e.key === 'ArrowLeft') ant.click();
    if (e.key === 'ArrowRight') sig.click();
  }
  document.addEventListener('keydown', onKey);
  ui.onClose(() => document.removeEventListener('keydown', onKey));

  pintar();
  return { close: ui.close };
}
