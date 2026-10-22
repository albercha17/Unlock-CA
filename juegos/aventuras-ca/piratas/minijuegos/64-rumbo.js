// Carta 64 — El timón: fijar en la brújula el rumbo que debe marcar la aguja. La carta náutica plegada (carta 66) da el rumbo verdadero con arrecifes en
// forma de cifras; el cuaderno del piloto (carta 67) dibuja la aguja torcida hacia el oeste. Desplegada, la carta náutica enseña cifras falsas.
// Instancia de herramientas/instancias_piratas.py (RUMBO).
import { openGame } from './ui.js';

const R = /*DATOS*/{"carta": "86", "aguja": 111, "senuelos": ["68", "95"]}/*FIN*/;

export function startMinigame(opts = {}) {
  const SOLUCION = R.aguja;
  const VERDADERO = Number(R.carta);
  const SENUELOS = R.senuelos.map(Number).concat(R.senuelos.map(s => Number(s.split('').reverse().join(''))));
  const ui = openGame({
    title: 'Carta 64 — El timón',
    instr: 'Gira la rosa de la brújula hasta el rumbo que debe marcar la aguja y fija el timón. El rumbo verdadero está en la carta náutica plegada (carta 66); el desvío de la aguja, en el cuaderno del piloto (carta 67).',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .pir-bitacora{position:relative;width:min(70vw,250px);aspect-ratio:1;margin:4px auto 10px;border-radius:50%;background:radial-gradient(circle,#3a2a18 0 62%,#b88a26 63% 66%,#5a3c1a 67%);box-shadow:0 6px 18px rgba(0,0,0,.5),inset 0 0 0 4px #e8b84a}
    .pir-rosa{position:absolute;inset:8%;background:center / contain no-repeat;transition:transform .35s ease}
    .pir-fiel{position:absolute;left:50%;top:1%;width:0;height:0;border-left:11px solid transparent;border-right:11px solid transparent;border-top:22px solid #e03a2a;transform:translateX(-50%);filter:drop-shadow(0 2px 2px rgba(0,0,0,.6))}
    .pir-lectura{text-align:center;font:700 1.5rem 'Pirata One',Georgia,serif;color:#f6e7b8;margin:0 0 8px;letter-spacing:.04em}
    .pir-giros{display:flex;gap:8px;justify-content:center;margin-bottom:10px}
    .pir-giros button{min-width:58px;min-height:48px;border-radius:10px;border:2px solid #e8b84a;background:#173a46;color:#f6e7b8;font:700 1rem system-ui,sans-serif;cursor:pointer}
    .pir-bitacora.ok{box-shadow:0 0 30px rgba(120,230,150,.7),inset 0 0 0 4px #7be495}
  `;
  ui.body.appendChild(style);

  const bit = document.createElement('div');
  bit.className = 'pir-bitacora';
  bit.innerHTML = '<div class="pir-rosa" style="background-image:url(\'./img/ui/rosa.png\')"></div><div class="pir-fiel"></div>';
  const lectura = document.createElement('p');
  lectura.className = 'pir-lectura';
  const giros = document.createElement('div');
  giros.className = 'pir-giros';
  ui.body.appendChild(bit);
  ui.body.appendChild(lectura);
  ui.body.appendChild(giros);

  let rumbo = 0;
  let resuelto = false;
  const rosa = bit.querySelector('.pir-rosa');

  function pintar() {
    rosa.style.transform = 'rotate(' + (-rumbo) + 'deg)';
    lectura.textContent = 'Rumbo de la aguja: ' + String(rumbo).padStart(3, '0') + '°';
  }

  [-10, -1, 1, 10].forEach(d => {
    const b = document.createElement('button');
    b.type = 'button';
    b.dataset.d = String(d);
    b.textContent = (d > 0 ? '+' : '−') + Math.abs(d) + '°';
    b.setAttribute('aria-label', (d > 0 ? 'Girar ' : 'Girar al revés ') + Math.abs(d) + ' grados');
    b.addEventListener('click', () => {
      if (resuelto) return;
      rumbo = (rumbo + d + 360) % 360;
      ui.say('');
      pintar();
    });
    giros.appendChild(b);
  });

  ui.button('Fijar el rumbo', 'primary', () => {
    if (resuelto) return;
    if (rumbo === SOLUCION) {
      resuelto = true;
      bit.classList.add('ok');
      ui.say('¡Rumbo fijado! La Gaviota vira y pone proa a la Isla Calavera con el viento a favor. La capitana Bruma asiente: «Por fin alguien que sabe leer una carta». Coged la carta 62.', 'ok');
    } else if (rumbo === VERDADERO) {
      ui.say('Ese es el rumbo de la carta náutica, pero el timón obedece a la aguja, y en este mar la aguja se tuerce. Mirad el cuaderno del piloto (carta 67).', 'bad');
    } else if (SENUELOS.includes(rumbo)) {
      ui.say('¡Ese rumbo lleva derecho a los arrecifes! La carta náutica desplegada engaña: buscad las líneas A y B.', 'bad');
    } else {
      ui.say('La capitana mira la brújula y niega con la cabeza: con ese rumbo no se llega a la Isla Calavera.', 'bad');
    }
  });

  pintar();
  return { close: ui.close };
}
