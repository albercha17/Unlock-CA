"""Actualiza `img/ui/lista.json` de un juego: la lista de imágenes de los minijuegos que existen de verdad.

Uso (desde la raíz del repo): python herramientas/listar_imagenes_ui.py juegos/aventuras-ca/cuento

Los minijuegos de «Cuento» cargan una imagen de `img/ui/` solo si está en esa lista (así no hay peticiones 404 cuando todavía no se ha
generado). Después de generar imágenes con chatgpt_fondos.py/chatgpt_imagenes.py, ejecuta este script y haz commit de `lista.json`.
También crea una textura de papel provisional (`papel.jpg`) si falta.
"""
import json
import os
import sys

from PIL import Image

carpeta = sys.argv[1] if len(sys.argv) > 1 else "juegos/aventuras-ca/cuento"
ui = os.path.join(carpeta, "img", "ui")
os.makedirs(ui, exist_ok=True)

papel = os.path.join(ui, "papel.jpg")
if not os.path.exists(papel):
    # pergamino provisional: degradado cálido con un poco de grano
    import random
    rng = random.Random(3)
    im = Image.new("RGB", (96, 128))
    px = im.load()
    for y in range(128):
        for x in range(96):
            g = rng.randint(-6, 6)
            px[x, y] = (min(255, 236 + g - y // 18), min(255, 220 + g - y // 14), min(255, 178 + g - y // 10))
    im.save(papel, quality=75)

nombres = []
for raiz, _, ficheros in os.walk(ui):
    for f in ficheros:
        rel = os.path.relpath(os.path.join(raiz, f), ui).replace("\\", "/")
        if f.lower().endswith((".jpg", ".png", ".webp")) and rel not in ("panel.jpg", "papel.jpg"):
            nombres.append(rel)
nombres.sort()
with open(os.path.join(ui, "lista.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(nombres, f, ensure_ascii=False)
print(len(nombres), "imágenes de minijuegos listadas en", os.path.join(ui, "lista.json"))
