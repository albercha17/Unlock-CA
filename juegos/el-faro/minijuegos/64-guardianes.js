// Carta 64 — La barraca de los guardianes: cinco literas en fila, cinco nombres y cinco gorros. Las pistas del cuaderno de relevos (cartas 66 y 67) dejan una
// sola ordenación posible (herramientas/instancias_faro.py, guardianes).
import { openGame } from './ui.js';
import { estilo } from './comun.js';

const D = /*DATOS*/{"nombres": ["Elías", "Nora", "Teo", "Irene", "Bruno"], "gorros": ["rojo", "azul", "verde", "amarillo", "blanco"], "solucion": [["Nora", "amarillo"], ["Teo", "verde"], ["Bruno", "azul"], ["Elías", "blanco"], ["Irene", "rojo"]]}/*FIN*/;
const HEX = { rojo: '#d63430', azul: '#2c68c4', verde: '#3aa054', amarillo: '#f6c42a', blanco: '#f4f4ec' };

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 64 — La barraca de los guardianes',
    instr: 'Cinco literas en fila, de izquierda a derecha. Tocad el nombre de cada litera para cambiarlo y el gorro para cambiar su color. Las pistas están en el cuaderno de relevos (cartas 66 y 67).',
    ...opts
  });
  estilo('fa-gua', '.gua-f{display:grid;grid-template-columns:repeat(5,1fr);gap:6px;width:min(94vw,360px);margin:8px auto}.gua-l{border:2px solid #c9a45a;border-radius:10px;padding:6px 2px;background:rgba(0,0,0,.28);text-align:center}.gua-l b{display:block;font:800 .8rem system-ui;color:#ffd27a}.gua-n,.gua-g{display:block;width:100%;margin-top:6px;border:1.5px solid rgba(255,255,255,.3);border-radius:8px;padding:8px 0;font:700 .72rem system-ui;color:#fff;background:rgba(255,255,255,.1);cursor:pointer}.gua-g{height:30px;color:#10202c}');
  const nombre = Array(5).fill(-1), gorro = Array(5).fill(-1);
  let resuelto = false;
  const fila = document.createElement('div');
  fila.className = 'gua-f';
  ui.body.appendChild(fila);
  function pintar() {
    fila.innerHTML = '';
    for (let i = 0; i < 5; i++) {
      const l = document.createElement('div');
      l.className = 'gua-l';
      l.innerHTML = '<b>' + (i + 1) + '</b>';
      const n = document.createElement('button');
      n.type = 'button';
      n.className = 'gua-n';
      n.dataset.n = String(i);
      n.textContent = nombre[i] < 0 ? '—' : D.nombres[nombre[i]];
      n.setAttribute('aria-label', 'Nombre de la litera ' + (i + 1));
      n.addEventListener('click', () => { if (!resuelto) { nombre[i] = (nombre[i] + 2) % (D.nombres.length + 1) - 1; ui.say(''); pintar(); } });
      const g = document.createElement('button');
      g.type = 'button';
      g.className = 'gua-g';
      g.dataset.g = String(i);
      g.style.background = gorro[i] < 0 ? 'rgba(255,255,255,.1)' : HEX[D.gorros[gorro[i]]];
      g.textContent = gorro[i] < 0 ? 'gorro' : '';
      g.setAttribute('aria-label', 'Gorro de la litera ' + (i + 1) + (gorro[i] < 0 ? '' : ': ' + D.gorros[gorro[i]]));
      g.addEventListener('click', () => { if (!resuelto) { gorro[i] = (gorro[i] + 2) % (D.gorros.length + 1) - 1; ui.say(''); pintar(); } });
      l.append(n, g);
      fila.appendChild(l);
    }
  }
  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    if (nombre.includes(-1) || gorro.includes(-1)) { ui.say('Faltan nombres o gorros: cada litera lleva un guardián con su gorro.', 'bad'); return; }
    if (new Set(nombre).size < 5 || new Set(gorro).size < 5) { ui.say('Hay un nombre o un gorro repetido: no se repite ninguno.', 'bad'); return; }
    if (D.solucion.every(([n, g], i) => D.nombres[nombre[i]] === n && D.gorros[gorro[i]] === g)) {
      resuelto = true;
      ui.say('¡Cuadra! Los cinco guardianes están donde deben y del colgador de la barraca cae un bidón de aceite. Coged la carta 62.', 'ok');
    } else {
      ui.say('Algo no cuadra con el cuaderno de relevos (cartas 66 y 67). Repasad pista por pista.', 'bad');
    }
  });
  ui.button('Vaciar', '', () => { if (!resuelto) { nombre.fill(-1); gorro.fill(-1); ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
