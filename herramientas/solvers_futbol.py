import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bot_core import *

# Las soluciones salen de lo que calcula instancias_futbol.py (y dibuja futbol.py), no de copias escritas a mano.
INST = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "instancias_futbol.json"), encoding="utf-8"))


def clic(d, css):
    """Clic por JS: los elementos pueden estar dentro de contenedores con overflow oculto."""
    d.execute_script("arguments[0].click()", d.find_element(By.CSS_SELECTOR, css))
    time.sleep(0.05)


def s20(d):
    """Convocatoria: sin elegir, un dorsal equivocado y luego el del jugador que describe el míster."""
    abrir_carta(d, "20")
    boton(d, "Convocar").click()
    assert "Elegid primero" in feedback(d), feedback(d)
    carta = INST["convocatoria"]
    bueno = INST["cromos"][carta]["dorsal"]
    malo = next(c["dorsal"] for c in INST["cromos"].values() if c["dorsal"] != bueno)
    clic(d, f".fut-dorsal[data-d='{malo}']")
    boton(d, "Convocar").click()
    assert "niega" in feedback(d), feedback(d)
    clic(d, f".fut-dorsal[data-d='{bueno}']")
    boton(d, "Convocar").click()
    m = feedback(d)
    cerrar(d)
    return m


def _colocar(d, sol):
    for slot, dorsal in sol.items():
        clic(d, f".fut-ficha[data-d='{dorsal}']")
        clic(d, f".fut-puesto[data-s='{slot}']")


def s24(d):
    """Pizarra: sin colocar, con dos defensas intercambiados (4 de 6) y luego la alineación deducida."""
    abrir_carta(d, "24")
    boton(d, "Comprobar").click()
    assert "Faltan jugadores" in feedback(d), feedback(d)
    sol = dict(INST["alineacion"]["solucion"])
    mala = dict(sol)
    mala["DI"], mala["DD"] = sol["DD"], sol["DI"]
    _colocar(d, mala)
    boton(d, "Comprobar").click()
    assert "de 6" in feedback(d), feedback(d)
    boton(d, "Vaciar").click()
    _colocar(d, sol)
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s46(d):
    """VAR: sin decidir, todo válido (falla) y luego la decisión que sale del reglamento."""
    abrir_carta(d, "46")
    boton(d, "Confirmar").click()
    assert "Faltan jugadas" in feedback(d), feedback(d)
    for j in range(4):
        clic(d, f".fut-jugada[data-j='{j}']")
    boton(d, "Confirmar").click()
    assert "no es correcta" in feedback(d), feedback(d)
    boton(d, "Vaciar").click()
    for j, jug in enumerate(INST["var"]):
        for _ in range(2 if jug["fuera"] else 1):
            clic(d, f".fut-jugada[data-j='{j}']")
    boton(d, "Confirmar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s48(d):
    """Liguilla: a cero (falla) y luego los tres marcadores que faltan."""
    abrir_carta(d, "48")
    boton(d, "Comprobar").click()
    assert "no coincide" in feedback(d), feedback(d)
    L = INST["liguilla"]
    for k, i in enumerate(L["desconocidos"]):
        for l in (0, 1):
            for _ in range(L["resultados"][i][l]):
                clic(d, f".fut-marcador button[data-m='{k}'][data-l='{l}'][data-d='1']")
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s69(d):
    """Penaltis: un primer tiro a la izquierda (el portero se lanza ahí: parada) y luego la tanda que sigue el informe."""
    abrir_carta(d, "69")
    clic(d, ".fut-tiro button[data-l='izquierda']")
    assert "Paradón" in feedback(d), feedback(d)
    for l in INST["penaltis"]["ejemplo"]:
        clic(d, f".fut-tiro button[data-l='{l}']")
    m = feedback(d)
    cerrar(d)
    return m


SOLVERS = {"20": s20, "24": s24, "46": s46, "48": s48, "69": s69}
# cartas que hay que tener en mesa para poder resolver cada minijuego
REQUIERE = {"20": ["14", "15", "16", "17", "18", "19"], "24": ["30", "31"], "46": ["40", "41", "42"], "48": ["52", "53"], "69": ["70"]}
