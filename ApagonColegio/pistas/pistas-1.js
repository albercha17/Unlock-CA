// ApagonColegio/pistas/pista-1.js
export function openPistas(card, opts = {}) {
  // opts: { onClose: fn() }
  const { onClose } = opts;

  // Datos de ejemplo para la carta
  const pistas = {
    1: {
      1: "Ordenalos como están ordenados en la tabla periódica.",
      2: "C ➜ N ➜ O ➜ S."
    }
    // Puedes añadir más cartas así: 2: {1: '...', 2:'...'}
  };

  const cardNum = String(Number(card)); // normalizar
  const data = pistas[cardNum] || {
    1: "Pista fácil: (no hay pistas definidas para esta carta).",
    2: "Pista clara: (no hay pistas definidas para esta carta)."
  };

  // Crear overlay y caja
  const overlay = document.createElement('div');
  overlay.style =
    'position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,0.6);z-index:2600;padding:18px;';

  const box = document.createElement('div');
  box.style =
    'width:420px;max-width:96%;background:#101216;color:#fff;border-radius:12px;padding:18px;border:1px solid rgba(255,255,255,0.04);box-shadow:0 20px 60px rgba(0,0,0,0.7);font-family:inherit;';

  box.innerHTML = `<h3 style="margin:0 0 8px 0">Pistas — Carta ${cardNum}</h3>`;

  // Área de texto para mostrar la pista
  const textArea = document.createElement('div');
  textArea.style =
    'min-height:80px;margin-top:10px;color:#d6d6d6;padding:12px;border-radius:8px;background:linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.00));border:1px solid rgba(255,255,255,0.02);';
  textArea.textContent = data[1];

  // Fila de botones numerados (selección de pista)
  const btnRow = document.createElement('div');
  btnRow.style = 'display:flex;gap:8px;justify-content:center;margin-top:12px;';

  // Helper para aplicar estilo consistente a botones
  function styleButton(btn) {
    btn.type = 'button';
    btn.style.padding = '8px 12px';
    btn.style.borderRadius = '8px';
    btn.style.border = '1px solid rgba(255,255,255,0.06)';
    btn.style.background = 'transparent';
    btn.style.color = '#fff';
    btn.style.cursor = 'pointer';
    btn.style.fontWeight = '700';
    btn.style.minWidth = '44px';
    btn.style.height = '44px';
    btn.style.display = 'inline-flex';
    btn.style.alignItems = 'center';
    btn.style.justifyContent = 'center';
    btn.style.transition = 'all .16s ease';
    btn.style.userSelect = 'none';
  }

  // Helper para marcar seleccionado
  function markSelected(btn) {
    [btn1, btn2].forEach(b => {
      b.style.background = 'transparent';
      b.style.boxShadow = 'none';
      b.style.color = '#fff';
    });
    btn.style.background = 'linear-gradient(90deg, rgba(255,255,255,0.06), rgba(255,255,255,0.03))';
    btn.style.boxShadow = '0 8px 26px rgba(0,0,0,0.45)';
    btn.style.color = '#ffdca6';
  }

  const btn1 = document.createElement('button');
  btn1.textContent = '1';
  styleButton(btn1);

  const btn2 = document.createElement('button');
  btn2.textContent = '2';
  styleButton(btn2);

  btnRow.appendChild(btn1);
  btnRow.appendChild(btn2);

  // Fila de acciones (solo botón cerrar)
  const closeRow = document.createElement('div');
  closeRow.style = 'display:flex;gap:8px;justify-content:center;margin-top:14px;';
  const closeBtn = document.createElement('button');
  closeBtn.textContent = 'Cerrar';
  styleButton(closeBtn);
  closeBtn.style.background = 'transparent';
  closeRow.appendChild(closeBtn);

  // Montar estructura
  box.appendChild(textArea);
  box.appendChild(btnRow);
  box.appendChild(closeRow);
  overlay.appendChild(box);
  document.body.appendChild(overlay);

  // Estado seleccionado (1 por defecto)
  markSelected(btn1);

  // Manejadores de selección
  btn1.addEventListener('click', () => {
    textArea.textContent = data[1];
    markSelected(btn1);
  });
  btn2.addEventListener('click', () => {
    textArea.textContent = data[2];
    markSelected(btn2);
  });

  // Cerrar modal
  function cleanup() {
    document.removeEventListener('keydown', escHandler);
    overlay.remove();
    if (typeof onClose === 'function') {
      try { onClose(); } catch (e) { console.error('onClose error', e); }
    }
  }
  closeBtn.addEventListener('click', cleanup);

  // ESC cierra también
  function escHandler(e) {
    if (e.key === 'Escape') cleanup();
  }
  document.addEventListener('keydown', escHandler);

  return { close: cleanup };
}
