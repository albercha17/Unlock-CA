// Carta 51 — Los consejeros: leales (siempre dicen la verdad) y traidores (siempre mienten). Las frases están en dos cartas
// (26 y 52); la app solo pide decidir quién es quién. Solución única comprobada por herramientas/instancias_trono.py.
import { openGame } from './ui.js';
import { guardarPalabra, estilo, conImagen, texturaSi } from './comun.js';

const NOMBRES = ['Aldric', 'Brenna', 'Corvin', 'Dalia'];
// frase de cada consejero: tipo, personas a las que se refiere
const FRASES = [
  { tipo: 'ambos', j: 1, k: 2, txt: 'Brenna y Corvin son leales.' },
  { tipo: 'es', j: 0, txt: 'Aldric es leal.' },
  { tipo: 'no es', j: 1, txt: 'Brenna es un traidor.' },
  { tipo: 'es', j: 2, txt: 'Corvin es leal.' }
];
const LEALES = [false, false, true, true];
const PALABRA = 'FUEGO';

function verdad(f, a) {
  if (f.tipo === 'es') return a[f.j];
  if (f.tipo === 'no es') return !a[f.j];
  return a[f.j] && a[f.k];
}

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 51 — Los consejeros',
    instr: 'Los leales siempre dicen la verdad y los traidores siempre mienten. Con las frases de las cartas 26 y 52, decidid quién es leal y quién traidor tocando cada nombre.',
    ...opts
  });
  texturaSi(ui, 'piedra.jpg', { opacidad: 0.3, mezcla: 'screen' });

  estilo(ui.body, `
    .con-lista{display:grid;gap:8px;max-width:360px;margin:0 auto 6px}
    .con-fila{display:grid;grid-template-columns:52px 1fr 118px;gap:8px;align-items:center;padding:7px 8px;border-radius:10px;background:linear-gradient(#2a323b,#1c232b);border:1px solid rgba(159,184,204,.45)}
    .con-ret{width:46px;height:46px;border-radius:50%;border:2px solid #9fb8cc;background:radial-gradient(circle at 40% 35%,#556270,#242d37);display:flex;align-items:center;justify-content:center;font:800 1.2rem Georgia,serif;color:#eaf4fb}
    .con-ret.img{background:var(--img) center/cover;color:transparent}
    .con-nom{text-align:left;font:700 1rem Georgia,serif;color:#eaf4fb}
    .con-nom small{display:block;font:500 .72rem Poppins,sans-serif;color:#a9bccb}
    .con-btn{min-height:48px;border-radius:10px;border:1px solid rgba(207,232,251,.55);background:rgba(6,10,16,.78);color:#cfe3f2;font:700 .9rem inherit;font-family:inherit;cursor:pointer;touch-action:manipulation}
    .con-btn[data-e="1"]{background:linear-gradient(#2d5a3c,#1c3a27);color:#d6ffe0;border-color:#7dffb0}
    .con-btn[data-e="2"]{background:linear-gradient(#6a2a2a,#401a1a);color:#ffdede;border-color:#ff9d9d}
  `);

  const lista = document.createElement('div');
  lista.className = 'con-lista';
  ui.body.appendChild(lista);

  const est = [0, 0, 0, 0]; // 0 ¿?, 1 leal, 2 traidor
  let resuelto = false;
  const botones = [];
  const ETQ = ['¿Leal o traidor?', 'Leal', 'Traidor'];

  NOMBRES.forEach((n, i) => {
    const f = document.createElement('div');
    f.className = 'con-fila';
    const ret = document.createElement('div');
    ret.className = 'con-ret';
    ret.textContent = n[0];
    ret.setAttribute('aria-hidden', 'true');
    conImagen(ret, 'consejeros/' + n.toLowerCase() + '.jpg');
    const nom = document.createElement('div');
    nom.className = 'con-nom';
    nom.innerHTML = n + '<small>consejero</small>';
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'con-btn';
    b.dataset.i = String(i);
    b.addEventListener('click', () => { if (!resuelto) { est[i] = (est[i] + 1) % 3; ui.say(''); pintar(); } });
    f.append(ret, nom, b);
    lista.appendChild(f);
    botones.push(b);
  });

  function pintar() {
    botones.forEach((b, i) => {
      b.dataset.e = String(est[i]);
      b.textContent = ETQ[est[i]];
      b.setAttribute('aria-label', NOMBRES[i] + ': ' + ['sin decidir', 'leal', 'traidor'][est[i]]);
    });
  }
  pintar();

  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    if (est.includes(0)) { ui.say('Falta decidir a alguno de los consejeros.', 'bad'); return; }
    const a = est.map(e => e === 1);
    const mala = FRASES.findIndex((f, i) => verdad(f, a) !== a[i]);
    if (mala >= 0) {
      ui.say('Algo se contradice: según vuestra decisión, ' + NOMBRES[mala] + ' ' + (a[mala] ? 'es leal pero dice algo falso' : 'es traidor pero dice algo cierto') + ' (« ' + FRASES[mala].txt + ' »). Un leal no puede mentir ni un traidor decir la verdad.', 'bad');
      return;
    }
    resuelto = true;
    guardarPalabra('51', PALABRA);
    ui.say('¡Correcto! Aldric y Brenna quedan al descubierto como traidores. Brenna, del susto, deja caer algo de su capa. Palabra de la profecía: «' + PALABRA + '». Anotadla. Coged la carta 58.', 'ok');
  });

  return { close: ui.close, leales: LEALES };
}
