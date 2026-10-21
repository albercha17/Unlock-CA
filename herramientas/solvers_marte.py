"""Solucionadores de los minijuegos de «Marte» (60 cartas): juegan cada app por la interfaz real, primero una jugada mala para comprobar el aviso
y luego la buena. Las soluciones salen de instancias_marte.py."""
import sys, time
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from bot_core import *
import instancias_marte as I


def clic(d, css):
    """Clic por JS: los elementos pueden estar dentro de contenedores con overflow oculto."""
    d.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}))", d.find_element(By.CSS_SELECTOR, css))
    time.sleep(0.03)


def cel(d, x, y):
    clic(d, f".mr-cel[data-x='{x}'][data-y='{y}']")


def s14(d):
    """Satélites: cero horas (falla) y la hora buena."""
    abrir_carta(d, "14")
    boton(d, "Programar la llamada").click()
    assert "no coinciden" in feedback(d), feedback(d)
    for _ in range(I.SATELITES["solucion"]):
        clic(d, ".mr-fila[data-c='horas'] button[data-d='1']")
    boton(d, "Programar la llamada").click()
    m = feedback(d)
    cerrar(d)
    return m


def s20(d):
    """Invernadero: nada marcado (falla) y el paso de la vida bueno."""
    abrir_carta(d, "20")
    boton(d, "Comprobar").click()
    assert "no sale como dicen" in feedback(d), feedback(d)
    for y, f in enumerate(I.VIDA["solucion"]):
        for x, v in enumerate(f):
            if v:
                cel(d, x, y)
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def _pinta_cables(d, grid):
    n = I.CABLEADO["n"]
    for y in range(n):
        for x in range(n):
            b = d.find_element(By.CSS_SELECTOR, f".mr-cel[data-x='{x}'][data-y='{y}']")
            for _ in range(7):
                t = b.text
                if t == str(grid[y][x] + 1):
                    break
                d.execute_script("arguments[0].click()", b)
            time.sleep(0.01)


def s40(d):
    """Cableado: casillas sin pintar (falla), todo del cable 2 (falla) y la placa buena."""
    abrir_carta(d, "40")
    boton(d, "Comprobar").click()
    assert "sin pintar" in feedback(d), feedback(d)
    n = I.CABLEADO["n"]
    _pinta_cables(d, [[1] * n for _ in range(n)])
    boton(d, "Comprobar").click()
    assert "Hay un cable" in feedback(d), feedback(d)
    _pinta_cables(d, I.CABLEADO["solucion"])
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s48(d):
    """Rocas: una roca de menos y una de más (falla) y las rocas buenas."""
    abrir_carta(d, "48")
    sol = {tuple(r) for r in I.ROCAS["solucion"]}
    n = I.ROCAS["n"]
    libre = next((x, y) for y in range(n) for x in range(n) if (x, y) not in sol)
    cel(d, *libre)
    boton(d, "Mandar al rover").click()
    assert "se atasca" in feedback(d), feedback(d)
    cel(d, *libre)
    for x, y in sol:
        cel(d, x, y)
    boton(d, "Mandar al rover").click()
    m = feedback(d)
    cerrar(d)
    return m


def s52(d):
    """Brazo: sin colgar (falla), piezas en el orden contrario (falla) y la colocación buena."""
    abrir_carta(d, "52")
    boton(d, "Soltar el brazo").click()
    assert "Faltan piezas" in feedback(d), feedback(d)
    sol = I.BALANCIN["solucion"]

    def pon(pos):
        for k, p in enumerate(pos):
            clic(d, f".bra-p[data-k='{k}']")
            clic(d, f".bra-m[data-p='{p}']")
    pon(sol[::-1])
    boton(d, "Soltar el brazo").click()
    assert "se inclina" in feedback(d), feedback(d)
    pon(sol)
    boton(d, "Soltar el brazo").click()
    m = feedback(d)
    cerrar(d)
    return m


def s46(d):
    """Cuenta: una resta que da cero o menos (falla) y una cuenta que llega al objetivo."""
    abrir_carta(d, "46")
    nums = I.CIFRAS["numeros"]
    menor, mayor = sorted(nums)[0], sorted(nums)[-1]

    def pieza(v, excluir=None):
        piezas = d.find_elements(By.CSS_SELECTOR, ".cue-p")
        for i, p in enumerate(piezas):
            if p.get_attribute("data-v") == str(v) and i != excluir:
                return i
        raise AssertionError(f"no hay una pieza {v}")

    def toca(i):
        clic(d, f".cue-p[data-i='{i}']")

    def op(o):
        d.execute_script("arguments[0].click()", d.find_element(By.XPATH, f"//div[contains(@class,'cue-ops')]/button[@data-o='{o}']"))
    i = pieza(menor)
    toca(i)
    op("−")
    toca(pieza(mayor, i))
    assert "mayores que cero" in feedback(d), feedback(d)
    for a, o, b, r in I.solucion_cifras(nums, I.CIFRAS["objetivo"]):
        i = pieza(a)
        toca(i)
        op(o)
        toca(pieza(b, i))
    time.sleep(0.1)
    m = feedback(d)
    cerrar(d)
    return m


def s51(d):
    """Anillo: sin trazar (falla), un solo lado (falla) y el bucle bueno."""
    abrir_carta(d, "51")
    boton(d, "Comprobar").click()
    assert "Todavía no hay" in feedback(d), feedback(d)
    sol = I.ANILLO["solucion"]
    t, x, y = sol[0]
    clic(d, f".ani-svg .hit[data-k='{t}{x},{y}']")
    boton(d, "Comprobar").click()
    assert "no cuadra" in feedback(d), feedback(d)
    clic(d, f".ani-svg .hit[data-k='{t}{x},{y}']")
    for t, x, y in sol:
        clic(d, f".ani-svg .hit[data-k='{t}{x},{y}']")
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s69(d):
    """Programa: un programa que choca (falla), uno que no llega (falla) y el bucle bueno."""
    abrir_carta(d, "69")
    clic(d, ".pro-bot button[data-c='a']")
    clic(d, ".pro-bot button[data-c='a']")
    boton(d, "Ejecutar").click()
    assert "chocado" in feedback(d), feedback(d)
    boton(d, "Vaciar").click()
    clic(d, ".pro-bot button[data-c='a']")
    boton(d, "Ejecutar").click()
    assert "sin llegar" in feedback(d), feedback(d)
    boton(d, "Vaciar").click()
    d.execute_script("var s = document.querySelector('.pro-bot select'); s.value = '3';")
    clic(d, ".pro-bot button[data-c='r']")
    for c in "aiada":
        clic(d, f".pro-bot button[data-c='{c}']")
    clic(d, ".pro-bot button[data-c='x']")
    boton(d, "Ejecutar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s64(d):
    """Paneles: un toque suelto y luego los toques buenos (el mensaje sale solo al coincidir)."""
    abrir_carta(d, "64")
    cel(d, 0, 0)
    assert "idéntico" not in feedback(d)
    boton(d, "Apagar todos").click()
    for x, y in I.PANELES["toques"]:
        cel(d, x, y)
    time.sleep(0.2)
    m = feedback(d)
    cerrar(d)
    return m


def s72(d):
    """Sopa: una clave equivocada (falla) y la buena."""
    abrir_carta(d, "72")

    def clave(v):
        d.execute_script("var e = document.querySelector('.sop-in'); e.value = arguments[0]; e.dispatchEvent(new Event('input'));", v)
        boton(d, "Probar la clave").click()
    clave("ABC")
    assert "incorrecta" in feedback(d), feedback(d)
    clave(I.SOPA["secreta"].lower())
    m = feedback(d)
    cerrar(d)
    return m


def s85(d):
    """Consola: ceros (falla) y la clave buena."""
    abrir_carta(d, "85")
    boton(d, "Lanzar").click()
    assert "parpadea en rojo" in feedback(d), feedback(d)
    for i, dig in enumerate(I.CODIGO):
        for _ in range(dig):
            clic(d, f".con-r[data-i='{i}'] button[data-d='1']")
    boton(d, "Lanzar").click()
    m = feedback(d)
    cerrar(d)
    return m


SOLVERS = {"14": s14, "20": s20, "40": s40, "48": s48, "52": s52, "46": s46, "51": s51, "69": s69, "64": s64, "72": s72, "85": s85}
REQUIERE = {"14": ["16"], "20": ["18", "19", "21"], "40": ["41", "43", "45"], "48": ["42", "49", "53"], "52": ["54", "55", "59"],
            "46": ["37", "39", "33"], "51": ["26", "61", "63"], "69": ["70", "71"], "64": ["66", "67"], "72": ["75", "79"], "85": ["86", "87"]}
