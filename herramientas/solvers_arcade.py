import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bot_core import *
import instancias_arcade as I

# Las soluciones salen de lo que dibuja herramientas/pixeles.py y de lo que calcula instancias_arcade.py, no de copias escritas a mano.
AQUI = os.path.dirname(os.path.abspath(__file__))
CODIGOS = json.load(open(os.path.join(AQUI, "codigos_arcade.json"), encoding="utf-8"))
INST = json.load(open(os.path.join(AQUI, "instancias_arcade.json"), encoding="utf-8"))


def clic(d, css):
    """Clic por JS: los elementos pueden estar dentro de contenedores con overflow oculto."""
    d.execute_script("arguments[0].click()", d.find_element(By.CSS_SELECTOR, css))
    time.sleep(0.05)


def s20(d):
    """Terminal: una palabra incompleta, otra mala y luego la de los componentes del cable."""
    abrir_carta(d, "20")
    boton(d, "Enviar").click()
    assert "Faltan letras" in feedback(d), feedback(d)
    for ch in "AAAAA":
        clic(d, f".arc-tecla[data-k='{ch}']")
    boton(d, "Enviar").click()
    assert "no reconoce" in feedback(d), feedback(d)
    for _ in range(5):
        boton(d, "Borrar").click()
    for ch in CODIGOS["placa"]["palabra"]:
        clic(d, f".arc-tecla[data-k='{ch}']")
    boton(d, "Enviar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s24(d):
    """Radar: sin elegir casilla, una casilla falsa y luego la del cofre."""
    abrir_carta(d, "24")
    boton(d, "Escanear").click()
    assert "Elegid primero" in feedback(d), feedback(d)
    clic(d, ".arc-casilla[data-c='C'][data-f='2']")
    boton(d, "Escanear").click()
    assert "Ahí no hay nada" in feedback(d), feedback(d)
    r = CODIGOS["radar"]
    clic(d, f".arc-casilla[data-c='{r['columna']}'][data-f='{r['fila']}']")
    boton(d, "Escanear").click()
    m = feedback(d)
    cerrar(d)
    return m


def s46(d):
    """Mando: una secuencia incompleta, otra mala y luego los botones encendidos del cartel."""
    abrir_carta(d, "46")
    boton(d, "Probar").click()
    assert "Faltan botones" in feedback(d), feedback(d)
    for _ in range(6):
        clic(d, ".arc-boton[data-k='derecha']")
    boton(d, "Probar").click()
    assert "no responde" in feedback(d), feedback(d)
    boton(d, "Vaciar").click()
    for k in CODIGOS["marquesina"]["botones"]:
        clic(d, f".arc-boton[data-k='{k}']")
    boton(d, "Probar").click()
    m = feedback(d)
    cerrar(d)
    return m


ETIQ = {"arriba": "Arriba", "izquierda": "Izquierda", "derecha": "Derecha", "quieto": "Esperar"}


def _estado_inicial():
    a = INST["autopista"]
    carriles = [(c["dir"], c["vel"], c["coches"]) for c in a["carriles"]]
    return carriles, (a["salida"][0], a["salida"][1], tuple(tuple(sorted(c[2])) for c in carriles))


def s48(d):
    """Autopista: un primer movimiento que atropella (si lo hay) y luego la solución calculada por búsqueda."""
    abrir_carta(d, "48")
    carriles, ini = _estado_inicial()
    for mov in ("arriba", "izquierda", "derecha"):
        # movimiento dentro de la carretera que acaba en choque
        f = ini[0] + (-1 if mov == "arriba" else 0)
        c = ini[1] + (-1 if mov == "izquierda" else 1 if mov == "derecha" else 0)
        if 0 <= f and 0 <= c < I.ANCHO and I.paso(ini, mov, carriles) is None:
            boton(d, ETIQ[mov]).click()
            assert "atropellado" in feedback(d), feedback(d)
            break
    for mov in INST["autopista"]["solucion"]:
        boton(d, ETIQ[mov]).click()
        time.sleep(0.05)
    m = feedback(d)
    cerrar(d)
    return m


def s69(d):
    """Pozo: sin llenar, una pieza fuera de sitio y luego la solución calculada por búsqueda."""
    abrir_carta(d, "69")
    boton(d, "Comprobar").click()
    assert "quedan huecos" in feedback(d), feedback(d)
    clic(d, ".arc-pieza[data-t='I']")
    clic(d, ".arc-hueco[data-r='3'][data-c='4']")
    assert "no cabe" in feedback(d), feedback(d)
    for p in INST["pozo"]["solucion"]:
        celdas = I.normalizar([tuple(x) for x in p["celdas"]])
        k = next(g for g in range(4) if _forma(p["tipo"], g) == celdas)
        clic(d, f".arc-pieza[data-t='{p['tipo']}']")
        for _ in range(k):
            boton(d, "Girar").click()
        r0 = min(x[0] for x in p["celdas"])
        c0 = min(x[1] for x in p["celdas"])
        clic(d, f".arc-hueco[data-r='{r0}'][data-c='{c0}']")
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def _forma(tipo, giros):
    c = I.normalizar(I.BASE[tipo])
    for _ in range(giros):
        c = I.girar(c)
    return c


SOLVERS = {"20": s20, "24": s24, "46": s46, "48": s48, "69": s69}
# cartas que hay que tener en mesa para poder resolver cada minijuego (las piezas se juntan en la mesa)
REQUIERE = {"20": ["14", "15", "16", "17", "18", "19"], "24": ["30", "31", "32", "33"], "46": ["40", "41", "42"], "48": ["52"], "69": ["70"]}
