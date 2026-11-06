// Carta 51 — El canto de los colosos: Simon traducido. Los colosos cantan con cuatro sonidos (se ven y se oyen); se responde con cuatro palabras.
// La traducción está repartida entre la hoja de la sargento y el cancionero; la última ronda se responde al revés.
// Rondas y respuestas en herramientas/instancias_colosos.py (canto).
import { openGame } from './ui.js';
import { estilo, boton, tono } from './comun.js';

const D = /*DATOS*/{"rondas": [["doble", "grave", "largo"], ["agudo", "doble", "largo", "grave"], ["agudo", "largo", "agudo", "doble", "agudo"]], "solucion": [["piedra", "flor", "río"], ["luna", "piedra", "río", "flor"], ["luna", "piedra", "luna", "río", "luna"]], "respuestas": ["piedra", "río", "luna", "flor"]}/*FIN*/;
const SON = { grave: { f: 98, d: 0.7, txt: 'GRAVE' }, agudo: { f: 392, d: 0.35, txt: 'AGUDO' }, largo: { f: 147, d: 1.2, txt: 'LARGO' }, doble: { f: 196, d: 0.25, txt: 'DOBLE' } };
const EMO = { piedra: '🪨', 'río': '🌊', luna: '🌙', flor: '🌸' };

estilo('co-canto', `
  .co-escena{height:96px;margin:6px auto;max-width:320px;border-radius:12px;background:radial-gradient(circle at 50% 120%,#3a5a3a,#142014);
    display:flex;align-items:center;justify-content:center;color:#ffd27a;font:800 1.6rem 'Cinzel',Georgia,serif;letter-spacing:.08em}
  .co-escena.canta{animation:coPulso .5s ease-out}
  @keyframes coPulso{0%{transform:scale(1.12);text-shadow:0 0 18px #ffd27a}100%{transform:scale(1)}}
  .co-resp{display:flex;gap:6px;justify-content:center;flex-wrap:wrap;min-height:30px;color:#fff6e4;font:700 1rem system-ui,sans-serif}
`);

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 51 — El canto de los colosos',
    instr: 'Pulsad «Escuchar» y responded al canto, sonido a sonido, con las palabras de los colosos. Son tres rondas.',
    ...opts
  });
  let ronda = 0;
  let resp = [];
  let sonando = false;
  const pie = document.createElement('div');
  pie.className = 'co-pie';
  const escena = document.createElement('div');
  escena.className = 'co-escena';
  escena.id = 'coEscena';
  const respuesta = document.createElement('div');
  respuesta.className = 'co-resp';
  const btns = document.createElement('div');
  btns.className = 'co-btns';
  D.respuestas.forEach(w => {
    const b = boton(EMO[w] + ' ' + w, () => responder(w));
    b.dataset.palabra = w;
    btns.appendChild(b);
  });
  ui.body.append(pie, escena, respuesta, btns);

  const esperar = ms => new Promise(r => setTimeout(r, ms));
  async function escuchar() {
    if (sonando) return;
    sonando = true;
    resp = [];
    pintar();
    for (const s of D.rondas[ronda]) {
      escena.textContent = SON[s].txt;
      escena.classList.remove('canta');
      void escena.offsetWidth;
      escena.classList.add('canta');
      if (s === 'doble') { tono(SON[s].f, 0.22, 'triangle', 0.25); await esperar(280); tono(SON[s].f, 0.22, 'triangle', 0.25); }
      else tono(SON[s].f, SON[s].d, 'triangle', 0.25);
      await esperar(SON[s].d * 1000 + 650);
      escena.textContent = '';
      await esperar(200);
    }
    escena.textContent = '…';
    sonando = false;
  }

  function responder(w) {
    if (ronda >= D.rondas.length) return;
    resp.push(w);
    pintar();
    const esperado = D.solucion[ronda];
    if (resp[resp.length - 1] !== esperado[resp.length - 1]) {
      ui.say('Los colosos se miran, confundidos, y se tumban otra vez. Volvemos a la primera ronda.', 'bad');
      ronda = 0;
      resp = [];
      setTimeout(pintar, 200);
      return;
    }
    if (resp.length === esperado.length) {
      ronda += 1;
      resp = [];
      if (ronda === D.rondas.length) {
        ui.say('El valle entero os responde con un canto suave y los colosos se apartan para dejaros pasar. Coged la carta 58.', 'ok');
        btns.querySelectorAll('button').forEach(b => { b.disabled = true; });
      } else {
        ui.say('¡Os han entendido! Los colosos cantan otra vez, un poco más largo.', '');
      }
      setTimeout(pintar, 200);
    }
  }

  function pintar() {
    pie.textContent = ronda < D.rondas.length ? `Ronda ${ronda + 1} de ${D.rondas.length}` : 'Canto terminado';
    respuesta.textContent = resp.map(w => EMO[w]).join(' ');
  }

  ui.button('Escuchar', 'primary', escuchar);
  pintar();
  return { close: ui.close };
}
