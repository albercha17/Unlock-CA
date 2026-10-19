"""Añade a todos los pc.html el soporte de FOLIOSCOPIOS («El Cuarto de Leo, 1995»): cartas-página que se ordenan y se hojean como una animación.

`_meta.folioscopios` = {clave: {"titulo": ..., "cartas": [...]}} en cartas.json. Cuando todas sus cartas están en la mesa sale el botón
«Hojear: <título>»: las páginas se ordenan tocando dos para cambiarlas de sitio (empiezan por número de carta) y «Reproducir» las pasa una tras
otra. No dice si el orden es el bueno: eso lo deduce quien juega. En papel, las cartas se apilan en orden y se pasan con el pulgar. Idempotente.
Uso (desde la raíz del repo):  python herramientas/parche_folioscopio.py
"""
import glob

CSS = """  /* ===== Folioscopio: páginas que se ordenan y se hojean ===== */
  #hojear{position:fixed;inset:0;z-index:60;background:rgba(2,6,12,.93);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;padding:16px;overflow:auto}
  #hojear[hidden]{display:none}
  #hojear h3{margin:0;font-size:1.1rem}
  .hj-visor{width:min(70vw,260px,calc(42vh * 63 / 88));aspect-ratio:63 / 88;border-radius:6px;border:2px solid var(--line);background:#1b2733 center / cover no-repeat}
  .hj-tira{display:flex;gap:6px;flex-wrap:wrap;justify-content:center}
  .hj-pag{width:min(16vw,74px);aspect-ratio:63 / 88;padding:0;border:2px solid var(--line);border-radius:4px;background:#1b2733 center / cover no-repeat;cursor:pointer;position:relative}
  .hj-pag span{position:absolute;left:2px;top:2px;background:rgba(0,0,0,.7);color:#fff;font-size:.7rem;padding:0 4px;border-radius:3px}
  .hj-pag.sel{border-color:var(--acc);box-shadow:0 0 0 2px var(--acc)}
  .hj-pag.ahora{outline:3px solid #7be495;outline-offset:1px}
"""

HTML = """<div id="hojear" hidden role="dialog" aria-modal="true" aria-label="Hojear el folioscopio">
  <h3 id="hjTitulo"></h3>
  <p class="aviso">Toca dos páginas para cambiarlas de sitio y pulsa «Reproducir» para hojearlas en ese orden.</p>
  <div id="hjVisor" class="hj-visor"></div>
  <div id="hjTira" class="hj-tira"></div>
  <div class="fila"><button type="button" id="hjPlay" class="primario">Reproducir</button><button type="button" id="hjCerrar">Cerrar</button></div>
</div>

"""

JS = """  // ----- Folioscopio: ordenar páginas y hojearlas -----
  var FOLIO = {}, folioActual = null, folioSel = null, folioTimer = null;
  function folioscopios(){ return (DATA._meta && DATA._meta.folioscopios) || {}; }
  function pintarFolioscopios(){
    var cont = $('montajes'), fs = folioscopios();
    Object.keys(fs).forEach(function(k){
      var f = fs[k];
      if (!f.cartas.every(function(id){ return estado.mesa.indexOf(id) >= 0; })) return;
      var b = document.createElement('button'); b.type = 'button'; b.className = 'montar primario hojear'; b.dataset.folio = k;
      b.textContent = 'Hojear: ' + f.titulo;
      b.addEventListener('click', function(){ abrirFolio(k); });
      cont.appendChild(b);
    });
  }
  function abrirFolio(k){
    var f = folioscopios()[k];
    if (!FOLIO[k]) FOLIO[k] = f.cartas.slice().sort(orden);
    folioActual = k; folioSel = null;
    $('hjTitulo').textContent = f.titulo;
    pintarFolio(-1);
    $('hojear').hidden = false; $('hjCerrar').focus();
  }
  function pintarFolio(ahora){
    var t = $('hjTira'), lista = FOLIO[folioActual]; t.innerHTML = '';
    lista.forEach(function(id, i){
      var b = document.createElement('button'); b.type = 'button'; b.className = 'hj-pag' + (folioSel === i ? ' sel' : '') + (ahora === i ? ' ahora' : '');
      b.dataset.pos = i; b.dataset.id = id; b.style.backgroundImage = "url('img/" + id + ".jpg')";
      b.innerHTML = '<span>' + esc(id) + '</span>';
      b.setAttribute('aria-label', 'Página ' + (i + 1) + ': carta ' + id);
      b.addEventListener('click', function(){
        if (folioTimer) return;
        if (folioSel === null) folioSel = i;
        else if (folioSel !== i) { var x = lista[i]; lista[i] = lista[folioSel]; lista[folioSel] = x; folioSel = null; }
        else folioSel = null;
        pintarFolio(-1);
      });
      t.appendChild(b);
    });
    $('hjVisor').style.backgroundImage = "url('img/" + lista[Math.max(0, ahora)] + ".jpg')";
  }
  function reproducirFolio(){
    if (folioTimer || !folioActual) return;
    var lista = FOLIO[folioActual], i = 0;
    function paso(){
      if (i >= lista.length) { folioTimer = null; pintarFolio(-1); return; }
      pintarFolio(i); i++;
      folioTimer = setTimeout(paso, 650);
    }
    folioSel = null; paso();
  }
  function cerrarFolio(){ clearTimeout(folioTimer); folioTimer = null; folioActual = null; $('hojear').hidden = true; }
  $('hjPlay').addEventListener('click', reproducirFolio);
  $('hjCerrar').addEventListener('click', cerrarFolio);
  document.addEventListener('keydown', function(e){ if (e.key === 'Escape' && !$('hojear').hidden) cerrarFolio(); });

"""

CAMBIOS = [
    ("  #zVoltear[hidden]{display:none}\n", "  #zVoltear[hidden]{display:none}\n" + CSS),
    ('<div id="zoom" hidden role="dialog"', HTML + '<div id="zoom" hidden role="dialog"'),
    ("      cont.appendChild(b);\n    });\n  }\n  function barajaInicial(c){", "      cont.appendChild(b);\n    });\n    pintarFolioscopios();\n  }\n  function barajaInicial(c){"),
    ("  fetchCartas().then(", JS + "  fetchCartas().then("),
]


def main():
    for ruta in sorted(glob.glob("juegos/el-faro/pc.html") + glob.glob("juegos/aventuras-ca/*/pc.html")):
        txt = open(ruta, encoding="utf-8").read()
        if "pintarFolioscopios" in txt:
            print("ya estaba:", ruta)
            continue
        for viejo, nuevo in CAMBIOS:
            assert txt.count(viejo) == 1, f"{ruta}: no encuentro {viejo[:70]!r}"
            txt = txt.replace(viejo, nuevo)
        open(ruta, "w", encoding="utf-8", newline="\n").write(txt)
        print("parcheado:", ruta)


if __name__ == "__main__":
    main()
