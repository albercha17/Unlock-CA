// Carta 52 — La dosis: llenar dos jeringuillas (0-15 ml) con la dosis exacta de la tabla de la doctora, leída con el peso y la estatura de la
// báscula y la vara. Se llena manteniendo pulsado (o a toques de 1 ml). Solución en herramientas/instancias_colosos.py (dosis).
import { openGame } from './ui.js';
import { estilo, tono } from './comun.js';

const D = /*DATOS*/{"dosis": {"Cristina": 8, "Alberto": 12}, "marca": "78"}/*FIN*/;
const MAX = 15;

estilo('co-dosis', `
  .co-jers{display:flex;gap:26px;justify-content:center;margin:8px 0}
  .co-jer{display:flex;flex-direction:column;align-items:center;gap:8px}
  .co-tubo{position:relative;width:54px;height:220px;border:3px solid #e8e2d4;border-radius:8px 8px 14px 14px;background:rgba(255,255,255,.08);overflow:hidden}
  .co-tubo .liq{position:absolute;left:0;right:0;bottom:0;background:linear-gradient(180deg,#ffd27a,#e08a1a);box-shadow:0 0 14px rgba(255,180,60,.7);transition:height .15s}
  .co-tubo .gr{position:absolute;left:0;height:2px;background:rgba(255,255,255,.7)}
  .co-tubo .gr.larga{width:60%}.co-tubo .gr.corta{width:30%}
  .co-tubo .num{position:absolute;right:3px;font:700 .62rem system-ui,sans-serif;color:#fff;transform:translateY(50%)}
  .co-aguja{width:3px;height:26px;background:#e8e2d4;margin-top:-8px}
  .co-ml{font:800 1.05rem system-ui,sans-serif;color:#ffd27a}
  .co-llenar{touch-action:none;user-select:none;-webkit-user-select:none}
`);

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 52 — La dosis',
    instr: 'Mantened pulsado «Llenar» para que suba el suero (o tocad para 1 ml). Cada jeringuilla, con la dosis exacta de su persona.',
    ...opts
  });
  const ml = { Cristina: 0, Alberto: 0 };
  const cont = document.createElement('div');
  cont.className = 'co-jers';
  const vistas = {};
  let timer = null;
  const parar = () => { if (timer) { clearInterval(timer); timer = null; } };
  ui.onClose(parar);

  ['Cristina', 'Alberto'].forEach(nombre => {
    const j = document.createElement('div');
    j.className = 'co-jer';
    j.dataset.persona = nombre;
    const titulo = document.createElement('div');
    titulo.className = 'co-ml';
    titulo.textContent = nombre;
    const tubo = document.createElement('div');
    tubo.className = 'co-tubo';
    const liq = document.createElement('div');
    liq.className = 'liq';
    tubo.appendChild(liq);
    for (let k = 0; k <= MAX; k++) {
      const g = document.createElement('div');
      g.className = 'gr ' + (k % 5 === 0 ? 'larga' : 'corta');
      g.style.bottom = (k / MAX * 100) + '%';
      tubo.appendChild(g);
      if (k % 5 === 0) {
        const t = document.createElement('div');
        t.className = 'num';
        t.style.bottom = (k / MAX * 100) + '%';
        t.textContent = k;
        tubo.appendChild(t);
      }
    }
    const aguja = document.createElement('div');
    aguja.className = 'co-aguja';
    const lect = document.createElement('div');
    lect.className = 'co-ml';
    const llenar = document.createElement('button');
    llenar.type = 'button';
    llenar.className = 'co-opc co-llenar';
    llenar.textContent = 'Llenar';
    const sumar = () => {
      if (ml[nombre] >= MAX) { parar(); ui.say('¡La jeringuilla está llena hasta arriba!', ''); return; }
      ml[nombre] += 1;
      tono(300 + ml[nombre] * 30, 0.12, 'triangle', 0.08);
      pintar();
    };
    llenar.addEventListener('pointerdown', e => { e.preventDefault(); parar(); sumar(); timer = setInterval(sumar, 260); });
    ['pointerup', 'pointerleave', 'pointercancel'].forEach(ev => llenar.addEventListener(ev, parar));
    llenar.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); sumar(); } });
    const vaciar = document.createElement('button');
    vaciar.type = 'button';
    vaciar.className = 'co-opc';
    vaciar.textContent = 'Vaciar';
    vaciar.addEventListener('click', () => { ml[nombre] = 0; pintar(); });
    j.append(titulo, tubo, aguja, lect, llenar, vaciar);
    cont.appendChild(j);
    vistas[nombre] = { liq, lect };
  });
  ui.body.append(cont);

  function pintar() {
    Object.keys(vistas).forEach(n => {
      vistas[n].liq.style.height = (ml[n] / MAX * 100) + '%';
      vistas[n].lect.textContent = ml[n] + ' ml';
    });
  }

  ui.button('Inyectar', 'primary', () => {
    parar();
    if (!ml.Cristina || !ml.Alberto) { ui.say('Las dos jeringuillas tienen que llevar suero.', ''); return; }
    if (ml.Cristina === D.dosis.Cristina && ml.Alberto === D.dosis.Alberto) {
      ui.say('«Exacto, ni una gota de más», dice la doctora, y os da las jeringuillas. Marca de la dosis: ' + D.marca + '. Coged la carta 44.', 'ok');
      cont.querySelectorAll('button').forEach(b => { b.disabled = true; });
    } else {
      ui.say('La doctora os quita las jeringuillas a tiempo: «¡Esa dosis no! Volved a mirar la tabla».', 'bad');
      ml.Cristina = 0;
      ml.Alberto = 0;
      pintar();
    }
  });
  pintar();
  return { close: ui.close };
}
