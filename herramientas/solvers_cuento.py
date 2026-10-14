"""Solucionadores de los minijuegos de «Cuento»: juegan cada app por la interfaz real (primero una jugada mala para comprobar el aviso y luego la buena)."""
import sys, time
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from bot_core import *
import instancias_cuento as IC


def clic(d, css):
    """Clic por JS: los elementos pueden estar dentro de contenedores con overflow oculto."""
    d.execute_script("arguments[0].click()", d.find_element(By.CSS_SELECTOR, css))
    time.sleep(0.05)


def s42(d):
    abrir_carta(d, "42")
    for _ in range(4):
        boton(d, "Siguiente →").click()
    texto = d.find_element(By.CSS_SELECTOR, ".far-hoja").text
    assert "ceniza" in texto.lower(), texto
    cerrar(d)
    return "(lector) " + texto[:40]


def s14(d):
    """Cartel: un movimiento que no forma cifra (falla) y luego el palito bueno."""
    abrir_carta(d, "14")
    de, a = IC.CERILLAS["desde"], IC.CERILLAS["hasta"]
    clic(d, f".cer-slot[data-k='{de[0]}'][data-s='{de[1]}']")
    clic(d, ".cer-slot[data-k='2'][data-s='0']")    # lo pone arriba del 4: no es una cifra
    assert "no existe" in feedback(d), feedback(d)
    boton(d, "Empezar de nuevo").click()
    clic(d, f".cer-slot[data-k='{de[0]}'][data-s='{de[1]}']")
    clic(d, f".cer-slot[data-k='{a[0]}'][data-s='{a[1]}']")
    time.sleep(0.2)
    m = feedback(d)
    cerrar(d)
    return m


def s20(d):
    """Puente: un plan de 17 minutos (falla) y luego el de 15."""
    abrir_carta(d, "20")

    def cruzan(lado, nombres):
        for n in nombres:
            clic(d, f".pue-orilla[data-lado='{lado}'] .pue-duende[data-n='{n}']")
        boton(d, "Cruzar").click()
        time.sleep(0.05)

    for lado, nombres in [("izq", ["Bigotes", "Abuela Musgo"]), ("der", ["Bigotes"]), ("izq", ["Bigotes", "Gruñón"]), ("der", ["Bigotes"]), ("izq", ["Bigotes", "Pétalo"])]:
        cruzan(lado, nombres)
    assert "sol ya ha salido" in feedback(d), feedback(d)
    boton(d, "Empezar de nuevo").click()
    for lado, nombres in [("izq", ["Bigotes", "Pétalo"]), ("der", ["Bigotes"]), ("izq", ["Gruñón", "Abuela Musgo"]), ("der", ["Pétalo"]), ("izq", ["Bigotes", "Pétalo"])]:
        cruzan(lado, nombres)
    m = feedback(d)
    cerrar(d)
    return m


def s40(d):
    """Salto: sin tres saltos (falla), tres saltos mal puestos (falla) y los buenos."""
    abrir_carta(d, "40")
    boton(d, "Cruzar al presente").click()
    assert "exactamente tres" in feedback(d), feedback(d)
    sol = IC.soluciones_salto()[0]

    def poner(a, i):
        clic(d, f".sal-accion[data-a='{a}']")
        clic(d, f".sal-casilla[data-i='{i}']")

    for a, i in [("plantar", 2), ("cavar", 4), ("fuego", 5)]:
        poner(a, i)
    boton(d, "Cruzar al presente").click()
    assert "sigue bloqueando" in feedback(d), feedback(d)
    boton(d, "Quitar los saltos").click()
    for i, a in sol.items():
        poner(a, i)
    boton(d, "Cruzar al presente").click()
    m = feedback(d)
    cerrar(d)
    return m


def s46(d):
    """Vidriera: los cristales empiezan solapados (falla) y luego se llevan a su sitio."""
    abrir_carta(d, "46")
    boton(d, "Comprobar").click()
    assert "solapan" in feedback(d), feedback(d)
    inicio = {"palo": (0, 0), "ese": (0, 1), "te": (2, 0)}
    meta = dict(zip(IC.VIDRIERA["piezas"], IC.VIDRIERA["solucion"]))
    for k, nombre in enumerate(["palo", "ese", "te"]):
        clic(d, f".vid-sel[data-i='{k}']")
        dx, dy = meta[nombre][0] - inicio[nombre][0], meta[nombre][1] - inicio[nombre][1]
        for _ in range(abs(dx)):
            clic(d, f".vid-mover[data-d='{'der' if dx > 0 else 'izq'}']")
        for _ in range(abs(dy)):
            clic(d, f".vid-mover[data-d='{'aba' if dy > 0 else 'arr'}']")
        if nombre == "palo":
            boton(d, "Comprobar").click()
            assert "Todavía no coincide" in feedback(d) or "solapan" in feedback(d), feedback(d)
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s51(d):
    """Hadas: sin marcar (falla), todas azules (falla) y la buena."""
    abrir_carta(d, "51")
    boton(d, "Comprobar").click()
    assert "por marcar" in feedback(d), feedback(d)
    for i in range(4):
        clic(d, f".had-hada[data-n='{i}']")
    boton(d, "Comprobar").click()
    assert "no cuadra" in feedback(d), feedback(d)
    reales = [h for h in ["azul", "roja", "roja", "azul"]]
    for i, esp in enumerate(reales):
        for _ in range(3):
            if d.find_element(By.CSS_SELECTOR, f".had-hada[data-n='{i}']").get_attribute("data-m") == esp:
                break
            clic(d, f".had-hada[data-n='{i}']")
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s64(d):
    """Rayos: tres espejos mal puestos (falla) y los buenos."""
    abrir_carta(d, "64")
    boton(d, "Comprobar").click()
    assert "exactamente 3" in feedback(d), feedback(d)
    for i in (6, 7, 8):
        clic(d, f".ray-cel[data-i='{i}']")
    boton(d, "Comprobar").click()
    assert "no llega" in feedback(d), feedback(d)
    boton(d, "Quitar todos").click()
    for celda, o in IC.RAYOS["solucion"]:
        for _ in range(1 if o == "/" else 2):
            clic(d, f".ray-cel[data-i='{celda}']")
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s69(d):
    """Tarros: un vertido que no se puede hacer (falla) y luego los once movimientos."""
    abrir_carta(d, "69")
    ruta = IC.POCIONES["ruta"]
    a, b = ruta[0]
    clic(d, f".tar-tubo[data-i='{a}']")
    clic(d, f".tar-tubo[data-i='{b}']")
    clic(d, ".tar-tubo[data-i='1']")               # dorado sobre rosa: no se puede
    clic(d, f".tar-tubo[data-i='{b}']")
    assert "No se puede verter" in feedback(d), feedback(d)
    for a, b in ruta[1:]:
        clic(d, f".tar-tubo[data-i='{a}']")
        clic(d, f".tar-tubo[data-i='{b}']")
    time.sleep(0.2)
    m = feedback(d)
    cerrar(d)
    return m


def s72(d):
    """Caja de música: una nota equivocada (falla) y luego la melodía."""
    abrir_carta(d, "72")
    clic(d, ".caj-nota[data-n='Do']")
    assert "carta 76" in feedback(d), feedback(d)
    for n in IC.SOLUCION_MUSICA:
        clic(d, f".caj-nota[data-n='{n}']")
    time.sleep(0.2)
    m = feedback(d)
    cerrar(d)
    return m


def s84(d):
    """Última página: las letras en el orden de las cartas (falla) y la palabra buena."""
    abrir_carta(d, "84")
    boton(d, "Comprobar").click()
    assert "Colocad las siete letras" in feedback(d) or "faltan" in feedback(d).lower(), feedback(d)
    for i in range(7):
        clic(d, f".pag-letra[data-n='{i}']")
    boton(d, "Comprobar").click()
    assert "no es la palabra" in feedback(d), feedback(d)
    boton(d, "Quitar todas").click()
    letras = [d.find_element(By.CSS_SELECTOR, f".pag-letra[data-n='{i}']").get_attribute("data-l") for i in range(7)]
    usadas = set()
    for ch in IC.PALABRA:
        i = next(k for k, l in enumerate(letras) if l == ch and k not in usadas)
        usadas.add(i)
        clic(d, f".pag-letra[data-n='{i}']")
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


SOLVERS = {"42": s42, "14": s14, "20": s20, "40": s40, "46": s46, "51": s51, "64": s64, "69": s69, "72": s72, "84": s84}
REQUIERE = {"14": ["16"], "20": ["18"], "40": ["42"], "46": ["48", "37"], "51": ["52", "26"], "64": ["66"], "69": ["70"], "72": ["76"], "84": ["86"]}
