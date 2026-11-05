"""Solucionadores de los minijuegos de «El primer salto» (nivel de prueba): juegan cada app por la interfaz real, con una jugada mala antes de la buena."""
import sys, time
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from bot_core import *
import instancias_cronoportal as I

D = I.INST


def clic(d, css):
    d.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}))", d.find_element(By.CSS_SELECTOR, css))
    time.sleep(0.03)


def teclea(d, texto):
    for ch in texto:
        tecla(d, ch)


def s14(d):
    """Vitrina: código corto (avisa), código equivocado (falla) y los engranajes contados."""
    abrir_carta(d, "14")
    cod = D["cerradura"]["codigo"]
    teclea(d, "1")
    tecla(d, "✓")
    assert "ruedas" in feedback(d), feedback(d)
    teclea(d, "000"[:len(cod) - 1])
    tecla(d, "⌫")
    tecla(d, "⌫")
    teclea(d, "0" * (len(cod) - 0))
    tecla(d, "✓")
    assert "no se abre" in feedback(d), feedback(d)
    teclea(d, cod)
    tecla(d, "✓")
    m = feedback(d)
    cerrar(d)
    return m


def s20(d):
    """Plano: pocos símbolos (avisa), orden equivocado (falla) y el camino del plano."""
    abrir_carta(d, "20")
    sol = D["mapa"]["solucion"]
    clic(d, f".map-b button[data-s='{sol[0]}']")
    boton(d, "Calibrar").click()
    assert "Faltan" in feedback(d), feedback(d)
    boton(d, "Borrar").click()
    for s in sol[::-1]:
        clic(d, f".map-b button[data-s='{s}']")
    boton(d, "Calibrar").click()
    assert "no es el camino" in feedback(d), feedback(d)
    boton(d, "Borrar").click()
    for s in sol:
        clic(d, f".map-b button[data-s='{s}']")
    boton(d, "Calibrar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s85(d):
    """Panel: cifras en el orden equivocado (falla) y en el bueno."""
    abrir_carta(d, "85")
    cod = D["meta"]["codigo"]
    teclea(d, cod[::-1] if cod[::-1] != cod else "00")
    tecla(d, "✓")
    assert "zumba" in feedback(d), feedback(d)
    teclea(d, cod)
    tecla(d, "✓")
    m = feedback(d)
    cerrar(d)
    return m


SOLVERS = {"14": s14, "20": s20, "85": s85}
REQUIERE = {"14": ["16"], "20": ["18", "19", "21"], "85": ["86"]}
