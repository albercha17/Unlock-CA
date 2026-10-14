// Carta 84 — La profecía (metapuzle final): las ocho palabras que dieron los puzles del castillo (14, 20, 40, 46, 51, 64, 69 y 72) aparecen
// mezcladas en el anillo del Cronoportal; hay que ponerlas en orden con las pistas del maestre (carta 86). Solución única comprobada por
// herramientas/instancias_trono.py. Si falta alguna palabra, la app dice de qué carta.
import { openGame } from './ui.js';
import { leerPalabra, estilo, texturaSi } from './comun.js';

const FRASE = ['SOLO', 'EL', 'FUEGO', 'VENCERÁ', 'AL', 'HIELO', 'DEL', 'NORTE'];
const CARTAS = ['14', '20', '40', '46', '51', '64', '69', '72'];
const REGLAS = [
  { txt: 'La profecía empieza con SOLO.', ok: (o) => o[0] === 'SOLO' },
  { txt: 'FUEGO va justo después de EL.', ok: (o) => o.indexOf('FUEGO') === o.indexOf('EL') + 1 },
  { txt: 'VENCERÁ va justo después de FUEGO.', ok: (o) => o.indexOf('VENCERÁ') === o.indexOf('FUEGO') + 1 },
  { txt: 'AL va justo antes de HIELO.', ok: (o) => o.indexOf('AL') + 1 === o.indexOf('HIELO') },
  { txt: 'VENCERÁ va antes que HIELO.', ok: (o) => o.indexOf('VENCERÁ') < o.indexOf('HIELO') },
  { txt: 'DEL va justo antes de NORTE.', ok: (o) => o.indexOf('DEL') + 1 === o.indexOf('NORTE') },
  { txt: 'NORTE es la última palabra.', ok: (o) => o[o.length - 1] === 'NORTE' }
];

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 84 — La profecía',
    instr: 'El Cronoportal repite las palabras que habéis ido recuperando en el castillo. Tocad las palabras en el orden correcto, con las pistas del maestre (carta 86). Tocad una palabra colocada para quitarla.',
    ...opts
  });
  texturaSi(ui, 'pergamino.jpg', { opacidad: 0.25, mezcla: 'screen' });

  estilo(ui.body, `
    .pro-frase{display:grid;grid-template-columns:repeat(2,1fr);gap:6px;max-width:340px;margin:0 auto 10px}
    .pro-hueco{min-height:46px;border-radius:8px;border:1px dashed rgba(207,232,251,.55);background:rgba(6,10,16,.6);color:#ffe3a8;font:700 .95rem Georgia,serif;letter-spacing:.05em;cursor:pointer;touch-action:manipulation;display:flex;align-items:center;justify-content:center;gap:6px;padding:0 6px}
    .pro-hueco span{color:#6f8294;font:600 .7rem Poppins,sans-serif;margin-right:2px}
    .pro-hueco[data-w]{border-style:solid;background:linear-gradient(#3b4856,#26303a)}
    .pro-banco{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;max-width:360px;margin:0 auto 8px}
    .pro-ficha{min-height:46px;padding:0 12px;border-radius:8px;border:1px solid #d9c79a;background:linear-gradient(#e3d3a8,#b9a574);color:#2a1c0a;font:700 .95rem Georgia,serif;letter-spacing:.05em;cursor:pointer;touch-action:manipulation}
    .pro-ficha:disabled{opacity:.35;cursor:default}
    .pro-ficha.falta{border-style:dashed;background:rgba(6,10,16,.6);color:#8aa0b2;opacity:1}
    .pro-nota{font-size:.78rem;color:#a9bccb;margin:2px 0 4px}
  `);

  const palabras = CARTAS.map(c => ({ carta: c, w: leerPalabra(c) }));
  const faltan = palabras.filter(p => !p.w);
  const frase = document.createElement('div');
  frase.className = 'pro-frase';
  const banco = document.createElement('div');
  banco.className = 'pro-banco';
  const nota = document.createElement('div');
  nota.className = 'pro-nota';
  ui.body.append(frase, banco, nota);

  const orden = []; // palabras colocadas
  let resuelto = false;
  const huecos = [];
  const fichas = {};

  for (let i = 0; i < 8; i++) {
    const h = document.createElement('button');
    h.type = 'button';
    h.className = 'pro-hueco';
    h.dataset.i = String(i);
    h.addEventListener('click', () => {
      if (resuelto || i >= orden.length) return;
      orden.splice(i, 1);
      ui.say('');
      pintar();
    });
    huecos.push(h);
    frase.appendChild(h);
  }

  palabras.forEach(p => {
    const f = document.createElement('button');
    f.type = 'button';
    f.className = 'pro-ficha' + (p.w ? '' : ' falta');
    f.dataset.w = p.w || '';
    f.dataset.carta = p.carta;
    f.textContent = p.w || '?';
    f.setAttribute('aria-label', p.w ? 'Palabra ' + p.w : 'Falta la palabra de la carta ' + p.carta);
    if (!p.w) f.disabled = true;
    f.addEventListener('click', () => {
      if (resuelto || !p.w || orden.includes(p.w) || orden.length >= 8) return;
      orden.push(p.w);
      ui.say('');
      pintar();
    });
    fichas[p.carta] = f;
    banco.appendChild(f);
  });

  function pintar() {
    huecos.forEach((h, i) => {
      const w = orden[i];
      if (w) h.dataset.w = w; else delete h.dataset.w;
      h.innerHTML = '<span>' + (i + 1) + '</span>' + (w || '');
      h.setAttribute('aria-label', 'Lugar ' + (i + 1) + (w ? ': ' + w + ' (tocad para quitarla)' : ': vacío'));
    });
    palabras.forEach(p => { if (p.w) fichas[p.carta].disabled = orden.includes(p.w); });
  }
  pintar();

  if (faltan.length) {
    nota.textContent = 'Faltan palabras: ' + faltan.map(p => 'carta ' + p.carta).join(', ') + '.';
    ui.say('Faltan palabras de la profecía. Cada puzle del castillo da una al resolverse: volved a resolver ' + (faltan.length === 1 ? 'el de la carta ' : 'los de las cartas ') + faltan.map(p => p.carta).join(', ') + '.', 'bad');
  } else {
    nota.textContent = 'Tenéis las ocho palabras. Las pistas para ordenarlas están en las notas del maestre (carta 86).';
  }

  ui.button('Quitar todas', 'ghost', () => { if (!resuelto) { orden.length = 0; ui.say(''); pintar(); } });
  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    if (faltan.length) { ui.say('Todavía faltan palabras: volved a resolver los puzles de las cartas ' + faltan.map(p => p.carta).join(', ') + '.', 'bad'); return; }
    if (orden.length < 8) { ui.say('Faltan palabras por colocar: hay ocho lugares.', 'bad'); return; }
    const mala = REGLAS.find(r => !r.ok(orden));
    if (mala) { ui.say('Algo no encaja con las pistas del maestre: «' + mala.txt + '»', 'bad'); return; }
    resuelto = true;
    ui.say('Las palabras se ordenan en el aire y el anillo las pronuncia: «Solo el fuego vencerá al hielo del norte». El portal se abre. Coged la carta 99.', 'ok');
  });

  return { close: ui.close };
}
