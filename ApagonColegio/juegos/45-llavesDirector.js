/*
  ./juegos/45-llavesDirector.js
  Minijuego: 20 llaves coloreadas usando un PNG de silueta (mask).
  Requisitos: coloca el PNG (silhouette, blanca/opaque sobre transparente) en:
    ./images/llave.png (o ajusta KEY_PNG)
  Exporta: startMinigame(opts)
    opts:
      - onClose(resultBoolean)
      - pauseGameTimer()
      - resumeGameTimer()

  También expone window.startMinijuegoLlaves para pruebas directas.
*/

const KEY_PNG = './images/llave.png'; // <-- ajusta si hace falta

function makeStyles() {
  return `
/* estilos del minijuego de llaves (imagen máscara + contorno) */
.mlj-root {
  position: fixed;
  inset: 0;
  z-index: 12000;
  display:flex;
  align-items:center;
  justify-content:center;
  background: linear-gradient(180deg, rgba(2,6,23,0.75), rgba(2,6,23,0.9));
  font-family: "Poppins", system-ui, -apple-system, "Segoe UI", Roboto, Arial;
  -webkit-font-smoothing:antialiased;
  -moz-osx-font-smoothing:grayscale;
}
.mlj-panel {
  width: min(980px, 94%);
  background: linear-gradient(180deg,#071022,#081426);
  border-radius: 12px;
  padding: 18px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.6);
  color: #eef6ff;
  text-align: center;
}
.mlj-header { display:flex; align-items:center; gap:12px; justify-content:space-between; margin-bottom:10px; }
.mlj-title { font-size:20px; font-weight:800; letter-spacing:0.6px; }
.mlj-sub { font-size:13px; color: #c9d7e6; opacity:0.9; }

.mlj-board {
  display:grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 12px;
  margin: 18px 0;
  justify-items:center;
}

/* botón de llave: ahora es contenedor; la forma la crean .k-outline y .k-fill */
.mlj-key {
  --size: 88px;
  width: var(--size);
  height: calc(var(--size) * 0.62);
  display:inline-flex;
  align-items:center;
  justify-content:center;
  cursor: pointer;
  user-select: none;
  border-radius: 10px;
  padding: 0;
  background: transparent;
  border: none;
  transition: transform 200ms cubic-bezier(.2,.9,.3,1), filter 160ms, box-shadow 160ms;
  outline: none;
  position: relative;
  overflow: visible;
  -webkit-tap-highlight-color: transparent;
}

/* contorno negro mediante máscara aplicada a un pseudo-elemento interno */
.mlj-key .k-outline,
.mlj-key .k-fill {
  position: absolute;
  inset: 0;
  display:block;
  -webkit-mask-image: url("${KEY_PNG}");
  -webkit-mask-size: contain;
  -webkit-mask-position: center;
  -webkit-mask-repeat: no-repeat;
  mask-image: url("${KEY_PNG}");
  mask-size: contain;
  mask-position: center;
  mask-repeat: no-repeat;
  border-radius: 6px;
  pointer-events: none; /* clicks los recibe el botón */
}

/* outline: negro, ligeramente escalado para crear borde visual */
.mlj-key .k-outline {
  background: rgba(0,0,0,0.95);
  transform: scale(1.06);
  z-index: 0;
}

/* fill: el color real de la llave (se establece inline) */
.mlj-key .k-fill {
  z-index: 1;
  transform: scale(1);
}

/* label sobre la cabeza (número) */
.mlj-key .k-label {
  position: absolute;
  top: 8%;
  left: 18%;
  transform: translate(-10%, 0);
  font-weight: 800;
  font-size: 13px;
  color: rgba(255,255,255,0.95);
  text-shadow: 0 1px 0 rgba(0,0,0,0.35);
  pointer-events: none;
  z-index: 2;
}

/* hover / focus */
.mlj-key:focus { transform: translateY(-6px) scale(1.03); box-shadow: 0 16px 36px rgba(0,0,0,0.6); }
.mlj-key:hover { transform: translateY(-6px) scale(1.03); }

/* success / fail */
.mlj-key.success { transform: translateY(-10px) scale(1.06); box-shadow: 0 18px 40px rgba(40,200,120,0.12); }
.mlj-key.fail { animation: shake-key 480ms; box-shadow: 0 6px 18px rgba(220,40,60,0.10); }
@keyframes shake-key {
  0% { transform: translateX(0) rotate(0deg); }
  20% { transform: translateX(-8px) rotate(-5deg); }
  40% { transform: translateX(8px) rotate(5deg); }
  60% { transform: translateX(-6px) rotate(-3deg); }
  80% { transform: translateX(6px) rotate(3deg); }
  100% { transform: translateX(0) rotate(0deg); }
}

/* small board shake when shuffled */
.mlj-board.shake {
  animation: boardShake 380ms linear;
}
@keyframes boardShake {
  0% { transform: translateY(0); }
  25% { transform: translateY(-6px); }
  50% { transform: translateY(0); }
  75% { transform: translateY(-4px); }
  100% { transform: translateY(0); }
}

/* responsive */
@media (max-width:620px) {
  .mlj-board { grid-template-columns: repeat(4, 1fr); gap:10px; }
  .mlj-key { --size: 72px; }
  .mlj-key .k-label { font-size:12px; left:16%; top:10%; transform: translate(-10%,0); }
}

.mlj-controls { display:flex; gap:8px; justify-content:center; margin-top: 10px; }
.mlj-btn {
  background: linear-gradient(180deg,#2fd09f,#0db07e);
  border-radius: 10px;
  border: none;
  padding: 8px 14px;
  font-weight:800;
  color:#042617;
  cursor:pointer;
  box-shadow: 0 8px 28px rgba(3,43,30,0.35);
}
.mlj-btn.ghost { background: transparent; border: 1px solid rgba(255,255,255,0.06); color:#d8edf0; box-shadow:none; }

.mlj-hint { font-size:13px; color:#bedae6; margin-top:8px; }
`;
}

function shuffleArray(a) {
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

export function startMinigame(opts = {}) {
  const { onClose, pauseGameTimer, resumeGameTimer } = opts;
  if (typeof pauseGameTimer === 'function') pauseGameTimer();

  // inject styles once
  if (!document.getElementById('mlj-styles')) {
    const s = document.createElement('style');
    s.id = 'mlj-styles';
    s.innerHTML = makeStyles();
    document.head.appendChild(s);
  }

  // root panel
  const root = document.createElement('div');
  root.className = 'mlj-root';
  root.setAttribute('role','dialog');
  root.setAttribute('aria-modal','true');

  const panel = document.createElement('div');
  panel.className = 'mlj-panel';

  const header = document.createElement('div');
  header.className = 'mlj-header';
  const titleWrap = document.createElement('div');
  titleWrap.innerHTML = `<div class="mlj-title">Elige la llave correcta</div><div class="mlj-sub">Hay 20 llaves. Si fallas, se reordenan.</div>`;
  const closeBtn = document.createElement('button');
  closeBtn.className = 'mlj-btn ghost';
  closeBtn.textContent = 'Cerrar';
  closeBtn.onclick = () => cleanup(false);
  header.appendChild(titleWrap);
  header.appendChild(closeBtn);
  panel.appendChild(header);

  const board = document.createElement('div');
  board.className = 'mlj-board';
  panel.appendChild(board);

  const info = document.createElement('div');
  info.className = 'mlj-hint';
  info.textContent = 'Pulsa una llave para seleccionar. Si fallas, las llaves se mezclan.';
  panel.appendChild(info);

  const controls = document.createElement('div');
  controls.className = 'mlj-controls';
  const btnShuffle = document.createElement('button');
  btnShuffle.className = 'mlj-btn ghost';
  btnShuffle.textContent = 'Mezclar';
  btnShuffle.onclick = () => shuffleAndRender();
  const btnGiveUp = document.createElement('button');
  btnGiveUp.className = 'mlj-btn';
  btnGiveUp.textContent = 'Rendirse';
  btnGiveUp.onclick = () => cleanup(false);
  controls.appendChild(btnShuffle);
  controls.appendChild(btnGiveUp);
  panel.appendChild(controls);

  root.appendChild(panel);
  document.body.appendChild(root);

  // build keys
  const total = 20;
  const keys = [];
  for (let i = 0; i < total; i++) {
    const hue = Math.round((i * 360 / total) % 360);
    const sat = 72 + (i % 3) * 2;
    const light = 52 - (i % 4);
    const color = `hsl(${hue} ${sat}% ${light}%)`; // space-separated HSL
    keys.push({ id: `k${i+1}`, color, label: `` });
  }

  // FIXED correct key: la morada (hue ~270) corresponde al índice 15 -> id 'k16'
  const correctKeyId = 'k16';

  let locked = false;
  let attempt = 0;

  function renderKeys(order = keys) {
    board.innerHTML = '';
    order.forEach(k => {
      const btn = document.createElement('button');
      btn.className = 'mlj-key';
      btn.dataset.keyId = k.id;
      btn.setAttribute('aria-label', `Llave ${k.label}`);
      btn.setAttribute('title', `Llave ${k.label}`);

      // estructura interna: outline (negro) + fill (color) + label
      const outline = document.createElement('div');
      outline.className = 'k-outline';
      // no pointer events on inner elements
      outline.style.pointerEvents = 'none';

      const fill = document.createElement('div');
      fill.className = 'k-fill';
      fill.style.background = k.color;

      const label = document.createElement('div');
      label.className = 'k-label';
      label.textContent = k.label;

      btn.appendChild(outline);
      btn.appendChild(fill);
      btn.appendChild(label);

      btn.tabIndex = 0;
      btn.addEventListener('click', onKeyClick);
      btn.addEventListener('keydown', (ev) => {
        if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); btn.click(); }
      });
      board.appendChild(btn);
    });
  }

  function onKeyClick(e) {
    if (locked) return;
    locked = true;
    const btn = e.currentTarget;
    const keyId = btn.dataset.keyId;
    attempt++;

    if (keyId === correctKeyId) {
      btn.classList.add('success');
      setTimeout(()=> showResult(true), 700);
    } else {
      btn.classList.add('fail');
      setTimeout(()=> {
        Array.from(board.children).forEach(c => c.classList.remove('fail'));
        shuffleAndRender();
        locked = false;
      }, 520);
    }
  }

  function shuffleAndRender() {
    shuffleArray(keys);
    // small shake cue
    board.classList.add('shake');
    setTimeout(()=> board.classList.remove('shake'), 420);
    renderKeys(keys);
  }

  function showResult(ok) {
    const msg = document.createElement('div');
    msg.style.padding = '14px';
    msg.style.borderRadius = '10px';
    msg.style.background = ok ? 'linear-gradient(180deg,#e6fff0,#dbffea)' : 'linear-gradient(180deg,#fff0f0,#ffecec)';
    msg.style.color = ok ? '#064829' : '#6b0b0b';
    msg.style.fontWeight = 800;
    msg.style.marginTop = '12px';
    msg.textContent = ok ? `¡Correcto! Coge la carta 4` : 'Incorrecto';
    panel.appendChild(msg);;
  }

  function cleanup(result) {
    if (document.body.contains(root)) document.body.removeChild(root);
    if (typeof resumeGameTimer === 'function') resumeGameTimer();
    if (typeof onClose === 'function') onClose(result === true);
  }

  // initial render
  renderKeys(keys);
  setTimeout(()=> { const first = board.querySelector('.mlj-key'); if(first) first.focus(); }, 120);

  return { root, getState: () => ({ correctKeyId, attempt }), pickCorrect: () => { /* no-op: correct is fixed */ } };
}

// expose for dev testing
if (typeof window !== 'undefined') window.startMinijuegoLlaves = startMinigame;