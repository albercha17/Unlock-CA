// juegos/12-farola.js
// Minijuego: teclado numérico de 3 cifras en la base de la farola.
// Código correcto: 249 (casas 4, 9, 2 del plano de Ernesto, ordenadas de menor a mayor).
// Exporta startMinigame(opts)

const CODE = '249';

export function startMinigame(opts = {}) {
  const { onClose, pauseGameTimer, resumeGameTimer } = opts;
  if (typeof pauseGameTimer === 'function') pauseGameTimer();

  const styleId = 'aeb-farola-style';
  if (!document.getElementById(styleId)) {
    const style = document.createElement('style');
    style.id = styleId;
    style.textContent = `
      .aeb-overlay{ position:fixed; inset:0; display:flex; align-items:center; justify-content:center;
        background:rgba(0,0,0,0.7); z-index:2500; padding:12px; font-family:"Poppins",system-ui,-apple-system,Segoe UI,Roboto,Arial; }
      .aeb-box{ width:min(380px,92vw); background:linear-gradient(180deg,#1b1b2f,#151527); border:1px solid rgba(255,255,255,0.12);
        border-radius:14px; padding:20px; color:#fff; box-shadow:0 18px 50px rgba(0,0,0,0.6); text-align:center; }
      .aeb-box h3{ margin:0 0 6px; font-size:1.1rem; }
      .aeb-box p.aeb-instr{ margin:0 0 14px; color:#cfcfd6; font-size:0.9rem; }
      .aeb-display{ font-size:1.8rem; font-weight:800; letter-spacing:6px; background:rgba(255,255,255,0.05);
        border:1px solid rgba(255,255,255,0.08); border-radius:10px; padding:10px 0; margin-bottom:14px; min-height:44px; }
      .aeb-keypad{ display:grid; grid-template-columns:repeat(3,1fr); gap:8px; margin-bottom:14px; }
      .aeb-key{ background:linear-gradient(180deg,rgba(255,255,255,0.08),rgba(255,255,255,0.02)); border:1px solid rgba(255,255,255,0.08);
        color:#fff; padding:14px 0; border-radius:10px; font-size:1.15rem; font-weight:700; cursor:pointer; }
      .aeb-key:active{ transform:translateY(1px); }
      .aeb-feedback{ min-height:1.4em; margin-bottom:10px; font-weight:700; }
      .aeb-feedback.ok{ color:#9dffb0; }
      .aeb-feedback.bad{ color:#ffb3b3; }
      .aeb-actions{ display:flex; gap:10px; justify-content:center; }
      .aeb-btn{ padding:10px 16px; border-radius:10px; border:none; font-weight:700; cursor:pointer; }
      .aeb-btn.primary{ background:linear-gradient(180deg,#ffcf6b,#ff9d1f); color:#2a1600; }
      .aeb-btn.ghost{ background:#2d2f33; color:#fff; border:1px solid rgba(255,255,255,0.1); }
    `;
    document.head.appendChild(style);
  }

  const overlay = document.createElement('div');
  overlay.className = 'aeb-overlay';
  overlay.innerHTML = `
    <div class="aeb-box">
      <h3>Carta 12 — Farola con teclado</h3>
      <p class="aeb-instr">Introduce el código de 3 cifras del plano del barrio.</p>
      <div class="aeb-display" id="aebDisplay">—</div>
      <div class="aeb-keypad" id="aebKeypad"></div>
      <div class="aeb-feedback" id="aebFeedback"></div>
      <div class="aeb-actions">
        <button class="aeb-btn ghost" id="aebClear">Borrar</button>
        <button class="aeb-btn primary" id="aebOk">Comprobar</button>
        <button class="aeb-btn ghost" id="aebClose">Cerrar</button>
      </div>
    </div>
  `;
  document.body.appendChild(overlay);

  const display = overlay.querySelector('#aebDisplay');
  const feedback = overlay.querySelector('#aebFeedback');
  const keypad = overlay.querySelector('#aebKeypad');
  let entered = '';

  function render() {
    display.textContent = entered === '' ? '—' : entered;
  }

  ['1','2','3','4','5','6','7','8','9','⌫','0','✓'].forEach(k => {
    const btn = document.createElement('button');
    btn.className = 'aeb-key';
    btn.textContent = k;
    btn.addEventListener('click', () => {
      if (k === '⌫') { entered = entered.slice(0, -1); render(); return; }
      if (k === '✓') { checkCode(); return; }
      if (entered.length < 3) { entered += k; render(); }
    });
    keypad.appendChild(btn);
  });

  function checkCode() {
    if (entered === CODE) {
      feedback.textContent = '¡Correcto! La tapa se abre. Coged la carta 63.';
      feedback.className = 'aeb-feedback ok';
      overlay.querySelectorAll('.aeb-key').forEach(b => b.disabled = true);
    } else {
      feedback.textContent = 'Código incorrecto. Revisad el plano del barrio.';
      feedback.className = 'aeb-feedback bad';
    }
  }

  overlay.querySelector('#aebClear').addEventListener('click', () => { entered=''; feedback.textContent=''; render(); });
  overlay.querySelector('#aebOk').addEventListener('click', checkCode);

  function close() {
    document.removeEventListener('keydown', onKey);
    overlay.remove();
    if (typeof resumeGameTimer === 'function') resumeGameTimer();
    if (typeof onClose === 'function') onClose();
  }
  overlay.querySelector('#aebClose').addEventListener('click', close);
  function onKey(e){ if (e.key === 'Escape') close(); }
  document.addEventListener('keydown', onKey);

  render();
  return { close };
}
