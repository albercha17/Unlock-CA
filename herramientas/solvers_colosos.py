"""Solucionadores de los minijuegos de «Altamuralla: El Valle de los Colosos» (60 cartas): juegan cada app por la interfaz real, primero una jugada
mala para comprobar el aviso y luego la buena. Las soluciones salen de instancias_colosos.py."""
import sys
import time
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from bot_core import *  # noqa: E402,F401,F403
import instancias_colosos as I  # noqa: E402

D = I.INST


def clic(d, css):
    d.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}))", d.find_element(By.CSS_SELECTOR, css))
    time.sleep(0.03)


def celda(d, f, c):
    clic(d, f".co-c[data-f='{f}'][data-c='{c}']")


def fin(d):
    m = feedback(d)
    cerrar(d)
    return m


def s14(d):
    """Faroles: un solo farol (quedan losas a oscuras) y luego la solución."""
    abrir_carta(d, "14")
    f, c = D["faroles"]["solucion"][0]
    celda(d, f, c)
    boton(d, "Encender").click()
    assert "oscuras" in feedback(d), feedback(d)
    boton(d, "Apagar todo").click()
    for f, c in D["faroles"]["solucion"]:
        celda(d, f, c)
    boton(d, "Encender").click()
    return fin(d)


def s20(d):
    """Crónica: orden equivocado y luego el bueno."""
    abrir_carta(d, "20")
    sol = D["cronica"]["solucion"]
    for i in sol[::-1]:
        clic(d, f"[data-suceso='{i}']")
    boton(d, "Comprobar").click()
    assert "niega" in feedback(d), feedback(d)
    for i in sol:
        clic(d, f"[data-suceso='{i}']")
    boton(d, "Comprobar").click()
    return fin(d)


def s40(d):
    """Barracones: todo a 1 (mal) y luego la solución."""
    abrir_carta(d, "40")
    n = D["barracones"]["n"]
    for f in range(n):
        for c in range(n):
            celda(d, f, c)
    boton(d, "Repartir").click()
    assert "intendente" in feedback(d), feedback(d)
    for f in range(n):
        for c in range(n):
            for _ in range(D["barracones"]["solucion"][f"{f},{c}"] - 1):
                celda(d, f, c)
    boton(d, "Repartir").click()
    return fin(d)


def s48(d):
    """Inscripción: la frase en el orden castellano (mal) y luego la buena."""
    abrir_carta(d, "48")
    ins = D["inscripcion"]
    obj = ins["objetivo"]["glifos"]
    for w in reversed(obj):
        clic(d, f".co-glifo[data-g='{ins['forma'][w]}']")
    boton(d, "Grabar").click()
    assert "ceño" in feedback(d), feedback(d)
    for w in obj:
        clic(d, f".co-glifo[data-g='{ins['forma'][w]}']")
    boton(d, "Grabar").click()
    return fin(d)


def _llenar(d, persona, ml):
    b = d.find_element(By.CSS_SELECTOR, f".co-jer[data-persona='{persona}'] .co-llenar")
    for _ in range(ml):
        d.execute_script("arguments[0].dispatchEvent(new PointerEvent('pointerdown', {bubbles: true}));"
                         "arguments[0].dispatchEvent(new PointerEvent('pointerup', {bubbles: true}));", b)
        time.sleep(0.02)


def s52(d):
    """Dosis: las dosis cambiadas (mal) y luego las buenas."""
    abrir_carta(d, "52")
    do = D["dosis"]["dosis"]
    _llenar(d, "Cristina", do["Alberto"])
    _llenar(d, "Alberto", do["Cristina"])
    boton(d, "Inyectar").click()
    assert "dosis no" in feedback(d), feedback(d)
    _llenar(d, "Cristina", do["Cristina"])
    _llenar(d, "Alberto", do["Alberto"])
    boton(d, "Inyectar").click()
    return fin(d)


def s46(d):
    """Pisadas: dos pisadas juntas (se hunde) y luego la solución."""
    abrir_carta(d, "46")
    celda(d, 0, 0)
    celda(d, 0, 1)
    boton(d, "Cruzar la plaza").click()
    assert "hunde" in feedback(d), feedback(d)
    boton(d, "Borrar pisadas").click()
    for f, c in D["pisadas"]["solucion"]:
        celda(d, f, c)
    boton(d, "Cruzar la plaza").click()
    return fin(d)


def s51(d):
    """Canto: una palabra equivocada y luego las tres rondas."""
    abrir_carta(d, "51")
    sol = D["canto"]["solucion"]
    mala = next(w for w in D["canto"]["respuestas"] if w != sol[0][0])
    clic(d, f"[data-palabra='{mala}']")
    assert "confundidos" in feedback(d), feedback(d)
    time.sleep(0.3)
    for ronda in sol:
        for w in ronda:
            clic(d, f"[data-palabra='{w}']")
        time.sleep(0.3)
    return fin(d)


def s69(d):
    """Ofrendas: todas (mal) y luego las buenas."""
    abrir_carta(d, "69")
    for i in range(6):
        clic(d, f"[data-ofrenda='{i}']")
    boton(d, "Ofrecer").click()
    assert "gruñe" in feedback(d), feedback(d)
    for i in D["ofrendas"]["solucion"]:
        clic(d, f"[data-ofrenda='{i}']")
    boton(d, "Ofrecer").click()
    return fin(d)


def _palanca_buena(d, hist):
    esfera = int(d.find_element(By.ID, "coEsfera").text)
    orden = [b.get_attribute("data-sim") for b in d.find_elements(By.CSS_SELECTOR, ".co-palanca")]
    t, x = D["palancas"]["reglas"][len(hist)][esfera - 1]
    if t == "pos":
        p = x
    elif t == "sim":
        p = orden.index(x)
    elif t == "igual_pos":
        p = hist[x][0]
    else:
        p = orden.index(hist[x][1])
    return p, orden[p]


def s72(d):
    """Palancas: una palanca equivocada en la etapa 1 y luego las cinco etapas leyendo la esfera."""
    abrir_carta(d, "72")
    p, _ = _palanca_buena(d, [])
    clic(d, f".co-palanca[data-pos='{(p + 1) % 4}']")
    assert "atascan" in feedback(d), feedback(d)
    time.sleep(0.9)
    hist = []
    for _ in range(5):
        p, s = _palanca_buena(d, hist)
        clic(d, f".co-palanca[data-pos='{p}']")
        hist.append((p, s))
        time.sleep(0.8)
    return fin(d)


def s64(d):
    """Tesoro: un montón mezclado (mal) y luego los cuatro montones."""
    abrir_carta(d, "64")
    G = D["tesoro"]["grupos"]
    L = "ABCDEFGHIJKLMNOP"
    for i in [G[0][0], G[1][0], G[2][0], G[3][0]]:
        clic(d, f"[data-letra='{L[i]}']")
    boton(d, "Juntar").click()
    assert "deshace" in feedback(d), feedback(d)
    for g in G:
        for i in g:
            clic(d, f"[data-letra='{L[i]}']")
        boton(d, "Juntar").click()
    return fin(d)


def s85(d):
    """Panel: palabra equivocada y luego HOGAR."""
    abrir_carta(d, "85")
    for ch in "LUNAS":
        tecla(d, ch)
    boton(d, "Encender").click()
    assert "rojo" in feedback(d), feedback(d)
    for ch in D["meta"]["palabra"]:
        tecla(d, ch)
    boton(d, "Encender").click()
    return fin(d)


SOLVERS = {"14": s14, "20": s20, "40": s40, "48": s48, "52": s52, "46": s46, "51": s51, "64": s64, "69": s69, "72": s72, "85": s85}
# cartas que hay que tener en mesa para poder resolver cada minijuego
REQUIERE = {"14": ["16"], "20": ["18", "19", "21"], "40": ["41", "43", "45"], "48": ["42", "49", "53"], "52": ["54", "55", "59"], "46": ["37", "39", "33"],
            "51": ["26", "61", "63"], "64": ["66", "67"], "69": ["70", "71"], "72": ["75", "79"], "85": ["86", "87"]}
