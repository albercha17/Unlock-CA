// juegos/70-interruptores.js
// Minijuego: dejar 6 interruptores en el patrón correcto (encendido/apagado),
// igual que el dibujo de estrellas de la nota de Ernesto (carta 39):
// rellena=encendido, vacía=apagado. Patrón: ON, OFF, ON, ON, OFF, ON.
// Exporta startMinigame(opts)

const TARGET = [1, 0, 1, 1, 0, 1];

export function startMinigame(opts = {}) {
  const { onClose, pauseGameTimer, resumeGameTimer } = opts;
  if (typeof pauseGameTimer === 'function') pauseGameTimer();

  const styleId = 'aebi-style';
  if (!document.getElementById(styleId)) {
    const style = document.createElement('style');
    style.id = styleId;
    style.textContent = `
      .aebi-overlay{ position:fixed; inset:0; display:flex; align-items:center; justify-content:center;
        background:rgba(0,0,0,0.7); z-index:2500; padding:12px; font-family:"Poppins",system-ui,-apple-system,Segoe UI,Roboto,Arial; }
      .aebi-box{ width:min(460px,94vw); background:#12121a; border:1px solid rgba(255,255,255,0.1);
        border-radius:14px; padding:20px; color:#fff; box-shadow:0 18px 50px rgba(0,0,0,0.6); text-align:center; }
      .aebi-box h3{ margin:0 0 4px; font-size:1.1rem; }
      .aebi-instr{ margin:0 0 16px; color:#cfcfd6; font-size:0.9rem; }
      .aebi-row{ display:flex; gap:10px; justify-content:center; margin-bottom:16px; flex-wrap:wrap; }
      .aebi-switch{ width:56px; height:96px; border-radius:28px; background:#2a2a38; border:2px solid rgba(255,255,255,0.15);
        position:relative; cursor:pointer; display:flex; align-items:flex-end; padding:4px; }
      .aebi-switch.on{ background:linear-gradient(180deg,#ffcf6b,#ff9d1f); align-items:flex-start; }
      .aebi-knob{ width:100%; height:44px; border-radius:22px; background:#fff; box-shadow:0 4px 10px rgba(0,0,0,0.4); }
      .aebi-feedback{ min-height:1.4em; font-weight:700; margin-bottom:10px; }
      .aebi-feedback.ok{ color:#9dffb0; }
      .aebi-feedback.bad{ color:#ffb3b3; }
      .aebi-actions{ display:flex; gap:10px; justify-content:center; }
      .aebi-btn{ padding:10px 16px; border-radius:10px; border:none; font-weight:700; cursor:pointer; }
      .aebi-btn.primary{ background:linear-gradient(180deg,#ffcf6b,#ff9d1f); color:#2a1600; }
      .aebi-btn.ghost{ background:#2d2f33; color:#fff; border:1px solid rgba(255,255,255,0.1); }
    `;
    document.head.appendChild(style);
  }

  const overlay = document.createElement('div');
  overlay.className = 'aebi-overlay';
  overlay.innerHTML = `
    <div class="aebi-box">
      <h3>Carta 70 — Cuadro de interruptores</h3>
      <p class="aebi-instr">Toca los interruptores hasta reproducir el patrón del dibujo de estrellas de la nota (carta 39).</p>
      <div class="aebi-row" id="aebiRow"></div>
      <div class="aebi-feedback" id="aebiFeedback"></div>
      <div class="aebi-actions">
        <button class="aebi-btn primary" id="aebiCheck">Comprobar</button>
        <button class="aebi-btn ghost" id="aebiClose">Cerrar</button>
      </div>
    </div>
  `;
  document.body.appendChild(overlay);

  const row = overlay.querySelector('#aebiRow');
  const feedback = overlay.querySelector('#aebiFeedback');
  const state = TARGET.map(() => 0);

  function render() {
    row.innerHTML = '';
    state.forEach((v, i) => {
      const sw = document.createElement('div');
      sw.className = 'aebi-switch' + (v ? ' on' : '');
      sw.innerHTML = '<div class="aebi-knob"></div>';
      sw.addEventListener('click', () => {
        state[i] = state[i] ? 0 : 1;
        feedback.textContent = '';
        render();
      });
      row.appendChild(sw);
    });
  }
  render();

  overlay.querySelector('#aebiCheck').addEventListener('click', () => {
    const ok = state.every((v, i) => v === TARGET[i]);
    if (ok) {
      feedback.textContent = '¡Correcto! La caseta queda arreglada del todo. Coged la carta 80.';
      feedback.className = 'aebi-feedback ok';
      overlay.querySelectorAll('.aebi-switch').forEach(s => s.style.pointerEvents = 'none');
    } else {
      feedback.textContent = 'Ese patrón no enciende nada. Revisad de nuevo el dibujo de estrellas.';
      feedback.className = 'aebi-feedback bad';
    }
  });

  function close() {
    document.removeEventListener('keydown', onKey);
    overlay.remove();
    if (typeof resumeGameTimer === 'function') resumeGameTimer();
    if (typeof onClose === 'function') onClose();
  }
  overlay.querySelector('#aebiClose').addEventListener('click', close);
  function onKey(e){ if (e.key === 'Escape') close(); }
  document.addEventListener('keydown', onKey);

  return { close };
}
