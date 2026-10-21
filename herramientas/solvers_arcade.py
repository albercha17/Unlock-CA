"""Solucionadores de los minijuegos de «Game Over, 1985» (60 cartas): juegan cada app por la interfaz real, primero una jugada mala para comprobar el
aviso y luego la buena. Las soluciones salen de instancias_arcade.py."""
import sys, time
from collections import deque
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from bot_core import *
import instancias_arcade as I


def clic(d, css):
    """Clic por JS: los elementos pueden estar dentro de contenedores con overflow oculto."""
    d.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}))", d.find_element(By.CSS_SELECTOR, css))
    time.sleep(0.03)


def ciclar(d, css, valor, veces=6):
    """Pulsa un botón de ciclo hasta que su atributo data-v valga `valor`."""
    for _ in range(veces):
        if d.find_element(By.CSS_SELECTOR, css).get_attribute("data-v") == valor:
            return
        clic(d, css)
    raise Fallo(f"no consigo poner «{valor}» en {css}")


def cel(d, x, y):
    clic(d, f".ar-cel[data-x='{x}'][data-y='{y}']")


def s14(d):
    """Circuito: todos arriba (falla) y la combinación buena."""
    abrir_carta(d, "14")
    boton(d, "Probar la placa").click()
    assert "Byte" not in feedback(d) and feedback(d), feedback(d)
    for i, v in enumerate(I.CIRCUITO["solucion"]):
        if v == 0:
            clic(d, f".cir-sw[data-i='{i}']")
    boton(d, "Probar la placa").click()
    m = feedback(d)
    cerrar(d)
    return m


RUTA = I.ATASCO["ruta"]


def s20(d):
    """Aparcamiento: mover la nave 1 bloqueada (falla) y la ruta mínima."""
    abrir_carta(d, "20")
    clic(d, ".ata-pieza[data-i='0']")
    clic(d, ".ata-mas")
    assert "no puede moverse" in feedback(d), feedback(d)
    for i, dd in RUTA:
        clic(d, f".ata-pieza[data-i='{i}']")
        clic(d, ".ata-mas" if dd > 0 else ".ata-menos")
    m = feedback(d)
    cerrar(d)
    return m


def s40(d):
    """Sprite: pantalla vacía (falla), una casilla de más (falla) y el dibujo."""
    abrir_carta(d, "40")
    boton(d, "Comprobar").click()
    assert "negro" in feedback(d), feedback(d)
    cel(d, 0, 0)
    boton(d, "Comprobar").click()
    assert "no cuadra" in feedback(d), feedback(d)
    cel(d, 0, 0)
    for y, f in enumerate(I.SPRITE_D["pixeles"]):
        for x, v in enumerate(f):
            if v:
                cel(d, x, y)
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def teclea(d, texto):
    for ch in texto:
        clic(d, f".asc-teclado button[data-k='{ch}']")


def s48(d):
    """Mensaje: ocho letras equivocadas (falla) y CONTINUE."""
    abrir_carta(d, "48")
    teclea(d, "ABCDEFGH")
    boton(d, "Enviar").click()
    assert "basura" in feedback(d), feedback(d)
    for _ in range(8):
        boton(d, "Borrar una").click()
    teclea(d, I.ASCII["claro"])
    boton(d, "Enviar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s52(d):
    """Fantasmas: sin decidir (falla), dos velocidades cambiadas (falla) y la solución."""
    abrir_carta(d, "52")
    boton(d, "Comprobar").click()
    assert "Falta decidir" in feedback(d), feedback(d)
    sol = {s["pasillo"]: dict(s) for s in I.FANTASMAS["solucion"]}
    mala = {p: dict(s) for p, s in sol.items()}
    mala[1]["velocidad"], mala[2]["velocidad"] = sol[2]["velocidad"], sol[1]["velocidad"]

    def poner(plan):
        for p, s in plan.items():
            ciclar(d, f".fan-sel[data-p='{p}'][data-k='f']", s["fantasma"])
            ciclar(d, f".fan-sel[data-p='{p}'][data-k='v']", s["velocidad"])
            ciclar(d, f".fan-sel[data-p='{p}'][data-k='r']", s["fruta"])
    poner(mala)
    boton(d, "Comprobar").click()
    assert "no encaja" in feedback(d), feedback(d)
    poner(sol)
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s46(d):
    """Marcador: sin rellenar (falla), dos números cambiados (falla) y el cuadrado."""
    abrir_carta(d, "46")
    boton(d, "Comprobar").click()
    assert "Faltan" in feedback(d), feedback(d)
    sol = I.MAGICO["solucion"]
    fijas = {(x, y) for x, y, _ in I.MAGICO["dados"]}
    libres = [(x, y) for y in range(4) for x in range(4) if (x, y) not in fijas]
    c1, c2 = libres[0], libres[1]
    v1, v2 = sol[c1[1]][c1[0]], sol[c2[1]][c2[0]]

    def poner(x, y, n):
        cel(d, x, y)
        clic(d, f".cua-num[data-n='{n}']")
    for (x, y) in libres:
        poner(x, y, v2 if (x, y) == c1 else v1 if (x, y) == c2 else sol[y][x])
    assert "no cuadra" in feedback(d), feedback(d)
    poner(c1[0], c1[1], v1)
    poner(c2[0], c2[1], v2)
    m = feedback(d)
    cerrar(d)
    return m


def s51(d):
    """Récords: catorce cambios inútiles (la máquina se cansa) y la ordenación por burbuja."""
    abrir_carta(d, "51")
    for _ in range(I.RANKING["limite"]):
        clic(d, ".ran-fila[data-pos='1'] .ran-sube")
    assert "paciencia" in feedback(d), feedback(d)
    pts = I.RANKING["puntos"]
    estado = list(range(len(pts)))
    cambiado = True
    while cambiado:
        cambiado = False
        for pos in range(1, len(estado)):
            if pts[estado[pos - 1]] > pts[estado[pos]]:
                clic(d, f".ran-fila[data-pos='{pos}'] .ran-sube")
                estado[pos - 1], estado[pos] = estado[pos], estado[pos - 1]
                cambiado = True
    m = feedback(d)
    cerrar(d)
    return m


def _deslizar():
    ini = tuple(tuple(f) for f in I.DESLIZANTE["inicio"])
    fin = tuple(tuple(f) for f in I.DESLIZANTE["objetivo"])
    prev = {ini: None}
    cola = deque([ini])
    while cola:
        e = cola.popleft()
        if e == fin:
            break
        y0, x0 = next((y, x) for y in range(3) for x in range(3) if e[y][x] == 0)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            x, y = x0 + dx, y0 + dy
            if 0 <= x < 3 and 0 <= y < 3:
                g = [list(f) for f in e]
                ficha = g[y][x]
                g[y0][x0], g[y][x] = ficha, 0
                n = tuple(tuple(f) for f in g)
                if n not in prev:
                    prev[n] = (e, ficha)
                    cola.append(n)
    ruta, e = [], fin
    while prev[e]:
        e, f = prev[e]
        ruta.append(f)
    return ruta[::-1]


def s64(d):
    """Deslizante: una ficha lejos del hueco (falla) y la ruta más corta."""
    abrir_carta(d, "64")
    primera = _deslizar()[0]
    lejos = next(v for f in I.DESLIZANTE["inicio"] for v in f if v and v != primera and not _vecina(v))
    clic(d, f".des-ficha[data-v='{lejos}']")
    assert "junto al hueco" in feedback(d), feedback(d)
    for ficha in _deslizar():
        clic(d, f".des-ficha[data-v='{ficha}']")
    m = feedback(d)
    cerrar(d)
    return m


def _vecina(v):
    g = I.DESLIZANTE["inicio"]
    y0, x0 = next((y, x) for y in range(3) for x in range(3) if g[y][x] == 0)
    return any(0 <= x0 + dx < 3 and 0 <= y0 + dy < 3 and g[y0 + dy][x0 + dx] == v for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))


def s69(d):
    """Rana: esperar sin más (falla) y la ruta correcta."""
    abrir_carta(d, "69")
    boton(d, "Ejecutar").click()
    assert "vacío" in feedback(d), feedback(d)
    for _ in range(3):
        clic(d, ".rana-b[data-m='W']")
    boton(d, "Ejecutar").click()
    assert "Byte" not in feedback(d) and feedback(d), feedback(d)
    boton(d, "Borrar todo").click()
    for m in I.RANA["solucion"]:
        clic(d, f".rana-b[data-m='{m}']")
    boton(d, "Ejecutar").click()
    m = feedback(d)
    cerrar(d)
    return m


def monedas(d, plan):
    for v, n in plan.items():
        for _ in range(n):
            clic(d, f".ar-fila[data-c='{v}'] button[data-d='1']")


def s72(d):
    """Monedas: nos pasamos (falla), justo pero con demasiadas (falla) y el pago mínimo."""
    abrir_carta(d, "72")
    boton(d, "Pagar").click()
    assert "ninguna" in feedback(d), feedback(d)
    monedas(d, {"20": 1, "15": 1})
    boton(d, "Pagar").click()
    assert "pasáis" in feedback(d), feedback(d)
    boton(d, "Vaciar").click()
    monedas(d, {"15": 2, "1": 4})
    boton(d, "Pagar").click()
    assert "menos monedas" in feedback(d), feedback(d)
    boton(d, "Vaciar").click()
    monedas(d, {str(v): n for v, n in zip(I.MONEDAS["monedas"], I.MONEDAS["solucion"]) if n})
    boton(d, "Pagar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s85(d):
    """Arranque: un byte equivocado (falla), clave equivocada (falla) y la buena."""
    abrir_carta(d, "85")
    bytes_ = [I.BYTES[k] for k in I.ORDEN]
    for i, v in enumerate(bytes_[:3]):
        monedas(d, {f"b{i}": v})
    boton(d, "Arrancar").click()
    assert "no es el que dejó" in feedback(d), feedback(d)
    monedas(d, {"b3": bytes_[3]})
    boton(d, "Arrancar").click()
    assert "clave no sale" in feedback(d), feedback(d)
    monedas(d, {"clave": I.RESULTADO})
    boton(d, "Arrancar").click()
    m = feedback(d)
    cerrar(d)
    return m


SOLVERS = {"14": s14, "20": s20, "40": s40, "48": s48, "52": s52, "46": s46, "51": s51, "64": s64, "69": s69, "72": s72, "85": s85}
REQUIERE = {"14": ["16"], "20": ["18", "19", "21"], "40": ["41", "43", "45"], "48": ["42", "49", "53"], "52": ["54", "55", "59"], "46": ["37", "39", "33"],
            "51": ["26", "61", "63"], "64": ["66", "67"], "69": ["70", "71"], "72": ["75", "79"], "85": ["86", "87"]}
