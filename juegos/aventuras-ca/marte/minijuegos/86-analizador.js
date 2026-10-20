// Carta 86 — El analizador de muestras: la cámara de descontaminación solo se abre si se meten en el analizador las muestras limpias
// de la bandeja. La regla no está escrita: se deduce de los ejemplos del cuaderno de la doctora (cartas 87, 89 y 90). Todas las reglas
// compatibles con los ejemplos clasifican igual la bandeja (herramientas/instancias_ampliacion.py).
import { openGame } from './ui.js';

const M = /*DATOS*/{"n": 8, "solucion": [5, 7]}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 86 — El analizador de muestras',
    instr: 'Tocad las muestras de la bandeja que estén limpias, según los ejemplos del cuaderno de la doctora, y pulsad «Analizar».',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .mar-bandeja{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;max-width:330px;margin:8px auto;padding:10px;border-radius:12px;background:#1a2a34;border:3px solid #6ee6f0}
    .mar-muestra{aspect-ratio:8 / 7;border-radius:10px;border:2px solid #3a5866;background:#0c1820 center / 88% no-repeat;cursor:pointer;padding:0;position:relative}
    .mar-muestra span{position:absolute;left:4px;top:2px;color:#9fd;font:700 .7rem system-ui}
    .mar-muestra.sel{border-color:#7be495;box-shadow:0 0 0 3px #7be495}
  `;
  ui.body.appendChild(style);
  const bandeja = document.createElement('div');
  bandeja.className = 'mar-bandeja';
  ui.body.appendChild(bandeja);

  const elegidas = new Set();
  let resuelto = false;
  for (let i = 0; i < M.n; i++) {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'mar-muestra';
    b.dataset.i = String(i);
    b.style.backgroundImage = "url('./img/ui/muestra-" + i + ".png')";
    b.innerHTML = '<span>' + (i + 1) + '</span>';
    b.setAttribute('aria-label', 'Muestra ' + (i + 1));
    b.addEventListener('click', () => {
      if (resuelto) return;
      elegidas.has(i) ? elegidas.delete(i) : elegidas.add(i);
      b.classList.toggle('sel', elegidas.has(i));
      ui.say('');
    });
    bandeja.appendChild(b);
  }

  ui.button('Analizar', 'primary', () => {
    if (resuelto) return;
    const bien = M.solucion.length === elegidas.size && M.solucion.every(i => elegidas.has(i));
    if (bien) {
      resuelto = true;
      ui.say('MUESTRAS LIMPIAS. La cámara de descontaminación sopla un chorro de aire y se abre: al fondo, la sala del reactor. Coged la carta 79.', 'ok');
    } else {
      ui.say('El analizador pita: no son exactamente las muestras limpias. Comparad con los ejemplos de la doctora (cartas 87, 89 y 90): ¿qué tienen en común las limpias?', 'bad');
    }
  });
  return { close: ui.close };
}
