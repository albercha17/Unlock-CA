// Carta 66 — El tren de Leo: cargar un juguete en cada vagón, del primero al último, en el orden en que Leo los rodeó en su cuaderno:
// las cinco páginas del folioscopio (cartas 41, 43, 45, 49 y 51) ordenadas por el sol de la ventana. Datos de instancias_juguetes.py.
import { openGame } from './ui.js';

const F = /*DATOS*/{"juguetes": ["patito", "pelota", "tambor", "cohete", "cometa"], "orden": ["pelota", "cometa", "patito", "tambor", "cohete"]}/*FIN*/;
const NOMBRE = { patito: 'patito', pelota: 'pelota', tambor: 'tambor', cohete: 'cohete', cometa: 'cometa' };
const COLOR_VAGON = ['#d63430', '#f6c42a', '#3aa054', '#2c68c4', '#8a4cc4'];

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 66 — El tren de Leo',
    instr: 'Toca un juguete del andén y luego un vagón para subirlo (toca un vagón cargado para bajarlo). Cargad los cinco en el orden del cuaderno de Leo, del primer vagón al último.',
    ...opts
  });

  const style = document.createElement('style');
  style.textContent = `
    .jug-tren{display:flex;align-items:flex-end;gap:3px;justify-content:center;margin:10px auto 2px;max-width:340px}
    .jug-loco{width:46px;height:58px;border-radius:8px 8px 4px 4px;background:linear-gradient(180deg,#e04848,#a01e28);border:2px solid #4a0e14;position:relative}
    .jug-loco::before{content:'';position:absolute;left:8px;top:-14px;width:10px;height:14px;background:#2a2a30;border-radius:2px}
    .jug-vagon{width:54px;height:58px;border:2px solid #2a1a10;border-radius:6px;padding:2px;cursor:pointer;position:relative;display:flex;align-items:center;justify-content:center}
    .jug-vagon img{width:44px;height:44px;object-fit:contain;pointer-events:none}
    .jug-vagon span{position:absolute;bottom:-18px;left:0;right:0;text-align:center;font:700 .72rem system-ui;color:#ffcc33}
    .jug-via{height:6px;max-width:340px;margin:0 auto 26px;background:repeating-linear-gradient(90deg,#6a4a2a 0 10px,#3a2a1a 10px 14px)}
    .jug-anden{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-bottom:6px}
    .jug-juguete{width:58px;height:58px;border-radius:12px;border:3px solid #ffcc33;background:#1e3470;padding:4px;cursor:pointer}
    .jug-juguete img{width:100%;height:100%;object-fit:contain;pointer-events:none}
    .jug-juguete.sel{background:#3a5ab0;box-shadow:0 0 0 3px #fff}
    .jug-juguete:disabled{opacity:.25;cursor:default}
    .jug-tren.arranca{animation:jug-arranca 1.2s ease-in forwards}
    @keyframes jug-arranca{to{transform:translateX(40px)}}
    @media (prefers-reduced-motion:reduce){.jug-tren.arranca{animation:none}}
  `;
  ui.body.appendChild(style);

  const tren = document.createElement('div');
  tren.className = 'jug-tren';
  const via = document.createElement('div');
  via.className = 'jug-via';
  const anden = document.createElement('div');
  anden.className = 'jug-anden';
  ui.body.appendChild(tren);
  ui.body.appendChild(via);
  ui.body.appendChild(anden);

  const carga = [null, null, null, null, null];
  let elegido = null, resuelto = false;
  const img = j => '<img src="./img/ui/jug-' + j + '.png" alt="">';

  function pintar() {
    tren.innerHTML = '<div class="jug-loco" aria-hidden="true"></div>';
    for (let v = 0; v < 5; v++) {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'jug-vagon';
      b.dataset.v = String(v);
      b.style.background = COLOR_VAGON[v];
      b.setAttribute('aria-label', 'Vagón ' + (v + 1) + (carga[v] ? ': ' + NOMBRE[carga[v]] : ': vacío'));
      b.innerHTML = (carga[v] ? img(carga[v]) : '') + '<span>' + (v + 1) + '.º</span>';
      b.addEventListener('click', () => {
        if (resuelto) return;
        if (carga[v]) carga[v] = null;
        else if (elegido) { carga[v] = elegido; elegido = null; }
        ui.say('');
        pintar();
      });
      tren.appendChild(b);
    }
    anden.innerHTML = '';
    F.juguetes.forEach(j => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'jug-juguete' + (elegido === j ? ' sel' : '');
      b.dataset.j = j;
      b.disabled = carga.includes(j);
      b.setAttribute('aria-label', NOMBRE[j]);
      b.innerHTML = img(j);
      b.addEventListener('click', () => { if (!resuelto) { elegido = j; ui.say(''); pintar(); } });
      anden.appendChild(b);
    });
  }

  ui.button('¡Viajeros al tren!', 'primary', () => {
    if (resuelto) return;
    if (carga.includes(null)) { ui.say('Quedan vagones vacíos: cada vagón lleva un juguete.', 'bad'); return; }
    if (carga.every((j, i) => j === F.orden[i])) {
      resuelto = true;
      pintar();
      tren.classList.add('arranca');
      ui.say('¡Chu-chu! El tren de Leo arranca con su carga en el orden del cuaderno y da la vuelta al cuarto hasta la estación del escritorio. Coged la carta 72.', 'ok');
    } else {
      ui.say('El tren no arranca: no es el orden del cuaderno de Leo. Ordenad las páginas por el sol de la ventana (cartas 41, 43, 45, 49 y 51).', 'bad');
    }
  });
  ui.button('Vaciar', '', () => { if (!resuelto) { carga.fill(null); elegido = null; ui.say(''); pintar(); } });

  pintar();
  return { close: ui.close };
}
