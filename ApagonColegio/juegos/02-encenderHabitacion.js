// juegos/minijuegoLinterna/main.js
// Minijuego: pulsa sobre la linterna en la imagen para obtener la carta 5.
// Luego la escena cambia, y al pulsar el papel se obtiene la carta 7.

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
  overlay.style.animation = "fadeIn 0.3s ease forwards";

  /* ======== Imagen (contenedor) ======== */
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
  img.style.transition = "opacity 0.4s ease";

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

  /* ======== Áreas interactivas ========
     Ajustadas: la posición del papel se ha desplazado hacia abajo y a la izquierda
  */
  const linternaArea = {
    x1: 0.58, // 60% aprox (linterna)
    y1: 0.78,
    x2: 0.83,
    y2: 0.93,
  };

  // Papel: desplazado hacia abajo y a la izquierda respecto a la versión anterior
  const paperArea = {
    x1: 0.28, // izquierda
    y1: 0.48, // más abajo
    x2: 0.50, // anchura aproximada
    y2: 0.58, // un poco más abajo
  };

  let linternaEncontrada = false;
  let paperEncontrado = false;
  let segundaEscena = false;

  img.addEventListener("click", (ev) => {
    const rect = img.getBoundingClientRect();
    const relX = (ev.clientX - rect.left) / rect.width;
    const relY = (ev.clientY - rect.top) / rect.height;

    // Si aún no hemos pasado a la segunda escena, buscamos la linterna
    if (!segundaEscena) {
      if (
        relX >= linternaArea.x1 &&
        relX <= linternaArea.x2 &&
        relY >= linternaArea.y1 &&
        relY <= linternaArea.y2
      ) {
        if (linternaEncontrada) return;
        linternaEncontrada = true;
        mostrarMensaje("🔦 Coge la carta 5", cambiarEscena);
      }
      return;
    }

    // En la segunda escena, comprobar si se pulsa el papel (carta 7)
    if (segundaEscena && !paperEncontrado) {
      if (
        relX >= paperArea.x1 &&
        relX <= paperArea.x2 &&
        relY >= paperArea.y1 &&
        relY <= paperArea.y2
      ) {
        paperEncontrado = true;
        mostrarMensaje("📄 Coge la carta 7", marcarPapel);
      }
    }
  });

  /* ======== FUNCIONES UI ======== */
  function mostrarMensaje(texto, callback) {
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
    boxMsg.style.padding = "24px 30px";
    boxMsg.style.fontFamily = '"Poppins", sans-serif';
    boxMsg.style.fontSize = "1.15rem";
    boxMsg.style.textAlign = "center";
    boxMsg.style.boxShadow = "0 12px 30px rgba(0,0,0,0.6)";
    boxMsg.style.border = "1px solid rgba(255,255,255,0.1)";
    boxMsg.innerHTML = texto;

    const btn = document.createElement("button");
    btn.textContent = "Aceptar";
    btn.style.marginTop = "16px";
    btn.style.padding = "9px 18px";
    btn.style.background = "linear-gradient(180deg,#2fd09f,#0db07e)";
    btn.style.color = "#fff";
    btn.style.fontWeight = "700";
    btn.style.border = "none";
    btn.style.borderRadius = "8px";
    btn.style.cursor = "pointer";
    btn.style.boxShadow = "0 8px 18px rgba(0,0,0,0.4)";
    btn.addEventListener("click", () => {
      modal.remove();
      if (typeof callback === "function") callback();
    });

    boxMsg.appendChild(document.createElement("br"));
    boxMsg.appendChild(btn);
    modal.appendChild(boxMsg);
    document.body.appendChild(modal);
  }

  /* ======== Cambiar a imagen encendida ======== */
  function cambiarEscena() {
    img.style.opacity = "0";
    setTimeout(() => {
      img.src = "../assets/images/apagonColegio/habitacionEncendida.png";
      img.style.opacity = "1";
      img.style.cursor = "crosshair";
      segundaEscena = true;
    }, 400);
  }

  /* ======== Marcar papel: colocar badge en la posición correcta ======== */
  function marcarPapel() {
    // calcular el centro real (porcentaje) del área de papel
    const cx = (paperArea.x1 + paperArea.x2) / 2;
    const cy = (paperArea.y1 + paperArea.y2) / 2;

    const mark = document.createElement("div");
    Object.assign(mark.style, {
      position: "absolute",
      left: `${cx * 100}%`,
      top: `${cy * 100}%`,
      transform: "translate(-50%, -50%) scale(0.9)",
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
    });
    mark.textContent = "Carta 7 ✓";
    imgContainer.appendChild(mark);

    // animación de entrada
    requestAnimationFrame(() => {
      mark.style.opacity = "1";
      mark.style.transform = "translate(-50%, -50%) scale(1)";
    });
  }

  /* ======== Cerrar ======== */
  function cerrar() {
    try { overlay.remove(); } catch (e) {}
    if (typeof resumeGameTimer === "function") resumeGameTimer();
    if (typeof onClose === "function") onClose();
  }

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") cerrar();
  });

  // click fuera no cierra (evita cierres accidentales) — solo el botón salir o Escape
}
