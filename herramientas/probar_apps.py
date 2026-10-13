"""Resuelve por la interfaz real los minijuegos de un juego (sin jugar la partida entera) y muestra el mensaje de cada uno.

Uso (desde la raíz del repo, con un servidor local en marcha):
    python herramientas/probar_apps.py http://127.0.0.1:8890 juegos/el-faro solvers_faro [70 95 ...]

Sirve para probar rápido un minijuego tras tocar su aspecto. Falla si algún solucionador no consigue resolverlo o si hay
errores de consola (fuera de vídeo y favicon).
"""
import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bot_core import abrir_app, cerrar, nuevo_driver  # noqa: E402


def main(base, carpeta, modulo, cartas):
    solv = importlib.import_module(modulo)
    cartas = cartas or list(solv.SOLVERS)
    d = nuevo_driver()
    malos = 0
    try:
        abrir_app(d, f"{base}/{carpeta}/index.html")
        for k in cartas:
            try:
                msg = solv.SOLVERS[k](d)
                print(f"[{k}] OK -> {msg[:110]}")
            except Exception as e:  # noqa: BLE001
                malos += 1
                print(f"[{k}] FALLO -> {type(e).__name__}: {str(e)[:300]}")
                cerrar(d)
        errs = [e["message"][:200] for e in d.get_log("browser")
                if e["level"] == "SEVERE" and "videoInicial" not in e["message"] and "favicon" not in e["message"]]
        print("errores de consola:", errs)
        malos += len(errs)
    finally:
        d.quit()
    sys.exit(1 if malos else 0)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:])
