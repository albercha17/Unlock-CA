export function startMinigame(opts = {}) {
  const { onClose, pauseGameTimer, resumeGameTimer } = opts;

  const numbers = ["15", "12", "17", "12"];
  const totalRounds = numbers.length;

  if (typeof pauseGameTimer === "function") pauseGameTimer();

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
    padding: "max(14px, env(safe-area-inset-top, 14px)) max(14px, env(safe-area-inset-right, 14px)) max(14px, env(safe-area-inset-bottom, 14px)) max(14px, env(safe-area-inset-left, 14px))",
    boxSizing: "border-box",
    touchAction: "none",
  });

  const panel = document.createElement("div");
  Object.assign(panel.style, {
    width: "min(420px, 92vw)",
    maxWidth: "480px",
    minHeight: "min(560px, 92vh)",
    background: "linear-gradient(180deg, rgba(15,23,42,0.95), rgba(6,11,25,0.95))",
    borderRadius: "22px",
    boxShadow: "0 20px 46px rgba(0,0,0,0.55)",
    border: "1px solid rgba(255,255,255,0.08)",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "22px 20px",
    color: "#f8fafc",
    position: "relative",
    overflow: "hidden",
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
  subtitle.textContent = "Gira la rueda para enfocar la muestra";
  subtitle.textContent = "Gira la rosca del telescopio para enfocar la muestra";
  Object.assign(subtitle.style, {
    margin: "6px 0 0 0",
    fontSize: "0.95rem",
    color: "rgba(226,232,240,0.8)",
  });

  const header = document.createElement("div");
  Object.assign(header.style, {
    textAlign: "center",
    marginBottom: "6px",
  });
  header.appendChild(title);
  header.appendChild(subtitle);

  const viewport = document.createElement("div");
  Object.assign(viewport.style, {
    width: "min(280px, 70vw)",
    height: "min(280px, 70vw)",
    borderRadius: "50%",
    background: "radial-gradient(circle at 35% 30%, rgba(65,114,255,0.25), rgba(19,40,86,0.9))",
    border: "4px solid rgba(148,163,184,0.28)",
    boxShadow: "inset 0 12px 30px rgba(0,0,0,0.65), 0 12px 30px rgba(8,12,28,0.8)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    position: "relative",
    overflow: "hidden",
  });

  const sample = document.createElement("div");
  const sampleSvg =
  const buildSampleSvg = (digit) =>
    "data:image/svg+xml;utf8," +
    encodeURIComponent(
      `<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 600 600'>` +
        `<defs>` +
        `<radialGradient id='g' cx='48%' cy='44%' r='60%'>` +
        `<stop offset='0%' stop-color='#2dd4bf' stop-opacity='0.35'/>` +
        `<stop offset='50%' stop-color='#1e3a8a' stop-opacity='0.65'/>` +
        `<stop offset='100%' stop-color='#020617' stop-opacity='0.85'/>` +
        `</radialGradient>` +
        `</defs>` +
        `<rect width='600' height='600' fill='url(#g)'/>` +
        `<g font-family="'Poppins', sans-serif" font-size='220' font-weight='800' fill='#fef9c3' opacity='0.92'>` +
        `<text x='50%' y='54%' text-anchor='middle'>742</text>` +
        `<text x='50%' y='55%' text-anchor='middle' dominant-baseline='middle'>${digit}</text>` +
        `</g>` +
        `<g stroke='#22d3ee' stroke-width='4' opacity='0.45'>` +
        `<circle cx='170' cy='170' r='38' fill='none'/>` +
        `<circle cx='440' cy='340' r='24' fill='none'/>` +
        `<path d='M80 280 q60 -100 120 -20 q50 60 130 -30 q80 -90 170 10' fill='none'/>` +
        `</g>` +
      `</svg>`
    );

  Object.assign(sample.style, {
    width: "100%",
    height: "100%",
    backgroundImage: `url("${sampleSvg}")`,
    backgroundImage: "",
    backgroundSize: "cover",
    backgroundPosition: "center",
    filter: "blur(18px)",
    transition: "filter 0.18s ease-out",
    filter: "blur(42px)",
    transition: "filter 0.14s ease-out",
  });

  viewport.appendChild(sample);

  const resultBadge = document.createElement("div");
  resultBadge.textContent = "742";
  resultBadge.textContent = "";
  Object.assign(resultBadge.style, {
    position: "absolute",
    bottom: "18px",
    left: "50%",
    transform: "translateX(-50%)",
    padding: "10px 22px",
    borderRadius: "999px",
    background: "rgba(15,185,129,0.18)",
    color: "#bbf7d0",
    fontSize: "1.15rem",
    fontWeight: "800",
    letterSpacing: "0.08em",
    opacity: "0",
    transition: "opacity 0.3s ease, transform 0.3s ease",
    pointerEvents: "none",
    border: "1px solid rgba(34,197,94,0.45)",
    backdropFilter: "blur(8px)",
  });

  const knobArea = document.createElement("div");
  Object.assign(knobArea.style, {
    marginTop: "18px",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    gap: "18px",
  });

  const knobLabel = document.createElement("span");
  knobLabel.textContent = "Enfoque";
  Object.assign(knobLabel.style, {
    fontSize: "0.9rem",
    letterSpacing: "0.12em",
    textTransform: "uppercase",
    color: "rgba(226,232,240,0.7)",
  });

  const knob = document.createElement("div");
  Object.assign(knob.style, {
    width: "150px",
    height: "150px",
    borderRadius: "50%",
    background: "radial-gradient(circle at 30% 30%, rgba(148,163,184,0.22), rgba(15,23,42,0.95))",
    border: "2px solid rgba(255,255,255,0.08)",
    boxShadow: "0 16px 30px rgba(2,6,23,0.65), inset 0 12px 22px rgba(148,163,184,0.18)",
    background: "radial-gradient(circle at 30% 30%, rgba(51,65,85,0.7), rgba(15,23,42,0.95))",
    border: "2px solid rgba(148,163,184,0.35)",
    boxShadow: "0 20px 34px rgba(2,6,23,0.65), inset 0 18px 32px rgba(10,20,46,0.55)",
    position: "relative",
    touchAction: "none",
    overflow: "hidden",
  });

  const knobIndicator = document.createElement("div");
  Object.assign(knobIndicator.style, {
  const knobDial = document.createElement("div");
  Object.assign(knobDial.style, {
    position: "absolute",
    width: "12px",
    height: "48px",
    background: "linear-gradient(180deg, #38bdf8, #0ea5e9)",
    top: "10px",
    left: "50%",
    transformOrigin: "50% 65px",
    borderRadius: "8px",
    transform: "translateX(-50%) rotate(-135deg)",
    boxShadow: "0 6px 16px rgba(14,165,233,0.45)",
    inset: "6px",
    borderRadius: "50%",
    background:
      "radial-gradient(circle at 50% 50%, rgba(15,23,42,0.65) 0%, rgba(10,12,32,0.85) 62%, rgba(2,6,23,0.95) 100%)," +
      "repeating-conic-gradient(from 0deg, rgba(59,130,246,0.35) 0deg 10deg, rgba(12,74,110,0.85) 10deg 22deg)",
    boxShadow: "inset 0 22px 32px rgba(2,6,23,0.85), inset 0 -12px 18px rgba(14,116,144,0.22)",
    transition: "transform 0.08s ease-out",
    pointerEvents: "none",
  });

  const knobGrip = document.createElement("div");
  Object.assign(knobGrip.style, {
    position: "absolute",
    inset: "26px",
    borderRadius: "50%",
    background:
      "radial-gradient(circle at 50% 45%, rgba(191,219,254,0.14) 0%, rgba(30,41,59,0.88) 70%, rgba(8,15,35,0.95) 100%)",
    border: "1px solid rgba(148,163,184,0.4)",
    boxShadow: "inset 0 8px 16px rgba(2,6,23,0.85)",
    pointerEvents: "none",
  });

  const knobCenter = document.createElement("div");
  Object.assign(knobCenter.style, {
  const knobCore = document.createElement("div");
  Object.assign(knobCore.style, {
    position: "absolute",
    inset: "28px",
    inset: "44px",
    borderRadius: "50%",
    background: "radial-gradient(circle, rgba(15,23,42,1) 0%, rgba(30,41,59,0.85) 70%, rgba(15,23,42,0.95) 100%)",
    border: "1px solid rgba(148,163,184,0.3)",
    boxShadow: "inset 0 8px 20px rgba(2,6,23,0.8)",
    background: "radial-gradient(circle, rgba(15,23,42,0.95) 0%, rgba(2,6,23,1) 90%)",
    border: "1px solid rgba(148,163,184,0.25)",
    boxShadow: "inset 0 10px 20px rgba(8,16,40,0.85)",
    pointerEvents: "none",
  });

  knob.appendChild(knobCenter);
  knob.appendChild(knobIndicator);
  knob.appendChild(knobDial);
  knob.appendChild(knobGrip);
  knob.appendChild(knobCore);

  knobArea.appendChild(knobLabel);
  knobArea.appendChild(knob);

  const instructions = document.createElement("p");
  instructions.textContent = "Cuando esté nítido, recuerda el número.";
  instructions.textContent = "Gira la rosca para enfocar la muestra (1/" + totalRounds + ").";
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
    padding: "12px 26px",
    borderRadius: "12px",
    border: "none",
    background: "linear-gradient(180deg, #22c55e, #15803d)",
    color: "#fff",
    fontWeight: "700",
    letterSpacing: "0.08em",
    cursor: "pointer",
    fontSize: "1rem",
    boxShadow: "0 12px 24px rgba(34,197,94,0.32)",
    opacity: "0.5",
    transition: "opacity 0.2s ease", 
    WebkitTapHighlightColor: "transparent",
  });

  const exitBtn = document.createElement("button");
  exitBtn.type = "button";
  exitBtn.textContent = "Salir";
  Object.assign(exitBtn.style, {
    padding: "12px 32px",
    borderRadius: "12px",
    border: "none",
    background: "linear-gradient(180deg, #ef4444, #b91c1c)",
    color: "#fff",
    fontWeight: "700",
    letterSpacing: "0.08em",
    cursor: "pointer",
    fontSize: "1rem",
    boxShadow: "0 12px 24px rgba(239,68,68,0.35)",
    WebkitTapHighlightColor: "transparent",
 });

  buttonBar.appendChild(nextBtn);
  buttonBar.appendChild(exitBtn);

  panel.appendChild(header);
  panel.appendChild(viewport);
  panel.appendChild(resultBadge);
  panel.appendChild(knobArea);
  panel.appendChild(instructions);
  panel.appendChild(buttonBar);

  overlay.appendChild(panel);
  document.body.appendChild(overlay);

  let knobValue = 0; // 0 -> 100
  let targetKnobValue = 0;
  let animationFrameId = null;
  let dragging = false;
  let successShown = false;
  let currentRound = 0;

  const maxBlur = 42;
  const minBlur = 0.35;
  const knobResistance = 0.075;
  const revealThreshold = 0.995;
  const hideThreshold = 0.985;

  function updateProgressBadge() {
    const progressIndex = currentRound + (successShown ? 1 : 0);
    const found = numbers.slice(0, progressIndex).join(" • ");
    const remaining = numbers.slice(progressIndex).map(() => "◦").join(" • ");
    resultBadge.textContent = [found, remaining].filter(Boolean).join(" • ");
    const shouldShow = currentRound > 0 || successShown;
    resultBadge.style.opacity = shouldShow ? "1" : "0";
    resultBadge.style.transform = shouldShow
      ? "translateX(-50%) translateY(-6px)"
      : "translateX(-50%)";
  }

  const maxBlur = 18;
  const minBlur = 1.2;
  function setDefaultInstruction() {
    instructions.textContent = `Gira la rosca para enfocar la muestra (${currentRound + 1}/${totalRounds}).`;
  }

  function refreshSample() {
    sample.style.backgroundImage = `url("${buildSampleSvg(numbers[currentRound])}")`;
  }

  function updateNextButtonState() {
    if (successShown) {
      nextBtn.disabled = false;
      nextBtn.style.opacity = "1";
      nextBtn.textContent = currentRound === totalRounds - 1 ? "Terminar" : "Siguiente";
    } else {
      nextBtn.disabled = true;
      nextBtn.style.opacity = "0.5";
      nextBtn.textContent = currentRound === totalRounds - 1 ? "Terminar" : "Siguiente";
    }
  }

  function setupRound(round) {
    currentRound = round;
    successShown = false;
    setDefaultInstruction();
    refreshSample();
    updateProgressBadge();
    updateNextButtonState();
    knobValue = 0;
    targetKnobValue = 0;
    updateBlur();
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
    const t = knobValue / 100;
    const blur = maxBlur - (maxBlur - minBlur) * t;
    const denominator = Math.max(0.0001, revealThreshold - hideThreshold);
    const focusBlend = Math.max(0, Math.min(1, (t - hideThreshold) / denominator));
    const eased = Math.pow(focusBlend, 8);
    const blur = t >= revealThreshold
      ? minBlur
      : maxBlur - (maxBlur - minBlur) * eased;
    sample.style.filter = `blur(${blur.toFixed(2)}px)`;
    knobIndicator.style.transform = `translateX(-50%) rotate(${lerp(-135, 135, t)}deg)`;

    if (t >= 0.94 && !successShown) {
      successShown = true;
      resultBadge.style.opacity = "1";
      resultBadge.style.transform = "translateX(-50%) translateY(-6px)";
      instructions.textContent = "¡Enfoque conseguido! El número es 742.";
    } else if (t < 0.9 && successShown) {
      successShown = false;
      resultBadge.style.opacity = "0";
      resultBadge.style.transform = "translateX(-50%)";
      instructions.textContent = "Cuando esté nítido, recuerda el número.";
    knobDial.style.transform = `rotate(${lerp(-150, 150, t)}deg)`;

    if (t >= revealThreshold && !successShown) {
      revealNumber();
    } else if (t < hideThreshold && successShown) {
      hideNumber();
    }
  }

  function lerp(a, b, t) {
    return a + (b - a) * t;
  }

  function setValueFromAngle(angleDeg) {
    const clamped = Math.max(-140, Math.min(140, angleDeg));
    const normalized = (clamped + 140) / 280;
    knobValue = Math.max(0, Math.min(100, normalized * 100));
    targetKnobValue = Math.max(0, Math.min(100, normalized * 100));
    ensureKnobAnimation();
  }

  function ensureKnobAnimation() {
    if (animationFrameId !== null) return;
    animationFrameId = requestAnimationFrame(stepKnobTowardsTarget);
  }

  function stepKnobTowardsTarget() {
    const delta = targetKnobValue - knobValue;
    if (Math.abs(delta) < 0.05) {
      knobValue = targetKnobValue;
      updateBlur();
      animationFrameId = null;
      return;
    }

    knobValue = Math.max(0, Math.min(100, knobValue + delta * knobResistance));
    updateBlur();
    animationFrameId = requestAnimationFrame(stepKnobTowardsTarget);
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

  exitBtn.addEventListener("click", cerrar);
  nextBtn.addEventListener("click", onNextClick);

  function onNextClick() {
    if (nextBtn.disabled) return;
    if (currentRound >= totalRounds - 1) {
      cerrar();
      return;
    }
    setupRound(currentRound + 1);
  }

  function cerrar() {
    cleanup();
    overlay.remove();
    if (typeof resumeGameTimer === "function") resumeGameTimer();
    if (typeof onClose === "function") onClose();
  }

  function cleanup() {
    knob.removeEventListener("pointerdown", onPointerDown);
    knob.removeEventListener("pointermove", onPointerMove);
    knob.removeEventListener("pointerup", onPointerUp);
    knob.removeEventListener("pointercancel", onPointerUp);
    exitBtn.removeEventListener("click", cerrar);
    nextBtn.removeEventListener("click", onNextClick);
    document.removeEventListener("keydown", onKeyDown);
    if (animationFrameId !== null) {
      cancelAnimationFrame(animationFrameId);
      animationFrameId = null;
    }
  }

  function onKeyDown(ev) {
    if (ev.key === "Escape") {
      ev.preventDefault();
      cerrar();
    }
  }

  document.addEventListener("keydown", onKeyDown);

  // iniciar con un ligero desenfoque
  knobValue = 0;
  updateBlur();
  setupRound(0);
}
