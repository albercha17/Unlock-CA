// Carta 20 — El candado del furgón: cinco ruedas con letras; la palabra son las letras de los vagones enganchados en orden (cartas 14 a 18 juntas).
// Solución: TEXAS.
import { openGame } from './ui.js';

const SOLUCION = 'TEXAS';
const ABC = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 20 — El candado del furgón',
    instr: 'Gira cada rueda con las flechas hasta formar la palabra de los vagones, de izquierda a derecha.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .oes-candado{display:flex;gap:8px;justify-content:center;margin:6px 0 14px;padding:14px 10px;border-radius:12px;border:3px solid #b8742a;background:linear-gradient(180deg,#5a3a1c,#2e1c0c);box-shadow:inset 0 0 18px rgba(0,0,0,.7)}
    .oes-rueda{display:flex;flex-direction:column;align-items:center;gap:6px}
    .oes-rueda .val{width:46px;height:62px;border-radius:8px;border:2px solid #f0b860;background:#f5e6c4;color:#2a1404;display:flex;align-items:center;justify-content:center;font:800 2rem Georgia,serif;box-shadow:inset 0 0 10px rgba(0,0,0,.35)}
    .oes-rueda.ok .val{border-color:#46c46a;color:#0c5a24}
    .oes-rueda button{width:46px;height:34px;border-radius:8px;border:2px solid #f0b860;background:linear-gradient(180deg,#c88a3a,#7a4a1a);color:#fff2d6;font-size:1.1rem;font-weight:800;cursor:pointer;box-shadow:0 3px 0 #2a1608}
    .oes-rueda button:active{transform:translateY(2px);box-shadow:0 1px 0 #2a1608}
  `;
  ui.body.appendChild(style);

  const candado = document.createElement('div');
  candado.className = 'oes-candado';
  ui.body.appendChild(candado);

  const letras = SOLUCION.split('').map(() => 0);
  let resuelto = false;

  function pintar() {
    candado.innerHTML = '';
    letras.forEach((v, i) => {
      const r = document.createElement('div');
      r.className = 'oes-rueda' + (resuelto ? ' ok' : '');
      r.dataset.i = String(i);
      r.innerHTML = '<button type="button" class="sube" aria-label="Letra siguiente de la rueda ' + (i + 1) + '">▲</button><div class="val" data-l="' + ABC[v] + '">' + ABC[v] + '</div><button type="button" class="baja" aria-label="Letra anterior de la rueda ' + (i + 1) + '">▼</button>';
      r.querySelector('.sube').addEventListener('click', () => { if (!resuelto) { letras[i] = (letras[i] + 1) % 26; ui.say(''); pintar(); } });
      r.querySelector('.baja').addEventListener('click', () => { if (!resuelto) { letras[i] = (letras[i] + 25) % 26; ui.say(''); pintar(); } });
      candado.appendChild(r);
    });
  }

  ui.button('Abrir', 'primary', () => {
    if (resuelto) return;
    if (letras.map(v => ABC[v]).join('') === SOLUCION) {
      resuelto = true;
      pintar();
      ui.say('¡Clic! El candado se abre y la puerta del furgón del correo cede. Dentro hay un telegrama del sheriff: os espera en su oficina. Coged la carta 26.', 'ok');
    } else {
      ui.say('El candado no se abre. Juntad los cinco vagones en fila, de manera que los símbolos de los enganches coincidan, y leed las letras de izquierda a derecha.', 'bad');
    }
  });

  pintar();
  return { close: ui.close };
}
