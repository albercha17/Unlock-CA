// Carta 46 — Vidriera de la torre: tres cristales de cuatro cuadrados (uno recto, uno en ese y uno en te) que se mueven por la ventana.
// Deben cubrir EXACTAMENTE el dibujo de la carta 37, cada uno una vez, sin girarlos y sin solaparse (donde se solapan brillan doble).
// Dibujo (columna,fila desde 0): fila 2 entera; fila 3 columnas 1-3; fila 4 columnas 1-4. Solución única (herramientas/instancias_cuento.py):
// recto en (1,4), ese en (2,2), te en (0,2). Letra del libro: F.
import { openGame } from './ui.js';
import { guardarLetra, estilo, conImagen, NOMBRES_COLUMNA } from './libro.js';

const LETRA = 'F';
const N = 5;
const DIBUJO = ['0,2', '1,2', '2,2', '3,2', '4,2', '1,3', '2,3', '3,3', '1,4', '2,4', '3,4', '4,4'];
const PIEZAS = [
  { id: 'palo', nombre: 'Cristal recto', celdas: [[0, 0], [1, 0], [2, 0], [3, 0]], color: '255,210,74', trama: 'solida', ini: [0, 0] },
  { id: 'ese', nombre: 'Cristal en ese', celdas: [[1, 0], [2, 0], [0, 1], [1, 1]], color: '255,122,168', trama: 'rayas', ini: [0, 1] },
  { id: 'te', nombre: 'Cristal en te', celdas: [[0, 0], [1, 0], [2, 0], [1, 1]], color: '90,176,255', trama: 'puntos', ini: [2, 0] }
];

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 46 — Vidriera de la torre',
    instr: 'Toca un cristal para elegirlo y muévelo con las flechas (o arrástralo). Deben llenar el dibujo de la carta 37, sin girarlos y sin solaparse.',
    ...opts
  });
  estilo('cu-vidriera-estilo', `
    .vid-marco{display:grid;grid-template-columns:18px 1fr;grid-template-rows:18px auto;max-width:330px;margin:0 auto 8px;font-size:.75rem;color:#ffe08a}
    .vid-letras{grid-column:2;display:grid;grid-template-columns:repeat(${N},1fr);justify-items:center;align-items:center}
    .vid-nums{grid-row:2;display:grid;grid-template-rows:repeat(${N},1fr);justify-items:center;align-items:center}
    .vid-tablero{grid-column:2;grid-row:2;position:relative;aspect-ratio:1;border-radius:10px;border:4px solid #8a6a2a;background:linear-gradient(180deg,#1a1038,#0c0620);box-shadow:inset 0 0 24px rgba(0,0,0,.7),0 0 18px rgba(255,224,138,.2);touch-action:none}
    .vid-rejilla{position:absolute;inset:0;display:grid;grid-template-columns:repeat(${N},1fr);grid-template-rows:repeat(${N},1fr)}
    .vid-celda{border:1px solid rgba(255,224,138,.14)}
    .vid-pieza{position:absolute;inset:0;pointer-events:none}
    .vid-bloque{position:absolute;width:${100 / N}%;height:${100 / N}%;box-sizing:border-box;border-radius:6px;border:2px solid rgba(255,255,255,.55);mix-blend-mode:screen;pointer-events:auto;cursor:grab;touch-action:none}
    .vid-pieza.sel .vid-bloque{border-color:#fff;box-shadow:0 0 14px rgba(255,255,255,.7)}
    .vid-bloque.solida{background:rgba(var(--c),.8)}
    .vid-bloque.rayas{background:repeating-linear-gradient(45deg,rgba(var(--c),.85) 0 6px,rgba(var(--c),.45) 6px 12px)}
    .vid-bloque.puntos{background:radial-gradient(circle,rgba(255,255,255,.7) 18%,transparent 20%) 0 0/10px 10px,rgba(var(--c),.7)}
    .vid-selector{display:flex;gap:6px;justify-content:center;flex-wrap:wrap;margin:6px 0}
    .vid-sel{min-height:44px;padding:4px 10px;border-radius:10px;border:2px solid rgba(255,224,138,.45);background:rgba(255,255,255,.08);color:#fff;font:700 .8rem inherit;font-family:inherit;cursor:pointer}
    .vid-sel.sel{background:#ffe08a;color:#2a1450;border-color:#fff}
    .vid-cruz{display:grid;grid-template-columns:repeat(3,52px);grid-template-rows:repeat(3,44px);gap:4px;justify-content:center;margin:6px auto}
    .vid-mover{border-radius:10px;border:2px solid rgba(255,224,138,.5);background:linear-gradient(180deg,#8a63d8,#5a3aa8);color:#fff;font:800 1.2rem inherit;cursor:pointer;min-width:0;padding:0}
    .vid-mover:active{filter:brightness(1.3)}
    .vid-mover[data-d="arr"]{grid-area:1/2}.vid-mover[data-d="izq"]{grid-area:2/1}.vid-mover[data-d="der"]{grid-area:2/3}.vid-mover[data-d="aba"]{grid-area:3/2}
    .vid-img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.55;pointer-events:none;border-radius:6px}
  `);

  const marco = document.createElement('div');
  marco.className = 'vid-marco';
  const letras = document.createElement('div');
  letras.className = 'vid-letras';
  for (let c = 0; c < N; c++) { const s = document.createElement('span'); s.textContent = NOMBRES_COLUMNA[c]; letras.appendChild(s); }
  const nums = document.createElement('div');
  nums.className = 'vid-nums';
  for (let r = 0; r < N; r++) { const s = document.createElement('span'); s.textContent = String(r + 1); nums.appendChild(s); }
  const tablero = document.createElement('div');
  tablero.className = 'vid-tablero';
  const rejilla = document.createElement('div');
  rejilla.className = 'vid-rejilla';
  for (let i = 0; i < N * N; i++) { const c = document.createElement('div'); c.className = 'vid-celda'; rejilla.appendChild(c); }
  tablero.appendChild(rejilla);
  conImagen(tablero, 'vidriera.jpg', { clase: 'vid-img', mezcla: 'screen' });
  marco.append(letras, nums, tablero);
  ui.body.appendChild(marco);

  const selector = document.createElement('div');
  selector.className = 'vid-selector';
  const cruz = document.createElement('div');
  cruz.className = 'vid-cruz';
  ui.body.append(selector, cruz);

  const pos = PIEZAS.map((p) => p.ini.slice());
  let sel = 0;
  let resuelto = false;
  const nodos = [];

  function anchoPieza(p) { return Math.max(...p.celdas.map((c) => c[0])) + 1; }
  function altoPieza(p) { return Math.max(...p.celdas.map((c) => c[1])) + 1; }

  PIEZAS.forEach((p, i) => {
    const cont = document.createElement('div');
    cont.className = 'vid-pieza';
    cont.dataset.i = String(i);
    p.celdas.forEach(() => {
      const b = document.createElement('div');
      b.className = 'vid-bloque ' + p.trama;
      b.style.setProperty('--c', p.color);
      cont.appendChild(b);
    });
    tablero.appendChild(cont);
    nodos.push(cont);
    const bs = document.createElement('button');
    bs.type = 'button';
    bs.className = 'vid-sel';
    bs.dataset.i = String(i);
    bs.textContent = p.nombre;
    bs.addEventListener('click', () => { sel = i; pintar(); });
    selector.appendChild(bs);
    // arrastrar con el dedo o el ratón: se mueve de casilla en casilla
    cont.addEventListener('pointerdown', (e) => {
      if (resuelto || !e.target.classList.contains('vid-bloque')) return;
      sel = i;
      pintar();
      const r = tablero.getBoundingClientRect();
      const celda = r.width / N;
      const x0 = e.clientX, y0 = e.clientY, p0 = pos[i].slice();
      const mover = (ev) => {
        const dx = Math.round((ev.clientX - x0) / celda), dy = Math.round((ev.clientY - y0) / celda);
        fijar(i, p0[0] + dx, p0[1] + dy);
      };
      const fin = () => { window.removeEventListener('pointermove', mover); window.removeEventListener('pointerup', fin); window.removeEventListener('pointercancel', fin); };
      window.addEventListener('pointermove', mover);
      window.addEventListener('pointerup', fin);
      window.addEventListener('pointercancel', fin);
      e.preventDefault();
    });
  });

  [['arr', '↑', 'Subir'], ['izq', '←', 'Mover a la izquierda'], ['der', '→', 'Mover a la derecha'], ['aba', '↓', 'Bajar']].forEach(([d, t, a]) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'vid-mover';
    b.dataset.d = d;
    b.textContent = t;
    b.setAttribute('aria-label', a);
    b.addEventListener('click', () => paso(d));
    cruz.appendChild(b);
  });

  function fijar(i, x, y) {
    const p = PIEZAS[i];
    pos[i] = [Math.max(0, Math.min(N - anchoPieza(p), x)), Math.max(0, Math.min(N - altoPieza(p), y))];
    pintar();
  }
  function paso(d) {
    if (resuelto) return;
    const dx = d === 'izq' ? -1 : d === 'der' ? 1 : 0;
    const dy = d === 'arr' ? -1 : d === 'aba' ? 1 : 0;
    fijar(sel, pos[sel][0] + dx, pos[sel][1] + dy);
    ui.say('');
  }
  const onKey = (e) => {
    const m = { ArrowUp: 'arr', ArrowDown: 'aba', ArrowLeft: 'izq', ArrowRight: 'der' }[e.key];
    if (m) { paso(m); e.preventDefault(); }
  };
  document.addEventListener('keydown', onKey);
  ui.onClose(() => document.removeEventListener('keydown', onKey));

  function pintar() {
    PIEZAS.forEach((p, i) => {
      nodos[i].classList.toggle('sel', i === sel);
      Array.from(nodos[i].children).forEach((b, k) => {
        b.style.left = ((pos[i][0] + p.celdas[k][0]) * 100 / N) + '%';
        b.style.top = ((pos[i][1] + p.celdas[k][1]) * 100 / N) + '%';
        b.setAttribute('aria-label', p.nombre + ' en ' + NOMBRES_COLUMNA[pos[i][0] + p.celdas[k][0]] + (pos[i][1] + p.celdas[k][1] + 1));
      });
      selector.children[i].classList.toggle('sel', i === sel);
    });
  }

  function comprobar() {
    if (resuelto) return;
    const cuenta = {};
    PIEZAS.forEach((p, i) => p.celdas.forEach((c) => { const k = (pos[i][0] + c[0]) + ',' + (pos[i][1] + c[1]); cuenta[k] = (cuenta[k] || 0) + 1; }));
    const solapes = Object.values(cuenta).filter((v) => v > 1).length;
    if (solapes) { ui.say('Hay ' + solapes + ' cuadrado' + (solapes > 1 ? 's' : '') + ' donde dos cristales se solapan y brillan doble: la vidriera se apaga. Separadlos.', 'bad'); return; }
    const iluminadas = Object.keys(cuenta);
    const de_mas = iluminadas.filter((k) => !DIBUJO.includes(k)).length;
    const faltan = DIBUJO.filter((k) => !cuenta[k]).length;
    if (!de_mas && !faltan) {
      resuelto = true;
      guardarLetra('46', LETRA);
      ui.say('¡Los tres cristales encajan y la vidriera se enciende con todos sus colores! Coged la carta 54. Letra del libro: ' + LETRA + '.', 'ok');
    } else {
      ui.say('Todavía no coincide con el dibujo de la carta 37: ' + de_mas + ' cuadrado' + (de_mas === 1 ? '' : 's') + ' iluminado' + (de_mas === 1 ? '' : 's') + ' de más y ' + faltan + ' sin iluminar.', 'bad');
    }
  }

  ui.button('Comprobar', 'primary', comprobar);
  pintar();
  return { close: ui.close };
}
