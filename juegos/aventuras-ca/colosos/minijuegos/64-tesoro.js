// Carta 64 — El tesoro del Coloso Viejo: agrupar dieciséis baratijas (A-P) en cuatro grupos de cuatro. El material y las muescas solo están
// en la carta de las baratijas; las condiciones, en la de cómo ordena. Reparto único (herramientas/instancias_colosos.py, tesoro).
import { openGame } from './ui.js';
import { estilo } from './comun.js';

const D = /*DATOS*/{"objetos": [{"letra": "A", "tipo": "campanita"}, {"letra": "B", "tipo": "campanita"}, {"letra": "C", "tipo": "moneda"}, {"letra": "D", "tipo": "llave"}, {"letra": "E", "tipo": "anillo"}, {"letra": "F", "tipo": "llave"}, {"letra": "G", "tipo": "llave"}, {"letra": "H", "tipo": "anillo"}, {"letra": "I", "tipo": "campanita"}, {"letra": "J", "tipo": "moneda"}, {"letra": "K", "tipo": "llave"}, {"letra": "L", "tipo": "moneda"}, {"letra": "M", "tipo": "moneda"}, {"letra": "N", "tipo": "anillo"}, {"letra": "O", "tipo": "anillo"}, {"letra": "P", "tipo": "campanita"}], "grupos": [[3, 9, 11, 12], [0, 1, 5, 6], [2, 8, 10, 15], [4, 7, 13, 14]]}/*FIN*/;
const EMO = { anillo: '💍', moneda: '🪙', llave: '🗝️', campanita: '🔔' };
const COLORES = ['#3f7a4a', '#2f5a9a', '#8a3a6a', '#9a6a1a'];

estilo('co-tes', `
  .co-tesoro{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;max-width:330px;margin:6px auto}
  .co-bar{aspect-ratio:1;border-radius:10px;border:1.5px solid rgba(224,166,64,.6);background:rgba(255,240,210,.1);color:#fff6e4;cursor:pointer;
    display:flex;flex-direction:column;align-items:center;justify-content:center;font:800 1rem system-ui,sans-serif;padding:0}
  .co-bar .emo{font-size:1.5rem}
  .co-bar.sel{outline:3px solid #ffd27a;background:rgba(255,210,122,.25)}
  .co-bar.hecha{cursor:default;color:#fff}
`);

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 64 — El tesoro del Coloso Viejo',
    instr: 'Elegid cuatro baratijas que vayan juntas y pulsad «Juntar». Hay que hacer los cuatro montones.',
    ...opts
  });
  const sel = new Set();
  const hecho = new Map();     // índice -> número de montón
  const malla = document.createElement('div');
  malla.className = 'co-tesoro';
  const pie = document.createElement('div');
  pie.className = 'co-pie';
  const bots = D.objetos.map((o, i) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'co-bar';
    b.dataset.letra = o.letra;
    b.innerHTML = `<span class="emo">${EMO[o.tipo]}</span><span>${o.letra}</span>`;
    b.setAttribute('aria-label', `${o.letra}: ${o.tipo}`);
    b.addEventListener('click', () => {
      if (hecho.has(i)) return;
      if (sel.has(i)) sel.delete(i); else if (sel.size < 4) sel.add(i);
      pintar();
    });
    malla.appendChild(b);
    return b;
  });
  ui.body.append(malla, pie);

  function pintar() {
    bots.forEach((b, i) => {
      b.classList.toggle('sel', sel.has(i));
      b.classList.toggle('hecha', hecho.has(i));
      b.style.background = hecho.has(i) ? COLORES[hecho.get(i)] : '';
    });
    const montones = new Set(hecho.values()).size;
    pie.textContent = `Montones hechos: ${montones} de 4 · elegidas: ${sel.size}`;
  }

  ui.button('Soltar', 'ghost', () => { sel.clear(); pintar(); });
  ui.button('Juntar', 'primary', () => {
    if (sel.size !== 4) { ui.say('Cada montón tiene exactamente cuatro baratijas.', ''); return; }
    const g = D.grupos.findIndex(gr => gr.every(i => sel.has(i)));
    if (g < 0) {
      ui.say('El Coloso Viejo deshace el montón con un dedo y niega despacio.', 'bad');
      sel.clear();
      pintar();
      return;
    }
    const num = new Set(hecho.values()).size;
    sel.forEach(i => hecho.set(i, num));
    sel.clear();
    if (hecho.size === 16) {
      pintar();
      ui.say('El Coloso Viejo asiente, satisfecho, y de debajo del último montón saca un destello azul: ¡vuestro cristal! Coged la carta 62.', 'ok');
      bots.forEach(b => { b.disabled = true; });
      return;
    }
    ui.say('¡Un montón bien hecho! El Coloso Viejo gruñe contento.', '');
    pintar();
  });
  pintar();
  return { close: ui.close };
}
