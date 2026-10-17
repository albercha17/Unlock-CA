"""Producción automática de los pedidos de la tienda (botón «Desarrollarlo» del panel tienda/admin.html).

Busca en Supabase los pedidos en estado «desarrollar» o «en_produccion» y, para cada uno:
  1. Descarga los datos y las fotos de los protagonistas (a una carpeta privada, fuera del repo).
  2. Monta un mini-sitio con las 4 aventuras elegidas, cambiando Cristina y Alberto por los protagonistas.
  3. Crea la hoja de personajes con las fotos (ChatGPT) y la sube al panel como ilustración de prueba.
  4. Genera con ChatGPT las ilustraciones de las cartas en las que salen personajes (las demás se reutilizan).
     Si ChatGPT pone límite de imágenes, para y sigue en la siguiente ejecución.
  5. Publica el pack en Netlify (una web por pedido) y deja el pedido «listo» con el enlace.

Lo lanza cada 10 minutos una tarea programada de Windows (ver --instalar). Se puede ejecutar a mano:
    python herramientas/tienda/produccion.py                    # procesa los pedidos pendientes
    python herramientas/tienda/produccion.py --simular          # sin ChatGPT: reutiliza las ilustraciones (pruebas)
    python herramientas/tienda/produccion.py --local CARPETA --simular --sin-publicar
                                                                # pedido de prueba sin Supabase: CARPETA/datos.json + fotos/
    python herramientas/tienda/produccion.py --instalar         # crea la configuración y la tarea programada

Configuración privada (NO va en el repo): %USERPROFILE%/.cronoportal/config.json
    {"supabase_url": "...", "service_key": "sb_secret_...", "netlify_token": "nfp_...", "carpeta": "..."}
Registro: %USERPROFILE%/.cronoportal/produccion.log
"""
import argparse
import io
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import time
import traceback
import urllib.error
import urllib.request
import zipfile
from datetime import datetime
from pathlib import Path

CONFIG_DIR = Path.home() / ".cronoportal"
LOG = CONFIG_DIR / "produccion.log"
CONFIG_DIR.mkdir(exist_ok=True)
if sys.stdout is None:  # pythonw (tarea programada): sin consola, todo al registro
    sys.stdout = sys.stderr = open(LOG, "a", encoding="utf-8", buffering=1)
else:
    sys.stdout.reconfigure(encoding="utf-8")

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "herramientas"))

AVENTURAS = RAIZ / "juegos" / "aventuras-ca"
ORIGINALES = ("Cristina", "Alberto")          # huecos de las historias: [0] la protagonista, [1] el protagonista
NO_COPIAR = {"arte", "video", "MANUAL.md", "prompts.html", "precache.json", "__pycache__"}
EXT_TEXTO = (".html", ".js", ".json", ".css", ".md", ".txt")
PUERTO_CHROME = 9222
# carpeta privada de los pedidos (fotos, hoja, ilustraciones): fuera del repo y de la copia que se actualiza sola
_UNLOCK = Path.home() / "Documents" / "MIS PROGRAMAS" / "Unlock"
CARPETA_PEDIDOS = (_UNLOCK if _UNLOCK.exists() else CONFIG_DIR) / "pedidos-tienda"


def log(*a):
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), *a, flush=True)


# ---------------------------------------------------------------- configuración

def leer_config():
    ruta = CONFIG_DIR / "config.json"
    cfg = json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else {}
    cfg.setdefault("supabase_url", "https://tomwaoskswxfbwxsrkkl.supabase.co")
    cfg.setdefault("carpeta", str(CARPETA_PEDIDOS))
    return cfg


# ---------------------------------------------------------------- Supabase (REST, con la clave secreta)

class Supabase:
    def __init__(self, cfg):
        if not cfg.get("service_key"):
            sys.exit(f"Falta service_key en {CONFIG_DIR / 'config.json'}")
        self.url = cfg["supabase_url"].rstrip("/")
        self.key = cfg["service_key"]

    def _pedir(self, metodo, ruta, cuerpo=None, cabeceras=None, crudo=False):
        h = {"apikey": self.key}
        if self.key.startswith("eyJ"):  # clave antigua (JWT): también en Authorization
            h["Authorization"] = f"Bearer {self.key}"
        h.update(cabeceras or {})
        datos = cuerpo if isinstance(cuerpo, (bytes, type(None))) else json.dumps(cuerpo).encode()
        if cuerpo is not None and not isinstance(cuerpo, bytes):
            h.setdefault("Content-Type", "application/json")
        req = urllib.request.Request(self.url + ruta, data=datos, headers=h, method=metodo)
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                b = r.read()
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"Supabase {metodo} {ruta}: {e.code} {e.read().decode(errors='replace')[:300]}") from None
        return b if crudo else (json.loads(b) if b else None)

    def pendientes(self):
        return self._pedir("GET", "/rest/v1/tienda_pedidos?estado=in.(desarrollar,en_produccion)&order=creado.asc&select=*")

    def cambiar(self, pid, **campos):
        self._pedir("PATCH", f"/rest/v1/tienda_pedidos?id=eq.{pid}", campos, {"Prefer": "return=minimal"})

    def bajar_foto(self, ruta):
        return self._pedir("GET", f"/storage/v1/object/tienda-fotos/{ruta}", crudo=True)

    def subir_foto(self, ruta, datos):
        self._pedir("POST", f"/storage/v1/object/tienda-fotos/{ruta}", datos,
                    {"Content-Type": "image/jpeg", "x-upsert": "true"})


class SinSupabase:
    """Para --local: imprime lo que se mandaría a Supabase."""
    def cambiar(self, pid, **campos):
        log(f"[local] pedido {pid[:8]} →", campos)

    def subir_foto(self, ruta, datos):
        log(f"[local] subiría {ruta} ({len(datos) // 1024} KB)")


# ---------------------------------------------------------------- 1. datos y fotos

def descargar(sb, pedido, carpeta):
    (carpeta / "fotos").mkdir(parents=True, exist_ok=True)
    (carpeta / "datos.json").write_text(json.dumps(pedido, ensure_ascii=False, indent=1), encoding="utf-8")
    for pr in pedido["protagonistas"]:
        for ruta in pr.get("fotos", []):
            destino = carpeta / "fotos" / Path(ruta).name
            if not destino.exists():
                destino.write_bytes(sb.bajar_foto(ruta))


def fotos_de(carpeta, prota):
    return [carpeta / "fotos" / Path(r).name for r in prota.get("fotos", [])]


def repartir(protagonistas):
    """Coloca a cada protagonista en el hueco de Cristina (ella) o Alberto (él) según su género."""
    protas = list(protagonistas)[:2]
    fem = lambda p: p.get("genero") in ("mujer", "niña")  # noqa: E731
    if len(protas) == 2 and not fem(protas[0]) and fem(protas[1]):
        protas.reverse()
    return protas


# ---------------------------------------------------------------- 2. mini-sitio personalizado

def descripcion(prota, original):
    """Nueva descripción del personaje: datos del cliente + la ropa de la aventura (lo que va tras «Lleva/Viste»)."""
    m = re.search(r"\b(Lleva|Viste)\b.*$", original)
    ropa = m.group(0) if m else ""
    quien = {"mujer": "mujer", "hombre": "hombre", "niña": "niña", "niño": "niño"}.get(prota.get("genero"), "persona")
    edad = re.sub(r"\D", "", str(prota.get("edad") or ""))
    partes = [f"{prota['nombre']}, " + ("versión de dibujos animados 2D clásicos: " if "dibujos animados" in original else "")
              + quien + (f" de unos {edad} años" if edad else "")]
    if prota.get("sobre"):
        partes.append(prota["sobre"].strip().rstrip("."))
    texto = ", ".join(partes) + ". Su cara, pelo y rasgos son exactamente los de la hoja de personajes adjunta."
    return f"{texto} {ropa}".strip()


def cambiar_nombres(texto, nombres):
    for i, original in enumerate(ORIGINALES):
        texto = re.sub(rf"\b{original}\b", f"\x00{i}\x00", texto)
    for i, nombre in enumerate(nombres):
        texto = texto.replace(f"\x00{i}\x00", nombre)
    return texto


def montar_sitio(pedido, protas, sitio):
    nombres = [p["nombre"].strip() for p in protas]
    catalogo = {c["id"]: c for c in json.loads((RAIZ / "juegos" / "catalogo.json").read_text(encoding="utf-8"))}
    if not (sitio / "assets").exists():
        shutil.copytree(RAIZ / "assets", sitio / "assets")
        for f in (sitio / "assets").rglob("*.js"):
            texto = f.read_text(encoding="utf-8", errors="ignore")
            if any(o in texto for o in ORIGINALES):
                f.write_text(cambiar_nombres(texto, nombres), encoding="utf-8")
    for aventura in pedido["aventuras"]:
        origen, destino = AVENTURAS / aventura, sitio / "juegos" / "aventuras-ca" / aventura
        for f in origen.rglob("*"):
            rel = f.relative_to(origen)
            if rel.parts[0] in NO_COPIAR or f.is_dir():
                continue
            d = destino / rel
            if rel.parts[0] == "img" and d.exists() and rel.name != "pendientes.json":
                continue  # no pisar las ilustraciones ya personalizadas
            d.parent.mkdir(parents=True, exist_ok=True)
            if f.suffix.lower() in EXT_TEXTO:
                d.write_text(cambiar_nombres(f.read_text(encoding="utf-8"), nombres), encoding="utf-8")
            else:
                shutil.copy2(f, d)
        # descripciones de los personajes para las ilustraciones
        cj = destino / "cartas.json"
        datos = json.loads((origen / "cartas.json").read_text(encoding="utf-8"))
        meta = {k: cambiar_nombres(v, nombres) if isinstance(v, str) else v for k, v in datos["_meta"].items()}
        meta["personajes"] = {p["nombre"].strip(): descripcion(p, meta["personajes"][o]) for p, o in zip(protas, ORIGINALES)}
        texto = cambiar_nombres(json.dumps({k: v for k, v in datos.items() if k != "_meta"}, ensure_ascii=False), nombres)
        datos = {"_meta": meta, **json.loads(texto)}
        cj.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
    escribir_menu(pedido, nombres, catalogo, sitio)


def esc(t):
    return str(t or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def escribir_menu(pedido, nombres, catalogo, sitio):
    quienes = " y ".join(nombres)
    tarjetas = "".join(f"""
      <article class="av">
        <img src="{a}/img/P.jpg" alt="">
        <div><h2>{esc(catalogo.get(a, {}).get('nombre', a))}</h2>
          <p class="meta">{catalogo.get(a, {}).get('minutos', 60)} min · {catalogo.get(a, {}).get('cartas', '')} cartas</p>
          <p class="botones"><a class="btn" href="{a}/index.html">Jugar con el móvil</a>
          <a class="btn sec" href="{a}/imprimir.html">Cartas para imprimir</a>
          <a class="btn sec" href="{a}/pc.html">Jugar en pantalla</a></p></div>
      </article>""" for a in pedido["aventuras"])
    dedicatoria = f'<p class="dedicatoria">«{esc(pedido.get("dedicatoria"))}»</p>' if pedido.get("dedicatoria") else ""
    html = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow"><title>Las aventuras de {esc(quienes)}</title>
<link rel="icon" type="image/png" href="../../assets/icons/favicon.png">
<link rel="manifest" href="../../manifest.webmanifest">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,700&family=Poppins:wght@400;600&display=swap" rel="stylesheet">
<style>
:root{{--oro:#e9b65c;--texto:#f4efe6;--suave:rgba(244,239,230,.72)}}
*{{box-sizing:border-box}}body{{margin:0;font-family:Poppins,system-ui,sans-serif;color:var(--texto);background:radial-gradient(900px 500px at 80% -10%,rgba(233,182,92,.16),transparent 60%),#0b0a12;line-height:1.55}}
main{{max-width:900px;margin:0 auto;padding:40px 16px 60px}}h1,h2{{font-family:Fraunces,Georgia,serif;margin:0}}h1{{font-size:clamp(1.9rem,6vw,2.8rem)}}
.eyebrow{{color:var(--oro);letter-spacing:.16em;text-transform:uppercase;font-size:.75rem;font-weight:600;margin:0 0 8px}}
.dedicatoria{{font-family:Fraunces,Georgia,serif;font-style:italic;font-size:1.15rem;color:var(--oro);margin:18px 0 0}}
.intro{{color:var(--suave)}}.lista{{display:grid;gap:18px;margin-top:30px}}
.av{{display:grid;grid-template-columns:150px 1fr;gap:18px;background:rgba(255,255,255,.045);border:1px solid rgba(255,255,255,.1);border-radius:18px;padding:14px;align-items:center}}
.av img{{width:100%;aspect-ratio:2/3;object-fit:cover;border-radius:12px}}.av h2{{font-size:1.3rem}}.meta{{color:var(--suave);font-size:.9rem;margin:4px 0 12px}}
.botones{{display:flex;flex-wrap:wrap;gap:8px;margin:0}}.btn{{display:inline-block;padding:10px 16px;border-radius:999px;background:linear-gradient(135deg,#ffd88f,var(--oro));color:#2a1a04;font-weight:600;text-decoration:none;font-size:.92rem}}
.btn.sec{{background:transparent;color:var(--texto);border:1px solid rgba(255,255,255,.25)}}
@media(max-width:560px){{.av{{grid-template-columns:96px 1fr}}}}
</style></head><body><main>
<p class="eyebrow">Cronoportal · vuestras aventuras</p>
<h1>Las aventuras de {esc(quienes)}</h1>{dedicatoria}
<p class="intro">Cuatro saltos con el Cronoportal. Imprimid las cartas (o usad el modo pantalla), abrid la aventura en el móvil y pulsad «Empezar»: la app lleva el tiempo, da pistas y tiene los minijuegos.</p>
<div class="lista">{tarjetas}
</div></main></body></html>
"""
    (sitio / "juegos" / "aventuras-ca" / "index.html").write_text(html, encoding="utf-8")
    (sitio / "index.html").write_text('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=juegos/aventuras-ca/">'
                                      '<meta name="robots" content="noindex"><a href="juegos/aventuras-ca/">Entrar</a>', encoding="utf-8")
    manifest = {"name": f"Aventuras de {quienes}", "short_name": "Cronoportal", "start_url": "./juegos/aventuras-ca/",
                "display": "standalone", "background_color": "#0b0a12", "theme_color": "#0b0a12",
                "icons": [{"src": "assets/icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
                          {"src": "assets/icons/icon-512.png", "sizes": "512x512", "type": "image/png"}]}
    (sitio / "manifest.webmanifest").write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    # service worker mínimo (pwa.js lo registra): red primero y copia en caché para jugar sin conexión
    (sitio / "sw.js").write_text("""const CACHE = 'pack-v1';
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', (e) => e.waitUntil(self.clients.claim()));
self.addEventListener('message', (e) => { if (e.data && e.data.tipo === 'saltar') self.skipWaiting(); });
self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET' || new URL(e.request.url).origin !== location.origin) return;
  e.respondWith(fetch(e.request).then((r) => {
    if (r.ok) { const copia = r.clone(); caches.open(CACHE).then((c) => c.put(e.request, copia)); }
    return r;
  }).catch(() => caches.match(e.request)));
});
""", encoding="utf-8")
    (sitio / "_headers").write_text("/*\n  X-Robots-Tag: noindex, nofollow\n", encoding="utf-8")


def cartas_con_personajes(juego):
    datos = json.loads((juego / "cartas.json").read_text(encoding="utf-8"))
    meta = datos.pop("_meta")
    return sorted((k for k, v in datos.items() if any(n in v.get("arte", "") for n in meta["personajes"])),
                  key=lambda k: (0, 0) if k == "P" else (1, int(k)))


def faltan(sitio, aventuras):
    res = {}
    for a in aventuras:
        juego = sitio / "juegos" / "aventuras-ca" / a
        res[a] = [i for i in cartas_con_personajes(juego) if not (juego / "arte" / f"{i}.png").exists()]
    return res


# ---------------------------------------------------------------- 3 y 4. ChatGPT

def prompt_hoja(protas, n_fotos):
    partes, inicio = [], 1
    for p, n in zip(protas, n_fotos):
        rango = f"la foto {inicio}" if n == 1 else f"las fotos {inicio} a {inicio + n - 1}"
        quien = p.get("genero") or "persona"
        edad = re.sub(r"\D", "", str(p.get("edad") or ""))
        partes.append(f"{rango} son de {p['nombre']} ({quien}" + (f", unos {edad} años" if edad else "") + ")")
        inicio += n
    p = ("Crea una imagen: hoja de personajes (character sheet) con las dos personas de las fotos adjuntas: "
         + "; ".join(partes) + ". De cuerpo entero y de frente, una al lado de la otra, sobre fondo claro y neutro. "
         "Mantén su parecido real con las fotos (cara, forma de la cara, pelo, ojos, barba si la tiene, gafas si las lleva). "
         "Ropa actual y cómoda: vaqueros, zapatillas y una chaqueta ligera. "
         "Estilo: ilustración digital pintada con estética de película de aventuras, trazo limpio y colores naturales, "
         "formato vertical 2:3. Sin ningún texto ni letras en la imagen.")
    return " ".join(p.split())


def chrome_abierto():
    with socket.socket() as s:
        s.settimeout(1)
        return s.connect_ex(("127.0.0.1", PUERTO_CHROME)) == 0


def abrir_chat():
    import chatgpt_imagenes as ci
    if not chrome_abierto():
        log("Abriendo Chrome con ChatGPT...")
        subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
                        str(RAIZ / "herramientas" / "abrir_chrome_chatgpt.ps1")], check=False)
        for _ in range(40):
            if chrome_abierto():
                break
            time.sleep(1)
        time.sleep(5)
    return ci.Chat(PUERTO_CHROME)


class ChatSimulado:
    """--simular: no usa ChatGPT; la hoja es un collage de las fotos y las cartas reutilizan su ilustración."""


def hacer_hoja(chat, protas, carpeta):
    from PIL import Image
    hoja = carpeta / "hoja.png"
    if hoja.exists():
        return hoja
    fotos = [fotos_de(carpeta, p) for p in protas]
    if isinstance(chat, ChatSimulado):
        imgs = [Image.open(f[0]).convert("RGB").resize((512, 768)) for f in fotos]
        lienzo = Image.new("RGB", (1024, 768), "white")
        for i, im in enumerate(imgs):
            lienzo.paste(im, (512 * i, 0))
        lienzo.save(hoja)
        return hoja
    chat.nuevo_chat()
    for f in [x for lista in fotos for x in lista]:
        if not chat.adjuntar(f):
            raise RuntimeError(f"No pude adjuntar la foto {f.name} en ChatGPT")
    chat.enviar(prompt_hoja(protas, [len(f) for f in fotos]))
    src = chat.esperar_imagen()
    if not src:
        return None
    chat.descargar(src, hoja)
    return hoja


def ilustrar(chat, juego, ids, hoja):
    """Devuelve (hechas, seguir). seguir=False si ChatGPT ha puesto límite."""
    from PIL import Image
    if isinstance(chat, ChatSimulado):
        for i in ids:
            (juego / "arte").mkdir(exist_ok=True)
            Image.open(juego / "img" / f"{i}.jpg").convert("RGB").save(juego / "arte" / f"{i}.png")
        return len(ids), True
    import chatgpt_imagenes as ci
    ci.HOJA = hoja
    return ci.hacer_juego(chat, juego, ids, False)


def preparar_imagenes(juego):
    subprocess.run([sys.executable, str(RAIZ / "herramientas" / "preparar_imagenes.py"), str(juego)],
                   cwd=RAIZ, stdout=sys.stdout, stderr=sys.stderr, check=False)


# ---------------------------------------------------------------- 5. Netlify

def netlify(token, metodo, ruta, cuerpo=None, tipo="application/json"):
    datos = cuerpo if isinstance(cuerpo, (bytes, type(None))) else json.dumps(cuerpo).encode()
    req = urllib.request.Request("https://api.netlify.com/api/v1" + ruta, data=datos, method=metodo,
                                 headers={"Authorization": f"Bearer {token}", "Content-Type": tipo, "User-Agent": "cronoportal"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.loads(r.read() or b"null")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Netlify {metodo} {ruta}: {e.code} {e.read().decode(errors='replace')[:300]}") from None


def comprimir(sitio):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sitio.rglob("*"):
            rel = f.relative_to(sitio)
            if f.is_file() and "arte" not in rel.parts:
                z.write(f, rel.as_posix())
    return buf.getvalue()


def publicar(token, pedido, sitio, carpeta):
    info_ruta = carpeta / "netlify.json"
    info = json.loads(info_ruta.read_text(encoding="utf-8")) if info_ruta.exists() else None
    if not info:
        nombre = f"cronoportal-{pedido['id'][:8]}-{os.urandom(3).hex()}"
        info = netlify(token, "POST", "/sites", {"name": nombre})
        info = {"id": info["id"], "url": info.get("ssl_url") or info["url"]}
        info_ruta.write_text(json.dumps(info), encoding="utf-8")
    dep = netlify(token, "POST", f"/sites/{info['id']}/deploys", comprimir(sitio), "application/zip")
    for _ in range(60):
        if dep.get("state") == "ready":
            break
        if dep.get("state") == "error":
            raise RuntimeError(f"Netlify no pudo publicar: {dep.get('error_message')}")
        time.sleep(5)
        dep = netlify(token, "GET", f"/deploys/{dep['id']}")
    return info["url"]


# ---------------------------------------------------------------- un pedido

def producir(sb, cfg, pedido, chat_fabrica, publicar_web=True):
    pid, codigo = pedido["id"], pedido["id"][:8].upper()
    carpeta = Path(cfg["carpeta"]) / codigo
    sitio = carpeta / "sitio"
    avisar = lambda texto, **extra: (log(f"[{codigo}] {texto}"), sb.cambiar(pid, progreso=texto, **extra))  # noqa: E731

    if pedido["estado"] == "desarrollar":
        avisar("Empezando: descargo las fotos y preparo las 4 aventuras.", estado="en_produccion")
    if not isinstance(sb, SinSupabase):
        descargar(sb, pedido, carpeta)
    protas = repartir(pedido["protagonistas"])
    montar_sitio(pedido, protas, sitio)

    pendientes = faltan(sitio, pedido["aventuras"])
    total = sum(len(cartas_con_personajes(sitio / "juegos" / "aventuras-ca" / a)) for a in pedido["aventuras"])
    if any(pendientes.values()) or not (carpeta / "hoja.png").exists():
        chat = chat_fabrica()
        if not (carpeta / "hoja.png").exists():
            avisar("Creando la hoja de personajes con las fotos (ChatGPT)...")
        hoja = hacer_hoja(chat, protas, carpeta)
        if not hoja:
            avisar("Esperando cupo de ChatGPT para la hoja de personajes. Seguirá solo más tarde.")
            return False
        from PIL import Image
        jpg = io.BytesIO()
        Image.open(hoja).convert("RGB").save(jpg, "JPEG", quality=85)
        sb.subir_foto(f"{pid}/hoja.jpg", jpg.getvalue())

        for a, ids in pendientes.items():
            if not ids:
                continue
            hechas_antes = total - sum(len(v) for v in faltan(sitio, pedido["aventuras"]).values())
            avisar(f"Ilustrando {a}: {hechas_antes}/{total} ilustraciones hechas.")
            juego = sitio / "juegos" / "aventuras-ca" / a
            hechas, seguir = ilustrar(chat, juego, ids, hoja)
            if hechas:
                preparar_imagenes(juego)
            if not seguir:
                hechas_ya = total - sum(len(v) for v in faltan(sitio, pedido["aventuras"]).values())
                avisar(f"Esperando cupo de ChatGPT: {hechas_ya}/{total} ilustraciones hechas. Seguirá solo más tarde.")
                return False
        restantes = sum(len(v) for v in faltan(sitio, pedido["aventuras"]).values())
        if restantes:
            avisar(f"Quedan {restantes} ilustraciones que no salieron; lo reintento en la próxima vuelta.")
            return False

    if publicar_web and cfg.get("netlify_token"):
        avisar(f"Publicando el pack ({total} ilustraciones con los protagonistas)...")
        url = publicar(cfg["netlify_token"], pedido, sitio, carpeta)
        avisar(f"Listo: {total} ilustraciones con los protagonistas. Revisa el pack y mándaselo al cliente.",
               estado="listo", entrega_url=url)
    else:
        avisar(f"Listo en tu PC (sin publicar): {sitio}", estado="listo")
    return True


# ---------------------------------------------------------------- instalación

def instalar():
    cfg_ruta = CONFIG_DIR / "config.json"
    if not cfg_ruta.exists():
        cfg_ruta.write_text(json.dumps({"supabase_url": "https://tomwaoskswxfbwxsrkkl.supabase.co", "service_key": "",
                                        "netlify_token": "", "carpeta": str(CARPETA_PEDIDOS)}, indent=1),
                            encoding="utf-8")
        print(f"Configuración creada: {cfg_ruta} (rellena service_key y netlify_token)")
    lanzador = CONFIG_DIR / "lanzador.py"
    shutil.copy2(Path(__file__).with_name("lanzador.py"), lanzador)
    pythonw = Path(sys.executable).with_name("pythonw.exe")
    ps = f"""
$accion = New-ScheduledTaskAction -Execute '{pythonw}' -Argument '"{lanzador}"' -WorkingDirectory '{CONFIG_DIR}'
$disparo = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 10)
$ajustes = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -StartWhenAvailable -DontStopIfGoingOnBatteries -AllowStartIfOnBatteries -ExecutionTimeLimit (New-TimeSpan -Hours 6)
Register-ScheduledTask -TaskName 'Cronoportal pedidos' -Action $accion -Trigger $disparo -Settings $ajustes -Force | Out-Null
'Tarea programada: Cronoportal pedidos (cada 10 minutos)'
"""
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)


# ---------------------------------------------------------------- principal

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--simular", action="store_true", help="sin ChatGPT (reutiliza las ilustraciones)")
    ap.add_argument("--local", help="carpeta con datos.json y fotos/ (sin Supabase)")
    ap.add_argument("--sin-publicar", action="store_true")
    ap.add_argument("--instalar", action="store_true")
    args = ap.parse_args()
    if args.instalar:
        return instalar()

    cfg = leer_config()
    cerrojo = CONFIG_DIR / "produccion.lock"
    if cerrojo.exists() and time.time() - cerrojo.stat().st_mtime < 6 * 3600:
        log("Otra ejecución sigue en marcha; salgo.")
        return
    cerrojo.write_text(str(os.getpid()))
    chat = {}
    fabrica = (lambda: chat.setdefault("c", ChatSimulado())) if args.simular else (lambda: chat.setdefault("c", abrir_chat()))
    try:
        if args.local:
            carpeta = Path(args.local)
            pedido = json.loads((carpeta / "datos.json").read_text(encoding="utf-8"))
            cfg["carpeta"] = str(carpeta.parent)
            producir(SinSupabase(), cfg, pedido, fabrica, not args.sin_publicar)
            return
        sb = Supabase(cfg)
        for pedido in sb.pendientes():
            try:
                if not producir(sb, cfg, pedido, fabrica, not args.sin_publicar):
                    break  # sin cupo de ChatGPT: los siguientes tampoco podrían avanzar
            except SystemExit as e:  # chatgpt_imagenes sale así si no hay sesión de ChatGPT
                sb.cambiar(pedido["id"], progreso=f"Parado: {e}. Abre Chrome con ChatGPT e inicia sesión; seguirá solo.")
                break
            except Exception as e:  # noqa: BLE001
                log(traceback.format_exc())
                sb.cambiar(pedido["id"], progreso=f"Error: {e}. Lo reintento en la próxima vuelta.")
    finally:
        cerrojo.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
