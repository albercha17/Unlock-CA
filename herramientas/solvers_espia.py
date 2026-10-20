import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bot_core import *
import instancias_espia as I

# Las soluciones salen de lo que dibuja herramientas/espia.py y de lo que calcula instancias_espia.py, no de copias escritas a mano.
AQUI = os.path.dirname(os.path.abspath(__file__))
COD = json.load(open(os.path.join(AQUI, "codigos_espia.json"), encoding="utf-8"))
INST = json.load(open(os.path.join(AQUI, "instancias_espia.json"), encoding="utf-8"))


def clic(d, css):
    """Clic por JS: los elementos pueden estar dentro de contenedores con overflow oculto."""
    d.execute_script("arguments[0].click()", d.find_element(By.CSS_SELECTOR, css))
    time.sleep(0.05)


def s20(d):
    """Caja: sin cifras, un número malo y luego el que se ve al superponer las hojas."""
    abrir_carta(d, "20")
    boton(d, "Abrir").click()
    assert "Faltan cifras" in feedback(d), feedback(d)
    for ch in "000":
        clic(d, f".esp-tecla[data-k='{ch}']")
    boton(d, "Abrir").click()
    assert "no es ese" in feedback(d), feedback(d)
    for _ in range(3):
        boton(d, "Borrar").click()
    for ch in "".join(str(x) for x in COD["cripto"]["digitos"]):
        clic(d, f".esp-tecla[data-k='{ch}']")
    boton(d, "Abrir").click()
    m = feedback(d)
    cerrar(d)
    return m


def s24(d):
    """Teletipo: sin letras, una palabra mala y luego la que se lee por las ventanas."""
    abrir_carta(d, "24")
    boton(d, "Enviar").click()
    assert "Faltan letras" in feedback(d), feedback(d)
    pal = COD["rejilla"]["palabra"]
    for _ in pal:
        clic(d, ".esp-letra[data-k='Q']")
    boton(d, "Enviar").click()
    assert "sin sentido" in feedback(d), feedback(d)
    for _ in pal:
        boton(d, "Borrar").click()
    for ch in pal:
        clic(d, f".esp-letra[data-k='{ch}']")
    boton(d, "Enviar").click()
    m = feedback(d)
    cerrar(d)
    return m


ETIQ = {"arriba": "Arriba", "abajo": "Abajo", "izquierda": "Izquierda", "derecha": "Derecha"}


def s46(d):
    """Pasillos: un choque contra un muro (la entrada solo se abre hacia la derecha) y luego el camino del plano."""
    abrir_carta(d, "46")
    boton(d, "Abajo").click()
    assert "Pum" in feedback(d), feedback(d)
    ruta = INST["laberinto"]["ruta"]
    for (f0, c0), (f1, c1) in zip(ruta, ruta[1:]):
        mov = "abajo" if f1 > f0 else "arriba" if f1 < f0 else "derecha" if c1 > c0 else "izquierda"
        boton(d, ETIQ[mov]).click()
        time.sleep(0.03)
    m = feedback(d)
    cerrar(d)
    return m


def _poner(d, f, c, h):
    for _ in range(h):
        clic(d, f".esp-edificio[data-f='{f}'][data-c='{c}']")


def s48(d):
    """Skyline: vacío, con repeticiones, un cuadrado latino que no cuadra con las pistas y luego la solución."""
    abrir_carta(d, "48")
    boton(d, "Comprobar").click()
    assert "Faltan edificios" in feedback(d), feedback(d)
    for f in range(4):
        for c in range(4):
            _poner(d, f, c, 1)
    boton(d, "Comprobar").click()
    assert "repetidas" in feedback(d), feedback(d)
    boton(d, "Vaciar").click()
    sol = INST["rascacielos"]["solucion"]
    otro = [[(f + c) % 4 + 1 for c in range(4)] for f in range(4)]
    if otro == sol:
        otro = [[(f + c + 1) % 4 + 1 for c in range(4)] for f in range(4)]
    for f in range(4):
        for c in range(4):
            _poner(d, f, c, otro[f][c])
    boton(d, "Comprobar").click()
    assert "no cuadra" in feedback(d), feedback(d)
    boton(d, "Vaciar").click()
    for f in range(4):
        for c in range(4):
            _poner(d, f, c, sol[f][c])
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s69(d):
    """Desactivador: lee los colores de cada carga de la pantalla y aplica las reglas del manual (primero un cable equivocado en la primera carga)."""
    abrir_carta(d, "69")
    for r in range(4):
        cables = [e.get_attribute("data-c") for e in d.find_elements(By.CSS_SELECTOR, f".esp-carga[data-r='{r}'] .esp-cable")]
        regla, i = I.regla_cable(cables)
        if r == 0:
            mal = (i + 1) % 5
            clic(d, f".esp-carga[data-r='0'] .esp-cable[data-i='{mal}']")
            assert "parpadea" in feedback(d), feedback(d)
        clic(d, f".esp-carga[data-r='{r}'] .esp-cable[data-i='{i}']")
    m = feedback(d)
    cerrar(d)
    return m


SOLVERS = {"20": s20, "24": s24, "46": s46, "48": s48, "69": s69}
# cartas que hay que tener en mesa para poder resolver cada minijuego
REQUIERE = {"20": ["14", "15"], "24": ["30", "31"], "46": ["40"], "48": ["52", "53"], "69": ["70"]}


# ---- ampliación a 36 cartas: el marcador del crupier
import json as _json  # noqa: E402
_AMP = _json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "instancias_ampliacion.json"), encoding="utf-8"))


def s36(d):
    """Póker: en el orden en que salen (falla) y luego de mejor a peor mano."""
    abrir_carta(d, "36")
    po = _AMP["espia_poker"]
    malo = po["jugadores"] if po["jugadores"] != po["orden"] else po["jugadores"][::-1]
    for j in malo:
        clic(d, f".esp-jug[data-j='{j}']")
    boton(d, "Entregar").click()
    assert "niega" in feedback(d), feedback(d)
    boton(d, "Borrar").click()
    for j in po["orden"]:
        clic(d, f".esp-jug[data-j='{j}']")
    boton(d, "Entregar").click()
    m = feedback(d)
    cerrar(d)
    return m


SOLVERS.update({"36": s36})
REQUIERE.update({"36": ["37", "39", "41", "42"]})
