// ./juegos/XX-candadoProbetas.js
// Minijuego: candado de 4 dígitos (0-9)
//
// Cambia esta combinación por la que tú quieras:
const CORRECT_CODE = "4732";

function makeLockStyles() {
  return `
.lock-root{
  position:fixed; inset:0; z-index:12000;
  display:flex; align-items:center; justify-content:center;
  background:linear-gradient(180deg, rgba(15,23,42,.90), rgba(2,6,23,.96));
  font-family:"Poppins", system-ui, -apple-system, "Segoe UI", Roboto, Arial;
}
.lock-panel{
  width:min(420px, 94vw);
  background:radial-gradient(circle at top, #111827 0%, #020617 55%, #000 100%);
  border-radius:20px;
  padding:20px 18px 18px;
  box-shadow:0 22px 60px rgba(0,0,0,.75);
  color:#e5e7eb;
  border:1px solid rgba(148,163,184,.45);
  position:relative;
  overflow:hidden;
  transition: box-shadow .18s ease, transform .18s ease, border-color .18s ease;
}
.lock-panel::before{
  content:"";
  position:absolute;
  inset:-40%;
  background:radial-gradient(circle at top, rgba(96,165,250,.16), transparent 60%);
  opacity:.75;
  pointer-events:none;
}
.lock-panel-inner{
  position:relative;
  z-index:1;
}
.lock-header{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:10px;
}
.lock-title{
  font-weight:900;
  letter-spacing:.16em;
  text-transform:uppercase;
  font-size:.82rem;
  color:#9ca3af;
}
.lock-led{
  width:10px; height:10px;
  border-radius:999px;
  background:radial-gradient(circle, #22c55e 0%, #166534 50%, #052e16 100%);
  box-shadow:0 0 12px rgba(34,197,94,.75);
}
.lock-body{
  margin-top:10px;
}
.lock-label{
  font-size:.9rem;
  color:#e5e7eb;
  margin-bottom:6px;
}
.lock-dials{
  margin-top:8px;
  display:flex;
  justify-content:center;
  gap:10px;
}
.lock-dial{
  width:64px;
  height:100px;
  background:linear-gradient(180deg,#020617,#020617,#020617);
  border-radius:16px;
  border:1px solid rgba(148,163,184,.4);
  box-shadow:
    inset 0 0 0 1px rgba(15,23,42,1),
    0 16px 30px rgba(0,0,0,.9);
  display:flex;
  flex-direction:column;
  align-items:stretch;
  justify-content:space-between;
  padding:4px 0;
}
.lock-arrow{
  border:none;
  background:transparent;
  color:#9ca3af;
  font-size:16px;
  cursor:pointer;
  display:flex;
  align-items:center;
  justify-content:center;
  padding:4px 0;
  transition: color .15s ease, transform .1s ease;
}
.lock-arrow:active{
  transform:translateY(1px) scale(.96);
}
.lock-arrow span{
  pointer-events:none;
}
.lock-display-wrap{
  flex:1;
  display:flex;
  align-items:center;
  justify-content:center;
}
.lock-display{
  width:44px;
  height:44px;
  border-radius:12px;
  background:radial-gradient(circle at 30% 20%, #111827, #020617 70%);
  border:1px solid rgba(55,65,81,.9);
  box-shadow:
    inset 0 3px 6px rgba(15,23,42,.9),
    0 6px 14px rgba(0,0,0,.9);
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:1.3rem;
  font-weight:800;
  color:#f9fafb;
}

.lock-footer{
  margin-top:14px;
  display:flex;
  justify-content:space-between;
  align-items:center;
  gap:8px;
}
.lock-message{
  font-size:.8rem;
  color:#9ca3af;
}
.lock-actions{
  display:flex;
  gap:8px;
}
.lock-btn{
  border:none;
  border-radius:999px;
  padding:8px 14px;
  font-weight:800;
  font-size:.8rem;
  letter-spacing:.08em;
  text-transform:uppercase;
  cursor:pointer;
}
.lock-btn-primary{
  background:linear-gradient(180deg,#22c55e,#16a34a);
  color:#022c22;
  box-shadow:0 14px 28px rgba(34,197,94,.4);
}
.lock-btn-ghost{
  background:transparent;
  border:1px solid rgba(148,163,184,.5);
  color:#e5e7eb;
}

/* estados de error (rojo + vibración) */
.lock-panel-error{
  border-color:rgba(248,113,113,.9) !important;
  box-shadow:
    0 22px 60px rgba(0,0,0,.9),
    0 0 28px rgba(248,113,113,.6);
  animation: lock-shake .45s ease;
}
.lock-panel-error .lock-display{
  border-color:rgba(248,113,113,.9);
  box-shadow:
    inset 0 3px 6px rgba(127,29,29,.9),
    0 6px 18px rgba(248,113,113,.6);
}
.lock-panel-error .lock-display span{
  color:#fecaca;
}
@keyframes lock-shake{
  0%{ transform:translateX(0) }
  20%{ transform:translateX(-6px) }
  40%{ transform:translateX(6px) }
  60%{ transform:translateX(-4px) }
  80%{ transform:translateX(4px) }
  100%{ transform:translateX(0) }
}

/* pequeño mensaje de estado */
.lock-toast{
  margin-top:8px;
  font-size:.78rem;
  color:#9ca3af;
  min-height:1.2em;
}
.lock-toast-ok{
  color:#bbf7d0;
}
.lock-toast-err{
  color:#fecaca;
}
@media (max-width:400px){
  .lock-dial{
    width:56px;
    height:92px;
  }
}
`;
}

export function startMinigame(opts = {}) {
  const { onClose, pauseGameTimer, resumeGameTimer } = opts;

  if (typeof pauseGameTimer === "function") pauseGameTimer();

  // inyectar estilos una sola vez
  if (!document.getElementById("lock-styles")) {
    const st = document.createElement("style");
    st.id = "lock-styles";
    st.textContent = makeLockStyles();
    document.head.appendChild(st);
  }

  // overlay raíz
  const root = document.createElement("div");
  root.className = "lock-root";
  root.setAttribute("role", "dialog");
  root.setAttribute("aria-modal", "true");

  const panel = document.createElement("div");
  panel.className = "lock-panel";

  const panelInner = document.createElement("div");
  panelInner.className = "lock-panel-inner";

  // header
  const header = document.createElement("div");
  header.className = "lock-header";

  const left = document.createElement("div");
  const title = document.createElement("div");
  title.className = "lock-title";
  title.textContent = "Candado de seguridad";

  const label = document.createElement("div");
  label.className = "lock-label";
  label.textContent = "Gira los rodillos y prueba la combinación.";

  left.appendChild(title);
  left.appendChild(label);

  const led = document.createElement("div");
  led.className = "lock-led";

  header.appendChild(left);
  header.appendChild(led);

  // cuerpo: diales
  const body = document.createElement("div");
  body.className = "lock-body";

  const dialsWrap = document.createElement("div");
  dialsWrap.className = "lock-dials";

  const digits = [0, 0, 0, 0];
  const displaySpans = [];

  function createDial(index) {
    const dial = document.createElement("div");
    dial.className = "lock-dial";

    const up = document.createElement("button");
    up.className = "lock-arrow";
    up.type = "button";
    up.innerHTML = `<span>▲</span>`;

    const mid = document.createElement("div");
    mid.className = "lock-display-wrap";
    const disp = document.createElement("div");
    disp.className = "lock-display";
    const spanVal = document.createElement("span");
    spanVal.textContent = String(digits[index]);
    disp.appendChild(spanVal);
    mid.appendChild(disp);

    const down = document.createElement("button");
    down.className = "lock-arrow";
    down.type = "button";
    down.innerHTML = `<span>▼</span>`;

    up.addEventListener("click", () => {
      digits[index] = (digits[index] + 1) % 10;
      spanVal.textContent = String(digits[index]);
      clearErrorVisual();
    });
    down.addEventListener("click", () => {
      digits[index] = (digits[index] + 9) % 10;
      spanVal.textContent = String(digits[index]);
      clearErrorVisual();
    });

    dial.appendChild(up);
    dial.appendChild(mid);
    dial.appendChild(down);
    dialsWrap.appendChild(dial);
    displaySpans.push(spanVal);
  }

  for (let i = 0; i < 4; i++) {
    createDial(i);
  }

  body.appendChild(dialsWrap);

  // toast info
  const toast = document.createElement("div");
  toast.className = "lock-toast";
  toast.textContent = "";

  // footer
  const footer = document.createElement("div");
  footer.className = "lock-footer";

  const msg = document.createElement("div");
  msg.className = "lock-message";
  msg.textContent = "Introduce el código y pulsa PROBAR.";

  const actions = document.createElement("div");
  actions.className = "lock-actions";

  const btnCancel = document.createElement("button");
  btnCancel.className = "lock-btn lock-btn-ghost";
  btnCancel.type = "button";
  btnCancel.textContent = "Cerrar";

  const btnCheck = document.createElement("button");
  btnCheck.className = "lock-btn lock-btn-primary";
  btnCheck.type = "button";
  btnCheck.textContent = "Probar";

  actions.appendChild(btnCancel);
  actions.appendChild(btnCheck);

  footer.appendChild(msg);
  footer.appendChild(actions);

  panelInner.appendChild(header);
  panelInner.appendChild(body);
  panelInner.appendChild(toast);
  panelInner.appendChild(footer);
  panel.appendChild(panelInner);
  root.appendChild(panel);
  document.body.appendChild(root);

  let closed = false;

  function getCode() {
    return digits.map((d) => String(d)).join("");
  }

  function clearErrorVisual() {
    panel.classList.remove("lock-panel-error");
    toast.classList.remove("lock-toast-err", "lock-toast-ok");
    toast.textContent = "";
  }

  function showError() {
    panel.classList.remove("lock-panel-error");
    void panel.offsetWidth; // reflow para reiniciar animación
    panel.classList.add("lock-panel-error");
    toast.classList.remove("lock-toast-ok");
    toast.classList.add("lock-toast-err");
    toast.textContent = "Código incorrecto.";
  }

  function showSuccessAndClose() {
    toast.classList.remove("lock-toast-err");
    toast.classList.add("lock-toast-ok");
    toast.textContent = "Candado abierto.";
    if (typeof alert === "function") {
      alert(
        "Candado abierto! Hay muchas probetas llenas!\nCoge la carta 33"
      );
    }
    close(true);
  }

  function onCheck() {
    if (closed) return;
    const current = getCode();
    if (current === CORRECT_CODE) {
      showSuccessAndClose();
    } else {
      showError();
    }
  }

  function onCancel() {
    close(false);
  }

  btnCheck.addEventListener("click", onCheck);
  btnCancel.addEventListener("click", onCancel);

  function onKey(ev) {
    if (ev.key === "Enter") {
      ev.preventDefault();
      onCheck();
    } else if (ev.key === "Escape") {
      ev.preventDefault();
      onCancel();
    }
  }
  document.addEventListener("keydown", onKey);

  function close(success) {
    if (closed) return;
    closed = true;

    btnCheck.removeEventListener("click", onCheck);
    btnCancel.removeEventListener("click", onCancel);
    document.removeEventListener("keydown", onKey);

    if (document.body.contains(root)) {
      document.body.removeChild(root);
    }
    if (typeof resumeGameTimer === "function") resumeGameTimer();
    if (typeof onClose === "function") onClose(!!success);
  }

  // devolver pequeño API por si quieres cacharrear desde consola
  return {
    root,
    getCode,
    setCode: (code) => {
      const c = (code || "").toString().padStart(4, "0").slice(0, 4);
      for (let i = 0; i < 4; i++) {
        digits[i] = Number(c[i]) || 0;
        if (displaySpans[i]) displaySpans[i].textContent = String(digits[i]);
      }
      clearErrorVisual();
    },
  };
}

// expositor para pruebas en navegador
if (typeof window !== "undefined") {
  window.startCandadoProbetas = startMinigame;
}
