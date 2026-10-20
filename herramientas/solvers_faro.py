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


# ---- ampliación a 36 cartas: la bahía, la lámpara de la mesa y el temporizador de la lente
import json as _json, os  # noqa: E402
_AMP = _json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "instancias_ampliacion.json"), encoding="utf-8"))


def _clic(d, css):
    d.execute_script("arguments[0].click()", d.find_element(By.CSS_SELECTOR, css))
    time.sleep(0.04)


def s45(d):
    """Bahía: sin islotes (falla) y luego los islotes de la solución."""
    abrir_carta(d, "45")
    boton(d, "Transmitir").click()
    assert "no cuadra" in feedback(d), feedback(d)
    for f, c in _AMP["faro_bahia"]["tierra"]:
        _clic(d, f".far-cas[data-f='{f}'][data-c='{c}']")
    boton(d, "Transmitir").click()
    m = feedback(d)
    cerrar(d)
    return m


def s55(d):
    """Lámpara: las tres cosas en otro orden (falla) y luego en el orden de la sombra."""
    abrir_carta(d, "55")
    sol = _AMP["faro_sombras"]["solucion"]
    for o in sol[::-1]:
        _clic(d, f".far-obj[data-o='{o}']")
    boton(d, "Encender la lámpara").click()
    assert "no es la de la pared" in feedback(d), feedback(d)
    for i in range(3):
        _clic(d, ".far-hueco[data-i='0']")
    for o in sol:
        _clic(d, f".far-obj[data-o='{o}']")
    boton(d, "Encender la lámpara").click()
    m = feedback(d)
    cerrar(d)
    return m


def s65(d):
    """Temporizador: todo apagado (falla) y luego los segundos de la luz de Cabo Niebla."""
    abrir_carta(d, "65")
    boton(d, "Programar").click()
    assert "otro faro" in feedback(d), feedback(d)
    for s, v in enumerate(_AMP["faro_destellos"]["solucion"]):
        if v:
            _clic(d, f".far-seg[data-s='{s}']")
    boton(d, "Programar").click()
    m = feedback(d)
    cerrar(d)
    return m


SOLVERS.update({"45": s45, "55": s55, "65": s65})
REQUIERE.update({"45": ["46", "47"], "55": ["56", "57"], "65": ["66", "67"]})
