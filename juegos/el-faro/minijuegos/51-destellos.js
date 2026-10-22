// Carta 51 — El temporizador de la lente: programar, segundo a segundo, la característica de la luz de Cabo Niebla, con el almanaque de faros (cartas 61 y 63) y la
// nota de Anselmo sobre cómo leerlo (carta 26). Patrón de herramientas/instancias_faro.py (destellos).
import { openGame } from './ui.js';

const D = /*DATOS*/{"periodo": 15, "solucion": [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 51 — El temporizador de la lente',
    instr: 'Cada casilla es un segundo del ciclo de la luz. Tocad las casillas en las que la luz debe estar encendida y pulsad «Programar». El almanaque está en las cartas 61 y 63 y la nota de Anselmo, en la 26.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .far-tira{display:grid;grid-template-columns:repeat(${D.periodo},1fr);gap:2px;width:min(92vw,350px);margin:14px auto 22px}
    .far-seg{aspect-ratio:1 / 2.2;border:2px solid #1a2a36;border-radius:4px;background:#22303c;cursor:pointer;padding:0;position:relative}
    .far-seg.on{background:linear-gradient(180deg,#fff2b0,#ffc83a);box-shadow:0 0 10px #ffd84a}
    .far-seg span{position:absolute;left:0;right:0;bottom:-18px;font:600 .55rem system-ui;color:#cfe3ee}
    .far-tira.ok{outline:3px solid #7be495;outline-offset:4px;border-radius:6px}
  `;
  ui.body.appendChild(style);
  const tira = document.createElement('div');
  tira.className = 'far-tira';
  ui.body.appendChild(tira);

  const v = new Array(D.periodo).fill(0);
  let resuelto = false;
  for (let s = 0; s < D.periodo; s++) {
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
      ui.say('El temporizador hace clic y la lente queda lista para dar la luz de Cabo Niebla: el capitán la reconocerá. Se oye un crujido en el piso de arriba. Coged la carta 58.', 'ok');
    } else {
      ui.say('Esa no es la luz de Cabo Niebla: el capitán la confundiría con otro faro. Repasad el almanaque (cartas 61 y 63) y la nota de Anselmo (carta 26).', 'bad');
    }
  });
  ui.button('Apagar todo', '', () => { if (!resuelto) { v.fill(0); tira.querySelectorAll('.on').forEach(x => x.classList.remove('on')); ui.say(''); } });
  return { close: ui.close };
}
