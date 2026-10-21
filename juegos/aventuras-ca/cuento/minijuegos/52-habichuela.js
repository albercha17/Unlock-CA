// Carta 52 — La habichuela mágica: la mata solo llega a la ventana de la torre si se riega con las hojas que tendrá el día pedido. Lo que
// crece cada día está dibujado en el diario del leñador (cartas 54, 55 y 59): cada día salen tantas hojas como tenía la mata anteayer.
import { openGame } from './ui.js';
import { estilo } from './libro.js';

const D = /*DATOS*/{"dibujados": [1, 1, 2, 3, 5, 8], "pregunta_dia": 9, "solucion": 34}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 52 — La habichuela mágica', instr: 'El leñador dice que la mata alcanzará la ventana de la torre la noche de la luna ' + D.pregunta_dia + '. Para regarla con magia hay que decirle cuántas hojas tendrá esa noche.', ...opts });
  estilo('cu-haba', `
    .hab-cont{display:flex;align-items:center;justify-content:center;gap:12px;margin:12px 0}
    .hab-cont button{width:52px;height:52px;border-radius:50%;border:2px solid #ffe08a;background:#3a7a3a;color:#fff;font:800 1.4rem system-ui;cursor:pointer}
    .hab-num{min-width:90px;text-align:center;font:800 2.4rem Georgia,serif;color:#fff7d6}`);
  const c = document.createElement('div'); c.className = 'hab-cont';
  const menos = document.createElement('button'); menos.type = 'button'; menos.textContent = '−'; menos.dataset.d = '-1';
  const num = document.createElement('div'); num.className = 'hab-num';
  const mas = document.createElement('button'); mas.type = 'button'; mas.textContent = '+'; mas.dataset.d = '1';
  const mas10 = document.createElement('button'); mas10.type = 'button'; mas10.textContent = '+10'; mas10.dataset.d = '10';
  c.append(menos, num, mas, mas10);
  ui.body.appendChild(c);
  let n = 0, resuelto = false;
  const pintar = () => { num.textContent = String(n); num.dataset.n = String(n); };
  [menos, mas, mas10].forEach(b => b.addEventListener('click', () => { if (!resuelto) { n = Math.max(0, n + Number(b.dataset.d)); ui.say(''); pintar(); } }));
  ui.button('Regar', 'primary', () => {
    if (resuelto) return;
    if (n === D.solucion) { resuelto = true; ui.say('La habichuela se estira con un crujido y, hoja a hoja, llega a la ventana de la torre. ¡A trepar! Coged la carta 44.', 'ok'); }
    else ui.say('La mata tiembla, crece un poco y se detiene: esas no son sus hojas. Mirad bien cómo crece día a día (cartas 54, 55 y 59).', 'bad');
  });
  pintar();
  return { close: ui.close };
}
