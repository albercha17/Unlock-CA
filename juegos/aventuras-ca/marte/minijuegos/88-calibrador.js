// Carta 88 — Calibrador del Cronoportal: amplitud 3 (diario, carta 35) y frecuencia 5 (tomatera, carta 36).
// No hay ninguna indicación de cercanía: solo la forma de la onda del propio calibrador.
import { openGame } from './ui.js';

const AMPLITUD = 3;
const FRECUENCIA = 5;
const FASE = 2;
const NS = 'http://www.w3.org/2000/svg';

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 88 — Calibrador del Cronoportal',
    instr: 'Ajusta la amplitud, la frecuencia y la fase con los datos que habéis reunido y pulsa Calibrar.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .far-osc{background:#04120c;border:2px solid #1f5a3a;border-radius:10px;margin-bottom:10px;box-shadow:inset 0 0 26px rgba(40,255,140,.12)}
    .far-osc polyline{filter:drop-shadow(0 0 4px #7dffb0)}
    .far-ajuste{display:grid;grid-template-columns:auto 1fr auto;gap:8px 10px;align-items:center;text-align:left;margin-bottom:6px;font-size:.9rem}
    .far-ajuste input{width:100%;accent-color:#7dffb0}
    .far-ajuste output{font-family:"IBM Plex Mono",ui-monospace,monospace;font-weight:700;color:#7dffb0;min-width:1.5em;text-align:right}
  `;
  ui.body.appendChild(style);

  const svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('viewBox', '0 0 300 100');
  svg.setAttribute('width', '100%');
  svg.classList.add('far-osc');
  const linea = document.createElementNS(NS, 'polyline');
  linea.setAttribute('fill', 'none');
  linea.setAttribute('stroke', '#7dffb0');
  linea.setAttribute('stroke-width', '2.5');
  const eje = document.createElementNS(NS, 'line');
  eje.setAttribute('x1', 0); eje.setAttribute('x2', 300); eje.setAttribute('y1', 50); eje.setAttribute('y2', 50);
  eje.setAttribute('stroke', '#1f5a3a');
  for (let x = 30; x < 300; x += 30) { const v = document.createElementNS(NS, 'line'); v.setAttribute('x1', x); v.setAttribute('x2', x); v.setAttribute('y1', 0); v.setAttribute('y2', 100); v.setAttribute('stroke', 'rgba(125,255,176,.08)'); svg.appendChild(v); }
  for (let y = 10; y < 100; y += 20) { const h = document.createElementNS(NS, 'line'); h.setAttribute('x1', 0); h.setAttribute('x2', 300); h.setAttribute('y1', y); h.setAttribute('y2', y); h.setAttribute('stroke', 'rgba(125,255,176,.08)'); svg.appendChild(h); }
  svg.append(eje, linea);

  const ajustes = document.createElement('div');
  ajustes.className = 'far-ajuste';
  ajustes.innerHTML =
    '<label for="marAmp">Amplitud</label><input type="range" id="marAmp" min="1" max="6" step="1" value="1"><output id="marAmpV">1</output>' +
    '<label for="marFrec">Frecuencia</label><input type="range" id="marFrec" min="1" max="8" step="1" value="1"><output id="marFrecV">1</output>' +
    '<label for="marFase">Fase</label><input type="range" id="marFase" min="0" max="3" step="1" value="0"><output id="marFaseV">0</output>';
  ui.body.append(svg, ajustes);

  const amp = ajustes.querySelector('#marAmp');
  const frec = ajustes.querySelector('#marFrec');
  const fase = ajustes.querySelector('#marFase');
  let resuelto = false;

  function pintar() {
    const a = Number(amp.value), f = Number(frec.value), ph = Number(fase.value);
    ajustes.querySelector('#marAmpV').textContent = a;
    ajustes.querySelector('#marFrecV').textContent = f;
    ajustes.querySelector('#marFaseV').textContent = ph;
    const pts = [];
    for (let x = 0; x <= 300; x += 2) {
      pts.push(x + ',' + (50 - a * 7 * Math.sin(2 * Math.PI * f * x / 300 + ph * Math.PI / 2)).toFixed(1));
    }
    linea.setAttribute('points', pts.join(' '));
  }
  [amp, frec, fase].forEach(c => c.addEventListener('input', () => { if (!resuelto) { ui.say(''); pintar(); } }));

  ui.button('Calibrar', 'primary', () => {
    if (resuelto) return;
    if (Number(amp.value) === AMPLITUD && Number(frec.value) === FRECUENCIA && Number(fase.value) === FASE) {
      resuelto = true;
      amp.disabled = true;
      frec.disabled = true;
      fase.disabled = true;
      ui.say('¡Señal sincronizada! El Cronoportal está calibrado. Coged la carta 99.', 'ok');
    } else {
      ui.say('SEÑAL INESTABLE. Alguno de los tres valores no es correcto.', 'bad');
    }
  });

  pintar();
  return { close: ui.close };
}
