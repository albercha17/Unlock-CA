// Carta 72 — Los hierros del ganado: de ocho marcas a fuego en las reses de la subasta (carta 75), marcar las que son de Don Abel, cuyo hierro está en la
// carta 79: las auténticas son el mismo hierro visto derecho, de lado, boca abajo o en espejo; las falsas cambian un solo cuadrito.
// instancias_oeste.py, HIERROS (tres auténticas entre ocho).
import { openGame } from './ui.js';
import { estilo } from './comun.js';

const D = /*DATOS*/{"candidatos": 8, "autenticos": [2, 3, 5]}/*FIN*/;

export function startMinigame(opts = {}) {
  const ui = openGame({ title: 'Carta 72 — Los hierros del ganado', instr: 'Marcad los números de las reses que llevan el hierro de Don Abel. Las ocho marcas están en la carta 75 y el hierro verdadero, en la 79.', ...opts });
  estilo('oe-hie', `.hie-fila{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;max-width:340px;margin:10px auto}.hie-op{min-height:56px;border-radius:10px;border:3px solid #3a2412;background:#e6c88c;color:#3a2412;font:800 1.4rem Georgia,serif;cursor:pointer}.hie-op[data-v="1"]{background:#b03a2e;color:#fff;border-color:#f5d48a}`);
  const sel = Array(D.candidatos).fill(0);
  let resuelto = false;
  const fila = document.createElement('div');
  fila.className = 'hie-fila';
  const botones = sel.map((_, i) => {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'hie-op';
    b.dataset.i = String(i + 1);
    b.textContent = String(i + 1);
    b.setAttribute('aria-label', 'Res número ' + (i + 1));
    b.addEventListener('click', () => { if (resuelto) return; sel[i] ^= 1; ui.say(''); pintar(); });
    fila.appendChild(b);
    return b;
  });
  ui.body.appendChild(fila);
  function pintar() { botones.forEach((b, i) => { b.dataset.v = String(sel[i]); }); }
  ui.button('Entregar la lista', 'primary', () => {
    if (resuelto) return;
    const marcados = sel.map((v, i) => (v ? i + 1 : 0)).filter(Boolean);
    if (!marcados.length) { ui.say('No habéis marcado ninguna res.', 'bad'); return; }
    const sobran = marcados.filter(i => !D.autenticos.includes(i)).length;
    const faltan = D.autenticos.filter(i => !marcados.includes(i)).length;
    if (sobran) { ui.say('El ganadero frunce el ceño: alguna de las reses que habéis marcado lleva un hierro falso.', 'bad'); return; }
    if (faltan) { ui.say('Todas las que habéis marcado son suyas, pero le faltan reses por recuperar.', 'bad'); return; }
    resuelto = true;
    ui.say('Don Abel recupera sus tres reses y os da las gracias con un apretón de manos. Coged la carta 82.', 'ok');
  });
  ui.button('Quitar marcas', 'ghost', () => { if (!resuelto) { sel.fill(0); ui.say(''); pintar(); } });
  pintar();
  return { close: ui.close };
}
