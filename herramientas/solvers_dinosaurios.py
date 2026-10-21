"""Solucionadores de los minijuegos de «Dinosaurios» (60 cartas): juegan cada app por la interfaz real, primero una jugada mala para
comprobar el aviso y luego la buena. Las soluciones salen de instancias_dinosaurios.py."""
import sys, time
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from bot_core import *
import instancias_dinosaurios as I


def clic(d, css):
    """Clic por JS: los elementos pueden estar dentro de contenedores con overflow oculto."""
    d.execute_script("arguments[0].click()", d.find_element(By.CSS_SELECTOR, css))
    time.sleep(0.04)


def s14(d):
    """Huellas: un orden incompleto (falla), uno al revés (falla) y el bueno."""
    abrir_carta(d, "14")
    boton(d, "Comprobar").click()
    assert "Faltan" in feedback(d), feedback(d)
    for e in reversed(I.HUELLAS["orden"]):
        clic(d, f".dn-chip[data-e='{e}']")
    boton(d, "Comprobar").click()
    assert "Así no pudo ser" in feedback(d), feedback(d)
    boton(d, "Quitar todos").click()
    for e in I.HUELLAS["orden"]:
        clic(d, f".dn-chip[data-e='{e}']")
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def _contar(d, clave, n):
    for _ in range(n):
        clic(d, f".dn-fila[data-c='{clave}'] button[data-d='1']")


def s20(d):
    """Manada: ceros (falla), cabezas que no cuadran (falla) y los números buenos."""
    abrir_carta(d, "20")
    s = I.MANADA["solucion"]
    boton(d, "Cruzar").click()
    assert "cabezas" in feedback(d), feedback(d)
    _contar(d, "triceratops", s["velociraptor"])       # los números cambiados: mismas cabezas, otras patas
    _contar(d, "velociraptor", s["triceratops"])
    boton(d, "Cruzar").click()
    assert "patas" in feedback(d), feedback(d)
    _contar(d, "triceratops", s["triceratops"] - s["velociraptor"])
    for _ in range(s["triceratops"] - s["velociraptor"]):
        clic(d, ".dn-fila[data-c='velociraptor'] button[data-d='-1']")
    boton(d, "Cruzar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s40(d):
    """Nidos: dos nidos que se tocan (falla), nidos mal puestos (falla) y los buenos."""
    abrir_carta(d, "40")
    sol = I.NIDOS["solucion"]
    libres = [(x, y) for y in range(I.NIDOS["n"]) for x in range(I.NIDOS["n"]) if [x, y] not in I.NIDOS["helechos"]]
    a = next(c for c in libres if (c[0] + 1, c[1]) in libres)
    for c in (a, (a[0] + 1, a[1])):
        clic(d, f".dn-cel[data-x='{c[0]}'][data-y='{c[1]}']")
    boton(d, "Comprobar").click()
    assert "diagonal" in feedback(d), feedback(d)
    for c in (a, (a[0] + 1, a[1])):
        clic(d, f".dn-cel[data-x='{c[0]}'][data-y='{c[1]}']")
    for x, y in sol[:-1]:
        clic(d, f".dn-cel[data-x='{x}'][data-y='{y}']")
    boton(d, "Comprobar").click()
    assert "Desde el acantilado" in feedback(d), feedback(d)
    x, y = sol[-1]
    clic(d, f".dn-cel[data-x='{x}'][data-y='{y}']")
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s48(d):
    """Cráter: sin marcar (falla), una casilla equivocada (falla) y la buena."""
    abrir_carta(d, "48")
    sol = I.CRATER["solucion"]
    boton(d, "Ir allí").click()
    assert "Marcad antes" in feedback(d), feedback(d)
    mala = [0, 0] if sol != [0, 0] else [7, 7]
    clic(d, f".dn-cel[data-x='{mala[0]}'][data-y='{mala[1]}']")
    boton(d, "Ir allí").click()
    assert "helechos aplastados" in feedback(d), feedback(d)
    clic(d, f".dn-cel[data-x='{sol[0]}'][data-y='{sol[1]}']")
    boton(d, "Ir allí").click()
    m = feedback(d)
    cerrar(d)
    return m


def s52(d):
    """Lava: una roca que no sirve (falla) y la que desvía la lava."""
    abrir_carta(d, "52")
    sol = I.LAVA["solucion"]
    mala = next(c for c in I.LAVA["camino"][1:-1] if list(c) != sol)
    clic(d, f".dn-cel[data-x='{mala[0]}'][data-y='{mala[1]}']")
    boton(d, "¡Que baje!").click()
    time.sleep(1.6)
    assert "llega a los nidos" in feedback(d), feedback(d)
    time.sleep(1.2)
    clic(d, f".dn-cel[data-x='{sol[0]}'][data-y='{sol[1]}']")
    boton(d, "¡Que baje!").click()
    time.sleep(1.6)
    m = feedback(d)
    cerrar(d)
    return m


def s46(d):
    """Senderos: un salto sin sendero (falla), repetir un sendero (falla) y un recorrido completo."""
    abrir_carta(d, "46")
    clic(d, ".sen-claro[data-k='N']")
    assert "ningún sendero directo" in feedback(d), feedback(d)
    clic(d, ".sen-claro[data-k='P']")
    clic(d, ".sen-claro[data-k='R']")
    assert "dos veces" in feedback(d), feedback(d)
    for k in I.euler(I.SENDEROS, "R")[1:]:
        clic(d, f".sen-claro[data-k='{k}']")
    m = feedback(d)
    cerrar(d)
    return m


def s51(d):
    """Árbol: ramas vacías (falla), el orden al revés (falla) y el bueno."""
    abrir_carta(d, "51")
    boton(d, "Comprobar").click()
    assert "vacías" in feedback(d), feedback(d)
    for i, a in enumerate(reversed(I.ARBOL["solucion"])):
        clic(d, f".dn-chip[data-a='{a}']")
        clic(d, f".arb-rama[data-i='{i}']")
    boton(d, "Comprobar").click()
    assert "marcas" in feedback(d), feedback(d)
    for i, a in enumerate(I.ARBOL["solucion"]):
        clic(d, f".dn-chip[data-a='{a}']")
        clic(d, f".arb-rama[data-i='{i}']")
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s69(d):
    """Corral: a medias (falla), con un depredador al lado de su presa (falla) y el reparto bueno."""
    abrir_carta(d, "69")
    boton(d, "Cerrar el corral").click()
    assert "Faltan" in feedback(d), feedback(d)
    sol = I.CORRAL["solucion"]
    # todos en su sitio salvo que el tiranosaurio y el edmontosaurio intercambian sitio con el triceratops y el protoceratops:
    # basta con una distribución cualquiera donde tiranosaurio y edmontosaurio estén pegados
    mala = dict(sol)
    mala["tiranosaurio"], mala["triceratops"] = sol["triceratops"], sol["tiranosaurio"]
    mala["edmontosaurio"], mala["compsognato"] = sol["compsognato"], sol["edmontosaurio"]
    mala["compsognato"] = sol["edmontosaurio"]

    def poner(pos):
        for a, c in pos.items():
            clic(d, f".dn-chip[data-a='{a}']")
            clic(d, f".cor-cerco[data-x='{c[0]}'][data-y='{c[1]}']")
    poner({"tiranosaurio": [0, 0], "edmontosaurio": [1, 0], "velociraptor": [2, 0], "protoceratops": [0, 1], "compsognato": [1, 1], "triceratops": [2, 1]})
    boton(d, "Cerrar el corral").click()
    assert "pared con pared" in feedback(d), feedback(d)
    poner(sol)
    boton(d, "Cerrar el corral").click()
    m = feedback(d)
    cerrar(d)
    return m


def s72(d):
    """Planear: una montaña (falla) y un vuelo que llega."""
    abrir_carta(d, "72")
    P = I.PLANEAR
    montes = {tuple(m) for m in P["montes"]}
    x, y = P["inicio"]
    dirs = {"arriba": (0, -1), "derecha": (1, 0), "abajo": (0, 1), "izquierda": (-1, 0)}
    malo = next((k for k, (dx, dy) in dirs.items() if (x + dx, y + dy) in montes), None)
    if malo:
        clic(d, f".dn-dirs button[data-d='{malo}']")
        assert "montaña" in feedback(d), feedback(d)
    else:
        for _ in range(P["altura"] + 1):
            clic(d, ".dn-dirs button[data-d='derecha']")
            clic(d, ".dn-dirs button[data-d='izquierda']")
    boton(d, "Volver al acantilado").click()
    for k in P["solucion"]:
        clic(d, f".dn-dirs button[data-d='{k}']")
    time.sleep(0.2)
    m = feedback(d)
    cerrar(d)
    return m


def s64(d):
    """Balsa: un empujón contra la orilla (falla) y la ruta buena."""
    abrir_carta(d, "64")
    clic(d, ".dn-dirs button[data-d='abajo']")
    assert "no se mueve" in feedback(d), feedback(d)
    for k in I.BARRO["solucion"]:
        clic(d, f".dn-dirs button[data-d='{k}']")
    time.sleep(0.2)
    m = feedback(d)
    cerrar(d)
    return m


def s85(d):
    """Calibrador: un número equivocado (falla) y los años buenos."""
    abrir_carta(d, "85")
    boton(d, "Calibrar").click()
    assert "parpadea en rojo" in feedback(d), feedback(d)
    n = I.ANILLOS["solucion"]
    for i, dig in enumerate((n // 10, n % 10)):
        for _ in range(dig):
            clic(d, f".ani-rueda[data-i='{i}'] button[data-d='1']")
    boton(d, "Calibrar").click()
    m = feedback(d)
    cerrar(d)
    return m


SOLVERS = {"14": s14, "20": s20, "40": s40, "48": s48, "52": s52, "46": s46, "51": s51, "69": s69, "72": s72, "64": s64, "85": s85}
REQUIERE = {"14": ["16", "18"], "20": ["19", "21"], "40": ["41", "43", "45"], "48": ["42", "49", "53"], "52": ["54", "55", "59"],
            "46": ["37", "39", "33"], "51": ["26", "61", "63"], "69": ["70", "71"], "72": ["75", "79"], "64": ["66", "67"], "85": ["86", "87", "76"]}
