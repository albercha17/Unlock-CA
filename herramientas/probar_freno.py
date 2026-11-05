"""Comprueba el freno al ensayo y error: tras 6 respuestas malas seguidas en la puerta del Faro (carta 14), los botones se bloquean (salvo Cerrar).
Uso: python herramientas/con_servidor.py python herramientas/probar_freno.py {URL}"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bot_core import *  # noqa: E402,F401
from bot_core import abrir_app, abrir_carta, cerrar, feedback, nuevo_driver, tecla  # noqa: E402

d = nuevo_driver()
try:
    abrir_app(d, sys.argv[1] + "/juegos/el-faro/index.html")
    abrir_carta(d, "14")
    for _ in range(6):
        for ch in "0000":
            tecla(d, ch)
        tecla(d, "✓")
        time.sleep(0.3)
    time.sleep(1.2)
    bloq = d.execute_script("return [...document.querySelectorAll('.far-body button')].filter(b=>b.disabled).length")
    msg = feedback(d)
    print("botones bloqueados:", bloq, "|", msg[:80])
    assert bloq >= 10 and "atascado" in msg, "el freno no se activó"
    cerrar(d)
    print("FRENO OK")
finally:
    d.quit()
