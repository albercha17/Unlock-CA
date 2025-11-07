// juegos/miniJuegoLevantarProyectar/main.js
// Minijuego: ordenar 4 probetas (C, N, O, S) por su número atómico (de menor a mayor).
// Versión mejorada para móvil: soporta touch (tap para seleccionar + tap para soltar)
// y drag&drop para escritorio. UI responsive para pantallas pequeñas.
// Exporta startMinigame(opts) que crea un overlay y maneja la lógica.
// opts: { onClose?: fn, pauseGameTimer?: fn, resumeGameTimer?: fn }

export function startMinigame(opts = {}) {
  const { onClose, pauseGameTimer, resumeGameTimer } = opts;

  // Pausar temporizador principal (si nos pasa la función)
  if (typeof pauseGameTimer === 'function') pauseGameTimer();

  // --- OVERLAY y CAJA PRINCIPAL (estilos en línea para encapsular) ---
  const overlay = document.createElement('div');
  overlay.style =
    'position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,0.65);z-index:2500;padding:12px;-webkit-overflow-scrolling:touch;';

  const box = document.createElement('div');
  // caja con ancho responsivo: en móvil ocupa casi toda la pantalla
  box.style =
    'width:92vw;max-width:820px;background:#0f1116;border-radius:12px;padding:16px 16px 20px;color:#fff;border:1px solid rgba(255,255,255,0.04);box-shadow:0 20px 60px rgba(0,0,0,0.7);font-family:inherit;';

  box.innerHTML =
    '<h3 style="margin:0 0 8px 0;font-size:1.05rem">Carta 01 — Ordena las Probetas</h3>' +
    '<div id="mm-instr" style="color:#d6d6d6;margin-bottom:8px;font-size:0.95rem">Cuatro probetas esperan su turno. Ordena su esencia de la más ligera a la más pesada — empieza por la que menos pesa.</div>';

  // Contenedor inicial de probetas (zona donde aparecen al inicio)
  const tubesRow = document.createElement('div');
  tubesRow.style = 'display:flex;gap:12px;justify-content:center;margin:12px 0;flex-wrap:wrap;';

  // --- DEFINICIÓN DE LOS ELEMENTOS (tus PNGs en assets/images/apagonColegio) ---
  // Carbono(C)=6, Nitrógeno(N)=7, Oxígeno(O)=8, Azufre(S)=16
  const ELEMENTS = [
    { sym: 'C', z: 6 },
    { sym: 'N', z: 7 },
    { sym: 'O', z: 8 },
    { sym: 'S', z: 16 }
  ];

  // Zona objetivo: slots donde soltar las probetas
  const targetRow = document.createElement('div');
  targetRow.style = 'display:flex;gap:12px;justify-content:center;margin:10px 0;flex-wrap:wrap;';

  // Creamos 4 slots vacíos (para ordenar) — tamaño responsivo
  for (let i = 0; i < 4; i++) {
    const slot = document.createElement('div');
    slot.className = 'mlp-slot';
    slot.dataset.index = String(i);
    // slot más grande en móvil (usa vw)
    slot.style =
      'width:22vw;max-width:140px;height:26vw;max-height:180px;border-radius:10px;border:2px dashed rgba(255,255,255,0.06);display:flex;align-items:center;justify-content:center;background:linear-gradient(180deg,rgba(255,255,255,0.01),rgba(0,0,0,0.04));transition:all .14s;';
    // Drag events (escritorio)
    slot.addEventListener('dragover', (e) => {
      e.preventDefault();
      slot.style.borderColor = 'rgba(255,255,255,0.18)';
      slot.style.boxShadow = '0 10px 30px rgba(0,0,0,0.35)';
    });
    slot.addEventListener('dragleave', () => {
      slot.style.borderColor = 'rgba(255,255,255,0.06)';
      slot.style.boxShadow = '';
    });
    slot.addEventListener('drop', (e) => {
      e.preventDefault();
      slot.style.borderColor = 'rgba(255,255,255,0.06)';
      slot.style.boxShadow = '';
      const z = e.dataTransfer.getData('text/plain');
      // buscar la probeta que tenga ese z
      let tube = Array.from(tubesRow.children).find(t => t.dataset.z === z);
      if (!tube) {
        // si no está en tubesRow (p. ej. viene de otro slot), buscar en todo box
        tube = box.querySelector(`.mlp-tube[data-z="${z}"]`);
      }
      if (!tube) return;
      // si el slot ya contiene algo, devolverlo al tubesRow
      if (slot.firstChild) tubesRow.appendChild(slot.firstChild);
      slot.appendChild(tube);
      checkOrder();
    });

    // Touch-friendly: si hay una probeta seleccionada por tap, soltar aquí
    slot.addEventListener('click', () => {
      if (selectedTube) {
        // si slot contiene algo, devolverlo al tubesRow (y soltar la seleccionada)
        if (slot.firstChild) tubesRow.appendChild(slot.firstChild);
        slot.appendChild(selectedTube);
        clearSelection();
        checkOrder();
      }
    });

    targetRow.appendChild(slot);
  }

  // Feedback (mensajes para el jugador)
  const feedback = document.createElement('div');
  feedback.style = 'min-height:28px;margin-top:8px;color:#ffdede;text-align:center;font-size:0.95rem';

  // --- Helpers ---
  function shuffle(arr) {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  // Crea la visual de una probeta usando tus PNGs en ../assets/images/apagonColegio/<SYM>.png
  // Ahora: SOLO la imagen (PNG), sin texto; tamaño grande y responsive.
  function makeTube(el) {
    const t = document.createElement('div');
    t.className = 'mlp-tube';
    t.dataset.z = String(el.z);
    t.dataset.sym = el.sym;
    // contenedor de la probeta: centrado y con área táctil amplia
    t.style =
      'width:22vw;max-width:140px;height:26vw;max-height:180px;padding:6px;border-radius:10px;display:flex;align-items:center;justify-content:center;cursor:pointer;user-select:none;transition:transform .12s;';
    // IMAGEN (probeta PNG)
    const img = document.createElement('img');
    img.className = 'mlp-tube-img';
    img.src = `../assets/images/apagonColegio/${el.sym}.png`; // usa tus PNGs
    img.alt = `Probeta ${el.sym}`;
    img.loading = 'lazy';
    // tamaño ocupando la caja (un poco más pequeña para tener margen)
    img.style = 'width:78%;height:78%;object-fit:contain;display:block;pointer-events:none;';
    t.appendChild(img);

    // Hacer draggable para escritorio
    t.draggable = true;
    t.addEventListener('dragstart', (e) => {
      e.dataTransfer.setData('text/plain', t.dataset.z);
      // imagen temporal para drag image
      try {
        const dragImg = img.cloneNode(true);
        dragImg.style.width = '120px';
        dragImg.style.height = '160px';
        dragImg.style.position = 'absolute';
        dragImg.style.top = '-9999px';
        document.body.appendChild(dragImg);
        e.dataTransfer.setDragImage(dragImg, dragImg.width / 2, dragImg.height / 2);
        setTimeout(() => {
          try { document.body.removeChild(dragImg); } catch (err) {}
        }, 0);
      } catch (err) {
        // no crítico
      }
    });

    // Para accesibilidad: efecto visual al tocar (tap)
    t.addEventListener('touchstart', (e) => {
      // evitar efecto doble-tap nativo rápido
      e.stopPropagation();
    }, { passive: true });

    // tap en probeta (modo touch): selecciona/desselecciona
    t.addEventListener('click', () => {
      // En escritorio también sirve como selección
      if (isTouchDevice) {
        if (selectedTube === t) {
          // si ya estaba seleccionada, la soltamos al contenedor original
          clearSelection();
        } else {
          setSelection(t);
        }
      }
    });

    return t;
  }

  // --- Selección por toque (modo móvil) ---
  let selectedTube = null;
  const isTouchDevice = ('ontouchstart' in window) || navigator.maxTouchPoints > 0;

  function setSelection(tube) {
    clearSelection();
    selectedTube = tube;
    // efecto visual (elevación)
    tube.style.transform = 'translateY(-6px) scale(1.03)';
    tube.style.boxShadow = '0 18px 40px rgba(0,0,0,0.45), 0 6px 22px rgba(0,0,0,0.35)';
    // mostrar instrucción ligera
    mmInstr.textContent = 'Toca un hueco vacío para colocar la probeta seleccionada.';
  }

  function clearSelection() {
    if (selectedTube) {
      selectedTube.style.transform = '';
      selectedTube.style.boxShadow = '';
      selectedTube = null;
      mmInstr.textContent = defaultInstr;
    }
  }

  // --- Añadimos elementos al DOM y layout ---
  const defaultInstr = 'Cuatro probetas esperan su turno. Ordena su esencia de la más ligera a la más pesada — empieza por la que menos pesa.';
  const mmInstr = box.querySelector('#mm-instr');
  mmInstr.textContent = defaultInstr;

  box.appendChild(tubesRow);
  box.appendChild(targetRow);
  box.appendChild(feedback);

  // Acciones: Recolocar + Cerrar (botones táctiles grandes)
  const actions = document.createElement('div');
  actions.style = 'display:flex;gap:12px;justify-content:center;margin-top:14px;flex-wrap:wrap;';

  const resetBtn = document.createElement('button');
  resetBtn.textContent = 'Recolocar';
  resetBtn.style =
    'padding:12px 16px;border-radius:10px;background:linear-gradient(90deg,#1f2230,#121217);border:1px solid rgba(255,255,255,0.06);color:#fff;cursor:pointer;font-weight:700;font-size:0.98rem';

  const closeBtn = document.createElement('button');
  closeBtn.textContent = 'Cerrar';
  closeBtn.style =
    'padding:12px 16px;border-radius:10px;background:linear-gradient(90deg,#1f2230,#121217);border:1px solid rgba(255,255,255,0.06);color:#fff;cursor:pointer;font-weight:700;font-size:0.98rem';

  actions.appendChild(resetBtn);
  actions.appendChild(closeBtn);
  box.appendChild(actions);
  overlay.appendChild(box);
  document.body.appendChild(overlay);

  // --- POBLAR las probetas inicialmente (aleatorio) ---
  function populateTubes(arr) {
    // devolver cualquier probeta que estuviera en slots al contenedor original
    Array.from(targetRow.children).forEach(slot => {
      if (slot.firstChild) tubesRow.appendChild(slot.firstChild);
    });
    // limpiar tubesRow
    while (tubesRow.firstChild) tubesRow.removeChild(tubesRow.firstChild);
    // añadimos probetas nuevas (creadas)
    arr.forEach(el => tubesRow.appendChild(makeTube(el)));
    // reactivar interacciones visuales
    Array.from(targetRow.children).forEach(s => {
      s.style.pointerEvents = '';
      s.style.borderColor = 'rgba(255,255,255,0.06)';
      s.style.boxShadow = '';
    });
    Array.from(tubesRow.children).forEach(t => (t.style.pointerEvents = 'auto'));
    feedback.textContent = '';
    clearSelection();
  }

  // Inicializamos con distribución aleatoria
  populateTubes(shuffle(ELEMENTS));

  // --- LÓGICA: comprobar si los slots están en orden ascendente por Z ---
  function checkOrder() {
    const slotZ = Array.from(targetRow.children).map(slot => {
      const child = slot.firstChild;
      return child ? child.dataset.z : null;
    });
    if (slotZ.some(z => z === null)) {
      feedback.textContent = 'Coloca todas las probetas en los slots.';
      return;
    }
    const nums = slotZ.map(z => Number(z));
    let ok = true;
    for (let i = 1; i < nums.length; i++) {
      if (nums[i] < nums[i - 1]) { ok = false; break; }
    }
    if (ok) {
      feedback.innerHTML =
        '<strong style="color:#b6ffb6">¡Correcto! Las probetas están en orden (menor → mayor).</strong>' +
        '<div style="margin-top:8px;color:#d6ffd6"><strong>Pista:</strong> Revisa el cajón del laboratorio.</div>';
      // deshabilitar más movimientos
      Array.from(targetRow.children).forEach(s => (s.style.pointerEvents = 'none'));
      Array.from(tubesRow.children).forEach(t => (t.style.pointerEvents = 'none'));
      mmInstr.textContent = 'Resuelto — pulsa Cerrar para volver.';
      clearSelection();
    } else {
      feedback.textContent = 'Orden incorrecto. Intenta reorganizarlas.';
    }
  }

  // --- Reset (recolocar) ---
  resetBtn.addEventListener('click', () => {
    Array.from(targetRow.children).forEach(slot => {
      if (slot.firstChild) tubesRow.appendChild(slot.firstChild);
    });
    populateTubes(shuffle(ELEMENTS));
    feedback.textContent = 'Probetas recolocadas. Intenta de nuevo.';
  });

  // --- Cerrar y limpieza final ---
  function cleanup() {
    document.removeEventListener('keydown', onKey);
    overlay.remove();
    if (typeof resumeGameTimer === 'function') resumeGameTimer();
    if (typeof onClose === 'function') onClose();
  }
  closeBtn.addEventListener('click', cleanup);

  // ESC cierra
  function onKey(e) { if (e.key === 'Escape') cleanup(); }
  document.addEventListener('keydown', onKey);

  // --- Soporte táctil adicional: permitir "tap pick + tap drop" desde cualquier probeta/slot
  // (ya implementado: t.addEventListener('click') en makeTube y slot click)
  // Para mejorar la UX: si tocan fuera del box, se deselecciona
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) {
      // tocar fuera del box cancela selección (no cierra)
      clearSelection();
    }
  });

  // Evitar scroll de fondo en iOS mientras está abierto (mejora mobile)
  const prevOverflow = document.documentElement.style.overflow;
  document.documentElement.style.overflow = 'hidden';

  // Cuando cerramos, restaurar overflow
  const origCleanup = cleanup;
  cleanup = function() {
    document.documentElement.style.overflow = prevOverflow || '';
    document.removeEventListener('keydown', onKey);
    try { overlay.remove(); } catch(e){ /*ignore*/ }
    if (typeof resumeGameTimer === 'function') resumeGameTimer();
    if (typeof onClose === 'function') onClose();
  };

  // re-asignar botones tras redefinir cleanup
  closeBtn.onclick = cleanup;
  // Aseguramos que resetBtn no pierde su handler
  resetBtn.addEventListener('click', () => {
    Array.from(targetRow.children).forEach(slot => {
      if (slot.firstChild) tubesRow.appendChild(slot.firstChild);
    });
    populateTubes(shuffle(ELEMENTS));
    feedback.textContent = 'Probetas recolocadas. Intenta de nuevo.';
  });

  // Devolvemos handle para cerrar desde fuera si se desea
  return { close: cleanup };
}
