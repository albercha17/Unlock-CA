// Carta 51 — Estratos: ordenar seis capas de roca de abajo arriba con el croquis (carta 26) y el cuaderno de capas (carta 52).
// Solución de arriba abajo: ceniza, carbón, arenisca, arcilla, caliza, conchas.
import { openGame } from './ui.js';

const NOMBRES = {
  ceniza: 'Ceniza volcánica', carbon: 'Carbón', arenisca: 'Arenisca roja',
  arcilla: 'Arcilla verde', caliza: 'Caliza', conchas: 'Arena con conchas'
};
const SOLUCION = ['ceniza', 'carbon', 'arenisca', 'arcilla', 'caliza', 'conchas'];     // de arriba abajo
const INICIAL = ['arcilla', 'conchas', 'ceniza', 'arenisca', 'caliza', 'carbon'];

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 51 — Estratos',
    instr: 'Toca dos capas para intercambiarlas. Ordénalas como estaban en el barranco: la más reciente arriba y la más antigua abajo.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .est-corte{position:relative;max-width:340px;margin:0 auto 10px;padding:8px 8px 8px 34px;border-radius:10px;border:3px solid #4a3418;background:#1a1208;box-shadow:inset 0 0 20px rgba(0,0,0,.7)}
    .est-eje{position:absolute;left:4px;top:8px;bottom:8px;width:24px;display:flex;flex-direction:column;justify-content:space-between;align-items:center;font-size:.58rem;color:#d8c9a0;letter-spacing:.06em;text-transform:uppercase;writing-mode:vertical-rl;transform:rotate(180deg)}
    .est-capa{position:relative;display:block;width:100%;height:50px;margin-bottom:3px;padding:0;border:2px solid rgba(0,0,0,.55);border-radius:6px;overflow:hidden;cursor:pointer;background-size:cover;background-position:center;color:#fff;font:700 .9rem Georgia,serif;text-shadow:0 1px 4px #000,0 0 8px #000;transition:transform .15s,box-shadow .15s,filter .15s}
    .est-capa:last-child{margin-bottom:0}
    .est-capa span{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:linear-gradient(90deg,rgba(0,0,0,.35),rgba(0,0,0,.05) 50%,rgba(0,0,0,.35))}
    .est-capa.sel{transform:scale(1.03);box-shadow:0 0 0 3px #ffd27a,0 0 18px rgba(255,210,122,.7);z-index:2}
    .est-capa.ok{filter:brightness(1.1) saturate(1.1)}
  `;
  ui.body.appendChild(style);

  const corte = document.createElement('div');
  corte.className = 'est-corte';
  corte.innerHTML = '<div class="est-eje"><span>más reciente</span><span>más antigua</span></div>';
  const pila = document.createElement('div');
  corte.appendChild(pila);
  ui.body.appendChild(corte);

  let orden = INICIAL.slice();
  let sel = null;
  let resuelto = false;

  function pintar() {
    pila.innerHTML = '';
    orden.forEach((k, i) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'est-capa' + (sel === i ? ' sel' : '');
      b.dataset.n = k;
      b.dataset.pos = String(i);
      b.style.backgroundImage = 'url(./img/ui/capas/' + k + '.jpg)';
      b.setAttribute('aria-label', 'Capa ' + NOMBRES[k]);
      b.innerHTML = '<span>' + NOMBRES[k] + '</span>';
      b.addEventListener('click', () => {
        if (resuelto) return;
        if (sel === null) { sel = i; }
        else if (sel === i) { sel = null; }
        else {
          [orden[sel], orden[i]] = [orden[i], orden[sel]];
          sel = null;
          ui.say('');
        }
        pintar();
      });
      pila.appendChild(b);
    });
  }

  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    if (orden.every((k, i) => k === SOLUCION[i])) {
      resuelto = true;
      pila.querySelectorAll('.est-capa').forEach(b => b.classList.add('ok'));
      ui.say('¡Las capas encajan con el corte del barranco! La cruz de Ibarra señala un hueco en la roca: ahí escondió su último equipo. Coged la carta 58.', 'ok');
    } else {
      ui.say('El orden no coincide con lo que dicen los dos documentos. Releed las frases sobre las capas.', 'bad');
    }
  });

  pintar();
  return { close: ui.close };
}
