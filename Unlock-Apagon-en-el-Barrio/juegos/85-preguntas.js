// juegos/85-preguntas.js
// Minijuego: 4 preguntas de Doña Pilar sobre electricidad y ahorro energético.
// Hay que acertar las 4 (si falla una, se puede reintentar esa misma pregunta).
// Exporta startMinigame(opts)

const QUESTIONS = [
  {
    q: '¿Qué debes hacer si ves un cable pelado por el suelo?',
    options: ['Tocarlo con cuidado para ver si da corriente', 'No tocarlo nunca y avisar a un adulto', 'Envolverlo con papel de aluminio'],
    correct: 1
  },
  {
    q: '¿Cuál de estas acciones ahorra energía en casa?',
    options: ['Dejar las luces encendidas todo el día', 'Apagar las luces al salir de una habitación', 'Dejar el frigorífico abierto'],
    correct: 1
  },
  {
    q: '¿Para qué sirve un fusible?',
    options: ['Es un tipo de bombilla especial', 'Corta la corriente si algo va mal, para evitar incendios', 'Es un cable de color'],
    correct: 1
  },
  {
    q: 'Si ves chispas saliendo de un enchufe, ¿qué haces?',
    options: ['Apagar el interruptor general y avisar a un adulto', 'Echarle agua', 'Seguir usándolo con cuidado'],
    correct: 0
  }
];

export function startMinigame(opts = {}) {
  const { onClose, pauseGameTimer, resumeGameTimer } = opts;
  if (typeof pauseGameTimer === 'function') pauseGameTimer();

  const styleId = 'aebq-style';
  if (!document.getElementById(styleId)) {
    const style = document.createElement('style');
    style.id = styleId;
    style.textContent = `
      .aebq-overlay{ position:fixed; inset:0; display:flex; align-items:center; justify-content:center;
        background:rgba(0,0,0,0.7); z-index:2500; padding:12px; font-family:"Poppins",system-ui,-apple-system,Segoe UI,Roboto,Arial; }
      .aebq-box{ width:min(460px,94vw); background:#12121a; border:1px solid rgba(255,255,255,0.1);
        border-radius:14px; padding:20px; color:#fff; box-shadow:0 18px 50px rgba(0,0,0,0.6); }
      .aebq-box h3{ margin:0 0 4px; text-align:center; font-size:1.1rem; }
      .aebq-progress{ text-align:center; color:#9fb3cc; font-size:0.85rem; margin-bottom:12px; }
      .aebq-q{ font-weight:700; margin-bottom:14px; text-align:center; }
      .aebq-opt{ display:block; width:100%; text-align:left; margin-bottom:10px; padding:12px 14px; border-radius:10px;
        background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.1); color:#fff; cursor:pointer; font-size:0.92rem; }
      .aebq-opt:hover{ background:rgba(255,255,255,0.12); }
      .aebq-opt.correct{ background:rgba(60,200,110,0.35); border-color:#3ec86e; }
      .aebq-opt.wrong{ background:rgba(230,60,60,0.35); border-color:#e63c3c; }
      .aebq-feedback{ min-height:1.4em; text-align:center; font-weight:700; margin:10px 0; }
      .aebq-feedback.ok{ color:#9dffb0; }
      .aebq-feedback.bad{ color:#ffb3b3; }
      .aebq-actions{ display:flex; gap:10px; justify-content:center; margin-top:6px; }
      .aebq-btn{ padding:10px 16px; border-radius:10px; border:none; font-weight:700; cursor:pointer; }
      .aebq-btn.primary{ background:linear-gradient(180deg,#ffcf6b,#ff9d1f); color:#2a1600; }
      .aebq-btn.ghost{ background:#2d2f33; color:#fff; border:1px solid rgba(255,255,255,0.1); }
    `;
    document.head.appendChild(style);
  }

  const overlay = document.createElement('div');
  overlay.className = 'aebq-overlay';
  overlay.innerHTML = `
    <div class="aebq-box">
      <h3>Carta 85 — Preguntas de Doña Pilar</h3>
      <div class="aebq-progress" id="aebqProgress"></div>
      <div class="aebq-q" id="aebqQuestion"></div>
      <div id="aebqOptions"></div>
      <div class="aebq-feedback" id="aebqFeedback"></div>
      <div class="aebq-actions">
        <button class="aebq-btn ghost" id="aebqClose">Cerrar</button>
      </div>
    </div>
  `;
  document.body.appendChild(overlay);

  const progressEl = overlay.querySelector('#aebqProgress');
  const questionEl = overlay.querySelector('#aebqQuestion');
  const optionsEl = overlay.querySelector('#aebqOptions');
  const feedback = overlay.querySelector('#aebqFeedback');

  let idx = 0;

  function renderQuestion() {
    feedback.textContent = '';
    const item = QUESTIONS[idx];
    progressEl.textContent = `Pregunta ${idx + 1} / ${QUESTIONS.length}`;
    questionEl.textContent = item.q;
    optionsEl.innerHTML = '';
    item.options.forEach((opt, i) => {
      const btn = document.createElement('button');
      btn.className = 'aebq-opt';
      btn.textContent = opt;
      btn.addEventListener('click', () => answer(i, btn));
      optionsEl.appendChild(btn);
    });
  }

  function answer(i, btn) {
    const item = QUESTIONS[idx];
    const buttons = Array.from(optionsEl.children);
    buttons.forEach(b => b.style.pointerEvents = 'none');
    if (i === item.correct) {
      btn.classList.add('correct');
      feedback.textContent = '¡Correcto!';
      feedback.className = 'aebq-feedback ok';
      setTimeout(() => {
        idx++;
        if (idx < QUESTIONS.length) {
          renderQuestion();
        } else {
          questionEl.textContent = '¡Habéis acertado las 4! Doña Pilar os da su vieja medalla.';
          optionsEl.innerHTML = '';
          progressEl.textContent = 'Coged la carta 90.';
          feedback.textContent = '';
        }
      }, 700);
    } else {
      btn.classList.add('wrong');
      feedback.textContent = 'No es correcta, inténtalo otra vez.';
      feedback.className = 'aebq-feedback bad';
      setTimeout(() => renderQuestion(), 900);
    }
  }

  renderQuestion();

  function close() {
    document.removeEventListener('keydown', onKey);
    overlay.remove();
    if (typeof resumeGameTimer === 'function') resumeGameTimer();
    if (typeof onClose === 'function') onClose();
  }
  overlay.querySelector('#aebqClose').addEventListener('click', close);
  function onKey(e){ if (e.key === 'Escape') close(); }
  document.addEventListener('keydown', onKey);

  return { close };
}
