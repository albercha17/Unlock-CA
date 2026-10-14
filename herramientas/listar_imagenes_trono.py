"""Actualiza `img/ui/disponibles.json` de «Trono»: la lista de dibujos de los minijuegos que existen de verdad.

Uso (desde la raíz del repo): python herramientas/listar_imagenes_trono.py [carpeta_del_juego]

Los minijuegos de «Trono» (juegos/aventuras-ca/trono/minijuegos/comun.js) usan un dibujo de `img/ui/` solo si está en esta lista: así no se
piden ficheros que todavía no existen (404 en la consola). Después de generar imágenes (herramientas/chatgpt_fondos.py --solo trono) ejecuta
este script y haz commit de `disponibles.json`. La lista incluye subcarpetas (`escudos/lobo.jpg`) y deja fuera `panel.jpg`, que es la textura
base del panel y la crea construir_aventuras.py.
"""
import json
import os
import random
import sys

from PIL import Image

carpeta = sys.argv[1] if len(sys.argv) > 1 else "juegos/aventuras-ca/trono"
ui = os.path.join(carpeta, "img", "ui")
os.makedirs(ui, exist_ok=True)
# pergamino provisional (la textura real se genera con ChatGPT; el lector de la crónica y la profecía lo usan de fondo)
papel = os.path.join(ui, "papel.jpg")
if not os.path.exists(papel):
    rng = random.Random(3)
    im = Image.new("RGB", (96, 128))
    px = im.load()
    for y in range(128):
        for x in range(96):
            g = rng.randint(-6, 6)
            px[x, y] = (min(255, 232 + g - y // 18), min(255, 214 + g - y // 14), min(255, 170 + g - y // 10))
    im.save(papel, quality=75)

nombres = []
for raiz, _dirs, ficheros in os.walk(ui):
    for f in ficheros:
        if f.lower().endswith((".jpg", ".png", ".webp")) and not (raiz == ui and f in ("panel.jpg", "papel.jpg")):
            nombres.append(os.path.relpath(os.path.join(raiz, f), ui).replace(os.sep, "/"))
nombres.sort()
with open(os.path.join(ui, "disponibles.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(nombres, f, ensure_ascii=False)
print(len(nombres), "dibujos de minijuegos listados en", os.path.join(ui, "disponibles.json"))
