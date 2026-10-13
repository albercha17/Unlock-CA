// Carta 46 — Secuenciador de ADN: escribir la cadena complementaria de la muestra de ámbar (carta 37).
// Muestra: A T G C C G T A. Pareja: A con T, C con G. Solución: T A C G G C A T.
import { openGame } from './ui.js';

const MUESTRA = 'ATGCCGTA';
const PAREJA = { A: 'T', T: 'A', C: 'G', G: 'C' };
const BASES = ['A', 'T', 'C', 'G'];
const IMG = './img/ui/';

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 46 — Secuenciador de ADN',
    instr: 'Escribe la cadena complementaria de la muestra, letra a letra, y pulsa Secuenciar.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .adn-mon{position:relative;max-width:350px;margin:0 auto 12px;aspect-ratio:4/3;background:#000}
    .adn-mon>img{position:absolute;inset:0;width:100%;height:100%;object-fit:fill;pointer-events:none;mix-blend-mode:screen}
    .adn-pant{position:absolute;left:13.6%;right:13.6%;top:16.4%;bottom:23%;overflow:hidden;border-radius:6px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;padding:4px;background:radial-gradient(ellipse at center,#052418,#020f0a);box-shadow:inset 0 0 26px rgba(60,255,150,.18)}
    .adn-hebra{display:grid;grid-template-columns:repeat(8,1fr);gap:4px;width:100%}
    .adn-slot{position:relative;aspect-ratio:1;border-radius:7px;border:2px dashed rgba(125,255,176,.45);display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,.35)}
    .adn-slot.lleno{border-style:solid;border-color:rgba(125,255,176,.9);background:rgba(0,0,0,.2)}
    .adn-slot img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;mix-blend-mode:screen}
    .adn-slot b{position:relative;font:800 1rem Georgia,serif;color:#fff;text-shadow:0 0 5px #000,0 0 3px #000}
    .adn-etq{font-size:.62rem;color:#7dffb0;letter-spacing:.14em;text-transform:uppercase}
    .adn-teclas{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;max-width:340px;margin:0 auto 8px}
    .adn-base{position:relative;aspect-ratio:1;padding:0;border:0;background:#000;border-radius:12px;cursor:pointer;overflow:hidden;box-shadow:0 4px 10px rgba(0,0,0,.55);transition:transform .1s}
    .adn-base:active{transform:scale(.94)}
    .adn-base img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;mix-blend-mode:screen}
    .adn-base b{position:relative;font:800 1.5rem Georgia,serif;color:#fff;text-shadow:0 0 6px #000,0 0 3px #000}
    .adn-base:disabled{opacity:.45;cursor:not-allowed}
  `;
  ui.body.appendChild(style);

  const mon = document.createElement('div');
  mon.className = 'adn-mon';
  const pant = document.createElement('div');
  pant.className = 'adn-pant';
  pant.innerHTML = '<div class="adn-etq">Cadena nueva</div>';
  const hebra = document.createElement('div');
  hebra.className = 'adn-hebra';
  pant.appendChild(hebra);
  mon.appendChild(pant);
  mon.insertAdjacentHTML('beforeend', '<img alt="" src="' + IMG + 'marco-lab.jpg">');
  const teclas = document.createElement('div');
  teclas.className = 'adn-teclas';
  ui.body.append(mon, teclas);

  let escrita = '';
  let resuelto = false;

  function pintar() {
    hebra.innerHTML = '';
    for (let i = 0; i < MUESTRA.length; i++) {
      const s = document.createElement('div');
      const b = escrita[i];
      s.className = 'adn-slot' + (b ? ' lleno' : '');
      s.dataset.i = String(i);
      s.dataset.base = b || '';
      if (b) s.innerHTML = '<img alt="" src="' + IMG + 'bases/' + b.toLowerCase() + '.jpg"><b>' + b + '</b>';
      hebra.appendChild(s);
    }
  }

  BASES.forEach(b => {
    const t = document.createElement('button');
    t.type = 'button';
    t.className = 'adn-base';
    t.dataset.b = b;
    t.setAttribute('aria-label', 'Base ' + b);
    t.innerHTML = '<img alt="" src="' + IMG + 'bases/' + b.toLowerCase() + '.jpg"><b>' + b + '</b>';
    t.addEventListener('click', () => {
      if (resuelto || escrita.length >= MUESTRA.length) return;
      escrita += b;
      ui.say('');
      pintar();
    });
    teclas.appendChild(t);
  });

  ui.button('Borrar', 'ghost', () => { if (!resuelto) { escrita = escrita.slice(0, -1); ui.say(''); pintar(); } });
  ui.button('Secuenciar', 'primary', () => {
    if (resuelto) return;
    const objetivo = MUESTRA.split('').map(c => PAREJA[c]).join('');
    if (escrita === objetivo) {
      resuelto = true;
      teclas.querySelectorAll('button').forEach(x => { x.disabled = true; });
      ui.say('La cerradura biométrica reconoce la cadena y la pequeña caja fuerte se abre con un chasquido. Coged la carta 54.', 'ok');
    } else if (escrita.length < MUESTRA.length) {
      ui.say('La cadena está incompleta: faltan bases.', 'bad');
    } else {
      ui.say('La cerradura no reconoce la cadena. Repasad cómo se emparejan las bases.', 'bad');
    }
  });

  pintar();
  return { close: ui.close };
}
