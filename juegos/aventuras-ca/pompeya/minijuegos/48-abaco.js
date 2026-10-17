// Carta 48 — El cofre del ábaco: dejar en el ábaco el número del fresco partido (cartas 52 y 53 juntas).
// Solución: centenas 4, decenas 7, unidades 2.
import { openGame } from './ui.js';

const VARILLAS = ['Centenas', 'Decenas', 'Unidades'];
const SOLUCION = [4, 7, 2];

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 48 — El cofre del ábaco',
    instr: 'Toca una cuenta para subir hasta ella las cuentas de esa varilla. Toca la última subida para bajarla.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .pom-abaco{display:flex;gap:16px;justify-content:center;margin:6px 0 14px;padding:14px 12px 10px;border-radius:12px;border:3px solid #6a4620;background:linear-gradient(180deg,#3a2210,#24140a);box-shadow:inset 0 0 22px rgba(0,0,0,.7)}
    .pom-varilla{display:flex;flex-direction:column;align-items:center;gap:6px}
    .pom-varilla h4{margin:0;font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;color:#f5c08a}
    .pom-varilla .eje{position:relative;display:flex;flex-direction:column;gap:3px;padding:6px 8px;background:linear-gradient(90deg,transparent 46%,#a77a42 46% 54%,transparent 54%)}
    .pom-cuenta{width:40px;height:20px;border-radius:10px;border:1px solid #1a0e06;background:radial-gradient(circle at 40% 30%,#c9b79a,#7c6a4e);cursor:pointer;padding:0;transition:transform .15s,background .15s}
    .pom-cuenta.arriba{background:radial-gradient(circle at 40% 30%,#ffd48a,#c9772a);transform:translateY(0)}
    .pom-varilla .v{font-size:1.4rem;font-weight:800;color:#ffe2bd}
    .pom-abaco.ok .pom-varilla .v{color:#9dffb0}
  `;
  ui.body.appendChild(style);

  const abaco = document.createElement('div');
  abaco.className = 'pom-abaco';
  ui.body.appendChild(abaco);

  const valores = VARILLAS.map(() => 0);
  let resuelto = false;

  function pintar() {
    abaco.className = 'pom-abaco' + (resuelto ? ' ok' : '');
    abaco.innerHTML = '';
    VARILLAS.forEach((nombre, r) => {
      const v = document.createElement('div');
      v.className = 'pom-varilla';
      v.dataset.r = String(r);
      v.innerHTML = '<h4>' + nombre + '</h4><div class="eje"></div><div class="v">' + valores[r] + '</div>';
      const eje = v.querySelector('.eje');
      // la cuenta n (1 = la de más arriba) está subida si n <= valor
      for (let n = 1; n <= 9; n++) {
        const b = document.createElement('button');
        b.type = 'button';
        b.className = 'pom-cuenta' + (n <= valores[r] ? ' arriba' : '');
        b.dataset.r = String(r);
        b.dataset.n = String(n);
        b.setAttribute('aria-label', nombre + ': cuenta ' + n);
        b.addEventListener('click', () => {
          if (resuelto) return;
          valores[r] = valores[r] === n ? n - 1 : n;
          ui.say('');
          pintar();
        });
        eje.appendChild(b);
      }
      abaco.appendChild(v);
    });
  }

  ui.button('Abrir el cofre', 'primary', () => {
    if (resuelto) return;
    if (valores.every((v, i) => v === SOLUCION[i])) {
      resuelto = true;
      pintar();
      ui.say('El cofre se abre con un chasquido. Dentro hay una lámpara de aceite de bronce. Coged la carta 58.', 'ok');
    } else {
      ui.say('El cofre sigue cerrado. Juntad las dos mitades del fresco: se lee un número de tres cifras. Cada varilla es una cifra.', 'bad');
    }
  });
  ui.button('Vaciar', '', () => { if (!resuelto) { valores.fill(0); ui.say(''); pintar(); } });

  pintar();
  return { close: ui.close };
}
