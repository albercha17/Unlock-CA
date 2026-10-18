import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bot_core import *

# Las soluciones salen de lo que dibuja herramientas/oeste.py, no de copias escritas a mano.
CODIGOS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "codigos_oeste.json"), encoding="utf-8"))
ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def clic(d, css):
    """Clic por JS: los elementos pueden estar dentro de contenedores con overflow oculto."""
    d.execute_script("arguments[0].click()", d.find_element(By.CSS_SELECTOR, css))
    time.sleep(0.05)


def s20(d):
    """Candado: sin tocar (AAAAA) y luego la palabra de los vagones."""
    abrir_carta(d, "20")
    boton(d, "Abrir").click()
    assert "no se abre" in feedback(d), feedback(d)
    for i, ch in enumerate(CODIGOS["tren"]["palabra"]):
        for _ in range(ABC.index(ch)):
            clic(d, f".oes-rueda[data-i='{i}'] .sube")
    boton(d, "Abrir").click()
    m = feedback(d)
    cerrar(d)
    return m


def s24(d):
    """Celda: sin elegir, un sospechoso equivocado y luego el del cartel."""
    abrir_carta(d, "24")
    boton(d, "Detener").click()
    assert "Elegid primero" in feedback(d), feedback(d)
    malo = next(n for n in CODIGOS["cartel"]["sospechosos"] if n != CODIGOS["cartel"]["sospechoso"])
    clic(d, f".oes-nombre[data-n='{malo}']")
    boton(d, "Detener").click()
    assert "Ese no es" in feedback(d), feedback(d)
    clic(d, f".oes-nombre[data-n='{CODIGOS['cartel']['sospechoso']}']")
    boton(d, "Detener").click()
    m = feedback(d)
    cerrar(d)
    return m


def _girar(d, desde, hasta, sentido):
    delta = (hasta - desde) % 40 if sentido == "derecha" else (desde - hasta) % 40
    p = "der" if sentido == "derecha" else "izq"
    for _ in range(delta // 5):
        clic(d, f".oes-giro[data-d='{p}5']")
    for _ in range(delta % 5):
        clic(d, f".oes-giro[data-d='{p}1']")


def s46(d):
    """Caja fuerte: Fijar sin girar (falla) y luego la combinación con sus sentidos."""
    abrir_carta(d, "46")
    boton(d, "Fijar").click()
    assert "vuelve a cero" in feedback(d), feedback(d)
    pos = 0
    for num, sentido in zip(CODIGOS["mapa"]["combinacion"], CODIGOS["mapa"]["giros"]):
        _girar(d, pos, num, sentido)
        pos = num
        boton(d, "Fijar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s48(d):
    """Mechas: una señal a destiempo (falla) y luego el método de los dos extremos."""
    abrir_carta(d, "48")
    boton(d, "Dar la señal").click()
    assert "no a la hora" in feedback(d), feedback(d)
    for m_, e in (("A", 1), ("A", 2), ("B", 1)):
        clic(d, f".oes-extremo[data-m='{m_}'][data-e='{e}']")
    boton(d, "Esperar hasta que se apague una mecha").click()
    clic(d, ".oes-extremo[data-m='B'][data-e='2']")
    boton(d, "Esperar hasta que se apague una mecha").click()
    assert d.find_element(By.CSS_SELECTOR, ".oes-reloj").get_attribute("data-t") == str(CODIGOS["mechas"]["minutos"]), "el reloj no marca la hora"
    boton(d, "Dar la señal").click()
    m = feedback(d)
    cerrar(d)
    return m


def _pesar(d, izq, der):
    boton(d, "Vaciar platillos").click()
    for i in izq:
        clic(d, f".oes-barra[data-i='{i}']")
    for i in der:
        clic(d, f".oes-barra[data-i='{i}']")
        clic(d, f".oes-barra[data-i='{i}']")
    boton(d, "Pesar").click()
    t = feedback(d)
    if "equilibrada" in t:
        return "igual"
    return "izq_pesa_mas" if "hacia la izquierda" in t else "der_pesa_mas"


def s69(d):
    """Báscula: sin barras (falla) y luego el método 3 + 3 y 1 + 1 leyendo lo que dice la balanza (no se conoce la barra falsa de antemano)."""
    abrir_carta(d, "69")
    boton(d, "Pesar").click()
    assert "mismo número" in feedback(d), feedback(d)
    r1 = _pesar(d, [0, 1, 2], [3, 4, 5])
    grupo = [6, 7, 8] if r1 == "igual" else [3, 4, 5] if r1 == "izq_pesa_mas" else [0, 1, 2]
    r2 = _pesar(d, [grupo[0]], [grupo[1]])
    falsa = grupo[2] if r2 == "igual" else grupo[1] if r2 == "izq_pesa_mas" else grupo[0]
    clic(d, f".oes-sospecha[data-i='{falsa}']")
    m = feedback(d)
    cerrar(d)
    return m


SOLVERS = {"20": s20, "24": s24, "46": s46, "48": s48, "69": s69}
# cartas que hay que tener en mesa para poder resolver cada minijuego
REQUIERE = {"20": ["14", "15", "16", "17", "18"], "24": ["30", "31", "32", "36"], "46": ["40", "41", "42", "43"], "48": ["52"], "69": ["70"]}
