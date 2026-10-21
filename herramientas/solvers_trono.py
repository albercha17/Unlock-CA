"""Solucionadores de los minijuegos de «Trono» (60 cartas): juegan cada app por la interfaz real, primero una jugada mala para comprobar el aviso
y luego la buena. Las soluciones salen de instancias_trono.py."""
import itertools, sys, time
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from bot_core import *
import instancias_trono as I


def clic(d, css):
    """Clic por JS: los elementos pueden estar dentro de contenedores con overflow oculto (y valen para SVG)."""
    d.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}))", d.find_element(By.CSS_SELECTOR, css))
    time.sleep(0.03)


def clic_attr(d, css, attr, val):
    d.execute_script("var b = [...document.querySelectorAll(arguments[0])].find(x => x.getAttribute(arguments[1]) === arguments[2]); b.click();", css, attr, val)
    time.sleep(0.03)


def escribe(d, css, texto):
    d.execute_script("var e = document.querySelector(arguments[0]); e.value = arguments[1]; e.dispatchEvent(new Event('input'));", css, texto)


def cel(d, x, y):
    clic(d, f".tr-cel[data-x='{x}'][data-y='{y}']")


def s14(d):
    """Jarras: vaciar sin más (no hay aviso) y la secuencia buena."""
    abrir_carta(d, "14")
    nombres = {"llenar A": "Llenar I", "llenar B": "Llenar II", "vaciar A": "Vaciar I", "vaciar B": "Vaciar II", "A a B": "I → II", "B a A": "II → I"}
    clic_attr(d, ".jar-botones button", "data-a", "Llenar II")
    boton(d, "Empezar de nuevo").click()
    for m in I.JARRAS["ruta"]:
        clic_attr(d, ".jar-botones button", "data-a", nombres[m])
    time.sleep(0.2)
    m = feedback(d)
    cerrar(d)
    return m


def s20(d):
    """Centinelas: ninguno (falla), ocho en una fila (se ven) y la disposición buena."""
    abrir_carta(d, "20")
    boton(d, "Dar el relevo").click()
    assert "Hacen falta" in feedback(d), feedback(d)
    n = I.CENTINELAS["n"]
    for x in range(n):
        cel(d, x, 0)
    boton(d, "Dar el relevo").click()
    assert "se ven" in feedback(d), feedback(d)
    for x in range(n):
        cel(d, x, 0)
    for x, y in I.CENTINELAS["solucion"]:
        cel(d, x, y)
    boton(d, "Dar el relevo").click()
    m = feedback(d)
    cerrar(d)
    return m


def s40(d):
    """Cuervos: una ruta que no es la más corta (falla) y la ruta buena."""
    abrir_carta(d, "40")
    dist = I.CUERVOS["distancias"]
    dd = lambda a, b: dist[f"{min(a, b)},{max(a, b)}"]
    sol = I.CUERVOS["solucion"]
    otra = next(p for p in itertools.permutations(range(1, 6)) if sum(dd(a, b) for a, b in zip((0,) + p, p + (0,))) != I.CUERVOS["minimo"])
    boton(d, "Enviar el cuervo").click()
    assert "Faltan" in feedback(d), feedback(d)
    for i in otra:
        clic(d, f".cue-f[data-i='{i}']")
    boton(d, "Enviar el cuervo").click()
    assert "ruta más corta" in feedback(d), feedback(d)
    boton(d, "Empezar de nuevo").click()
    for i in sol[1:]:
        clic(d, f".cue-f[data-i='{i}']")
    boton(d, "Enviar el cuervo").click()
    m = feedback(d)
    cerrar(d)
    return m


def s48(d):
    """Playfair: una palabra equivocada (falla) y el mensaje."""
    abrir_carta(d, "48")
    escribe(d, ".pla-in", "TRAIDORES")
    boton(d, "Descifrar").click()
    assert "no tiene sentido" in feedback(d), feedback(d)
    escribe(d, ".pla-in", I.PLAYFAIR["claro"].lower())
    boton(d, "Descifrar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s52(d):
    """Piedras: una partida perdida (tomando siempre 1) y una ganada con la estrategia."""
    abrir_carta(d, "52")
    for _ in range(30):
        clic(d, ".pie-bot button[data-n='1']")
        if "habéis perdido" in feedback(d):
            break
    assert "habéis perdido" in feedback(d), feedback(d)
    time.sleep(0.9)
    quedan = lambda: int(d.find_element(By.CSS_SELECTOR, ".pie-mesa").get_attribute("data-quedan"))
    assert quedan() == I.PIEDRAS["piedras"], quedan()
    clic(d, ".pie-bot button[data-n='1']")                   # 21 - 1 = 20: múltiplo de cuatro
    for _ in range(20):
        if "Cifra de la profecía" in feedback(d):
            break
        q = quedan()
        clic(d, f".pie-bot button[data-n='{q % 4 or 1}']")
    m = feedback(d)
    cerrar(d)
    return m


def s46(d):
    """Hashi: sin puentes (falla), un puente imposible (falla) y los puentes buenos."""
    abrir_carta(d, "46")
    letras = {}
    for k in I.CAMINOS["islas"]:
        x, y = map(int, k.split(","))
        letras[(x, y)] = None
    orden = sorted(letras, key=lambda t: (t[1], t[0]))
    L = {p: "ABCDEFGHIJKLMNOP"[i] for i, p in enumerate(orden)}
    boton(d, "Comprobar").click()
    assert "Algún castillo" in feedback(d), feedback(d)
    a, b = next((p, q) for p in orden for q in orden if p[0] != q[0] and p[1] != q[1])
    clic(d, f".cam-isla[data-l='{L[a]}']")
    clic(d, f".cam-isla[data-l='{L[b]}']")
    assert "no se puede tender" in feedback(d), feedback(d)
    for (p, q, c) in I.CAMINOS["puentes"]:
        for _ in range(c):
            clic(d, f".cam-isla[data-l='{L[tuple(p)]}']")
            clic(d, f".cam-isla[data-l='{L[tuple(q)]}']")
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s51(d):
    """Sucesión: sin elegir (falla), el septón (falla) y el heredero."""
    abrir_carta(d, "51")
    boton(d, "Coronar").click()
    assert "Elegid" in feedback(d), feedback(d)
    clic(d, ".suc-b[data-n='Maegor']")
    boton(d, "Coronar").click()
    assert "no dicen eso" in feedback(d), feedback(d)
    clic(d, f".suc-b[data-n='{I.SUCESION['solucion']}']")
    boton(d, "Coronar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s69(d):
    """Sudoku: casillas vacías (falla), todo unos (falla) y la solución."""
    abrir_carta(d, "69")
    boton(d, "Comprobar").click()
    assert "Quedan" in feedback(d), feedback(d)
    sol, dados = I.SUDOKU["solucion"], I.SUDOKU["dados"]

    def estado():
        return [list(map(int, f)) for f in d.find_element(By.CSS_SELECTOR, ".sud-t").get_attribute("data-estado").split("/")]

    def pon(g):
        for f in range(6):
            for c in range(6):
                if dados[f][c]:
                    continue
                actual = estado()[f][c]
                for _ in range((g[f][c] - actual) % 7):
                    clic(d, f".sud-c[data-f='{f}'][data-c='{c}']")
    pon([[1] * 6 for _ in range(6)])
    boton(d, "Comprobar").click()
    assert "Algún escudo" in feedback(d), feedback(d)
    pon(sol)
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s64(d):
    """Tapiz: vacío (falla) y el dibujo bueno."""
    abrir_carta(d, "64")
    boton(d, "Comprobar").click()
    assert "no cuadran" in feedback(d), feedback(d)
    for y, f in enumerate(I.TAPIZ["solucion"]):
        for x, v in enumerate(f):
            if v:
                cel(d, x, y)
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s72(d):
    """Torres: un disco grande sobre uno pequeño (falla) y los quince movimientos."""
    abrir_carta(d, "72")
    pos = {"I": 0, "II": 1, "III": 2}
    clic(d, ".tor-t[data-t='0']")
    clic(d, ".tor-t[data-t='1']")
    clic(d, ".tor-t[data-t='0']")
    clic(d, ".tor-t[data-t='1']")
    assert "nunca va sobre" in feedback(d), feedback(d)
    boton(d, "Empezar de nuevo").click()
    movs = []

    def hanoi(n, a, b, c):
        if n:
            hanoi(n - 1, a, c, b)
            movs.append((a, c))
            hanoi(n - 1, b, a, c)
    hanoi(I.TORRES["discos"], "I", "II", "III")
    for a, c in movs:
        clic(d, f".tor-t[data-t='{pos[a]}']")
        clic(d, f".tor-t[data-t='{pos[c]}']")
    time.sleep(0.2)
    m = feedback(d)
    cerrar(d)
    return m


def s85(d):
    """Profecía: cero (falla) y el resultado de la cuenta."""
    abrir_carta(d, "85")
    boton(d, "Abrir la puerta").click()
    assert "no se mueve" in feedback(d), feedback(d)
    for _ in range(I.RESULTADO):
        clic(d, ".tr-fila[data-c='numero'] button[data-d='1']")
    boton(d, "Abrir la puerta").click()
    m = feedback(d)
    cerrar(d)
    return m


SOLVERS = {"14": s14, "20": s20, "40": s40, "48": s48, "52": s52, "46": s46, "51": s51, "69": s69, "64": s64, "72": s72, "85": s85}
REQUIERE = {"14": ["16"], "20": ["18", "19", "21"], "40": ["41", "43", "45"], "48": ["42", "49", "53"], "52": ["54", "55", "59"],
            "46": ["37", "39", "33"], "51": ["26", "61", "63"], "69": ["70", "71"], "64": ["66", "67"], "72": ["75", "79"], "85": ["86", "87"]}
