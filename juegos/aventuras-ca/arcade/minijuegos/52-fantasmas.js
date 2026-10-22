// Carta 52 — Los cuatro fantasmas: averiguar qué fantasma patrulla cada pasillo, a qué velocidad y qué fruta persigue. Las pistas, en las cartas 54 y 55
// (frases) y 59 (el plano de los pasillos). Solución única (instancias_arcade.py, FANTASMAS). Byte de la máquina: el de D.dato.
import { openGame } from './ui.js';
import { estilo } from './maquina.js';

const D = /*DATOS*/{"fantasmas": ["rojo", "rosa", "cian", "naranja"], "velocidades": ["lento", "normal", "rápido", "loco"], "frutas": ["cereza", "fresa", "naranja", "manzana"], "solucion": [{"fantasma": "rojo", "pasillo": 3, "velocidad": "lento", "fruta": "cereza"}, {"fantasma": "rosa", "pasillo": 1, "velocidad": "rápido", "fruta": "naranja"}, {"fantasma": "cian", "pasillo": 2, "velocidad": "loco", "fruta": "manzana"}, {"fantasma": "naranja", "pasillo": 4, "velocidad": "normal", "fruta": "fresa"}], "dato": 9}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 52 — Los cuatro fantasmas', instr: 'En cada pasillo (de izquierda a derecha, 1 a 4) hay un fantasma distinto, con su velocidad y la fruta que persigue. Tocad cada casilla para cambiar de opción. Las pistas están en las cartas 54, 55 y 59.', ...opts });
  estilo('ar-fan', `
    .fan-tab{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;max-width:340px;margin:8px auto}
    .fan-col{border:2px solid #00e2ff;border-radius:10px;background:#12082a;padding:6px 4px;display:flex;flex-direction:column;gap:6px}
    .fan-col h4{margin:0;text-align:center;color:#ffde46;font:700 .8rem system-ui}
    .fan-sel{min-height:44px;border-radius:8px;border:2px solid #ff5ad8;background:#1c0a30;color:#ffd6f6;font:700 .72rem system-ui;cursor:pointer;padding:2px}
    .fan-sel[data-v=""]{color:#7f6aa8}
  `);
  const listas = { f: D.fantasmas, v: D.velocidades, r: D.frutas };
  const rotulo = { f: 'fantasma', v: 'velocidad', r: 'fruta' };
  const val = Array.from({ length: 4 }, () => ({ f: '', v: '', r: '' }));
  let resuelto = false;
  const tab = document.createElement('div');
  tab.className = 'fan-tab';
  const botones = [];
  for (let p = 0; p < 4; p++) {
    const col = document.createElement('div');
    col.className = 'fan-col';
    col.innerHTML = '<h4>Pasillo ' + (p + 1) + '</h4>';
    ['f', 'v', 'r'].forEach(k => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'fan-sel';
      b.dataset.p = String(p + 1);
      b.dataset.k = k;
      b.setAttribute('aria-label', rotulo[k] + ' del pasillo ' + (p + 1));
      b.addEventListener('click', () => {
        if (resuelto) return;
        const l = listas[k];
        const i = l.indexOf(val[p][k]);
        val[p][k] = i + 1 >= l.length ? '' : l[i + 1];
        ui.say('');
        pintar();
      });
      botones.push([b, p, k]);
      col.appendChild(b);
    });
    tab.appendChild(col);
  }
  ui.body.appendChild(tab);
  function pintar() {
    botones.forEach(([b, p, k]) => { b.dataset.v = val[p][k]; b.textContent = val[p][k] || rotulo[k] + ' ?'; });
  }
  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    if (val.some(c => !c.f || !c.v || !c.r)) { ui.say('Falta decidir alguna casilla de la sala.', 'bad'); return; }
    for (const k of ['f', 'v', 'r']) {
      if (new Set(val.map(c => c[k])).size < 4) { ui.say('Hay un ' + rotulo[k] + ' repetido: cada pasillo tiene uno distinto.', 'bad'); return; }
    }
    const ok = D.solucion.every(s => { const c = val[s.pasillo - 1]; return c.f === s.fantasma && c.v === s.velocidad && c.r === s.fruta; });
    if (!ok) { ui.say('Alguna combinación no encaja con las pistas (cartas 54, 55 y 59).', 'bad'); return; }
    resuelto = true;
    ui.say('Cada fantasma queda en su pasillo y la máquina los da por buenos. Byte de la máquina: ' + D.dato + '. Coged la carta 44.', 'ok');
  });
  ui.button('Vaciar', 'ghost', () => { if (!resuelto) { val.forEach(c => { c.f = c.v = c.r = ''; }); ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
