// Carta 50 — La mesa de ofrendas: 4 x 4 huecos con ofrendas del 1 al 4, sin repetir en filas ni columnas, y cada recinto del plano
// (cartas 38 y 51) suma su número rojo (tipo KenKen). Solución única (herramientas/instancias_ampliacion.py).
import { openGame } from './ui.js';

const O = /*DATOS*/{"solucion": [[2, 4, 3, 1], [4, 1, 2, 3], [3, 2, 1, 4], [1, 3, 4, 2]]}/*FIN*/;
const NOMBRE = ['', 'pan', 'jarra', 'loto', 'incienso'];

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 50 — La mesa de ofrendas',
    instr: 'Tocad un hueco para cambiar su ofrenda (1 pan, 2 jarra, 3 loto, 4 incienso). Sin repetir en filas ni columnas, y cada recinto del plano debe sumar su número rojo.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .egi-mesa{display:grid;grid-template-columns:repeat(4,1fr);gap:4px;width:min(80vw,290px);margin:6px auto;padding:8px;border-radius:8px;background:#6a4a26;border:4px solid #c8a050}
    .egi-hueco{aspect-ratio:1;border:2px solid #3a2410;border-radius:6px;background:#d8c08a;cursor:pointer;font:800 1.5rem Georgia,serif;color:#3a2410;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0}
    .egi-hueco small{font:600 .6rem system-ui,sans-serif}
    .egi-hueco[data-v="0"]{background:#b8a070}
    .egi-mesa.ok{border-color:#7be495}
  `;
  ui.body.appendChild(style);
  const mesa = document.createElement('div');
  mesa.className = 'egi-mesa';
  ui.body.appendChild(mesa);

  const v = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]];
  let resuelto = false;
  function pintar() {
    mesa.innerHTML = '';
    mesa.classList.toggle('ok', resuelto);
    for (let f = 0; f < 4; f++) {
      for (let c = 0; c < 4; c++) {
        const b = document.createElement('button');
        b.type = 'button';
        b.className = 'egi-hueco';
        b.dataset.f = String(f);
        b.dataset.c = String(c);
        b.dataset.v = String(v[f][c]);
        b.innerHTML = v[f][c] ? v[f][c] + '<small>' + NOMBRE[v[f][c]] + '</small>' : '';
        b.setAttribute('aria-label', 'Fila ' + (f + 1) + ', columna ' + (c + 1) + ': ' + (v[f][c] ? NOMBRE[v[f][c]] : 'vacío'));
        b.addEventListener('click', () => { if (!resuelto) { v[f][c] = (v[f][c] + 1) % 5; ui.say(''); pintar(); } });
        mesa.appendChild(b);
      }
    }
  }

  ui.button('Ofrecer', 'primary', () => {
    if (resuelto) return;
    if (v.some(fila => fila.includes(0))) { ui.say('Quedan huecos vacíos en la mesa.', 'bad'); return; }
    const bien = v.every((fila, f) => fila.every((x, c) => x === O.solucion[f][c]));
    if (bien) {
      resuelto = true;
      pintar();
      ui.say('Las ofrendas se hunden en la mesa con un rumor de piedra y se abre un pasadizo. Coged la carta 41.', 'ok');
    } else {
      ui.say('Los dioses no aceptan la ofrenda. Revisad que nada se repita en filas ni columnas y las sumas de los recintos (cartas 38 y 51).', 'bad');
    }
  });
  ui.button('Vaciar', '', () => { if (!resuelto) { v.forEach(f => f.fill(0)); ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
