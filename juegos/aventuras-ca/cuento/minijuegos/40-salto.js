// Carta 40 — Había una vez... y ahora: el camino de la aldea al castillo en dos épocas. Con exactamente tres saltos al pasado
// (plantar la habichuela, cavar o encender fuego, una acción por casilla) hay que dejar libre el camino en el presente.
// Las reglas de cada acción están en el cuento del Búho (carta 42). Solución única (comprobada en herramientas/instancias_cuento.py):
// fuego en la casilla 3 (zarzas), plantar en la 5 (río) y cavar en la 6 (roca). Letra del libro: L.
import { openGame } from './ui.js';
import { guardarLetra, estilo } from './libro.js';

const LETRA = 'L';
const PRESENTE = ['aldea', 'libre', 'zarza', 'libre', 'rio', 'roca', 'castillo'];
const PASADO = ['aldea', 'pradera', 'bosquecillo', 'pradera', 'charca', 'colina', 'castillo'];
const ACCIONES = [
  { a: 'plantar', nombre: 'Plantar la habichuela' },
  { a: 'cavar', nombre: 'Cavar' },
  { a: 'fuego', nombre: 'Encender fuego' }
];
const TERRENO = {
  aldea: ['Aldea', '#8d7bd6'], libre: ['Camino', '#9ccf6a'], zarza: ['Zarzas', '#7a3d5e'], rio: ['Río', '#3b6fd6'], roca: ['Roca', '#8a8a96'], castillo: ['Castillo', '#d6a84a'],
  puente: ['Puente de habichuela', '#58c46a'], zarzal: ['Zarzas enredadas', '#7a3d5e'], hueco: ['Hueco bajo la roca', '#5a4a3a'], foso: ['Foso', '#2a1a14'], ceniza: ['Ceniza', '#b8b0a8'], habichuela: ['Habichuela', '#58c46a'],
  pradera: ['Pradera', '#a9dc74'], bosquecillo: ['Bosquecillo', '#2e8a4a'], charca: ['Charca', '#4da3d6'], colina: ['Colina', '#c4a35a']
};
// nombres cortos para las casillas estrechas (los largos van en los mensajes y en aria-label)
const CORTO = { bosquecillo: 'Bosque', pradera: 'Prado', puente: 'Puente', zarzal: 'Zarzal', hueco: 'Hueco', habichuela: 'Haba', castillo: 'Castillo', zarza: 'Zarzas', charca: 'Charca', camino: 'Camino' };
const PASABLES = new Set(['aldea', 'castillo', 'libre', 'ceniza', 'puente', 'hueco', 'habichuela']);

function efecto(accion, t) {
  if (accion === 'plantar') return { rio: 'puente', zarza: 'zarzal', roca: 'roca', libre: 'habichuela' }[t] || t;
  if (accion === 'cavar') return { roca: 'hueco', libre: 'foso', rio: 'rio', zarza: 'zarza' }[t] || t;
  if (accion === 'fuego') return { zarza: 'ceniza', libre: 'ceniza', rio: 'rio', roca: 'roca' }[t] || t;
  return t;
}

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 40 — Había una vez... y ahora',
    instr: 'Elige una acción y toca una casilla de «Había una vez»: cambiará «Y ahora». Tenéis exactamente tres saltos y una acción por casilla. Las reglas están en el cuento del Búho (carta 42).',
    ...opts
  });
  estilo('cu-salto-estilo', `
    .sal-fila{margin:4px 0 8px}
    .sal-fila h4{margin:0 0 4px;font-size:.85rem;color:#ffe08a;text-align:left;letter-spacing:.03em}
    .sal-celdas{display:grid;grid-template-columns:repeat(7,1fr);gap:3px}
    .sal-celda{position:relative;aspect-ratio:1/1.15;border-radius:8px;border:2px solid rgba(255,255,255,.25);padding:2px;color:#12082a;font:700 .54rem/1.1 inherit;letter-spacing:-.01em;font-family:inherit;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;text-align:center;overflow:hidden;min-width:0}
    button.sal-celda{cursor:pointer}
    .sal-celda .num{position:absolute;top:2px;left:4px;font-size:.62rem;color:#12082a;opacity:.8}
    .sal-celda .ico{position:absolute;top:12px;left:50%;transform:translateX(-50%);width:46%;aspect-ratio:1;border-radius:50%;background:rgba(255,255,255,.35)}
    .sal-celda[data-t="rio"] .ico,.sal-celda[data-t="charca"] .ico{border-radius:40% 60% 50% 50%;background:rgba(255,255,255,.5)}
    .sal-celda[data-t="zarza"] .ico,.sal-celda[data-t="zarzal"] .ico,.sal-celda[data-t="bosquecillo"] .ico{clip-path:polygon(50% 0,100% 100%,0 100%);border-radius:0;background:rgba(20,70,30,.55)}
    .sal-celda[data-t="roca"] .ico,.sal-celda[data-t="colina"] .ico{border-radius:50% 50% 8% 8%;background:rgba(60,60,70,.5)}
    .sal-celda[data-t="foso"] .ico,.sal-celda[data-t="hueco"] .ico{background:rgba(0,0,0,.55)}
    .sal-celda[data-t="castillo"] .ico,.sal-celda[data-t="aldea"] .ico{border-radius:2px;background:rgba(40,20,80,.45)}
    .sal-celda[data-t="puente"] .ico,.sal-celda[data-t="habichuela"] .ico{border-radius:30% 70% 30% 70%;background:rgba(10,90,40,.6)}
    .sal-celda[data-t="ceniza"] .ico{background:rgba(70,70,70,.5)}
    .sal-celda.hecha{outline:3px solid #fff2a8;outline-offset:-3px}
    .sal-celda .marca{position:absolute;top:2px;right:3px;font-size:.55rem;font-weight:800;background:#12082a;color:#ffe08a;padding:0 3px;border-radius:4px}
    .sal-celda.bloquea{outline:3px solid #ff8f8f;outline-offset:-3px}
    .sal-paleta{display:flex;gap:6px;justify-content:center;flex-wrap:wrap;margin:8px 0}
    .sal-accion{min-height:44px;padding:6px 10px;border-radius:10px;border:2px solid rgba(255,224,138,.5);background:rgba(255,255,255,.08);color:#fff;font:700 .82rem inherit;font-family:inherit;cursor:pointer}
    .sal-accion.sel{background:#ffe08a;color:#2a1450;border-color:#fff}
    .sal-cont{font-size:.85rem;color:#d8e2ee;margin-bottom:4px}
    .sal-img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.6;pointer-events:none}
  `);

  const cont = document.createElement('div');
  cont.className = 'sal-cont';
  const paleta = document.createElement('div');
  paleta.className = 'sal-paleta';
  paleta.setAttribute('role', 'group');
  paleta.setAttribute('aria-label', 'Acciones en el pasado');
  const filaPasado = document.createElement('div');
  filaPasado.className = 'sal-fila';
  filaPasado.innerHTML = '<h4>Había una vez... (el pasado)</h4>';
  const celdasPasado = document.createElement('div');
  celdasPasado.className = 'sal-celdas';
  filaPasado.appendChild(celdasPasado);
  const filaAhora = document.createElement('div');
  filaAhora.className = 'sal-fila';
  filaAhora.innerHTML = '<h4>Y ahora... (el presente)</h4>';
  const celdasAhora = document.createElement('div');
  celdasAhora.className = 'sal-celdas';
  filaAhora.appendChild(celdasAhora);
  ui.body.append(cont, filaPasado, paleta, filaAhora);

  let accionSel = null;
  const hechas = {}; // casilla -> acción
  let resuelto = false;

  ACCIONES.forEach((x) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'sal-accion';
    b.dataset.a = x.a;
    b.textContent = x.nombre;
    b.addEventListener('click', () => { accionSel = accionSel === x.a ? null : x.a; pintar(); });
    paleta.appendChild(b);
  });

  function celda(t, i, interactiva) {
    const e = document.createElement(interactiva ? 'button' : 'div');
    if (interactiva) e.type = 'button';
    e.className = 'sal-celda';
    e.dataset.i = String(i);
    e.dataset.t = t;
    e.style.background = TERRENO[t][1];
    e.innerHTML = '<span class="num">' + (i + 1) + '</span><span class="ico"></span><span>' + (CORTO[t] || TERRENO[t][0]) + '</span>';
    return e;
  }

  function pintar() {
    paleta.querySelectorAll('.sal-accion').forEach((b) => b.classList.toggle('sel', b.dataset.a === accionSel));
    celdasPasado.replaceChildren();
    celdasAhora.replaceChildren();
    const presente = PRESENTE.map((t, i) => (hechas[i] ? efecto(hechas[i], t) : t));
    PASADO.forEach((t, i) => {
      const e = celda(t, i, true);
      e.classList.add('sal-casilla');
      if (hechas[i]) {
        e.classList.add('hecha');
        const m = document.createElement('span');
        m.className = 'marca';
        m.textContent = ACCIONES.find((x) => x.a === hechas[i]).nombre.split(' ')[0];
        e.appendChild(m);
      }
      e.setAttribute('aria-label', 'Casilla ' + (i + 1) + ' en el pasado: ' + TERRENO[t][0] + (hechas[i] ? ', con la acción ' + hechas[i] : ''));
      e.addEventListener('click', () => tocar(i));
      celdasPasado.appendChild(e);
    });
    presente.forEach((t, i) => {
      const e = celda(t, i, false);
      e.classList.add('sal-ahora');
      e.setAttribute('aria-label', 'Casilla ' + (i + 1) + ' hoy: ' + TERRENO[t][0] + (PASABLES.has(t) ? ', se puede pasar' : ', bloquea el camino'));
      celdasAhora.appendChild(e);
    });
    cont.textContent = 'Saltos usados: ' + Object.keys(hechas).length + ' de 3';
  }

  function tocar(i) {
    if (resuelto) return;
    if (i === 0 || i === 6) { ui.say('Esa casilla es la aldea o el castillo: no se puede cambiar.', 'bad'); return; }
    ui.say('');
    if (!accionSel) {
      if (hechas[i]) { delete hechas[i]; pintar(); return; }
      ui.say('Primero elige una acción: plantar, cavar o fuego.', '');
      return;
    }
    if (!hechas[i] && Object.keys(hechas).length >= 3) { ui.say('Ya habéis usado los tres saltos. Quitad uno tocando su casilla sin acción elegida.', 'bad'); return; }
    hechas[i] = accionSel;
    pintar();
  }

  function cruzar() {
    if (resuelto) return;
    const n = Object.keys(hechas).length;
    if (n !== 3) { ui.say('Tenéis que hacer exactamente tres saltos y habéis hecho ' + n + '.', 'bad'); return; }
    const presente = PRESENTE.map((t, i) => (hechas[i] ? efecto(hechas[i], t) : t));
    const bloqueo = presente.findIndex((t) => !PASABLES.has(t));
    celdasAhora.querySelectorAll('.sal-celda').forEach((c, i) => c.classList.toggle('bloquea', i === bloqueo));
    if (bloqueo === -1) {
      resuelto = true;
      guardarLetra('40', LETRA);
      ui.say('¡El camino queda libre de la aldea al castillo! La habichuela, el fuego y la pala del pasado lo han cambiado todo. Coged la carta 44. Letra del libro: ' + LETRA + '.', 'ok');
    } else {
      ui.say('En el presente sigue bloqueando el camino: ' + TERRENO[presente[bloqueo]][0].toLowerCase() + ' (casilla ' + (bloqueo + 1) + '). Cambiad los saltos y volved a probar.', 'bad');
    }
  }

  ui.button('Cruzar al presente', 'primary', cruzar).classList.add('sal-cruzar');
  ui.button('Quitar los saltos', 'ghost', () => { if (!resuelto) { Object.keys(hechas).forEach((k) => delete hechas[k]); accionSel = null; ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
