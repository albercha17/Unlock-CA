// juegos/minijuegoLinterna/main.js
// Minijuego: pulsa sobre la linterna en la imagen para obtener la carta 5.
// Luego la escena cambia, y al pulsar el papel se obtiene la carta 7.
// Hay un botón "Salir" para cerrar el minijuego.

export function startMinigame(opts = {}) {
  const { onClose, pauseGameTimer, resumeGameTimer } = opts;

  if (typeof pauseGameTimer === "function") pauseGameTimer();

  /* ======== Crear overlay ======== */
  const overlay = document.createElement("div");
  overlay.style.position = "fixed";
  overlay.style.inset = "0";
  overlay.style.background = "rgba(0, 0, 0, 0.9)";
  overlay.style.display = "flex";
  overlay.style.flexDirection = "column";
  overlay.style.alignItems = "center";
  overlay.style.justifyContent = "center";
  overlay.style.zIndex = "2500";
  overlay.style.padding = "10px";
  overlay.style.boxSizing = "border-box";
  overlay.style.animation = "fadeIn 0.25s ease forwards";

  /* ======== Imagen container ======== */
  const imgContainer = document.createElement("div");
  imgContainer.style.flex = "1";
  imgContainer.style.display = "flex";
  imgContainer.style.alignItems = "center";
  imgContainer.style.justifyContent = "center";
  imgContainer.style.width = "100%";
  imgContainer.style.maxHeight = "calc(100vh - 100px)";
  imgContainer.style.overflow = "hidden";
  imgContainer.style.position = "relative";

  const img = document.createElement("img");
  img.src = "../assets/images/apagonColegio/habitacionApagada.png";
  img.alt = "Habitación oscura";
  img.style.width = "auto";
  img.style.height = "100%";
  img.style.maxWidth = "100%";
  img.style.objectFit = "contain";
  img.style.cursor = "crosshair";
  img.style.transition = "opacity 0.35s ease";

  imgContainer.appendChild(img);
  overlay.appendChild(imgContainer);

  /* ======== Botón de salir ======== */
  const btnSalir = document.createElement("button");
  btnSalir.textContent = "🚪 Salir";
  btnSalir.style.marginTop = "12px";
  btnSalir.style.padding = "10px 18px";
  btnSalir.style.fontFamily = '"Poppins", sans-serif';
  btnSalir.style.fontSize = "1rem";
  btnSalir.style.fontWeight = "700";
  btnSalir.style.color = "#fff";
  btnSalir.style.background = "linear-gradient(180deg, #ff4444, #bb2222)";
  btnSalir.style.border = "none";
  btnSalir.style.borderRadius = "10px";
  btnSalir.style.cursor = "pointer";
  btnSalir.style.boxShadow = "0 8px 20px rgba(0,0,0,0.4)";
  btnSalir.addEventListener("click", cerrar);

  overlay.appendChild(btnSalir);
  document.body.appendChild(overlay);

  /* ======== Áreas interactuables (porcentuales respecto a la imagen) ======== */
  const linternaArea = { x1: 0.58, y1: 0.78, x2: 0.83, y2: 0.93 };

  // He movido el área del papel hacia abajo (encima de la mesa).
  // Si hay que ajustarlo más, cambia valores en increments de 0.01 (1%).
  const paperArea = { x1: 0.32, y1: 0.36, x2: 0.52, y2: 0.46 };

  // DEBUG: muestra la guía visual del paperArea y del linternaArea
  const SHOW_DEBUG = true; // pon false para esconder las guías

  let linternaEncontrada = false;
  let secondSceneActive = false;
  let paperPicked = false;

  /* ======== Click sobre la imagen ======== */
  function onImageClick(ev) {
    const rect = img.getBoundingClientRect();
    const relX = (ev.clientX - rect.left) / rect.width;
    const relY = (ev.clientY - rect.top) / rect.height;

    // console.log('click rel', relX.toFixed(3), relY.toFixed(3));

    if (!secondSceneActive) {
      if (relX >= linternaArea.x1 && relX <= linternaArea.x2 && relY >= linternaArea.y1 && relY <= linternaArea.y2) {
        if (linternaEncontrada) return;
        linternaEncontrada = true;
        efectoHaz(() => mostrarMensajeCarta5());
      }
      return;
    }

    if (secondSceneActive && !paperPicked) {
      if (relX >= paperArea.x1 && relX <= paperArea.x2 && relY >= paperArea.y1 && relY <= paperArea.y2) {
        paperPicked = true;
        mostrarMensajeCarta7();
      }
    }
  }

  img.addEventListener("click", onImageClick);

  /* ======== Mostrar guías visuales temporales (si SHOW_DEBUG true) ======== */
  function drawDebugAreas() {
    // elimina anteriores si existen
    const existing = imgContainer.querySelectorAll(".debug-area");
    existing.forEach(e => e.remove());

    if (!SHOW_DEBUG) return;

    // Helper para dibujar una caja porcentual sobre la imagenContainer
    function addDebugBox(area, color = "rgba(255,255,255,0.2)") {
      const box = document.createElement("div");
      box.className = "debug-area";
      box.style.position = "absolute";
      box.style.left = (area.x1 * 100) + "%";
      box.style.top = (area.y1 * 100) + "%";
      box.style.width = ((area.x2 - area.x1) * 100) + "%";
      box.style.height = ((area.y2 - area.y1) * 100) + "%";
      box.style.border = `2px dashed ${color}`;
      box.style.background = color.replace("0.2", "0.06");
      box.style.zIndex = "60";
      box.style.pointerEvents = "none";
      imgContainer.appendChild(box);
    }

    addDebugBox(linternaArea, "rgba(255,200,80,0.22)");
    addDebugBox(paperArea, "rgba(120,200,255,0.22)");
  }

  // dibuja al empezar y cada vez que la imagen cambie tamaño/posición (resize/rotation)
  drawDebugAreas();
  const resizeObs = new ResizeObserver(() => drawDebugAreas());
  resizeObs.observe(img);
  window.addEventListener("orientationchange", drawDebugAreas);

  /* ======== Efecto visual de haz de linterna ======== */
  function efectoHaz(done) {
    const glow = document.createElement("div");
    glow.style.position = "absolute";
    glow.style.pointerEvents = "none";
    glow.style.left = "0";
    glow.style.top = "0";
    glow.style.width = "100%";
    glow.style.height = "100%";
    glow.style.zIndex = "50";
    glow.style.background = `radial-gradient(ellipse at ${((linternaArea.x1+linternaArea.x2)/2)*100}% ${((linternaArea.y1+linternaArea.y2)/2)*100}%, rgba(255,240,200,0.28) 0%, rgba(255,240,200,0.12) 12%, rgba(0,0,0,0) 40%)`;
    glow.style.opacity = "0";
    glow.style.transition = "opacity 300ms ease, transform 350ms ease";
    imgContainer.appendChild(glow);
    requestAnimationFrame(() => {
      glow.style.opacity = "1";
      glow.style.transform = "scale(1.02)";
    });
    setTimeout(() => {
      glow.style.opacity = "0";
      glow.style.transform = "scale(1.08)";
      setTimeout(() => { try { glow.remove(); } catch (e) {} if (typeof done === "function") done(); }, 360);
    }, 340);
    try { if (navigator.vibrate) navigator.vibrate(50); } catch (e) {}
  }

  /* ======== Mensajes y modales ======== */
  function mostrarMensajeCarta5() {
    mostrarModalCentral("🔦 <strong>Coge la carta 5</strong>", "Aceptar", () => cambiarEscena());
  }
  function mostrarMensajeCarta7() {
    mostrarModalCentral("📄 <strong>Coge la carta 7</strong>", "Aceptar", () => marcarPapelRecogido());
  }

  function mostrarModalCentral(htmlContent, btnText = "Aceptar", onAccept) {
    const modal = document.createElement("div");
    modal.style.position = "fixed";
    modal.style.inset = "0";
    modal.style.background = "rgba(0,0,0,0.7)";
    modal.style.display = "flex";
    modal.style.alignItems = "center";
    modal.style.justifyContent = "center";
    modal.style.zIndex = "2600";

    const boxMsg = document.createElement("div");
    boxMsg.style.background = "#1c1f2b";
    boxMsg.style.color = "#fff";
    boxMsg.style.borderRadius = "12px";
    boxMsg.style.padding = "20px 26px";
    boxMsg.style.fontFamily = '"Poppins", sans-serif';
    boxMsg.style.fontSize = "1.05rem";
    boxMsg.style.textAlign = "center";
    boxMsg.style.boxShadow = "0 12px 30px rgba(0,0,0,0.6)";
    boxMsg.style.border = "1px solid rgba(255,255,255,0.08)";
    boxMsg.innerHTML = htmlContent;

    const btn = document.createElement("button");
    btn.textContent = btnText;
    btn.style.marginTop = "14px";
    btn.style.padding = "9px 16px";
    btn.style.background = "linear-gradient(180deg,#2fd09f,#0db07e)";
    btn.style.color = "#fff";
    btn.style.fontWeight = "700";
    btn.style.border = "none";
    btn.style.borderRadius = "8px";
    btn.style.cursor = "pointer";
    btn.style.boxShadow = "0 8px 18px rgba(0,0,0,0.4)";
    btn.addEventListener("click", () => {
      modal.remove();
      if (typeof onAccept === "function") onAccept();
    });

    boxMsg.appendChild(document.createElement("br"));
    boxMsg.appendChild(btn);
    modal.appendChild(boxMsg);
    document.body.appendChild(modal);
  }

  /* ======== Cambiar imagen a encendida (segunda escena) ======== */
  function cambiarEscena() {
    img.style.opacity = "0";
    setTimeout(() => {
      img.src = "../assets/images/apagonColegio/habitacionEncendida.png";
      img.style.opacity = "1";
      img.style.cursor = "crosshair";
      secondSceneActive = true;
      // redraw debug boxes for new scene
      drawDebugAreas();
    }, 380);
  }

  /* ======== Marcar papel como recogido (visual) ======== */
  function marcarPapelRecogido() {
    const centerX = (paperArea.x1 + paperArea.x2) / 2;
    const centerY = (paperArea.y1 + paperArea.y2) / 2;

    const mark = document.createElement("div");
    mark.style.position = "absolute";
    mark.style.left = (centerX * 100) + "%";
    mark.style.top = (centerY * 100) + "%";
    mark.style.transform = "translate(-50%, -50%) scale(0.9)";
    mark.style.zIndex = "70";
    mark.style.pointerEvents = "none";
    mark.style.background = "linear-gradient(180deg,#2fd09f,#0db07e)";
    mark.style.color = "#042214";
    mark.style.fontWeight = "800";
    mark.style.padding = "8px 10px";
    mark.style.borderRadius = "999px";
    mark.style.boxShadow = "0 8px 20px rgba(0,0,0,0.45)";
    mark.style.fontFamily = '"Poppins",sans-serif';
    mark.style.fontSize = "0.9rem";
    mark.textContent = "Carta 7 ✓";

    imgContainer.appendChild(mark);

    requestAnimationFrame(() => {
      mark.style.transition = "transform 260ms cubic-bezier(.2,.9,.2,1), opacity 260ms";
      mark.style.transform = "translate(-50%,-50%) scale(1.06)";
    });

    img.style.cursor = "default";
  }

  /* ======== Cerrar y limpieza ======== */
  function cerrar() {
    try { img.removeEventListener("click", onImageClick); } catch (e) {}
    try { overlay.remove(); } catch (e) {}
    try { resizeObs.disconnect(); } catch (e) {}
    if (typeof resumeGameTimer === "function") resumeGameTimer();
    if (typeof onClose === "function") onClose();
  }

  document.addEventListener("keydown", function onKey(e) {
    if (e.key === "Escape") {
      document.removeEventListener("keydown", onKey);
      cerrar();
    }
  });

  overlay.addEventListener("click", (ev) => {
    if (ev.target === overlay) cerrar();
  });

  // Fin startMinigame
}
