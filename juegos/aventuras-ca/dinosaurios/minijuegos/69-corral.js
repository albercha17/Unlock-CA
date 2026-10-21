// Carta 69 — El corral: meter seis animales en seis cercados sin que nadie quede pared con pared con quien se lo come.
// Quién come a quién: carta 70; el plano, con un animal que ya estaba dentro: carta 71 (la app no lo enseña). Solución única (CORRAL).
import { openGame } from './ui.js';
import { estilo } from './valle.js';

const D = /*DATOS*/{"animales": ["compsognato", "edmontosaurio", "protoceratops", "tiranosaurio", "triceratops", "velociraptor"], "come": [["tiranosaurio", "edmontosaurio"], ["tiranosaurio", "protoceratops"], ["tiranosaurio", "velociraptor"], ["velociraptor", "protoceratops"], ["velociraptor", "compsognato"]], "fijos": {"compsognato": [0, 0]}, "cols": 3, "filas": 2, "solucion": {"compsognato": [0, 0], "edmontosaurio": [2, 0], "protoceratops": [1, 0], "tiranosaurio": [0, 1], "triceratops": [1, 1], "velociraptor": [2, 1]}}/*FIN*/;
const NOM = { compsognato: 'Compsognato', edmontosaurio: 'Edmontosaurio', protoceratops: 'Protoceratops', tiranosaurio: 'Tiranosaurio', triceratops: 'Tricerátops', velociraptor: 'Velocirraptor' };

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 69 — El corral', instr: 'Llega la noche y hay que encerrar a los animales de la doctora. Elegid un animal y tocad su cercado. Pulsad «Cerrar el corral» cuando estén todos.', ...opts });
  estilo('dn-corral', `
    .cor-plano{display:grid;gap:5px;max-width:330px;margin:8px auto;padding:6px;border-radius:10px;background:#5a3a1e}
    .cor-cerco{min-height:74px;border-radius:6px;border:0;background:#c8a86a;color:#2a1a08;font:800 .7rem system-ui;cursor:pointer}`);
  const plano = document.createElement('div'); plano.className = 'cor-plano';
  plano.style.gridTemplateColumns = 'repeat(' + D.cols + ',1fr)';
  const chips = document.createElement('div'); chips.className = 'dn-chips';
  ui.body.append(plano, chips);
  const pos = {};
  let sel = null, resuelto = false;
  const quien = (x, y) => Object.keys(pos).find(a => pos[a][0] === x && pos[a][1] === y);
  function pintar() {
    plano.innerHTML = '';
    for (let y = 0; y < D.filas; y++) for (let x = 0; x < D.cols; x++) {
      const b = document.createElement('button'); b.type = 'button'; b.className = 'cor-cerco'; b.dataset.x = String(x); b.dataset.y = String(y);
      b.textContent = quien(x, y) ? NOM[quien(x, y)] : '';
      b.addEventListener('click', () => {
        if (resuelto) return;
        const q = quien(x, y);
        if (sel) { if (q) delete pos[q]; pos[sel] = [x, y]; sel = null; }
        else if (q) delete pos[q];
        ui.say(''); pintar();
      });
      plano.appendChild(b);
    }
    chips.querySelectorAll('.dn-chip').forEach(c => { c.classList.toggle('sel', c.dataset.a === sel); c.classList.toggle('usado', !!pos[c.dataset.a]); });
  }
  D.animales.forEach(a => {
    const c = document.createElement('button'); c.type = 'button'; c.className = 'dn-chip'; c.dataset.a = a; c.textContent = NOM[a];
    c.addEventListener('click', () => { if (!resuelto) { sel = sel === a ? null : a; pintar(); } });
    chips.appendChild(c);
  });
  ui.button('Cerrar el corral', 'primary', () => {
    if (resuelto) return;
    if (Object.keys(pos).length < D.animales.length) { ui.say('Faltan animales por encerrar.', 'bad'); return; }
    const pegados = ([a, b]) => Math.abs(pos[a][0] - pos[b][0]) + Math.abs(pos[a][1] - pos[b][1]) === 1;
    const mal = D.come.find(pegados);
    if (mal) { ui.say('A medianoche se oyen gruñidos: el ' + NOM[mal[0]].toLowerCase() + ' tiene al ' + NOM[mal[1]].toLowerCase() + ' pared con pared (carta 70). Volved a repartirlos.', 'bad'); return; }
    if (D.animales.every(a => pos[a][0] === D.solucion[a][0] && pos[a][1] === D.solucion[a][1])) {
      resuelto = true;
      ui.say('Noche tranquila en el corral. Al amanecer, el pterosaurio de la doctora se posa en la cerca y os mira. Coged la carta 80.', 'ok');
    } else ui.say('Nadie se come a nadie, pero el animal que ya estaba dentro no estaba ahí (carta 71).', 'bad');
  });
  pintar();
  return { close: ui.close };
}
