// Carta 66 — La huida: marcar, cruce a cruce, la ruta del foro al puerto que llega antes de que la ceniza cierre la puerta. Tiempos en el
// mapa (carta 67); calles cortadas y tiempo límite, en el vigía (carta 75). Una sola ruta llega a tiempo.
import { openGame } from './ui.js';

const D = /*DATOS*/{"calles": [["F", "A", 4], ["F", "B", 6], ["A", "C", 5], ["B", "C", 3], ["A", "D", 7], ["C", "E", 6], ["D", "E", 3], ["B", "G", 9], ["G", "P", 4], ["E", "P", 5], ["D", "P", 9], ["C", "G", 4]], "cortadas": [["C", "E"], ["D", "P"], ["A", "C"]], "limite": 17}/*FIN*/;
const NOM = { F: 'foro', A: 'templo', B: 'termas', C: 'teatro', D: 'mercado', E: 'lupanar', G: 'anfiteatro', P: 'puerto' };
const POS = { F: [12, 26], A: [38, 16], B: [33, 50], C: [62, 40], D: [66, 16], E: [88, 32], G: [60, 72], P: [86, 86] };

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 66 — La huida', instr: 'Salís del foro. Tocad los cruces en el orden en que corréis, hasta el puerto, y pulsad «¡Corred!».', ...opts });
  const style = document.createElement('style');
  style.textContent = `
    .pom-mapa{position:relative;width:min(88vw,320px);aspect-ratio:1;margin:6px auto;border-radius:8px;background:#5a5048}
    .pom-mapa svg{position:absolute;inset:0;width:100%;height:100%}
    .pom-nodo{position:absolute;width:44px;height:44px;margin:-22px;border-radius:50%;border:3px solid #f6e4b8;background:#3a2a1a;color:#f6e4b8;font:700 .55rem system-ui;cursor:pointer;padding:0}
    .pom-nodo.en{background:#c84a2a}`;
  ui.body.appendChild(style);
  const mapa = document.createElement('div'); mapa.className = 'pom-mapa';
  const lin = D.calles.map(([a, b]) => '<line x1="' + POS[a][0] + '" y1="' + POS[a][1] + '" x2="' + POS[b][0] + '" y2="' + POS[b][1] + '" stroke="#a8988a" stroke-width="2.5"/>').join('');
  mapa.innerHTML = '<svg viewBox="0 0 100 100" aria-hidden="true">' + lin + '</svg>';
  ui.body.appendChild(mapa);
  const tramo = (a, b) => D.calles.find(([x, y]) => (x === a && y === b) || (x === b && y === a));
  let ruta = ['F'], resuelto = false;
  function pintar() { mapa.querySelectorAll('.pom-nodo').forEach(b => b.classList.toggle('en', ruta.includes(b.dataset.n))); mapa.dataset.ruta = ruta.join(''); }
  Object.keys(POS).forEach(n => {
    const b = document.createElement('button'); b.type = 'button'; b.className = 'pom-nodo'; b.dataset.n = n; b.textContent = NOM[n];
    b.style.left = POS[n][0] + '%'; b.style.top = POS[n][1] + '%';
    b.addEventListener('click', () => {
      if (resuelto || ruta.includes(n)) return;
      if (!tramo(ruta[ruta.length - 1], n)) { ui.say('No hay calle directa desde ' + NOM[ruta[ruta.length - 1]] + ' hasta ' + NOM[n] + '.', 'bad'); return; }
      ruta.push(n); ui.say(''); pintar();
    });
    mapa.appendChild(b);
  });
  ui.button('¡Corred!', 'primary', () => {
    if (resuelto) return;
    if (ruta[ruta.length - 1] !== 'P') { ui.say('La ruta tiene que acabar en el puerto.', 'bad'); return; }
    const corta = ruta.slice(1).some((n, i) => D.cortadas.some(([a, b]) => (a === ruta[i] && b === n) || (b === ruta[i] && a === n)));
    if (corta) { ui.say('¡Columnas caídas! Esa calle está cortada y tenéis que volver al foro.', 'bad'); ruta = ['F']; pintar(); return; }
    const t = ruta.slice(1).reduce((s, n, i) => s + tramo(ruta[i], n)[2], 0);
    if (t <= D.limite) { resuelto = true; ui.say('Llegáis al puerto tosiendo, justo cuando la ceniza empieza a tapar la puerta. Coged la carta 69.', 'ok'); }
    else { ui.say('Por ahí se tarda demasiado: la ceniza os cierra el paso y tenéis que volver al foro. Sumad bien los tramos (carta 67).', 'bad'); ruta = ['F']; pintar(); }
  });
  ui.button('Volver al foro', '', () => { if (!resuelto) { ruta = ['F']; ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
