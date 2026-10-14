// Carta 46 — Lengua del pueblo libre: traducir una frase usando los ejemplos de dos cartas (48 y 37). Cada carta trae tres frases y
// ninguna sola da todo el vocabulario. La lengua tiene orden fijo (sujeto-objeto-verbo), adjetivo detrás del nombre y plural en -i
// (también en el adjetivo). Comprobado por herramientas/instancias_trono.py: los seis ejemplos fijan una única traducción.
import { openGame } from './ui.js';
import { guardarPalabra, estilo, texturaSi } from './comun.js';

const PREGUNTA = 'Los cuervos negros temen al guerrero';
const RESPUESTA = 'krai skai hod ven';
const PALABRA = 'DEL';

function normalizar(t) { return t.trim().toLowerCase().replace(/\s+/g, ' '); }

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 46 — Lengua del pueblo libre',
    instr: 'La prisionera solo confiará en vosotros si sabéis decir una frase en su lengua. Los rollos de las cartas 48 y 37 traen ejemplos: fijaos en el orden de las palabras y en los plurales.',
    ...opts
  });
  texturaSi(ui, 'piedra.jpg', { opacidad: 0.3, mezcla: 'screen' });

  estilo(ui.body, `
    .len-dice{margin:0 auto 10px;max-width:340px;padding:12px;border-radius:10px;background:rgba(0,0,0,.34);border:1px solid rgba(159,184,204,.45)}
    .len-dice small{display:block;color:#a9bccb;font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;margin-bottom:4px}
    .len-dice q{display:block;color:#eaf4fb;font:700 1.12rem Georgia,serif;quotes:"«" "»"}
    .len-in{width:100%;max-width:340px;min-height:50px;border-radius:10px;border:1px solid rgba(207,232,251,.55);background:rgba(6,10,16,.8);color:#ffe3a8;font:700 1.15rem Georgia,serif;letter-spacing:.06em;padding:8px 12px;text-align:center}
    .len-in:focus{outline:2px solid #8fc7ee}
    .len-ayuda{font-size:.78rem;color:#a9bccb;margin:6px 0 2px}
  `);

  const dice = document.createElement('div');
  dice.className = 'len-dice';
  dice.innerHTML = '<small>La prisionera pide que digáis en su lengua</small><q></q>';
  dice.querySelector('q').textContent = PREGUNTA;
  const inp = document.createElement('input');
  inp.type = 'text';
  inp.className = 'len-in';
  inp.autocomplete = 'off';
  inp.autocapitalize = 'off';
  inp.spellcheck = false;
  inp.setAttribute('aria-label', 'Tu frase en la lengua del pueblo libre');
  inp.placeholder = 'Escribid la frase';
  const ayuda = document.createElement('div');
  ayuda.className = 'len-ayuda';
  ayuda.textContent = 'Todo lo que necesitáis está en los ejemplos de las dos cartas.';
  ui.body.append(dice, inp, ayuda);

  let resuelto = false;
  function comprobar() {
    if (resuelto) return;
    const r = normalizar(inp.value);
    if (!r) { ui.say('Escribid la frase en la lengua del pueblo libre.', 'bad'); return; }
    if (r === RESPUESTA) {
      resuelto = true;
      guardarPalabra('46', PALABRA);
      ui.say('La prisionera sonríe por primera vez: habéis hablado como los suyos. Palabra de la profecía: «' + PALABRA + '». Anotadla. Coged la carta 54.', 'ok');
      return;
    }
    const a = r.split(' ').sort().join(' ');
    const b = RESPUESTA.split(' ').sort().join(' ');
    const sinPlural = (t) => t.split(' ').map(w => w.replace(/i$/, '')).sort().join(' ');
    if (a === b) ui.say('Reconoce las palabras, pero no el orden de su lengua. Mirad dónde van el verbo y el nombre en los ejemplos.', 'bad');
    else if (sinPlural(r) === sinPlural(RESPUESTA)) ui.say('Las palabras son las correctas, pero algún plural no suena bien: mirad cómo cambian en los ejemplos con «Los».', 'bad');
    else ui.say('Esa frase no es la que espera: alguna palabra no es de su lengua. Buscadla en los ejemplos de los rollos (cartas 48 y 37).', 'bad');
  }
  inp.addEventListener('keydown', (e) => { if (e.key === 'Enter') { e.preventDefault(); comprobar(); } });
  ui.button('Decirlo', 'primary', comprobar);
  return { close: ui.close };
}
