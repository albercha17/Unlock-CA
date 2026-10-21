// Carta 51 — El árbol de la doctora: poner cada animal en su rama del árbol de parentesco. El árbol, con sus marcas, está en la carta 26;
// los rasgos de cada animal, dibujados en las fichas (cartas 61 y 63). Solución única (instancias_dinosaurios.py, ARBOL).
import { openGame } from './ui.js';
import { estilo } from './valle.js';

const D = /*DATOS*/{"rasgos": ["patas", "patas rectas bajo el cuerpo", "plumas", "alas"], "animales": {"cocodrilo": ["patas"], "triceratops": ["patas", "patas rectas bajo el cuerpo"], "velociraptor": ["patas", "patas rectas bajo el cuerpo", "plumas"], "ave primitiva": ["patas", "patas rectas bajo el cuerpo", "plumas", "alas"], "pez": []}, "solucion": ["pez", "cocodrilo", "triceratops", "velociraptor", "ave primitiva"]}/*FIN*/;
const NOM = { pez: 'Pez', cocodrilo: 'Cocodrilo', triceratops: 'Tricerátops', velociraptor: 'Velocirraptor', 'ave primitiva': 'Ave primitiva' };

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 51 — El árbol de la doctora', instr: 'La doctora dejó vacías las cinco ramas de su árbol. Elegid un animal y tocad la rama donde va (otra vez para quitarlo).', ...opts });
  estilo('dn-arbol', `
    .arb-ramas{display:grid;grid-template-columns:repeat(5,1fr);gap:6px;max-width:340px;margin:8px auto}
    .arb-rama{min-height:64px;border-radius:10px;border:2px solid #b5e35b;background:rgba(0,0,0,.25);color:#f2ffd6;font:700 .62rem system-ui;cursor:pointer;padding:4px}
    .arb-rama b{display:block;font:800 1.1rem Georgia,serif;color:#b5e35b}`);
  const ramas = document.createElement('div'); ramas.className = 'arb-ramas';
  const chips = document.createElement('div'); chips.className = 'dn-chips';
  ui.body.append(ramas, chips);
  const puesto = [null, null, null, null, null];
  let sel = null, resuelto = false;
  function pintar() {
    ramas.innerHTML = '';
    puesto.forEach((a, i) => {
      const b = document.createElement('button'); b.type = 'button'; b.className = 'arb-rama'; b.dataset.i = String(i);
      b.innerHTML = '<b>' + (i + 1) + '</b>' + (a ? NOM[a] : '');
      b.addEventListener('click', () => {
        if (resuelto) return;
        if (sel) { const j = puesto.indexOf(sel); if (j >= 0) puesto[j] = null; puesto[i] = sel; sel = null; }
        else puesto[i] = null;
        ui.say(''); pintar();
      });
      ramas.appendChild(b);
    });
    chips.querySelectorAll('.dn-chip').forEach(c => { c.classList.toggle('sel', c.dataset.a === sel); c.classList.toggle('usado', puesto.includes(c.dataset.a)); });
    ramas.dataset.puesto = puesto.join(',');
  }
  Object.keys(NOM).forEach(a => {
    const c = document.createElement('button'); c.type = 'button'; c.className = 'dn-chip'; c.dataset.a = a; c.textContent = NOM[a];
    c.addEventListener('click', () => { if (!resuelto) { sel = sel === a ? null : a; pintar(); } });
    chips.appendChild(c);
  });
  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    if (puesto.includes(null)) { ui.say('Quedan ramas vacías.', 'bad'); return; }
    if (puesto.every((a, i) => a === D.solucion[i])) {
      resuelto = true;
      ui.say('El árbol queda completo. Bajo la última rama, la doctora había escrito dónde guarda su corral. Coged la carta 58.', 'ok');
    } else ui.say('Algún animal está en una rama cuyas marcas no tiene, o le falta alguna (cartas 26, 61 y 63).', 'bad');
  });
  pintar();
  return { close: ui.close };
}
