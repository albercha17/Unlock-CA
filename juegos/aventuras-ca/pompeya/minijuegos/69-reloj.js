// Carta 69 — La rueda del reloj de sol: girar el puntero hasta la marca a la que llega la sombra del mosaico (cartas 64 a 67 juntas).
// Solución: la séptima marca contando desde la estrella, en el sentido de las agujas del reloj (la estrella es la marca 0).
import { openGame } from './ui.js';

const MARCAS = 12;
const SOLUCION = 7;

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 69 — La rueda del reloj de sol',
    instr: 'Toca la marca a la que quieres llevar el puntero. La estrella es el comienzo de las horas.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .pom-reloj{position:relative;width:260px;height:260px;margin:6px auto 12px;border-radius:50%;border:4px solid #b8793c;background:radial-gradient(circle,#4a2a12,#24140a);box-shadow:inset 0 0 26px rgba(0,0,0,.8)}
    .pom-marca{position:absolute;width:32px;height:32px;margin:-16px 0 0 -16px;border-radius:50%;border:2px solid #f5c08a;background:#6a3c1a;color:#ffe2bd;font-size:.8rem;font-weight:700;padding:0;cursor:pointer;display:flex;align-items:center;justify-content:center}
    .pom-marca.estrella{background:#c9772a;border-color:#ffd48a}
    .pom-marca.elegida{background:#e08a4a;border-color:#fff;box-shadow:0 0 12px #f5c08a}
    .pom-reloj.ok .pom-marca.elegida{background:#3a9a56;border-color:#9dffb0;box-shadow:0 0 14px #9dffb0}
    .pom-puntero{position:absolute;left:50%;top:50%;width:6px;height:96px;margin:-96px 0 0 -3px;border-radius:3px;background:linear-gradient(#ffd48a,#c9772a);transform-origin:50% 100%;transition:transform .35s ease}
    .pom-centro{position:absolute;left:50%;top:50%;width:22px;height:22px;margin:-11px 0 0 -11px;border-radius:50%;background:#f5c08a;border:2px solid #6a3c1a}
  `;
  ui.body.appendChild(style);

  const reloj = document.createElement('div');
  reloj.className = 'pom-reloj';
  ui.body.appendChild(reloj);

  let elegida = 0;
  let resuelto = false;

  function pintar() {
    reloj.className = 'pom-reloj' + (resuelto ? ' ok' : '');
    reloj.innerHTML = '';
    for (let k = 0; k < MARCAS; k++) {
      const ang = -Math.PI / 2 + k * Math.PI * 2 / MARCAS;
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'pom-marca' + (k === 0 ? ' estrella' : '') + (k === elegida ? ' elegida' : '');
      b.dataset.k = String(k);
      b.style.left = (130 + 108 * Math.cos(ang)) + 'px';
      b.style.top = (130 + 108 * Math.sin(ang)) + 'px';
      b.setAttribute('aria-label', k === 0 ? 'Marca de la estrella' : 'Marca ' + k);
      if (k === 0) b.innerHTML = '<svg viewBox="0 0 40 40" width="20" height="20" aria-hidden="true" fill="currentColor"><polygon points="20,4 24.5,15 36,15.5 27,23 30,35 20,28 10,35 13,23 4,15.5 15.5,15"/></svg>';
      else b.textContent = String(k);
      b.addEventListener('click', () => { if (!resuelto) { elegida = k; ui.say(''); pintar(); } });
      reloj.appendChild(b);
    }
    const p = document.createElement('div');
    p.className = 'pom-puntero';
    p.style.transform = 'rotate(' + (elegida * 360 / MARCAS) + 'deg)';
    reloj.appendChild(p);
    const c = document.createElement('div');
    c.className = 'pom-centro';
    reloj.appendChild(c);
  }

  ui.button('Girar la rueda', 'primary', () => {
    if (resuelto) return;
    if (elegida === SOLUCION) {
      resuelto = true;
      pintar();
      ui.say('La rueda gira, el mosaico se ilumina y la pared del fondo se desliza: aparece la sala del altar. Coged la carta 82.', 'ok');
    } else {
      ui.say('Nada se mueve. Contad las marcas en el sentido de las agujas del reloj desde la estrella (la estrella no cuenta) hasta donde llega la sombra.', 'bad');
    }
  });

  pintar();
  return { close: ui.close };
}
