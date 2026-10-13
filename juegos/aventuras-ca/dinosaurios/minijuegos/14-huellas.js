// Carta 14 — Huellas en el barro: reconocer cuatro huellas con la guía de huellas (carta 16).
// Solución (de izquierda a derecha, arriba y abajo): Triceratops, Tiranosaurio, Anquilosaurio, Edmontosaurio.
import { openGame } from './ui.js';

const ESPECIES = ['Tiranosaurio', 'Edmontosaurio', 'Triceratops', 'Anquilosaurio'];
// huella que muestra cada casilla y especie correcta
const CASILLAS = [
  { img: 'triceratops', sol: 'Triceratops' },
  { img: 'tiranosaurio', sol: 'Tiranosaurio' },
  { img: 'anquilosaurio', sol: 'Anquilosaurio' },
  { img: 'edmontosaurio', sol: 'Edmontosaurio' }
];

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 14 — Huellas en el barro',
    instr: 'Toca cada huella para ir cambiando el nombre del dinosaurio que la dejó. Usa la guía de huellas.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .din-huellas{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;max-width:340px;margin:0 auto 10px;padding:12px;border-radius:12px;border:3px solid #4a3418;background:linear-gradient(rgba(20,12,4,.35),rgba(20,12,4,.55)),url(./img/ui/barro.jpg) center/cover;box-shadow:inset 0 0 26px rgba(0,0,0,.7)}
    .din-huella{display:flex;flex-direction:column;align-items:center;gap:6px;padding:0;border:0;background:none;cursor:pointer;font:inherit;color:#fff}
    .din-huella .foto{display:block;width:100%;aspect-ratio:1;border-radius:50%;overflow:hidden;border:3px solid #2a1b0a;box-shadow:inset 0 0 18px rgba(0,0,0,.65),0 4px 10px rgba(0,0,0,.55);transition:transform .15s}
    .din-huella .foto img{display:block;width:100%;height:100%;object-fit:cover}
    .din-huella:active .foto{transform:scale(.96)}
    .din-huella .nombre{min-width:100%;padding:6px 4px;border-radius:8px;background:rgba(0,0,0,.55);border:1px solid rgba(181,227,91,.5);font-weight:700;font-size:.85rem;color:#e6f6b8}
    .din-huella[data-esp=""] .nombre{color:#aab99a;font-weight:500}
    .din-huella.ok .nombre{border-color:#9dffb0;color:#9dffb0}
  `;
  ui.body.appendChild(style);

  const rejilla = document.createElement('div');
  rejilla.className = 'din-huellas';
  ui.body.appendChild(rejilla);

  const elegida = CASILLAS.map(() => 0);   // 0 = sin nombre, 1..4 = especie
  let resuelto = false;

  function pintar() {
    rejilla.innerHTML = '';
    CASILLAS.forEach((c, i) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'din-huella';
      b.dataset.i = String(i);
      b.dataset.esp = elegida[i] ? ESPECIES[elegida[i] - 1] : '';
      b.setAttribute('aria-label', 'Huella ' + (i + 1) + ': ' + (b.dataset.esp || 'sin nombre'));
      b.innerHTML = '<span class="foto"><img alt="" src="./img/ui/huellas/' + c.img + '.jpg"></span><span class="nombre">' + (b.dataset.esp || 'Toca para nombrar') + '</span>';
      b.addEventListener('click', () => {
        if (resuelto) return;
        elegida[i] = (elegida[i] + 1) % (ESPECIES.length + 1);
        ui.say('');
        pintar();
      });
      rejilla.appendChild(b);
    });
  }

  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    if (elegida.some(e => e === 0)) { ui.say('Falta poner nombre a alguna huella.', 'bad'); return; }
    const bien = CASILLAS.filter((c, i) => ESPECIES[elegida[i] - 1] === c.sol).length;
    if (bien === CASILLAS.length) {
      resuelto = true;
      rejilla.querySelectorAll('.din-huella').forEach(b => b.classList.add('ok'));
      ui.say('¡Las reconocéis todas! Un triceratops, un tiranosaurio, un anquilosaurio y un edmontosaurio han bajado al vado, y las huellas del tiranosaurio son las más frescas. Entre el barro encontráis un croquis del barranco. Coged la carta 26.', 'ok');
    } else {
      ui.say('Alguna huella no corresponde a ese dinosaurio. Comparad con la guía: dedos, garras y forma.', 'bad');
    }
  });

  pintar();
  return { close: ui.close };
}
