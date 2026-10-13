import sys, time
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from bot_core import *


def clic(d, css):
    """Clic por JS: los elementos pueden estar dentro de contenedores con overflow oculto."""
    d.execute_script("arguments[0].click()", d.find_element(By.CSS_SELECTOR, css))
    time.sleep(0.05)


def s42(d):
    abrir_carta(d, "42")
    for _ in range(3):
        boton(d, "Siguiente →").click()
    texto = d.find_element(By.CSS_SELECTOR, ".far-hoja").text
    cerrar(d)
    return "(lector) " + texto[:40]


def s14(d):
    """Huellas: primero todas con el mismo nombre (falla) y luego las cuatro bien."""
    abrir_carta(d, "14")
    boton(d, "Comprobar").click()
    assert "Falta poner nombre" in feedback(d), feedback(d)
    solucion = ["Triceratops", "Tiranosaurio", "Anquilosaurio", "Edmontosaurio"]

    def poner(i, esp):
        for _ in range(6):
            if d.find_element(By.CSS_SELECTOR, f".din-huella[data-i='{i}']").get_attribute("data-esp") == esp:
                return
            clic(d, f".din-huella[data-i='{i}']")
        raise Fallo(f"no consigo poner {esp} en la huella {i}")

    for i in range(4):
        poner(i, "Tiranosaurio")
    boton(d, "Comprobar").click()
    assert "no corresponde" in feedback(d), feedback(d)
    for i, esp in enumerate(solucion):
        poner(i, esp)
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


HUESOS = [(1, 1), (2, 3), (3, 0), (3, 4), (4, 1), (4, 2), (5, 4)]


def s20(d):
    """Excavacion: sin marcas, con un hueso mal puesto y por fin la solucion."""
    abrir_carta(d, "20")
    boton(d, "Comprobar").click()
    assert "siete huesos" in feedback(d), feedback(d)
    for c, r in HUESOS:
        clic(d, f".exc-cell[data-c='{c},{r}']")
    clic(d, ".exc-cell[data-c='3,0']")      # lo quita...
    clic(d, ".exc-cell[data-c='2,0']")      # ...y pone otro mal
    boton(d, "Comprobar").click()
    assert "no cuadra" in feedback(d), feedback(d)
    clic(d, ".exc-cell[data-c='2,0']")
    clic(d, ".exc-cell[data-c='3,0']")
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s40(d):
    """Balsa: un primer viaje vacio deja al compsognato con el bebe (falla) y luego los siete viajes buenos."""
    abrir_carta(d, "40")
    boton(d, "Cruzar el río").click()
    time.sleep(1.4)
    assert "se abalanza" in feedback(d), feedback(d)
    for k in [None, "compsognato"]:
        pass
    viajes = ["driosaurio", None, "compsognato", "driosaurio", "helechos", None, "driosaurio"]
    for k in viajes:
        if k:
            clic(d, f".bal-item[data-k='{k}']")
        boton(d, "Cruzar el río").click()
        time.sleep(1.25)
    m = feedback(d)
    cerrar(d)
    return m


def s46(d):
    """ADN: una cadena mala y luego T A C G G C A T."""
    abrir_carta(d, "46")
    boton(d, "Secuenciar").click()
    assert "incompleta" in feedback(d), feedback(d)
    for _ in range(8):
        clic(d, ".adn-base[data-b='A']")
    boton(d, "Secuenciar").click()
    assert "no reconoce" in feedback(d), feedback(d)
    for _ in range(8):
        boton(d, "Borrar").click()
    for b in "TACGGCAT":
        clic(d, f".adn-base[data-b='{b}']")
    boton(d, "Secuenciar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s51(d):
    """Estratos: ordena por seleccion (intercambios) hasta ceniza, carbon, arenisca, arcilla, caliza, conchas."""
    abrir_carta(d, "51")
    boton(d, "Comprobar").click()
    assert "no coincide" in feedback(d), feedback(d)
    meta = ["ceniza", "carbon", "arenisca", "arcilla", "caliza", "conchas"]
    for i, k in enumerate(meta):
        actual = [e.get_attribute("data-n") for e in d.find_elements(By.CSS_SELECTOR, ".est-capa")]
        j = actual.index(k)
        if j != i:
            clic(d, f".est-capa[data-pos='{i}']")
            clic(d, f".est-capa[data-pos='{j}']")
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s64(d):
    """Cristales: pulsa B1, A2, B2, A3 y D3 (indices 1, 4, 5, 8, 11)."""
    abrir_carta(d, "64")
    clic(d, ".cri-cell[data-i='0']")
    boton(d, "Apagar todo").click()
    for i in (1, 4, 5, 8, 11):
        clic(d, f".cri-cell[data-i='{i}']")
    time.sleep(0.2)
    m = feedback(d)
    cerrar(d)
    return m


def hanoi(n, a, c, b, movs):
    if n == 0:
        return
    hanoi(n - 1, a, b, c, movs)
    movs.append((a, c))
    hanoi(n - 1, b, c, a, movs)


def s69(d):
    """Nidos: un movimiento prohibido y luego los quince movimientos de las torres de Hanoi."""
    abrir_carta(d, "69")
    nidos = ["ramas", "piedras", "plumas"]

    def mover(a, b):
        clic(d, f".nid-nido[data-n='{nidos[a]}']")
        clic(d, f".nid-nido[data-n='{nidos[b]}']")

    mover(0, 1)
    mover(0, 1)         # el segundo huevo sobre el pequeno: prohibido
    assert "aplastaría" in feedback(d), feedback(d)
    boton(d, "Empezar de nuevo").click()
    movs = []
    hanoi(4, 0, 2, 1, movs)
    assert len(movs) == 15
    for a, b in movs:
        mover(a, b)
    time.sleep(0.2)
    m = feedback(d)
    cerrar(d)
    return m


def s72(d):
    """Geiser: primero sin tocar nada (falla) y luego valvulas 3, 1 y 4."""
    abrir_carta(d, "72")
    boton(d, "Comprobar presión").click()
    assert "no marcan" in feedback(d), feedback(d)
    for i, veces in enumerate([3, 1, 4]):
        for _ in range(veces):
            clic(d, f".gei-valv[data-v='{i}'] .gei-mas")
    boton(d, "Comprobar presión").click()
    m = feedback(d)
    cerrar(d)
    return m


def s84(d):
    """Esqueleto: falta de piezas, cadena mala y cadena buena."""
    abrir_carta(d, "84")
    boton(d, "Comprobar").click()
    assert "Faltan huesos" in feedback(d), feedback(d)

    def poner(lista):
        for n in lista:
            clic(d, f".esq-bandeja .esq-hueso[data-n='{n}']")

    poner(["cuello", "intruso1", "torso", "cadera", "cola"])
    boton(d, "Comprobar").click()
    assert "no encaja" in feedback(d), feedback(d)
    boton(d, "Vaciar").click()
    poner(["cuello", "torso", "cadera", "cola", "punta"])
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


SOLVERS = {"42": s42, "14": s14, "20": s20, "40": s40, "46": s46, "51": s51, "64": s64, "69": s69, "72": s72, "84": s84}
REQUIERE = {"14": ["16"], "20": ["18"], "40": ["42"], "46": ["48", "37"], "51": ["52", "26"], "64": ["66"], "69": ["70"], "72": ["76"], "84": ["86"]}
