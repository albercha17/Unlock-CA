// Carta 21 — Terminal de seguridad: descubrir un código de 4 cifras (1 a 6, sin repetir) con pistas tipo Mastermind.
// Código: 4 1 6 3. La nota adhesiva (carta 25) dice que no lleva 2 ni 5.
import { openGame } from './ui.js';

const SECRETO = [4, 1, 6, 3];

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 21 — Terminal de seguridad',
    instr: 'Descubre el código de 4 cifras. ● = cifra bien colocada, ○ = existe pero en otro sitio.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .far-term{background:#06140d;border:1px solid #1f5a3a;border-radius:10px;padding:10px 12px;margin-bottom:10px;min-height:110px;max-height:170px;overflow:auto;text-align:left;font-family:"IBM Plex Mono",ui-monospace,Consolas,monospace;color:#7dffb0;font-size:.95rem}
    .far-term div{padding:2px 0;letter-spacing:.12em}
    .far-term .vacio{opacity:.55;letter-spacing:0}
    .far-pad4{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:10px}
  `;
  ui.body.appendChild(style);

  const hist = document.createElement('div');
  hist.className = 'far-term';
  hist.innerHTML = '<div class="vacio">Esperando código...</div>';
  const display = document.createElement('div');
  display.className = 'far-display';
  const pad = document.createElement('div');
  pad.className = 'far-pad4';
  ui.body.append(hist, display, pad);

  let entered = [];
  let resuelto = false;
  const render = () => { display.textContent = entered.length ? entered.join(' ') : '—'; };

  function comprobar() {
    if (resuelto) return;
    if (entered.length < 4) { ui.say('Introduce las 4 cifras.', 'bad'); return; }
    const exactas = entered.filter((v, i) => v === SECRETO[i]).length;
    let comunes = 0;
    for (let d = 1; d <= 6; d++) {
      comunes += Math.min(entered.filter(v => v === d).length, SECRETO.filter(v => v === d).length);
    }
    const parciales = comunes - exactas;
    if (hist.querySelector('.vacio')) hist.innerHTML = '';
    const fila = document.createElement('div');
    fila.textContent = entered.join(' ') + '   ' + ('●'.repeat(exactas) + '○'.repeat(parciales) || '·');
    hist.appendChild(fila);
    hist.scrollTop = hist.scrollHeight;
    if (exactas === 4) {
      resuelto = true;
      ui.say('ACCESO CONCEDIDO. La puerta de seguridad se abre. Coged la carta 44.', 'ok');
      pad.querySelectorAll('button').forEach(b => { b.disabled = true; });
    } else {
      ui.say('');
    }
    entered = [];
    render();
  }

  ['1', '2', '3', '4', '5', '6', '⌫', '✓'].forEach(k => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'far-key';
    b.textContent = k;
    b.addEventListener('click', () => {
      if (resuelto) return;
      if (k === '⌫') { entered.pop(); render(); return; }
      if (k === '✓') { comprobar(); return; }
      if (entered.length < 4) { entered.push(Number(k)); render(); }
    });
    pad.appendChild(b);
  });

  render();
  return { close: ui.close };
}
