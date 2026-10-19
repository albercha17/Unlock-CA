// Carta 48 — La persecución: llevar La Gaviota al banco de niebla sin que la alcance la fragata, que da dos pasos por cada uno vuestro
// con la regla de la ordenanza (carta 52): primero se acerca en horizontal; si no puede, en vertical; si no, se queda (como el Minotauro).
// Instancia de herramientas/instancias_piratas.py (BFS: 13 turnos como mínimo; ir directo son 6 y la fragata os apresa).
import { openGame } from './ui.js';

const P = /*DATOS*/{"ancho": 6, "alto": 6, "rocas": [[0, 3], [2, 0], [3, 0], [3, 3], [4, 2], [4, 4]], "barco": [4, 5], "fragata": [4, 0], "niebla": [5, 0]}/*FIN*/;
const MOV = { arriba: [0, -1], abajo: [0, 1], izquierda: [-1, 0], derecha: [1, 0], esperar: [0, 0] };
const k = c => c[0] + ',' + c[1];

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 48 — La persecución',
    instr: 'Llevad La Gaviota (marco dorado) al banco de niebla blanco; la fragata va con marco rojo. Por cada casilla que avanzáis (o cada turno que esperáis), la fragata da dos pasos según la ordenanza de la Armada. Si os alcanza, os apresa.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .pir-mar{display:grid;grid-template-columns:repeat(${P.ancho},1fr);gap:2px;width:min(86vw,312px);margin:4px auto 8px;padding:4px;border-radius:8px;background:#0c3440;border:3px solid #e8b84a}
    .pir-casilla{position:relative;aspect-ratio:1;border-radius:3px;background:linear-gradient(160deg,#3a8aa0,#22647a)}
    .pir-casilla.roca{background:radial-gradient(circle at 40% 35%,#9a8a7a,#5a4c40 55%,#2a2018 75%),#22647a}
    .pir-casilla.niebla{background:radial-gradient(circle,#f4f8fa,#c8d8de 60%,#8aaab4)}
    .pir-casilla img{position:absolute;inset:4%;width:92%;height:92%;object-fit:contain;transition:transform .25s}
    .pir-casilla.con-fragata{box-shadow:inset 0 0 0 3px #e0443a;background:linear-gradient(160deg,#6a3a3a,#3a2026)}
    .pir-casilla.con-fragata img{filter:brightness(.8) contrast(1.2) drop-shadow(0 0 4px #ff5040)}
    .pir-casilla.con-gaviota{box-shadow:inset 0 0 0 3px #e8b84a}
    .pir-casilla.huella::before{content:'';position:absolute;inset:40%;border-radius:50%;background:rgba(255,255,255,.35)}
    .pir-mar.ok{border-color:#7be495;box-shadow:0 0 24px rgba(123,228,149,.6)}
    .pir-timon{display:grid;grid-template-columns:repeat(3,56px);grid-template-rows:repeat(2,48px);gap:6px;justify-content:center;margin:0 auto 6px}
    .pir-timon button{border-radius:10px;border:2px solid #e8b84a;background:#173a46;color:#f6e7b8;font:700 1.2rem system-ui,sans-serif;cursor:pointer}
    .pir-timon [data-d=arriba]{grid-column:2;grid-row:1}.pir-timon [data-d=izquierda]{grid-column:1;grid-row:2}
    .pir-timon [data-d=abajo]{grid-column:2;grid-row:2}.pir-timon [data-d=derecha]{grid-column:3;grid-row:2}
    .pir-timon [data-d=esperar]{grid-column:3;grid-row:1;font-size:.72rem}
  `;
  ui.body.appendChild(style);

  const mar = document.createElement('div');
  mar.className = 'pir-mar';
  const mando = document.createElement('div');
  mando.className = 'pir-timon';
  ui.body.appendChild(mar);
  ui.body.appendChild(mando);

  const rocas = new Set(P.rocas.map(k));
  const libre = c => c[0] >= 0 && c[1] >= 0 && c[0] < P.ancho && c[1] < P.alto && !rocas.has(k(c));
  let barco, fragata, historia, estela, resuelto = false;

  function reiniciar() {
    barco = P.barco.slice();
    fragata = P.fragata.slice();
    historia = [];
    estela = new Set();
  }

  // un paso de la fragata: horizontal si se acerca; si no, vertical; si no, quieta
  function pasoFragata() {
    if (barco[0] !== fragata[0]) {
      const c = [fragata[0] + (barco[0] > fragata[0] ? 1 : -1), fragata[1]];
      if (libre(c)) { fragata = c; return; }
    }
    if (barco[1] !== fragata[1]) {
      const c = [fragata[0], fragata[1] + (barco[1] > fragata[1] ? 1 : -1)];
      if (libre(c)) fragata = c;
    }
  }

  function pintar() {
    mar.className = 'pir-mar' + (resuelto ? ' ok' : '');
    mar.innerHTML = '';
    for (let y = 0; y < P.alto; y++) {
      for (let x = 0; x < P.ancho; x++) {
        const d = document.createElement('div');
        const id = k([x, y]);
        d.className = 'pir-casilla' + (rocas.has(id) ? ' roca' : '') + (k(P.niebla) === id ? ' niebla' : '') + (estela.has(id) ? ' huella' : '');
        d.dataset.x = String(x);
        d.dataset.y = String(y);
        if (k(barco) === id) { d.classList.add('con-gaviota'); d.innerHTML = '<img src="./img/ui/gaviota.png" alt="La Gaviota">'; }
        else if (k(fragata) === id) { d.classList.add('con-fragata'); d.innerHTML = '<img src="./img/ui/fragata.png" alt="La fragata">'; }
        mar.appendChild(d);
      }
    }
    mar.dataset.barco = k(barco);
    mar.dataset.fragata = k(fragata);
  }

  function mover(dir) {
    if (resuelto) return;
    const [dx, dy] = MOV[dir];
    const nb = [barco[0] + dx, barco[1] + dy];
    if (!libre(nb)) { ui.say('Por ahí hay rocas o se acaba la carta: La Gaviota no puede ir.', 'bad'); return; }
    if (k(nb) === k(fragata)) { ui.say('¡Eso es meterse en la boca del lobo! No os acerquéis a la fragata.', 'bad'); return; }
    historia.push({ barco: barco.slice(), fragata: fragata.slice(), estela: new Set(estela) });
    estela.add(k(barco));
    barco = nb;
    if (k(barco) === k(P.niebla)) {
      resuelto = true;
      pintar();
      ui.say('¡La Gaviota se mete en el banco de niebla y la fragata pasa de largo, perdida! La capitana Bruma suelta una carcajada: «¡Tierra a la vista!». Coged la carta 58.', 'ok');
      return;
    }
    for (let i = 0; i < 2; i++) {
      pasoFragata();
      if (k(fragata) === k(barco)) {
        pintar();
        ui.say('¡La fragata os da alcance y os apresa! Volvéis a empezar. Pensad cómo se mueve (carta 52): a veces conviene esperar a que una roca la frene.', 'bad');
        reiniciar();
        setTimeout(pintar, 900);
        return;
      }
    }
    ui.say(dir === 'esperar' ? 'Esperáis al pairo. La fragata se mueve.' : '');
    pintar();
  }

  Object.keys(MOV).forEach(d => {
    const b = document.createElement('button');
    b.type = 'button';
    b.dataset.d = d;
    b.textContent = { arriba: '▲', abajo: '▼', izquierda: '◀', derecha: '▶', esperar: 'Esperar' }[d];
    b.setAttribute('aria-label', d === 'esperar' ? 'Esperar un turno' : 'Navegar hacia ' + d);
    b.addEventListener('click', () => mover(d));
    mando.appendChild(b);
  });

  ui.button('Deshacer', '', () => {
    if (resuelto || !historia.length) return;
    const h = historia.pop();
    barco = h.barco; fragata = h.fragata; estela = h.estela;
    ui.say('');
    pintar();
  });
  ui.button('Empezar de nuevo', '', () => { if (!resuelto) { reiniciar(); ui.say(''); pintar(); } });

  reiniciar();
  pintar();
  return { close: ui.close };
}
