import sys, time
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from bot_core import *


def s33(d):
    abrir_carta(d, "35")
    for _ in range(3):
        boton(d, "Siguiente →").click()
    texto = d.find_element(By.CSS_SELECTOR, ".far-hoja").text
    cerrar(d)
    return "(lector) " + texto[:40]


def s21(d):
    abrir_carta(d, "21")
    for ch in "1346":
        tecla(d, ch)
    tecla(d, "✓")
    hist = d.find_element(By.CSS_SELECTOR, ".far-term").text
    assert "1 3 4 6" in hist and "○" in hist, hist
    for ch in "4163":
        tecla(d, ch)
    tecla(d, "✓")
    m = feedback(d)
    cerrar(d)
    return m


def s52(d):
    abrir_carta(d, "52")
    # (indice de casilla, clics): ver GRID de 52-tuberias.js
    for idx, clics in [(1, 2), (2, 1), (3, 2), (5, 1), (6, 2), (8, 1), (9, 3), (13, 2), (14, 3)]:
        for _ in range(clics):
            d.find_element(By.CSS_SELECTOR, ".mar-celda[data-i='%d']" % idx).click()
            time.sleep(0.05)
    time.sleep(0.2)
    m = feedback(d)
    cerrar(d)
    return m


def s66(d):
    abrir_carta(d, "66")
    boton(d, "Abrir esclusa").click()
    assert "incorrecto" in feedback(d)
    for i in (0, 2, 4, 5, 7):   # 128 + 32 + 8 + 4 + 1 = 173
        js(d, "document.querySelectorAll('.far-bit')[%d].click();" % i)
        time.sleep(0.05)
    assert "173" in d.find_element(By.CSS_SELECTOR, ".far-valor").text
    boton(d, "Abrir esclusa").click()
    m = feedback(d)
    cerrar(d)
    return m


def s88(d):
    abrir_carta(d, "88")
    def poner(i, v):
        js(d, f"var e=document.getElementById('{i}'); e.value='{v}'; e.dispatchEvent(new Event('input'));")
    poner("marAmp", 3)
    boton(d, "Calibrar").click()
    assert "INESTABLE" in feedback(d)
    poner("marFrec", 5)
    poner("marFase", 1)
    boton(d, "Calibrar").click()
    assert "INESTABLE" in feedback(d), "con la fase 1 no debe calibrar"
    poner("marFase", 2)
    boton(d, "Calibrar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s48(d):
    """Rover: busca una ruta con BFS sobre el mapa (7x5, rocas, de A5 a F2) y la programa con las flechas."""
    from collections import deque
    abrir_carta(d, "48")
    rocas = {(1, 1), (3, 1), (3, 2), (1, 3), (5, 3), (4, 4)}
    inicio, meta = (0, 4), (5, 1)
    dirs = {"↑": (0, -1), "↓": (0, 1), "←": (-1, 0), "→": (1, 0)}
    previo = {inicio: None}
    cola = deque([inicio])
    while cola:
        p = cola.popleft()
        if p == meta:
            break
        for f, (dc, dr) in dirs.items():
            q = (p[0] + dc, p[1] + dr)
            if 0 <= q[0] < 7 and 0 <= q[1] < 5 and q not in rocas and q not in previo:
                previo[q] = (p, f)
                cola.append(q)
    ruta, p = [], meta
    while previo[p] is not None:
        p, f = previo[p]
        ruta.append(f)
    ruta.reverse()
    # primero un intento malo contra una roca: sube tres (A2) y gira hacia B2, que es una roca
    for f in ["↑", "↑", "↑", "→"]:
        d.find_element(By.XPATH, f"//button[@aria-label='Añadir {f}']").click()
    boton(d, "Ejecutar").click()
    for _ in range(40):
        time.sleep(0.2)
        if "roca" in feedback(d):
            break
    assert "roca" in feedback(d) or "borde" in feedback(d), feedback(d)
    time.sleep(0.9)   # el rover termina de sacudirse antes de aceptar ordenes
    boton(d, "Reiniciar").click()
    for f in ruta:
        d.find_element(By.XPATH, f"//button[@aria-label='Añadir {f}']").click()
    boton(d, "Ejecutar").click()
    m = ""
    for _ in range(60):
        time.sleep(0.2)
        m = feedback(d)
        if "baliza" in m and "¡" in m:
            break
    cerrar(d)
    return m


def s62(d):
    abrir_carta(d, "62")
    def sis(i):
        d.find_element(By.CSS_SELECTOR, f".far-sis[data-sis='{i}']").click()
    sis("radio"); sis("luz")
    boton(d, "Conectar").click()
    assert "escudo" in feedback(d).lower(), feedback(d)
    sis("luz"); sis("escudo")                     # escudo + radio = 12
    boton(d, "Conectar").click()
    assert "no arranca" in feedback(d), feedback(d)
    sis("luz")                                    # escudo + radio + luz = 15
    boton(d, "Conectar").click()
    m = feedback(d)
    cerrar(d)
    return m


SOLVERS = {"35": s33, "21": s21, "52": s52, "66": s66, "88": s88, "48": s48, "62": s62}
REQUIERE = {"21": ["25"], "66": ["28", "40"], "48": ["57"], "62": ["59"], "88": ["35", "36", "51"]}
