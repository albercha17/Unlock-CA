// Carta 72 — El juego de memoria de Leo: dieciséis cartas boca abajo (A1 a D4) con ocho dibujos, cada uno dos veces. Los doce intentos de Leo (cartas 75 y 79)
// enseñan quince posiciones; hay que formar las ocho parejas tocando las dos cartas de cada una (instancias_juguetes.py, MEMORIA).
import { openGame } from './ui.js';
import { estilo } from './comun.js';

const D = /*DATOS*/{"cartas": ["tambor", "cohete", "coche", "osito", "pelota", "pelota", "barco", "cometa", "patito", "cometa", "tambor", "barco", "coche", "osito", "cohete", "patito"], "solucion": [[0, 10], [1, 14], [2, 12], [3, 13], [4, 5], [6, 11], [7, 9], [8, 15]], "imagenes": ["patito", "pelota", "tambor", "cohete", "coche", "osito", "barco", "cometa"]}/*FIN*/;
const ET = i => 'ABCD'[i % 4] + (Math.floor(i / 4) + 1);
const COLORES = ['#d63430', '#2c68c4', '#3aa054', '#f6c42a', '#8a4cc4', '#ee8028', '#1ea8a0', '#e0609a'];

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 72 — La memoria de Leo', instr: 'Formad las ocho parejas: tocad una carta y luego su pareja. Los doce intentos de Leo están en las cartas 75 y 79.', ...opts });
  estilo('ju-mem', '.mem-t{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;width:min(86vw,300px);margin:8px auto}.mem-t button{aspect-ratio:3/4;border-radius:10px;border:3px solid #1a2a5a;background:#2c68c4;color:#fff;font:800 1rem system-ui,sans-serif;cursor:pointer;padding:0}.mem-t button.sel{outline:4px solid #fff}.mem-t button.par{border-color:#fff;color:#1a2a5a}');
  const parDe = Array(16).fill(-1);          // número de pareja formada, o -1
  const pares = [];
  let sel = null, resuelto = false;
  const t = document.createElement('div');
  t.className = 'mem-t';
  const bs = Array.from({ length: 16 }, (_, i) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.dataset.i = String(i);
    b.dataset.p = ET(i);
    b.textContent = ET(i);
    b.setAttribute('aria-label', 'Carta ' + ET(i));
    b.addEventListener('click', () => {
      if (resuelto) return;
      if (parDe[i] >= 0) { ui.say('Esa carta ya está emparejada: tocad «Deshacer parejas» para empezar de nuevo.', 'bad'); return; }
      if (sel === null) sel = i;
      else if (sel === i) sel = null;
      else { pares.push([sel, i]); parDe[sel] = parDe[i] = pares.length - 1; sel = null; ui.say(''); }
      pintar();
    });
    t.appendChild(b);
    return b;
  });
  ui.body.appendChild(t);
  function pintar() {
    bs.forEach((b, i) => {
      b.classList.toggle('sel', sel === i);
      b.classList.toggle('par', parDe[i] >= 0);
      b.style.background = parDe[i] >= 0 ? COLORES[parDe[i] % 8] : '';
    });
  }
  ui.button('Comprobar las parejas', 'primary', () => {
    if (resuelto) return;
    if (pares.length < 8) { ui.say('Faltan parejas: son ocho.', 'bad'); return; }
    const clave = ps => ps.map(p => p.slice().sort((a, b) => a - b).join('-')).sort().join('|');
    if (clave(pares) !== clave(D.solucion)) { ui.say('Alguna pareja no es la buena: repasad los intentos de Leo.', 'bad'); return; }
    resuelto = true;
    ui.say('¡Las ocho parejas! Al darse la vuelta, las cartas dejan ver el fondo del cajoncito: la cajita de música de Leo. Coged la carta 82.', 'ok');
  });
  ui.button('Deshacer parejas', '', () => { if (!resuelto) { parDe.fill(-1); pares.length = 0; sel = null; ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
