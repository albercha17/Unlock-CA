// Carta 69 — El desactivador: cuatro cargas con seis cables de colores cada una; el manual del desactivador (cartas 70 y 71) dice qué cable cortar según
// los colores. Hay que elegir un cable por carga (instancias_espia.py, CABLES). Pulsaciones del teléfono rojo: D.pulsa.
import { openGame } from './ui.js';
import { estilo, COLORES } from './comun.js';

const D = /*DATOS*/{"cargas": [{"cables": ["rojo", "negro", "azul", "negro", "amarillo", "azul"], "regla": 2, "corta": 0}, {"cables": ["negro", "rojo", "rojo", "amarillo", "rojo", "amarillo"], "regla": 3, "corta": 4}, {"cables": ["azul", "blanco", "rojo", "azul", "azul", "blanco"], "regla": 1, "corta": 4}, {"cables": ["rojo", "rojo", "blanco", "rojo", "negro", "blanco"], "regla": 5, "corta": 3}], "pulsa": "7"}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 69 — El desactivador', instr: 'Elegid un cable de cada carga para cortarlo. El manual del desactivador está en las cartas 70 y 71.', ...opts });
  estilo('es-cab', `
    .cab-carga{margin:8px auto;max-width:340px;padding:8px;border-radius:8px;background:#0a2a36;border:2px solid #ff6fa8}
    .cab-carga b{display:block;color:#7fe8f0;font:700 .85rem system-ui,Arial,sans-serif;margin-bottom:6px}
    .cab-fila{display:flex;gap:6px;justify-content:space-between}
    .cab-w{flex:1;min-height:44px;border-radius:6px;border:3px solid #04141a;cursor:pointer;padding:0}
    .cab-w.sel{outline:4px solid #ffe08a;border-color:#fff}`);
  const elegido = D.cargas.map(() => -1);
  let resuelto = false;
  const filas = D.cargas.map((c, k) => {
    const caja = document.createElement('div');
    caja.className = 'cab-carga';
    caja.dataset.k = String(k);
    const t = document.createElement('b');
    t.textContent = 'Carga ' + (k + 1);
    const fila = document.createElement('div');
    fila.className = 'cab-fila';
    const bs = c.cables.map((col, i) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'cab-w';
      b.dataset.k = String(k);
      b.dataset.i = String(i);
      b.dataset.color = col;
      b.style.background = COLORES[col];
      b.setAttribute('aria-label', 'Carga ' + (k + 1) + ', cable ' + (i + 1) + ', ' + col);
      b.addEventListener('click', () => { if (resuelto) return; elegido[k] = i; ui.say(''); pintar(); });
      fila.appendChild(b);
      return b;
    });
    caja.append(t, fila);
    ui.body.appendChild(caja);
    return bs;
  });
  function pintar() { filas.forEach((bs, k) => bs.forEach((b, i) => b.classList.toggle('sel', elegido[k] === i))); }
  ui.button('Cortar los cables', 'primary', () => {
    if (resuelto) return;
    const sin = elegido.findIndex(e => e < 0);
    if (sin >= 0) { ui.say('Falta elegir el cable de la carga ' + (sin + 1) + '.', 'bad'); return; }
    const mal = D.cargas.findIndex((c, k) => elegido[k] !== c.corta);
    if (mal >= 0) { ui.say('¡Pi, pi, pi! La carga ' + (mal + 1) + ' no se desactiva: el cable cortado no es el que manda el manual. Se reinician las cuatro.', 'bad'); elegido.fill(-1); pintar(); return; }
    resuelto = true;
    ui.say('Las cuatro cargas quedan mudas. Teléfono rojo: pulsad ' + D.pulsa + '. Coged la carta 80.', 'ok');
  });
  ui.button('Elegir de nuevo', 'ghost', () => { if (!resuelto) { elegido.fill(-1); ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
