"""Prepara la parte «app instalable» (PWA): sw.js con versión automática y la lista de ficheros de cada juego para jugar sin conexión.

Uso (desde la raíz del repo, después de cambiar cualquier fichero del sitio):  python herramientas/generar_pwa.py

- Escribe `juegos/<ruta>/precache.json` por juego (lo que descarga el botón «Descargar para jugar sin conexión»).
- Escribe `sw.js` a partir de `herramientas/sw_plantilla.js`. La VERSIÓN es un hash del contenido del cascarón y de todas las listas:
  si cambia cualquier fichero, cambia la versión y los móviles reciben los ficheros nuevos (borran la caché vieja).
- Con --comprobar solo avisa si hay algo desfasado (sale con 1), para usarlo en las pruebas.
"""
import glob
import hashlib
import json
import os
import re
import sys

RAIZ_SITIO_CASCARON = [
    "./", "index.html", "perfil.html", "instalar.html", "ajustes.html", "manifest.webmanifest",
    "assets/css/style.css", "assets/css/menu.css", "assets/css/cuenta.css", "assets/css/barra.css",
    "assets/js/menu.js", "assets/js/ajustes.js", "assets/js/barra.js", "assets/js/splash.js", "assets/js/cuenta.js", "assets/js/cuenta-ui.js", "assets/js/accesos.js", "assets/js/filtro-juegos.js", "assets/js/pwa.js", "assets/js/vendor/supabase.js",
    "assets/images/logo.png", "assets/images/faro.jpg",
    "assets/icons/icon-192.png", "assets/icons/icon-512.png", "assets/icons/apple-touch-icon.png", "assets/icons/favicon.png",
    "juegos/catalogo.json", "juegos/aventuras-ca/index.html",
]
EXT_JUEGO = (".html", ".js", ".css", ".json", ".jpg", ".jpeg", ".png", ".webp", ".svg")
EXCLUIR = ("arte/", "precache.json", "MANUAL", "PENDIENTE", "prompts.html", "LEEME", "__pycache__", "video/")


def carpetas_juego():
    return ["juegos/el-faro"] + sorted(d.replace("\\", "/").rstrip("/") for d in glob.glob("juegos/aventuras-ca/*/") if os.path.exists(os.path.join(d, "cartas.json")))


def lista_juego(carpeta):
    carpeta = carpeta.rstrip("/")
    cola = []
    for dp, dn, fn in os.walk(carpeta):
        dn[:] = [x for x in dn if not x.startswith(".")]  # carpetas ocultas (p. ej. un perfil de Chrome local): nunca al precache
        for f in sorted(fn):
            ruta = os.path.join(dp, f).replace("\\", "/")
            rel = ruta[len(carpeta) + 1:]
            if any(x in rel for x in EXCLUIR) or not f.lower().endswith(EXT_JUEGO):
                continue
            cola.append(ruta)
    return sorted(cola)


def sha(rutas):
    h = hashlib.sha1()
    for r in rutas:
        h.update(r.encode())
        try:
            h.update(open(r, "rb").read().replace(b"\r\n", b"\n"))
        except FileNotFoundError:
            h.update(b"?")
    return h.hexdigest()[:10]


def main(comprobar=False):
    desfase = False
    todas = []
    for c in carpetas_juego():
        lista = lista_juego(c)
        todas += lista
        nuevo = json.dumps(lista, ensure_ascii=False, indent=1) + "\n"
        ruta = f"{c}/precache.json"
        actual = open(ruta, encoding="utf-8").read().replace("\r\n", "\n") if os.path.exists(ruta) else ""
        if nuevo != actual:
            desfase = True
            if not comprobar:
                open(ruta, "w", encoding="utf-8", newline="\n").write(nuevo)
        mb = sum(os.path.getsize(r) for r in lista) / 1e6
        print(f"{c}: {len(lista)} ficheros, {mb:.1f} MB")
    casc = [x for x in RAIZ_SITIO_CASCARON]
    version = sha([x for x in casc if x not in ("./",) and os.path.exists(x)] + sorted(todas))
    plantilla = open("herramientas/sw_plantilla.js", encoding="utf-8").read()
    sw = plantilla.replace("__VERSION__", version).replace("__CASCARON__", json.dumps(casc, ensure_ascii=False))
    actual = open("sw.js", encoding="utf-8").read().replace("\r\n", "\n") if os.path.exists("sw.js") else ""
    if sw != actual:
        desfase = True
        if not comprobar:
            open("sw.js", "w", encoding="utf-8", newline="\n").write(sw)
    print("versión del service worker:", version)
    if comprobar and desfase:
        print("DESFASADO: ejecuta python herramientas/generar_pwa.py")
        sys.exit(1)


if __name__ == "__main__":
    main("--comprobar" in sys.argv)
