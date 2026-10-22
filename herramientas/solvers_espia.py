"""Solucionadores de los minijuegos de «Montecarlo, 1965: Operación Cristal» (60 cartas): juegan cada app por la interfaz real, primero una jugada mala
para comprobar el aviso y luego la buena. Las soluciones salen de instancias_espia.py."""
import sys, time
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from bot_core import *
import instancias_espia as I


def clic(d, css):
    """Clic por JS: los elementos pueden estar dentro de contenedores con overflow oculto."""
    d.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}))", d.find_element(By.CSS_SELECTOR, css))
    time.sleep(0.03)


def escribe(d, css, texto):
    d.execute_script("var e = document.querySelector(arguments[0]); e.value = arguments[1]; e.dispatchEvent(new Event('input'));", css, texto)


def poner(d, r, c, v):
    clic(d, f".es-cel[data-r='{r}'][data-c='{c}']")
    clic(d, f".es-nums button[data-n='{v}']")


def rellenar(d, g):
    for r, f in enumerate(g):
        for c, v in enumerate(f):
            poner(d, r, c, v)


def ajusta(d, nombre, objetivo):
    """Lleva un contador (+/−) hasta el valor pedido."""
    css = f".es-cont[data-nombre='{nombre}']"
    for _ in range(80):
        v = int(d.find_element(By.CSS_SELECTOR, css).get_attribute("data-v"))
        if v == objetivo:
            return
        clic(d, css + (" button[data-d='1']" if v < objetivo else " button[data-d='-1']"))
    raise Fallo("no llego a " + str(objetivo) + " en " + nombre)


def s14(d):
    """Nota: demasiado corta (falla), de la longitud justa pero equivocada (falla) y el mensaje."""
    abrir_carta(d, "14")
    boton(d, "Entregar el mensaje").click()
    assert "Todavía no" in feedback(d), feedback(d)
    escribe(d, ".es-in", "AGENTE")
    boton(d, "Entregar el mensaje").click()
    assert "letras" in feedback(d), feedback(d)
    n = len("".join(I.CRIPTOGRAMA["claro"].split()))
    escribe(d, ".es-in", "A" * n)
    boton(d, "Entregar el mensaje").click()
    assert "en su sitio" in feedback(d), feedback(d)
    escribe(d, ".es-in", I.CRIPTOGRAMA["claro"].lower())
    boton(d, "Entregar el mensaje").click()
    m = feedback(d)
    cerrar(d)
    return m


def _caminos_validos():
    """Todos los caminos simples A→I que no cruzan glorietas cortadas, con su coste."""
    r = I.RUTA
    adj = {k: [] for k in range(len(r["nodos"]))}
    for a, b, w in r["aristas"]:
        adj[a].append((b, w))
        adj[b].append((a, w))
    res = []

    def rec(u, vis, coste):
        if u == len(r["nodos"]) - 1:
            res.append((coste, list(vis)))
            return
        for v, w in adj[u]:
            if v not in vis and v not in r["cerrados"]:
                vis.append(v)
                rec(v, vis, coste + w)
                vis.pop()
    rec(0, [0], 0)
    return sorted(res)


def ruta(d, camino):
    for k in camino:
        clic(d, f".es-nodo[data-n='{I.RUTA['nodos'][k]}']")


def s20(d):
    """Ruta: vacía (falla), sin empezar en la A (falla), por una glorieta cortada (falla), un camino más lento (falla) y el mejor."""
    abrir_carta(d, "20")
    boton(d, "Salir de caza").click()
    assert "Marcad primero" in feedback(d), feedback(d)
    ruta(d, [1, 2])
    boton(d, "Salir de caza").click()
    assert "empezar en el Casino" in feedback(d), feedback(d)
    boton(d, "Empezar de nuevo").click()
    ruta(d, [0, 1, 2])
    boton(d, "Salir de caza").click()
    assert "cortada" in feedback(d), feedback(d)
    boton(d, "Empezar de nuevo").click()
    lento = next(c for coste, c in reversed(_caminos_validos()) if coste != I.RUTA["mejor"])
    ruta(d, lento)
    boton(d, "Salir de caza").click()
    assert "más rápido" in feedback(d), feedback(d)
    boton(d, "Empezar de nuevo").click()
    ruta(d, I.RUTA["camino"])
    boton(d, "Salir de caza").click()
    m = feedback(d)
    cerrar(d)
    return m


def s40(d):
    """Skyline: sin llenar (falla), todo unos (falla), un latino cíclico que no cuadra (falla) y el skyline bueno."""
    abrir_carta(d, "40")
    n = I.RASCACIELOS["n"]
    boton(d, "Comprobar").click()
    assert "sin torre" in feedback(d), feedback(d)
    rellenar(d, [[1] * n for _ in range(n)])
    boton(d, "Comprobar").click()
    assert "misma altura" in feedback(d), feedback(d)
    rellenar(d, [[(i + j) % n + 1 for j in range(n)] for i in range(n)])
    boton(d, "Comprobar").click()
    assert "no cuadra" in feedback(d), feedback(d)
    rellenar(d, I.RASCACIELOS["solucion"])
    boton(d, "Comprobar").click()
    m = feedback(d)
    cerrar(d)
    return m


def s48(d):
    """Libro: nada (falla), un mensaje equivocado (falla) y el bueno."""
    abrir_carta(d, "48")
    boton(d, "Entregar el mensaje").click()
    assert "Todavía no" in feedback(d), feedback(d)
    escribe(d, ".es-in", "EL BOTIN ESTA EN LA CAJA")
    boton(d, "Entregar el mensaje").click()
    assert "No tiene sentido" in feedback(d), feedback(d)
    escribe(d, ".es-in", I.LIBRO["claro"].lower())
    boton(d, "Entregar el mensaje").click()
    m = feedback(d)
    cerrar(d)
    return m


def s52(d):
    """Caja: sin llenar (falla), todo unos (falla), un latino cíclico que no cuadra (falla) y la caja buena."""
    abrir_carta(d, "52")
    n = I.KENKEN["n"]
    boton(d, "Probar la combinación").click()
    assert "sin cifra" in feedback(d), feedback(d)
    rellenar(d, [[1] * n for _ in range(n)])
    boton(d, "Probar la combinación").click()
    assert "repetida" in feedback(d), feedback(d)
    rellenar(d, [[(i + j) % n + 1 for j in range(n)] for i in range(n)])
    boton(d, "Probar la combinación").click()
    assert "no cede" in feedback(d), feedback(d)
    rellenar(d, I.KENKEN["solucion"])
    boton(d, "Probar la combinación").click()
    m = feedback(d)
    cerrar(d)
    return m


def s46(d):
    """Conteo: cuenta del corte mala (falla), cuenta final mala (falla) y las dos buenas."""
    abrir_carta(d, "46")
    ajusta(d, "corte", I.CONTEO["cuenta_corte"] + 1)
    boton(d, "Cantar la cuenta").click()
    assert "en el corte" in feedback(d), feedback(d)
    ajusta(d, "corte", I.CONTEO["cuenta_corte"])
    ajusta(d, "final", I.CONTEO["cuenta_final"] + 1)
    boton(d, "Cantar la cuenta").click()
    assert "del final no cuadra" in feedback(d), feedback(d)
    ajusta(d, "final", I.CONTEO["cuenta_final"])
    boton(d, "Cantar la cuenta").click()
    m = feedback(d)
    cerrar(d)
    return m


def s51(d):
    """Pasaportes: sin dígitos (falla), todos mal (falla) y los tres buenos."""
    abrir_carta(d, "51")
    boton(d, "Sellar los pasaportes").click()
    assert "Falta" in feedback(d), feedback(d)

    def digitos(vals):
        for i, v in enumerate(vals):
            clic(d, f".pas-f[data-i='{i}']")
            clic(d, f".es-nums button[data-n='{v}']")
    digitos([(x + 1) % 10 for x in I.PASAPORTES["digitos"]])
    boton(d, "Sellar los pasaportes").click()
    assert "no coinciden" in feedback(d), feedback(d)
    digitos(I.PASAPORTES["digitos"])
    boton(d, "Sellar los pasaportes").click()
    m = feedback(d)
    cerrar(d)
    return m


def s64(d):
    """Husos: el día malo (falla), la hora mala (falla) y la llegada buena."""
    abrir_carta(d, "64")
    L = I.HUSOS["llegada"]
    ajusta(d, "dia", L["dia"] + 1)
    boton(d, "Abrir la caja de seguridad").click()
    assert "día no cuadra" in feedback(d), feedback(d)
    ajusta(d, "dia", L["dia"])
    boton(d, "Abrir la caja de seguridad").click()
    assert "hora de aterrizaje" in feedback(d), feedback(d)
    ajusta(d, "hora", L["hora"])
    ajusta(d, "min", L["min"])
    boton(d, "Abrir la caja de seguridad").click()
    m = feedback(d)
    cerrar(d)
    return m


def s69(d):
    """Cables: sin elegir (falla), un cable malo en una carga (falla y reinicia) y los cuatro cortes buenos."""
    abrir_carta(d, "69")
    boton(d, "Cortar los cables").click()
    assert "Falta elegir" in feedback(d), feedback(d)
    cs = I.CABLES["cargas"]
    for k, c in enumerate(cs):
        clic(d, f".cab-w[data-k='{k}'][data-i='{(c['corta'] + 1) % 6}']")
    boton(d, "Cortar los cables").click()
    assert "no se desactiva" in feedback(d), feedback(d)
    for k, c in enumerate(cs):
        clic(d, f".cab-w[data-k='{k}'][data-i='{c['corta']}']")
    boton(d, "Cortar los cables").click()
    m = feedback(d)
    cerrar(d)
    return m


def s72(d):
    """Ruleta: el banco de partida (falla) y el banco final."""
    abrir_carta(d, "72")
    boton(d, "Contar el banco").click()
    assert "no sale" in feedback(d), feedback(d)
    ajusta(d, "fichas", I.RULETA["final"])
    boton(d, "Contar el banco").click()
    m = feedback(d)
    cerrar(d)
    return m


def s85(d):
    """Teléfono: nada (falla), una letra mala (falla) y la clave por multitoque."""
    abrir_carta(d, "85")
    boton(d, "Marcar").click()
    assert "Todavía no" in feedback(d), feedback(d)
    clic(d, ".tel-teclas button[data-k='2']")
    boton(d, "Marcar").click()
    assert "tono agudo" in feedback(d), feedback(d)
    boton(d, "Borrar una letra").click()
    for k in I.ORDEN:
        for ch in I.PULSA[k]:
            clic(d, f".tel-teclas button[data-k='{ch}']")
        boton(d, "Pausa").click()
    boton(d, "Marcar").click()
    m = feedback(d)
    cerrar(d)
    return m


SOLVERS = {"14": s14, "20": s20, "40": s40, "48": s48, "52": s52, "46": s46, "51": s51, "64": s64, "69": s69, "72": s72, "85": s85}
REQUIERE = {"14": ["16"], "20": ["18", "19", "21"], "40": ["41", "43", "45"], "48": ["42", "49", "53"], "52": ["54", "55", "59"], "46": ["37", "39", "33"],
            "51": ["26", "61", "63"], "64": ["66", "67"], "69": ["70", "71"], "72": ["75", "79"], "85": ["86", "87"]}
