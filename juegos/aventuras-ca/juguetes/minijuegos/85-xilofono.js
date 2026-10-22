// Carta 85 — La nana: el xilófono de la cajita de música tiene siete barras de colores. La nana son cinco notas, las que dejaron cinco puzles, en el orden de los
// dibujos de la carta 86; la carta 87 dice de qué color es cada nota (instancias_juguetes.py, NANA). En la app las barras solo tienen color.
import { openGame } from './ui.js';
import { estilo } from './comun.js';

const D = /*DATOS*/{"melodia": ["MI", "SOL", "DO", "RE", "LA"], "colores": {"DO": "rojo", "RE": "naranja", "MI": "amarillo", "FA": "verde", "SOL": "azul", "LA": "añil", "SI": "violeta"}}/*FIN*/;
const HEX = { rojo: '#d63430', naranja: '#ee8028', amarillo: '#f6c42a', verde: '#3aa054', azul: '#2c68c4', 'añil': '#46409c', violeta: '#8a4cc4' };

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 85 — La nana', instr: 'Tocad las cinco notas de la nana, en orden, en las barras del xilófono. Las notas las dejaron cinco puzles; el orden está en la carta 86 y los colores de las notas, en la 87.', ...opts });
  estilo('ju-xil', '.xil-b{display:flex;gap:6px;justify-content:center;align-items:flex-start;margin:10px 0}.xil-b button{width:40px;border:3px solid #1a2a5a;border-radius:8px;padding:0;cursor:pointer}.xil-s{display:flex;gap:6px;justify-content:center;min-height:34px;margin:6px 0}.xil-s i{width:30px;height:30px;border-radius:50%;border:3px solid #1a2a5a;display:inline-block}');
  const colores = Object.values(D.colores);
  const tocadas = [];
  let resuelto = false;
  const barras = document.createElement('div');
  barras.className = 'xil-b';
  colores.forEach((c, i) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.dataset.c = c;
    b.style.background = HEX[c];
    b.style.height = (160 - i * 14) + 'px';
    b.setAttribute('aria-label', 'Barra ' + c);
    b.addEventListener('click', () => { if (resuelto) return; tocadas.push(c); ui.say(''); pintar(); });
    barras.appendChild(b);
  });
  const sonadas = document.createElement('div');
  sonadas.className = 'xil-s';
  ui.body.append(barras, sonadas);
  function pintar() {
    sonadas.innerHTML = tocadas.map(c => '<i style="background:' + HEX[c] + '"></i>').join('');
  }
  ui.button('Tocar la nana', 'primary', () => {
    if (resuelto) return;
    if (tocadas.length !== D.melodia.length) { ui.say('La nana tiene cinco notas.', 'bad'); return; }
    if (tocadas.some((c, i) => c !== D.colores[D.melodia[i]])) { ui.say('Suena una nana rara y el oso de peluche bosteza con cara de disgusto: alguna nota no es la suya.', 'bad'); return; }
    resuelto = true;
    ui.say('La nana suena entera, suave como una brisa, y Leo se da la vuelta y sigue durmiendo. El anillo del Cronoportal empieza a brillar. Coged la carta 99.', 'ok');
  });
  ui.button('Borrar la última', '', () => { if (!resuelto) { tocadas.pop(); ui.say(''); pintar(); } });
  ui.button('Empezar de nuevo', '', () => { if (!resuelto) { tocadas.length = 0; ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
