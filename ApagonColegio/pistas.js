// ./pistas/cartas.js
// Interfaz: openPistas(card, { onClose() })
// Lee ./pistas/cartas.json y muestra UNA pista a la vez con botones Anterior / Siguiente.
// IMPORTANTE: No dispara onChoose ni abre diálogos externos.

const PISTAS_JSON_URL = './cartas.json';

function css() {
  return `
.pst-root{
  position:fixed; inset:0; z-index:13000;
  display:flex; align-items:center; justify-content:center;
  background:rgba(2,6,23,.72);
  font-family:"Poppins",system-ui,-apple-system,"Segoe UI",Roboto,Arial;
}
.pst-panel{
  width:min(560px,94vw);
  background:linear-gradient(180deg,#0b1220,#081018);
  border:1px solid rgba(255,255,255,.06);
  border-radius:14px; color:#e7eefc; padding:16px 16px 12px;
  box-shadow:0 18px 46px rgba(0,0,0,.55);
}
.pst-header{ display:flex; align-items:center; justify-content:space-between; gap:12px; }
.pst-title{ font-weight:900; letter-spacing:.06em; font-size:1.06rem; }
.pst-sub{ color:#b9c7d9; opacity:.9; font-size:.9rem; margin-top:4px; }

.pst-card{
  margin-top:12px; border-radius:12px; padding:12px;
  background:linear-gradient(180deg,#10182a,#0e1624);
  border:1px solid rgba(255,255,255,.06);
  min-height:72px; display:flex; gap:10px; align-items:flex-start;
}
.pst-badge{
  width:38px; height:38px; border-radius:10px; flex:0 0 38px;
  display:flex; align-items:center; justify-content:center;
  background:linear-gradient(180deg,#2fd09f,#0db07e); color:#042617; font-weight:900;
}
.pst-text{ color:#dfe9fb; line-height:1.4; white-space:pre-wrap; }

.pst-empty{
  margin-top:12px; padding:12px; border-radius:12px; text-align:center; font-weight:800;
  background:rgba(127,29,29,.12); color:#fecaca; border:1px solid rgba(239,68,68,.35);
}

.pst-footer{
  display:flex; align-items:center; justify-content:space-between;
  gap:10px; margin-top:12px;
}
.pst-ind{ color:#9fb3cc; font-size:.9rem; letter-spacing:.04em; }
.pst-actions{ display:flex; gap:8px; }
.pst-btn{
  padding:8px 14px; border-radius:10px; font-weight:800; border:1px solid transparent; cursor:pointer;
}
.pst-ghost{ background:transparent; color:#eaf2ff; border-color:rgba(255,255,255,.06); }
.pst-primary{ background:linear-gradient(180deg,#2fd09f,#0db07e); color:#042617; }
.pst-muted{ background:#1a2336; color:#dfe9fb; border-color:rgba(255,255,255,.08); }
.pst-btn:disabled{ opacity:.45; cursor:not-allowed; }
`;
}

async function loadPistas() {
  const res = await fetch(PISTAS_JSON_URL, { cache: 'no-store' });
  if (!res.ok) throw new Error('No se pudo cargar pistas.json');
  return res.json();
}

export async function openPistas(card, opts = {}) {
  const { onClose } = opts;

  // Estilos (una vez)
  if (!document.getElementById('pst-styles')) {
    const st = document.createElement('style');
    st.id = 'pst-styles';
    st.textContent = css();
    document.head.appendChild(st);
  }

  // Cargar JSON
  let data = null;
  try { data = await loadPistas(); } catch (e) { console.warn('Error cargando pistas:', e); }

  const pistas = (data && data[card] && Array.isArray(data[card].pistas)) ? data[card].pistas : null;
  const titulo = (data && data[card] && data[card].titulo) ? data[card].titulo : `Carta ${card}`;

  // Raíz y panel
  const root = document.createElement('div');
  root.className = 'pst-root';
  root.setAttribute('role','dialog');
  root.setAttribute('aria-modal','true');

  const panel = document.createElement('div');
  panel.className = 'pst-panel';

  // Header
  const header = document.createElement('div');
  header.className = 'pst-header';

  const left = document.createElement('div');
  left.innerHTML = `<div class="pst-title">${titulo}</div>`;


  header.appendChild(left);
  panel.appendChild(header);

  let idx = 0;

  if (pistas && pistas.length) {
    const cardWrap = document.createElement('div');
    cardWrap.className = 'pst-card';

    const badgeEl = document.createElement('div');
    badgeEl.className = 'pst-badge';

    const textEl = document.createElement('div');
    textEl.className = 'pst-text';

    cardWrap.appendChild(badgeEl);
    cardWrap.appendChild(textEl);
    panel.appendChild(cardWrap);

    const footer = document.createElement('div');
    footer.className = 'pst-footer';

    const indEl = document.createElement('div');
    indEl.className = 'pst-ind';

    const actions = document.createElement('div');
    actions.className = 'pst-actions';

    const prevBtn = document.createElement('button');
    prevBtn.className = 'pst-btn pst-muted';
    prevBtn.textContent = 'Anterior';

    const nextBtn = document.createElement('button');
    nextBtn.className = 'pst-btn pst-primary';
    nextBtn.textContent = 'Siguiente';

    const closeBtn = document.createElement('button');
    closeBtn.className = 'pst-btn pst-ghost';
    closeBtn.textContent = 'Cerrar';
    closeBtn.onclick = () => { cleanup(); if (typeof onClose === 'function') onClose(); };

    actions.appendChild(prevBtn);
    actions.appendChild(nextBtn);
    actions.appendChild(closeBtn);

    footer.appendChild(indEl);
    footer.appendChild(actions);
    panel.appendChild(footer);

    function setIndex(newIdx) {
      idx = Math.max(0, Math.min(pistas.length - 1, newIdx));
      const n = idx + 1;
      badgeEl.textContent = n;
      textEl.textContent = pistas[idx];
      indEl.textContent = `Pista ${n} / ${pistas.length}`;
      prevBtn.disabled = (idx === 0);
      nextBtn.disabled = (idx === pistas.length - 1);
    }

    prevBtn.onclick = () => setIndex(idx - 1);
    nextBtn.onclick = () => setIndex(idx + 1);

    // Navegación con flechas
    function onKey(e) {
      if (e.key === 'Escape') { e.preventDefault(); cleanup(); if (typeof onClose === 'function') onClose(); }
      if (e.key === 'ArrowLeft' && idx > 0) setIndex(idx - 1);
      if (e.key === 'ArrowRight' && idx < pistas.length - 1) setIndex(idx + 1);
    }
    document.addEventListener('keydown', onKey);

    // limpiar
    function cleanup() {
      document.removeEventListener('keydown', onKey);
      if (document.body.contains(root)) document.body.removeChild(root);
    }

    root.cleanup = cleanup; // opcional
    setIndex(0);
  } else {
    const emptyEl = document.createElement('div');
    emptyEl.className = 'pst-empty';
    emptyEl.textContent = 'No hay pistas para esta carta.';
    panel.appendChild(emptyEl);

    const onlyClose = document.createElement('div');
    onlyClose.className = 'pst-actions';
    const cbtn = document.createElement('button');
    cbtn.className = 'pst-btn pst-ghost';
    cbtn.textContent = 'Cerrar';
    cbtn.onclick = () => { cleanup(); if (typeof onClose === 'function') onClose(); };
    onlyClose.appendChild(cbtn);
    panel.appendChild(onlyClose);

    function cleanup() {
      if (document.body.contains(root)) document.body.removeChild(root);
    }
    root.cleanup = cleanup;
  }

  root.appendChild(panel);
  document.body.appendChild(root);
}

// Compatibilidad con import default
export { openPistas as default };
