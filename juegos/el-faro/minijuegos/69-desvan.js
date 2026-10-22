// Carta 69 — El desván a oscuras: pilas de cajas forman un laberinto de 8 x 8 casillas. Solo se ve la linterna: hay que cruzarlo con las órdenes «avanzar»,
// «girar a la izquierda» y «girar a la derecha», empezando abajo a la izquierda y mirando al norte. El plano está en las cartas 70 y 71
// (herramientas/instancias_faro.py, laberinto).
import { openGame } from './ui.js';
import { estilo } from './comun.js';

const L = /*DATOS*/{"n": 8, "abierto": [["ES", "OS", "ES", "EO", "EOS", "EO", "EO", "OS"], ["NS", "N", "NS", "S", "EN", "OS", "ES", "NO"], ["ENS", "EO", "NO", "NS", "ES", "NO", "EN", "O"], ["ENS", "EO", "EO", "NO", "EN", "EOS", "EO", "OS"], ["N", "ES", "EO", "EO", "OS", "N", "ES", "NOS"], ["ES", "NO", "ES", "OS", "NS", "ES", "NO", "NS"], ["NS", "S", "NS", "NS", "EN", "NO", "ES", "NO"], ["N", "EN", "NO", "EN", "EO", "EO", "ENO", "O"]], "inicio": [7, 0], "meta": [0, 7], "mira": "N"}/*FIN*/;
const ORDEN = 'NESO';
const DF = { N: [-1, 0], E: [0, 1], S: [1, 0], O: [0, -1] };
const NOMBRE = { N: 'el norte', E: 'el este', S: 'el sur', O: 'el oeste' };
const FLECHA = { N: '↑', E: '→', S: '↓', O: '←' };

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 69 — El desván a oscuras',
    instr: 'No se ve nada más que la linterna. Avanzad una casilla, o girad a un lado, hasta llegar a la trampilla del plano (cartas 70 y 71). Entráis abajo a la izquierda mirando al norte.',
    ...opts
  });
  estilo('fa-des', '.des-b{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:8px 0}.des-b button{padding:14px 4px;border-radius:10px;border:1.5px solid rgba(201,164,90,.6);background:linear-gradient(180deg,rgba(255,255,255,.12),rgba(0,0,0,.25));color:#fff;font:700 .95rem system-ui,sans-serif;cursor:pointer}.des-v{text-align:center;color:#ffd27a;font:700 1.4rem system-ui,sans-serif;margin:8px 0}.des-r{min-height:2.6em;color:#cfe3ee;font:600 .85rem ui-monospace,Consolas,monospace;word-break:break-all;text-align:center}');
  let f, c, mira, pasos, resuelto = false;
  const vista = document.createElement('div');
  vista.className = 'des-v';
  const botones = document.createElement('div');
  botones.className = 'des-b';
  const reg = document.createElement('div');
  reg.className = 'des-r';
  ui.body.append(vista, botones, reg);
  const reiniciar = () => { f = L.inicio[0]; c = L.inicio[1]; mira = L.mira; pasos = ''; };
  reiniciar();
  function pintar() {
    vista.textContent = 'La linterna mira hacia ' + NOMBRE[mira] + ' ' + FLECHA[mira];
    reg.textContent = pasos.split('').join(' ');
  }
  function orden(o) {
    if (resuelto) return;
    if (o === 'A') {
      if (!L.abierto[f][c].includes(mira)) { ui.say('Chocáis con una pila de cajas: por ahí no se pasa.', 'bad'); return; }
      f += DF[mira][0];
      c += DF[mira][1];
      pasos += 'A';
      ui.say('');
      if (f === L.meta[0] && c === L.meta[1]) {
        resuelto = true;
        ui.say('¡La trampilla! Os colais por ella y llegáis, tras la última escalera, a la sala de la lente. Coged la carta 80.', 'ok');
      }
    } else {
      mira = ORDEN[(ORDEN.indexOf(mira) + (o === 'D' ? 1 : 3)) % 4];
      pasos += o;
      ui.say('');
    }
    pintar();
  }
  [['A', 'Avanzar'], ['I', 'Girar a la izquierda'], ['D', 'Girar a la derecha']].forEach(([o, t]) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.dataset.o = o;
    b.textContent = t;
    b.addEventListener('click', () => orden(o));
    botones.appendChild(b);
  });
  ui.button('Volver a la entrada', '', () => { if (!resuelto) { reiniciar(); ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
