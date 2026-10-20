// Carta 65 — El temporizador de la lente: programar, segundo a segundo, la característica de la luz de Cabo Niebla (almanaque, carta
// 66; cómo leerlo, carta 67). Patrón de herramientas/instancias_ampliacion.py.
import { openGame } from './ui.js';

const D = /*DATOS*/{"solucion": [1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0]}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 65 — El temporizador de la lente',
    instr: 'Cada casilla es un segundo de los doce del ciclo. Tocad las casillas en las que la luz debe estar encendida y pulsad «Programar».',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .far-tira{display:grid;grid-template-columns:repeat(12,1fr);gap:3px;width:min(90vw,340px);margin:14px auto 4px}
    .far-seg{aspect-ratio:1 / 2;border:2px solid #1a2a36;border-radius:4px;background:#22303c;cursor:pointer;padding:0;position:relative}
    .far-seg.on{background:linear-gradient(180deg,#fff2b0,#ffc83a);box-shadow:0 0 10px #ffd84a}
    .far-seg span{position:absolute;left:0;right:0;bottom:-18px;font:600 .6rem system-ui;color:#cfe3ee}
    .far-tira.ok{outline:3px solid #7be495;outline-offset:4px;border-radius:6px}
  `;
  ui.body.appendChild(style);
  const tira = document.createElement('div');
  tira.className = 'far-tira';
  ui.body.appendChild(tira);

  const v = new Array(12).fill(0);
  let resuelto = false;
  for (let s = 0; s < 12; s++) {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'far-seg';
    b.dataset.s = String(s);
    b.innerHTML = '<span>' + (s + 1) + '</span>';
    b.setAttribute('aria-label', 'Segundo ' + (s + 1));
    b.addEventListener('click', () => {
      if (resuelto) return;
      v[s] = 1 - v[s];
      b.classList.toggle('on', !!v[s]);
      ui.say('');
    });
    tira.appendChild(b);
  }

  ui.button('Programar', 'primary', () => {
    if (resuelto) return;
    if (v.every((x, i) => x === D.solucion[i])) {
      resuelto = true;
      tira.classList.add('ok');
      ui.say('El temporizador hace clic y la lente queda lista para dar la luz de Cabo Niebla: el capitán la reconocerá. Subís a lo más alto del faro. Coged la carta 78.', 'ok');
    } else {
      ui.say('Esa no es la luz de Cabo Niebla: el capitán la confundiría con otro faro. Repasad el almanaque (carta 66) y la nota de Anselmo (carta 67).', 'bad');
    }
  });
  ui.button('Apagar todo', '', () => { if (!resuelto) { v.fill(0); tira.querySelectorAll('.on').forEach(x => x.classList.remove('on')); ui.say(''); } });
  return { close: ui.close };
}
