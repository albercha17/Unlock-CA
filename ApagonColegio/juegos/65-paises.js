// juegos/globoPaises/main.js
// Minijuego: elegir país sobre un globo terráqueo PNG.
// Alberto Approved™: estética Unlock, animaciones suaves, compatible iPhone.

export function startMinigame(opts = {}) {
  const { onClose, pauseGameTimer, resumeGameTimer } = opts;

  if (typeof pauseGameTimer === "function") pauseGameTimer();

  /* =============== ESTILOS =============== */
  if (!document.getElementById("mgl-styles")) {
    const st = document.createElement("style");
    st.id = "mgl-styles";
    st.textContent = makeStyles();
    document.head.appendChild(st);
  }

  /* =============== OVERLAY =============== */
  const root = document.createElement("div");
  root.className = "mgl-root";
  root.setAttribute("role", "dialog");
  root.setAttribute("aria-modal", "true");

  const panel = document.createElement("div");
  panel.className = "mgl-panel";

  /* =============== HEADER =============== */
  const header = document.createElement("div");
  header.className = "mgl-header";
  header.innerHTML = `
    <div class="mgl-title">Explorador de Países</div>
    <button class="mgl-close">Salir</button>
  `;
  header.querySelector(".mgl-close").onclick = () => cerrar(false);

  /* =============== MAIN ZONE =============== */
  const main = document.createElement("div");
  main.className = "mgl-main";

  /* --- GLOBO PNG --- */
  const globeWrap = document.createElement("div");
  globeWrap.className = "mgl-globe-wrap";

  const globeImg = document.createElement("img");
  globeImg.className = "mgl-globe-img";
  globeImg.src = "./images/mundo.png"; // <-- tu PNG
  globeImg.alt = "Globo terráqueo";

  globeWrap.appendChild(globeImg);

  /* =============== LISTA DE PAÍSES =============== */
  const countryWrap = document.createElement("div");
  countryWrap.className = "mgl-side";

  const countryGrid = document.createElement("div");
  countryGrid.className = "mgl-country-grid";

  const countries = [
    { name: "EEUU", file: "eeuu.png" },
    { name: "España", file: "espana.png" },
    { name: "Italia", file: "italia.png" },
    { name: "Inglaterra", file: "inglaterra.png" },
    { name: "Francia", file: "francia.png" },
    { name: "Alemania", file: "alemania.png" },
  ];

  countries.forEach((c) => {
    const btn = document.createElement("button");
    btn.className = "mgl-country-btn";
    btn.textContent = c.name;
    btn.onclick = () => mostrarPais(c);
    countryGrid.appendChild(btn);
  });

  countryWrap.appendChild(countryGrid);

  /* =============== VISTA DE PAÍS ELEGIDO =============== */
  const view = document.createElement("div");
  view.className = "mgl-country-view";

  const viewImgWrap = document.createElement("div");
  viewImgWrap.className = "mgl-country-image-wrap";

  const viewImg = document.createElement("img");
  viewImg.style.width = "100%";
  viewImg.style.borderRadius = "12px";

  viewImgWrap.appendChild(viewImg);

  const backBtn = document.createElement("button");
  backBtn.className = "mgl-back-btn";
  backBtn.textContent = "← Volver";
  backBtn.onclick = () => mostrarSelector();

  view.appendChild(viewImgWrap);
  view.appendChild(backBtn);

  /* Añadir todo al panel */
  main.appendChild(globeWrap);
  main.appendChild(countryWrap);
  panel.appendChild(header);
  panel.appendChild(main);
  panel.appendChild(view);
  root.appendChild(panel);
  document.body.appendChild(root);

  /* =============== FUNCIONES DE LÓGICA =============== */

  function mostrarPais(country) {
    viewImg.src = `./images/${country.file}`;
    main.style.display = "none";
    view.style.display = "flex";
    view.classList.add("mgl-fade");
  }

  function mostrarSelector() {
    view.style.display = "none";
    main.style.display = "grid";
  }

  function cerrar(ok) {
    try {
      root.remove();
    } catch (e) {}

    if (typeof resumeGameTimer === "function") resumeGameTimer();
    if (typeof onClose === "function") onClose(ok === true);
  }

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") cerrar(false);
  });
}

/* =============== ESTILOS =============== */
function makeStyles() {
  return `
.mgl-root{
  position:fixed; inset:0; z-index:2400;
  display:flex; align-items:center; justify-content:center;
  background:radial-gradient(circle at top,#020617 0%,#020617 40%,#000 100%);
  font-family:"Poppins",system-ui,-apple-system,"Segoe UI",Roboto,Arial;
}
.mgl-panel{
  width:min(820px,96vw);
  min-height:min(520px,92vh);
  background:#020617;
  border-radius:20px;
  border:1px solid rgba(148,163,184,0.45);
  box-shadow:0 22px 52px rgba(15,23,42,0.9);
  color:#e5edff;
  padding:18px;
  display:flex; flex-direction:column;
  position:relative;
}

.mgl-header{
  display:flex; justify-content:space-between; align-items:center;
  margin-bottom:12px;
}
.mgl-title{
  font-size:1.2rem; font-weight:900; letter-spacing:.06em;
}
.mgl-close{
  padding:8px 14px; font-weight:800; border-radius:10px; cursor:pointer;
  border:1px solid rgba(255,255,255,.08);
  background:#1e293b; color:#fff;
}

.mgl-main{
  flex:1;
  display:grid;
  grid-template-columns: minmax(0,1.2fr) minmax(0,1fr);
  gap:18px;
}
@media (max-width:720px){
  .mgl-main{ grid-template-columns:1fr; }
}

/* GLOBO PNG */
.mgl-globe-wrap{
  display:flex;
  align-items:center;
  justify-content:center;
}
.mgl-globe-img{
  width:100%;
  max-width:360px;
  height:auto;
  border-radius:999px;
  object-fit:cover;
  box-shadow:0 18px 38px rgba(0,0,0,0.55);
  border:2px solid rgba(255,255,255,0.05);
}

.mgl-side{
  display:flex; flex-direction:column; gap:10px;
}

.mgl-country-grid{
  display:grid; gap:8px;
  grid-template-columns:repeat(2,1fr);
}

.mgl-country-btn{
  border-radius:999px;
  padding:10px 14px;
  border:1px solid rgba(148,163,184,.5);
  background:#0b1120;
  color:#e5edff;
  font-weight:700;
  cursor:pointer;
  box-shadow:0 6px 16px rgba(0,0,0,.35);
  transition:0.2s;
}
.mgl-country-btn:hover{
  transform:translateY(-3px);
  border-color:rgba(96,165,250,.9);
}

/* VISTA PAÍS */
.mgl-country-view{
  display:none;
  flex-direction:column;
  background:#0b1120;
  border-radius:12px;
  padding:14px;
  gap:10px;
  box-shadow:0 14px 28px rgba(0,0,0,.45);
}
.mgl-back-btn{
  padding:6px 12px;
  border-radius:10px;
  border:none;
  background:#1e293b;
  color:#fff;
  cursor:pointer;
}
.mgl-fade{ animation:mgl-fade .25s ease-out; }

@keyframes mgl-fade{
  from{opacity:0; transform:translateY(6px);}
  to{opacity:1;}
}
`;
}
