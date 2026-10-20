// Carta 42 — La losa: 5 x 5 piedras sin números (los números están en las franjas de papiro, cartas 45, 48 y 49). Hay que tapar con
// arena los que sobran (tipo Hitori). Solución única (herramientas/instancias_ampliacion.py).
import { openGame } from './ui.js';

const T = /*DATOS*/{"tachadas": [[1, 1], [1, 3], [2, 2], [2, 4], [3, 1], [4, 3]]}/*FIN*/;
const N = 5;

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 42 — La losa',
    instr: 'Tocad una piedra para taparla con arena (otra vez para destaparla). Los números están en las tres franjas de papiro. Tapad los que sobran y pulsad «Comprobar».',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .egi-losa{display:grid;grid-template-columns:repeat(5,1fr);gap:4px;width:min(82vw,300px);margin:6px auto;padding:8px;border-radius:6px;background:#5a4a34;border:4px solid #a08a60}
    .egi-piedra{aspect-ratio:1;border:2px solid #3a2e1e;border-radius:4px;cursor:pointer;padding:0;position:relative;
      background:radial-gradient(circle at 30% 25%,#c8b896,#9a8a6a 70%)}
    .egi-piedra span{position:absolute;left:3px;top:1px;font:600 .55rem system-ui;color:#3a2e1e}
    .egi-piedra.arena{background:radial-gradient(circle at 40% 35%,#f0d890,#d0a850 70%);box-shadow:inset 0 0 10px rgba(120,80,20,.6)}
    .egi-losa.ok{border-color:#7be495}
  `;
  ui.body.appendChild(style);
  const losa = document.createElement('div');
  losa.className = 'egi-losa';
  ui.body.appendChild(losa);

  const tap = new Set();
  let resuelto = false;
  for (let f = 0; f < N; f++) {
    for (let c = 0; c < N; c++) {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'egi-piedra';
      b.dataset.f = String(f);
      b.dataset.c = String(c);
      b.innerHTML = '<span>' + (f + 1) + '·' + (c + 1) + '</span>';
      b.setAttribute('aria-label', 'Piedra de la fila ' + (f + 1) + ', columna ' + (c + 1));
      b.addEventListener('click', () => {
        if (resuelto) return;
        const k = f + ',' + c;
        tap.has(k) ? tap.delete(k) : tap.add(k);
        b.classList.toggle('arena', tap.has(k));
        ui.say('');
      });
      losa.appendChild(b);
    }
  }

  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    const sol = new Set(T.tachadas.map(([f, c]) => f + ',' + c));
    if (sol.size === tap.size && [...sol].every(k => tap.has(k))) {
      resuelto = true;
      losa.classList.add('ok');
      ui.say('La arena se cuela entre las piedras tapadas y, con un crujido, se abre la puerta de la sala del sarcófago. Coged la carta 33.', 'ok');
    } else {
      ui.say('La losa no se mueve. Juntad las tres franjas (cartas 45, 48 y 49): que no se repita ningún número a la vista en filas ni columnas, sin tapadas juntas y sin dejar piedras aisladas.', 'bad');
    }
  });
  ui.button('Destapar todo', '', () => { if (!resuelto) { tap.clear(); losa.querySelectorAll('.arena').forEach(x => x.classList.remove('arena')); ui.say(''); } });
  return { close: ui.close };
}
