import sys, time
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from bot_core import *


def s15(d):
    abrir_carta(d, "15")
    for _ in range(3):
        boton(d, "Siguiente →").click()
    texto = d.find_element(By.CSS_SELECTOR, ".far-hoja").text
    cerrar(d)
    return "(lector) " + texto[:40]


def s36(d):
    abrir_carta(d, "36")
    for ch in "0435":
        tecla(d, ch)
    tecla(d, "✓")
    m = feedback(d)
    cerrar(d)
    return m


def s52(d):
    abrir_carta(d, "52")
    for ch in "ANCLA":
        tecla(d, ch)
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s85(d):
    abrir_carta(d, "85")
    grande = d.find_element(By.CSS_SELECTOR, ".far-knob.grande")
    fina = d.find_element(By.CSS_SELECTOR, ".far-knob.fino")
    from selenium.webdriver.common.keys import Keys
    for _ in range(120):
        f = float(d.find_element(By.ID, "farReadout").text.split()[0])
        if abs(f - 91.7) < 0.06:
            break
        dif = 91.7 - f
        rueda = grande if abs(dif) > 1.0 else fina
        rueda.send_keys(Keys.ARROW_RIGHT if dif > 0 else Keys.ARROW_LEFT)
    time.sleep(1.4)
    m = feedback(d)
    cerrar(d)
    return m


# Espejos que toca el rayo en la solucion (columna,fila desde 0)
SOL70 = {"1,3": "/", "1,2": "/", "3,2": "/", "3,1": "/", "6,1": "\\", "6,2": "/", "5,2": "/"}


def s70(d):
    abrir_carta(d, "70")
    assert feedback(d) == "", "el puzle de los espejos no debe empezar resuelto"

    def girar(celda):
        js(d, "document.querySelector(\".far-m-hot[data-c='%s']\").dispatchEvent(new MouseEvent('click',{bubbles:true}));" % celda)
        time.sleep(0.08)

    def estado(celda):
        return d.find_element(By.CSS_SELECTOR, ".far-mirror[data-c='%s']" % celda).get_attribute("data-o")

    girar("0,2")                                   # un senuelo no resuelve nada
    girar("0,2")
    assert feedback(d) == ""
    for celda, orient in SOL70.items():
        if estado(celda) != orient:
            girar(celda)
    time.sleep(0.5)
    m = feedback(d)
    cerrar(d)
    return m


def s95(d):
    abrir_carta(d, "95")
    for paso in ["Abrir la válvula del aceite", "Cebar la mecha", "Girar el engranaje", "Encender el piloto", "Soltar el freno de la lente"]:
        d.find_element(By.XPATH, f"//button[contains(@class,'far-step')][.//span[text()='{paso}']]").click()
    boton(d, "Arrancar").click()
    m = feedback(d)
    cerrar(d)
    return m


SOLVERS = {"15": s15, "36": s36, "52": s52, "85": s85, "70": s70, "95": s95}
REQUIERE = {"36": ["21", "19"], "52": ["15"], "85": ["74", "3"], "70": ["27"], "95": ["15", "12", "18", "82"]}
