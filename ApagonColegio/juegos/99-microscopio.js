export function startMinigame(opts = {}) {
  const { onClose, pauseGameTimer, resumeGameTimer } = opts;

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
    backgroundSize: "cover",
    backgroundPosition: "center",
    filter: "blur(18px)",
    transition: "filter 0.18s ease-out",
  });

  viewport.appendChild(sample);

  const resultBadge = document.createElement("div");
  resultBadge.textContent = "742";
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
    position: "relative",
    touchAction: "none",
  });

  const knobIndicator = document.createElement("div");
  Object.assign(knobIndicator.style, {
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
  });

  const knobCenter = document.createElement("div");
  Object.assign(knobCenter.style, {
    position: "absolute",
    inset: "28px",
    borderRadius: "50%",
    background: "radial-gradient(circle, rgba(15,23,42,1) 0%, rgba(30,41,59,0.85) 70%, rgba(15,23,42,0.95) 100%)",
    border: "1px solid rgba(148,163,184,0.3)",
    boxShadow: "inset 0 8px 20px rgba(2,6,23,0.8)",
  });

  knob.appendChild(knobCenter);
  knob.appendChild(knobIndicator);

  knobArea.appendChild(knobLabel);
  knobArea.appendChild(knob);

  const instructions = document.createElement("p");
  instructions.textContent = "Cuando esté nítido, recuerda el número.";
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
    -webkitTapHighlightColor: "transparent",
  });

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
  let dragging = false;
  let successShown = false;

  const maxBlur = 18;
  const minBlur = 1.2;

  function updateBlur() {
    const t = knobValue / 100;
    const blur = maxBlur - (maxBlur - minBlur) * t;
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
    }
  }

  function lerp(a, b, t) {
    return a + (b - a) * t;
  }

  function setValueFromAngle(angleDeg) {
    const clamped = Math.max(-140, Math.min(140, angleDeg));
    const normalized = (clamped + 140) / 280;
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

  exitBtn.addEventListener("click", cerrar);

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
    document.removeEventListener("keydown", onKeyDown);
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
}
