// ./juegos/99-microscopio.js

// Pequeña utilidad para generar la imagen de la muestra
function buildSampleSvg(digit) {
  const svg =
    `<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 600 600'>
      <defs>
        <radialGradient id='g' cx='48%' cy='44%' r='60%'>
          <stop offset='0%' stop-color='#2dd4bf' stop-opacity='0.35'/>
          <stop offset='50%' stop-color='#1e3a8a' stop-opacity='0.65'/>
          <stop offset='100%' stop-color='#020617' stop-opacity='0.9'/>
        </radialGradient>
      </defs>
      <rect width='600' height='600' fill='url(#g)'/>
      <g font-family="Poppins, system-ui" font-size='220' font-weight='800'
         fill='#fef9c3' opacity='0.95'>
        <text x='50%' y='54%' text-anchor='middle'>${digit}</text>
      </g>
      <g stroke='#22d3ee' stroke-width='4' opacity='0.45' fill='none'>
        <circle cx='150' cy='150' r='40'/>
        <circle cx='430' cy='360' r='28'/>
        <path d='M80 280 q60 -100 120 -20 q50 60 130 -30 q80 -90 170 10'/>
      </g>
    </svg>`;

  return "data:image/svg+xml;utf8," + encodeURIComponent(svg);
}

export function startMinigame(opts = {}) {
  const { onClose, pauseGameTimer, resumeGameTimer } = opts;

  // Números que deben ir viendo (4 rondas) -> 4 7 3 2
  const numbers = ["4", "7", "3", "2"];
  const totalRounds = numbers.length;

  // Para que cada número tenga "otra combinación" de clics izquierda/derecha
  // valores de enfoque objetivo (clics desde 0): negativos = izquierda, positivos = derecha
  const focusTargets = [-3, 4, -1, 2];

  if (typeof pauseGameTimer === "function") pauseGameTimer();

  // === OVERLAY PRINCIPAL ===
  const overlay = document.createElement("div");
  overlay.setAttribute("role", "dialog");
  overlay.setAttribute("aria-modal", "true");
  Object.assign(overlay.style, {
    position: "fixed",
    inset: "0",
    zIndex: "2600",
    background: "rgba(3, 6, 14, 0.92)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    padding: "16px",
    boxSizing: "border-box",
  });

  const panel = document.createElement("div");
  Object.assign(panel.style, {
    width: "min(420px, 92vw)",
    maxWidth: "480px",
    minHeight: "min(540px, 92vh)",
    background:
      "linear-gradient(180deg, rgba(15,23,42,0.96), rgba(6,11,25,0.96))",
    borderRadius: "22px",
    boxShadow: "0 20px 46px rgba(0,0,0,0.55)",
    border: "1px solid rgba(148,163,184,0.4)",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    padding: "22px 20px",
    color: "#f8fafc",
    position: "relative",
    overflow: "hidden",
  });

  // === CABECERA ===
  const header = document.createElement("div");
  Object.assign(header.style, {
    textAlign: "center",
    marginBottom: "8px",
  });

  const title = document.createElement("h2");
  title.textContent = "Microscopio";
  Object.assign(title.style, {
    margin: "0",
    fontSize: "1.35rem",
    fontWeight: "800",
    letterSpacing: "0.04em",
  });

  const subtitle = document.createElement("p");
  subtitle.textContent = "Usa las flechas para enfocar la muestra";
  Object.assign(subtitle.style, {
    margin: "4px 0 0 0",
    fontSize: "0.95rem",
    color: "rgba(226,232,240,0.8)",
  });

  header.appendChild(title);
  header.appendChild(subtitle);

  // === ZONA CENTRAL: BOTÓN IZQUIERDA + CÍRCULO + BOTÓN DERECHA ===
  const centerRow = document.createElement("div");
  Object.assign(centerRow.style, {
    marginTop: "18px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    gap: "14px",
  });

  const btnLeft = document.createElement("button");
  btnLeft.textContent = "⟲";
  Object.assign(btnLeft.style, {
    width: "52px",
    height: "52px",
    borderRadius: "999px",
    border: "1px solid rgba(148,163,184,0.6)",
    background: "radial-gradient(circle at 30% 30%, #1f2937, #020617)",
    color: "#e5edff",
    fontWeight: "800",
    fontSize: "1.4rem",
    cursor: "pointer",
    boxShadow: "0 10px 26px rgba(0,0,0,0.5)",
  });

  const btnRight = document.createElement("button");
  btnRight.textContent = "⟳";
  Object.assign(btnRight.style, {
    width: "52px",
    height: "52px",
    borderRadius: "999px",
    border: "1px solid rgba(148,163,184,0.6)",
    background: "radial-gradient(circle at 70% 30%, #1f2937, #020617)",
    color: "#e5edff",
    fontWeight: "800",
    fontSize: "1.4rem",
    cursor: "pointer",
    boxShadow: "0 10px 26px rgba(0,0,0,0.5)",
  });

  const viewport = document.createElement("div");
  Object.assign(viewport.style, {
    width: "min(260px, 70vw)",
    height: "min(260px, 70vw)",
    borderRadius: "50%",
    background:
      "radial-gradient(circle at 35% 30%, rgba(65,114,255,0.25), rgba(19,40,86,0.9))",
    border: "4px solid rgba(148,163,184,0.3)",
    boxShadow:
      "inset 0 12px 30px rgba(0,0,0,0.65), 0 12px 30px rgba(8,12,28,0.8)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    position: "relative",
    overflow: "hidden",
    transition: "transform 0.18s ease-out",
  });

  const sample = document.createElement("div");
  Object.assign(sample.style, {
    width: "100%",
    height: "100%",
    backgroundSize: "cover",
    backgroundPosition: "center",
    filter: "blur(30px)",
    transition: "filter 0.12s ease-out",
  });

  viewport.appendChild(sample);

  centerRow.appendChild(btnLeft);
  centerRow.appendChild(viewport);
  centerRow.appendChild(btnRight);

  // === INSTRUCCIONES Y BOTONES ===
  const instructions = document.createElement("p");
  Object.assign(instructions.style, {
    fontSize: "0.88rem",
    color: "rgba(226,232,240,0.74)",
    textAlign: "center",
    margin: "16px 0 0",
  });

  const buttonBar = document.createElement("div");
  Object.assign(buttonBar.style, {
    width: "100%",
    display: "flex",
    justifyContent: "center",
    marginTop: "18px",
    gap: "12px",
  });

  const nextBtn = document.createElement("button");
  nextBtn.type = "button";
  nextBtn.textContent = "Siguiente";
  nextBtn.disabled = true;
  Object.assign(nextBtn.style, {
    padding: "10px 20px",
    borderRadius: "12px",
    border: "none",
    background: "linear-gradient(180deg, #22c55e, #15803d)",
    color: "#fff",
    fontWeight: "700",
    letterSpacing: "0.08em",
    cursor: "pointer",
    fontSize: "0.95rem",
    boxShadow: "0 12px 24px rgba(34,197,94,0.32)",
    opacity: "0.5",
    transition: "opacity 0.2s ease",
    textTransform: "uppercase",
  });

  const exitBtn = document.createElement("button");
  exitBtn.type = "button";
  exitBtn.textContent = "Salir";
  Object.assign(exitBtn.style, {
    padding: "10px 20px",
    borderRadius: "12px",
    border: "none",
    background: "linear-gradient(180deg, #ef4444, #b91c1c)",
    color: "#fff",
    fontWeight: "700",
    letterSpacing: "0.08em",
    cursor: "pointer",
    fontSize: "0.95rem",
    boxShadow: "0 12px 24px rgba(239,68,68,0.35)",
    textTransform: "uppercase",
  });

  buttonBar.appendChild(nextBtn);
  buttonBar.appendChild(exitBtn);

  // Montar panel
  panel.appendChild(header);
  panel.appendChild(centerRow);
  panel.appendChild(instructions);
  panel.appendChild(buttonBar);
  overlay.appendChild(panel);
  document.body.appendChild(overlay);

  // === LÓGICA DEL JUEGO ===

  let currentRound = 0;
  let focusValue = 0;      // empieza en 0, se mueve con las flechas
  let successShown = false;
  let spinAngle = 0;

  const maxBlur = 30;
  const minBlur = 1.4;
  const maxOffset = 6;     // distancia máxima que consideramos para desenfoque

  function setDefaultInstruction() {
    instructions.textContent = `Usa las flechas para enfocar la muestra (${currentRound + 1}/${totalRounds}).`;
  }

  function refreshSample() {
    sample.style.backgroundImage = `url("${buildSampleSvg(numbers[currentRound])}")`;
  }

  function updateNextButtonState() {
    nextBtn.disabled = !successShown;
    nextBtn.style.opacity = successShown ? "1" : "0.5";
    nextBtn.textContent = currentRound === totalRounds - 1 ? "Terminar" : "Siguiente";
  }

  function setupRound(round) {
    currentRound = round;
    focusValue = 0;
    successShown = false;
    spinAngle = 0;
    viewport.style.transform = "rotate(0deg)";
    refreshSample();
    updateBlur();
    setDefaultInstruction();
    updateNextButtonState();
  }

  function revealNumber() {
    successShown = true;
    instructions.textContent = `¡Enfoque conseguido! El número es ${numbers[currentRound]}.`;
    updateNextButtonState();
  }

  function hideNumber() {
    successShown = false;
    setDefaultInstruction();
    updateNextButtonState();
  }

  function updateBlur() {
    const target = focusTargets[currentRound];
    const offset = focusValue - target;
    const distance = Math.min(maxOffset, Math.abs(offset));

    const t = distance / maxOffset; // 0..1
    const blur = minBlur + t * (maxBlur - minBlur);
    sample.style.filter = `blur(${blur.toFixed(2)}px)`;

    const inFocus = distance === 0;

    if (inFocus && !successShown) {
      revealNumber();
    } else if (!inFocus && successShown) {
      hideNumber();
    }
  }

  function spin(direction) {
    // pequeño giro para dar sensación de rotación
    spinAngle += direction * 18;
    viewport.style.transform = `rotate(${spinAngle}deg)`;
  }

  function onLeftClick() {
    focusValue -= 1;
    spin(-1);
    updateBlur();
  }

  function onRightClick() {
    focusValue += 1;
    spin(1);
    updateBlur();
  }

  btnLeft.addEventListener("click", onLeftClick);
  btnRight.addEventListener("click", onRightClick);

  function onNextClick() {
    if (nextBtn.disabled) return;
    if (currentRound >= totalRounds - 1) {
      closeOverlay(true);
      return;
    }
    setupRound(currentRound + 1);
  }

  function onExitClick() {
    closeOverlay(false);
  }

  function onKeyDown(ev) {
    if (ev.key === "Escape") {
      ev.preventDefault();
      closeOverlay(false);
    } else if (ev.key === "ArrowLeft") {
      onLeftClick();
    } else if (ev.key === "ArrowRight") {
      onRightClick();
    }
  }

  nextBtn.addEventListener("click", onNextClick);
  exitBtn.addEventListener("click", onExitClick);
  document.addEventListener("keydown", onKeyDown);

  function cleanup() {
    btnLeft.removeEventListener("click", onLeftClick);
    btnRight.removeEventListener("click", onRightClick);
    nextBtn.removeEventListener("click", onNextClick);
    exitBtn.removeEventListener("click", onExitClick);
    document.removeEventListener("keydown", onKeyDown);
  }

  function closeOverlay(success) {
    cleanup();
    overlay.remove();
    if (typeof resumeGameTimer === "function") resumeGameTimer();
    if (typeof onClose === "function") onClose(!!success);
  }

  // Iniciar primera ronda
  setupRound(0);
}

// Para poder probarlo desde la consola del navegador si quieres
if (typeof window !== "undefined") {
  window.startMicroscopioMinigame = startMinigame;
}
