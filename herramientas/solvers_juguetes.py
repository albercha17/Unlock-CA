import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bot_core import *

# Las soluciones salen de lo que calcula instancias_juguetes.py (y dibuja juguetes.py), no de copias escritas a mano.
INST = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "instancias_juguetes.json"), encoding="utf-8"))


def clic(d, css):
    """Clic por JS: los elementos pueden estar dentro de contenedores con overflow oculto."""
    d.execute_script("arguments[0].click()", d.find_element(By.CSS_SELECTOR, css))
    time.sleep(0.03)


def s24(d):
    """Estantería: un toque en una zona sin cambios (avisa) y luego las cinco diferencias."""
    abrir_carta(d, "24")
    d.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}))", d.find_element(By.CSS_SELECTOR, ".jug-estante"))
    assert "igual que en la foto" in feedback(d), feedback(d)
    for i in range(len(INST["estanteria"]["cambios"])):
        clic(d, f".jug-zona[data-i='{i}']")
    m = feedback(d)
    cerrar(d)
    return m


def s46(d):
    """Torre: sin bloques (avisa del total), con las filas de delante y detrás cambiadas (falla una vista) y luego la torre."""
    abrir_carta(d, "46")
    boton(d, "Comprobar").click()
    assert "bloques" in feedback(d), feedback(d)
    h = INST["torre"]["alturas"]
    mala = [h[2], h[1], h[0]] if h[0] != h[2] else [h[1], h[0], h[2]]

    def construir(m):
        for f in range(3):
            for c in range(3):
                for _ in range(m[f][c]):
                    clic(d, f".jug-casilla[data-f='{f}'][data-c='{c}']")
    construir(mala)
    boton(d, "Comprobar").click()
    assert "instrucciones" in feedback(d), feedback(d)
    boton(d, "Vaciar").click()
    construir(h)
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s48(d):
    """Marioneta: tirar de todos (falla) y luego solo de los mandos que mueven los miembros del cartel."""
    abrir_carta(d, "48")
    ma = INST["marioneta"]
    for m in ma["mandos"]:
        clic(d, f".jug-mando[data-m='{m}']")
    boton(d, "¡Saluda!").click()
    assert "no está como" in feedback(d), feedback(d)
    boton(d, "Soltar todo").click()
    for m in ma["solucion"]:
        clic(d, f".jug-mando[data-m='{m}']")
    boton(d, "¡Saluda!").click()
    m = feedback(d)
    cerrar(d)
    return m


def s66(d):
    """Tren: en el orden del andén (falla) y luego en el orden del folioscopio."""
    abrir_carta(d, "66")
    fo = INST["folioscopio"]

    def cargar(orden):
        for v, j in enumerate(orden):
            clic(d, f".jug-juguete[data-j='{j}']")
            clic(d, f".jug-vagon[data-v='{v}']")
    mal = fo["juguetes"] if fo["juguetes"] != fo["orden"] else fo["juguetes"][::-1]
    cargar(mal)
    boton(d, "¡Viajeros al tren!").click()
    assert "no arranca" in feedback(d), feedback(d)
    boton(d, "Vaciar").click()
    cargar(fo["orden"])
    boton(d, "¡Viajeros al tren!").click()
    m = feedback(d)
    cerrar(d)
    return m


def s69(d):
    """Pista: con los balancines como están (falla) y luego en la posición que manda el cristal al tarro."""
    abrir_carta(d, "69")
    p = INST["pista"]
    boton(d, "Soltar las canicas").click()
    time.sleep(4)
    if "Coged la carta" not in feedback(d):
        assert "no en el tarro" in feedback(d), feedback(d)
        for b, lado in p["solucion"].items():
            if d.find_element(By.CSS_SELECTOR, f".jug-bal[data-b='{b}']").get_attribute("data-lado") != lado:
                clic(d, f".jug-bal[data-b='{b}']")
        boton(d, "Soltar las canicas").click()
        time.sleep(4)
    m = feedback(d)
    cerrar(d)
    return m


SOLVERS = {"24": s24, "46": s46, "48": s48, "66": s66, "69": s69}
# cartas que hay que tener en mesa para poder resolver cada minijuego
REQUIERE = {"24": ["20"], "46": ["30", "31"], "48": ["52", "53"], "66": ["41", "43", "45", "49", "51"], "69": ["70"]}


# ---- ampliación a 36 cartas: los cubos de Leo
_AMP = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "instancias_ampliacion.json"), encoding="utf-8"))


def s64(d):
    """Cubos: se gira cada cubo hasta su cara del dibujo de la tapa."""
    abrir_carta(d, "64")
    cu = _AMP["juguetes_cubos"]
    for i in range(4):
        veces = (cu["solucion"][i] - cu["inicial"][i]) % len(cu["caras"][i])
        for _ in range(veces):
            clic(d, f".jug-cubo[data-i='{i}']")
            time.sleep(0.25)
    time.sleep(0.6)
    m = feedback(d)
    cerrar(d)
    return m


SOLVERS.update({"64": s64})
REQUIERE.update({"64": ["67"]})
