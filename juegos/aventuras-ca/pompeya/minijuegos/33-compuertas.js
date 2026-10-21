// Carta 33 — Las compuertas: abrir y cerrar las nueve compuertas del acueducto para que cada parterre reciba lo que pide el jardinero
// (carta 37), según el plano del fontanero (carta 36). Cada arqueta reparte a partes iguales; no se puede perder agua. Solución única.
import { openGame } from './ui.js';

const D = /*DATOS*/{"red": {"acueducto": [["I", "A"], ["II", "B"], ["III", "C"]], "A": [["IV", "rosas"], ["V", "B"]], "B": [["VI", "laureles"], ["VII", "vina"]], "C": [["VIII", "vina"], ["IX", "lirios"]]}, "orden": ["acueducto", "A", "B", "C"], "caudal": 36, "pide": {"rosas": 12, "laureles": 6, "vina": 6, "lirios": 12}, "compuertas": ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]}/*FIN*/;
const NOMBRE = { rosas: 'las rosas', laureles: 'los laureles', vina: 'la viña', lirios: 'los lirios' };

function regar(abiertas) {
  const agua = { acueducto: D.caudal }, llega = { rosas: 0, laureles: 0, vina: 0, lirios: 0 };
  let perdida = 0;
  for (const nudo of D.orden) {
    const q = agua[nudo] || 0;
    const sal = D.red[nudo].filter(([c]) => abiertas.has(c));
    if (!sal.length) { perdida += q; continue; }
    for (const [, d] of sal) { if (d in llega) llega[d] += q / sal.length; else agua[d] = (agua[d] || 0) + q / sal.length; }
  }
  return { llega, perdida };
}

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 33 — Las compuertas', instr: 'Subid o bajad cada palanca (arriba, abierta) y abrid el agua. El jardinero quiere lo justo en cada parterre y que no se pierda nada.', ...opts });
  const style = document.createElement('style');
  style.textContent = `
    .pom-palancas{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;max-width:320px;margin:8px auto}
    .pom-pal{height:90px;border-radius:8px;border:2px solid #3a2410;background:#6a4a2a;cursor:pointer;position:relative;padding:0;color:#f6e4b8;font:800 .85rem Georgia,serif}
    .pom-pal i{position:absolute;left:30%;right:30%;height:30px;border-radius:6px;background:#c8a050;transition:top .15s}
    .pom-pal[data-on="1"] i{top:8px;background:#7ec8e8}
    .pom-pal[data-on="0"] i{top:44px}
    .pom-pal span{position:absolute;left:0;right:0;bottom:2px}`;
  ui.body.appendChild(style);
  const p = document.createElement('div'); p.className = 'pom-palancas'; ui.body.appendChild(p);
  const abiertas = new Set();
  let resuelto = false;
  D.compuertas.forEach(c => {
    const b = document.createElement('button'); b.type = 'button'; b.className = 'pom-pal'; b.dataset.c = c; b.dataset.on = '0';
    b.innerHTML = '<i></i><span>' + c + '</span>'; b.setAttribute('aria-label', 'Compuerta ' + c);
    b.addEventListener('click', () => { if (resuelto) return; abiertas.has(c) ? abiertas.delete(c) : abiertas.add(c); b.dataset.on = abiertas.has(c) ? '1' : '0'; ui.say(''); });
    p.appendChild(b);
  });
  ui.button('Abrir el agua', 'primary', () => {
    if (resuelto) return;
    const { llega, perdida } = regar(abiertas);
    if (perdida > 0) { ui.say('El agua se queda estancada en alguna arqueta sin salida y se desborda. El jardinero se lleva las manos a la cabeza.', 'bad'); return; }
    const mal = Object.keys(llega).filter(k => Math.abs(llega[k] - D.pide[k]) > 1e-9);
    if (!mal.length) { resuelto = true; ui.say('El agua corre justa por cada parterre y la fuente vuelve a manar. En el fondo del pilón brilla la otra mitad de la llave. Coged la carta 35.', 'ok'); }
    else ui.say('El jardinero niega con la cabeza: ' + mal.map(k => NOMBRE[k]).join(', ') + ' no reciben lo que deben.', 'bad');
  });
  return { close: ui.close };
}
