"""Captura cómo se ve cada minijuego (la ventana de la app) para revisar su aspecto.
Uso:  python herramientas/capturar_apps.py URL carpeta_juego carpeta_salida carta [carta ...]
(con servidor propio:  python herramientas/con_servidor.py python herramientas/capturar_apps.py {URL} juegos/aventuras-ca/juguetes <salida> 14 20 )"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bot_core import abrir_app, abrir_carta, cerrar, nuevo_driver  # noqa: E402


def main(base, carpeta, salida, cartas):
    os.makedirs(salida, exist_ok=True)
    d = nuevo_driver()
    try:
        d.set_window_size(430, 900)
        abrir_app(d, f"{base}/{carpeta}/index.html")
        for c in cartas:
            try:
                abrir_carta(d, c)
                time.sleep(1.8)
                ruta = os.path.join(salida, f"{os.path.basename(carpeta)}-{c}.png")
                d.save_screenshot(ruta)
                print("ok", ruta)
            except Exception as e:  # noqa: BLE001
                print("fallo", c, type(e).__name__, str(e)[:120])
            cerrar(d)
    finally:
        d.quit()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:])
