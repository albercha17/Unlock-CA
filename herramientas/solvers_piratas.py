import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bot_core import *

# Las soluciones salen de lo que calcula instancias_piratas.py (y dibuja piratas.py), no de copias escritas a mano.
INST = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "instancias_piratas.json"), encoding="utf-8"))


def clic(d, css):
    """Clic por JS: los elementos pueden estar dentro de contenedores con overflow oculto."""
    d.execute_script("arguments[0].click()", d.find_element(By.CSS_SELECTOR, css))
    time.sleep(0.03)


def s24(d):
    """Timón: a 0 (falla), al rumbo de la carta sin desvío (avisa del desvío) y luego al rumbo de la aguja."""
    abrir_carta(d, "24")
    boton(d, "Fijar el rumbo").click()
    assert "niega" in feedback(d), feedback(d)
    r = INST["rumbo"]

    def ir_a(objetivo, actual):
        dif = (objetivo - actual) % 360
        for _ in range(dif // 10):
            clic(d, ".pir-giros button[data-d='10']")
        for _ in range(dif % 10):
            clic(d, ".pir-giros button[data-d='1']")
    ir_a(int(r["carta"]), 0)
    boton(d, "Fijar el rumbo").click()
    assert "desvía" in feedback(d), feedback(d)
    ir_a(r["aguja"], int(r["carta"]))
    boton(d, "Fijar el rumbo").click()
    m = feedback(d)
    cerrar(d)
    return m


def s46(d):
    """Bodega: marca con tiza una X, choca con una cuaderna si se puede, deshace y empuja los barriles por la solución más corta (BFS)."""
    abrir_carta(d, "46")
    b = INST["bodega"]
    x, y = b["metas"][0]
    clic(d, f".pir-celda[data-x='{x}'][data-y='{y}']")
    assert d.find_elements(By.CSS_SELECTOR, ".pir-celda.tiza"), "la tiza no marca la casilla"
    clic(d, ".pir-mando button[data-d='arriba']")
    boton(d, "Deshacer").click()
    for mov in b["solucion"]:
        clic(d, f".pir-mando button[data-d='{mov}']")
    m = feedback(d)
    cerrar(d)
    return m


def s48(d):
    """Persecución: ir directo hacia la niebla (la fragata os apresa) y luego la solución más corta (BFS)."""
    abrir_carta(d, "48")
    pe = INST["persecucion"]
    from instancias_piratas import resolver_persecucion
    directo = resolver_persecucion({tuple(r) for r in pe["rocas"]}, tuple(pe["barco"]), (-9, -9), tuple(pe["niebla"]), pe["ancho"], pe["alto"])
    for mov in directo:                                    # el camino más corto sin pensar en la fragata
        clic(d, f".pir-timon button[data-d='{mov}']")
        if "apresa" in feedback(d) or "boca del lobo" in feedback(d):
            break
    assert "apresa" in feedback(d) or "boca del lobo" in feedback(d), feedback(d)
    boton(d, "Empezar de nuevo").click()
    time.sleep(1.0)
    for mov in pe["solucion"]:
        clic(d, f".pir-timon button[data-d='{mov}']")
    m = feedback(d)
    cerrar(d)
    return m


def s66(d):
    """Tapa del cofre: cinco tachuelas (faltan), seis equivocadas (no es la forma) y luego las seis de la Calavera."""
    abrir_carta(d, "66")
    ci = INST["cielo"]
    malas = [i for i in range(len(ci["estrellas"])) if i not in ci["solucion"]][:6]
    for i in malas[:5]:
        clic(d, f".pir-tachuela[data-i='{i}']")
    boton(d, "Abrir el cofre").click()
    assert "seis estrellas" in feedback(d), feedback(d)
    clic(d, f".pir-tachuela[data-i='{malas[5]}']")
    boton(d, "Abrir el cofre").click()
    assert "no forman" in feedback(d), feedback(d)
    boton(d, "Quitar todas").click()
    for i in ci["solucion"]:
        clic(d, f".pir-tachuela[data-i='{i}']")
    boton(d, "Abrir el cofre").click()
    m = feedback(d)
    cerrar(d)
    return m


def s79(d):
    """Suelo de la cueva: una losa de abajo con otro símbolo (se hunde) y luego el único camino."""
    abrir_carta(d, "79")
    lo = INST["losas"]
    n = lo["n"]
    mala = next(x for x in range(n) if lo["suelo"][n - 1][x] != lo["ciclo"][0])
    clic(d, f".pir-losa[data-x='{mala}'][data-y='{n - 1}']")
    assert "se hunde" in feedback(d), feedback(d)
    for x, y in lo["camino"]:
        clic(d, f".pir-losa[data-x='{x}'][data-y='{y}']")
    m = feedback(d)
    cerrar(d)
    return m


def s69(d):
    """Gruta: cavar donde cae la X del mapa DESPLEGADO sin girar (solo arena) y luego en la X del mapa plegado, girada."""
    abrir_carta(d, "69")
    ru = INST["ruta"]
    xm, ym = ru["celdas"][-1]
    sx, sy = ru["filas"] - 1 - ym, xm                      # en pantalla el norte queda a la derecha
    clic(d, f".pir-arena[data-x='{(sx + 2) % ru['filas']}'][data-y='{sy}']")
    assert "Solo arena" in feedback(d), feedback(d)
    clic(d, f".pir-arena[data-x='{sx}'][data-y='{sy}']")
    m = feedback(d)
    cerrar(d)
    return m


SOLVERS = {"24": s24, "46": s46, "48": s48, "66": s66, "79": s79, "69": s69}
# cartas que hay que tener en mesa para poder resolver cada minijuego
REQUIERE = {"24": ["30", "31"], "46": ["40"], "48": ["52"], "66": ["64"], "79": ["76"], "69": ["70"]}


# ---- ampliación a 36 cartas: el reloj de bitácora
_AMP = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "instancias_ampliacion.json"), encoding="utf-8"))


def s61(d):
    """Reloj: a las 00:00 (falla) y luego a la hora del diario, de media en media hora."""
    abrir_carta(d, "61")
    boton(d, "Esta es la hora").click()
    assert "no se puede pasar" in feedback(d), feedback(d)
    h, m = _AMP["piratas_campanas"]["hora"]
    medias = h * 2 + m // 30
    for _ in range(medias // 4):
        clic(d, ".pir-mandos button[data-d='4']")
    for _ in range(medias % 4):
        clic(d, ".pir-mandos button[data-d='1']")
    boton(d, "Esta es la hora").click()
    m = feedback(d)
    cerrar(d)
    return m


SOLVERS.update({"61": s61})
REQUIERE.update({"61": ["63", "65", "67"]})
