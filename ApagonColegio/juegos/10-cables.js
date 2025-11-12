// ./juegos/41-secuenciaPuerta.js

const TARGET_SEQUENCE = ["18", "34", "66", "35", "78", "81", "53"];

function makeStyles() {
  return `
.msp-root{
  position:fixed; inset:0; z-index:12000;
  display:flex; align-items:center; justify-content:center;
  background:linear-gradient(180deg, rgba(2,6,23,.80), rgba(2,6,23,.92));
  font-family:"Poppins", system-ui, -apple-system, "Segoe UI", Roboto, Arial;
}
.msp-panel{
  width:min(720px,94vw);
  background:linear-gradient(180deg,#0b1220,#081018);
  border:1px solid rgba(255,255,255,.06);
  border-radius:16px;
  color:#eaf2ff;
  padding:18px;
  box-shadow:0 18px 46px rgba(0,0,0,.55);
}
.msp-header{display:flex; align-items:center; justify-content:space-between; gap:12px;}
.msp-title{font-weight:900; letter-spacing:.06em; font-size:1.05rem;}
.msp-sub{color:#c9d7e6; opacity:.85; font-size:.9rem; margin-top:4px}

.msp-grid{
  display:grid; gap:12px; margin-top:14px;
  grid-template-columns: repeat(4, 1fr);
}
@media (max-width:540px){ .msp-grid{ grid-template-columns: repeat(3, 1fr); } }

/* BOTONES REDONDOS */
.msp-btn{
  aspect-ratio: 1 / 1; /* círculo */
  display:flex; align-items:center; justify-content:center;
  border:none; border-radius:9999px; cursor:pointer;
  font-weight:900; font-size:1.1rem; letter-spacing:.04em;
  background:linear-gradient(180deg,#162030,#0e1622);
  color:#eaf2ff;
  box-shadow:0 10px 26px rgba(0,0,0,.45), inset 0 0 0 1px rgba(255,255,255,.06);
  transition: transform .15s ease, box-shadow .15s ease, background .15s ease;
}
.msp-btn:focus{ outline:none; transform: translateY(-4px) }
.msp-btn:active{ transform: translateY(1px) scale(.99) }

.msp-progress{
  margin-top:10px; font-size:.92rem; color:#a7bed8;
}
.msp-progress b{ color:#e2f0ff }

.msp-controls{ display:flex; gap:8px; justify-content:flex-end; margin-top:12px }
.msp-ghost, .msp-primary{
  padding:8px 14px; border-radius:10px; font-weight:800; border:1px solid transparent; cursor:pointer;
}
.msp-ghost{ background:transparent; color:#eaf2ff; border-color:rgba(255,255,255,.06); }
.msp-primary{ background:linear-gradient(180deg,#2fd09f,#0db07e); color:#042617; box-shadow: 0 10px 28px rgba(3,43,30,.35); }

.msp-grid.shake{ animation:msp-shake .36s ease }
@keyframes msp-shake{
  0%{transform:translateX(0)}
  25%{transform:translateX(-6px)}
  50%{transform:translateX(6px)}
  75%{transform:translateX(-4px)}
  100%{transform:translateX(0)}
}

.msp-toast{
  margin-top:10px;
  background:rgba(20,83,45,.14);
  color:#bbf7d0; border:1px solid rgba(34,197,94,.35);
  padding:8px 12px; border-radius:10px; font-weight:800; text-align:center;
  display:none;
}
.msp-toast.error{
  background:rgba(127,29,29,.12);
  color:#fecaca; border-color: rgba(239,68,68,.35);
}

.msp-success{
  display:none; margin-top:12px; padding:14px;
  border-radius:12px; text-align:center; font-weight:900; line-height:1.25;
  background:linear-gradient(180deg,#e6fff0,#dbffea); color:#064829;
  border:1px solid rgba(34,197,94,.35);
  white-space:pre-line;
}
`;
}

function shuffle(arr){
  for(let i=arr.length-1;i>0;i--){
    const j = Math.floor(Math.random()*(i+1));
    [arr[i],arr[j]]=[arr[j],arr[i]];
  }
  return arr;
}

export function startMinigame(opts = {}){
  const { onClose, pauseGameTimer, resumeGameTimer } = opts;
  if(typeof pauseGameTimer === 'function') pauseGameTimer();

  if(!document.getElementById('msp-styles')){
    const st = document.createElement('style');
    st.id = 'msp-styles';
    st.textContent = makeStyles();
    document.head.appendChild(st);
  }

  const root = document.createElement('div');
  root.className = 'msp-root';
  root.setAttribute('role','dialog');
  root.setAttribute('aria-modal','true');

  const panel = document.createElement('div');
  panel.className = 'msp-panel';

  const header = document.createElement('div');
  header.className = 'msp-header';
  const left = document.createElement('div');
  left.innerHTML = `<div class="msp-title">Panel de Secuencia</div>
                    <div class="msp-sub">Pulsa los números en el orden correcto.</div>`;
  const closeBtn = document.createElement('button');
  closeBtn.className = 'msp-ghost';
  closeBtn.textContent = 'Cerrar';
  closeBtn.onclick = () => cleanup(false); // si cierras manual sin completar
  header.appendChild(left);
  header.appendChild(closeBtn);

  const grid = document.createElement('div');
  grid.className = 'msp-grid';
  const numbers = shuffle([...TARGET_SEQUENCE]);

  const progress = document.createElement('div');
  progress.className = 'msp-progress';

  const toast = document.createElement('div');
  toast.className = 'msp-toast';

  const success = document.createElement('div');
  success.className = 'msp-success';
  success.textContent = 'PUERTA ABIERTA.\nCoge la carta 41';

  const controls = document.createElement('div');
  controls.className = 'msp-controls';
  const resetBtn = document.createElement('button');
  resetBtn.className = 'msp-ghost';
  resetBtn.textContent = 'Reiniciar';
  const exitBtn = document.createElement('button');
  exitBtn.className = 'msp-primary';
  exitBtn.textContent = 'Cerrar'; // al gusto: cierra siempre
  controls.appendChild(resetBtn);
  controls.appendChild(exitBtn);

  panel.appendChild(header);
  panel.appendChild(grid);
  panel.appendChild(progress);
  panel.appendChild(toast);
  panel.appendChild(success);
  panel.appendChild(controls);
  root.appendChild(panel);
  document.body.appendChild(root);

  let idx = 0;
  let completed = false;

  renderButtons();
  updateProgress();
  toastHide();

  function renderButtons(){
    grid.innerHTML = '';
    numbers.forEach(n=>{
      const btn = document.createElement('button');
      btn.className = 'msp-btn';
      btn.textContent = n;
      btn.setAttribute('aria-label', `Número ${n}`);
      btn.addEventListener('click', ()=> onPick(n, btn));
      grid.appendChild(btn);
    });
  }

  function onPick(n, btn){
    if (completed) return;
    const expected = TARGET_SEQUENCE[idx];
    if(n === expected){
      btn.style.background = 'linear-gradient(180deg,#183329,#0f241a)';
      btn.style.boxShadow = '0 10px 26px rgba(3,43,30,.35), inset 0 0 0 1px rgba(46,204,149,.55)';
      btn.style.color = '#b6f3d8';
      idx++;
      updateProgress();
      if(idx === TARGET_SEQUENCE.length){
        completed = true;
        grid.style.pointerEvents = 'none';
        toastHide();
        success.style.display = 'block';
        // NO cerrar automáticamente: esperar a que el usuario pulse "Cerrar"
        // Si quieres notificar éxito al juego sin cerrar:
        if (typeof onClose === 'function') onClose(true);
      }
    } else {
      grid.classList.remove('shake'); void grid.offsetWidth; grid.classList.add('shake');
      toast.className = 'msp-toast error';
      toast.textContent = 'Orden incorrecto. Secuencia reiniciada.';
      toast.style.display = 'block';
      idx = 0;
      updateProgress();
      Array.from(grid.children).forEach(b=> b.removeAttribute('style'));
      setTimeout(toastHide, 1200);
    }
  }

  function updateProgress(){
    // Solo mostrar lo ya acertado, sin revelar el siguiente
    const count = idx;
    const total = TARGET_SEQUENCE.length;
    const done = TARGET_SEQUENCE.slice(0, idx).join(' → ') || '—';
    progress.innerHTML = `Progreso: <b>${count}/${total}</b> &nbsp;|&nbsp; Pulsados: <b>${done}</b>`;
  }

  function toastHide(){ toast.style.display = 'none'; }

  resetBtn.onclick = ()=>{
    if (completed) return; // si ya has abierto la puerta, no tiene sentido reiniciar
    idx = 0;
    updateProgress();
    Array.from(grid.children).forEach(b=> b.removeAttribute('style'));
    toastHide();
    grid.classList.remove('shake');
  };

  exitBtn.onclick = ()=> cleanup(completed);

  function onKey(e){
    if(e.key === 'Escape'){ e.preventDefault(); cleanup(completed); }
  }
  document.addEventListener('keydown', onKey);

  function cleanup(ok){
    document.removeEventListener('keydown', onKey);
    if(document.body.contains(root)) document.body.removeChild(root);
    if(typeof resumeGameTimer === 'function') resumeGameTimer();
    // onClose(true) ya se lanzó al completar; si cierran sin completar, manda false.
    if(typeof onClose === 'function' && !ok) onClose(false);
  }

  return {
    root,
    getProgress: ()=> ({ idx, total: TARGET_SEQUENCE.length, done: TARGET_SEQUENCE.slice(0, idx) }),
    reset: ()=> resetBtn.click()
  };
}

if(typeof window !== 'undefined'){
  window.startMinijuegoSecuencia = startMinigame;
}
