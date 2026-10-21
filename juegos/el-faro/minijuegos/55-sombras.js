// Carta 55 — La lámpara de la mesa: poner en fila, de izquierda a derecha, tres cosas del estante del farero (carta 57) para que su sombra
// sea la que Anselmo pintó en la pared (carta 56). Ninguna otra terna da esa sombra (herramientas/instancias_ampliacion.py).
import { openGame } from './ui.js';

const S = /*DATOS*/{"objetos": ["farol", "ancla", "botella", "tetera", "gaviota", "catalejo", "campana", "llave"], "solucion": ["catalejo", "tetera", "ancla"]}/*FIN*/;
const NOMBRE = { farol: 'farol', ancla: 'ancla', botella: 'botella', tetera: 'tetera', gaviota: 'gaviota', catalejo: 'catalejo', campana: 'campana', llave: 'llave' };

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 55 — La lámpara de la mesa',
    instr: 'Tocad tres cosas del estante para ponerlas en la mesa, de izquierda a derecha (tocad una de la mesa para quitarla). Luego encended la lámpara.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .far-mesa{display:grid;grid-template-columns:repeat(3,1fr);gap:4px;width:min(86vw,320px);margin:6px auto;padding:8px;border-radius:8px;background:#2a2622;border:3px solid #c8a050}
    .far-hueco{aspect-ratio:3 / 4;border:2px dashed #8a7650;border-radius:6px;background:#1a1816 center bottom / 80% no-repeat;cursor:pointer;padding:0}
    .far-pared{width:min(86vw,320px);aspect-ratio:9 / 4;margin:0 auto 8px;border-radius:6px;background:#e8dcba;display:grid;grid-template-columns:repeat(3,1fr);overflow:hidden}
    .far-pared i{background:center bottom / contain no-repeat;opacity:0;transition:opacity .4s}
    .far-pared.on i{opacity:1}
    .far-estante{display:grid;grid-template-columns:repeat(4,1fr);gap:4px;max-width:320px;margin:0 auto}
    .far-obj{aspect-ratio:3 / 4;border:2px solid #6a5030;border-radius:6px;background:#3a2c1e center / 78% no-repeat;cursor:pointer;padding:0}
    .far-obj:disabled{opacity:.25}
  `;
  ui.body.appendChild(style);
  const pared = document.createElement('div');
  pared.className = 'far-pared';
  const mesa = document.createElement('div');
  mesa.className = 'far-mesa';
  const est = document.createElement('div');
  est.className = 'far-estante';
  ui.body.append(pared, mesa, est);

  let fila = [], resuelto = false;
  function pintar() {
    pared.classList.remove('on');
    pared.innerHTML = '';
    mesa.innerHTML = '';
    for (let i = 0; i < 3; i++) {
      const o = fila[i];
      const sombra = document.createElement('i');
      if (o) sombra.style.backgroundImage = "url('./img/ui/sombra-" + o + ".png')";
      pared.appendChild(sombra);
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'far-hueco';
      b.dataset.i = String(i);
      if (o) b.style.backgroundImage = "url('./img/ui/obj-" + o + ".png')";
      b.setAttribute('aria-label', 'Sitio ' + (i + 1) + ' de la mesa' + (o ? ': ' + NOMBRE[o] : ''));
      b.addEventListener('click', () => { if (!resuelto && o) { fila = fila.filter(x => x !== o); ui.say(''); pintar(); } });
      mesa.appendChild(b);
    }
    est.innerHTML = '';
    S.objetos.forEach((o, k) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'far-obj';
      b.dataset.o = o;
      b.style.backgroundImage = "url('./img/ui/obj-" + o + ".png')";
      b.disabled = fila.includes(o);
      b.setAttribute('aria-label', (k + 1) + ': ' + NOMBRE[o]);
      b.addEventListener('click', () => { if (!resuelto && fila.length < 3) { fila.push(o); ui.say(''); pintar(); } });
      est.appendChild(b);
    });
  }

  ui.button('Encender la lámpara', 'primary', () => {
    if (resuelto) return;
    if (fila.length < 3) { ui.say('Hacen falta tres cosas en la mesa.', 'bad'); return; }
    pared.classList.add('on');
    if (fila.every((o, i) => o === S.solucion[i])) {
      resuelto = true;
      ui.say('La sombra encaja con la pintura de la pared y, con un chasquido, se abre la trampilla de la escalera de hierro. Coged la carta 64.', 'ok');
    } else {
      ui.say('Esa sombra no es la de la pared (carta 56). Comparad bien las formas y el orden con el estante (carta 57).', 'bad');
    }
  });
  pintar();
  return { close: ui.close };
}
