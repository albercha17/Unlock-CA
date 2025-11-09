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

  // Números que deben ir viendo (4 rondas)
  const numbers = ["15", "12", "17", "12"];
  const totalRounds = numbers.length;

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
  subtitle.textContent = "Gira la rosca para enfocar la muestra";
  Object.assign(subtitle.style, {
    margin: "4px 0 0 0",
    fontSize: "0.95rem",
    color: "rgba(226,232,240,0.8)",
  });

  header.appendChild(title);
  header.appendChild(subtitle);

  // === VISOR CIRCULAR ===
  const viewport = document.createElement("div");
  Object.assign(viewport.style, {
    width: "min(280px, 70vw)",
    height: "min(280px, 70vw)",
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
    marginTop: "4px",
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

  // Badgito con el progreso (muestra los números ya enfocados)
  const resultBadge = document.createElement("div");
  Object.assign(resultBadge.style, {
    position: "absolute",
    bottom: "16px",
    left: "50%",
    transform: "translateX(-50%)",
    padding: "8px 18px",
    borderRadius: "999px",
    background: "rgba(21,128,61,0.12)",
    color: "#bbf7d0",
    fontSize: "0.9rem",
    fontWeight: "700",
    letterSpacing: "0.12em",
    opacity: "0",
    transition: "opacity 0.25s ease, transform 0.25s ease",
    border: "1px solid rgba(34,197,94,0.45)",
    backdropFilter: "blur(8px)",
    pointerEvents: "none",
    textTransform: "uppercase",
  });

  viewport.appendChild(resultBadge);

  // === KNOB / ROSCA ===
  const knobArea = document.createElement("div");
  Object.assign(knobArea.style, {
    marginTop: "18px",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: "12px",
  });

  const knobLabel = document.createElement("span");
  knobLabel.textContent = "Enfoque";
  Object.assign(knobLabel.style, {
    fontSize: "0.8rem",
    letterSpacing: "0.16em",
    textTransform: "uppercase",
    color: "rgba(226,232,240,0.7)",
  });

  const knob = document.createElement("div");
  Object.assign(knob.style, {
    width: "164px",
    height: "164px",
    borderRadius: "50%",
    background:
      "radial-gradient(circle at 32% 30%, rgba(51,65,85,0.9), rgba(15,23,42,1) 60%, rgba(2,6,23,1) 100%)",
    border: "4px solid rgba(30,41,59,0.55)",
    boxShadow:
      "0 28px 48px rgba(2,6,23,0.65), inset 0 22px 38px rgba(2,6,23,0.5)",
    position: "relative",
    touchAction: "none",
    overflow: "hidden",
  });

  const knobRidges = document.createElement("div");
  Object.assign(knobRidges.style, {
    position: "absolute",
    inset: "0",
    borderRadius: "50%",
    background:
      "repeating-conic-gradient(from 90deg, rgba(148,163,184,0.16) 0deg, rgba(148,163,184,0.16) 6deg, rgba(15,23,42,0.92) 6deg, rgba(15,23,42,0.92) 12deg)",
    mixBlendMode: "screen",
    opacity: "0.55",
    pointerEvents: "none",
  });

  const knobRim = document.createElement("div");
  Object.assign(knobRim.style, {
    position: "absolute",
    inset: "10px",
    borderRadius: "50%",
    background:
      "radial-gradient(circle, rgba(30,41,59,0.85) 0%, rgba(15,23,42,1) 70%, rgba(15,23,42,1) 100%)",
    border: "1px solid rgba(71,85,105,0.45)",
    boxShadow: "inset 0 16px 28px rgba(8,15,35,0.85), inset 0 -18px 28px rgba(148,163,184,0.12)",
    pointerEvents: "none",
  });

  const knobCore = document.createElement("div");
  Object.assign(knobCore.style, {
    position: "absolute",
    inset: "36px",
    borderRadius: "50%",
    background:
      "radial-gradient(circle at 40% 35%, rgba(148,163,184,0.15), rgba(15,23,42,0.95) 68%, rgba(2,6,23,1) 100%)",
    border: "1px solid rgba(100,116,139,0.35)",
    boxShadow: "inset 0 10px 22px rgba(5,13,32,0.92)",
    pointerEvents: "none",
  });

  const knobDial = document.createElement("div");
  Object.assign(knobDial.style, {
    position: "absolute",
    width: "14px",
    height: "72px",
    background: "linear-gradient(180deg, #f8fafc, #94a3b8 55%, #1f2937)",
    top: "-6px",
    left: "50%",
    transformOrigin: "50% 86px",
    borderRadius: "999px",
    transform: "translateX(-50%) rotate(-140deg)",
    boxShadow: "0 10px 20px rgba(15,23,42,0.45)",
    pointerEvents: "none",
  });

  const knobIndicator = document.createElement("div");
  Object.assign(knobIndicator.style, {
    position: "absolute",
    top: "14px",
    left: "50%",
    width: "24px",
    height: "24px",
    transform: "translateX(-50%)",
    borderRadius: "50%",
    background:
      "radial-gradient(circle, rgba(248,250,252,0.95) 0%, rgba(148,163,184,0.8) 55%, rgba(30,41,59,0.95) 100%)",
    boxShadow: "0 6px 14px rgba(15,23,42,0.55)",
    pointerEvents: "none",
  });

  knob.appendChild(knobRidges);
  knob.appendChild(knobRim);
  knob.appendChild(knobCore);
  knob.appendChild(knobDial);
  knob.appendChild(knobIndicator);

  knobArea.appendChild(knobLabel);
  knobArea.appendChild(knob);

  // === INSTRUCCIONES Y BOTONES ===
  const instructions = document.createElement("p");
  Object.assign(instructions.style, {
    fontSize: "0.88rem",
    color: "rgba(226,232,240,0.74)",
    textAlign: "center",
    margin: "10px 0 0",
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
  panel.appendChild(viewport);
  panel.appendChild(knobArea);
  panel.appendChild(instructions);
  panel.appendChild(buttonBar);
  overlay.appendChild(panel);
  document.body.appendChild(overlay);

  // === LÓGICA DEL JUEGO ===

  let knobValue = 0;           // 0 .. 100
  let dragging = false;
  let currentRound = 0;
  let successShown = false;

  const maxBlur = 30;
  const minBlur = 1.2;
  const revealThreshold = 0.9; // cuánto hay que girar para "enfocar"

  function setDefaultInstruction() {
    instructions.textContent = `Gira la rosca para enfocar la muestra (${currentRound + 1}/${totalRounds}).`;
  }

  function refreshSample() {
    sample.style.backgroundImage = `url("${buildSampleSvg(numbers[currentRound])}")`;
  }

  function updateProgressBadge() {
    const done = numbers.slice(0, currentRound + (successShown ? 1 : 0));
    if (done.length === 0) {
      resultBadge.style.opacity = "0";
      resultBadge.style.transform = "translateX(-50%)";
      resultBadge.textContent = "";
      return;
    }
    resultBadge.textContent = done.join(" • ");
    resultBadge.style.opacity = "1";
    resultBadge.style.transform = "translateX(-50%) translateY(-6px)";
  }

  function updateNextButtonState() {
    nextBtn.disabled = !successShown;
    nextBtn.style.opacity = successShown ? "1" : "0.5";
    nextBtn.textContent = currentRound === totalRounds - 1 ? "Terminar" : "Siguiente";
  }

  function setupRound(round) {
    currentRound = round;
    successShown = false;
    knobValue = 0;
    updateBlur();
    refreshSample();
    setDefaultInstruction();
    updateProgressBadge();
    updateNextButtonState();
  }

  function revealNumber() {
    successShown = true;
    instructions.textContent = `¡Enfoque conseguido! El número es ${numbers[currentRound]}.`;
    updateProgressBadge();
    updateNextButtonState();
  }

  function hideNumber() {
    successShown = false;
    setDefaultInstruction();
    updateProgressBadge();
    updateNextButtonState();
  }

  function updateBlur() {
    const t = knobValue / 100; // 0..1
    const blur = maxBlur - (maxBlur - minBlur) * t;
    sample.style.filter = `blur(${blur.toFixed(2)}px)`;
    knobDial.style.transform = `translateX(-50%) rotate(${lerp(-140, 140, t)}deg)`;

    if (t >= revealThreshold && !successShown) {
      revealNumber();
    } else if (t < revealThreshold * 0.95 && successShown) {
      hideNumber();
    }
  }

  function lerp(a, b, t) {
    return a + (b - a) * t;
  }

  function setValueFromAngle(angleDeg) {
    // Limitamos el giro a un arco de -140º a 140º
    const clamped = Math.max(-140, Math.min(140, angleDeg));
    const normalized = (clamped + 140) / 280; // 0..1
    knobValue = Math.max(0, Math.min(100, normalized * 100));
    updateBlur();
  }

  function computeAngle(clientX, clientY) {
    const rect = knob.getBoundingClientRect();
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;
    const dx = clientX - cx;
    const dy = clientY - cy;
    return (Math.atan2(dy, dx) * 180) / Math.PI;
  }

  function onPointerDown(ev) {
    dragging = true;
    knob.setPointerCapture(ev.pointerId);
    const angle = computeAngle(ev.clientX, ev.clientY);
    setValueFromAngle(angle);
    ev.preventDefault();
  }

  function onPointerMove(ev) {
    if (!dragging) return;
    const angle = computeAngle(ev.clientX, ev.clientY);
    setValueFromAngle(angle);
    ev.preventDefault();
  }

  function onPointerUp(ev) {
    if (!dragging) return;
    dragging = false;
    knob.releasePointerCapture(ev.pointerId);
    ev.preventDefault();
  }

  knob.addEventListener("pointerdown", onPointerDown);
  knob.addEventListener("pointermove", onPointerMove);
  knob.addEventListener("pointerup", onPointerUp);
  knob.addEventListener("pointercancel", onPointerUp);

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
    }
  }

  nextBtn.addEventListener("click", onNextClick);
  exitBtn.addEventListener("click", onExitClick);
  document.addEventListener("keydown", onKeyDown);

  function cleanup() {
    knob.removeEventListener("pointerdown", onPointerDown);
    knob.removeEventListener("pointermove", onPointerMove);
    knob.removeEventListener("pointerup", onPointerUp);
    knob.removeEventListener("pointercancel", onPointerUp);
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
