// juegos/miniJuegoLevantarProyectar/main.js
// Minijuego: ordenar 4 probetas (C, N, O, S) por su número atómico (de menor a mayor).
// Ahora: SOLO se muestran las probetas (PNG) — sin nombres ni Z — y son más grandes.
// Exporta startMinigame(opts) que crea un overlay y maneja la lógica.
// opts: { onClose?: fn, pauseGameTimer?: fn, resumeGameTimer?: fn }

export function startMinigame(opts = {}) {
  const { onClose, pauseGameTimer, resumeGameTimer } = opts;

  // Si se nos pasa la función para pausar el temporizador principal, la ejecutamos.
  if (typeof pauseGameTimer === 'function') pauseGameTimer();

  // --- OVERLAY y CAJA PRINCIPAL ---
  const overlay = document.createElement('div');
  overlay.style =
    'position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,0.6);z-index:2500;padding:18px;';

  const box = document.createElement('div');
  box.style =
    'width:760px;max-width:96%;background:#0f1116;border-radius:12px;padding:22px;color:#fff;border:1px solid rgba(255,255,255,0.04);box-shadow:0 20px 60px rgba(0,0,0,0.7);font-family:inherit;';

  box.innerHTML =
    '<h3 style="margin:0 0 8px 0">Carta 01 — Ordena las Probetas</h3>' +
    '<div style="color:#d6d6d6;margin-bottom:10px">Cuatro probetas esperan su turno. Su esencia no miente: el orden correcto está en sus raíces.</div>';

  // Contenedor inicial de probetas (donde aparecen al inicio)
  const tubesRow = document.createElement('div');
  tubesRow.style = 'display:flex;gap:18px;justify-content:center;margin:18px 0;flex-wrap:wrap;';

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
  // Slots más grandes para ajustarse a las probetas grandes
  targetRow.style = 'display:flex;gap:18px;justify-content:center;margin:14px 0;flex-wrap:wrap;';

  // Creamos 4 slots vacíos (para ordenar) — slots más grandes
  for (let i = 0; i < 4; i++) {
    const slot = document.createElement('div');
    slot.className = 'mlp-slot';
    slot.dataset.index = String(i);
    slot.style =
      'width:150px;height:200px;border-radius:14px;border:2px dashed rgba(255,255,255,0.06);display:flex;align-items:center;justify-content:center;background:linear-gradient(180deg,rgba(255,255,255,0.01),rgba(0,0,0,0.04));';
    // Drag events
    slot.addEventListener('dragover', (e) => {
      e.preventDefault();
      slot.style.borderColor = 'rgba(255,255,255,0.18)';
      slot.style.boxShadow = '0 10px 40px rgba(0,0,0,0.45)';
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
      // buscar la probeta que tenga ese z en tubesRow o incluso en otro slot (para mover entre slots)
      let tube = Array.from(tubesRow.children).find(t => t.dataset.z === z);
      if (!tube) {
        tube = box.querySelector(`.mlp-tube[data-z="${z}"]`);
      }
      if (!tube) return;
      // si el slot ya contiene algo, devolverlo al tubesRow para no perder ningún nodo
      if (slot.firstChild) {
        tubesRow.appendChild(slot.firstChild);
      }
      // colocar la probeta en el slot
      slot.appendChild(tube);
      checkOrder();
    });

    targetRow.appendChild(slot);
  }

  // Feedback (mensajes para el jugador)
  const feedback = document.createElement('div');
  feedback.style = 'min-height:28px;margin-top:10px;color:#ffdede;text-align:center';

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
  // Ahora: SOLO la imagen, sin texto bajo la probeta. Imagen más grande.
  function makeTube(el) {
    const t = document.createElement('div');
    t.className = 'mlp-tube';
    t.dataset.z = String(el.z);
    t.dataset.sym = el.sym;
    // contenedor reducido (sin labels)
    t.style =
      'width:150px;height:200px;padding:6px;border-radius:12px;display:flex;align-items:center;justify-content:center;cursor:pointer;user-select:none;';

    const img = document.createElement('img');
    img.className = 'mlp-tube-img';
    // ruta a tus PNGs
    img.src = `../assets/images/apagonColegio/${el.sym}.png`;
    img.alt = `Probeta ${el.sym}`;
    img.loading = 'lazy';
    // IMAGEN MÁS GRANDE: ajusta width/height según necesidad
    img.style = 'width:120px;height:160px;object-fit:contain;display:block;pointer-events:none;';

    t.appendChild(img);

    // Hacer draggable: transferimos el número atómico en dataTransfer
    t.draggable = true;
    t.addEventListener('dragstart', (e) => {
      e.dataTransfer.setData('text/plain', t.dataset.z);
      // crear imagen temporal para el "drag image"
      try {
        const dragImg = img.cloneNode(true);
        dragImg.style.width = '120px';
        dragImg.style.height = '160px';
        dragImg.style.position = 'absolute';
        dragImg.style.top = '-9999px';
        document.body.appendChild(dragImg);
        e.dataTransfer.setDragImage(dragImg, 60, 80);
        // limpiar
        setTimeout(() => {
          try { document.body.removeChild(dragImg); } catch (err) {}
        }, 0);
      } catch (err) {
        // no crítico
      }
    });

    return t;
  }

  // Poblamos la zona inicial con un array de elementos
  function populateTubes(arr) {
    // devolver cualquier probeta que estuviera en slots al contenedor original
    Array.from(targetRow.children).forEach(slot => {
      if (slot.firstChild) {
        tubesRow.appendChild(slot.firstChild);
      }
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
  }

  // Añadimos al box
  box.appendChild(tubesRow);
  box.appendChild(targetRow);
  box.appendChild(feedback);

  // Acciones: Recolocar + Cerrar
  const actions = document.createElement('div');
  actions.style = 'display:flex;gap:12px;justify-content:center;margin-top:16px;';

  const resetBtn = document.createElement('button');
  resetBtn.textContent = 'Recolocar';
  resetBtn.style =
    'padding:10px 14px;border-radius:10px;background:transparent;border:1px solid rgba(255,255,255,0.06);color:#fff;cursor:pointer;font-weight:700';

  const closeBtn = document.createElement('button');
  closeBtn.textContent = 'Cerrar';
  closeBtn.style =
    'padding:10px 14px;border-radius:10px;background:transparent;border:1px solid rgba(255,255,255,0.06);color:#fff;cursor:pointer;font-weight:700';

  actions.appendChild(resetBtn);
  actions.appendChild(closeBtn);
  box.appendChild(actions);
  overlay.appendChild(box);
  document.body.appendChild(overlay);

  // Lógica para comprobar orden en los slots (ascendente por Z)
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
    } else {
      feedback.textContent = 'Orden incorrecto. Intenta reorganizarlas.';
    }
  }

  // Reset (recolocar) — devuelve las probetas de los slots y baraja de nuevo
  resetBtn.addEventListener('click', () => {
    Array.from(targetRow.children).forEach(slot => {
      if (slot.firstChild) tubesRow.appendChild(slot.firstChild);
    });
    populateTubes(shuffle(ELEMENTS));
    feedback.textContent = 'Probetas recolocadas. Intenta de nuevo.';
  });

  // Cerrar y limpieza final
  function cleanup() {
    document.removeEventListener('keydown', onKey);
    overlay.remove();
    if (typeof resumeGameTimer === 'function') resumeGameTimer();
    if (typeof onClose === 'function') onClose();
  }
  closeBtn.addEventListener('click', cleanup);

  function onKey(e) { if (e.key === 'Escape') cleanup(); }
  document.addEventListener('keydown', onKey);

  // Inicializamos con una distribución aleatoria
  populateTubes(shuffle(ELEMENTS));

  // devolvemos handle por si quieres cerrarlo desde fuera
  return { close: cleanup };
}
