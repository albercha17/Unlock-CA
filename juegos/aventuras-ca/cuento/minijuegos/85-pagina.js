// Carta 85 — La última página (metapuzle): cada puzle resuelto dejó una letra del libro (cartas 14, 20, 40, 46, 51, 64, 69 y 72) y el libro las guarda.
// Hay que ordenar las ocho letras para escribir la palabra del final (pistas en las cartas 86 y 87): PERDICES.
import { openGame } from './ui.js';
import { leerLetras, estilo, conImagen } from './libro.js';

const CARTAS = ['14', '20', '40', '46', '51', '64', '69', '72'];
const PALABRA = 'PERDICES';

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 85 — La última página',
    instr: 'El libro guardó una letra por cada puzle que habéis resuelto. Tocadlas en el orden que forme la palabra del final (cartas 86 y 87). Tocad un hueco para devolver su letra.',
    ...opts
  });
  estilo('cu-pagina-estilo', `
    .pag-hoja{position:relative;border-radius:10px;padding:14px 8px 12px;background:linear-gradient(180deg,#f4e7c2,#e3cf9a);box-shadow:inset 0 0 26px rgba(120,80,20,.4);margin-bottom:10px;color:#3a2410}
    .pag-huecos{display:grid;grid-template-columns:repeat(8,1fr);gap:4px;margin-bottom:6px}
    .pag-hueco{aspect-ratio:1/1.15;border-radius:8px;border:2px dashed rgba(90,50,10,.55);background:rgba(255,255,255,.35);font:800 1.5rem Georgia,serif;color:#3a2410;padding:0;cursor:pointer;min-width:0}
    .pag-hueco.lleno{border-style:solid;background:rgba(255,224,138,.8)}
    .pag-letras{display:grid;grid-template-columns:repeat(8,1fr);gap:4px;margin:4px 0 6px}
    .pag-letra{aspect-ratio:1/1.15;border-radius:8px;border:2px solid #ffe08a;background:linear-gradient(180deg,#8a63d8,#5a3aa8);color:#fff7d6;font:800 1.5rem inherit;font-family:inherit;cursor:pointer;padding:0;min-width:0}
    .pag-letra[disabled]{opacity:.35;cursor:default}
    .pag-letra.falta{background:rgba(255,255,255,.1);border-style:dashed;color:#cdbbff}
    .pag-nota{font-size:.82rem;color:#d8e2ee;margin-top:4px}
    .pag-img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.35;pointer-events:none;border-radius:10px}
  `);

  const letras = leerLetras();
  const hoja = document.createElement('div');
  hoja.className = 'pag-hoja';
  const huecos = document.createElement('div');
  huecos.className = 'pag-huecos';
  hoja.appendChild(huecos);
  const banco = document.createElement('div');
  banco.className = 'pag-letras';
  const nota = document.createElement('div');
  nota.className = 'pag-nota';
  ui.body.append(hoja, banco, nota);
  conImagen(hoja, 'pagina.jpg', { clase: 'pag-img', mezcla: 'multiply' });

  const faltan = CARTAS.filter((c) => !letras[c]);
  nota.textContent = faltan.length ? 'El libro todavía no tiene la letra de las cartas: ' + faltan.join(', ') + '. Resolvedlas primero (si ya lo hicisteis en otro móvil, volved a resolverlas).' : 'El libro tiene las ocho letras.';

  const colocadas = []; // índices (de CARTAS) en orden de colocación
  let resuelto = false;

  CARTAS.forEach((c, i) => {
    const h = document.createElement('button');
    h.type = 'button';
    h.className = 'pag-hueco';
    h.dataset.i = String(i);
    h.setAttribute('aria-label', 'Hueco ' + (i + 1) + ' de la palabra');
    h.addEventListener('click', () => { if (!resuelto && i < colocadas.length) { colocadas.splice(i, 1); ui.say(''); pintar(); } });
    huecos.appendChild(h);
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'pag-letra' + (letras[c] ? '' : ' falta');
    b.dataset.n = String(i);
    b.dataset.l = letras[c] || '';
    b.textContent = letras[c] || '?';
    b.setAttribute('aria-label', letras[c] ? 'Letra ' + letras[c] : 'Letra todavía sin conseguir');
    b.addEventListener('click', () => {
      if (resuelto) return;
      if (!letras[c]) { ui.say('Esa letra todavía no está en el libro: resolved antes el puzle de la carta ' + c + '.', 'bad'); return; }
      if (colocadas.length < CARTAS.length && !colocadas.includes(i)) { colocadas.push(i); ui.say(''); pintar(); }
    });
    banco.appendChild(b);
  });

  function pintar() {
    huecos.querySelectorAll('.pag-hueco').forEach((h, k) => {
      const i = colocadas[k];
      h.textContent = i === undefined ? '' : letras[CARTAS[i]];
      h.classList.toggle('lleno', i !== undefined);
    });
    banco.querySelectorAll('.pag-letra').forEach((b, i) => { b.disabled = colocadas.includes(i); });
  }

  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    if (faltan.length) { ui.say('Todavía faltan letras en el libro (cartas ' + faltan.join(', ') + ').', 'bad'); return; }
    if (colocadas.length < CARTAS.length) { ui.say('Colocad las ocho letras para escribir la palabra.', 'bad'); return; }
    const palabra = colocadas.map((i) => letras[CARTAS[i]]).join('');
    if (palabra === PALABRA) {
      resuelto = true;
      ui.say('¡La palabra aparece con letras de oro: ' + PALABRA + '! El cuento por fin tiene final y el Cronoportal se enciende. Coged la carta 99.', 'ok');
    } else {
      ui.say('«' + palabra + '» no es la palabra del final: no es lo que se comió en el banquete del final (cartas 86 y 87). Reordenad las letras.', 'bad');
    }
  });
  ui.button('Quitar todas', 'ghost', () => { if (!resuelto) { colocadas.length = 0; ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
