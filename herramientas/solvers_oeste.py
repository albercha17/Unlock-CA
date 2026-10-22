"""Solucionadores de los minijuegos de «Dry Gulch, 1878» (60 cartas): juegan cada app por la interfaz real, primero una jugada mala para comprobar el aviso
y luego la buena. Las soluciones salen de instancias_oeste.py."""
import sys, time
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from bot_core import *
import instancias_oeste as I


def clic(d, css):
    """Clic por JS: los elementos pueden estar dentro de contenedores con overflow oculto."""
    d.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}))", d.find_element(By.CSS_SELECTOR, css))
    time.sleep(0.03)


def cel(d, r, c):
    clic(d, f".oe-cel[data-r='{r}'][data-c='{c}']")


def escribe(d, css, texto):
    d.execute_script("var e = document.querySelector(arguments[0]); e.value = arguments[1]; e.dispatchEvent(new Event('input'));", css, texto)


def s14(d):
    """Telegrama: demasiado corto (falla), de la longitud justa pero equivocado (falla) y el mensaje."""
    abrir_carta(d, "14")
    escribe(d, ".tel-in", "EL ORO")
    boton(d, "Entregar el mensaje").click()
    assert "letras" in feedback(d), feedback(d)
    escribe(d, ".tel-in", "A" * len(I.VALLAS["claro"]))
    boton(d, "Entregar el mensaje").click()
    assert "arruga" in feedback(d), feedback(d)
    escribe(d, ".tel-in", I.VALLAS["claro"].lower())
    boton(d, "Entregar el mensaje").click()
    m = feedback(d)
    cerrar(d)
    return m


def s20(d):
    """Banco: sin tachar (falla), dos tachones vecinos (falla) y los tachones buenos."""
    abrir_carta(d, "20")
    boton(d, "Comprobar").click()
    assert "Todavía no" in feedback(d), feedback(d)
    cel(d, 0, 0)
    cel(d, 0, 1)
    boton(d, "Comprobar").click()
    assert "se tocan" in feedback(d), feedback(d)
    boton(d, "Borrar todo").click()
    for r, f in enumerate(I.HITORI["tachones"]):
        for c, v in enumerate(f):
            if v:
                cel(d, r, c)
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s40(d):
    """Caja: sin llenar (falla), todo con la pieza A (falla) y el relleno bueno."""
    abrir_carta(d, "40")
    boton(d, "Comprobar").click()
    assert "sin llenar" in feedback(d), feedback(d)
    for r in range(I.PENTOMINO["filas"]):
        for c in range(I.PENTOMINO["cols"]):
            cel(d, r, c)
    boton(d, "Comprobar").click()
    assert "no tiene la forma" in feedback(d), feedback(d)
    boton(d, "Borrar todo").click()
    for k, letra in enumerate(I.PENTOMINO["piezas"]):
        clic(d, f".caj-pal button[data-p='{'ABCDEF'[k]}']")
        for r, c in I.PENTOMINO["solucion"][letra]:
            cel(d, r, c)
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s48(d):
    """Apuestas: sin rellenar (falla), todo unos (falla) y el cuadro bueno."""
    abrir_carta(d, "48")
    boton(d, "Comprobar").click()
    assert "sin cifra" in feedback(d), feedback(d)
    sol = {tuple(map(int, k.split(","))): v for k, v in I.KAKURO["solucion"].items()}

    def poner(plan):
        for (r, c), v in plan.items():
            cel(d, r, c)
            clic(d, f".kak-nums button[data-n='{v}']")
    poner({q: 1 for q in sol})
    boton(d, "Comprobar").click()
    assert "repetida" in feedback(d), feedback(d)
    poner(sol)
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s52(d):
    """Carga: vacío (falla), todo (peso) y solo una cosa (se puede más); luego la mejor carga."""
    abrir_carta(d, "52")
    boton(d, "Cargar el carro").click()
    assert "vacío" in feedback(d), feedback(d)
    for i in range(len(I.MOCHILA["pesos"])):
        clic(d, f".car-art[data-i='{i}']")
    boton(d, "Cargar el carro").click()
    assert "pasado de peso" in feedback(d), feedback(d)
    boton(d, "Descargar todo").click()
    clic(d, f".car-art[data-i='{I.MOCHILA['solucion'][0]}']")
    boton(d, "Cargar el carro").click()
    assert "cartera más gorda" in feedback(d), feedback(d)
    for i in I.MOCHILA["solucion"][1:]:
        clic(d, f".car-art[data-i='{i}']")
    boton(d, "Cargar el carro").click()
    m = feedback(d)
    cerrar(d)
    return m


def s46(d):
    """Duelo: un asiento que cae y el que sobrevive."""
    abrir_carta(d, "46")
    boton(d, "Sentarse").click()
    assert "Elegid primero" in feedback(d), feedback(d)
    clic(d, ".due-as[data-s='1']")
    boton(d, "Sentarse").click()
    assert "disparo número" in feedback(d), feedback(d)
    clic(d, f".due-as[data-s='{I.JOSEFO['sobrevive']}']")
    boton(d, "Sentarse").click()
    m = feedback(d)
    cerrar(d)
    return m


def s51(d):
    """Bodega: pasos hacia un muro (nada), reiniciar y la solución."""
    abrir_carta(d, "51")
    for _ in range(3):
        clic(d, ".bod-mv[data-m='L']")
    boton(d, "Empezar de nuevo").click()
    for m in I.SOKOBAN["solucion"]:
        clic(d, f".bod-mv[data-m='{m}']")
    m = feedback(d)
    cerrar(d)
    return m


def s64(d):
    """Bomba: tubos como están (falla) y todos girados a la solución."""
    abrir_carta(d, "64")
    boton(d, "Abrir la llave").click()
    assert "extremo abierto" in feedback(d) or "redes sueltas" in feedback(d) or "plano" in feedback(d), feedback(d)
    sol = I.TUBERIAS["solucion"]
    for r in range(I.TUBERIAS["n"]):
        for c in range(I.TUBERIAS["n"]):
            for _ in range(4):
                if d.find_element(By.CSS_SELECTOR, f".bom-c[data-r='{r}'][data-c='{c}']").get_attribute("data-m") == str(sol[r][c]):
                    break
                clic(d, f".bom-c[data-r='{r}'][data-c='{c}']")
    boton(d, "Abrir la llave").click()
    m = feedback(d)
    cerrar(d)
    return m


def s69(d):
    """Maniobra: sacar del apartadero vacío (falla), sacar en orden inverso (sale desordenado) y la maniobra buena."""
    abrir_carta(d, "69")
    boton(d, "Sacar del apartadero").click()
    assert "vacío" in feedback(d), feedback(d)
    n = len(I.VAGONES["pesos"])
    for _ in range(n):
        boton(d, "Entrar al apartadero").click()
    for _ in range(n):
        boton(d, "Sacar del apartadero").click()
    assert "desordenado" in feedback(d), feedback(d)
    for o in I.VAGONES["ops"]:
        boton(d, "Entrar al apartadero" if o == "E" else "Sacar del apartadero").click()
    m = feedback(d)
    cerrar(d)
    return m


def s72(d):
    """Hierros: una res falsa (falla), solo una buena (faltan) y las tres."""
    abrir_carta(d, "72")
    buenas = [i + 1 for i in I.HIERROS["autenticos"]]
    falsa = next(i for i in range(1, 9) if i not in buenas)
    clic(d, f".hie-op[data-i='{falsa}']")
    boton(d, "Entregar la lista").click()
    assert "falso" in feedback(d), feedback(d)
    boton(d, "Quitar marcas").click()
    clic(d, f".hie-op[data-i='{buenas[0]}']")
    boton(d, "Entregar la lista").click()
    assert "faltan" in feedback(d), feedback(d)
    for i in buenas[1:]:
        clic(d, f".hie-op[data-i='{i}']")
    boton(d, "Entregar la lista").click()
    m = feedback(d)
    cerrar(d)
    return m


def s85(d):
    """Válvula: cinco letras equivocadas (falla) y VAPOR."""
    abrir_carta(d, "85")
    for ch in "AAAAA":
        clic(d, f".pol-teclado button[data-k='{ch}']")
    boton(d, "Abrir la válvula").click()
    assert "no cede" in feedback(d), feedback(d)
    for _ in range(5):
        boton(d, "Borrar una").click()
    for ch in I.PALABRA:
        clic(d, f".pol-teclado button[data-k='{ch}']")
    boton(d, "Abrir la válvula").click()
    m = feedback(d)
    cerrar(d)
    return m


SOLVERS = {"14": s14, "20": s20, "40": s40, "48": s48, "52": s52, "46": s46, "51": s51, "64": s64, "69": s69, "72": s72, "85": s85}
REQUIERE = {"14": ["16"], "20": ["18", "19", "21"], "40": ["41", "43", "45"], "48": ["42", "49", "53"], "52": ["54", "55", "59"], "46": ["37", "39", "33"],
            "51": ["26", "61", "63"], "64": ["66", "67"], "69": ["70", "71"], "72": ["75", "79"], "85": ["86", "87"]}
