"""Solucionadores de los minijuegos de «Trono»: juegan cada app por la interfaz real (primero un fallo explicado, luego la solución)."""
import sys, time
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from bot_core import *

PALABRAS = {"14": "HIELO", "20": "SOLO", "40": "VENCERÁ", "46": "DEL", "51": "FUEGO", "64": "NORTE", "69": "AL", "72": "EL"}
FRASE = ["SOLO", "EL", "FUEGO", "VENCERÁ", "AL", "HIELO", "DEL", "NORTE"]


def clic(d, css):
    """Clic por JS: los elementos pueden estar dentro de contenedores con overflow oculto."""
    d.execute_script("arguments[0].click()", d.find_element(By.CSS_SELECTOR, css))
    time.sleep(0.05)


def ciclar(d, css, valor, veces=6):
    """Pulsa un botón de ciclo hasta que su atributo data-v valga `valor`."""
    for _ in range(veces):
        if d.find_element(By.CSS_SELECTOR, css).get_attribute("data-v") == valor:
            return
        clic(d, css)
    raise Fallo(f"no consigo poner «{valor}» en {css}")


def s42(d):
    abrir_carta(d, "42")
    for _ in range(2):
        boton(d, "Siguiente →").click()
    texto = d.find_element(By.CSS_SELECTOR, ".far-hoja").text
    assert "tres caminos" in texto and "cuatro" in texto, texto
    boton(d, "Siguiente →").click()
    cerrar(d)
    return "(lector) " + texto[:40]


def s14(d):
    """Cuervo: primero sin girar (falla) y luego tres puestos."""
    abrir_carta(d, "14")
    boton(d, "Leer el mensaje").click()
    assert "palabras con sentido" in feedback(d), feedback(d)
    for _ in range(3):
        clic(d, ".cue-mas")
    assert d.find_element(By.CSS_SELECTOR, ".cue-claro").text == "BAJAD AL ARCHIVO"
    boton(d, "Leer el mensaje").click()
    m = feedback(d)
    cerrar(d)
    return m


def s20(d):
    """Banquete: mesa vacía, dos casas intercambiadas (falla por una pista) y la solución."""
    abrir_carta(d, "20")
    boton(d, "Comprobar").click()
    assert "Falta decidir" in feedback(d), feedback(d)
    casas = ["León Dorado", "Lobo Gris", "Oso Pardo", "Halcón Plateado"]
    regalos = ["copa", "pieles", "espada", "cuerno"]
    mala = ["Lobo Gris", "León Dorado", "Oso Pardo", "Halcón Plateado"]   # el lobo a la izquierda del león: rompe una pista
    for s in range(4):
        ciclar(d, f".ban-casa[data-s='{s}']", mala[s])
        ciclar(d, f".ban-regalo[data-s='{s}']", regalos[s])
    boton(d, "Comprobar").click()
    assert "no encaja" in feedback(d), feedback(d)
    for s in range(4):
        ciclar(d, f".ban-casa[data-s='{s}']", casas[s])
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


PUENTES = [((1, 1), (1, 3), 1), ((1, 1), (2, 1), 1), ((1, 3), (1, 4), 1), ((1, 4), (1, 6), 1), ((2, 1), (6, 1), 2), ((6, 0), (6, 1), 1), ((6, 1), (6, 2), 1)]


def s40(d):
    """Caminos: sin caminos (falla) y los siete tramos (uno doble)."""
    abrir_carta(d, "40")
    boton(d, "Comprobar").click()
    assert "más o menos caminos" in feedback(d), feedback(d)
    for a, b, v in PUENTES:
        for _ in range(v):
            clic(d, f".cam-isla[data-k='{a[0]},{a[1]}']")
            clic(d, f".cam-isla[data-k='{b[0]},{b[1]}']")
    m = feedback(d)
    cerrar(d)
    return m


def s46(d):
    """Lengua: una palabra inventada, el orden mal y la frase buena."""
    abrir_carta(d, "46")
    campo = d.find_element(By.CSS_SELECTOR, ".len-in")

    def decir(t):
        campo.clear()
        campo.send_keys(t)
        boton(d, "Decirlo").click()
        time.sleep(0.1)
        return feedback(d)

    assert "no es la que espera" in decir("kra kra"), feedback(d)
    assert "orden" in decir("hod krai skai ven"), feedback(d)
    m = decir("krai skai hod ven")
    cerrar(d)
    return m


def s51(d):
    """Consejeros: todos leales (se contradice) y la solución."""
    abrir_carta(d, "51")
    boton(d, "Comprobar").click()
    assert "Falta decidir" in feedback(d), feedback(d)
    for i in range(4):
        clic(d, f".con-btn[data-i='{i}']")        # todos leales
    boton(d, "Comprobar").click()
    assert "se contradice" in feedback(d), feedback(d)
    for i in (0, 1):
        clic(d, f".con-btn[data-i='{i}']")        # leal -> traidor
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


ANTORCHAS = [(0, 1), (0, 3), (1, 4), (2, 0), (2, 5), (3, 1), (3, 4), (4, 2), (5, 0)]


def s64(d):
    """Antorchas: sin ninguna (a oscuras), dos que se ven y la solución."""
    abrir_carta(d, "64")
    boton(d, "Comprobar").click()
    assert "a oscuras" in feedback(d), feedback(d)
    clic(d, ".ant-cel[data-c='0,3']")
    clic(d, ".ant-cel[data-c='0,4']")
    boton(d, "Comprobar").click()
    assert "entre sí" in feedback(d), feedback(d)
    clic(d, ".ant-cel[data-c='0,3']")
    clic(d, ".ant-cel[data-c='0,4']")
    for r, c in ANTORCHAS:
        clic(d, f".ant-cel[data-c='{r},{c}']")
    m = feedback(d)
    cerrar(d)
    return m


RUTA_PUERTA = [(4, -1), (4, -1), (1, 1), (1, 1), (1, 1), (5, -1), (0, 1), (0, 1), (0, 1), (0, 1)]


def s69(d):
    """Puerta: intentar mover el ariete bloqueado y los diez movimientos."""
    abrir_carta(d, "69")
    clic(d, ".pue-pieza[data-i='0']")
    clic(d, ".pue-mas")
    assert "no puede moverse" in feedback(d), feedback(d)
    for i, paso in RUTA_PUERTA:
        clic(d, f".pue-pieza[data-i='{i}']")
        clic(d, ".pue-mas" if paso > 0 else ".pue-menos")
    m = feedback(d)
    cerrar(d)
    return m


TAPIZ = ["..##..", ".####.", "######", "##..##", ".####.", "..##.."]


def s72(d):
    """Tapiz: sin pintar, una casilla mal puesta y el dibujo."""
    abrir_carta(d, "72")
    boton(d, "Comprobar").click()
    assert "Todavía no" in feedback(d), feedback(d)
    clic(d, ".tap-cel[data-i='0']")
    boton(d, "Comprobar").click()
    assert "no coincide" in feedback(d), feedback(d)
    clic(d, ".tap-cel[data-i='0']")
    clic(d, ".tap-cel[data-i='0']")             # pintada -> cruz -> vacía
    for r, fila in enumerate(TAPIZ):
        for c, ch in enumerate(fila):
            if ch == "#":
                clic(d, f".tap-cel[data-i='{r * 6 + c}']")
    m = feedback(d)
    cerrar(d)
    return m


def s84(d):
    """Profecía: con las ocho palabras guardadas, un orden malo y el bueno. También prueba la falta de palabras."""
    d.execute_script("Object.keys(localStorage).filter(k => k.startsWith('ca-palabra:trono:')).forEach(k => localStorage.removeItem(k))")
    abrir_carta(d, "84")
    boton(d, "Comprobar").click()
    assert "faltan palabras" in feedback(d).lower(), feedback(d)
    cerrar(d)
    for carta, w in PALABRAS.items():
        d.execute_script("localStorage.setItem('ca-palabra:trono:' + arguments[0], arguments[1])", carta, w)
    abrir_carta(d, "84")
    mala = list(FRASE)
    mala[1], mala[2] = mala[2], mala[1]
    for w in mala:
        clic(d, f".pro-ficha[data-w='{w}']")
    boton(d, "Comprobar").click()
    assert "no encaja" in feedback(d), feedback(d)
    boton(d, "Quitar todas").click()
    for w in FRASE:
        clic(d, f".pro-ficha[data-w='{w}']")
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


SOLVERS = {"14": s14, "20": s20, "42": s42, "40": s40, "46": s46, "51": s51, "64": s64, "69": s69, "72": s72, "84": s84}
REQUIERE = {"14": ["16"], "20": ["18"], "40": ["42"], "46": ["48", "37"], "51": ["52", "26"], "64": ["66"], "69": ["70"], "72": ["76"], "84": ["86"]}
