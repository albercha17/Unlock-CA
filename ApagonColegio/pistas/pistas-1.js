// ApagonColegio/pistas/pista-1.js
export function openPistas(card, opts = {}) {
  // opts: { onChoose: fn(choiceNumber, text), onClose: fn() }
  const { onChoose, onClose } = opts;

  // Datos de ejemplo para la carta (puedes leer desde JSON o generar dinámicamente)
  const pistas = {
    1: {
      1: "Pista fácil: La sala con número impar guarda algo bajo la alfombra.",
      2: "Pista clara: Busca en la sala 3, debajo del felpudo que tiene una mancha de pintura."
    }
    // puedes añadir más cartas así: 2: {1: '...', 2:'...'}
  };

  const cardNum = String(Number(card)); // normalizar
  const data = pistas[cardNum] || {
    1: "Pista fácil: (no hay pistas definidas para esta carta).",
    2: "Pista clara: (no hay pistas definidas para esta carta)."
  };

  // Crear modal
  const overlay = document.createElement('div');
  overlay.style = 'position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,0.6);z-index:2600;padding:18px;';

  const box = document.createElement('div');
  box.style = 'width:420px;max-width:96%;background:#101216;color:#fff;border-radius:12px;padding:18px;border:1px solid rgba(255,255,255,0.04);box-shadow:0 20px 60px rgba(0,0,0,0.7);';

  box.innerHTML = `<h3 style="margin:0 0 8px 0">Pistas — Carta ${cardNum}</h3>`;

  // area para mostrar la pista
  const textArea = document.createElement('div');
  textArea.style = 'min-height:70px;margin-top:10px;color:#d6d6d6;padding:10px;border-radius:8px;background:rgba(255,255,255,0.02);';
  textArea.textContent = data[1];

  // botones para elegir pista 1 o 2
  const btnRow = document.createElement('div');
  btnRow.style = 'display:flex;gap:8px;justify-content:center;margin-top:12px;';

  const btn1 = document.createElement('button');
  btn1.textContent = '1';
  btn1.style = 'padding:8px 12px;border-radius:8px;border:1px solid rgba(255,255,255,0.06);background:transparent;color:#fff;cursor:pointer;font-weight:700';
  const btn2 = document.createElement('button');
  btn2.textContent = '2';
  btn2.style = btn1.style;

  btnRow.appendChild(btn1);
  btnRow.appendChild(btn2);

  // botón cerrar
  const closeRow = document.createElement('div');
  closeRow.style = 'display:flex;gap:8px;justify-content:center;margin-top:14px;';
  const closeBtn = document.createElement('button');
  closeBtn.textContent = 'Cerrar';
  closeBtn.style = 'padding:8px 12px;border-radius:8px;border:1px solid rgba(255,255,255,0.06);background:transparent;color:#fff;cursor:pointer;font-weight:700';
  closeRow.appendChild(closeBtn);

  box.appendChild(textArea);
  box.appendChild(btnRow);
  box.appendChild(closeRow);
  overlay.appendChild(box);
  document.body.appendChild(overlay);

  // manejadores
  btn1.addEventListener('click', () => {
    textArea.textContent = data[1];
    if(typeof onChoose === 'function') onChoose(1, data[1]);
  });
  btn2.addEventListener('click', () => {
    textArea.textContent = data[2];
    if(typeof onChoose === 'function') onChoose(2, data[2]);
  });

  function cleanup(){
    overlay.remove();
    if(typeof onClose === 'function') onClose();
  }
  closeBtn.addEventListener('click', cleanup);
  document.addEventListener('keydown', function escHandler(e){
    if(e.key === 'Escape'){ cleanup(); document.removeEventListener('keydown', escHandler); }
  });

  // devuelve handle por si quieres cerrarlo desde fuera
  return { close: cleanup };
}
