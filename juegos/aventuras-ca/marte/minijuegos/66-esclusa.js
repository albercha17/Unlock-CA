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
    .far-bit{display:flex;flex-direction:column;align-items:center;gap:4px;padding:6px 0;border-radius:10px;border:1px solid rgba(255,255,255,.12);background:linear-gradient(rgba(6,10,16,.78),rgba(6,10,16,.92)),url(./img/ui/panel.jpg) center/cover;color:#9fb4c8;cursor:pointer;font:inherit;font-weight:700;overflow:hidden}
    .far-bit .luz{display:block;width:100%;height:62px;line-height:0}
    .far-bit .luz img{width:100%;height:100%;object-fit:contain;mix-blend-mode:screen}
    .far-bit.on{color:#fff;border-color:#ff9f43;box-shadow:0 0 10px rgba(255,159,67,.45)}
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
      b.innerHTML = '<span class="luz"><img alt="" src="./img/ui/interruptores/' + (activos[i] ? 'encendido' : 'apagado') + '.jpg"></span><span>' + p + '</span><small>' + (activos[i] ? '1' : '0') + '</small>';
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
      ui.say('ESCLUSA ABIERTA. Con el traje puesto, salís a la superficie de Marte. Coged la carta 41.', 'ok');
    } else {
      ui.say('Código incorrecto (' + total() + '). La esclusa permanece cerrada.', 'bad');
    }
  });

  pintar();
  return { close: ui.close };
}
