"""Solucionadores de los minijuegos de «Egipto» (60 cartas): juegan cada app por la interfaz real, primero una jugada mala para comprobar el
aviso y luego la buena. Las soluciones salen de instancias_egipto.py."""
import sys, time
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from bot_core import *
import instancias_egipto as I


def clic(d, css):
    """Clic por JS: los elementos pueden estar dentro de contenedores con overflow oculto."""
    d.execute_script("arguments[0].click()", d.find_element(By.CSS_SELECTOR, css))
    time.sleep(0.03)


def sube(d, clave, n):
    for _ in range(n):
        clic(d, f".eg-fila[data-c='{clave}'] button[data-d='1']")


def s14(d):
    """Granero: 0 sacos (falla) y los sacos buenos."""
    abrir_carta(d, "14")
    boton(d, "Abrir la puerta").click()
    assert "no cuadran" in feedback(d), feedback(d)
    sube(d, "sacos", I.MONTON["solucion"])
    boton(d, "Abrir la puerta").click()
    m = feedback(d)
    cerrar(d)
    return m


def _pon_piramide(d, v):
    for i, x in enumerate(v):
        d.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'))",
                         d.find_element(By.CSS_SELECTOR, f".pir-base input[data-i='{i}']"), str(x))


def s20(d):
    """Pirámide: la base vacía (falla), una base que no cuadra (falla) y la buena."""
    abrir_carta(d, "20")
    boton(d, "Comprobar").click()
    assert "Faltan" in feedback(d), feedback(d)
    _pon_piramide(d, [1, 1, 1, 1, 1])
    boton(d, "Comprobar").click()
    assert "no coinciden" in feedback(d), feedback(d)
    _pon_piramide(d, I.PIRAMIDE["solucion"])
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s40(d):
    """Nilómetro: cero (falla) y la crecida buena."""
    abrir_carta(d, "40")
    boton(d, "Avisar a los sacerdotes").click()
    assert "desbordaría" in feedback(d), feedback(d)
    c, p = I.NILOMETRO["solucion"]
    sube(d, "codos", c)
    sube(d, "palmos", p)
    boton(d, "Avisar a los sacerdotes").click()
    m = feedback(d)
    cerrar(d)
    return m


def s48(d):
    """Friso: todo ceros (falla) y la cuenta buena."""
    abrir_carta(d, "48")
    boton(d, "Responder").click()
    assert "niega con la cabeza" in feedback(d), feedback(d)
    for a, n in zip(I.ANIMALES, I.CONTAR["solucion"]):
        sube(d, a, n)
    boton(d, "Responder").click()
    m = feedback(d)
    cerrar(d)
    return m


def s52(d):
    """Heqat: sin elegir (falla), una parte sola (falla) y las partes buenas."""
    abrir_carta(d, "52")
    boton(d, "Medir").click()
    assert "Elegid alguna" in feedback(d), feedback(d)
    clic(d, ".heq-parte[data-i='1']")
    boton(d, "Medir").click()
    assert "no es lo que se ha cobrado" in feedback(d), feedback(d)
    boton(d, "Vaciar").click()
    for i in I.HEQAT["solucion"]:
        clic(d, f".heq-parte[data-i='{i}']")
    boton(d, "Medir").click()
    m = feedback(d)
    cerrar(d)
    return m


def s46(d):
    """Criptograma: cifras repetidas (falla), suma falsa (falla), suma cierta sin las notas (falla) y la solución."""
    abrir_carta(d, "46")
    boton(d, "Comprobar").click()
    assert "repetidas" in feedback(d), feedback(d)
    letras = list(I.CRIPTO["signos"])

    def pon(m):
        for l in letras:
            actual = int(d.find_element(By.CSS_SELECTOR, f".eg-fila[data-c='{l}']").get_attribute("data-v"))
            for _ in range(m[l] - actual):
                clic(d, f".eg-fila[data-c='{l}'] button[data-d='1']")
            for _ in range(actual - m[l]):
                clic(d, f".eg-fila[data-c='{l}'] button[data-d='-1']")
    pon({l: k + 1 for k, l in enumerate(letras)})
    boton(d, "Comprobar").click()
    assert "no es cierta" in feedback(d), feedback(d)
    otra = next(m for m in I._soluciones_cripto() if m != I.CRIPTO["solucion"])
    pon(otra)
    boton(d, "Comprobar").click()
    assert "no cumple" in feedback(d), feedback(d)
    pon(I.CRIPTO["solucion"])
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s51(d):
    """Cámaras: sin pintar (falla), todas ocre (falla) y la pintura buena."""
    abrir_carta(d, "51")
    boton(d, "Comprobar").click()
    assert "sin pintar" in feedback(d), feedback(d)
    sol = I.CAMARAS["solucion"]
    for i in range(len(sol)):
        clic(d, f".cam-cel[data-i='{i}']")
    boton(d, "Comprobar").click()
    assert "no cuadra" in feedback(d), feedback(d)
    for i, c in enumerate(sol):
        for _ in range(c):
            clic(d, f".cam-cel[data-i='{i}']")
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s69(d):
    """Canales: un canal imposible (falla), campos aislados (falla), canales de más (falla) y el riego más barato."""
    abrir_carta(d, "69")
    existen = {frozenset(c[:2]) for c in I.CANALES["canales"]}
    ks = list(I.CANALES["campos"])
    a, b = next((x, y) for x in ks for y in ks if x < y and frozenset((x, y)) not in existen)
    clic(d, f".can-campo[data-k='{a}']")
    clic(d, f".can-campo[data-k='{b}']")
    assert "no se puede cavar" in feedback(d), feedback(d)
    boton(d, "Abrir las compuertas").click()
    assert "aislado" in feedback(d), feedback(d)

    def canal(x, y):
        clic(d, f".can-campo[data-k='{x}']")
        clic(d, f".can-campo[data-k='{y}']")
    sol = [tuple(e) for e in I.CANALES["solucion"]]
    for x, y in sol:
        canal(x, y)
    extra = next(c[:2] for c in I.CANALES["canales"] if frozenset(c[:2]) not in {frozenset(e) for e in sol})
    canal(*extra)
    boton(d, "Abrir las compuertas").click()
    assert "más de lo necesario" in feedback(d), feedback(d)
    canal(*extra)
    boton(d, "Abrir las compuertas").click()
    m = feedback(d)
    cerrar(d)
    return m


def s64(d):
    """Azulejos: sin elegir (falla), uno equivocado (falla) y el bueno."""
    abrir_carta(d, "64")
    boton(d, "Colocar").click()
    assert "Elegid un azulejo" in feedback(d), feedback(d)
    mal = next(i for i in range(len(I.FRISO["opciones"])) if i != I.FRISO["solucion"])
    clic(d, f".azu-t[data-i='{mal}']")
    boton(d, "Colocar").click()
    assert "rompe alguna regla" in feedback(d), feedback(d)
    clic(d, f".azu-t[data-i='{I.FRISO['solucion']}']")
    boton(d, "Colocar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s72(d):
    """Tierras: sin repartir (falla), una parcela que pisa a otra (falla), una partición distinta (falla) y la buena."""
    abrir_carta(d, "72")
    boton(d, "Comprobar").click()
    assert "sin repartir" in feedback(d), feedback(d)

    def parcela(r):
        x0, y0, w, h = r
        clic(d, f".eg-cel[data-x='{x0}'][data-y='{y0}']")
        clic(d, f".eg-cel[data-x='{x0 + w - 1}'][data-y='{y0 + h - 1}']")
    sol = I.TIERRAS["solucion"]
    parcela(sol[0])
    n = I.TIERRAS["n"]
    clic(d, f".eg-cel[data-x='{n - 1}'][data-y='{n - 1}']")                 # una esquina fuera y otra dentro de la parcela hecha
    clic(d, f".eg-cel[data-x='{sol[0][0]}'][data-y='{sol[0][1]}']")
    assert "pisa a otra" in feedback(d), feedback(d)
    # una partición válida pero distinta: todas las casillas en filas sueltas de una casilla de alto
    boton(d, "Borrar todo").click()
    for y in range(I.TIERRAS["n"]):
        parcela([0, y, I.TIERRAS["n"], 1])
    boton(d, "Comprobar").click()
    assert "no cuadra" in feedback(d), feedback(d)
    boton(d, "Borrar todo").click()
    for r in sol:
        parcela(r)
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s85(d):
    """Consola: los sellos al revés (falla) y en el orden de los acertijos."""
    abrir_carta(d, "85")
    boton(d, "Despertar al Cronoportal").click()
    assert "Faltan sellos" in feedback(d), feedback(d)
    for c in reversed(I.ORDEN_SELLOS):
        clic(d, f".sel-s[data-c='{c}']")
    boton(d, "Despertar al Cronoportal").click()
    assert "no es el orden" in feedback(d), feedback(d)
    boton(d, "Quitar todos").click()
    for c in I.ORDEN_SELLOS:
        clic(d, f".sel-s[data-c='{c}']")
    boton(d, "Despertar al Cronoportal").click()
    m = feedback(d)
    cerrar(d)
    return m


SOLVERS = {"14": s14, "20": s20, "40": s40, "48": s48, "52": s52, "46": s46, "51": s51, "69": s69, "64": s64, "72": s72, "85": s85}
REQUIERE = {"14": ["16"], "20": ["18", "19", "21"], "40": ["41", "43", "45"], "48": ["42", "49", "53"], "52": ["54", "55", "59"],
            "46": ["37", "39", "33"], "51": ["26", "61", "63"], "69": ["70", "71"], "64": ["66", "67"], "72": ["75", "79"], "85": ["86", "87"]}
