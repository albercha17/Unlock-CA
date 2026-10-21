// Carta 14 — El barro del vado: decir en qué orden cruzaron cinco dinosaurios. En el barro (carta 16) cada huella que pisa a otra pasó
// después; qué huella es de quién, en la guía (carta 18). Orden único (herramientas/instancias_dinosaurios.py, HUELLAS).
import { openGame } from './ui.js';
import { estilo } from './valle.js';

const D = /*DATOS*/{"orden": ["triceratops", "tiranosaurio", "edmontosaurio", "anquilosaurio", "velociraptor"], "encima": [["anquilosaurio", "edmontosaurio"], ["velociraptor", "anquilosaurio"], ["edmontosaurio", "tiranosaurio"], ["tiranosaurio", "triceratops"], ["anquilosaurio", "triceratops"]]}/*FIN*/;
const NOM = { triceratops: 'Triceratops', tiranosaurio: 'Tiranosaurio', anquilosaurio: 'Anquilosaurio', edmontosaurio: 'Edmontosaurio', velociraptor: 'Velociraptor' };

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 14 — El barro del vado', instr: 'Tocad a los cinco dinosaurios en el orden en que cruzaron el vado, del primero al último. Tocad un hueco para devolverlo.', ...opts });
  estilo('dn-huellas', `
    .hue-huecos{display:grid;grid-template-columns:repeat(5,1fr);gap:6px;max-width:340px;margin:6px auto}
    .hue-hueco{min-height:54px;border-radius:10px;border:2px dashed #b5e35b;background:rgba(0,0,0,.25);color:#f2ffd6;font:700 .64rem system-ui;cursor:pointer;padding:4px}
    .hue-hueco b{display:block;font:800 1rem Georgia,serif;color:#b5e35b}`);
  const huecos = document.createElement('div'); huecos.className = 'hue-huecos';
  const chips = document.createElement('div'); chips.className = 'dn-chips';
  ui.body.append(huecos, chips);
  let orden = [], resuelto = false;
  const especies = Object.keys(NOM);
  function pintar() {
    huecos.innerHTML = '';
    for (let i = 0; i < 5; i++) {
      const b = document.createElement('button'); b.type = 'button'; b.className = 'hue-hueco'; b.dataset.i = String(i);
      b.innerHTML = '<b>' + (i + 1) + '.º</b>' + (orden[i] ? NOM[orden[i]] : '');
      b.addEventListener('click', () => { if (!resuelto && orden[i]) { orden.splice(i, 1); ui.say(''); pintar(); } });
      huecos.appendChild(b);
    }
    chips.querySelectorAll('.dn-chip').forEach(c => c.classList.toggle('usado', orden.includes(c.dataset.e)));
    huecos.dataset.orden = orden.join(',');
  }
  especies.forEach(e => {
    const c = document.createElement('button'); c.type = 'button'; c.className = 'dn-chip'; c.dataset.e = e; c.textContent = NOM[e];
    c.addEventListener('click', () => { if (resuelto || orden.includes(e) || orden.length >= 5) return; orden.push(e); ui.say(''); pintar(); });
    chips.appendChild(c);
  });
  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    if (orden.length < 5) { ui.say('Faltan dinosaurios por colocar.', 'bad'); return; }
    if (orden.every((e, i) => e === D.orden[i])) {
      resuelto = true;
      ui.say('¡Eso es! El último en cruzar fue el ' + NOM[D.orden[4]].toLowerCase() + ', y su rastro lleva a un campamento escondido entre los helechos. Coged la carta 24.', 'ok');
    } else ui.say('Así no pudo ser: alguna huella quedaría pisando a otra que pasó después. Mirad otra vez el barro (cartas 16 y 18).', 'bad');
  });
  ui.button('Quitar todos', 'ghost', () => { if (!resuelto) { orden = []; ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
