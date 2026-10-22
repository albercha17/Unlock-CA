// Carta 51 — La tabla de récords: ordenar de menos a más puntos las ocho entradas intercambiando solo vecinas, con un máximo de cambios. Las entradas son
// bloques de colores sin puntos; los puntos de cada color, en la tabla de las cartas 61 y 63 (dos mitades); la regla, en la carta 26.
// instancias_arcade.py, RANKING (límite = número mínimo de cambios).
import { openGame } from './ui.js';
import { estilo, NEON } from './maquina.js';

const D = /*DATOS*/{"puntos": [790, 620, 110, 410, 370, 230, 580, 830], "limite": 14}/*FIN*/;
const NOMBRES = ['rojo', 'cian', 'verde', 'amarillo', 'rosa', 'naranja', 'violeta', 'blanco'];

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 51 — La tabla de récords', instr: 'Ordenad las entradas de menos a más puntos, de arriba abajo. Solo podéis subir una entrada un puesto (la baja la de encima). Los puntos de cada color, en la tabla de las cartas 61 y 63; la regla, en la carta 26.', ...opts });
  estilo('ar-ran', `
    .ran-lista{display:flex;flex-direction:column;gap:5px;max-width:320px;margin:8px auto}
    .ran-fila{display:flex;align-items:center;gap:10px;border:2px solid #5a3f9a;border-radius:10px;background:#12082a;padding:5px 8px}
    .ran-blq{flex:1;height:34px;border-radius:6px;border:3px solid #f0f0ff;display:flex;align-items:center;padding-left:10px;font:700 .8rem system-ui;color:#10081c}
    .ran-sube{width:46px;height:40px;border-radius:8px;border:2px solid #ff5ad8;background:linear-gradient(180deg,#3a1458,#1c0a30);color:#ffd6f6;font:700 1.1rem system-ui;cursor:pointer}
    .ran-sube:disabled{opacity:.3;cursor:default}
  `);
  let orden = D.puntos.map((_, i) => i);
  let cambios = 0, resuelto = false;
  const lista = document.createElement('div');
  lista.className = 'ran-lista';
  const info = document.createElement('div');
  info.className = 'ar-pie';
  ui.body.append(lista, info);
  function pintar() {
    lista.innerHTML = '';
    orden.forEach((b, pos) => {
      const f = document.createElement('div');
      f.className = 'ran-fila';
      f.dataset.pos = String(pos);
      f.dataset.b = String(b);
      const bq = document.createElement('div');
      bq.className = 'ran-blq';
      bq.style.background = NEON[b];
      bq.textContent = NOMBRES[b];
      const s = document.createElement('button');
      s.type = 'button';
      s.className = 'ran-sube';
      s.textContent = '▲';
      s.disabled = pos === 0;
      s.setAttribute('aria-label', 'Subir el bloque ' + NOMBRES[b]);
      s.addEventListener('click', () => subir(pos));
      f.append(bq, s);
      lista.appendChild(f);
    });
    info.textContent = 'Cambios hechos: ' + cambios + ' de ' + D.limite + ' como máximo.';
    lista.dataset.cambios = String(cambios);
  }
  function subir(pos) {
    if (resuelto || pos < 1) return;
    [orden[pos - 1], orden[pos]] = [orden[pos], orden[pos - 1]];
    cambios++;
    if (orden.every((b, i) => i === 0 || D.puntos[orden[i - 1]] < D.puntos[b])) {
      resuelto = true;
      pintar();
      ui.say('La tabla queda ordenada de menos a más puntos en ' + cambios + ' cambios y la máquina la acepta. Coged la carta 58.', 'ok');
      return;
    }
    if (cambios >= D.limite) {
      ui.say('La máquina pierde la paciencia: ' + D.limite + ' cambios y la tabla sigue desordenada. Se reinicia.', 'bad');
      orden = D.puntos.map((_, i) => i);
      cambios = 0;
    } else ui.say('');
    pintar();
  }
  ui.button('Empezar de nuevo', 'ghost', () => { if (!resuelto) { orden = D.puntos.map((_, i) => i); cambios = 0; ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
