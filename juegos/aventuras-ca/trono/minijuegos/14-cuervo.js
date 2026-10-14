// Carta 14 — Mensaje del cuervo: leer un mensaje cifrado (cifra del César, desplazamiento 3) con la rueda del maestre (carta 16).
// Es el primer puzle del juego: enseña el control. La rueda muestra, bajo cada letra del anillo exterior, la letra verdadera.
import { openGame } from './ui.js';
import { guardarPalabra, estilo, conImagen, texturaSi } from './comun.js';

const ABC = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
const CIFRADO = 'EDMDG DO DUFKLYR';
const CLARO = 'BAJAD AL ARCHIVO';
const PALABRA = 'HIELO';

function descifrar(texto, k) {
  return texto.split('').map(c => (ABC.includes(c) ? ABC[(ABC.indexOf(c) - k + 26) % 26] : c)).join('');
}

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 14 — Mensaje del cuervo',
    instr: 'El mensaje del maestre está en cifra. Gira la rueda hasta que bajo cada letra del mensaje aparezca una letra con sentido.',
    ...opts
  });
  texturaSi(ui, 'piedra.jpg', { opacidad: 0.3, mezcla: 'screen' });

  estilo(ui.body, `
    .cue-pergamino{margin:0 auto 10px;max-width:340px;padding:10px 12px;border-radius:8px;background:linear-gradient(#e7d9b4,#cdb98a);color:#2b1c0a;font:700 1.35rem Georgia,serif;letter-spacing:.14em;text-align:center;box-shadow:inset 0 0 18px rgba(90,60,20,.45)}
    .cue-pergamino small{display:block;font:600 .7rem Poppins,sans-serif;letter-spacing:.08em;text-transform:uppercase;opacity:.7;margin-bottom:2px}
    .cue-claro{margin-top:6px;padding-top:6px;border-top:1px dashed rgba(60,40,10,.45);min-height:1.7rem;color:#143a58}
    .cue-rueda{position:relative;width:min(280px,80vw);aspect-ratio:1;margin:4px auto 6px}
    .cue-rueda svg{width:100%;height:100%;display:block}
    .cue-mando{display:flex;justify-content:center;align-items:center;gap:10px;margin:6px 0 2px}
    .cue-mando button{min-width:64px;min-height:48px;font-size:1.2rem}
    .cue-pos{min-width:96px;color:#d6e8f5;font-size:.9rem}
    .cue-cuervo{position:absolute;left:50%;top:50%;width:26%;aspect-ratio:1;transform:translate(-50%,-50%);border-radius:50%;background:radial-gradient(circle at 40% 35%,#2d3946,#0b1118);border:2px solid #8aa6bc;display:flex;align-items:center;justify-content:center}
    .cue-cuervo.img{background:var(--img) center/cover}
    .cue-cuervo svg{width:70%;height:70%}
  `);

  let desp = 0;
  let resuelto = false;

  const perg = document.createElement('div');
  perg.className = 'cue-pergamino';
  perg.innerHTML = '<small>Mensaje del cuervo</small><div class="cue-cif"></div><div class="cue-claro" aria-live="polite"></div>';
  perg.querySelector('.cue-cif').textContent = CIFRADO;

  const rueda = document.createElement('div');
  rueda.className = 'cue-rueda';
  rueda.dataset.desp = '0';
  const cuervo = document.createElement('div');
  cuervo.className = 'cue-cuervo';
  cuervo.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#cfe3f2" d="M3 14c2-1 3-3 5-4 2-1 4-.5 5 1l5-3c1 0 2 .5 3 1-1 1-2 1.5-3.500 1.500l-1 3c-1 3-4 5-7 5-2 0-3-1-3-3-1 0-2-.5-3-1.500z"/></svg>';
  conImagen(cuervo, 'cuervo.jpg');

  const mando = document.createElement('div');
  mando.className = 'cue-mando';
  const pos = document.createElement('span');
  pos.className = 'cue-pos';
  const menos = document.createElement('button');
  menos.type = 'button';
  menos.className = 'far-btn ghost cue-menos';
  menos.textContent = '‹';
  menos.setAttribute('aria-label', 'Girar la rueda un puesto hacia atrás');
  const mas = document.createElement('button');
  mas.type = 'button';
  mas.className = 'far-btn ghost cue-mas';
  mas.textContent = '›';
  mas.setAttribute('aria-label', 'Girar la rueda un puesto hacia adelante');
  mando.append(menos, pos, mas);
  ui.body.append(perg, rueda, mando);

  function pintarRueda() {
    const R1 = 118, R2 = 90;
    let s = '<svg viewBox="0 0 260 260" role="img" aria-label="Rueda de cifrado: anillo exterior con las letras del mensaje y anillo interior con las letras verdaderas"><circle cx="130" cy="130" r="127" fill="#1a232d" stroke="#8aa6bc" stroke-width="2"/><circle cx="130" cy="130" r="102" fill="#101820" stroke="#5d7a90" stroke-width="1.5"/><circle cx="130" cy="130" r="74" fill="#0b1118" stroke="#8aa6bc" stroke-width="2"/>';
    for (let i = 0; i < 26; i++) {
      const ang = (i * 360 / 26 - 90) * Math.PI / 180;
      const x1 = 130 + R1 * Math.cos(ang), y1 = 130 + R1 * Math.sin(ang) + 4;
      const x2 = 130 + R2 * Math.cos(ang), y2 = 130 + R2 * Math.sin(ang) + 4;
      s += '<text x="' + x1.toFixed(1) + '" y="' + y1.toFixed(1) + '" text-anchor="middle" font-size="13" font-weight="700" fill="#cfe3f2" font-family="Georgia,serif">' + ABC[i] + '</text>';
      s += '<text x="' + x2.toFixed(1) + '" y="' + y2.toFixed(1) + '" text-anchor="middle" font-size="13" font-weight="700" fill="#ffd9a0" font-family="Georgia,serif">' + ABC[(i - desp + 26) % 26] + '</text>';
    }
    s += '</svg>';
    const prev = rueda.querySelector('svg');
    if (prev) prev.remove();
    rueda.insertAdjacentHTML('afterbegin', s);
    rueda.appendChild(cuervo);
    rueda.dataset.desp = String(desp);
    pos.textContent = desp === 0 ? 'Sin girar' : 'Girada ' + desp + (desp === 1 ? ' puesto' : ' puestos');
    perg.querySelector('.cue-claro').textContent = descifrar(CIFRADO, desp);
  }

  function girar(d) {
    if (resuelto) return;
    desp = (desp + d + 26) % 26;
    ui.say('');
    pintarRueda();
  }
  menos.addEventListener('click', () => girar(-1));
  mas.addEventListener('click', () => girar(1));

  ui.button('Leer el mensaje', 'primary', () => {
    if (resuelto) return;
    if (descifrar(CIFRADO, desp) !== CLARO) {
      ui.say('Esas letras no forman palabras con sentido. Girad la rueda hasta que el mensaje se lea con claridad: la carta 16 dice cuántos puestos hay que retroceder.', 'bad');
      return;
    }
    resuelto = true;
    guardarPalabra('14', PALABRA);
    ui.say('El mensaje dice: «' + CLARO + '». El maestre os espera en el archivo de la torre y el cuervo, ya tranquilo, os deja pasar. Palabra de la profecía: «' + PALABRA + '». Anotadla. Coged la carta 26.', 'ok');
  });

  pintarRueda();
  return { close: ui.close };
}
