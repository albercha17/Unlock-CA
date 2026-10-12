import sys, time
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from bot_core import *


def s33(d):
    abrir_carta(d, "33")
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
            js(d, "document.querySelectorAll('svg rect[fill=transparent]')[%d].dispatchEvent(new MouseEvent('click',{bubbles:true}));" % idx)
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
    js(d, "var a=document.getElementById('marAmp'); a.value='3'; a.dispatchEvent(new Event('input'));")
    boton(d, "Calibrar").click()
    assert "INESTABLE" in feedback(d)
    js(d, "var f=document.getElementById('marFrec'); f.value='5'; f.dispatchEvent(new Event('input'));")
    boton(d, "Calibrar").click()
    m = feedback(d)
    cerrar(d)
    return m


SOLVERS = {"33": s33, "21": s21, "52": s52, "66": s66, "88": s88}
REQUIERE = {"21": ["25"], "66": ["28", "40"], "88": ["33", "36"]}
