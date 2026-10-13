import sys, time
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from bot_core import *


def lector(d, num):
    abrir_carta(d, num)
    for _ in range(3):
        boton(d, "Siguiente →").click()
    texto = d.find_element(By.CSS_SELECTOR, ".far-hoja").text
    cerrar(d)
    return "(lector) " + texto[:40]


def s15(d):
    return lector(d, "15")


def s23(d):
    abrir_carta(d, "23")
    # primero una palabra mala
    for ch in "AAAAA":
        tecla(d, ch)
    boton(d, "Comprobar").click()
    mal = feedback(d)
    assert "Nada sucede" in mal, mal
    for _ in range(5):
        boton(d, "Borrar").click()
    for ch in "HORUS":
        tecla(d, ch)
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s47(d):
    abrir_carta(d, "47")
    tecla(d, "3")           # 3 -> el plato derecho pesa menos que el corazon
    assert feedback(d) == ""
    tecla(d, "3")           # la quita
    tecla(d, "11")
    tecla(d, "6")           # 11 + 6 = 17
    time.sleep(0.2)
    m = feedback(d)
    cerrar(d)
    return m


def s71(d):
    abrir_carta(d, "71")
    def clic(aria, veces):
        for _ in range(veces):
            d.find_element(By.XPATH, f"//button[@aria-label='{aria}']").click()
            time.sleep(0.05)
    boton(d, "Comprobar").click()
    assert "no encajan" in feedback(d)
    clic("Anillo 1 arriba", 3)   # serpiente(3) -> sol(0)
    clic("Anillo 3 arriba", 2)   # agua(4) -> escarabajo(2)
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s95(d):
    abrir_carta(d, "95")
    def cristal(c):
        d.find_element(By.CSS_SELECTOR, f".far-cristal[data-color='{c}']").click()
        time.sleep(0.05)
    cristal("azul"); cristal("rojo")        # error: se reinicia
    assert "Empezad de nuevo" in feedback(d)
    for c in ["azul", "amarillo", "rojo", "verde", "amarillo"]:
        cristal(c)
    m = feedback(d)
    cerrar(d)
    return m


def s37(d):
    """Tablilla deslizante: lee el estado del tablero y lo resuelve con una busqueda (BFS)."""
    from collections import deque
    abrir_carta(d, "37")
    codigos = {0x2600: 1, 0x1F441: 2, 0x1F41E: 3, 0x1F40D: 4, 0x1F30A: 5, 0x1F985: 6, 0x1F3FA: 7, 0x1F402: 8}
    piezas = d.find_elements(By.CSS_SELECTOR, ".far-pieza")
    estado = tuple(codigos[ord(p.text.strip()[0])] if p.text.strip() else 0 for p in piezas)
    meta = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    previo = {estado: None}
    cola = deque([estado])
    while cola:
        s = cola.popleft()
        if s == meta:
            break
        i = s.index(0)
        r, c = divmod(i, 3)
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                j = nr * 3 + nc
                l = list(s)
                l[i], l[j] = l[j], l[i]
                t = tuple(l)
                if t not in previo:
                    previo[t] = (s, j)
                    cola.append(t)
    clics = []
    s = meta
    while previo[s] is not None:
        s, j = previo[s]
        clics.append(j)
    clics.reverse()
    assert len(clics) == 16, f"se esperaban 16 movimientos y hay {len(clics)}"
    for j in clics:
        d.find_element(By.CSS_SELECTOR, f".far-pieza[data-pos='{j}']").click()
        time.sleep(0.03)
    time.sleep(0.2)
    m = feedback(d)
    cerrar(d)
    return m


def s34(d):
    abrir_carta(d, "34")
    for ch in "1111":
        tecla(d, ch)
    tecla(d, "✓")
    assert "no cede" in feedback(d), feedback(d)
    for ch in "2343":
        tecla(d, ch)
    tecla(d, "✓")
    m = feedback(d)
    cerrar(d)
    return m


SOLVERS = {"15": s15, "23": s23, "47": s47, "71": s71, "95": s95, "37": s37, "34": s34}
REQUIERE = {"23": ["31"], "47": ["52"], "71": ["26"], "37": ["28"], "34": ["46"], "95": ["15", "44"]}
