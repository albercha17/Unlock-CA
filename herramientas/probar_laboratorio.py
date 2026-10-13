"""Resuelve por la interfaz real cada prototipo de juegos/laboratorio y comprueba que muestra el mensaje de éxito.

Uso (desde la raíz, con servidor local):  python herramientas/probar_laboratorio.py http://127.0.0.1:8890
"""
import itertools
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bot_core import By, nuevo_driver  # noqa: E402
import generadores_puzles as G  # noqa: E402

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8890"


def clic(d, css):
    d.execute_script("arguments[0].click()", d.find_element(By.CSS_SELECTOR, css))
    time.sleep(0.02)


def ok(d):
    m = d.find_element(By.ID, "msg") if d.find_elements(By.ID, "msg") else None
    return m is not None and "ok" in (m.get_attribute("class") or "")


def nonograma(d):
    sol = d.execute_script("return window.LAB.nonograma.solucion")
    c = len(sol[0])
    for r, fila in enumerate(sol):
        for k, v in enumerate(fila):
            if v:
                clic(d, f".celda[data-i='{r * c + k}']")


def akari(d):
    for r, c in d.execute_script("return window.LAB.akari.bombillas"):
        clic(d, f".celda[data-c='{r},{c}']")


def caja_negra(d):
    regla = G.REGLAS[d.execute_script("return window.LAB.cajaNegra.regla")]
    buenas = [c for c in itertools.permutations(range(len(G.FICHAS)), 3) if regla([G.FICHAS[i] for i in c])][:12]
    # un intento malo primero
    malo = next(c for c in itertools.permutations(range(len(G.FICHAS)), 3) if not regla([G.FICHAS[i] for i in c]))
    for combo in [malo] + buenas[:5]:
        clic(d, "#vaciar")
        for i in combo:
            clic(d, f".ficha[data-id='{i}']")
        clic(d, "#probar")
        if ok(d):
            return


def lengua(d):
    r = d.execute_script("return window.LAB.rosetta.pregunta[1]")
    d.find_element(By.ID, "resp").send_keys("tak ba")
    clic(d, "#comprobar")
    assert "bad" in d.find_element(By.ID, "msg").get_attribute("class")
    d.find_element(By.ID, "resp").clear()
    d.find_element(By.ID, "resp").send_keys(r)
    clic(d, "#comprobar")


def tabla(d):
    D = d.execute_script("return window.LAB.zebra")
    for a, valores in D["atributos"].items():
        for i, persona in enumerate(D["personas"]):
            j = valores.index(D["solucion"][a][i])
            clic(d, f"button.celda[data-a='{a}'][data-p='{i}'][data-v='{j}']")
            clic(d, f"button.celda[data-a='{a}'][data-p='{i}'][data-v='{j}']")
    clic(d, "#comprobar")


def caballeros(d):
    sol = d.execute_script("return window.LAB.caballeros.caballeros")
    clic(d, "#comprobar")
    assert "bad" in d.find_element(By.ID, "msg").get_attribute("class")
    for i, esc in enumerate(sol):
        for _ in range(1 if esc else 2):
            clic(d, f".pers button[data-i='{i}']")
    clic(d, "#comprobar")


def bloques(d):
    for i, paso in d.execute_script("return window.LAB.bloques.ruta"):
        d.execute_script("window.__moverCoche(arguments[0], arguments[1])", i, paso)
        time.sleep(0.01)


def tubos(d):
    for a, b in d.execute_script("return window.LAB.tubos.ruta"):
        clic(d, f".tubo[data-i='{a}']")
        clic(d, f".tubo[data-i='{b}']")


def puentes(d):
    for a, b, v in d.execute_script("return window.LAB.puentes.puentes"):
        for _ in range(v):
            clic(d, f".isla[data-k='{a[0]},{a[1]}']")
            clic(d, f".isla[data-k='{b[0]},{b[1]}']")


def linterna(d):
    for sentido, tiempos in d.execute_script("return window.LAB.linterna.plan"):
        for t in tiempos:
            # selecciona al explorador con ese tiempo que esté en la orilla de salida/llegada
            hecho = False
            for e in d.find_elements(By.CSS_SELECTOR, ".pers.lado-" + ("izq" if sentido == "ida" else "der")):
                if e.get_attribute("data-t") == str(t) and "sel" not in e.get_attribute("class"):
                    d.execute_script("arguments[0].click()", e)
                    hecho = True
                    break
            assert hecho, f"no encuentro al explorador de {t}"
        clic(d, "#cruzar")


def cerillas(d):
    de, a = d.execute_script("const c = window.LAB.cerillas; return [c.desde, c.hasta]")
    clic(d, f".slot[data-k='{de[0]}'][data-s='{de[1]}']")
    clic(d, f".slot[data-k='{a[0]}'][data-s='{a[1]}']")


def rayos(d):
    for celda, o in d.execute_script("return window.LAB.rayos.solucion"):
        for _ in range(1 if o == "/" else 2):
            clic(d, f".cel[data-i='{celda}']")


def luces(d):
    for i in d.execute_script("return window.LAB.luces.toques_minimos"):
        clic(d, f".cri[data-i='{i}']")


PRUEBAS = [("nonograma", nonograma), ("akari", akari), ("caja-negra", caja_negra), ("lengua", lengua),
           ("tabla-logica", tabla), ("caballeros", caballeros), ("bloques", bloques), ("tubos", tubos), ("puentes", puentes), ("linterna", linterna), ("luces", luces), ("cerillas", cerillas), ("rayos", rayos)]


def main():
    d = nuevo_driver()
    fallos = []
    try:
        for nombre, f in PRUEBAS:
            d.get(f"{BASE}/juegos/laboratorio/{nombre}.html")
            time.sleep(0.6)
            try:
                f(d)
                time.sleep(0.2)
                if not ok(d):
                    raise AssertionError("no aparece el mensaje de éxito")
                errs = [e for e in d.get_log("browser") if e["level"] == "SEVERE" and "favicon" not in e["message"]]
                if errs:
                    raise AssertionError(f"errores de consola: {errs}")
                print("OK    ", nombre, "->", d.find_element(By.ID, "msg").text)
            except Exception as e:  # noqa: BLE001
                print("FALLO ", nombre, "->", type(e).__name__, str(e)[:200])
                fallos.append(nombre)
    finally:
        d.quit()
    print("RESULTADO:", "OK" if not fallos else f"fallan {fallos}")
    sys.exit(1 if fallos else 0)


if __name__ == "__main__":
    main()
