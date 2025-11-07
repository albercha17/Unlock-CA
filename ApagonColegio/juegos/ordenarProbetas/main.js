// juegos/miniJuegoLevantarProyectar/main.js
// Minijuego: ordenar 4 probetas (C, N, O, S) por su número atómico (de menor a mayor).
// Versión optimizada móvil (iPhone): todo el minijuego cabe en pantalla,
// caja centrada con scroll interno, tap-to-pick + tap-to-drop para touch,
// drag&drop nativo en escritorio y vibración en interacciones.

// Exporta startMinigame(opts)
// opts: { onClose?: fn, pauseGameTimer?: fn, resumeGameTimer?: fn }
export function startMinigame(opts = {}) {
  const { onClose, pauseGameTimer, resumeGameTimer } = opts;

  // Si nos pasan la función para pausar el temporizador principal, la ejecutamos.
  if (typeof pauseGameTimer === 'function') pauseGameTimer();

  /* ---------------------- INSERCIÓN DE ESTILOS (para mobile-friendly) ---------------------- */
  // Se inyectan unos estilos mínimos en <head> para mantener el DOM más limpio.
  const styleId = 'miniJuego-levantar-style';
  if (!document.getElementById(styleId)) {
    const style = document.createElement('style');
    style.id = styleId;
    style.textContent = `
      /* overlay flexible y centrado */
      .mlp-overlay {
        position:fixed;
        inset:0;
        display:flex;
        align-items:center;
        justify-content:center;
        background:rgba(0,0,0,0.66);
        z-index:2500;
        padding:10px;
        -webkit-overflow-scrolling:touch;
      }
      /* caja principal: cabe en pantalla y permite scroll interno */
      .mlp-box {
        width:94vw;
        max-width:820px;
        max-height:92vh; /* muy importante para que todo quede dentro del viewport móvil */
        overflow:auto;
        -webkit-overflow-scrolling:touch;
        background:#0f1116;
        border-radius:12px;
        padding:14px;
        color:#fff;
        border:1px solid rgba(255,255,255,0.04);
        box-shadow:0 18px 56px rgba(0,0,0,0.7);
        font-family:inherit;
      }
      .mlp-title { margin:0 0 8px 0; font-size:1.05rem; }
      .mlp-instr { color:#d6d6d6; margin-bottom:10px; font-size:0.95rem; }

      .mlp-row { display:flex; gap:12px; justify-content:center; margin:12px 0; flex-wrap:wrap; }

      /* probeta: tamaño relativo a viewport para que sea grande en móviles */
      .mlp-tube {
        width:22vw; max-width:150px;
        height:26vw; max-height:180px;
        padding:6px; border-radius:10px;
        display:flex; align-items:center; justify-content:center;
        cursor:pointer; user-select:none; transition:transform .12s;
      }
      .mlp-tube img { width:78%; height:78%; object-fit:contain; display:block; pointer-events:none; }

      /* slot (donde soltar) */
      .mlp-slot {
        width:22vw; max-width:150px;
        height:26vw; max-height:180px;
        border-radius:10px;
        border:2px dashed rgba(255,255,255,0.06);
        display:flex; align-items:center; justify-content:center;
        background:linear-gradient(180deg,rgba(255,255,255,0.01),rgba(0,0,0,0.04));
        transition:all .14s;
      }
      .mlp-slot.highlight { border-color: rgba(255,255,255,0.18); box-shadow:0 10px 30px rgba(0,0,0,0.35); }

      .mlp-actions { display:flex; gap:12px; justify-content:center; margin-top:12px; flex-wrap:wrap; }
      .mlp-btn {
        padding:12px 16px; border-radius:10px;
        background:linear-gradient(90deg,#1f2230,#121217);
        border:1px solid rgba(255,255,255,0.06); color:#fff;
        cursor:pointer; font-weight:700; font-size:0.98rem;
      }
      .mlp-feedback { min-height:28px; margin-top:8px; color:#ffdede; text-align:center; font-size:0.95rem; }

      /* mejor foco para accesibilidad */
      .mlp-tube:focus, .mlp-slot:focus { outline:3px solid rgba(255,255,255,0.06); outline-offset:3px; }
      @media(min-width:900px) {
        .mlp-tube { width:120px; height:160px; }
        .mlp-slot { width:120px; height:160px; }
      }
    `;
    document.head.appendChild(style);
  }

  /* ---------------------- CREAMOS ELEMENTOS DEL DOM ---------------------- */
  const overlay = document.createElement('div');
  overlay.className = 'mlp-overlay';

  const box = document.createElement('div');
  box.className = 'mlp-box';

  box.innerHTML =
    '<h3 class="mlp-title">Carta 01 — Ordena las Probetas</h3>' +
    '<div id="mm-instr" class="mlp-instr">Cuatro probetas esperan su turno. Ordena su esencia de la más ligera a la más pesada — empieza por la que menos pesa.</div>';

  // contenedores
  const tubesRow = document.createElement('div');
  tubesRow.className = 'mlp-row';

  const targetRow = document.createElement('div');
  targetRow.className = 'mlp-row';

  const feedback = document.createElement('div');
  feedback.className = 'mlp-feedback';

  // botones
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

  // añadimos al DOM
  box.appendChild(tubesRow);
  box.appendChild(targetRow);
  box.appendChild(feedback);
  box.appendChild(actions);
  overlay.appendChild(box);
  document.body.appendChild(overlay);

  /* ---------------------- DATOS: 4 elementos que tienes en /assets/images/apagonColegio/ ---------------------- */
  const ELEMENTS = [
    { sym: 'C', z: 6 },
    { sym: 'N', z: 7 },
    { sym: 'O', z: 8 },
    { sym: 'S', z: 16 }
  ];

  /* ---------------------- UTIL helpers ---------------------- */
  function shuffle(arr) {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }
  // pequeña ayuda de vibración si está disponible (UX móvil)
  function vib(ms = 20) { try { if (navigator.vibrate) navigator.vibrate(ms); } catch (e) {} }

  /* ---------------------- CREAR PROBETA (imagen sólo) ---------------------- */
  function makeTube(el) {
    const t = document.createElement('div');
    t.className = 'mlp-tube';
    t.tabIndex = 0; // foco accesible
    t.dataset.z = String(el.z);
    t.dataset.sym = el.sym;

    const img = document.createElement('img');
    img.src = `../assets/images/apagonColegio/${el.sym}.png`;
    img.alt = `Probeta ${el.sym}`;
    img.loading = 'lazy';
    t.appendChild(img);

    // Drag native (escritorio)
    t.draggable = true;
    t.addEventListener('dragstart', (e) => {
      e.dataTransfer.setData('text/plain', t.dataset.z);
      // drag image temporal (evita hueco)
      try {
        const dragImg = img.cloneNode(true);
        dragImg.style.width = '120px';
        dragImg.style.height = '160px';
        dragImg.style.position = 'absolute';
        dragImg.style.top = '-9999px';
        document.body.appendChild(dragImg);
        e.dataTransfer.setDragImage(dragImg, dragImg.width/2, dragImg.height/2);
        setTimeout(()=> { try { document.body.removeChild(dragImg); } catch(_){} }, 0);
      } catch (err) {}
      vib(10);
    });

    // Tap (touch) -> selección/desselección. en iPhone esto será el comportamiento principal.
    t.addEventListener('click', (ev) => {
      ev.stopPropagation();
      if (isTouchDevice) {
        if (selectedTube === t) { clearSelection(); }
        else { setSelection(t); }
      }
    });

    // teclado: Enter para seleccionar
    t.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        if (selectedTube === t) clearSelection(); else setSelection(t);
      }
    });

    return t;
  }

  /* ---------------------- SLOTS (drop targets) ---------------------- */
  for (let i = 0; i < 4; i++) {
    const slot = document.createElement('div');
    slot.className = 'mlp-slot';
    slot.dataset.index = String(i);
    slot.tabIndex = 0;

    // dragover / drop (escritorio)
    slot.addEventListener('dragover', (e) => {
      e.preventDefault();
      slot.classList.add('highlight');
    });
    slot.addEventListener('dragleave', () => slot.classList.remove('highlight'));
    slot.addEventListener('drop', (e) => {
      e.preventDefault();
      slot.classList.remove('highlight');
      const z = e.dataTransfer.getData('text/plain');
      let tube = Array.from(tubesRow.children).find(t => t.dataset.z === z);
      if (!tube) tube = box.querySelector(`.mlp-tube[data-z="${z}"]`);
      if (!tube) return;
      // si el slot tenía algo, lo devolvemos al tubesRow
      if (slot.firstChild) tubesRow.appendChild(slot.firstChild);
      slot.appendChild(tube);
      vib(8);
      checkOrder();
    });

    // tap en slot: si hay una probeta seleccionada (modo touch), soltarla aquí
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

  /* ---------------------- SELECCIÓN TOUCH (pick & drop) ---------------------- */
  let selectedTube = null;
  const isTouchDevice = ('ontouchstart' in window) || (navigator.maxTouchPoints && navigator.maxTouchPoints > 0);
  const mmInstr = box.querySelector('#mm-instr');
  const defaultInstr = mmInstr.textContent;

  function setSelection(tube) {
    clearSelection();
    selectedTube = tube;
    tube.style.transform = 'translateY(-6px) scale(1.03)';
    tube.style.boxShadow = '0 18px 40px rgba(0,0,0,0.45)';
    mmInstr.textContent = 'Toca un hueco vacío para colocar la probeta seleccionada.';
  }
  function clearSelection() {
    if (!selectedTube) return;
    selectedTube.style.transform = '';
    selectedTube.style.boxShadow = '';
    selectedTube = null;
    mmInstr.textContent = defaultInstr;
  }

  /* ---------------------- LOGICA: checkOrder ---------------------- */
  function checkOrder(){
    const slotZ = Array.from(targetRow.children).map(slot => slot.firstChild ? slot.firstChild.dataset.z : null);
    if (slotZ.some(z=> z === null)) {
      feedback.textContent = 'Coloca todas las probetas en los slots.';
      return;
    }
    const nums = slotZ.map(z=>Number(z));
    let ok = true;
    for (let i=1;i<nums.length;i++){ if (nums[i] < nums[i-1]) { ok=false; break; } }
    if (ok) {
      vib(60);
      feedback.innerHTML = '<strong style="color:#b6ffb6">¡Correcto! Las probetas están en orden (menor → mayor).</strong><div style="margin-top:8px;color:#d6ffd6"><strong>Pista:</strong> Revisa el cajón del laboratorio.</div>';
      // bloquear movimientos
      Array.from(targetRow.children).forEach(s => s.style.pointerEvents = 'none');
      Array.from(tubesRow.children).forEach(t => t.style.pointerEvents = 'none');
      mmInstr.textContent = 'Resuelto — pulsa Cerrar para volver.';
    } else {
      feedback.textContent = 'Orden incorrecto. Intenta reorganizarlas.';
    }
  }

  /* ---------------------- POBLAR INICIALMENTE ---------------------- */
  function populateTubes(arr){
    // devolver probetas de slots al contenedor
    Array.from(targetRow.children).forEach(s => { if (s.firstChild) tubesRow.appendChild(s.firstChild); });
    // limpiar
    while (tubesRow.firstChild) tubesRow.removeChild(tubesRow.firstChild);
    // añadir probetas
    arr.forEach(el => tubesRow.appendChild(makeTube(el)));
    feedback.textContent = '';
    clearSelection();
  }
  populateTubes(shuffle(ELEMENTS));

  /* ---------------------- BOTONES: Recolocar y Cerrar ---------------------- */
  resetBtn.addEventListener('click', () => {
    Array.from(targetRow.children).forEach(s => { if (s.firstChild) tubesRow.appendChild(s.firstChild); });
    populateTubes(shuffle(ELEMENTS));
    feedback.textContent = 'Probetas recolocadas. Intenta de nuevo.';
    vib(10);
  });

  function cleanup() {
    // restaurar scroll del documento (no lo tocamos aquí, pero si en el futuro se hace, rest.)
    document.removeEventListener('keydown', onKey);
    try { overlay.remove(); } catch (e) {}
    if (typeof resumeGameTimer === 'function') resumeGameTimer();
    if (typeof onClose === 'function') onClose();
  }
  closeBtn.addEventListener('click', () => { cleanup(); vib(10); });

  function onKey(e) { if (e.key === 'Escape') cleanup(); }
  document.addEventListener('keydown', onKey);

  // tocar fuera del box cancela selección (no cierra el modal)
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) clearSelection();
  });

  // devolvemos objeto con método close
  return { close: cleanup };
}
