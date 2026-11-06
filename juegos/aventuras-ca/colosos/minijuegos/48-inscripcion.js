// Carta 48 — La inscripción del viajero: escribir con doce signos una frase en su lengua (objeto, «no», verbo, sujeto y marca de plural).
// Se deduce de las frases traducidas de la piedra partida y de la nota de la doctora (herramientas/instancias_colosos.py, inscripcion).
import { openGame } from './ui.js';
import { estilo, glifoSVG } from './comun.js';

const D = /*DATOS*/{"glifos": [[["l", 0.5, 0.1, 0.5, 0.9], ["c", 0.5, 0.3, 0.18]], [["l", 0.15, 0.85, 0.5, 0.15], ["l", 0.5, 0.15, 0.85, 0.85], ["l", 0.3, 0.55, 0.7, 0.55]], [["c", 0.5, 0.5, 0.32], ["p", 0.5, 0.5]], [["l", 0.15, 0.2, 0.85, 0.2], ["l", 0.5, 0.2, 0.5, 0.85], ["l", 0.25, 0.85, 0.75, 0.85]], [["l", 0.15, 0.15, 0.85, 0.85], ["l", 0.85, 0.15, 0.15, 0.85], ["c", 0.5, 0.5, 0.12]], [["l", 0.2, 0.5, 0.8, 0.5], ["l", 0.8, 0.5, 0.55, 0.25], ["l", 0.8, 0.5, 0.55, 0.75]], [["l", 0.2, 0.2, 0.2, 0.8], ["l", 0.2, 0.8, 0.8, 0.8], ["l", 0.8, 0.8, 0.8, 0.4], ["p", 0.55, 0.45]], [["c", 0.35, 0.5, 0.17], ["c", 0.65, 0.5, 0.17]], [["l", 0.5, 0.1, 0.9, 0.5], ["l", 0.9, 0.5, 0.5, 0.9], ["l", 0.5, 0.9, 0.1, 0.5], ["l", 0.1, 0.5, 0.5, 0.1]], [["l", 0.2, 0.3, 0.8, 0.3], ["l", 0.2, 0.7, 0.8, 0.7], ["p", 0.5, 0.5]], [["l", 0.3, 0.1, 0.3, 0.9], ["l", 0.7, 0.1, 0.7, 0.9], ["l", 0.3, 0.5, 0.7, 0.5]], [["c", 0.5, 0.62, 0.25], ["l", 0.5, 0.1, 0.5, 0.37], ["l", 0.35, 0.2, 0.65, 0.2]]], "forma": {"FLOR": 4, "MURO": 11, "VIAJERO": 10, "CRISTAL": 9, "COLOSO": 8, "BUSCAR": 1, "GUARDAR": 6, "ABRIR": 3, "NO": 0, "PLURAL": 2, "CAMINO": 5, "LUNA": 7}, "objetivo": ["CRISTAL", "NO", "BUSCAR", "COLOSO", "PLURAL"], "marca": "18"}/*FIN*/;

estilo('co-ins', `
  .co-losa{min-height:74px;margin:6px auto;max-width:360px;border-radius:10px;background:linear-gradient(180deg,#8e8a80,#6a665e);
    border:2px solid #3e3a34;display:flex;gap:6px;align-items:center;justify-content:center;flex-wrap:wrap;padding:8px}
  .co-glifos{display:grid;grid-template-columns:repeat(6,1fr);gap:6px;max-width:360px;margin:8px auto}
  .co-glifo{aspect-ratio:1;border-radius:10px;border:1.5px solid #e0a640;background:rgba(255,240,210,.1);display:flex;align-items:center;justify-content:center;cursor:pointer;padding:0}
  .co-glifo:active{transform:scale(.94)}
`);

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 48 — La inscripción del viajero',
    instr: 'Tocad los signos en orden para grabar en la piedra, en la lengua del viajero, la frase que le falta a la doctora.',
    ...opts
  });
  const escritos = [];
  const losa = document.createElement('div');
  losa.className = 'co-losa';
  const teclado = document.createElement('div');
  teclado.className = 'co-glifos';
  D.glifos.forEach((g, i) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'co-glifo';
    b.dataset.g = i;
    b.setAttribute('aria-label', 'Signo ' + (i + 1));
    b.appendChild(glifoSVG(g, 36));
    b.addEventListener('click', () => { if (escritos.length < 8) { escritos.push(i); pintar(); } });
    teclado.appendChild(b);
  });
  ui.body.append(losa, teclado);

  function pintar() {
    losa.innerHTML = '';
    if (!escritos.length) { losa.textContent = '· · ·'; return; }
    escritos.forEach(i => losa.appendChild(glifoSVG(D.glifos[i], 44, '#1e1a16')));
  }

  const objetivo = D.objetivo.map(w => D.forma[w]);
  ui.button('Borrar', 'ghost', () => { escritos.pop(); pintar(); });
  ui.button('Grabar', 'primary', () => {
    if (!escritos.length) { ui.say('La piedra está en blanco.', ''); return; }
    if (escritos.length === objetivo.length && escritos.every((g, k) => g === objetivo[k])) {
      ui.say('La doctora lee la frase en voz alta y se le cae el matraz: «¡Los colosos no buscan el cristal!». Marca de la inscripción: ' + D.marca + '. Coged la carta 36.', 'ok');
      teclado.querySelectorAll('button').forEach(b => { b.disabled = true; });
    } else {
      ui.say('La doctora frunce el ceño: el viajero no lo habría escrito así (mirad las palabras y su orden).', 'bad');
      escritos.length = 0;
      pintar();
    }
  });
  pintar();
  return { close: ui.close };
}
