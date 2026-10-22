"""Solucionadores de los minijuegos de «La Final del Siglo, 1970» (60 cartas): juegan cada app por la interfaz real, primero una jugada mala para comprobar
el aviso y luego la buena. Las soluciones salen de instancias_futbol.py."""
import sys, time
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from bot_core import *
import instancias_futbol as I


def clic(d, css):
    """Clic por JS: los elementos pueden estar dentro de contenedores con overflow oculto."""
    d.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}))", d.find_element(By.CSS_SELECTOR, css))
    time.sleep(0.03)


def ajusta(d, nombre, objetivo):
    """Lleva un contador (+/−) hasta el valor pedido."""
    css = f".fu-cont[data-nombre='{nombre}']"
    for _ in range(80):
        v = int(d.find_element(By.CSS_SELECTOR, css).get_attribute("data-v"))
        if v == objetivo:
            return
        clic(d, css + (" button[data-d='1']" if v < objetivo else " button[data-d='-1']"))
    raise Fallo("no llego a " + str(objetivo) + " en " + nombre)


def s14(d):
    """Liguilla: todo a cero (falla), un marcador cambiado (falla) y los cuatro buenos."""
    abrir_carta(d, "14")
    L = I.LIGUILLA
    boton(d, "Entregar la tabla").click()
    assert "no sale" in feedback(d), feedback(d)
    for i in L["desconocidos"]:
        x, y = L["resultados"][i]
        ajusta(d, f"l{i}a", x)
        ajusta(d, f"l{i}b", y)
    i0 = L["desconocidos"][0]
    ajusta(d, f"l{i0}a", L["resultados"][i0][0] + 1)
    boton(d, "Entregar la tabla").click()
    assert "no sale" in feedback(d), feedback(d)
    ajusta(d, f"l{i0}a", L["resultados"][i0][0])
    boton(d, "Entregar la tabla").click()
    m = feedback(d)
    cerrar(d)
    return m


def s20(d):
    """Convocatoria: una sola camiseta (falla), dos equivocadas (falla) y las dos buenas."""
    abrir_carta(d, "20")
    sol = I.CROMOS["solucion"]
    mala = [j["dorsal"] for j in I.CROMOS["jugadores"] if j["dorsal"] not in sol]
    clic(d, f".conv-g button[data-d='{sol[0]}']")
    boton(d, "Presentar la lista").click()
    assert "exactamente dos" in feedback(d), feedback(d)
    clic(d, f".conv-g button[data-d='{mala[0]}']")
    boton(d, "Presentar la lista").click()
    assert "niega" in feedback(d), feedback(d)
    clic(d, f".conv-g button[data-d='{mala[0]}']")
    clic(d, f".conv-g button[data-d='{sol[1]}']")
    boton(d, "Presentar la lista").click()
    m = feedback(d)
    cerrar(d)
    return m


def s40(d):
    """VAR: sin decidir (falla), una jugada cambiada (falla) y las seis buenas."""
    abrir_carta(d, "40")
    boton(d, "Pitar").click()
    assert "Falta decidir" in feedback(d), feedback(d)
    fuera = I.VAR["fuera"]
    for i, f in enumerate(fuera):
        clic(d, f".var-f[data-i='{i}'] button[data-v='{'fuera' if not f else 'valida'}']")
    boton(d, "Pitar").click()
    assert "no está de acuerdo" in feedback(d), feedback(d)
    for i, f in enumerate(fuera):
        clic(d, f".var-f[data-i='{i}'] button[data-v='{'fuera' if f else 'valida'}']")
    boton(d, "Pitar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s48(d):
    """Pase: sin pases (falla), sin empezar en el portero (falla), por un pase cortado (falla) y la cadena buena."""
    abrir_carta(d, "48")
    et = ["P", "A", "B", "C", "D", "E", "Z"]
    boton(d, "Sacar de puerta").click()
    assert "Marcad primero" in feedback(d), feedback(d)
    clic(d, ".fu-btns button[data-k='A']")
    clic(d, ".fu-btns button[data-k='B']")
    boton(d, "Sacar de puerta").click()
    assert "empezar en el portero" in feedback(d), feedback(d)
    boton(d, "Empezar de nuevo").click()
    par = next((q for q in I.PASE["bloqueadas"] if 0 not in q), None)
    seq = [0, par[0], par[1]] if par else [0, I.PASE["bloqueadas"][0][1]]
    for k in seq:
        clic(d, f".fu-btns button[data-k='{et[k]}']")
    boton(d, "Sacar de puerta").click()
    assert "lo corta" in feedback(d), feedback(d)
    boton(d, "Empezar de nuevo").click()
    for k in I.PASE["camino"]:
        clic(d, f".fu-btns button[data-k='{et[k]}']")
    boton(d, "Sacar de puerta").click()
    m = feedback(d)
    cerrar(d)
    return m


def s52(d):
    """Alineación: sin colocar (falla), repetidos (falla), la voraz por puestos (falla) y el once bueno."""
    abrir_carta(d, "52")
    A = I.ALINEACION
    boton(d, "Presentar el once").click()
    assert "Falta poner" in feedback(d), feedback(d)
    for i in range(5):
        clic(d, f".ali-f button[data-i='{i}'][data-p='0']")
    boton(d, "Presentar el once").click()
    assert "mismo puesto" in feedback(d), feedback(d)
    # una asignación válida pero que no es la mejor: la de la permutación identidad, si no es la óptima
    ident = list(range(5))
    otra = ident if ident != A["solucion"] else [1, 2, 3, 4, 0]
    for i, p in enumerate(otra):
        clic(d, f".ali-f button[data-i='{i}'][data-p='{p}']")
    boton(d, "Presentar el once").click()
    assert "Suman" in feedback(d), feedback(d)
    for i, p in enumerate(A["solucion"]):
        clic(d, f".ali-f button[data-i='{i}'][data-p='{p}']")
    boton(d, "Presentar el once").click()
    m = feedback(d)
    cerrar(d)
    return m


def s46(d):
    """Penaltis: tirar siempre al lado donde el portero se lanza (la para y se reinicia) y luego tirar a un lado seguro cada vez."""
    abrir_carta(d, "46")
    P = I.PENALTIS
    ult = list(P["ultimos"])
    salto = P["regla"][f"{ult[-2]}{ult[-1]}"]
    clic(d, f".fu-btns button[data-l='{salto}']")
    assert "la para" in feedback(d), feedback(d)
    ult = list(P["ultimos"])
    for _ in range(P["tanda"]):
        salto = P["regla"][f"{ult[-2]}{ult[-1]}"]
        k = next(x for x in (0, 1, 2) if x != salto)
        clic(d, f".fu-btns button[data-l='{k}']")
        ult.append(k)
    m = feedback(d)
    cerrar(d)
    return m


def s51(d):
    """Cuadro: sin decidir (falla), todo al primer equipo (falla) y los resultados buenos."""
    abrir_carta(d, "51")
    bits = I.ELIMINATORIAS["bits"]
    boton(d, "Cantar el cuadro").click()
    assert "Faltan" in feedback(d), feedback(d)

    def jugar(bits):
        # cuartos 0-3, semifinales 4-5, final 6: se pulsa el botón de la posición bits[i] de cada partido
        for i in range(7):
            filas = d.find_elements(By.CSS_SELECTOR, f".eli-p[data-i='{i}'] button")
            d.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}))", filas[bits[i]])
            time.sleep(0.03)
    jugar([1 - b for b in bits])
    boton(d, "Cantar el cuadro").click()
    assert "no cuadra" in feedback(d), feedback(d)
    jugar(bits)
    boton(d, "Cantar el cuadro").click()
    m = feedback(d)
    cerrar(d)
    return m


def s64(d):
    """Calendario: un solo cruce (falla), cruces de la jornada 1 (falla) y los de la jornada buena."""
    abrir_carta(d, "64")
    C = I.CALENDARIO
    boton(d, "Sortear la jornada").click()
    assert "Faltan cruces" in feedback(d), feedback(d)
    for a, b in C["jornada1"]:
        clic(d, f".cal-g button[data-k='{a}']")
        clic(d, f".cal-g button[data-k='{b}']")
    boton(d, "Sortear la jornada").click()
    assert "no coinciden" in feedback(d), feedback(d)
    boton(d, "Empezar de nuevo").click()
    for a, b in C["solucion"]:
        clic(d, f".cal-g button[data-k='{a}']")
        clic(d, f".cal-g button[data-k='{b}']")
    boton(d, "Sortear la jornada").click()
    m = feedback(d)
    cerrar(d)
    return m


def s69(d):
    """Cambios: sin rellenar (falla), la alineación inicial (falla) y la final."""
    abrir_carta(d, "69")
    S = I.SUSTITUCIONES
    boton(d, "Presentar la alineación").click()
    assert "Falta algún puesto" in feedback(d), feedback(d)

    def poner(vals):
        for k, v in enumerate(vals):
            clic(d, f".sus-p button[data-p='{k + 1}']")
            clic(d, f".sus-d button[data-d='{v}']")
    poner(S["dorsales"])
    boton(d, "Presentar la alineación").click()
    assert "Esa no es" in feedback(d), feedback(d)
    poner(S["final"])
    boton(d, "Presentar la alineación").click()
    m = feedback(d)
    cerrar(d)
    return m


def s72(d):
    """Grada: fila vacía (falla), la fila de partida (falla) y la fila buena."""
    abrir_carta(d, "72")
    G = I.GRADA
    boton(d, "Comprobar la fila").click()
    assert "no cuadra" in feedback(d), feedback(d)
    for i, v in enumerate(G["inicio"]):
        if v:
            clic(d, f".gra-f button[data-i='{i}']")
    boton(d, "Comprobar la fila").click()
    assert "no cuadra" in feedback(d), feedback(d)
    boton(d, "Vaciar").click()
    for i, v in enumerate(G["final"]):
        if v:
            clic(d, f".gra-f button[data-i='{i}']")
    boton(d, "Comprobar la fila").click()
    m = feedback(d)
    cerrar(d)
    return m


def s85(d):
    """Aros: sin colocar (falla), todos a 1 (falla) y las cinco posiciones."""
    abrir_carta(d, "85")
    boton(d, "Abrir la Copa").click()
    assert "Falta colocar" in feedback(d), feedback(d)
    for i in range(5):
        clic(d, f".aro-n button[data-i='{i}'][data-n='1']")
    boton(d, "Abrir la Copa").click()
    assert "no cede" in feedback(d), feedback(d)
    for i, n in enumerate(I.FINAL_ARO):
        clic(d, f".aro-n button[data-i='{i}'][data-n='{n}']")
    boton(d, "Abrir la Copa").click()
    m = feedback(d)
    cerrar(d)
    return m


SOLVERS = {"14": s14, "20": s20, "40": s40, "48": s48, "52": s52, "46": s46, "51": s51, "64": s64, "69": s69, "72": s72, "85": s85}
REQUIERE = {"14": ["16"], "20": ["18", "19", "21"], "40": ["41", "43", "45"], "48": ["42", "49", "53"], "52": ["54", "55", "59"], "46": ["37", "39", "33"],
            "51": ["26", "61", "63"], "64": ["66", "67"], "69": ["70", "71"], "72": ["75", "79"], "85": ["86", "87"]}
