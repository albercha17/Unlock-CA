"""Partidas completas en orden aleatorio, en el navegador.

uso: python herramientas/bot_azar.py BASE JUEGO N [semilla_inicial] [-v]
JUEGO: faro | egipto | marte. Cada partida usa una semilla distinta (semilla_inicial, +1, +2...).
En cada paso elige al azar entre las acciones posibles (leer una carta nueva, coger o descartar lo que
dice, combinar, resolver una app) y solo hace lo que dicen las cartas y los mensajes de la app.
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bot_core import Fallo, Mesa, abrir_app, instrucciones_mensaje, nuevo_driver  # noqa: E402

VERBOSE = "-v" in sys.argv


def log(m):
    if VERBOSE:
        print(m, flush=True)


def jugar_azar(nombre, url_pc, url_app, solvers, requiere, semilla, final="99", max_acciones=500):
    rng = random.Random(semilla)
    d_pc, d_app = nuevo_driver(), nuevo_driver()
    try:
        mesa = Mesa(d_pc, url_pc)
        abrir_app(d_app, url_app)
        if mesa.en_mesa() != ["P"]:
            raise Fallo(f"al empezar la mesa deberia tener solo P y tiene {mesa.en_mesa()}")
        leidas, resueltas, combinadas, pendientes = set(), set(), set(), []
        hechas = 0
        while hechas < max_acciones:
            opciones = []
            if pendientes:
                opciones.append(("instruccion", None))
            for n in mesa.en_mesa():
                if n not in leidas:
                    opciones.append(("leer", n))
            comb = [n for n in mesa.en_mesa() if mesa.info(n)["etq"] == "COMBINA"]
            for i, a in enumerate(comb):
                for b in comb[i + 1:]:
                    clave = tuple(sorted((a, b)))
                    if clave not in combinadas and str(int(a) + int(b)) in mesa.en_mazo():
                        opciones.append(("combinar", clave))
            for n in mesa.en_mesa():
                if n not in resueltas and mesa.info(n)["etq"] == "APP" and all(r in mesa.en_mesa() for r in requiere.get(n, [])):
                    opciones.append(("app", n))
            if not opciones:
                break
            tipo, dato = rng.choice(opciones)
            hechas += 1
            if tipo == "instruccion":
                accion, n, motivo = pendientes.pop(rng.randrange(len(pendientes)))
                (mesa.descartar if accion == "descartar" else mesa.coger)(n, motivo)
            elif tipo == "leer":
                leidas.add(dato)
                inf = mesa.info(dato)
                for x in inf["descarta"]:
                    pendientes.append(("descartar", x, f"lo manda la carta {dato}"))
                for x in inf["coge"]:
                    pendientes.append(("coger", x, f"lo manda la carta {dato}"))
                log(f"- lee {dato}")
            elif tipo == "combinar":
                combinadas.add(dato)
                s = str(int(dato[0]) + int(dato[1]))
                log(f"- combina {dato[0]} + {dato[1]} = {s}")
                mesa.coger(s, f"suma {dato[0]}+{dato[1]}")
            else:
                if dato not in solvers:
                    raise Fallo(f"no hay solucionador para la app {dato}")
                msg = solvers[dato](d_app)
                resueltas.add(dato)
                log(f"- app {dato}: {msg[:70]}")
                coger, descartar = instrucciones_mensaje(msg)
                for x in descartar:
                    pendientes.append(("descartar", x, f"lo manda la app {dato}"))
                for x in coger:
                    pendientes.append(("coger", x, f"lo manda la app {dato}"))
        if pendientes:
            raise Fallo(f"quedan instrucciones sin hacer: {pendientes}")
        if mesa.en_mesa() != [final]:
            raise Fallo(f"la partida no termina limpia: mesa={mesa.en_mesa()}, mazo={mesa.en_mazo()}")
        if mesa.en_mazo():
            raise Fallo(f"sobran cartas en el mazo: {mesa.en_mazo()}")
        errs = [e["message"] for e in d_app.get_log("browser") + d_pc.get_log("browser")
                if e["level"] == "SEVERE" and "videoInicial" not in e["message"] and "favicon" not in e["message"]]
        if errs:
            raise Fallo(f"errores de consola: {errs}")
        return True, None
    except Fallo as e:
        return False, str(e)
    except Exception as e:  # noqa: BLE001
        return False, f"{type(e).__name__}: {str(e)[:300]}"
    finally:
        d_pc.quit()
        d_app.quit()


def main():
    args = [a for a in sys.argv[1:] if a != "-v"]
    base, juego, n = args[0], args[1], int(args[2])
    s0 = int(args[3]) if len(args) > 3 else 1
    cfg = {"faro": ("juegos/el-faro", "solvers_faro"),
           "egipto": ("juegos/aventuras-ca/egipto", "solvers_egipto"),
           "marte": ("juegos/aventuras-ca/marte", "solvers_marte")}
    carpeta, modulo = cfg[juego]
    mod = __import__(modulo)
    fallos = []
    for semilla in range(s0, s0 + n):
        ok, motivo = jugar_azar(juego, f"{base}/{carpeta}/pc.html", f"{base}/{carpeta}/index.html", mod.SOLVERS, mod.REQUIERE, semilla)
        print(f"{juego} semilla {semilla}: {'OK' if ok else 'FALLO: ' + str(motivo)}", flush=True)
        if not ok:
            fallos.append(semilla)
    print(f"RESUMEN {juego}: {n - len(fallos)} ok, {len(fallos)} fallos {fallos}", flush=True)
    sys.exit(1 if fallos else 0)


if __name__ == "__main__":
    main()
