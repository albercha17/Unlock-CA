import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bot_core import *

# La solución sale de lo que dibuja herramientas/mosaicos.py, no de una copia escrita a mano.
CODIGOS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "codigos_pompeya.json"), encoding="utf-8"))


def clic(d, css):
    """Clic por JS: los elementos pueden estar dentro de contenedores con overflow oculto."""
    d.execute_script("arguments[0].click()", d.find_element(By.CSS_SELECTOR, css))
    time.sleep(0.05)


def secuencia(d, carta, clase, claves, malo, pista_fallo, boton_ok="Probar"):
    """Formas / flechas: primero una combinación mala (falla), luego la buena."""
    abrir_carta(d, carta)
    boton(d, boton_ok).click()
    assert "Faltan" in feedback(d), feedback(d)
    for _ in claves:
        clic(d, f".{clase}[data-k='{malo}']")
    boton(d, boton_ok).click()
    assert pista_fallo in feedback(d), feedback(d)
    boton(d, "Vaciar").click()
    for k in claves:
        clic(d, f".{clase}[data-k='{k}']")
    boton(d, boton_ok).click()
    m = feedback(d)
    cerrar(d)
    return m


def s20(d):
    return secuencia(d, "20", "pom-forma", CODIGOS["atrio"]["formas"], "cuadrado", "La puerta no cede")


def s24(d):
    return secuencia(d, "24", "pom-flecha", CODIGOS["peristilo"]["flechas"], "izquierda", "La verja no se mueve")


def s46(d):
    """Rosetas: tres ruedas; primero todas a 1 (falla) y luego sube cada una a su número de pétalos."""
    abrir_carta(d, "46")
    boton(d, "Abrir").click()
    assert "no se abre" in feedback(d), feedback(d)
    for i, n in enumerate(CODIGOS["rosetas"]["petalos"]):
        for _ in range(n - 1):
            clic(d, f".pom-rueda[data-i='{i}'] .mas")
    boton(d, "Abrir").click()
    m = feedback(d)
    cerrar(d)
    return m


def s48(d):
    """Ábaco: un número mal puesto y luego las cifras del fresco partido."""
    abrir_carta(d, "48")
    boton(d, "Abrir el cofre").click()
    assert "sigue cerrado" in feedback(d), feedback(d)
    for r, n in enumerate(CODIGOS["digitos"]["digitos"]):
        clic(d, f".pom-cuenta[data-r='{r}'][data-n='9']")
    boton(d, "Abrir el cofre").click()
    assert "sigue cerrado" in feedback(d), feedback(d)
    boton(d, "Vaciar").click()
    for r, n in enumerate(CODIGOS["digitos"]["digitos"]):
        clic(d, f".pom-cuenta[data-r='{r}'][data-n='{n}']")
    boton(d, "Abrir el cofre").click()
    m = feedback(d)
    cerrar(d)
    return m


def s69(d):
    """Reloj de sol: la marca 3 no es (falla) y luego la marca donde llega la sombra."""
    abrir_carta(d, "69")
    clic(d, ".pom-marca[data-k='3']")
    boton(d, "Girar la rueda").click()
    assert "Nada se mueve" in feedback(d), feedback(d)
    clic(d, f".pom-marca[data-k='{CODIGOS['reloj']['marca']}']")
    boton(d, "Girar la rueda").click()
    m = feedback(d)
    cerrar(d)
    return m


SOLVERS = {"20": s20, "24": s24, "46": s46, "48": s48, "69": s69}
# cartas que hay que tener en mesa para poder resolver cada minijuego (los mosaicos se montan en la mesa)
REQUIERE = {"20": ["14", "15", "16", "17", "18"], "24": ["30", "31", "32", "33", "36"], "46": ["40", "41", "42", "43", "45"],
            "48": ["52", "53"], "69": ["64", "65", "66", "67", "70"]}
