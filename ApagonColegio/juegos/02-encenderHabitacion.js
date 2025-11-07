// juegos/minijuegoLinterna/main.js
// Minijuego: pulsa sobre la linterna en la imagen para obtener la carta 5.
// Luego la escena cambia, y hay un botón "Salir" para cerrar el minijuego.

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

  /* ======== Imagen ======== */
  const imgContainer = document.createElement("div");
  imgContainer.style.flex = "1";
  imgContainer.style.display = "flex";
  imgContainer.style.alignItems = "center";
  imgContainer.style.justifyContent = "center";
  imgContainer.style.width = "100%";
  imgContainer.style.maxHeight = "calc(100vh - 100px)";
  imgContainer.style.overflow = "hidden";

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

  /* ======== Área clicable (linterna) ======== */
  const linternaArea = {
    x1: 0.58, // ajustar según la imagen
    y1: 0.78,
    x2: 0.83,
    y2: 0.93,
  };

  let linternaEncontrada = false;

  img.addEventListener("click", (ev) => {
    const rect = img.getBoundingClientRect();
    const relX = (ev.clientX - rect.left) / rect.width;
    const relY = (ev.clientY - rect.top) / rect.height;

    if (
      relX >= linternaArea.x1 &&
      relX <= linternaArea.x2 &&
      relY >= linternaArea.y1 &&
      relY <= linternaArea.y2
    ) {
      if (linternaEncontrada) return;
      linternaEncontrada = true;
      mostrarMensaje();
    }
  });

  /* ======== Modal: Coge la carta ======== */
  function mostrarMensaje() {
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
    boxMsg.innerHTML = "🔦 <strong>Coge la carta 5</strong>";

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
      cambiarEscena();
    });

    boxMsg.appendChild(document.createElement("br"));
    boxMsg.appendChild(btn);
    modal.appendChild(boxMsg);
    document.body.appendChild(modal);
  }

  /* ======== Cambiar imagen ======== */
  function cambiarEscena() {
    img.style.opacity = "0";
    setTimeout(() => {
      img.src = "../assets/images/apagonColegio/habitacionEncendida.png";
      img.style.opacity = "1";
      img.style.cursor = "default";
    }, 400);
  }

  /* ======== Función cerrar ======== */
  function cerrar() {
    overlay.remove();
    if (typeof resumeGameTimer === "function") resumeGameTimer();
    if (typeof onClose === "function") onClose();
  }

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") cerrar();
  });
}
