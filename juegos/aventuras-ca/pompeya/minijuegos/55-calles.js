// Carta 55 — La casa de la manzana: tocar, en el plano, la casa donde paró Lucrecia. Los rasgos de las casas están en el plano de la carta 54
// y los grafitos (51, 52 y 53) dejan una sola.
import { openGame } from './ui.js';

const D = /*DATOS*/{"filas": 4, "cols": 5, "solucion": [3, 3]}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 55 — La casa de la manzana', instr: 'El plano está gastado por la lluvia: solo se ven las casas. Tocad la casa donde paró Lucrecia y llamad a la puerta.', ...opts });
  const style = document.createElement('style');
  style.textContent = `
    .pom-manzana{display:grid;gap:6px;max-width:320px;margin:6px auto;padding:10px;border-radius:8px;background:#8a7a5a}
    .pom-casa{aspect-ratio:1;border-radius:4px;border:2px solid #3a2a1a;background:#c8b896;cursor:pointer;padding:0}
    .pom-casa.sel{outline:3px solid #fff;background:#e8d8b0}
    .pom-pc{text-align:center;color:#f6e4b8;font:700 .72rem system-ui;margin:0}`;
  ui.body.appendChild(style);
  const n = document.createElement('p'); n.className = 'pom-pc'; n.textContent = 'NORTE · calle del foro';
  const g = document.createElement('div'); g.className = 'pom-manzana'; g.style.gridTemplateColumns = 'repeat(' + D.cols + ',1fr)';
  const s = document.createElement('p'); s.className = 'pom-pc'; s.textContent = 'SUR · calle del mar';
  ui.body.append(n, g, s);
  let elegida = null, resuelto = false;
  for (let f = 0; f < D.filas; f++) for (let c = 0; c < D.cols; c++) {
    const b = document.createElement('button'); b.type = 'button'; b.className = 'pom-casa'; b.dataset.f = String(f); b.dataset.c = String(c);
    b.setAttribute('aria-label', 'Casa de la fila ' + (f + 1) + ', columna ' + (c + 1));
    b.addEventListener('click', () => { if (resuelto) return; elegida = [f, c]; g.querySelectorAll('.pom-casa').forEach(x => x.classList.toggle('sel', x === b)); ui.say(''); });
    g.appendChild(b);
  }
  ui.button('Llamar a la puerta', 'primary', () => {
    if (resuelto) return;
    if (!elegida) { ui.say('Elegid una casa.', 'bad'); return; }
    if (elegida[0] === D.solucion[0] && elegida[1] === D.solucion[1]) { resuelto = true; ui.say('La puerta está abierta y dentro hay una nota de Lucrecia. Coged la carta 58.', 'ok'); }
    else ui.say('Os abre un vecino asustado que no sabe nada de Lucrecia. Repasad los grafitos (51, 52 y 53) con el plano (54).', 'bad');
  });
  return { close: ui.close };
}
