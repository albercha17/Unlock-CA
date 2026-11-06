// Carta 72 — Las palancas de la torre: memoria por etapas. En cada una de las cinco etapas la esfera marca un número (1-4) y las cuatro palancas
// llevan dibujos en otro orden; las placas dicen de cuál tirar (por sitio, por dibujo o «la misma que en la etapa N»). Al fallar, todo cambia
// y se vuelve a la etapa 1. Reglas en herramientas/instancias_colosos.py (palancas).
import { openGame } from './ui.js';
import { estilo, tono } from './comun.js';

const D = /*DATOS*/{"simbolos": ["campana", "llave", "luna", "rueda"], "reglas": [[["sim", "llave"], ["pos", 2], ["sim", "rueda"], ["pos", 3]], [["igual_pos", 0], ["igual_sim", 0], ["pos", 2], ["igual_pos", 0]], [["pos", 0], ["sim", "campana"], ["pos", 0], ["sim", "luna"]], [["pos", 2], ["igual_pos", 0], ["pos", 3], ["igual_pos", 1]], [["sim", "campana"], ["igual_pos", 1], ["sim", "llave"], ["pos", 2]]]}/*FIN*/;
const EMO = { campana: '🔔', llave: '🗝️', luna: '🌙', rueda: '⚙️' };

estilo('co-pal', `
  .co-esfera{width:110px;height:110px;margin:4px auto 10px;border-radius:50%;border:6px solid #8a6a3a;background:radial-gradient(circle,#fff6e4,#d8c8a0);
    display:flex;align-items:center;justify-content:center;font:800 3rem 'Cinzel',Georgia,serif;color:#3a2410;box-shadow:0 0 18px rgba(255,190,90,.4)}
  .co-palancas{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;max-width:340px;margin:0 auto}
  .co-palanca{display:flex;flex-direction:column;align-items:center;gap:4px;padding:10px 4px;border-radius:10px;border:1.5px solid #e0a640;
    background:linear-gradient(180deg,#5a4630,#2e2216);color:#fff6e4;font:700 .85rem system-ui,sans-serif;cursor:pointer}
  .co-palanca .emo{font-size:1.8rem}
  .co-palanca .barra{width:10px;height:44px;border-radius:5px;background:linear-gradient(180deg,#d0d0d0,#6a6a6a);transform-origin:bottom;transition:transform .25s}
  .co-palanca.tirada .barra{transform:rotate(35deg)}
  .co-etapas{display:flex;gap:6px;justify-content:center;margin:8px 0}
  .co-etapas span{width:14px;height:14px;border-radius:50%;border:2px solid #e0a640}
  .co-etapas span.hecha{background:#e0a640}
`);

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 72 — Las palancas de la torre',
    instr: 'Mirad el número de la esfera y tirad de la palanca que dicen las placas. Son cinco etapas; si falláis, la maquinaria vuelve a empezar.',
    ...opts
  });
  let etapa = 0, esfera = 1, orden = [];
  const hist = [];          // [{pos, sim}]
  const etapas = document.createElement('div');
  etapas.className = 'co-etapas';
  for (let k = 0; k < 5; k++) etapas.appendChild(document.createElement('span'));
  const esf = document.createElement('div');
  esf.className = 'co-esfera';
  esf.id = 'coEsfera';
  const pal = document.createElement('div');
  pal.className = 'co-palancas';
  ui.body.append(etapas, esf, pal);

  const azar = n => Math.floor(Math.random() * n);
  function nuevaEtapa() {
    esfera = 1 + azar(4);
    orden = D.simbolos.slice();
    for (let i = orden.length - 1; i > 0; i--) { const j = azar(i + 1); [orden[i], orden[j]] = [orden[j], orden[i]]; }
    pintar();
  }
  function correcta() {
    const [t, x] = D.reglas[etapa][esfera - 1];
    if (t === 'pos') return x;
    if (t === 'sim') return orden.indexOf(x);
    if (t === 'igual_pos') return hist[x].pos;
    return orden.indexOf(hist[x].sim);
  }
  function tirar(p, b) {
    b.classList.add('tirada');
    tono(110, 0.3, 'sawtooth', 0.12);
    if (p !== correcta()) {
      ui.say('¡Clonc! Los engranajes se atascan y la maquinaria vuelve a la primera etapa.', 'bad');
      etapa = 0;
      hist.length = 0;
      setTimeout(nuevaEtapa, 600);
      return;
    }
    hist.push({ pos: p, sim: orden[p] });
    etapa += 1;
    if (etapa === 5) {
      ui.say('Los engranajes giran con un rugido y la puerta de la Torre del Reloj se abre de par en par. Coged la carta 82.', 'ok');
      pintar();
      pal.querySelectorAll('button').forEach(x => { x.disabled = true; });
      return;
    }
    ui.say('¡Clac! La etapa ' + etapa + ' encaja.', '');
    setTimeout(nuevaEtapa, 450);
  }
  function pintar() {
    [...etapas.children].forEach((s, k) => s.classList.toggle('hecha', k < etapa));
    esf.textContent = etapa < 5 ? String(esfera) : '✿';
    pal.innerHTML = '';
    orden.forEach((s, p) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'co-palanca';
      b.dataset.pos = p;
      b.dataset.sim = s;
      b.innerHTML = `<span class="emo">${EMO[s]}</span><span class="barra"></span><span>${s}</span>`;
      b.addEventListener('click', () => tirar(p, b));
      pal.appendChild(b);
    });
  }
  nuevaEtapa();
  return { close: ui.close };
}
