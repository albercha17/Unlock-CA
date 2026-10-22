// Carta 40 — Los cuervos mensajeros (problema del viajante): el cuervo sale de Piedra Negra, visita las otras cinco fortalezas una vez y vuelve.
// Hay que elegir la ruta que menos leguas gasta. Dónde está cada fortaleza, en el mapa (carta 41); las leguas entre cada dos, en la tabla (carta 43);
// el acertijo, en la 45. La app no enseña las leguas. Solución única (instancias_trono.py, CUERVOS). Cifra de la profecía: 7.
import { openGame } from './ui.js';
import { estilo } from './reino.js';

const D = /*DATOS*/{"fortalezas": ["Piedra Negra", "Invernalia", "Altojardín", "Roca Casterly", "Dorne", "Aguasdulces"], "solucion": [0, 2, 4, 1, 5, 3], "minimo": 138, "distancias": {"0,1": 46, "0,2": 30, "0,3": 20, "0,4": 47, "0,5": 36, "1,2": 24, "1,3": 34, "1,4": 26, "1,5": 28, "2,3": 30, "2,4": 18, "2,5": 36, "3,4": 47, "3,5": 16, "4,5": 49}, "dato": 7}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 40 — Los cuervos mensajeros', instr: 'El cuervo sale de Piedra Negra (1). Tocad las otras fortalezas en el orden en que las visita; al final vuelve solo a casa. Mapa y leguas, en las cartas 41, 43 y 45.', ...opts });
  estilo('tr-cuer', `.cue-fort{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;max-width:320px;margin:12px auto}.cue-f{padding:10px 4px;border-radius:12px;border:3px solid #6d8aa6;background:#2c3a4a;color:#e6f1fb;font:700 .75rem system-ui;cursor:pointer;line-height:1.2}.cue-f b{display:block;font:800 1.3rem Georgia,serif;color:#8fc7ee}.cue-f.on{background:#3a5a78;border-color:#8fc7ee}.cue-f.base{border-style:dashed}.cue-ruta{text-align:center;color:#e6f1fb;font:700 .85rem system-ui;margin:6px 0;min-height:1.3em}`);
  const g = document.createElement('div'); g.className = 'cue-fort';
  const rt = document.createElement('div'); rt.className = 'cue-ruta';
  ui.body.append(g, rt);
  const ruta = [0];
  let resuelto = false;
  function pintar() {
    g.querySelectorAll('.cue-f').forEach(b => b.classList.toggle('on', ruta.includes(Number(b.dataset.i))));
    rt.textContent = ruta.map(i => i + 1).join(' → ');
    g.dataset.ruta = ruta.join(',');
  }
  D.fortalezas.forEach((n, i) => {
    const b = document.createElement('button'); b.type = 'button'; b.className = 'cue-f' + (i === 0 ? ' base' : ''); b.dataset.i = String(i);
    b.innerHTML = '<b>' + (i + 1) + '</b>' + n;
    b.addEventListener('click', () => { if (resuelto || i === 0 || ruta.includes(i)) return; ruta.push(i); ui.say(''); pintar(); });
    g.appendChild(b);
  });
  const d = (a, b) => D.distancias[Math.min(a, b) + ',' + Math.max(a, b)];
  ui.button('Enviar el cuervo', 'primary', () => {
    if (resuelto) return;
    if (ruta.length < D.fortalezas.length) { ui.say('Faltan fortalezas por visitar.', 'bad'); return; }
    const total = ruta.concat([0]).reduce((s, v, k, a) => k ? s + d(a[k - 1], v) : 0, 0);
    if (total === D.minimo) {
      resuelto = true;
      ui.say('El cuervo vuela sin desviarse y vuelve con el pico lleno de cartas: es la ruta más corta. Cifra de la profecía: ' + D.dato + '. Coged la carta 30.', 'ok');
    } else ui.say('Todas las fortalezas, pero el cuervo gasta ' + total + ' leguas y el maestre sabe de una ruta más corta (cartas 41, 43 y 45).', 'bad');
  });
  ui.button('Empezar de nuevo', 'ghost', () => { if (!resuelto) { ruta.length = 1; ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
