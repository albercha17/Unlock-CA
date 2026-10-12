// Carta 66 — Esclusa del reactor: 8 interruptores en binario. Código: 173 = 10101101 (dato del plano, carta 28).
import { openGame } from './ui.js';

const PESOS = [128, 64, 32, 16, 8, 4, 2, 1];
const CODIGO = 173;

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 66 — Esclusa del reactor',
    instr: 'Activa los interruptores cuyo valor suma el código de la esclusa.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .far-bits{display:grid;grid-template-columns:repeat(8,1fr);gap:6px;margin-bottom:10px}
    .far-bit{display:flex;flex-direction:column;align-items:center;gap:4px;padding:8px 0;border-radius:10px;border:1px solid rgba(255,255,255,.12);background:#0d1822;color:#9fb4c8;cursor:pointer;font:inherit;font-weight:700}
    .far-bit .luz{width:16px;height:16px;border-radius:50%;background:#2a3a48}
    .far-bit.on{color:#fff;border-color:#4cc9f0}
    .far-bit.on .luz{background:#4cc9f0;box-shadow:0 0 10px #4cc9f0}
    .far-bit small{font-size:.65rem;opacity:.7}
    .far-valor{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:1.3rem;color:#7dffb0;margin-bottom:6px}
  `;
  ui.body.appendChild(style);

  const fila = document.createElement('div');
  fila.className = 'far-bits';
  const valor = document.createElement('div');
  valor.className = 'far-valor';
  ui.body.append(fila, valor);

  const activos = PESOS.map(() => false);
  let resuelto = false;
  const total = () => PESOS.reduce((a, p, i) => a + (activos[i] ? p : 0), 0);

  function pintar() {
    fila.innerHTML = '';
    PESOS.forEach((p, i) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'far-bit' + (activos[i] ? ' on' : '');
      b.setAttribute('aria-pressed', String(activos[i]));
      b.innerHTML = '<span class="luz"></span><span>' + p + '</span><small>' + (activos[i] ? '1' : '0') + '</small>';
      b.addEventListener('click', () => {
        if (resuelto) return;
        activos[i] = !activos[i];
        ui.say('');
        pintar();
      });
      fila.appendChild(b);
    });
    valor.textContent = 'Valor: ' + total();
  }

  ui.button('Abrir esclusa', 'primary', () => {
    if (resuelto) return;
    if (total() === CODIGO) {
      resuelto = true;
      ui.say('ESCLUSA ABIERTA. Con el traje puesto, cruzáis al reactor. Coged la carta 79.', 'ok');
    } else {
      ui.say('Código incorrecto (' + total() + '). La esclusa permanece cerrada.', 'bad');
    }
  });

  pintar();
  return { close: ui.close };
}
