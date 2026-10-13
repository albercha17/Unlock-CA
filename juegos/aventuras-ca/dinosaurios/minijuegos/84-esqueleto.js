// Carta 84 — El esqueleto: encadenar los huesos del tiranosaurio como un dominó. Las marcas de las articulaciones que se tocan deben ser iguales
// (notas de montaje, carta 86). El cráneo (2 marcas) va primero; la punta de la cola (sin marcas a la derecha) va la última. Dos piezas sobran.
// Solución: cuello (2-4), torso (4-1), cadera (1-3), cola (3-2) y punta (2).
import { openGame } from './ui.js';

const IMG = './img/ui/huesos/';
const PIEZAS = {
  cuello: [2, 4], torso: [4, 1], cadera: [1, 3], cola: [3, 2], punta: [2, 0],
  intruso1: [4, 4], intruso2: [4, 2]
};
const CRANEO = [0, 2];
const BANDEJA = ['cadera', 'intruso2', 'punta', 'torso', 'intruso1', 'cuello', 'cola'];
const NOMBRES = {
  cuello: 'Vértebras del cuello', torso: 'Caja torácica', cadera: 'Cadera', cola: 'Vértebras de la cola', punta: 'Punta de la cola',
  intruso1: 'Fémur grueso', intruso2: 'Costilla suelta'
};

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 84 — El esqueleto',
    instr: 'Toca los huesos de la bandeja para colocarlos tras el cráneo. Toca uno colocado para devolverlo. Las marcas que se tocan deben ser iguales.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .esq-suelo{max-width:350px;margin:0 auto 8px;padding:8px;border-radius:12px;border:3px solid #4a3418;background:linear-gradient(rgba(20,12,4,.45),rgba(20,12,4,.7)),url(./img/ui/suelo-limpio.jpg) center/cover;box-shadow:inset 0 0 24px rgba(0,0,0,.75)}
    .esq-cadena{display:flex;flex-direction:column;gap:3px;margin-bottom:6px}
    .esq-fila{display:flex;align-items:center;gap:6px;min-height:36px;padding:2px 6px;border-radius:8px;background:rgba(0,0,0,.35);border:1px dashed rgba(255,235,170,.25);color:#cdbf9a;font-size:.75rem}
    .esq-fila.ocupada{border-style:solid;border-color:rgba(255,235,170,.4)}
    .esq-hueso{display:flex;align-items:center;gap:6px;width:100%;padding:0;border:0;background:none;cursor:pointer;color:inherit}
    .esq-hueso img{flex:1;min-width:0;height:34px;object-fit:contain;mix-blend-mode:screen;filter:drop-shadow(0 2px 3px rgba(0,0,0,.6))}
    .esq-marcas{display:grid;grid-template-columns:repeat(2,9px);gap:2px;width:22px;min-height:22px;align-content:center;justify-content:center}
    .esq-marcas i{display:block;width:9px;height:9px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff3c0,#e0a020);box-shadow:0 0 5px rgba(255,200,80,.8)}
    .esq-bandeja{display:grid;grid-template-columns:repeat(2,1fr);gap:6px}
    .esq-bandeja .esq-hueso{padding:2px 4px;border-radius:8px;background:rgba(0,0,0,.4);border:1px solid rgba(255,235,170,.25)}
    .esq-bandeja .esq-hueso img{height:28px}
    .esq-bandeja .esq-hueso.usada{opacity:.25;cursor:default}
    .esq-titulo{font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;color:#e6d9b0;text-align:left;margin:2px 0 4px}
  `;
  ui.body.appendChild(style);

  const suelo = document.createElement('div');
  suelo.className = 'esq-suelo';
  suelo.innerHTML = '<div class="esq-titulo">Esqueleto (del cráneo a la cola)</div><div class="esq-cadena"></div><div class="esq-titulo">Huesos sueltos</div><div class="esq-bandeja"></div>';
  ui.body.appendChild(suelo);
  const cadenaEl = suelo.querySelector('.esq-cadena');
  const bandejaEl = suelo.querySelector('.esq-bandeja');

  let cadena = [];
  let resuelto = false;

  function marcas(n) {
    const d = document.createElement('span');
    d.className = 'esq-marcas';
    d.dataset.n = String(n);
    for (let i = 0; i < n; i++) d.appendChild(document.createElement('i'));
    return d;
  }

  function hueso(nombre, pieza, extra) {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'esq-hueso' + (extra || '');
    b.dataset.n = nombre;
    b.setAttribute('aria-label', NOMBRES[nombre] || 'Cráneo');
    b.append(marcas(pieza[0]));
    const im = document.createElement('img');
    im.alt = NOMBRES[nombre] || 'Cráneo';
    im.src = IMG + nombre + '.jpg';
    b.appendChild(im);
    b.append(marcas(pieza[1]));
    return b;
  }

  function pintar() {
    cadenaEl.innerHTML = '';
    const f0 = document.createElement('div');
    f0.className = 'esq-fila ocupada';
    const c = hueso('craneo', CRANEO);
    c.disabled = true;
    c.style.cursor = 'default';
    f0.appendChild(c);
    cadenaEl.appendChild(f0);
    for (let i = 0; i < 5; i++) {
      const f = document.createElement('div');
      f.className = 'esq-fila' + (cadena[i] ? ' ocupada' : '');
      f.dataset.i = String(i);
      if (cadena[i]) {
        const h = hueso(cadena[i], PIEZAS[cadena[i]]);
        h.addEventListener('click', () => { if (!resuelto) { cadena.splice(i, 1); ui.say(''); pintar(); } });
        f.appendChild(h);
      } else {
        f.textContent = 'hueco ' + (i + 1);
      }
      cadenaEl.appendChild(f);
    }
    bandejaEl.innerHTML = '';
    BANDEJA.forEach(n => {
      const usada = cadena.includes(n);
      const h = hueso(n, PIEZAS[n], usada ? ' usada' : '');
      h.disabled = usada;
      h.addEventListener('click', () => {
        if (resuelto || usada || cadena.length >= 5) return;
        cadena.push(n);
        ui.say('');
        pintar();
      });
      bandejaEl.appendChild(h);
    });
  }

  ui.button('Vaciar', 'ghost', () => { if (!resuelto) { cadena = []; ui.say(''); pintar(); } });
  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    if (cadena.length < 5) { ui.say('Faltan huesos por colocar: el esqueleto tiene cinco piezas tras el cráneo.', 'bad'); return; }
    let ok = PIEZAS[cadena[0]][0] === CRANEO[1];
    for (let i = 1; i < cadena.length; i++) ok = ok && PIEZAS[cadena[i - 1]][1] === PIEZAS[cadena[i]][0];
    ok = ok && PIEZAS[cadena[4]][1] === 0;
    if (ok) {
      resuelto = true;
      cadenaEl.querySelectorAll('button').forEach(b => { b.style.cursor = 'default'; });
      ui.say('¡Las articulaciones encajan una a una! El esqueleto del tiranosaurio se alza como una antena gigante y el Cronoportal vibra de energía. Coged la carta 99.', 'ok');
    } else {
      ui.say('Alguna articulación no encaja: las marcas que se tocan no son iguales, o falta la punta de la cola al final.', 'bad');
    }
  });

  pintar();
  return { close: ui.close };
}
