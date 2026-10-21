// Carta 40 — La tablilla de cera: escribir la palabra de la cruz del cuadrado del grafito (cartas 41 y 42).
import { openGame } from './ui.js';

const D = /*DATOS*/{"solucion": "TENET"}/*FIN*/;
const LETRAS = 'ABCDEFGHILMNOPQRSTVX';

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 40 — La tablilla de cera', instr: 'Escribid con el punzón una palabra de cinco letras y apretad la tablilla contra el nicho.', ...opts });
  const style = document.createElement('style');
  style.textContent = `
    .pom-cera{display:flex;gap:6px;justify-content:center;margin:8px auto 12px;padding:12px;border-radius:8px;background:#3a2a14;max-width:300px}
    .pom-cera span{width:44px;height:54px;border-radius:4px;background:#c8a050;display:flex;align-items:center;justify-content:center;font:800 1.6rem Georgia,serif;color:#3a2410}
    .pom-teclas{display:grid;grid-template-columns:repeat(5,1fr);gap:5px;max-width:300px;margin:0 auto}
    .pom-teclas button{padding:10px 0;border-radius:6px;border:2px solid #c8a050;background:#2a1a10;color:#f6e4b8;font:800 1rem Georgia,serif;cursor:pointer}`;
  ui.body.appendChild(style);
  const cera = document.createElement('div'); cera.className = 'pom-cera';
  const teclas = document.createElement('div'); teclas.className = 'pom-teclas';
  ui.body.append(cera, teclas);
  let txt = '', resuelto = false;
  const pintar = () => { cera.innerHTML = ''; for (let i = 0; i < 5; i++) { const s = document.createElement('span'); s.textContent = txt[i] || ''; cera.appendChild(s); } cera.dataset.txt = txt; };
  LETRAS.split('').forEach(l => {
    const b = document.createElement('button'); b.type = 'button'; b.textContent = l; b.dataset.l = l;
    b.addEventListener('click', () => { if (!resuelto && txt.length < 5) { txt += l; ui.say(''); pintar(); } });
    teclas.appendChild(b);
  });
  ui.button('Apretar la tablilla', 'primary', () => {
    if (resuelto) return;
    if (txt === D.solucion) { resuelto = true; ui.say('La palabra se hunde en la cera y el nicho de la pared se abre. Dentro, un pedernal y yesca. Coged la carta 38.', 'ok'); }
    else ui.say('El nicho sigue cerrado. El sembrador dice que su cruz se lee igual en todas direcciones (cartas 41 y 42).', 'bad');
  });
  ui.button('Alisar la cera', '', () => { if (!resuelto) { txt = ''; ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
