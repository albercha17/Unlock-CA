// Carta 85 — La cerradura de la Copa: cinco aros de doce posiciones; cada uno parte de un número que dejó un puzle y gira tantos puestos como flechas
// dibujadas, hacia la derecha las verdes y hacia la izquierda las rojas. Los aros y sus giros, en la carta 86; el dial, en la 87 (instancias_futbol.py, ARO).
import { openGame } from './ui.js';
import { estilo, opcion } from './comun.js';

const D = /*DATOS*/{"orden": ["14", "40", "52", "69", "72"], "final": [10, 9, 9, 5, 3]}/*FIN*/;
const NOMBRES = { '14': 'la tabla', '40': 'la bandera', '52': 'la camiseta', '69': 'las flechas', '72': 'la grada' };

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 85 — La cerradura de la Copa', instr: 'Colocad cada aro en su posición (1 a 12). Los aros y sus giros están en la carta 86 y el dial, en la 87.', ...opts });
  estilo('fu-aro', '.aro-f{max-width:340px;margin:8px auto;padding:6px;border-radius:8px;background:#0e3a18;border:2px solid #f2c230}.aro-f b{display:block;color:#f2c230;font:800 .85rem system-ui,Arial,sans-serif;margin-bottom:4px}.aro-n{display:grid;grid-template-columns:repeat(6,1fr);gap:4px}.aro-n button{min-height:40px;padding:0}');
  const val = D.orden.map(() => null);
  let resuelto = false;
  const filas = D.orden.map((k, i) => {
    const f = document.createElement('div');
    f.className = 'aro-f';
    f.dataset.i = String(i);
    const t = document.createElement('b');
    t.textContent = 'Aro de ' + NOMBRES[k];
    const g = document.createElement('div');
    g.className = 'aro-n';
    const bs = Array.from({ length: 12 }, (_, n) => {
      const b = opcion(String(n + 1), () => { if (resuelto) return; val[i] = n + 1; ui.say(''); pintar(); });
      b.dataset.i = String(i);
      b.dataset.n = String(n + 1);
      b.setAttribute('aria-label', 'Aro de ' + NOMBRES[k] + ', posición ' + (n + 1));
      g.appendChild(b);
      return b;
    });
    f.append(t, g);
    ui.body.appendChild(f);
    return bs;
  });
  function pintar() { filas.forEach((bs, i) => bs.forEach((b, n) => b.classList.toggle('sel', val[i] === n + 1))); }
  ui.button('Abrir la Copa', 'primary', () => {
    if (resuelto) return;
    if (val.some(v => v === null)) { ui.say('Falta colocar algún aro.', 'bad'); return; }
    if (val.some((v, i) => v !== D.final[i])) { ui.say('La cerradura no cede: algún aro no está en su sitio.', 'bad'); return; }
    resuelto = true;
    ui.say('Clac: la cerradura gira y la Copa de cristal se abre por la mitad. Coged la carta 99.', 'ok');
  });
  ui.button('Borrar todo', 'ghost', () => { if (!resuelto) { val.fill(null); ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
