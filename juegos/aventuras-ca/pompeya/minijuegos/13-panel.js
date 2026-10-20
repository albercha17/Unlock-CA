// Carta 13 — El panel del despacho: tocar, en orden, las cuatro figuras que el único camino blanco del mosaico del atrio (cartas 14 a 17)
// encuentra del sol a la puerta (acertijo de Lucio, carta 18). Datos de herramientas/instancias_pompeya.py.
import { openGame } from './ui.js';

const D = /*DATOS*/{"todas": ["delfin", "anfora", "laurel", "lechuza", "racimo", "concha", "lucerna", "escudo"], "solucion": ["anfora", "escudo", "laurel", "lechuza"]}/*FIN*/;
const NOMBRE = { delfin: 'delfín', anfora: 'ánfora', laurel: 'laurel', lechuza: 'lechuza', racimo: 'racimo', concha: 'concha', lucerna: 'lucerna', escudo: 'escudo' };

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 13 — El panel del despacho', instr: 'Tocad cuatro figuras en orden para ponerlas en los huecos del panel y pulsad «Empujar la puerta».', ...opts });
  const style = document.createElement('style');
  style.textContent = `
    .pom-huecos{display:flex;gap:8px;justify-content:center;margin:6px 0 12px}
    .pom-hueco{width:62px;height:62px;border-radius:50%;border:3px dashed #c8a050;background:#2a1a10 center / 90% no-repeat}
    .pom-figs{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;max-width:300px;margin:0 auto}
    .pom-fig{aspect-ratio:1;border-radius:50%;border:3px solid #c8a050;background:#1e3c6e center / 92% no-repeat;cursor:pointer;padding:0}
    .pom-fig:disabled{opacity:.3}`;
  ui.body.appendChild(style);
  const huecos = document.createElement('div'); huecos.className = 'pom-huecos';
  const figs = document.createElement('div'); figs.className = 'pom-figs';
  ui.body.append(huecos, figs);
  let puestas = [], resuelto = false;
  function pintar() {
    huecos.innerHTML = '';
    for (let i = 0; i < 4; i++) {
      const h = document.createElement('div'); h.className = 'pom-hueco';
      if (puestas[i]) h.style.backgroundImage = "url('./img/ui/fig-" + puestas[i] + ".png')";
      huecos.appendChild(h);
    }
    figs.innerHTML = '';
    D.todas.forEach(f => {
      const b = document.createElement('button'); b.type = 'button'; b.className = 'pom-fig'; b.dataset.f = f;
      b.style.backgroundImage = "url('./img/ui/fig-" + f + ".png')"; b.setAttribute('aria-label', NOMBRE[f]);
      b.disabled = puestas.includes(f) || puestas.length >= 4;
      b.addEventListener('click', () => { if (!resuelto) { puestas.push(f); ui.say(''); pintar(); } });
      figs.appendChild(b);
    });
  }
  ui.button('Empujar la puerta', 'primary', () => {
    if (resuelto) return;
    if (puestas.length < 4) { ui.say('Faltan figuras: el panel tiene cuatro huecos.', 'bad'); return; }
    if (puestas.every((f, i) => f === D.solucion[i])) { resuelto = true; ui.say('Las figuras encajan con un chasquido de bronce y la puerta del despacho se abre. Coged la carta 19.', 'ok'); }
    else ui.say('La puerta no cede. Lucio era muy suyo con su camino (cartas 14 a 18).', 'bad');
  });
  ui.button('Quitar las figuras', '', () => { if (!resuelto) { puestas = []; ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
