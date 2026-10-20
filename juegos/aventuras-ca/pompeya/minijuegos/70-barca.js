// Carta 70 — La barca: cargar lo más valioso sin pasar del peso que aguanta (manifiesto 71, barquero 72, Lucrecia 76). Óptimo único.
import { openGame } from './ui.js';

const D = /*DATOS*/{"carga": {"anfora_aceite": [4, 9], "anfora_vino": [3, 6], "fardo_lana": [2, 3], "cofre_monedas": [5, 11], "estatua_lar": [1, 4], "saco_trigo": [3, 5]}, "maximo": 9, "solucion": ["anfora_vino", "cofre_monedas", "estatua_lar"]}/*FIN*/;
const NOM = { anfora_aceite: 'ánfora de aceite', anfora_vino: 'ánfora de vino', fardo_lana: 'fardo de lana', cofre_monedas: 'cofre de monedas', estatua_lar: 'estatua del lar', saco_trigo: 'saco de trigo' };

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 70 — La barca', instr: 'Tocad lo que subís a la barca (otra vez para bajarlo) y pulsad «Zarpar». Lucrecia quiere lo que más vale, y el barquero, no hundirse.', ...opts });
  const style = document.createElement('style');
  style.textContent = `
    .pom-muelle{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;max-width:320px;margin:6px auto}
    .pom-bulto{border-radius:10px;border:2px solid #8a6a3a;background:#3a2a1a center 30% / 60% no-repeat;cursor:pointer;padding:62px 4px 6px;color:#f6e4b8;font:600 .68rem system-ui}
    .pom-bulto.dentro{background-color:#2a4a6a;border-color:#7ec8e8}`;
  ui.body.appendChild(style);
  const m = document.createElement('div'); m.className = 'pom-muelle'; ui.body.appendChild(m);
  const dentro = new Set();
  let resuelto = false;
  Object.keys(D.carga).forEach(k => {
    const b = document.createElement('button'); b.type = 'button'; b.className = 'pom-bulto'; b.dataset.k = k;
    b.style.backgroundImage = "url('./img/ui/carga-" + k + ".png')"; b.textContent = NOM[k];
    b.addEventListener('click', () => { if (resuelto) return; dentro.has(k) ? dentro.delete(k) : dentro.add(k); b.classList.toggle('dentro', dentro.has(k)); ui.say(''); });
    m.appendChild(b);
  });
  ui.button('Zarpar', 'primary', () => {
    if (resuelto) return;
    const peso = [...dentro].reduce((s, k) => s + D.carga[k][0], 0);
    if (peso > D.maximo) { ui.say('¡La barca hace agua y empieza a hundirse! Tenéis que descargar (carta 72).', 'bad'); return; }
    if (D.solucion.length === dentro.size && D.solucion.every(k => dentro.has(k))) { resuelto = true; ui.say('La barca flota justa y lleva lo que más vale. Lucrecia sonríe por primera vez en todo el día. Coged la carta 82.', 'ok'); }
    else ui.say('La barca flota, pero Lucrecia protesta: «¡Con ese peso podríais llevar algo que valga más!» (cartas 71 y 76).', 'bad');
  });
  return { close: ui.close };
}
