// Carta 66 — Ornitóptero: elegir ala, tela y lastre. Las tres notas (cartas 68, 70 y 71) descartan combinaciones.
// Solución única: ala LARGA, tela de SEDA, lastre de 2 sacos.
//   68: ala corta no levanta · con ala media siempre 2 sacos · ala larga no admite 3 sacos
//   70: con un solo saco cae de lado
//   71: 2 sacos + cuero vuelca · lino + 2 sacos se arruga · ala media + seda sin fuerza
import { openGame } from './ui.js';

const IMG = './img/ui/';
const GRUPOS = [
  { id: 'ala', titulo: 'Ala', opciones: [['corta', 'Corta'], ['media', 'Media'], ['larga', 'Larga']] },
  { id: 'tela', titulo: 'Tela', opciones: [['lino', 'Lino'], ['seda', 'Seda'], ['cuero', 'Cuero']] },
  { id: 'lastre', titulo: 'Lastre', opciones: [['1', '1 saco'], ['2', '2 sacos'], ['3', '3 sacos']] }
];
const SOLUCION = { ala: 'larga', tela: 'seda', lastre: '2' };
// anchura del ala en la escena (% del ancho) y tinte de cada tela sobre el ala de tela natural
const ENVERGADURA = { corta: 58, media: 78, larga: 98 };
const TINTE = {
  lino: 'sepia(.15) brightness(1)',
  seda: 'sepia(1) saturate(5) hue-rotate(-38deg) brightness(.95)',
  cuero: 'sepia(1) saturate(1.4) brightness(.5)'
};

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 66 — Ornitóptero',
    instr: 'Prepara el ornitóptero con ala, tela y lastre según las notas de Leonardo y Salaì. Solo una combinación vuela.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .far-o-esc{position:relative;aspect-ratio:2/1;overflow:hidden;background:linear-gradient(180deg,rgba(29,42,58,.78),rgba(58,42,28,.86) 80%),url(./img/ui/suelo.jpg) center/cover;border:2px solid #6b4a1e;border-radius:12px;margin-bottom:10px}
    .far-o-esc::after{content:"";position:absolute;left:0;right:0;bottom:0;height:13%;background:linear-gradient(180deg,rgba(20,12,4,.2),rgba(20,12,4,.85))}
    .far-o-luc{position:absolute;right:4%;top:4%;width:17%;mix-blend-mode:screen;filter:brightness(.55);transition:filter .8s}
    .far-o-esc.abierto .far-o-luc{filter:brightness(1.3) drop-shadow(0 0 14px rgba(255,220,130,.9))}
    .far-o-ave{position:absolute;left:50%;bottom:11%;width:100%;display:flex;flex-direction:column;align-items:center;mix-blend-mode:screen;transform:translateX(-50%);transition:transform 1.2s ease-in,opacity .3s;z-index:2}
    .far-o-ave.vuela{transform:translate(calc(-50% + 22%),-52%) rotate(-8deg)}
    .far-o-ave.cae{transform:translate(calc(-50% + 4%),14%) rotate(24deg)}
    .far-o-ala{display:block;height:auto;transition:width .3s,filter .3s}
    .far-o-sacos{display:flex;gap:4px;justify-content:center;margin-top:-6%;min-height:22px}
    .far-o-sacos img{width:22px;height:auto;display:block}
    .far-o-grupo{display:flex;align-items:center;gap:8px;margin-bottom:8px}
    .far-o-grupo b{width:58px;color:#ffd27a;font-size:.9rem}
    .far-o-opts{display:flex;gap:6px;flex:1}
    .far-o-opt{flex:1;padding:9px 4px;border-radius:9px;border:2px solid rgba(255,255,255,.14);background:rgba(255,255,255,.06);color:#fff;font-weight:700;font-size:.88rem;cursor:pointer;font-family:inherit}
    .far-o-opt.sel{border-color:#ffd27a;background:rgba(255,210,122,.18);color:#ffd27a}
    .far-o-intentos{color:#9fb4c8;font-size:.82rem;text-align:center;margin:4px 0}
  `;
  ui.body.appendChild(style);

  const esc = document.createElement('div');
  esc.className = 'far-o-esc';
  esc.innerHTML = '<img class="far-o-luc" alt="" src="' + IMG + 'taller/claraboya.jpg">';
  const ave = document.createElement('div');
  ave.className = 'far-o-ave';
  const ala = document.createElement('img');
  ala.className = 'far-o-ala';
  ala.alt = '';
  const sacosEl = document.createElement('div');
  sacosEl.className = 'far-o-sacos';
  ave.append(ala, sacosEl);
  esc.appendChild(ave);
  const grupos = document.createElement('div');
  const intentosEl = document.createElement('div');
  intentosEl.className = 'far-o-intentos';
  ui.body.append(esc, grupos, intentosEl);

  const eleccion = { ala: null, tela: null, lastre: null };
  let intentos = 0;
  let resuelto = false;
  let estadoVuelo = '';

  function pintarAve() {
    const tamano = eleccion.ala || 'media';
    ala.src = IMG + 'ornitoptero/' + ({ corta: 'corto', media: 'medio', larga: 'largo' })[tamano] + '.jpg';
    ala.style.width = ENVERGADURA[tamano] + '%';
    ala.style.filter = TINTE[eleccion.tela] || 'grayscale(.5) brightness(.85)';
    ala.style.opacity = eleccion.ala ? '1' : '.6';
    ave.className = 'far-o-ave ' + estadoVuelo;
    ave.dataset.estado = estadoVuelo;
    esc.classList.toggle('abierto', estadoVuelo === 'vuela');
    sacosEl.innerHTML = '';
    for (let i = 0; i < (Number(eleccion.lastre) || 0); i++) {
      const s = document.createElement('img');
      s.alt = '';
      s.src = IMG + 'saco.jpg';
      sacosEl.appendChild(s);
    }
  }

  function pintarGrupos() {
    grupos.innerHTML = '';
    GRUPOS.forEach(g => {
      const fila = document.createElement('div');
      fila.className = 'far-o-grupo';
      const t = document.createElement('b');
      t.textContent = g.titulo;
      const opts = document.createElement('div');
      opts.className = 'far-o-opts';
      g.opciones.forEach(([v, txt]) => {
        const b = document.createElement('button');
        b.type = 'button';
        b.className = 'far-o-opt' + (eleccion[g.id] === v ? ' sel' : '');
        b.dataset.g = g.id;
        b.dataset.v = v;
        b.textContent = txt;
        b.addEventListener('click', () => {
          if (resuelto) return;
          eleccion[g.id] = v;
          estadoVuelo = '';
          ui.say('');
          pintarGrupos();
          pintarAve();
        });
        opts.appendChild(b);
      });
      fila.append(t, opts);
      grupos.appendChild(fila);
    });
    intentosEl.textContent = 'Intentos de vuelo: ' + intentos;
  }

  const vuela = () => GRUPOS.every(g => eleccion[g.id] === SOLUCION[g.id]);

  ui.button('Probar vuelo', 'primary', () => {
    if (resuelto) return;
    if (!eleccion.ala || !eleccion.tela || !eleccion.lastre) { ui.say('Elige un ala, una tela y un lastre antes de probar.', 'bad'); return; }
    intentos++;
    if (vuela()) {
      resuelto = true;
      estadoVuelo = 'vuela';
      pintarAve();
      pintarGrupos();
      ui.say('¡Vuela! El ornitóptero se eleva por la rampa y su ala golpea la palanca: el lucernario del tejado se abre y entra el primer rayo del amanecer. Coged la carta 90.', 'ok');
    } else {
      estadoVuelo = 'cae';
      pintarAve();
      pintarGrupos();
      ui.say('El ornitóptero no consigue despegar y se desploma. Releed las tres notas: cada frase descarta combinaciones.', 'bad');
    }
  });

  pintarGrupos();
  pintarAve();
  return { close: ui.close };
}
