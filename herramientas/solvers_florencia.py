"""Solucionadores de los minijuegos de «Florencia» (60 cartas): juegan cada app por la interfaz real, primero una jugada mala para comprobar el aviso
y luego la buena. Las soluciones salen de instancias_florencia.py."""
import sys, time
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from bot_core import *
import instancias_florencia as I


def clic(d, css):
    """Clic por JS: los elementos pueden estar dentro de contenedores con overflow oculto."""
    d.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}))", d.find_element(By.CSS_SELECTOR, css))
    time.sleep(0.03)


def cel(d, x, y):
    clic(d, f".fl-cel[data-x='{x}'][data-y='{y}']")


def escribe(d, css, texto):
    d.execute_script("var e = document.querySelector(arguments[0]); e.value = arguments[1]; e.dispatchEvent(new Event('input'));", css, texto)


def sube(d, clave, n):
    for _ in range(n):
        clic(d, f".fl-fila[data-c='{clave}'] button[data-d='1']")


def s14(d):
    """Escítala: una palabra equivocada (falla) y ALAS."""
    abrir_carta(d, "14")
    escribe(d, ".esc-in", "LEON")
    boton(d, "Probar").click()
    assert "no cede" in feedback(d), feedback(d)
    escribe(d, ".esc-in", I.ESCITALA["solucion"].lower())
    boton(d, "Probar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s20(d):
    """Punto de fuga: sin marcar (falla), una casilla lejana (falla) y la casilla buena."""
    abrir_carta(d, "20")
    boton(d, "Fijar el punto de fuga").click()
    assert "Marcad antes" in feedback(d), feedback(d)
    x, y = I.PERSPECTIVA["solucion"]
    clic(d, f".per-c[data-c='{(x + 3) % I.PERSPECTIVA['cols']}'][data-f='{I.PERSPECTIVA['filas'] - 1}']")
    boton(d, "Fijar el punto de fuga").click()
    assert "no se juntan" in feedback(d), feedback(d)
    clic(d, f".per-c[data-c='{x}'][data-f='{y}']")
    boton(d, "Fijar el punto de fuga").click()
    m = feedback(d)
    cerrar(d)
    return m


def s40(d):
    """Futoshiki: vacío (falla), todo unos (falla) y el cuadrado bueno."""
    abrir_carta(d, "40")
    boton(d, "Comprobar").click()
    assert "vacías" in feedback(d), feedback(d)
    n = I.FUTOSHIKI["n"]

    def pon(g):
        for y in range(n):
            for x in range(n):
                b = d.find_element(By.CSS_SELECTOR, f".fl-cel[data-x='{x}'][data-y='{y}']")
                for _ in range(7):
                    if b.text == str(g[y][x]):
                        break
                    d.execute_script("arguments[0].click()", b)
    pon([[1] * n for _ in range(n)])
    boton(d, "Comprobar").click()
    assert "se repite" in feedback(d), feedback(d)
    pon(I.FUTOSHIKI["solucion"])
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s48(d):
    """Caballo: nada marcado (falla), un salto que no es de caballo (falla) y un recorrido completo."""
    abrir_carta(d, "48")
    boton(d, "Comprobar").click()
    assert "ningún salto" in feedback(d), feedback(d)
    ini = I.CABALLO["inicio"]
    cel(d, *ini)
    cel(d, ini[0] + 1, ini[1])                               # un paso lateral: no es salto de caballo
    boton(d, "Comprobar").click()
    assert "no es de caballo" in feedback(d), feedback(d)
    boton(d, "Empezar de nuevo").click()
    for x, y in I.CABALLO["ruta"]:
        cel(d, x, y)
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s52(d):
    """Pigmentos: ninguna cucharada (falla) y la mezcla buena."""
    abrir_carta(d, "52")
    boton(d, "Mezclar").click()
    assert "Ese no es el color" in feedback(d), feedback(d)
    for j, n in enumerate(I.PIGMENTOS["solucion"]):
        sube(d, f"p{j}", n)
    boton(d, "Mezclar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s46(d):
    """Engranajes: sin lado (falla), lado equivocado (falla), vueltas equivocadas (falla) y la buena."""
    abrir_carta(d, "46")
    s = I.ENGRANAJES["solucion"]
    sube(d, "vueltas", s["vueltas"])
    boton(d, "Comprobar").click()
    assert "Decid también" in feedback(d), feedback(d)
    otro = "izquierda" if s["sentido"] == "derecha" else "derecha"
    clic(d, f".eng-lados button[data-l='{otro}']")
    boton(d, "Comprobar").click()
    assert "otro lado" in feedback(d), feedback(d)
    sube(d, "vueltas", 1)
    clic(d, f".eng-lados button[data-l='{s['sentido']}']")
    boton(d, "Comprobar").click()
    assert "se atasca" in feedback(d), feedback(d)
    clic(d, ".fl-fila[data-c='vueltas'] button[data-d='-1']")
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s51(d):
    """Vigilantes: sin torres (falla), todas las plazas (falla por exceso) y un conjunto mínimo."""
    abrir_carta(d, "51")
    boton(d, "Avisar al Gonfaloniere").click()
    assert "Levantad alguna" in feedback(d), feedback(d)
    n = I.VIGILANTES["n"]
    for i in range(n):
        clic(d, f".vig-p[data-i='{i}']")
    boton(d, "Avisar al Gonfaloniere").click()
    assert "con menos torres" in feedback(d), feedback(d)
    for i in range(n):
        clic(d, f".vig-p[data-i='{i}']")
    for i in I.VIGILANTES["soluciones"][0]:
        clic(d, f".vig-p[data-i='{i}']")
    boton(d, "Avisar al Gonfaloniere").click()
    m = feedback(d)
    cerrar(d)
    return m


def s69(d):
    """Caja: huecos vacíos (falla), el orden al revés (falla) y el orden bueno."""
    abrir_carta(d, "69")
    boton(d, "Abrir la caja").click()
    assert "Faltan" in feedback(d), feedback(d)
    sol = I.MASTERMIND["solucion"]

    def pon(orden):
        for i, c in enumerate(orden):
            clic(d, f".mas-c[data-k='{c}']")
            clic(d, f".mas-h[data-i='{i}']")
    pon(sol[::-1])
    boton(d, "Abrir la caja").click()
    assert "contradice" in feedback(d), feedback(d)
    pon(sol)
    boton(d, "Abrir la caja").click()
    m = feedback(d)
    cerrar(d)
    return m


def s64(d):
    """Hidato: una numeración completa con los dos últimos cambiados (falla) y la buena."""
    abrir_carta(d, "64")
    cam = I.HIDATO["camino"]
    for x, y in cam[:-2]:
        cel(d, x, y)
    cel(d, *cam[-1])
    cel(d, *cam[-2])
    assert "algún número no coincide" in feedback(d), feedback(d)
    boton(d, "Quitar el último").click()
    boton(d, "Quitar el último").click()
    cel(d, *cam[-2])
    cel(d, *cam[-1])
    time.sleep(0.2)
    m = feedback(d)
    cerrar(d)
    return m


def s72(d):
    """Poleas: sin elegir (falla), un aparejo equivocado (falla) y el bueno."""
    abrir_carta(d, "72")
    boton(d, "Alzar la carga").click()
    assert "Elegid un aparejo" in feedback(d), feedback(d)
    mal = (I.POLEAS["solucion"] + 1) % 4
    clic(d, f".pol-b[data-i='{mal}']")
    boton(d, "Alzar la carga").click()
    assert "no puede" in feedback(d), feedback(d)
    clic(d, f".pol-b[data-i='{I.POLEAS['solucion']}']")
    boton(d, "Alzar la carga").click()
    m = feedback(d)
    cerrar(d)
    return m


def s85(d):
    """Cifrado: una palabra equivocada (falla) y la buena."""
    abrir_carta(d, "85")
    escribe(d, ".cif-in", "AMANECES")
    boton(d, "Descifrar").click()
    assert "sigue oscuro" in feedback(d), feedback(d)
    escribe(d, ".cif-in", I.CIFRADO["claro"])
    boton(d, "Descifrar").click()
    m = feedback(d)
    cerrar(d)
    return m


SOLVERS = {"14": s14, "20": s20, "40": s40, "48": s48, "52": s52, "46": s46, "51": s51, "69": s69, "64": s64, "72": s72, "85": s85}
REQUIERE = {"14": ["16"], "20": ["18", "19", "21"], "40": ["41", "43", "45"], "48": ["42", "49", "53"], "52": ["54", "55", "59"],
            "46": ["37", "39", "33"], "51": ["26", "61", "63"], "69": ["70", "71"], "64": ["66", "67"], "72": ["75", "79"], "85": ["86", "87"]}
