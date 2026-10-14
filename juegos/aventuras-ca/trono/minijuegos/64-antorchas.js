// Carta 64 — Antorchas de la cripta (akari): colocar antorchas que iluminen todo el suelo sin verse entre sí; los números de los pilares
// dicen cuántas antorchas tienen pegadas. Dos pilares muestran «?» y su número está en el plano del maestre (carta 66).
// Solución única comprobada por herramientas/instancias_trono.py. Antorchas: B1 D1 E2 A3 F3 B4 E4 C5 A6.
import { openGame } from './ui.js';
import { guardarPalabra, estilo, conImagen, texturaSi } from './comun.js';

const N = 6;
const LETRAS = 'ABCDEF';
const MUROS = ['0,2', '1,5', '2,1', '2,2', '2,4', '3,2', '4,0', '5,2', '5,4', '5,5'];
const NUMEROS = { '0,2': 2, '1,5': 2, '2,2': 0, '3,2': 2 };
const EN_CARTA = ['0,2', '2,2']; // se muestran como «?»
const PALABRA = 'NORTE';

export function startMinigame(opts = {}) {
  const ui = openGame({
    title: 'Carta 64 — Antorchas de la cripta',
    instr: 'Tocad una casilla libre para colocar una antorcha. Cada antorcha ilumina su fila y su columna hasta un pilar. Todo el suelo debe quedar iluminado y ninguna antorcha puede iluminar a otra.',
    ...opts
  });
  texturaSi(ui, 'cripta.jpg', { opacidad: 0.3, mezcla: 'screen' });

  estilo(ui.body, `
    .ant-ext{display:grid;grid-template-columns:18px 1fr;grid-template-rows:18px auto;max-width:340px;margin:0 auto 6px;font-size:.78rem;color:#a9bccb}
    .ant-letras{grid-column:2;display:grid;grid-template-columns:repeat(${N},1fr);justify-items:center;align-items:center}
    .ant-nums{grid-row:2;display:grid;grid-template-rows:repeat(${N},1fr);justify-items:center;align-items:center}
    .ant-plano{grid-column:2;grid-row:2;display:grid;grid-template-columns:repeat(${N},1fr);gap:3px;padding:5px;border-radius:8px;border:3px solid #4a5a68;background:#05080c}
    .ant-cel{position:relative;aspect-ratio:1;padding:0;border:0;border-radius:5px;cursor:pointer;background:#141b23;color:#ffd9a0;font:800 1.2rem Georgia,serif;touch-action:manipulation;overflow:hidden}
    .ant-cel.luz{background:linear-gradient(180deg,#6b4a1c,#3f2a0e)}
    .ant-cel.mala{background:#7a2a2a}
    .ant-cel.pilar{background:linear-gradient(135deg,#7a8794,#3d4752);cursor:default;color:#fff;border:2px solid #aebccb;box-shadow:inset 0 0 8px rgba(0,0,0,.5);text-shadow:0 1px 2px #000}
    .ant-llama{position:absolute;inset:14%;display:flex;align-items:center;justify-content:center}
    .ant-llama i{display:block;width:44%;height:70%;border-radius:50% 50% 50% 50% / 62% 62% 38% 38%;background:linear-gradient(#fff3b8,#ff9a30 60%,#c2410c);box-shadow:0 0 12px #ffb347;transform:rotate(-8deg)}
    .ant-llama.img{background:var(--img) center/contain no-repeat;mix-blend-mode:screen}
    .ant-llama.img i{display:none}
    .ant-nota{font-size:.78rem;color:#a9bccb}
  `);

  const ext = document.createElement('div');
  ext.className = 'ant-ext';
  const letras = document.createElement('div');
  letras.className = 'ant-letras';
  for (let c = 0; c < N; c++) { const s = document.createElement('span'); s.textContent = LETRAS[c]; letras.appendChild(s); }
  const nums = document.createElement('div');
  nums.className = 'ant-nums';
  for (let r = 0; r < N; r++) { const s = document.createElement('span'); s.textContent = String(r + 1); nums.appendChild(s); }
  const plano = document.createElement('div');
  plano.className = 'ant-plano';
  ext.append(letras, nums, plano);
  const nota = document.createElement('div');
  nota.className = 'ant-nota';
  nota.textContent = 'Los pilares marcados con «?» tienen su número en el plano del maestre (carta 66).';
  ui.body.append(ext, nota);

  const muros = new Set(MUROS);
  const antorchas = new Set();
  const celdas = {};
  let resuelto = false;

  for (let r = 0; r < N; r++) {
    for (let c = 0; c < N; c++) {
      const k = r + ',' + c;
      const b = document.createElement('button');
      b.type = 'button';
      b.dataset.c = k;
      if (muros.has(k)) {
        b.className = 'ant-cel pilar';
        b.disabled = true;
        const oculto = EN_CARTA.includes(k);
        if (k in NUMEROS) b.textContent = oculto ? '?' : String(NUMEROS[k]);
        b.setAttribute('aria-label', 'Pilar ' + LETRAS[c] + (r + 1) + (k in NUMEROS ? (oculto ? ', número en el plano del maestre' : ', ' + NUMEROS[k] + ' antorchas') : ''));
      } else {
        b.className = 'ant-cel';
        b.setAttribute('aria-label', 'Casilla ' + LETRAS[c] + (r + 1));
        b.addEventListener('click', () => {
          if (resuelto) return;
          if (antorchas.has(k)) antorchas.delete(k); else antorchas.add(k);
          pintar();
        });
      }
      celdas[k] = b;
      plano.appendChild(b);
    }
  }

  function ilumina() {
    const luz = new Set();
    antorchas.forEach(k => {
      const [r, c] = k.split(',').map(Number);
      luz.add(k);
      [[1, 0], [-1, 0], [0, 1], [0, -1]].forEach(([dr, dc]) => {
        let y = r + dr, x = c + dc;
        while (y >= 0 && y < N && x >= 0 && x < N && !muros.has(y + ',' + x)) { luz.add(y + ',' + x); y += dr; x += dc; }
      });
    });
    return luz;
  }
  function seVen() {
    const malas = new Set();
    antorchas.forEach(k => {
      const [r, c] = k.split(',').map(Number);
      [[1, 0], [0, 1]].forEach(([dr, dc]) => {
        let y = r + dr, x = c + dc;
        while (y < N && x < N && !muros.has(y + ',' + x)) {
          if (antorchas.has(y + ',' + x)) { malas.add(k); malas.add(y + ',' + x); }
          y += dr; x += dc;
        }
      });
    });
    return malas;
  }
  function vecinas(k) {
    const [r, c] = k.split(',').map(Number);
    return [[1, 0], [-1, 0], [0, 1], [0, -1]].filter(([dr, dc]) => antorchas.has((r + dr) + ',' + (c + dc))).length;
  }

  function pintar() {
    const luz = ilumina();
    const malas = seVen();
    Object.keys(celdas).forEach(k => {
      if (muros.has(k)) return;
      const b = celdas[k];
      const tiene = antorchas.has(k);
      b.dataset.vela = tiene ? '1' : '0';
      b.classList.toggle('luz', luz.has(k) && !malas.has(k));
      b.classList.toggle('mala', malas.has(k));
      const llama = b.querySelector('.ant-llama');
      if (tiene && !llama) {
        const l = document.createElement('span');
        l.className = 'ant-llama';
        l.innerHTML = '<i></i>';
        conImagen(l, 'antorcha.jpg');
        b.appendChild(l);
      } else if (!tiene && llama) llama.remove();
    });
    const oscuras = Object.keys(celdas).filter(k => !muros.has(k) && !luz.has(k)).length;
    const visiblesOk = Object.keys(NUMEROS).filter(k => !EN_CARTA.includes(k)).every(k => vecinas(k) === NUMEROS[k]);
    const ocultosOk = EN_CARTA.every(k => vecinas(k) === NUMEROS[k]);
    if (resuelto) return;
    if (oscuras === 0 && malas.size === 0 && visiblesOk && ocultosOk) {
      resuelto = true;
      guardarPalabra('64', PALABRA);
      ui.say('¡Toda la cripta está iluminada! Las llamas revelan unas palabras grabadas en la piedra. Palabra de la profecía: «' + PALABRA + '». Anotadla. Coged la carta 78.', 'ok');
    } else if (oscuras === 0 && malas.size === 0 && visiblesOk) {
      ui.say('Todo el suelo está iluminado, pero algún pilar marcado con «?» no tiene las antorchas que anota el plano del maestre (carta 66).', 'bad');
    } else {
      ui.say('');
    }
  }

  ui.button('Quitar antorchas', 'ghost', () => { if (!resuelto) { antorchas.clear(); ui.say(''); pintar(); } });
  ui.button('Comprobar', 'primary', () => {
    if (resuelto) return;
    const luz = ilumina();
    const malas = seVen();
    if (malas.size) ui.say('Hay antorchas que se iluminan entre sí (las casillas rojas): ninguna debe iluminar a otra.', 'bad');
    else if (Object.keys(celdas).some(k => !muros.has(k) && !luz.has(k))) ui.say('Quedan casillas del suelo a oscuras: todas deben recibir luz.', 'bad');
    else if (!Object.keys(NUMEROS).filter(k => !EN_CARTA.includes(k)).every(k => vecinas(k) === NUMEROS[k])) ui.say('Algún pilar con número no tiene tantas antorchas pegadas como indica.', 'bad');
    else ui.say('Todo el suelo está iluminado, pero algún pilar marcado con «?» no cumple el plano del maestre (carta 66).', 'bad');
  });

  pintar();
  return { close: ui.close };
}
