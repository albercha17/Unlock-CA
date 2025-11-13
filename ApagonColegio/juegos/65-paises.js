// juegos/globoPaises/main.js
// Minijuego: elegir país sobre un globo terráqueo PNG.

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

  /* =============== MAIN ZONE (GLOBO + LISTA) =============== */
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
    { name: "EEUU", key: "eeuu", file: "eeuu.png" },
    { name: "España", key: "espana", file: "espana.png" },
    { name: "Italia", key: "italia", file: "italia.png" },
    { name: "Inglaterra", key: "inglaterra", file: "inglaterra.png" },
    { name: "Francia", key: "francia", file: "francia.png" },
    { name: "Alemania", key: "alemania", file: "alemania.png" },
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
  viewImg.className = "mgl-country-img";
  viewImg.alt = "Mapa del país";

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

  /* =============== LÓGICA =============== */

  let currentCountryKey = null;

  function mostrarPais(country) {
    currentCountryKey = country.key;

    viewImg.src = `./images/${country.file}`;
    viewImg.style.cursor = "default";
    viewImg.onclick = null; // limpiar cualquier handler anterior

    // Comportamiento especial para Italia → click en Roma
    if (country.key === "italia") {
      viewImg.style.cursor = "pointer";
      viewImg.onclick = (ev) => {
        const rect = viewImg.getBoundingClientRect();
        if (!rect.width || !rect.height) return;

        const x = (ev.clientX - rect.left) / rect.width;
        const y = (ev.clientY - rect.top) / rect.height;

        // Zona aproximada de ROMA en tu imagen.
        // Si no cuadra perfecto, ajusta estos rangos:
        //          ↓↓↓  x entre 0 y 1  ↓↓↓        ↓↓↓ y entre 0 y 1 ↓↓↓
        const inRome =
          x >= 0.40 && x <= 0.70 &&   // más/menos ancho
          y >= 0.46 && y <= 0.63;     // más/menos alto

        if (inRome) {
          // En tu apagon.html ya hay un override bonito de alert()
          alert("ACERTIJO RESUELTO!\nCoge la carta 17.");
        }
      };
    }

    main.style.display = "none";
    view.style.display = "flex";
    view.classList.add("mgl-fade");
  }

  function mostrarSelector() {
    view.style.display = "none";
    main.style.display = "grid";
    currentCountryKey = null;
    viewImg.src = "";
    viewImg.style.cursor = "default";
    viewImg.onclick = null;
  }

  function cerrar(ok) {
    try {
      root.remove();
    } catch (e) {}

    if (typeof resumeGameTimer === "function") resumeGameTimer();
    if (typeof onClose === "function") onClose(ok === true);
  }

  function onKey(e) {
    if (e.key === "Escape") cerrar(false);
  }
  document.addEventListener("keydown", onKey);

  // Limpieza si hiciera falta
  function cleanup() {
    document.removeEventListener("keydown", onKey);
  }

  // Exponer cleanup opcionalmente
  return { root, cleanup };
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
  max-height:96vh;
  background:#020617;
  border-radius:20px;
  border:1px solid rgba(148,163,184,0.45);
  box-shadow:0 22px 52px rgba(15,23,42,0.9);
  color:#e5edff;
  padding:18px;
  display:flex;
  flex-direction:column;
  position:relative;
  box-sizing:border-box;
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

/* Zona principal: globo + lista */
.mgl-main{
  flex:1;
  display:grid;
  grid-template-columns: minmax(0,1.2fr) minmax(0,1fr);
  gap:18px;
  min-height:0;
}
@media (max-width:720px){
  .mgl-main{ grid-template-columns:1fr; }
}

/* GLOBO PNG */
.mgl-globe-wrap{
  display:flex;
  align-items:center;
  justify-content:center;
  min-height:0;
}
.mgl-globe-img{
  width:100%;
  max-width:360px;
  height:auto;
  border-radius:999px;
  object-fit:contain;
  box-shadow:0 18px 38px rgba(0,0,0,0.55);
  border:2px solid rgba(255,255,255,0.05);
}

/* Lista de países */
.mgl-side{
  display:flex; flex-direction:column; gap:10px;
  min-height:0;
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

/* Vista país (ocupa el mismo hueco que main) */
.mgl-country-view{
  flex:1;
  display:none;
  flex-direction:column;
  background:#0b1120;
  border-radius:12px;
  padding:14px;
  gap:10px;
  box-shadow:0 14px 28px rgba(0,0,0,.45);
  min-height:0;
}

/* Contenedor de la imagen para que no se salga */
.mgl-country-image-wrap{
  flex:1;
  display:flex;
  align-items:center;
  justify-content:center;
  max-height:100%;
  overflow:hidden;
}

/* Imagen responsiva del país */
.mgl-country-img{
  max-width:100%;
  max-height:100%;
  width:auto;
  height:auto;
  object-fit:contain;
  border-radius:12px;
  box-shadow:0 18px 36px rgba(0,0,0,0.65);
  border:1px solid rgba(15,23,42,0.9);
}

.mgl-back-btn{
  padding:6px 12px;
  border-radius:10px;
  border:none;
  background:#1e293b;
  color:#fff;
  cursor:pointer;
  align-self:flex-start;
}

.mgl-fade{ animation:mgl-fade .25s ease-out; }

@keyframes mgl-fade{
  from{opacity:0; transform:translateY(6px);}
  to{opacity:1;}
}
`;
}
