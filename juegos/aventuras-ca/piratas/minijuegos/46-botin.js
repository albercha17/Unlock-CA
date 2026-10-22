// Carta 46 — El reparto del botín: siete piratas por orden de antigüedad (carta 37), el Código de la Hermandad (carta 39) y el botín (carta 33). El capitán
// propone un reparto y todos votan. Hay que proponer el reparto que se aprueba y en el que el capitán se queda con lo máximo (instancias_piratas.py, BOTIN).
import { openGame } from './ui.js';
import { estilo } from './comun.js';

const D = /*DATOS*/{"piratas": 7, "monedas": 120, "solucion": [117, 0, 1, 0, 1, 0, 1], "necesarios": 4, "previo": [118, 0, 1, 0, 1, 0]}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 46 — El reparto del botín', instr: 'Escribid cuántos doblones da el capitán a cada pirata (el 1 es él mismo) para que el reparto se apruebe y el capitán se quede con lo máximo. La tripulación está en la carta 37, el Código en la 39 y el botín, en la 33.', ...opts });
  estilo('pi-bot', '.bot-f{display:flex;align-items:center;gap:8px;max-width:340px;margin:4px auto}.bot-f label{min-width:92px;color:#e8b84a;font:800 .9rem system-ui,sans-serif}.bot-f input{flex:1;min-height:40px;border-radius:8px;border:2px solid #e8b84a;background:#f6e7b8;color:#10242c;font:700 1.1rem system-ui,sans-serif;padding:0 10px}');
  let resuelto = false;
  const campos = Array.from({ length: D.piratas }, (_, i) => {
    const f = document.createElement('div');
    f.className = 'bot-f';
    const l = document.createElement('label');
    l.textContent = i === 0 ? 'Pirata 1 (capitán)' : 'Pirata ' + (i + 1);
    const inp = document.createElement('input');
    inp.type = 'number';
    inp.min = '0';
    inp.max = String(D.monedas);
    inp.value = '0';
    inp.dataset.i = String(i);
    inp.setAttribute('aria-label', 'Doblones para el pirata ' + (i + 1));
    f.append(l, inp);
    ui.body.appendChild(f);
    return inp;
  });
  const suma = document.createElement('div');
  suma.className = 'pi-pie';
  ui.body.appendChild(suma);
  const valores = () => campos.map(c => Math.max(0, Math.floor(Number(c.value) || 0)));
  function pintar() { suma.textContent = 'Repartidos: ' + valores().reduce((a, b) => a + b, 0) + ' de ' + D.monedas; }
  campos.forEach(c => c.addEventListener('input', () => { ui.say(''); pintar(); }));
  ui.button('Proponer el reparto', 'primary', () => {
    if (resuelto) return;
    const v = valores();
    const total = v.reduce((a, b) => a + b, 0);
    if (total !== D.monedas) { ui.say(total < D.monedas ? 'Quedan ' + (D.monedas - total) + ' doblones sin repartir: el contador del barco no lo permite.' : 'Os habéis pasado en ' + (total - D.monedas) + ' doblones: no hay tantos.', 'bad'); return; }
    let votos = 1;                                                   // el capitán vota a favor de su propio reparto
    for (let k = 1; k < D.piratas; k++) if (v[k] > D.previo[k - 1]) votos++;
    if (votos < D.necesarios) { ui.say('Solo ' + votos + ' votos a favor y hacen falta ' + D.necesarios + ': la tripulación rechaza el reparto y el capitán se va por la borda.', 'bad'); return; }
    if (v.some((x, i) => x !== D.solucion[i])) { ui.say('Se aprueba con ' + votos + ' votos, pero el capitán podía haberse quedado con más doblones sin perder la votación.', 'bad'); return; }
    resuelto = true;
    ui.say('Se aprueba con ' + votos + ' votos y el capitán se queda con ' + v[0] + ' doblones. Los demás gruñen, pero cobran lo suyo. Coged la carta 56.', 'ok');
  });
  ui.button('Poner todo a cero', '', () => { if (!resuelto) { campos.forEach(c => { c.value = '0'; }); ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
