"""Solucionadores de los minijuegos de «El Faro de Cabo Niebla» (60 cartas): juegan cada app por la interfaz real, primero una jugada mala para comprobar
el aviso y luego la buena. Las soluciones salen de instancias_faro.py."""
import sys, time
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from bot_core import *
import instancias_faro as I

D = I.INST


def clic(d, css):
    """Clic por JS: los elementos pueden estar dentro de contenedores con overflow oculto."""
    d.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}))", d.find_element(By.CSS_SELECTOR, css))
    time.sleep(0.03)


def teclea(d, texto):
    for ch in texto:
        tecla(d, ch)


def s14(d):
    """Puerta: código equivocado (falla) y la hora real."""
    abrir_carta(d, "14")
    teclea(d, "0435")
    tecla(d, "✓")
    assert "incorrecto" in feedback(d), feedback(d)
    teclea(d, D["puerta"]["codigo"])
    tecla(d, "✓")
    m = feedback(d)
    cerrar(d)
    return m


def s20(d):
    """Banderas: palabra corta (avisa), palabra equivocada (falla) y la buena."""
    abrir_carta(d, "20")
    P = D["banderas"]["palabra"]
    teclea(d, "AB")
    boton(d, "Comprobar").click()
    assert "letras" in feedback(d), feedback(d)
    for _ in range(2):
        boton(d, "Borrar").click()
    teclea(d, "A" * len(P))
    boton(d, "Comprobar").click()
    assert "no es" in feedback(d), feedback(d)
    for _ in range(len(P)):
        boton(d, "Borrar").click()
    teclea(d, P)
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s40(d):
    """Radio: se gira hasta la frecuencia de Cabo Niebla."""
    abrir_carta(d, "40")
    obj = D["radio"]["objetivo"]
    grande = d.find_element(By.CSS_SELECTOR, ".far-knob.grande")
    fina = d.find_element(By.CSS_SELECTOR, ".far-knob.fino")
    from selenium.webdriver.common.keys import Keys
    for _ in range(160):
        f = float(d.find_element(By.ID, "farReadout").text.split()[0])
        if abs(f - obj) < 0.06:
            break
        dif = obj - f
        rueda = grande if abs(dif) > 1.0 else fina
        rueda.send_keys(Keys.ARROW_RIGHT if dif > 0 else Keys.ARROW_LEFT)
    time.sleep(1.4)
    m = feedback(d)
    cerrar(d)
    return m


def s48(d):
    """Morse: palabra equivocada (falla) y la palabra sin los destellos rojos."""
    abrir_carta(d, "48")
    P = D["morse"]["palabra"]
    teclea(d, "A" * len(P))
    boton(d, "Comprobar").click()
    assert "no es" in feedback(d), feedback(d)
    for _ in range(len(P)):
        boton(d, "Borrar").click()
    teclea(d, P)
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s52(d):
    """Bahía: sin islotes (falla) y luego los islotes de la solución."""
    abrir_carta(d, "52")
    boton(d, "Transmitir").click()
    assert "no cuadra" in feedback(d), feedback(d)
    for f, c in D["bahia"]["tierra"]:
        clic(d, f".far-cas[data-f='{f}'][data-c='{c}']")
    boton(d, "Transmitir").click()
    m = feedback(d)
    cerrar(d)
    return m


def s46(d):
    """Sombras: faltan cosas (avisa), cuatro en otro orden (falla) y luego en el orden de la sombra."""
    abrir_carta(d, "46")
    sol = D["sombras"]["solucion"]
    boton(d, "Encender la lámpara").click()
    assert "Hacen falta" in feedback(d), feedback(d)
    for o in sol[::-1]:
        clic(d, f".far-obj[data-o='{o}']")
    boton(d, "Encender la lámpara").click()
    assert "no es la de la pared" in feedback(d), feedback(d)
    for _ in sol:
        clic(d, ".far-hueco[data-i='0']")
    for o in sol:
        clic(d, f".far-obj[data-o='{o}']")
    boton(d, "Encender la lámpara").click()
    m = feedback(d)
    cerrar(d)
    return m


def s51(d):
    """Temporizador: todo apagado (falla) y luego los segundos de la luz de Cabo Niebla."""
    abrir_carta(d, "51")
    boton(d, "Programar").click()
    assert "otro faro" in feedback(d), feedback(d)
    for s, v in enumerate(D["destellos"]["solucion"]):
        if v:
            clic(d, f".far-seg[data-s='{s}']")
    boton(d, "Programar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s64(d):
    """Guardianes: sin rellenar (avisa) y luego cada nombre y cada gorro de la solución."""
    abrir_carta(d, "64")
    G = D["guardianes"]
    boton(d, "Comprobar").click()
    assert "Faltan" in feedback(d), feedback(d)
    for i, (nom, gor) in enumerate(G["solucion"]):
        for _ in range(6):
            b = d.find_element(By.CSS_SELECTOR, f".gua-n[data-n='{i}']")
            if b.text == nom:
                break
            clic(d, f".gua-n[data-n='{i}']")
        for _ in range(6):
            b = d.find_element(By.CSS_SELECTOR, f".gua-g[data-g='{i}']")
            if (b.get_attribute("aria-label") or "").endswith(": " + gor):
                break
            clic(d, f".gua-g[data-g='{i}']")
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s69(d):
    """Desván: chocar con la pared del borde (avisa) y luego las órdenes de la solución."""
    abrir_carta(d, "69")
    clic(d, ".des-b button[data-o='I']")
    clic(d, ".des-b button[data-o='A']")
    assert "Chocáis" in feedback(d), feedback(d)
    boton(d, "Volver a la entrada").click()
    for o in D["laberinto"]["solucion"]:
        clic(d, f".des-b button[data-o='{o}']")
    m = feedback(d)
    cerrar(d)
    return m


def s72(d):
    """Espejos: girar un señuelo dos veces no resuelve nada; luego los espejos que toca el rayo."""
    abrir_carta(d, "72")
    assert feedback(d) == "", "el puzle de los espejos no debe empezar resuelto"

    def girar(celda):
        clic(d, f".far-m-hot[data-c='{celda}']")
        time.sleep(0.05)
    girar("0,2")
    girar("0,2")
    assert feedback(d) == ""
    for celda in D["espejos"]["giran"]:
        girar(celda)
    time.sleep(0.5)
    m = feedback(d)
    cerrar(d)
    return m


def s85(d):
    """Panel: combinación equivocada (falla) y la combinación de las cinco cifras."""
    abrir_carta(d, "85")
    teclea(d, "00000")
    tecla(d, "✓")
    assert "no es la combinación" in feedback(d), feedback(d)
    teclea(d, D["meta"]["codigo"])
    tecla(d, "✓")
    m = feedback(d)
    cerrar(d)
    return m


SOLVERS = {"14": s14, "20": s20, "40": s40, "48": s48, "52": s52, "46": s46, "51": s51, "64": s64, "69": s69, "72": s72, "85": s85}
# cartas que hay que tener en mesa para poder resolver cada minijuego
REQUIERE = {"14": ["16"], "20": ["18", "19", "21"], "40": ["41", "43", "45"], "48": ["42", "49", "53"], "52": ["54", "55", "59"], "46": ["37", "39", "33"],
            "51": ["26", "61", "63"], "64": ["66", "67"], "69": ["70", "71"], "72": ["75", "79"], "85": ["86", "87"]}
