// Carta 69 — La báscula: nueve barras de oro, una falsa que pesa menos; solo hay dos pesadas (informe del orfebre, carta 70).
// Método: tres contra tres; con el resultado, una contra otra dentro del grupo sospechoso. La barra falsa es la nº 6.
import { openGame } from './ui.js';

const N = 9;
const FALSA = 5;                       // índice (0-based): la barra 6
const PESADAS = 2;

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 69 — La báscula',
    instr: 'Toca una barra para pasarla al platillo izquierdo, otra vez al derecho y otra vez para quitarla. Pesa solo dos veces y señala la falsa.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .oes-balanza{display:flex;justify-content:space-between;gap:10px;margin:4px 0 8px}
    .oes-platillo{flex:1;min-height:64px;padding:8px;border-radius:10px;border:2px dashed #b8742a;background:rgba(40,22,8,.6);color:#f5d48a;font:600 .8rem system-ui,sans-serif;text-align:center}
    .oes-platillo strong{display:block;margin-bottom:4px;font:700 .85rem Georgia,serif}
    .oes-platillo.inclinado{transition:transform .3s}
    .oes-barras{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;max-width:330px;margin:6px auto 8px}
    .oes-barra{padding:12px 4px;border-radius:8px;border:2px solid #7a4a1a;background:linear-gradient(180deg,#ffd964,#d9a82e);color:#3a2204;font:800 .95rem Georgia,serif;cursor:pointer;box-shadow:0 3px 0 #4a2c10}
    .oes-barra.izq{border-color:#2e86de;box-shadow:0 0 0 3px #2e86de}
    .oes-barra.der{border-color:#c0392b;box-shadow:0 0 0 3px #c0392b}
    .oes-estado{text-align:center;color:#f5d48a;font:600 .85rem system-ui,sans-serif;margin:0 0 8px}
    .oes-sospechas{display:grid;grid-template-columns:repeat(5,1fr);gap:5px;max-width:330px;margin:4px auto 8px}
    .oes-sospecha{padding:8px 2px;border-radius:6px;border:2px solid #f0b860;background:linear-gradient(180deg,#8a5a2c,#4a2c14);color:#fff2d6;font:700 .75rem system-ui,sans-serif;cursor:pointer}
    .oes-bloque{max-width:330px;margin:6px auto 0;color:#f5d48a;font:700 .8rem Georgia,serif;text-align:center}
  `;
  ui.body.appendChild(style);

  const balanza = document.createElement('div');
  balanza.className = 'oes-balanza';
  const barras = document.createElement('div');
  barras.className = 'oes-barras';
  const estado = document.createElement('p');
  estado.className = 'oes-estado';
  const sospechas = document.createElement('div');
  sospechas.className = 'oes-sospechas';
  const etiqueta = document.createElement('div');
  etiqueta.className = 'oes-bloque';
  etiqueta.textContent = '¿Cuál es la barra falsa?';
  [balanza, barras, estado, etiqueta, sospechas].forEach(e => ui.body.appendChild(e));

  const lado = new Array(N).fill('');   // '', 'izq', 'der'
  let pesadas = 0;
  let resuelto = false;

  function pintar() {
    ['izq', 'der'].forEach(l => {});
    balanza.innerHTML = ['izq', 'der'].map(l => {
      const ids = lado.map((x, i) => (x === l ? i + 1 : null)).filter(Boolean);
      return '<div class="oes-platillo" data-l="' + l + '"><strong>Platillo ' + (l === 'izq' ? 'izquierdo' : 'derecho') + '</strong>' + (ids.length ? 'Barras ' + ids.join(', ') : 'vacío') + '</div>';
    }).join('');
    barras.innerHTML = '';
    for (let i = 0; i < N; i++) {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'oes-barra' + (lado[i] ? ' ' + lado[i] : '');
      b.dataset.i = String(i);
      b.textContent = 'Barra ' + (i + 1);
      b.setAttribute('aria-label', 'Barra ' + (i + 1) + (lado[i] === 'izq' ? ' en el platillo izquierdo' : lado[i] === 'der' ? ' en el platillo derecho' : ' fuera de la balanza'));
      b.addEventListener('click', () => {
        if (resuelto) return;
        lado[i] = lado[i] === '' ? 'izq' : lado[i] === 'izq' ? 'der' : '';
        ui.say('');
        pintar();
      });
      barras.appendChild(b);
    }
    estado.textContent = 'Pesadas hechas: ' + pesadas + ' de ' + PESADAS;
    sospechas.innerHTML = '';
    for (let i = 0; i < N; i++) {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'oes-sospecha';
      b.dataset.i = String(i);
      b.textContent = String(i + 1);
      b.setAttribute('aria-label', 'La barra falsa es la ' + (i + 1));
      b.addEventListener('click', () => responder(i));
      sospechas.appendChild(b);
    }
  }

  function reiniciar() { lado.fill(''); pesadas = 0; }

  function pesar() {
    if (resuelto) return;
    const izq = lado.map((x, i) => (x === 'izq' ? i : -1)).filter(i => i >= 0);
    const der = lado.map((x, i) => (x === 'der' ? i : -1)).filter(i => i >= 0);
    if (!izq.length || izq.length !== der.length) { ui.say('Poned el mismo número de barras, y al menos una, en cada platillo.', 'bad'); return; }
    if (pesadas >= PESADAS) { ui.say('Ya habéis hecho las dos pesadas que permite el informe del orfebre: señalad la barra falsa o volved a empezar.', 'bad'); return; }
    pesadas++;
    const pi = izq.reduce((s, i) => s + (i === FALSA ? 2 : 3), 0);
    const pd = der.reduce((s, i) => s + (i === FALSA ? 2 : 3), 0);
    const r = pi === pd ? 'La balanza queda equilibrada: pesan igual.' : pi > pd ? 'La balanza se inclina hacia la izquierda: el platillo izquierdo pesa más.' : 'La balanza se inclina hacia la derecha: el platillo derecho pesa más.';
    pintar();
    ui.say(r, '');
  }

  function responder(i) {
    if (resuelto) return;
    if (pesadas < PESADAS) { ui.say('Todavía no habéis pesado lo suficiente para estar seguros: haced las dos pesadas.', 'bad'); return; }
    if (i === FALSA) {
      resuelto = true;
      pintar();
      ui.say('¡Esa es! La barra falsa se parte: es yeso pintado de dorado y dentro brilla el cristal de energía. Coged la carta 82.', 'ok');
    } else {
      reiniciar();
      pintar();
      ui.say('Esa barra es de oro de verdad. Se vuelve a empezar con las pesadas: tres barras contra tres y, con el resultado, una contra otra.', 'bad');
    }
  }

  ui.button('Pesar', 'primary', pesar);
  ui.button('Vaciar platillos', '', () => { if (!resuelto) { lado.fill(''); ui.say(''); pintar(); } });
  ui.button('Volver a empezar', '', () => { if (!resuelto) { reiniciar(); ui.say(''); pintar(); } });

  pintar();
  return { close: ui.close };
}
