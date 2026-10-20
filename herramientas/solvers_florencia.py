import sys, time
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from bot_core import *


def clic_js(d, css):
    """Clic sobre elementos SVG (no siempre se pueden pulsar con el raton de Selenium)."""
    d.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}))", d.find_element(By.CSS_SELECTOR, css))
    time.sleep(0.04)


def s24(d):
    """Cofre: teclado de 4 cifras (2759)."""
    abrir_carta(d, "24")
    for ch in "1111":
        tecla(d, ch)
    tecla(d, "✓")
    assert "no se abre" in feedback(d), feedback(d)
    for ch in "2759":
        tecla(d, ch)
    tecla(d, "✓")
    m = feedback(d)
    cerrar(d)
    return m


def s32(d):
    """Disco de Alberti: la A de fuera sobre la F de dentro; palabra LEON."""
    abrir_carta(d, "32")
    for ch in "ABCD":
        tecla(d, ch)
    boton(d, "Comprobar").click()
    assert "no abre nada" in feedback(d), feedback(d)
    for _ in range(4):
        boton(d, "Borrar").click()
    giro = d.find_element(By.CSS_SELECTOR, ".far-par").get_attribute("data-giro")
    assert giro == "0", giro
    clic_js(d, ".far-d-in[data-l='F']")      # letra de dentro
    clic_js(d, ".far-d-out[data-l='A']")     # letra de fuera
    giro = d.find_element(By.CSS_SELECTOR, ".far-par").get_attribute("data-giro")
    assert giro == "5", f"el disco deberia estar en 5 y esta en {giro}"
    # descifrar el pergamino leyendo la tabla del disco: JQ QJTS LZFWIF XZ HTWFETS
    tabla = {}
    celdas = d.find_elements(By.CSS_SELECTOR, ".far-tabla2 > div:not(.et)")
    fuera = [c.text for c in celdas if "in" not in (c.get_attribute("class") or "")]
    dentro = [c.text for c in celdas if "in" in (c.get_attribute("class") or "")]
    for f, i in zip(fuera, dentro):
        tabla[i] = f
    claro = "".join(tabla.get(c, c) for c in "QJTS")
    assert claro == "LEON", claro
    for ch in claro:
        tecla(d, ch)
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s38(d):
    """Engranajes: primero la cadena corta (la cuerda gira a la mitad), luego la buena: D=pequena, B=mediana, Z=mediana."""
    abrir_carta(d, "38")

    def poner(peg, r):
        d.find_element(By.CSS_SELECTOR, f".far-g-rueda[data-r='{r}']:not(:disabled)").click()
        clic_js(d, f".far-g-peg[data-peg='{peg}']")

    boton(d, "Girar manivela").click()
    assert "Falta la rueda" in feedback(d), feedback(d)
    poner("D", 1)
    poner("Z", 4)
    boton(d, "Girar manivela").click()
    assert "la mitad de rápido" in feedback(d), feedback(d)
    boton(d, "Quitar todo").click()
    poner("Z", 2)                              # suelta, sin unir
    boton(d, "Girar manivela").click()
    assert "no se mueve" in feedback(d), feedback(d)
    boton(d, "Quitar todo").click()
    poner("D", 1)
    poner("B", 2)
    poner("Z", 2)
    boton(d, "Girar manivela").click()
    time.sleep(0.2)
    m = feedback(d)
    cerrar(d)
    return m


SOL_CUADRADO = [16, 3, 2, 13, 5, 10, 11, 8, 9, 6, 7, 12, 4, 15, 14, 1]
BLOQ = {0, 2, 12}


def s54(d):
    """Cuadrado magico: primero con dos numeros cambiados de sitio, luego bien."""
    abrir_carta(d, "54")
    boton(d, "Comprobar").click()
    assert "Aún quedan casillas vacías" in feedback(d), feedback(d)

    def poner(i, n):
        d.find_element(By.CSS_SELECTOR, f".far-q-cell[data-i='{i}']").click()
        d.find_element(By.CSS_SELECTOR, f".far-q-num[data-n='{n}']").click()

    sol = list(SOL_CUADRADO)
    mala = list(sol)
    mala[1], mala[3] = mala[3], mala[1]
    for i in range(16):
        if i not in BLOQ:
            poner(i, mala[i])
    boton(d, "Comprobar").click()
    assert "no suma" in feedback(d), feedback(d)
    poner(1, sol[1])
    poner(3, sol[3])
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s58(d):
    """Cisterna: llenar grande, verter, vaciar pequena, verter, llenar grande, verter."""
    abrir_carta(d, "58")
    for txt in ["Llenar grande", "Verter grande → pequeña", "Vaciar pequeña", "Verter grande → pequeña", "Llenar grande", "Verter grande → pequeña"]:
        boton(d, txt).click()
        time.sleep(0.03)
    time.sleep(0.2)
    m = feedback(d)
    cerrar(d)
    return m


def s66(d):
    """Ornitoptero: ala larga, seda, 2 sacos."""
    abrir_carta(d, "66")

    def elegir(g, v):
        d.find_element(By.CSS_SELECTOR, f".far-o-opt[data-g='{g}'][data-v='{v}']").click()

    boton(d, "Probar vuelo").click()
    assert "Elige un ala" in feedback(d), feedback(d)
    for g, v in [("ala", "corta"), ("tela", "lino"), ("lastre", "1")]:
        elegir(g, v)
    boton(d, "Probar vuelo").click()
    assert "se desploma" in feedback(d), feedback(d)
    for g, v in [("ala", "larga"), ("tela", "seda"), ("lastre", "3")]:
        elegir(g, v)
    boton(d, "Probar vuelo").click()
    assert "se desploma" in feedback(d), feedback(d)
    elegir("lastre", "2")
    boton(d, "Probar vuelo").click()
    time.sleep(0.2)
    m = feedback(d)
    cerrar(d)
    return m


def s92(d):
    """Espejos: lente en B3 (1,2); espejos \\ en A2 (0,1), \\ en C2 (2,1) y / en C3 (2,2)."""
    abrir_carta(d, "92")

    def herramienta(h):
        d.find_element(By.CSS_SELECTOR, f".far-e-tool[data-tool='{h}']").click()

    def celda(x, y, veces=1):
        for _ in range(veces):
            clic_js(d, f".far-e-cell[data-c='{x},{y}']")

    boton(d, "Probar").click()
    assert "Falta la lente" in feedback(d), feedback(d)
    herramienta("lente")
    celda(0, 0)                                    # no es un atril
    assert "solo cabe en un atril" in feedback(d), feedback(d)
    celda(4, 2)                                    # atril equivocado
    boton(d, "Probar").click()
    assert "Probar" and feedback(d) != "", feedback(d)
    celda(1, 2)                                    # atril bueno (B3)
    herramienta("espejo")
    celda(0, 1, 2)                                 # \ en A2
    celda(2, 1, 2)                                 # \ en C2
    celda(2, 2, 1)                                 # / en C3
    boton(d, "Probar").click()
    time.sleep(0.2)
    m = feedback(d)
    cerrar(d)
    return m


SOLVERS = {"24": s24, "32": s32, "38": s38, "54": s54, "58": s58, "66": s66, "92": s92}
REQUIERE = {"24": ["26"], "32": ["28", "35"], "38": ["40", "42"], "54": ["56"], "58": ["60"], "66": ["68", "70", "71"], "92": ["84", "72", "94"]}


# ---- ampliación a 36 cartas: el baúl de viaje
import json as _json, os  # noqa: E402
_AMP = _json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "instancias_ampliacion.json"), encoding="utf-8"))


def _clic(d, css):
    d.execute_script("arguments[0].click()", d.find_element(By.CSS_SELECTOR, css))
    time.sleep(0.04)


def _girar(celdas, veces):
    p = [tuple(c) for c in celdas]
    for _ in range(veces):
        p = [(y, -x) for x, y in p]
    mx, my = min(x for x, _ in p), min(y for _, y in p)
    return sorted((x - mx, y - my) for x, y in p)


def s46(d):
    """Baúl: una caja que se sale (avisa) y luego un encaje que lo llena."""
    abrir_carta(d, "46")
    b = _AMP["florencia_baul"]
    _clic(d, ".flo-caja[data-p='carro']")
    _clic(d, f".flo-celda[data-x='{b['ancho'] - 1}'][data-y='{b['alto'] - 1}']")
    assert "no cabe" in feedback(d), feedback(d)
    for nombre, celdas in b["soluciones"][0].items():
        mx, my = min(x for x, _ in celdas), min(y for _, y in celdas)
        rel = sorted((x - mx, y - my) for x, y in celdas)
        giro = next(k for k in range(4) if _girar(b["piezas"][nombre], k) == rel)
        _clic(d, f".flo-caja[data-p='{nombre}']")
        for _ in range(giro):
            boton(d, "Girar la caja").click()
        _clic(d, f".flo-celda[data-x='{mx}'][data-y='{my}']")
    m = feedback(d)
    cerrar(d)
    return m


SOLVERS.update({"46": s46})
REQUIERE.update({"46": ["47", "48", "49", "50"]})
