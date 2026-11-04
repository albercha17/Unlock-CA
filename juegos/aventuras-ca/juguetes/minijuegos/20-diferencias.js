// Carta 20 — Las diferencias: tocar las siete cosas que han cambiado desde la foto Polaroid (cartas 19 y 21, dos mitades; la nota de Leo, en la 18).
// Imagen y zonas de herramientas/juguetes.py (instancias_juguetes.json). Nota de la nana: E.nota.
import { openGame } from './ui.js';

const E = /*DATOS*/{"zonas": [[[8.72, 40.19, 14.81, 20.75]], [[28.26, 44.44, 24.12, 16.51]], [[76.59, 10.94, 14.55, 23.11]], [[77.24, 37.83, 16.48, 23.11]], [[55.12, 9.06, 12.34, 25.0]], [[69.47, 44.91, 11.06, 16.04]], [[23.38, 67.74, 12.93, 20.28], [9.67, 13.77, 12.93, 20.28]]], "textos": ["la pelota era roja y ahora es azul", "el coche era azul y ahora es rojo", "falta el libro morado", "falta el barco rojo", "el cohete está boca abajo", "hay un dado que no estaba", "el patito ha bajado a la balda de abajo"], "nota": "SOL"}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 20 — Las diferencias',
    instr: 'Así está ahora la estantería de Leo. Comparadla con la foto Polaroid y tocad las siete cosas que han cambiado.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .jug-estante{position:relative;width:min(92vw,360px);aspect-ratio:620 / 400;margin:4px auto 8px;border-radius:10px;overflow:hidden;
      background:url('./img/ui/estanteria.jpg') center / 100% 100% no-repeat;border:4px solid #ffcc33;cursor:crosshair}
    .jug-zona{position:absolute;border:0;padding:0;background:transparent;border-radius:50%;cursor:crosshair}
    .jug-zona.hallada{border:4px solid #ff4a6a;box-shadow:0 0 0 3px rgba(255,255,255,.7);cursor:default}
    .jug-cuenta{text-align:center;font:700 1rem 'Fredoka',system-ui,sans-serif;color:#ffcc33;margin:0}
  `;
  ui.body.appendChild(style);

  const estante = document.createElement('div');
  estante.className = 'jug-estante';
  const cuenta = document.createElement('p');
  cuenta.className = 'jug-cuenta';
  ui.body.appendChild(estante);
  ui.body.appendChild(cuenta);

  const halladas = new Set();
  let resuelto = false;

  function pintar() {
    cuenta.textContent = 'Diferencias encontradas: ' + halladas.size + ' de ' + E.zonas.length;
  }

  estante.addEventListener('click', e => {
    if (resuelto || e.target !== estante) return;
    ui.say('Ahí todo está igual que en la foto. Mirad bien la Polaroid.', 'bad');
  });

  E.zonas.forEach((rects, i) => rects.forEach(([x, y, w, h]) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'jug-zona';
    b.dataset.i = String(i);
    b.style.left = x + '%';
    b.style.top = y + '%';
    b.style.width = w + '%';
    b.style.height = h + '%';
    b.setAttribute('aria-label', 'Zona de la estantería ' + (i + 1));
    b.addEventListener('click', ev => {
      ev.stopPropagation();
      if (resuelto || halladas.has(i)) return;
      halladas.add(i);
      estante.querySelectorAll('.jug-zona[data-i="' + i + '"]').forEach(z => z.classList.add('hallada'));
      pintar();
      if (halladas.size === E.zonas.length) {
        resuelto = true;
        ui.say('¡Las siete! El Capitán Pelusa aplaude con sus patas de peluche: detrás de los juguetes revueltos asoma un hueco con un paquetito. Nota de las diferencias: ' + E.nota + '. Coged la carta 28.', 'ok');
      } else {
        ui.say('¡Bien visto! ' + E.textos[i].charAt(0).toUpperCase() + E.textos[i].slice(1) + '.', '');
      }
    });
    estante.appendChild(b);
  }));

  pintar();
  return { close: ui.close };
}
