"""Hace una captura (tamaño móvil) de CADA minijuego de un juego y las junta en una hoja de contactos.

Uso (desde la raíz del repo, con un servidor local en marcha):
    python herramientas/capturar_minijuegos.py http://127.0.0.1:8880 juegos/aventuras-ca/egipto SALIDA_DIR

Escribe SALIDA_DIR/<carta>.png y SALIDA_DIR/_hoja.png. Sirve para revisar de un vistazo el aspecto de todos los
minijuegos (ambientación, fondos, desbordes de texto) y para comparar antes y después de un cambio visual.
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bot_core import By, abrir_app, abrir_carta, cerrar  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402
from selenium import webdriver  # noqa: E402


def main(base, carpeta, salida):
    os.makedirs(salida, exist_ok=True)
    datos = json.load(open(os.path.join(carpeta, "cartas.json"), encoding="utf-8"))
    apps = [k for k, c in datos.items() if k != "_meta" and c.get("tipo") == "verde"]
    o = webdriver.ChromeOptions()
    o.add_argument("--headless=new")
    o.add_argument("--window-size=430,900")
    d = webdriver.Chrome(options=o)
    hechas = []
    try:
        abrir_app(d, f"{base}/{carpeta}/index.html")
        for k in apps:
            try:
                abrir_carta(d, k)
                time.sleep(1.0)
                d.save_screenshot(os.path.join(salida, f"{k}.png"))
                hechas.append(k)
            except Exception as e:  # noqa: BLE001
                print(f"  ! carta {k}: {type(e).__name__}: {str(e)[:120]}")
            cerrar(d)
    finally:
        d.quit()
    if hechas:
        W, H, cols = 260, 540, 4
        filas = (len(hechas) + cols - 1) // cols
        hoja = Image.new("RGB", (cols * W, filas * H), (15, 15, 15))
        dib = ImageDraw.Draw(hoja)
        for n, k in enumerate(hechas):
            im = Image.open(os.path.join(salida, f"{k}.png")).convert("RGB").resize((W, H))
            hoja.paste(im, ((n % cols) * W, (n // cols) * H))
            dib.text(((n % cols) * W + 6, (n // cols) * H + 6), k, fill=(255, 255, 0))
        hoja.save(os.path.join(salida, "_hoja.png"))
    print(f"{carpeta}: {len(hechas)}/{len(apps)} minijuegos fotografiados -> {salida}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
