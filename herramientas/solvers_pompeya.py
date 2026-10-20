import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bot_core import *

# Pompeya (60 cartas): las soluciones salen de instancias_pompeya.json, no de copias escritas a mano.
I = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "instancias_pompeya.json"), encoding="utf-8"))


def clic(d, css):
    d.execute_script("arguments[0].click()", d.find_element(By.CSS_SELECTOR, css))
    time.sleep(0.03)


def s13(d):
    """Panel: un orden equivocado (falla) y luego las figuras del camino."""
    abrir_carta(d, "13")
    sol = I["laberinto"]["solucion"]
    for f in sol[::-1]:
        clic(d, f".pom-fig[data-f='{f}']")
    boton(d, "Empujar la puerta").click()
    assert "no cede" in feedback(d), feedback(d)
    boton(d, "Quitar las figuras").click()
    for f in sol:
        clic(d, f".pom-fig[data-f='{f}']")
    boton(d, "Empujar la puerta").click()
    m = feedback(d)
    cerrar(d)
    return m


def _abaco(d, n):
    for k, v in (("M", 1000), ("C", 100), ("X", 10), ("I", 1)):
        dig = n // v % 10
        if dig >= 5:
            clic(d, f".pom-cuenta[data-col='{k}'][data-t='5']")
        if dig % 5:
            clic(d, f".pom-cuenta[data-col='{k}'][data-t='1'][data-i='{dig % 5 - 1}']")


def s20(d):
    """Arca: el total de Tiro (con su error) falla y luego el verdadero."""
    abrir_carta(d, "20")
    cu = I["cuentas"]
    _abaco(d, sum(x["escrito"] for x in cu["dias"]))
    boton(d, "Abrir el arca").click()
    assert "no se mueve" in feedback(d), feedback(d)
    cerrar(d)
    abrir_carta(d, "20")
    _abaco(d, cu["total"])
    boton(d, "Abrir el arca").click()
    m = feedback(d)
    cerrar(d)
    return m


def s28(d):
    """Joyero: el anillo idéntico a la impronta (falla) y luego el bueno."""
    abrir_carta(d, "28")
    clic(d, ".pom-anillo[data-a='b']")
    boton(d, "Sellar").click()
    assert "no deja esa marca" in feedback(d), feedback(d)
    clic(d, f".pom-anillo[data-a='{I['sello']['solucion']}']")
    boton(d, "Sellar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s33(d):
    """Compuertas: todas abiertas (riego mal) y luego la combinación justa."""
    abrir_carta(d, "33")
    fu = I["fuente"]
    for c in fu["compuertas"]:
        clic(d, f".pom-pal[data-c='{c}']")
    boton(d, "Abrir el agua").click()
    assert "no reciben" in feedback(d) or "desborda" in feedback(d), feedback(d)
    for c in fu["compuertas"]:
        if c not in fu["solucion"]:
            clic(d, f".pom-pal[data-c='{c}']")
    boton(d, "Abrir el agua").click()
    m = feedback(d)
    cerrar(d)
    return m


def s40(d):
    """Tablilla: SATOR (falla) y luego la palabra de la cruz."""
    abrir_carta(d, "40")
    for l in "SATOR":
        clic(d, f".pom-teclas button[data-l='{l}']")
    boton(d, "Apretar la tablilla").click()
    assert "sigue cerrado" in feedback(d), feedback(d)
    boton(d, "Alisar la cera").click()
    for l in I["sator"]["solucion"]:
        clic(d, f".pom-teclas button[data-l='{l}']")
    boton(d, "Apretar la tablilla").click()
    m = feedback(d)
    cerrar(d)
    return m


def s46(d):
    """Balanza: en la muesca 1 (falla) y luego en la buena."""
    abrir_carta(d, "46")
    boton(d, "Soltar la balanza").click()
    assert "torcido" in feedback(d), feedback(d)
    for _ in range(I["statera"]["muesca"] - 1):
        clic(d, ".pom-giro button[data-d='1']")
    boton(d, "Soltar la balanza").click()
    m = feedback(d)
    cerrar(d)
    return m


def s55(d):
    """Casa: la de la esquina (falla, salvo que sea la buena) y luego la que dejan los grafitos."""
    abrir_carta(d, "55")
    f, c = I["calles"]["solucion"]
    mala = (0, 0) if (f, c) != (0, 0) else (0, 1)
    clic(d, f".pom-casa[data-f='{mala[0]}'][data-c='{mala[1]}']")
    boton(d, "Llamar a la puerta").click()
    assert "vecino" in feedback(d), feedback(d)
    clic(d, f".pom-casa[data-f='{f}'][data-c='{c}']")
    boton(d, "Llamar a la puerta").click()
    m = feedback(d)
    cerrar(d)
    return m


def s59(d):
    """Calendario: el día 23 (falla: contar sin incluir las calendas) y luego el bueno."""
    abrir_carta(d, "59")
    dia = I["calendario"]["dia"]
    clic(d, f".pom-dia[data-d='{dia - 1}']")
    boton(d, "Entregar al sacerdote").click()
    assert "no es el día" in feedback(d), feedback(d)
    clic(d, f".pom-dia[data-d='{dia}']")
    boton(d, "Entregar al sacerdote").click()
    m = feedback(d)
    cerrar(d)
    return m


def s66(d):
    """Huida: por una calle cortada (falla) y luego la ruta buena."""
    abrir_carta(d, "66")
    for n in ("A", "C", "G", "P"):
        clic(d, f".pom-nodo[data-n='{n}']")
    boton(d, "¡Corred!").click()
    assert "cortada" in feedback(d), feedback(d)
    for n in I["huida"]["solucion"][1:]:
        clic(d, f".pom-nodo[data-n='{n}']")
    boton(d, "¡Corred!").click()
    m = feedback(d)
    cerrar(d)
    return m


def s70(d):
    """Barca: todo (se hunde) y luego la carga óptima."""
    abrir_carta(d, "70")
    ba = I["barca"]
    for k in ba["carga"]:
        clic(d, f".pom-bulto[data-k='{k}']")
    boton(d, "Zarpar").click()
    assert "hundirse" in feedback(d), feedback(d)
    for k in ba["carga"]:
        if k not in ba["solucion"]:
            clic(d, f".pom-bulto[data-k='{k}']")
    boton(d, "Zarpar").click()
    m = feedback(d)
    cerrar(d)
    return m


SOLVERS = {"13": s13, "20": s20, "28": s28, "33": s33, "40": s40, "46": s46, "55": s55, "59": s59, "66": s66, "70": s70}
REQUIERE = {"13": ["14", "15", "16", "17", "18"], "20": ["21", "23", "24", "25"], "28": ["27", "29"], "33": ["36", "37"], "40": ["41", "42"],
            "46": ["43", "45"], "55": ["51", "52", "53", "54"], "59": ["61", "63", "65"], "66": ["67", "75"], "70": ["71", "72", "76"]}
