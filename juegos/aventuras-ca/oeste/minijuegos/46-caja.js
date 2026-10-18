// Carta 46 — La caja fuerte: rueda de combinación. Derecha hasta el primer número, izquierda hasta el segundo y derecha hasta el tercero.
// Los números son las rayitas del mapa (cartas 40 a 43 juntas), en el orden del camino desde la hoguera.
// Solución: 14 (derecha), 7 (izquierda), 29 (derecha).
import { openGame } from './ui.js';

const COMBINACION = [14, 7, 29];
const SENTIDOS = ['der', 'izq', 'der'];
const MARCAS = 40;

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 46 — La caja fuerte',
    instr: 'Gira la rueda: derecha hasta el primer número, izquierda hasta el segundo y derecha hasta el tercero. Pulsa Fijar en cada número.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .oes-caja{display:flex;flex-direction:column;align-items:center;gap:10px;margin:6px 0 12px}
    .oes-rueda-c{position:relative;width:170px;height:170px;border-radius:50%;border:6px solid #b8742a;background:radial-gradient(circle,#f5e6c4 0 38%,#caa268 39% 100%);box-shadow:0 0 0 4px #4a2c10,inset 0 0 16px rgba(0,0,0,.45);transition:transform .25s}
    .oes-rueda-c i{position:absolute;left:50%;top:6px;width:4px;height:16px;margin-left:-2px;background:#4a2c10;transform-origin:50% 79px}
    .oes-puntero{position:absolute;left:50%;top:-14px;margin-left:-9px;width:0;height:0;border-left:9px solid transparent;border-right:9px solid transparent;border-top:16px solid #c0392b}
    .oes-num{font:800 2.4rem Georgia,serif;color:#fff2d6;text-shadow:0 2px 0 #2a1404}
    .oes-estado{font:600 .85rem system-ui,sans-serif;color:#f5d48a}
    .oes-giros{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;max-width:340px;margin:0 auto 10px}
    .oes-giro{padding:10px 4px;border-radius:8px;border:2px solid #f0b860;background:linear-gradient(180deg,#c88a3a,#7a4a1a);color:#fff2d6;font:800 .9rem system-ui,sans-serif;cursor:pointer;box-shadow:0 3px 0 #2a1608}
    .oes-giro:active{transform:translateY(2px);box-shadow:0 1px 0 #2a1608}
  `;
  ui.body.appendChild(style);

  const caja = document.createElement('div');
  caja.className = 'oes-caja';
  const giros = document.createElement('div');
  giros.className = 'oes-giros';
  ui.body.appendChild(caja);
  ui.body.appendChild(giros);

  let pos = 0;
  let sentido = null;                    // último sentido en que se ha girado
  let paso = 0;                          // números ya fijados
  let resuelto = false;

  function pintar() {
    caja.innerHTML = '';
    const rueda = document.createElement('div');
    rueda.className = 'oes-rueda-c';
    rueda.style.transform = 'rotate(' + (-pos * 360 / MARCAS) + 'deg)';
    for (let k = 0; k < MARCAS; k++) {
      const m = document.createElement('i');
      m.style.transform = 'rotate(' + (k * 360 / MARCAS) + 'deg)';
      if (k % 5 === 0) m.style.height = '24px';
      rueda.appendChild(m);
    }
    const p = document.createElement('div');
    p.className = 'oes-puntero';
    const n = document.createElement('div');
    n.className = 'oes-num';
    n.dataset.pos = String(pos);
    n.textContent = String(pos);
    const e = document.createElement('div');
    e.className = 'oes-estado';
    e.textContent = 'Números fijados: ' + paso + ' de 3';
    const marco = document.createElement('div');
    marco.style.position = 'relative';
    marco.appendChild(p);
    marco.appendChild(rueda);
    caja.appendChild(marco);
    caja.appendChild(n);
    caja.appendChild(e);
  }

  [['izq5', '← 5', -5], ['izq1', '← 1', -1], ['der1', '1 →', 1], ['der5', '5 →', 5]].forEach(([k, txt, d]) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'oes-giro';
    b.dataset.d = k;
    b.textContent = txt;
    b.setAttribute('aria-label', d < 0 ? 'Girar ' + (-d) + ' a la izquierda' : 'Girar ' + d + ' a la derecha');
    b.addEventListener('click', () => {
      if (resuelto) return;
      pos = ((pos + d) % MARCAS + MARCAS) % MARCAS;
      sentido = d < 0 ? 'izq' : 'der';
      ui.say('');
      pintar();
    });
    giros.appendChild(b);
  });

  ui.button('Fijar', 'primary', () => {
    if (resuelto) return;
    if (pos === COMBINACION[paso] && sentido === SENTIDOS[paso]) {
      paso++;
      if (paso === COMBINACION.length) {
        resuelto = true;
        pintar();
        ui.say('¡Clic, clic, CLIC! La caja fuerte se abre y la roca se desliza: detrás está la entrada de la vieja mina. Coged la carta 44.', 'ok');
      } else {
        pintar();
        ui.say('Clic. Ese número encaja; seguid con el siguiente.', '');
      }
    } else {
      paso = 0; pos = 0; sentido = null;
      pintar();
      ui.say('La rueda chasquea y vuelve a cero: ese no era el número o no veníais girando en el sentido correcto. Contad las rayitas del mapa, en grupos de cinco, desde la hoguera, y recordad: derecha, izquierda, derecha.', 'bad');
    }
  });

  pintar();
  return { close: ui.close };
}
