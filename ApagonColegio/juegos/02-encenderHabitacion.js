// juegos/minijuegoLinterna/main.js
// Minijuego: pulsa sobre la linterna en la imagen para obtener la carta 5.
// Luego la escena cambia, y al pulsar el papel (o el cubo azul) se obtiene la carta 26.

export function startMinigame(opts = {}) {
  const { onClose, pauseGameTimer, resumeGameTimer } = opts;

  if (typeof pauseGameTimer === "function") pauseGameTimer();

  /* ===== Overlay general ===== */
  const overlay = document.createElement("div");
  Object.assign(overlay.style, {
    position: "fixed",
    inset: "0",
    background: "rgba(0, 0, 0, 0.9)",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    zIndex: "2500",
    padding: "10px",
    boxSizing: "border-box",
  });

  /* ===== Imagen ===== */
  const imgContainer = document.createElement("div");
  Object.assign(imgContainer.style, {
    flex: "1",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    width: "100%",
    maxHeight: "calc(100vh - 100px)",
    overflow: "hidden",
    position: "relative",
  });

  const img = document.createElement("img");
  img.src = "./images/habitacionApagada.png";
  img.alt = "Habitación oscura";
  Object.assign(img.style, {
    width: "auto",
    height: "100%",
    maxWidth: "100%",
    objectFit: "contain",
    cursor: "crosshair",
    transition: "opacity 0.4s ease",
    display: "block",
  });

  imgContainer.appendChild(img);
  overlay.appendChild(imgContainer);

  /* ===== Botón salir ===== */
  const btnSalir = document.createElement("button");
  btnSalir.textContent = "Salir";
  Object.assign(btnSalir.style, {
    marginTop: "12px",
    padding: "10px 18px",
    fontFamily: '"Poppins", sans-serif',
    fontSize: "1rem",
    fontWeight: "700",
    color: "#fff",
    background: "linear-gradient(180deg, #ff4444, #bb2222)",
    border: "none",
    borderRadius: "10px",
    cursor: "pointer",
    boxShadow: "0 8px 20px rgba(0,0,0,0.4)",
  });
  btnSalir.addEventListener("click", cerrar);
  overlay.appendChild(btnSalir);

  document.body.appendChild(overlay);

  /* ===== Coordenadas (normalizadas 0..1) ===== */

  // Linterna escena apagada
  const linternaArea = { x1: 0.58, y1: 0.78, x2: 0.83, y2: 0.93 };

  // Papel escena encendida (ligero ajuste)
  const paperArea = { x1: 0.29, y1: 0.46, x2: 0.51, y2: 0.56 };

  // NUEVO: cubo azul escena encendida (aprox. abajo a la izquierda, ajústalo si hace falta)
  const bucketArea = { x1: 0.05, y1: 0.78, x2: 0.20, y2: 0.97 };

  function isInside(area, x, y) {
    return (
      x >= area.x1 &&
      x <= area.x2 &&
      y >= area.y1 &&
      y <= area.y2
    );
  }

  let linternaEncontrada = false;
  let paperEncontrado = false;
  let cuboEncontrado = false;
  let segundaEscena = false;

  img.addEventListener("click", (e) => {
    const rect = img.getBoundingClientRect();
    if (rect.width === 0 || rect.height === 0) return;

    const x = (e.clientX - rect.left) / rect.width;
    const y = (e.clientY - rect.top) / rect.height;

    // ESCENA 1: apagada, buscar linterna
    if (!segundaEscena) {
      if (!linternaEncontrada && isInside(linternaArea, x, y)) {
        linternaEncontrada = true;
        mostrarMensaje("🔦 Coge la carta 5", cambiarEscena);
      }
      return;
    }

    // ESCENA 2: encendida, papel o cubo azul
    if (segundaEscena && !paperEncontrado) {
      if (isInside(paperArea, x, y)) {
        paperEncontrado = true;
        // Reutilizamos el mismo flujo que con el papel
        mostrarMensaje("📄 Coge la carta 26", marcarPapel);
      }
    }
    // ESCENA 2: encendida, papel o cubo azul
    if (segundaEscena && !cuboEncontrado) {
      if (isInside(bucketArea, x, y)) {
        cuboEncontrado = true;
        // Reutilizamos el mismo flujo que con el papel
        mostrarMensaje("🟦 Coge la carta 8", marcarPapel);
      }
    }
  });
  

  /* ===== Mostrar mensajes ===== */
  function mostrarMensaje(texto, callback) {
    const modal = document.createElement("div");
    Object.assign(modal.style, {
      position: "fixed",
      inset: "0",
      background: "rgba(0,0,0,0.7)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      zIndex: "2600",
    });

    const boxMsg = document.createElement("div");
    Object.assign(boxMsg.style, {
      background: "#1c1f2b",
      color: "#fff",
      borderRadius: "12px",
      padding: "24px 30px",
      fontFamily: '"Poppins", sans-serif',
      fontSize: "1.15rem",
      textAlign: "center",
      boxShadow: "0 12px 30px rgba(0,0,0,0.6)",
      border: "1px solid rgba(255,255,255,0.1)",
      maxWidth: "92%",
    });
    boxMsg.innerHTML = texto;

    const btn = document.createElement("button");
    btn.textContent = "Aceptar";
    Object.assign(btn.style, {
      marginTop: "16px",
      padding: "9px 18px",
      background: "linear-gradient(180deg,#2fd09f,#0db07e)",
      color: "#fff",
      fontWeight: "700",
      border: "none",
      borderRadius: "8px",
      cursor: "pointer",
      boxShadow: "0 8px 18px rgba(0,0,0,0.4)",
    });
    btn.addEventListener("click", () => {
      modal.remove();
      if (typeof callback === "function") callback();
    });

    boxMsg.appendChild(document.createElement("br"));
    boxMsg.appendChild(btn);
    modal.appendChild(boxMsg);
    document.body.appendChild(modal);
  }

  /* ===== Cambiar a la imagen encendida ===== */
  function cambiarEscena() {
    img.style.opacity = "0";
    setTimeout(() => {
      img.src = "./images/habitacionEncendida.png";
      img.style.opacity = "1";
      img.style.cursor = "crosshair";
      segundaEscena = true;
    }, 400);
  }

  /* ===== Marcar carta del papel ===== */
  function marcarPapel() {
    const imgRect = img.getBoundingClientRect();
    const contRect = imgContainer.getBoundingClientRect();

    const cxPct = (paperArea.x1 + paperArea.x2) / 2;
    const cyPct = (paperArea.y1 + paperArea.y2) / 2;

    const pxInImgX = imgRect.width * cxPct;
    const pxInImgY = imgRect.height * cyPct;

    const leftPx = imgRect.left - contRect.left + pxInImgX;
    const topPx = imgRect.top - contRect.top + pxInImgY;

    const mark = document.createElement("div");
    Object.assign(mark.style, {
      position: "absolute",
      left: `${leftPx}px`,
      top: `${topPx}px`,
      transform: "translate(-50%, -50%) scale(0.95)",
      zIndex: "20",
      background: "linear-gradient(180deg,#2fd09f,#0db07e)",
      color: "#042214",
      fontWeight: "800",
      padding: "8px 10px",
      borderRadius: "999px",
      boxShadow: "0 8px 20px rgba(0,0,0,0.45)",
      fontFamily: '"Poppins",sans-serif',
      fontSize: "0.95rem",
      opacity: "0",
      transition: "transform .25s ease, opacity .25s ease",
      pointerEvents: "none",
      whiteSpace: "nowrap",
    });
    mark.textContent = "Carta encontrada ✓";
    imgContainer.appendChild(mark);

    requestAnimationFrame(() => {
      mark.style.opacity = "1";
      mark.style.transform = "translate(-50%, -50%) scale(1)";
    });

    setTimeout(() => {
      mark.style.opacity = "0";
      mark.style.transform = "translate(-50%, -50%) scale(0.9)";
      setTimeout(() => {
        try {
          mark.remove();
        } catch (e) {}
      }, 300);
    }, 2500);
  }

  /* ===== Cerrar minijuego ===== */
  function cerrar() {
    try {
      overlay.remove();
    } catch (e) {}
    if (typeof resumeGameTimer === "function") resumeGameTimer();
    if (typeof onClose === "function") onClose();
  }

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") cerrar();
  });
}
