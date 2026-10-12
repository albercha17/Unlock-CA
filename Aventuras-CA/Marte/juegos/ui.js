// Base común de los minijuegos: overlay, título, feedback, botones y cierre.

const STYLE_ID = 'far-ui-style';

function injectStyle() {
  if (document.getElementById(STYLE_ID)) return;
  const s = document.createElement('style');
  s.id = STYLE_ID;
  s.textContent = `
    .far-overlay{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:rgba(2,6,12,.8);z-index:2500;padding:12px;font-family:"Poppins",system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}
    .far-box{width:min(480px,94vw);max-height:94vh;overflow:auto;background:linear-gradient(180deg,#14202c,#0c141d);border:1px solid rgba(255,255,255,.1);border-radius:14px;padding:20px;color:#fff;box-shadow:0 18px 50px rgba(0,0,0,.65);text-align:center}
    .far-title{margin:0 0 4px;font-size:1.1rem}
    .far-instr{margin:0 0 14px;color:#b9c7d6;font-size:.9rem}
    .far-feedback{min-height:1.4em;margin:10px 0;font-weight:700}
    .far-feedback.ok{color:#9dffb0}
    .far-feedback.bad{color:#ffb3b3}
    .far-actions{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}
    .far-btn{padding:10px 16px;border-radius:10px;border:none;font-weight:700;cursor:pointer;font-family:inherit}
    .far-btn.primary{background:linear-gradient(180deg,#ffd27a,#f0a020);color:#2a1600}
    .far-btn.ghost{background:#26323f;color:#fff;border:1px solid rgba(255,255,255,.12)}
    .far-btn:disabled{opacity:.5;cursor:not-allowed}
    .far-btn:focus-visible,.far-key:focus-visible{outline:2px solid #ffd27a;outline-offset:2px}
    .far-display{font-size:1.8rem;font-weight:800;letter-spacing:6px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08);border-radius:10px;padding:10px 0;margin-bottom:14px;min-height:46px}
    .far-keypad{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:12px}
    .far-keyboard{display:grid;grid-template-columns:repeat(7,1fr);gap:6px;margin-bottom:12px}
    .far-key{background:linear-gradient(180deg,rgba(255,255,255,.1),rgba(255,255,255,.03));border:1px solid rgba(255,255,255,.1);color:#fff;padding:12px 0;border-radius:9px;font-size:1.05rem;font-weight:700;cursor:pointer;font-family:inherit}
    .far-key:active{transform:translateY(1px)}
    .far-key:disabled{opacity:.45;cursor:not-allowed}
  `;
  document.head.appendChild(s);
}

export function openGame({ title, instr, pauseGameTimer, resumeGameTimer, onClose }) {
  injectStyle();
  if (typeof pauseGameTimer === 'function') pauseGameTimer();

  const overlay = document.createElement('div');
  overlay.className = 'far-overlay';
  overlay.innerHTML =
    '<div class="far-box" role="dialog" aria-modal="true">' +
    '<h3 class="far-title"></h3><p class="far-instr"></p>' +
    '<div class="far-body"></div><div class="far-feedback" aria-live="polite"></div><div class="far-actions"></div></div>';
  overlay.querySelector('.far-title').textContent = title;
  overlay.querySelector('.far-instr').textContent = instr;
  document.body.appendChild(overlay);

  const body = overlay.querySelector('.far-body');
  const feedback = overlay.querySelector('.far-feedback');
  const actions = overlay.querySelector('.far-actions');
  const closers = [];
  let closed = false;

  function close() {
    if (closed) return;
    closed = true;
    closers.forEach(fn => { try { fn(); } catch (e) { /* ignore */ } });
    document.removeEventListener('keydown', onKey);
    overlay.remove();
    if (typeof resumeGameTimer === 'function') resumeGameTimer();
    if (typeof onClose === 'function') onClose();
  }
  function onKey(e) { if (e.key === 'Escape') close(); }
  document.addEventListener('keydown', onKey);

  function button(label, kind, fn) {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = 'far-btn ' + kind;
    b.textContent = label;
    b.addEventListener('click', fn);
    actions.appendChild(b);
    return b;
  }
  button('Cerrar', 'ghost', close);

  return {
    body,
    button,
    close,
    onClose(fn) { closers.push(fn); },
    say(text, kind) {
      feedback.textContent = text;
      feedback.className = 'far-feedback' + (kind ? ' ' + kind : '');
    }
  };
}
