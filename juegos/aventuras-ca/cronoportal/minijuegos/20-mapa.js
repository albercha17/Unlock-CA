// Carta 20 — Calibrar el portal: tocar, en orden, los símbolos de las cuatro casillas de en medio del camino del plano (cartas 19 y 21 juntas).
// Datos de herramientas/instancias_cronoportal.py (mapa). Enseña a juntar las dos mitades de una lámina.
import { openGame } from './ui.js';
import { estilo } from './comun.js';

const D = /*DATOS*/{"simbolos": ["sol", "luna", "estrella", "llave", "reloj", "flor"], "solucion": ["reloj", "luna", "estrella", "sol"], "cifra": 7}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 20 — Calibrar el portal',
    instr: 'Tocad, en el orden en que los pisa el camino del plano, los símbolos de las cuatro casillas de en medio. El primero y el último no cuentan.',
    ...opts
  });
  estilo('cr-map', '.map-s{display:flex;gap:8px;justify-content:center;margin:10px 0}.map-s i{width:52px;height:52px;border-radius:12px;border:2px dashed rgba(255,210,122,.6);background:rgba(0,0,0,.25) center/80% no-repeat;display:block}'
    + '.map-b{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:8px 0}.map-b button{aspect-ratio:1;border-radius:14px;border:2px solid rgba(255,210,122,.7);background:rgba(255,255,255,.08) center/80% no-repeat;cursor:pointer;padding:0}');
  const N = D.solucion.length;
  const puestos = [];
  let resuelto = false;
  const ranuras = document.createElement('div');
  ranuras.className = 'map-s';
  const banco = document.createElement('div');
  banco.className = 'map-b';
  ui.body.append(ranuras, banco);
  for (let i = 0; i < N; i++) { const r = document.createElement('i'); r.dataset.r = String(i); ranuras.appendChild(r); }
  D.simbolos.forEach(s => {
    const b = document.createElement('button');
    b.type = 'button';
    b.dataset.s = s;
    b.style.backgroundImage = "url('./img/ui/sim-" + s + ".png')";
    b.setAttribute('aria-label', s);
    b.addEventListener('click', () => {
      if (resuelto || puestos.length >= N) return;
      puestos.push(s);
      ui.say('');
      pintar();
    });
    banco.appendChild(b);
  });
  function pintar() {
    ranuras.querySelectorAll('i').forEach((r, i) => { r.style.backgroundImage = puestos[i] ? "url('./img/ui/sim-" + puestos[i] + ".png')" : ''; r.style.borderStyle = puestos[i] ? 'solid' : 'dashed'; });
  }
  ui.button('Calibrar', 'primary', () => {
    if (resuelto) return;
    if (puestos.length < N) { ui.say('Faltan símbolos: son ' + N + '.', 'bad'); return; }
    if (puestos.every((s, i) => s === D.solucion[i])) {
      resuelto = true;
      ui.say('¡El anillo del Cronoportal gira y se llena de luz! Cifra del plano: ' + D.cifra + ' (apuntadla). Coged la carta 28.', 'ok');
    } else {
      ui.say('El anillo tiembla y se apaga: ese no es el camino. Seguid de nuevo la línea roja desde la entrada.', 'bad');
    }
  });
  ui.button('Borrar', '', () => { if (!resuelto) { puestos.length = 0; ui.say(''); pintar(); } });
  return { close: ui.close };
}
