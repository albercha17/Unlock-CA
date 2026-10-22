"""Solucionadores de los minijuegos de «Mar de las Brumas, 1715» (60 cartas): juegan cada app por la interfaz real, primero una jugada mala para comprobar
el aviso y luego la buena. Las soluciones salen de instancias_piratas.py."""
import sys, time
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from bot_core import *
import instancias_piratas as I

D = I.INST


def clic(d, css):
    """Clic por JS: los elementos pueden estar dentro de contenedores con overflow oculto."""
    d.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}))", d.find_element(By.CSS_SELECTOR, css))
    time.sleep(0.03)


def escribe(d, css, texto):
    d.execute_script("var e = document.querySelector(arguments[0]); e.value = arguments[1]; e.dispatchEvent(new Event('input'));", css, str(texto))


def ajusta(d, nombre, objetivo, paso=1):
    """Lleva un contador (+/−) hasta el valor pedido."""
    css = f".pi-cont[data-nombre='{nombre}']"
    for _ in range(80):
        v = int(d.find_element(By.CSS_SELECTOR, css).get_attribute("data-v"))
        if v == objetivo:
            return
        clic(d, css + (" button[data-d='1']" if v < objetivo else " button[data-d='-1']"))
    raise Fallo("no llego a " + str(objetivo) + " en " + nombre)


def s14(d):
    """Bitácora: todo a cero (falla), las horas bien y los minutos mal (falla) y el tiempo bueno."""
    abrir_carta(d, "14")
    B = D["bitacora"]
    boton(d, "Anotar en el cuaderno").click()
    assert "niega" in feedback(d), feedback(d)
    ajusta(d, "horas", B["entre_horas"])
    ajusta(d, "minutos", (B["entre_min"] + 15) % 60, 15)
    boton(d, "Anotar en el cuaderno").click()
    assert "niega" in feedback(d), feedback(d)
    ajusta(d, "minutos", B["entre_min"], 15)
    boton(d, "Anotar en el cuaderno").click()
    m = feedback(d)
    cerrar(d)
    return m


def s20(d):
    """Persecución: salir de la carta (falla) y la solución."""
    abrir_carta(d, "20")
    P = D["persecucion"]
    x, y = P["barco"]
    afuera = "izquierda" if x == 0 else "arriba" if y == 0 else "derecha" if x == P["ancho"] - 1 else "abajo"
    clic(d, f".pir-timon button[data-d='{afuera}']")
    assert "roca" in feedback(d), feedback(d)
    for m in P["solucion"]:
        clic(d, f".pir-timon button[data-d='{m}']")
        time.sleep(0.02)
    m = feedback(d)
    cerrar(d)
    return m


def s40(d):
    """Cielo: pocas estrellas (falla), seis equivocadas (falla) y las buenas."""
    abrir_carta(d, "40")
    C = D["cielo"]
    boton(d, "Abrir el cofre").click()
    assert "seis estrellas" in feedback(d), feedback(d)
    malas = [n for n in range(1, 37) if n not in C["solucion"]][:6]
    for n in malas:
        clic(d, f".cie-g button[data-n='{n}']")
    boton(d, "Abrir el cofre").click()
    assert "no cede" in feedback(d), feedback(d)
    boton(d, "Quitar todas").click()
    for n in C["solucion"]:
        clic(d, f".cie-g button[data-n='{n}']")
    boton(d, "Abrir el cofre").click()
    m = feedback(d)
    cerrar(d)
    return m


def s48(d):
    """Suelo: una losa que no es de la fila de abajo (falla), un primer paso equivocado (se hunde) y el camino."""
    abrir_carta(d, "48")
    L = D["losas"]
    n = L["n"]
    clic(d, f".pir-losa[data-x='0'][data-y='0']")
    assert "fila de abajo" in feedback(d), feedback(d)
    mala = next(x for x in range(n) if L["suelo"][n - 1][x] != L["ciclo"][0])
    clic(d, f".pir-losa[data-x='{mala}'][data-y='{n - 1}']")
    assert "se hunde" in feedback(d), feedback(d)
    for x, y in L["camino"]:
        clic(d, f".pir-losa[data-x='{x}'][data-y='{y}']")
    m = feedback(d)
    cerrar(d)
    return m


def s52(d):
    """Cañón: sin apuntar (falla), carga repetida (falla), demasiada pólvora (falla), elevaciones equivocadas (falla) y los tres tiros."""
    abrir_carta(d, "52")
    K = D["canon"]

    def poner(i, c, e):
        clic(d, f".can-f button[data-t='c'][data-i='{i}'][data-v='{c}']")
        clic(d, f".can-f button[data-t='e'][data-i='{i}'][data-v='{e}']")
    boton(d, "¡Fuego!").click()
    assert "Falta" in feedback(d), feedback(d)
    for i in range(3):
        poner(i, 0, 0)
    boton(d, "¡Fuego!").click()
    assert "misma carga" in feedback(d), feedback(d)
    for i, c in enumerate([5, 4, 3]):
        poner(i, c, 0)
    boton(d, "¡Fuego!").click()
    assert "pólvora" in feedback(d), feedback(d)
    for i, (c, a) in enumerate(K["solucion"]):
        poner(i, c, (a + 1) % 5)
    boton(d, "¡Fuego!").click()
    assert "no aciertan" in feedback(d) or "no acierta" in feedback(d) or "caen al agua" in feedback(d), feedback(d)
    for i, (c, a) in enumerate(K["solucion"]):
        poner(i, c, a)
    boton(d, "¡Fuego!").click()
    m = feedback(d)
    cerrar(d)
    return m


def s46(d):
    """Botín: sin repartir bien (falla), un reparto que se rechaza (falla), uno que se aprueba pero no es el máximo (falla) y el bueno."""
    abrir_carta(d, "46")
    B = D["botin"]

    def reparto(v):
        for i, x in enumerate(v):
            escribe(d, f".bot-f input[data-i='{i}']", x)
    boton(d, "Proponer el reparto").click()
    assert "sin repartir" in feedback(d), feedback(d)
    reparto([B["monedas"]] + [0] * (B["piratas"] - 1))
    boton(d, "Proponer el reparto").click()
    assert "rechaza" in feedback(d), feedback(d)
    v = list(B["solucion"])
    v[0] -= 1
    v[1] += 1
    reparto(v)
    boton(d, "Proponer el reparto").click()
    assert "podía haberse quedado" in feedback(d), feedback(d)
    reparto(B["solucion"])
    boton(d, "Proponer el reparto").click()
    m = feedback(d)
    cerrar(d)
    return m


def s51(d):
    """Mareas: sin elegir (falla), una hora en la que embarranca (falla) y la hora buena."""
    abrir_carta(d, "51")
    M = D["mareas"]
    boton(d, "Zarpar").click()
    assert "Elegid primero" in feedback(d), feedback(d)
    mala = next(t for t in range(19) if any(M["alturas"][t + b["tras"]] + b["fondo"] < M["calado"] for b in M["barras"]))
    clic(d, f".mar-g button[data-h='{mala}']")
    boton(d, "Zarpar").click()
    assert "embarranca" in feedback(d), feedback(d)
    clic(d, f".mar-g button[data-h='{M['salida']}']")
    boton(d, "Zarpar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s64(d):
    """Timón: un rumbo cualquiera (falla), el rumbo de la carta sin el desvío (falla) y el rumbo de la aguja."""
    abrir_carta(d, "64")
    R = D["rumbo"]
    actual = [0]

    def girar(objetivo):
        dif = (objetivo - actual[0]) % 360
        if dif > 180:
            dif -= 360
        for paso in (10, 1):
            while abs(dif) >= paso:
                s = paso if dif > 0 else -paso
                clic(d, f".pir-giros button[data-d='{s}']")
                dif -= s
        actual[0] = objetivo
    girar(200)
    boton(d, "Fijar el rumbo").click()
    assert "niega" in feedback(d), feedback(d)
    girar(int(R["carta"]))
    boton(d, "Fijar el rumbo").click()
    assert "cuaderno del piloto" in feedback(d), feedback(d)
    girar(R["aguja"])
    boton(d, "Fijar el rumbo").click()
    m = feedback(d)
    cerrar(d)
    return m


def s69(d):
    """Balanza: sin pesas (falla) y las pesas buenas."""
    abrir_carta(d, "69")
    P = D["pesas"]
    boton(d, "Pesar").click()
    assert "se inclina" in feedback(d), feedback(d)
    for o, s in enumerate(P["solucion"]):
        for p, c in enumerate(s):
            for _ in range(1 if c < 0 else 2 if c > 0 else 0):
                clic(d, f".pes-f button[data-o='{o}'][data-p='{p}']")
    boton(d, "Pesar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s72(d):
    """Gruta: una casilla de arena (falla) y la casilla de la X."""
    abrir_carta(d, "72")
    R = D["ruta"]
    xm, ym = R["celdas"][-1]
    t = [R["filas"] - 1 - ym, xm]
    otra = (0, 0) if t != [0, 0] else (1, 1)
    palm = [R["filas"] - 1 - R["inicio"][1], R["inicio"][0]]
    if list(otra) == palm:
        otra = (2, 2)
    clic(d, f".pir-gruta .pir-arena[data-x='{otra[0]}'][data-y='{otra[1]}']")
    assert "arena" in feedback(d), feedback(d)
    clic(d, f".pir-gruta .pir-arena[data-x='{t[0]}'][data-y='{t[1]}']")
    m = feedback(d)
    cerrar(d)
    return m


def s85(d):
    """Isla: sin elegir (falla), la salida (falla) y la casilla final."""
    abrir_carta(d, "85")
    L = D["isla"]
    boton(d, "Echar el ancla").click()
    assert "Elegid primero" in feedback(d), feedback(d)
    clic(d, f".isl-g button[data-x='{L['inicio'][0] + 1}'][data-y='{L['inicio'][1] + 1}']")
    boton(d, "Echar el ancla").click()
    assert "no muerde" in feedback(d), feedback(d)
    clic(d, f".isl-g button[data-x='{L['final'][0] + 1}'][data-y='{L['final'][1] + 1}']")
    boton(d, "Echar el ancla").click()
    m = feedback(d)
    cerrar(d)
    return m


SOLVERS = {"14": s14, "20": s20, "40": s40, "48": s48, "52": s52, "46": s46, "51": s51, "64": s64, "69": s69, "72": s72, "85": s85}
REQUIERE = {"14": ["16"], "20": ["18", "19", "21"], "40": ["41", "43", "45"], "48": ["42", "49", "53"], "52": ["54", "55", "59"], "46": ["37", "39", "33"],
            "51": ["26", "61", "63"], "64": ["66", "67"], "69": ["70", "71"], "72": ["75", "79"], "85": ["86", "87"]}
