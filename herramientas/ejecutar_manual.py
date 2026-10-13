"""Ejecuta los pasos del manual en navegador y comprueba la mesa tras cada paso.
uso: python herramientas/ejecutar_manual.py <BASE> <carpeta_juego> <modulo_datos> <modulo_solvers>
ej.: python herramientas/ejecutar_manual.py http://127.0.0.1:8810 juegos/el-faro datos_faro solvers_faro"""
import importlib, sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from bot_core import *

BASE, JUEGO, MOD_PASOS, MOD_SOLV = sys.argv[1:5]
PASOS = importlib.import_module(MOD_PASOS).PASOS
SOLVERS = importlib.import_module(MOD_SOLV).SOLVERS


def main():
    d_pc, d_app = nuevo_driver(), nuevo_driver()
    try:
        mesa = Mesa(d_pc, f"{BASE}/{JUEGO}/pc.html")
        abrir_app(d_app, f"{BASE}/{JUEGO}/index.html")
        if mesa.en_mesa() != ["P"]:
            raise Fallo(f"al empezar la mesa deberia ser solo P y es {mesa.en_mesa()}")
        n_mazo = len(mesa.en_mazo())
        log(f"inicio: mesa=['P'], mazo={n_mazo} cartas")
        for i, p in enumerate(PASOS, 1):
            log(f"PASO {i}: {p['t']}")
            for a in p["acciones"]:
                if a[0] == "leer":
                    inf = mesa.info(a[1])
                    for x in inf["descarta"]:
                        mesa.descartar(x, f"lo manda la carta {a[1]}")
                    for x in inf["coge"]:
                        mesa.coger(x, f"lo manda la carta {a[1]}")
                elif a[0] == "app":
                    msg = SOLVERS[a[1]](d_app)
                    log(f"   app {a[1]} -> {msg}")
                    if a[2] not in msg:
                        raise Fallo(f"paso {i}: el mensaje de la app {a[1]} no contiene '{a[2]}': {msg}")
                    coger, descartar = instrucciones_mensaje(msg)
                    for x in descartar:
                        mesa.descartar(x, f"lo manda la app {a[1]}")
                    for x in coger:
                        mesa.coger(x, f"lo manda la app {a[1]}")
                elif a[0] == "combinar":
                    s = str(int(a[1]) + int(a[2]))
                    for x in (a[1], a[2]):
                        if x not in mesa.en_mesa():
                            raise Fallo(f"paso {i}: para combinar falta la carta {x} en la mesa")
                        if mesa.info(x)["etq"] != "COMBINA":
                            raise Fallo(f"paso {i}: la carta {x} no tiene la etiqueta Combina")
                    mesa.coger(s, f"suma {a[1]}+{a[2]}")
            esperada = sorted(p["mesa"])
            real = sorted(mesa.en_mesa())
            if esperada != real:
                raise Fallo(f"paso {i}: la mesa deberia ser {esperada} y es {real}")
            log(f"   mesa OK: {real}")
        if mesa.en_mazo():
            raise Fallo(f"sobran cartas en el mazo: {mesa.en_mazo()}")
        log("*** MANUAL VERIFICADO: todos los pasos funcionan y se llega al final con solo la 99 en mesa")
        return True
    except Fallo as e:
        log(f"*** FALLO: {e}")
        return False
    finally:
        d_pc.quit()
        d_app.quit()


sys.exit(0 if main() else 1)
