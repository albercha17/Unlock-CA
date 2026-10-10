// juegos/95-final.js
// Minijuego final: introducir la palabra formada por las 5 letras ocultas
// reveladas con el llavero morado (cartas 63=I, 28=P, 39=A, 71=L, 90=S).
// Palabra correcta: PILAS.
// Exporta startMinigame(opts)

const WORD = 'PILAS';

export function startMinigame(opts = {}) {
  const { onClose, pauseGameTimer, resumeGameTimer } = opts;
  if (typeof pauseGameTimer === 'function') pauseGameTimer();

  const styleId = 'aebf-style';
  if (!document.getElementById(styleId)) {
    const style = document.createElement('style');
    style.id = styleId;
    style.textContent = `
      .aebf-overlay{ position:fixed; inset:0; display:flex; align-items:center; justify-content:center;
        background:rgba(0,0,0,0.75); z-index:2500; padding:12px; font-family:"Poppins",system-ui,-apple-system,Segoe UI,Roboto,Arial; }
      .aebf-box{ width:min(460px,94vw); background:#12121a; border:1px solid rgba(255,255,255,0.1);
        border-radius:14px; padding:20px; color:#fff; box-shadow:0 18px 50px rgba(0,0,0,0.6); text-align:center; }
      .aebf-box h3{ margin:0 0 4px; font-size:1.1rem; }
      .aebf-instr{ margin:0 0 16px; color:#cfcfd6; font-size:0.9rem; }
      .aebf-display{ font-size:1.8rem; font-weight:900; letter-spacing:8px; background:rgba(255,255,255,0.05);
        border:1px solid rgba(255,255,255,0.08); border-radius:10px; padding:10px 0; margin-bottom:14px; min-height:44px; }
      .aebf-keyboard{ display:grid; grid-template-columns:repeat(7,1fr); gap:6px; margin-bottom:14px; }
      .aebf-key{ background:linear-gradient(180deg,rgba(255,255,255,0.08),rgba(255,255,255,0.02)); border:1px solid rgba(255,255,255,0.08);
        color:#fff; padding:10px 0; border-radius:8px; font-size:1rem; font-weight:700; cursor:pointer; }
      .aebf-key:active{ transform:translateY(1px); }
      .aebf-feedback{ min-height:1.4em; margin-bottom:10px; font-weight:700; }
      .aebf-feedback.ok{ color:#9dffb0; }
      .aebf-feedback.bad{ color:#ffb3b3; }
      .aebf-actions{ display:flex; gap:10px; justify-content:center; }
      .aebf-btn{ padding:10px 16px; border-radius:10px; border:none; font-weight:700; cursor:pointer; }
      .aebf-btn.primary{ background:linear-gradient(180deg,#ffcf6b,#ff9d1f); color:#2a1600; }
      .aebf-btn.ghost{ background:#2d2f33; color:#fff; border:1px solid rgba(255,255,255,0.1); }
    `;
    document.head.appendChild(style);
  }

  const overlay = document.createElement('div');
  overlay.className = 'aebf-overlay';
  overlay.innerHTML = `
    <div class="aebf-box">
      <h3>Carta 95 — Cuadro general del barrio</h3>
      <p class="aebf-instr">Escribe la palabra formada por las 5 letras que habéis descubierto con el llavero morado.</p>
      <div class="aebf-display" id="aebfDisplay">—</div>
      <div class="aebf-keyboard" id="aebfKeyboard"></div>
      <div class="aebf-feedback" id="aebfFeedback"></div>
      <div class="aebf-actions">
        <button class="aebf-btn ghost" id="aebfClear">Borrar</button>
        <button class="aebf-btn primary" id="aebfOk">Comprobar</button>
        <button class="aebf-btn ghost" id="aebfClose">Cerrar</button>
      </div>
    </div>
  `;
  document.body.appendChild(overlay);

  const display = overlay.querySelector('#aebfDisplay');
  const feedback = overlay.querySelector('#aebfFeedback');
  const keyboard = overlay.querySelector('#aebfKeyboard');
  let entered = '';

  function render() {
    display.textContent = entered === '' ? '—' : entered;
  }

  const LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
  LETTERS.forEach(letter => {
    const btn = document.createElement('button');
    btn.className = 'aebf-key';
    btn.textContent = letter;
    btn.addEventListener('click', () => {
      if (entered.length < WORD.length) { entered += letter; render(); }
    });
    keyboard.appendChild(btn);
  });

  function checkWord() {
    if (entered === WORD) {
      feedback.textContent = '¡Correcto! Toda la calle se ilumina de golpe. Coged la carta 99.';
      feedback.className = 'aebf-feedback ok';
      overlay.querySelectorAll('.aebf-key').forEach(b => b.disabled = true);
    } else {
      feedback.textContent = 'Esa palabra no enciende nada. Revisad las 5 letras.';
      feedback.className = 'aebf-feedback bad';
    }
  }

  overlay.querySelector('#aebfClear').addEventListener('click', () => { entered=''; feedback.textContent=''; render(); });
  overlay.querySelector('#aebfOk').addEventListener('click', checkWord);

  function close() {
    document.removeEventListener('keydown', onKey);
    overlay.remove();
    if (typeof resumeGameTimer === 'function') resumeGameTimer();
    if (typeof onClose === 'function') onClose();
  }
  overlay.querySelector('#aebfClose').addEventListener('click', close);
  function onKey(e){ if (e.key === 'Escape') close(); }
  document.addEventListener('keydown', onKey);

  render();
  return { close };
}
