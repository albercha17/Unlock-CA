// Carta 46 — El candado de rosetas: tres ruedas con el número de pétalos de cada roseta del suelo (cartas 40 a 43 juntas).
// Solución, de arriba abajo y de izquierda a derecha: 5, 3, 7.
import { openGame } from './ui.js';

const SOLUCION = [5, 3, 7];

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 46 — El candado de rosetas',
    instr: 'Cada rueda cuenta los pétalos de una roseta. Usa + y − para poner el número.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .pom-ruedas{display:flex;gap:14px;justify-content:center;margin:6px 0 14px}
    .pom-rueda{display:flex;flex-direction:column;align-items:center;gap:8px}
    .pom-rueda .val{width:64px;height:76px;border-radius:12px;border:3px solid #b8793c;background:linear-gradient(180deg,#2a1608,#4a2a12);color:#ffe2bd;display:flex;align-items:center;justify-content:center;font-size:2.4rem;font-weight:800;box-shadow:inset 0 0 16px rgba(0,0,0,.75)}
    .pom-rueda.ok .val{border-color:#9dffb0;color:#9dffb0}
    .pom-rueda button{width:64px;height:40px;border-radius:10px;border:2px solid #b8793c;background:linear-gradient(180deg,#8a5a2c,#4a2c14);color:#ffe2bd;font-size:1.4rem;font-weight:800;cursor:pointer;box-shadow:0 3px 0 #2a1608}
    .pom-rueda button:active{transform:translateY(2px);box-shadow:0 1px 0 #2a1608}
  `;
  ui.body.appendChild(style);

  const ruedas = document.createElement('div');
  ruedas.className = 'pom-ruedas';
  ui.body.appendChild(ruedas);

  const valores = SOLUCION.map(() => 1);
  let resuelto = false;

  function pintar() {
    ruedas.innerHTML = '';
    valores.forEach((v, i) => {
      const r = document.createElement('div');
      r.className = 'pom-rueda' + (resuelto ? ' ok' : '');
      r.dataset.i = String(i);
      r.innerHTML = '<button type="button" class="mas" aria-label="Sumar a la rueda ' + (i + 1) + '">+</button><div class="val" data-v="' + v + '">' + v + '</div><button type="button" class="menos" aria-label="Restar a la rueda ' + (i + 1) + '">−</button>';
      r.querySelector('.mas').addEventListener('click', () => { if (!resuelto) { valores[i] = valores[i] % 9 + 1; ui.say(''); pintar(); } });
      r.querySelector('.menos').addEventListener('click', () => { if (!resuelto) { valores[i] = (valores[i] + 7) % 9 + 1; ui.say(''); pintar(); } });
      ruedas.appendChild(r);
    });
  }

  ui.button('Abrir', 'primary', () => {
    if (resuelto) return;
    if (valores.every((v, i) => v === SOLUCION[i])) {
      resuelto = true;
      pintar();
      ui.say('El candado de bronce se abre con un clic y la puerta del comedor cede. Coged la carta 44.', 'ok');
    } else {
      ui.say('El candado no se abre. Juntad las cuatro placas del suelo y contad bien los pétalos de cada roseta, de arriba abajo y de izquierda a derecha.', 'bad');
    }
  });

  pintar();
  return { close: ui.close };
}
