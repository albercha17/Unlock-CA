"""Solucionadores de los minijuegos de «El Cuarto de Leo, 1995» (62 cartas): juegan cada app por la interfaz real, primero una jugada mala para comprobar
el aviso (cuando la app avisa) y luego la buena. Las soluciones salen de instancias_juguetes.py."""
import sys, time
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from bot_core import *
import instancias_juguetes as I

D = I.INST


def clic(d, css):
    """Clic por JS: los elementos pueden estar dentro de contenedores con overflow oculto."""
    d.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}))", d.find_element(By.CSS_SELECTOR, css))
    time.sleep(0.03)


def escribe(d, css, texto):
    d.execute_script("var e = document.querySelector(arguments[0]); e.value = arguments[1]; e.dispatchEvent(new Event('input'));", css, str(texto))


def s14(d):
    """Cubos: se gira cada cubo hasta su cara del dibujo de la tapa."""
    abrir_carta(d, "14")
    cu = D["cubos"]
    for i in range(4):
        for _ in range((cu["solucion"][i] - cu["inicial"][i]) % len(cu["caras"][i])):
            clic(d, f".jug-cubo[data-i='{i}']")
            time.sleep(0.25)
    time.sleep(0.6)
    m = feedback(d)
    cerrar(d)
    return m


def s20(d):
    """Diferencias: un toque en una zona sin cambios (avisa) y luego las siete diferencias."""
    abrir_carta(d, "20")
    d.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}))", d.find_element(By.CSS_SELECTOR, ".jug-estante"))
    assert "igual que en la foto" in feedback(d), feedback(d)
    for i in range(len(D["estanteria"]["cambios"])):
        clic(d, f".jug-zona[data-i='{i}']")
    m = feedback(d)
    cerrar(d)
    return m


def s40(d):
    """Tren: en el orden del andén (falla) y luego en el orden del folioscopio."""
    abrir_carta(d, "40")
    fo = D["folioscopio"]

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


def s48(d):
    """Marioneta: tirar de todos (falla) y luego solo de los mandos que mueven los miembros del cartel."""
    abrir_carta(d, "48")
    ma = D["marioneta"]
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


def s52(d):
    """Oca: una casilla equivocada (falla) y la casilla final."""
    abrir_carta(d, "52")
    O = D["oca"]
    boton(d, "Mover la ficha").click()
    assert "Todavía" in feedback(d), feedback(d)
    escribe(d, ".ju-in", O["final"] % 60 + 1)
    boton(d, "Mover la ficha").click()
    assert "no acaba ahí" in feedback(d), feedback(d)
    escribe(d, ".ju-in", O["final"])
    boton(d, "Mover la ficha").click()
    m = feedback(d)
    cerrar(d)
    return m


def s46(d):
    """Clavijas: un salto en diagonal (avisa) y luego la solución guardada, salto a salto."""
    abrir_carta(d, "46")
    C = D["clavijas"]
    (r, c), _ = C["solucion"][0]
    clic(d, f".cla-t button[data-r='{r}'][data-c='{c}']")
    clic(d, f".cla-t button[data-r='{r}'][data-c='{c}']")
    for (a, b), (e, f) in C["solucion"]:
        clic(d, f".cla-t button[data-r='{a}'][data-c='{b}']")
        clic(d, f".cla-t button[data-r='{e}'][data-c='{f}']")
    m = feedback(d)
    cerrar(d)
    return m


def s51(d):
    """Collar: último color mal (falla), color bien y azules mal (falla) y los dos bien."""
    abrir_carta(d, "51")
    Co = D["collar"]
    boton(d, "Enhebrar el collar").click()
    assert "Elegid primero" in feedback(d), feedback(d)
    mal = "rojo" if Co["ultimo"] != "rojo" else "azul"
    clic(d, f".col-c button[data-c='{mal}']")
    boton(d, "Enhebrar el collar").click()
    assert "no es la última" in feedback(d), feedback(d)
    clic(d, f".col-c button[data-c='{Co['ultimo']}']")
    escribe(d, ".ju-in", Co["azules"] + 1)
    boton(d, "Enhebrar el collar").click()
    assert "azules no sale" in feedback(d), feedback(d)
    escribe(d, ".ju-in", Co["azules"])
    boton(d, "Enhebrar el collar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s64(d):
    """Torre: sin bloques (avisa del total), con las filas de delante y detrás cambiadas (falla una vista) y luego la torre."""
    abrir_carta(d, "64")
    boton(d, "Comprobar").click()
    assert "bloques" in feedback(d), feedback(d)
    h = D["torre"]["alturas"]
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


def s69(d):
    """Pista: con los balancines como están (falla, si no son los buenos) y luego en la posición que manda la canica al tarro."""
    abrir_carta(d, "69")
    p = D["pista"]
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


def s72(d):
    """Memoria: sin parejas (falla), una pareja mal puesta (falla) y las ocho buenas."""
    abrir_carta(d, "72")
    sol = D["memoria"]["solucion"]
    boton(d, "Comprobar las parejas").click()
    assert "Faltan parejas" in feedback(d), feedback(d)

    def juntar(ps):
        for a, b in ps:
            clic(d, f".mem-t button[data-i='{a}']")
            clic(d, f".mem-t button[data-i='{b}']")
    malas = [[sol[0][0], sol[1][0]], [sol[0][1], sol[1][1]]] + [list(p) for p in sol[2:]]
    juntar(malas)
    boton(d, "Comprobar las parejas").click()
    assert "no es la buena" in feedback(d), feedback(d)
    boton(d, "Deshacer parejas").click()
    juntar(sol)
    boton(d, "Comprobar las parejas").click()
    m = feedback(d)
    cerrar(d)
    return m


def s85(d):
    """Nana: pocas notas (falla), melodía al revés (falla) y la melodía buena."""
    abrir_carta(d, "85")
    N = D["nana"]
    boton(d, "Tocar la nana").click()
    assert "cinco notas" in feedback(d), feedback(d)

    def tocar(melodia):
        for n in melodia:
            clic(d, f".xil-b button[data-c='{N['colores'][n]}']")
    tocar(N["melodia"][::-1])
    boton(d, "Tocar la nana").click()
    assert "rara" in feedback(d), feedback(d)
    boton(d, "Empezar de nuevo").click()
    tocar(N["melodia"])
    boton(d, "Tocar la nana").click()
    m = feedback(d)
    cerrar(d)
    return m


SOLVERS = {"14": s14, "20": s20, "40": s40, "48": s48, "52": s52, "46": s46, "51": s51, "64": s64, "69": s69, "72": s72, "85": s85}
# cartas que hay que tener en mesa para poder resolver cada minijuego
REQUIERE = {"14": ["16"], "20": ["18", "19", "21"], "40": ["41", "43", "45", "27", "23"], "48": ["42", "49", "53"], "52": ["54", "55", "59"], "46": ["37", "39", "33"],
            "51": ["26", "61", "63"], "64": ["66", "67"], "69": ["70", "71"], "72": ["75", "79"], "85": ["86", "87"]}
