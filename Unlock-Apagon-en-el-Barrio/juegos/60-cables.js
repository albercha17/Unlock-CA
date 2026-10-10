// juegos/60-cables.js
// Minijuego: ordenar 4 cables (rojo, azul, amarillo, verde) según los números
// casi borrados de las cartas 61,62,64,66 (rojo=2, azul=4, amarillo=1, verde=3).
// Orden correcto (de menor a mayor): amarillo, rojo, verde, azul.
// Exporta startMinigame(opts)

export function startMinigame(opts = {}) {
  const { onClose, pauseGameTimer, resumeGameTimer } = opts;
  if (typeof pauseGameTimer === 'function') pauseGameTimer();

  const CABLES = [
    { id: 'amarillo', color: '#f5d306', num: 1 },
    { id: 'rojo',     color: '#e63946', num: 2 },
    { id: 'verde',    color: '#2fbf71', num: 3 },
    { id: 'azul',     color: '#3a86ff', num: 4 }
  ];
  const CORRECT_ORDER = ['amarillo', 'rojo', 'verde', 'azul'];

  const styleId = 'aeb-cables-style';
  if (!document.getElementById(styleId)) {
    const style = document.createElement('style');
    style.id = styleId;
    style.textContent = `
      .aebc-overlay{ position:fixed; inset:0; display:flex; align-items:center; justify-content:center;
        background:rgba(0,0,0,0.7); z-index:2500; padding:12px; font-family:"Poppins",system-ui,-apple-system,Segoe UI,Roboto,Arial; }
      .aebc-box{ width:min(480px,94vw); background:#12121a; border:1px solid rgba(255,255,255,0.1);
        border-radius:14px; padding:20px; color:#fff; box-shadow:0 18px 50px rgba(0,0,0,0.6); }
      .aebc-box h3{ margin:0 0 4px; text-align:center; font-size:1.1rem; }
      .aebc-instr{ margin:0 0 16px; color:#cfcfd6; font-size:0.9rem; text-align:center; }
      .aebc-row{ display:flex; gap:10px; justify-content:center; flex-wrap:wrap; margin-bottom:14px; }
      .aebc-cable{ width:70px; height:90px; border-radius:10px; display:flex; align-items:center; justify-content:center;
        color:#111; font-weight:900; font-size:0.85rem; cursor:pointer; user-select:none; box-shadow:0 8px 20px rgba(0,0,0,0.4);
        border:3px solid rgba(255,255,255,0.15); transition:transform .12s; }
      .aebc-cable.selected{ transform:translateY(-6px) scale(1.05); border-color:#fff; }
      .aebc-slot{ width:70px; height:90px; border-radius:10px; border:2px dashed rgba(255,255,255,0.25);
        display:flex; align-items:center; justify-content:center; background:rgba(255,255,255,0.03); }
      .aebc-slot.highlight{ border-color:#fff; }
      .aebc-label{ text-align:center; color:#9fb3cc; font-size:0.8rem; margin-bottom:6px; }
      .aebc-feedback{ min-height:1.4em; text-align:center; font-weight:700; margin-bottom:10px; }
      .aebc-feedback.ok{ color:#9dffb0; }
      .aebc-feedback.bad{ color:#ffb3b3; }
      .aebc-actions{ display:flex; gap:10px; justify-content:center; }
      .aebc-btn{ padding:10px 16px; border-radius:10px; border:none; font-weight:700; cursor:pointer; }
      .aebc-btn.primary{ background:linear-gradient(180deg,#ffcf6b,#ff9d1f); color:#2a1600; }
      .aebc-btn.ghost{ background:#2d2f33; color:#fff; border:1px solid rgba(255,255,255,0.1); }
    `;
    document.head.appendChild(style);
  }

  const overlay = document.createElement('div');
  overlay.className = 'aebc-overlay';
  overlay.innerHTML = `
    <div class="aebc-box">
      <h3>Carta 60 — Juego de los cables</h3>
      <p class="aebc-instr">Toca un cable y luego el hueco donde quieras colocarlo. Ordénalos según el número de cada uno.</p>
      <div class="aebc-label">Cables disponibles</div>
      <div class="aebc-row" id="aebcSource"></div>
      <div class="aebc-label">Orden final (de menor a mayor)</div>
      <div class="aebc-row" id="aebcTarget"></div>
      <div class="aebc-feedback" id="aebcFeedback"></div>
      <div class="aebc-actions">
        <button class="aebc-btn ghost" id="aebcReset">Recolocar</button>
        <button class="aebc-btn primary" id="aebcCheck">Comprobar</button>
        <button class="aebc-btn ghost" id="aebcClose">Cerrar</button>
      </div>
    </div>
  `;
  document.body.appendChild(overlay);

  const source = overlay.querySelector('#aebcSource');
  const target = overlay.querySelector('#aebcTarget');
  const feedback = overlay.querySelector('#aebcFeedback');
  let selected = null;

  function shuffle(arr) {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  function makeCable(c) {
    const el = document.createElement('div');
    el.className = 'aebc-cable';
    el.style.background = c.color;
    el.dataset.id = c.id;
    el.textContent = c.num;
    el.tabIndex = 0;
    el.addEventListener('click', () => {
      if (selected === el) { clearSelection(); return; }
      clearSelection();
      selected = el;
      el.classList.add('selected');
    });
    return el;
  }

  function clearSelection() {
    if (selected) selected.classList.remove('selected');
    selected = null;
  }

  function buildSlots() {
    target.innerHTML = '';
    for (let i = 0; i < CABLES.length; i++) {
      const slot = document.createElement('div');
      slot.className = 'aebc-slot';
      slot.dataset.index = String(i);
      slot.addEventListener('click', () => {
        if (!selected) return;
        if (slot.firstChild) source.appendChild(slot.firstChild);
        slot.appendChild(selected);
        clearSelection();
        feedback.textContent = '';
      });
      target.appendChild(slot);
    }
  }

  function populate() {
    source.innerHTML = '';
    shuffle(CABLES).forEach(c => source.appendChild(makeCable(c)));
  }

  buildSlots();
  populate();

  function checkOrder() {
    const order = Array.from(target.children).map(s => s.firstChild ? s.firstChild.dataset.id : null);
    if (order.some(x => x === null)) {
      feedback.textContent = 'Coloca los cuatro cables en los huecos.';
      feedback.className = 'aebc-feedback bad';
      return;
    }
    const ok = order.every((id, i) => id === CORRECT_ORDER[i]);
    if (ok) {
      feedback.textContent = '¡Correcto! En el nido de la ardilla hay algo brillante. Coged la carta 71.';
      feedback.className = 'aebc-feedback ok';
      overlay.querySelectorAll('.aebc-cable').forEach(c => c.style.pointerEvents = 'none');
    } else {
      feedback.textContent = 'Ese orden no es correcto. Revisad los números de cada cable.';
      feedback.className = 'aebc-feedback bad';
    }
  }

  overlay.querySelector('#aebcCheck').addEventListener('click', checkOrder);
  overlay.querySelector('#aebcReset').addEventListener('click', () => {
    Array.from(target.children).forEach(s => { if (s.firstChild) source.appendChild(s.firstChild); });
    populate();
    feedback.textContent = '';
  });

  function close() {
    document.removeEventListener('keydown', onKey);
    overlay.remove();
    if (typeof resumeGameTimer === 'function') resumeGameTimer();
    if (typeof onClose === 'function') onClose();
  }
  overlay.querySelector('#aebcClose').addEventListener('click', close);
  function onKey(e){ if (e.key === 'Escape') close(); }
  document.addEventListener('keydown', onKey);

  return { close };
}
