// juegos/miniJuegoLevantarProyectar/main.js
// Minijuego: ordenar 4 probetas (C, N, O, S) por su número atómico (de menor a mayor).
// Ajustes: centrado total, tamaño máximo que quepa en pantalla, header y acciones centrados.
// Exporta startMinigame(opts)
// opts: { onClose?: fn, pauseGameTimer?: fn, resumeGameTimer?: fn }

export function startMinigame(opts = {}) {
  const { onClose, pauseGameTimer, resumeGameTimer } = opts;

  if (typeof pauseGameTimer === 'function') pauseGameTimer();

  /* --------------------- INYECTAR ESTILOS (incluye animaciones) --------------------- */
  const styleId = 'miniJuego-levantar-style';
  if (!document.getElementById(styleId)) {
    const style = document.createElement('style');
    style.id = styleId;
    style.textContent = `
      :root {
        --mlp-gap: 10px;
        --mlp-box-padding: 12px;
        --tube-w: 110px;
        --tube-h: 140px;
        --slot-border-radius: 10px;
        --mlp-header-h: 56px;
        --mlp-actions-h: 56px;
        --mlp-feedback-h: 40px;
      }

      .mlp-overlay {
        position: fixed; inset: 0;
        display:flex; align-items:center; justify-content:center;
        background: rgba(0,0,0,0.66); z-index: 2500; padding:8px;
        -webkit-overflow-scrolling: touch;
      }

      @keyframes mlp-enter { from { transform: translateY(8px) scale(.995); opacity:0 } to { transform: translateY(0) scale(1); opacity:1 } }
      @keyframes mlp-exit  { from { transform: translateY(0) scale(1); opacity:1 } to { transform: translateY(8px) scale(.99); opacity:0 } }

      .mlp-box {
        width: 94vw;
        max-width: 920px;
        height: calc(var(--vh, 1vh) * 100 - 24px);
        max-height: calc(var(--vh, 1vh) * 100 - 24px);
        overflow: hidden;
        background: #0f1116;
        border-radius: 12px;
        padding: var(--mlp-box-padding);
        color: #fff;
        border: 1px solid rgba(255,255,255,0.04);
        box-shadow: 0 18px 56px rgba(0,0,0,0.7);
        font-family: inherit;
        animation: mlp-enter .28s cubic-bezier(.2,.9,.2,1);
        display: flex;
        flex-direction: column;
        box-sizing: border-box;
      }
      .mlp-box.mlp-exiting { animation: mlp-exit .22s cubic-bezier(.2,.9,.2,1) forwards; }

      .mlp-header {
        flex: 0 0 auto;
        display:flex;
        align-items:center;
        justify-content:center; /* CENTRADO */
        gap:8px;
        height: var(--mlp-header-h);
        text-align:center;
      }
      .mlp-title { margin:0; font-size:1.02rem; font-weight:700; }
      .mlp-instr { color:#d6d6d6; font-size:0.92rem; margin-top:4px; opacity:0.95; }

      .mlp-center {
        flex: 1 1 auto;
        display:flex;
        flex-direction:column;
        align-items:center;
        justify-content:center;
        gap:8px;
        padding:4px 0;
        box-sizing: border-box;
      }

      .mlp-row {
        display:flex;
        gap: var(--mlp-gap);
        justify-content:center; /* CENTRADO */
        align-items:flex-end;
        flex-wrap: wrap; /* permitimos wrap para evitar overflow horizontal */
        box-sizing: border-box;
      }

      .mlp-tube {
        width: var(--tube-w);
        height: var(--tube-h);
        padding: 6px;
        border-radius:  var(--slot-border-radius);
        display:flex; align-items:center; justify-content:center;
        cursor: pointer; user-select:none; transition: transform .12s, box-shadow .12s;
        background: linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.00));
        box-sizing: border-box;
        flex: 0 0 auto;
      }
      .mlp-tube img { width: 88%; height: 88%; object-fit: contain; display:block; pointer-events:none; }

      .mlp-slot {
        width: var(--tube-w);
        height: var(--tube-h);
        border-radius: var(--slot-border-radius);
        border: 2px dashed rgba(255,255,255,0.06);
        display:flex; align-items:center; justify-content:center;
        background: linear-gradient(180deg, rgba(255,255,255,0.01), rgba(0,0,0,0.04));
        transition: all .14s;
        box-sizing: border-box;
        flex: 0 0 auto;
      }
      .mlp-slot.highlight { border-color: rgba(255,255,255,0.18); box-shadow: 0 10px 30px rgba(0,0,0,0.35); }

      .mlp-feedback { min-height: var(--mlp-feedback-h); margin-top:6px; color:#ffdede; text-align:center; font-size:0.92rem; }

      .mlp-actions {
        flex: 0 0 auto;
        display:flex; gap:12px; justify-content:center; align-items:center;
        height: var(--mlp-actions-h);
        margin-top:8px;
        box-sizing: border-box;
      }
      .mlp-btn { padding:10px 14px; border-radius:10px; background: linear-gradient(90deg,#1f2230,#121217); border:1px solid rgba(255,255,255,0.06); color:#fff; cursor:pointer; font-weight:700; font-size:0.96rem; }

      .mlp-tube:focus, .mlp-slot:focus { outline:3px solid rgba(255,255,255,0.06); outline-offset:3px; }

      @media (max-height:660px) {
        :root { --mlp-gap: 6px; --mlp-box-padding:10px; --mlp-header-h:48px; --mlp-actions_h:48px; --mlp-feedback-h:36px; }
      }

      @media (min-height:900px) and (min-width:900px) {
        :root { --tube-w: 180px; --tube-h: 230px; --mlp-gap:14px; --mlp-box-padding:16px; --mlp-header-h:72px; --mlp-actions-h:64px; --mlp-feedback-h:48px; }
      }
    `;
    document.head.appendChild(style);
  }

  /* --------------------- Helper para iOS vh bug --------------------- */
  function setVhVar() {
    const vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
  }
  setVhVar();
  window.addEventListener('resize', setVhVar);
  window.addEventListener('orientationchange', () => { setTimeout(setVhVar, 250); });

  /* --------------------- ELEMENTOS DOM --------------------- */
  const overlay = document.createElement('div');
  overlay.className = 'mlp-overlay';

  const box = document.createElement('div');
  box.className = 'mlp-box';

  box.innerHTML =
    '<div class="mlp-header"><div><h3 class="mlp-title">Carta 01 — Ordena las Probetas</h3><div id="mm-instr" class="mlp-instr">Ordena de la más ligera a la más pesada.</div></div></div>';

  const center = document.createElement('div');
  center.className = 'mlp-center';

  const tubesRow = document.createElement('div');
  tubesRow.className = 'mlp-row';
  tubesRow.setAttribute('aria-label', 'Probetas disponibles');

  const targetRow = document.createElement('div');
  targetRow.className = 'mlp-row';
  targetRow.setAttribute('aria-label', 'Slots para ordenar');

  const feedback = document.createElement('div');
  feedback.className = 'mlp-feedback';

  const actions = document.createElement('div');
  actions.className = 'mlp-actions';
  const resetBtn = document.createElement('button');
  resetBtn.className = 'mlp-btn';
  resetBtn.textContent = 'Recolocar';
  const closeBtn = document.createElement('button');
  closeBtn.className = 'mlp-btn';
  closeBtn.textContent = 'Cerrar';
  actions.appendChild(resetBtn);
  actions.appendChild(closeBtn);

  center.appendChild(tubesRow);
  center.appendChild(targetRow);
  center.appendChild(feedback);

  box.appendChild(center);
  box.appendChild(actions);
  overlay.appendChild(box);
  document.body.appendChild(overlay);

  /* --------------------- DATOS (C, N, O, S) --------------------- */
  const ELEMENTS = [{ sym: 'C', z: 6 }, { sym: 'N', z: 7 }, { sym: 'O', z: 8 }, { sym: 'S', z: 16 }];

  /* --------------------- HELPERS --------------------- */
  function shuffle(arr) {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }
  function vib(ms = 20) { try { if (navigator.vibrate) navigator.vibrate(ms); } catch (e) {} }

  let audioCtx = null;
  function playSuccessSound() {
    try {
      if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      const t = audioCtx.currentTime;
      const o = audioCtx.createOscillator();
      const g = audioCtx.createGain();
      o.type = 'sine';
      o.frequency.setValueAtTime(880, t);
      g.gain.setValueAtTime(0.0001, t);
      g.gain.exponentialRampToValueAtTime(0.12, t + 0.01);
      g.gain.exponentialRampToValueAtTime(0.0001, t + 0.45);
      o.connect(g); g.connect(audioCtx.destination);
      o.start(t); o.stop(t + 0.5);
      const o2 = audioCtx.createOscillator();
      const g2 = audioCtx.createGain();
      o2.type = 'sine';
      o2.frequency.setValueAtTime(1320, t + 0.06);
      g2.gain.setValueAtTime(0.0001, t + 0.06);
      g2.gain.exponentialRampToValueAtTime(0.08, t + 0.08);
      g2.gain.exponentialRampToValueAtTime(0.0001, t + 0.42);
      o2.connect(g2); g2.connect(audioCtx.destination);
      o2.start(t + 0.06); o2.stop(t + 0.5);
    } catch (e) { /* ignore */ }
  }

  /* --------------------- Crear probeta --------------------- */
  function makeTube(el) {
    const t = document.createElement('div');
    t.className = 'mlp-tube';
    t.tabIndex = 0;
    t.dataset.z = String(el.z);
    t.dataset.sym = el.sym;

    const img = document.createElement('img');
    img.src = `./images/${el.sym}.png`;
    img.alt = `Probeta ${el.sym}`;
    img.loading = 'lazy';
    t.appendChild(img);

    t.draggable = true;
    t.addEventListener('dragstart', (e) => {
      e.dataTransfer.setData('text/plain', t.dataset.z);
      try {
        const dragImg = img.cloneNode(true);
        dragImg.style.width = '120px';
        dragImg.style.height = '160px';
        dragImg.style.position = 'absolute';
        dragImg.style.top = '-9999px';
        document.body.appendChild(dragImg);
        e.dataTransfer.setDragImage(dragImg, dragImg.width / 2, dragImg.height / 2);
        setTimeout(() => { try { document.body.removeChild(dragImg); } catch (_) {} }, 0);
      } catch (err) {}
      vib(10);
    });

    t.addEventListener('click', (ev) => {
      ev.stopPropagation();
      if (isTouchDevice) {
        if (selectedTube === t) clearSelection(); else setSelection(t);
      }
    });

    t.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        if (selectedTube === t) clearSelection(); else setSelection(t);
      }
    });

    return t;
  }

  /* --------------------- SLOTS --------------------- */
  for (let i = 0; i < 4; i++) {
    const slot = document.createElement('div');
    slot.className = 'mlp-slot';
    slot.dataset.index = String(i);
    slot.tabIndex = 0;

    slot.addEventListener('dragover', (e) => { e.preventDefault(); slot.classList.add('highlight'); });
    slot.addEventListener('dragleave', () => slot.classList.remove('highlight'));
    slot.addEventListener('drop', (e) => {
      e.preventDefault(); slot.classList.remove('highlight');
      const z = e.dataTransfer.getData('text/plain');
      let tube = Array.from(tubesRow.children).find(t => t.dataset.z === z);
      if (!tube) tube = box.querySelector(`.mlp-tube[data-z="${z}"]`);
      if (!tube) return;
      if (slot.firstChild) tubesRow.appendChild(slot.firstChild);
      slot.appendChild(tube);
      vib(8); checkOrder();
    });

    slot.addEventListener('click', () => {
      if (selectedTube) {
        if (slot.firstChild) tubesRow.appendChild(slot.firstChild);
        slot.appendChild(selectedTube);
        vib(8);
        clearSelection();
        checkOrder();
      }
    });

    slot.addEventListener('keydown', (e) => {
      if ((e.key === 'Enter' || e.key === ' ') && selectedTube) {
        e.preventDefault();
        if (slot.firstChild) tubesRow.appendChild(slot.firstChild);
        slot.appendChild(selectedTube);
        vib(8);
        clearSelection();
        checkOrder();
      }
    });

    targetRow.appendChild(slot);
  }

  /* --------------------- SELECCIÓN TOUCH --------------------- */
  let selectedTube = null;
  const isTouchDevice = ('ontouchstart' in window) || (navigator.maxTouchPoints && navigator.maxTouchPoints > 0);
  const mmInstrEl = box.querySelector('#mm-instr');
  const defaultInstr = mmInstrEl ? mmInstrEl.textContent : '';

  function setSelection(tube) {
    clearSelection();
    selectedTube = tube;
    tube.style.transform = 'translateY(-6px) scale(1.03)';
    tube.style.boxShadow = '0 18px 40px rgba(0,0,0,0.45)';
    if (mmInstrEl) mmInstrEl.textContent = 'Toca un hueco vacío para colocar la probeta seleccionada.';
  }
  function clearSelection() {
    if (!selectedTube) return;
    selectedTube.style.transform = '';
    selectedTube.style.boxShadow = '';
    selectedTube = null;
    if (mmInstrEl) mmInstrEl.textContent = defaultInstr;
  }

  /* --------------------- COMPROBAR ORDEN --------------------- */
  function checkOrder() {
    const slotZ = Array.from(targetRow.children).map(s => s.firstChild ? s.firstChild.dataset.z : null);
    if (slotZ.some(z => z === null)) { feedback.textContent = 'Coloca todas las probetas en los slots.'; return; }
    const nums = slotZ.map(z => Number(z));
    let ok = true;
    for (let i = 1; i < nums.length; i++) { if (nums[i] < nums[i - 1]) { ok = false; break; } }
    if (ok) {
      vib(60);
      playSuccessSound();
      feedback.innerHTML = '<strong style="color:#b6ffb6">¡Correcto! Se ha creado una sustancia nueva.</strong><div style="margin-top:8px;color:#d6ffd6"><strong>Pista:</strong> Revisa el cajón del laboratorio.</div>';
      Array.from(targetRow.children).forEach(s => s.style.pointerEvents = 'none');
      Array.from(tubesRow.children).forEach(t => t.style.pointerEvents = 'none');
      if (mmInstrEl) mmInstrEl.textContent = 'Resuelto — pulsa Cerrar para volver.';
    } else {
      feedback.textContent = 'Orden incorrecto. Intenta reorganizarlas.';
    }
  }

  /* --------------------- POBLAR INICIAL --------------------- */
  function populateTubes(arr) {
    Array.from(targetRow.children).forEach(s => { if (s.firstChild) tubesRow.appendChild(s.firstChild); });
    while (tubesRow.firstChild) tubesRow.removeChild(tubesRow.firstChild);
    arr.forEach(el => tubesRow.appendChild(makeTube(el)));
    feedback.textContent = '';
    clearSelection();
    adjustSizes(); // ajustar tamaños después de poblar
  }
  populateTubes(shuffle(ELEMENTS));

  /* --------------------- AJUSTE DINÁMICO DE TAMAÑOS (centrado y sin overflow) --------------------- */
  function adjustSizes() {
    setVhVar();

    // medir caja interior
    const boxRect = box.getBoundingClientRect();
    const styleBox = getComputedStyle(box);
    const padTop = parseFloat(styleBox.paddingTop || 12);
    const padBottom = parseFloat(styleBox.paddingBottom || 12);
    const padLeft = parseFloat(styleBox.paddingLeft || 12);
    const padRight = parseFloat(styleBox.paddingRight || 12);

    const innerW = Math.max(180, boxRect.width - padLeft - padRight);
    const innerH = Math.max(160, boxRect.height - padTop - padBottom);

    // header/actions/feedback heights
    const headerEl = box.querySelector('.mlp-header');
    const actionsEl = box.querySelector('.mlp-actions');
    const feedbackEl = box.querySelector('.mlp-feedback');
    const headerH = headerEl ? headerEl.getBoundingClientRect().height : 56;
    const actionsH = actionsEl ? actionsEl.getBoundingClientRect().height : 56;
    const feedbackH = feedbackEl ? feedbackEl.getBoundingClientRect().height : 40;

    // espacio disponible central para las dos filas + gap
    const centerAvailableH = innerH - headerH - actionsH - feedbackH - 24; // margen extra
    const gap = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--mlp-gap')) || 10;

    // decide mejor número de columnas para que las probetas sean lo más grandes posible sin salirse
    const minTubeW = 64; // no más pequeño que esto
    const maxCols = 4;
    let chosenCols = maxCols;
    let tubeW = 0;
    let tubeH = 0;

    for (let cols = maxCols; cols >= 1; cols--) {
      // width-based candidate
      const totalGapX = gap * (Math.min(cols, 4) - 1);
      const candidateW = Math.floor((innerW - totalGapX) / Math.min(cols, 4));
      // height-limited candidate: we need two rows (tubesRow + targetRow)
      const maxRowH = Math.floor((centerAvailableH - gap) / 2); // each row
      // choose tube height as min(maxRowH, candidateW * ratio)
      const candidateH_fromW = Math.round(candidateW * 1.25);
      const candidateH = Math.min(maxRowH, candidateH_fromW, Math.round(window.innerHeight * 0.32));
      const candidateW_final = Math.min(candidateW, Math.round(candidateH / 1.25));

      if (candidateW_final >= minTubeW) {
        chosenCols = cols;
        tubeW = candidateW_final;
        tubeH = Math.max(60, Math.round(tubeW * 1.25));
        break;
      }
      // if not acceptable, loop to try fewer columns (which increases candidateW)
    }

    // fallback if loop didn't set values
    if (!tubeW || !tubeH) {
      tubeW = Math.max(minTubeW, Math.floor(innerW / 2) - gap);
      tubeH = Math.max(80, Math.round(tubeW * 1.25));
    }

    // apply computed sizes to CSS variables for layout
    box.style.setProperty('--tube-w', `${tubeW}px`);
    box.style.setProperty('--tube-h', `${tubeH}px`);

    // extra centering: ensure rows are centered and don't exceed inner width
    const rows = [tubesRow, targetRow];
    rows.forEach(row => {
      row.style.width = '100%';
      row.style.maxWidth = `${innerW}px`;
      row.style.justifyContent = 'center';
    });
  }

  const resizeObserver = () => { adjustSizes(); };
  window.addEventListener('resize', resizeObserver);
  window.addEventListener('orientationchange', () => { setTimeout(adjustSizes, 220); });

  /* --------------------- BOTONES --------------------- */
  resetBtn.addEventListener('click', () => {
    Array.from(targetRow.children).forEach(s => { if (s.firstChild) tubesRow.appendChild(s.firstChild); });
    populateTubes(shuffle(ELEMENTS));
    feedback.textContent = 'Probetas recolocadas. Intenta de nuevo.';
    vib(10);
  });

  closeBtn.addEventListener('click', () => { vib(10); cleanupWithAnimation(); });

  /* --------------------- CERRAR / LIMPIEZA --------------------- */
  function cleanupWithAnimation() {
    box.classList.add('mlp-exiting');
    box.addEventListener('animationend', function handler() {
      box.removeEventListener('animationend', handler);
      cleanupImmediate();
    });
  }

  function cleanupImmediate() {
    document.removeEventListener('keydown', onKey);
    try { overlay.remove(); } catch (e) {}
    window.removeEventListener('resize', resizeObserver);
    window.removeEventListener('orientationchange', resizeObserver);
    if (typeof resumeGameTimer === 'function') resumeGameTimer();
    if (typeof onClose === 'function') onClose();
  }

  function onKey(e) { if (e.key === 'Escape') cleanupWithAnimation(); }
  document.addEventListener('keydown', onKey);
  overlay.addEventListener('click', (e) => { if (e.target === overlay) clearSelection(); });

  // ajuste inicial
  setTimeout(adjustSizes, 60);

  return { close: cleanupWithAnimation };
}
