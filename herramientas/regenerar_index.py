"""Regenera la app de cada juego de Aventuras C&A (index.html, app.css, app.js, pistas.js) a partir de la plantilla del Faro.

Uso (desde la raíz del repo):
    python herramientas/regenerar_index.py            # escribe lo que cambia
    python herramientas/regenerar_index.py --probar   # solo informa de qué cambiaría
    python herramientas/regenerar_index.py Marte      # solo ese juego

El Faro (juegos/el-faro) es la fuente de verdad de la app: se edita ahí y se propaga con este script. El index.html de cada juego se
genera con su configuración (título, sinopsis, duración, minijuegos) de juegos_config.py.
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from juegos_config import FARO, JUEGOS, generar_index, leer, escribir  # noqa: E402

PROBAR = "--probar" in sys.argv
SOLO = [a.lower() for a in sys.argv[1:] if not a.startswith("--")]
COMUNES = ("app.css", "app.js", "pistas.js")
plantilla = leer(f"{FARO}/index.html")
cambios = 0
for nombre, cfg in JUEGOS.items():
    if SOLO and nombre.lower() not in SOLO:
        continue
    carpeta = f"juegos/aventuras-ca/{nombre.lower()}"
    ruta = f"{carpeta}/index.html"
    nuevo = generar_index(plantilla, cfg)
    actual = leer(ruta) if os.path.exists(ruta) else ""
    if nuevo != actual.replace("\r\n", "\n"):
        cambios += 1
        print(f"{nombre}: index.html " + ("cambiaría" if PROBAR else "actualizado"))
        if not PROBAR:
            escribir(ruta, nuevo)
    for extra in COMUNES:
        origen, destino = f"{FARO}/{extra}", f"{carpeta}/{extra}"
        if not os.path.exists(origen):
            continue
        igual = os.path.exists(destino) and open(origen, "rb").read().replace(b"\r\n", b"\n") == open(destino, "rb").read().replace(b"\r\n", b"\n")
        if not igual:
            cambios += 1
            print(f"{nombre}: {extra} " + ("cambiaría" if PROBAR else "actualizado"))
            if not PROBAR:
                shutil.copy(origen, destino)
print("cambios:", cambios)
