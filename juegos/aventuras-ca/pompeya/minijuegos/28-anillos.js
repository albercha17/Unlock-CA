// Carta 28 — El joyero: elegir el anillo que selló la carta. La impronta (cartas 27 y 29) es el sello en espejo; hay anillos trampa.
import { openGame } from './ui.js';

const D = /*DATOS*/{"orden": ["d", "b", "f", "a", "c", "e"], "solucion": "a"}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 28 — El joyero de anillos', instr: 'Elegid el anillo que selló la carta de Lucrecia y pulsad «Sellar».', ...opts });
  const style = document.createElement('style');
  style.textContent = `
    .pom-joyero{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;max-width:300px;margin:6px auto;padding:12px;border-radius:12px;background:#7a1a1a;border:4px solid #c8a050}
    .pom-anillo{aspect-ratio:1;border:3px solid transparent;border-radius:50%;background:center / 96% no-repeat;cursor:pointer;padding:0}
    .pom-anillo.sel{border-color:#fff;box-shadow:0 0 14px #ffd27a}`;
  ui.body.appendChild(style);
  const j = document.createElement('div'); j.className = 'pom-joyero'; ui.body.appendChild(j);
  let elegido = null, resuelto = false;
  D.orden.forEach((id, k) => {
    const b = document.createElement('button'); b.type = 'button'; b.className = 'pom-anillo'; b.dataset.a = id;
    b.style.backgroundImage = "url('./img/ui/anillo-" + id + ".png')"; b.setAttribute('aria-label', 'Anillo ' + (k + 1));
    b.addEventListener('click', () => { if (resuelto) return; elegido = id; j.querySelectorAll('.pom-anillo').forEach(x => x.classList.toggle('sel', x === b)); ui.say(''); });
    j.appendChild(b);
  });
  ui.button('Sellar', 'primary', () => {
    if (resuelto) return;
    if (!elegido) { ui.say('Elegid un anillo.', 'bad'); return; }
    if (elegido === D.solucion) { resuelto = true; ui.say('El anillo encaja en la impronta como una llave. Es el de Lucrecia: la carta es auténtica. Coged la carta 30.', 'ok'); }
    else ui.say('Ese anillo no deja esa marca. Pensad en lo que hace un sello al apretarlo contra el lacre (cartas 27 y 29).', 'bad');
  });
  return { close: ui.close };
}
