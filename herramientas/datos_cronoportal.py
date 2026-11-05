"""El primer salto — el nivel de prueba (gratis para todos) de Aventuras C&A: 17 cartas, 3 puzles muy sencillos y las reglas del juego explicadas con cada carta.

Cristina y Alberto acaban de montar el Cronoportal en el salón de su casa; falta el cristal de energía, que está en una vitrina. Al encenderlo por primera
vez el portal los lleva al Umbral del Tiempo, un salón de relojes flotantes: su primer salto a otro mundo. Un panel de vuelta los devuelve a casa.
Reglas que se aprenden: leer una carta (Coged y Descartad), el botón Acción con el número de una carta verde, el botón Pista, unir las dos mitades de una
lámina (mosaico), combinar dos cartas sumando sus números y apuntar las cifras que dejan los puzles."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ampliacion as _amp  # noqa: E402
import instancias_cronoportal as I  # noqa: E402

INST = I.INST
CE, MA, ME = INST["cerradura"], INST["mapa"], INST["meta"]

ESTILO = ("Ilustración de animación 3D familiar y luminosa, como una película de aventuras de ciencia ficción amable: colores vivos y limpios, latón pulido, cristal azul brillante, "
          "relojes y engranajes, luz cálida de tarde en el salón y destellos azules y dorados del portal. Formato vertical 2:3. Sin texto, letras ni números legibles en la imagen. "
          "Deja libre de detalles importantes la esquina superior izquierda y el 18 % inferior de la imagen. "
          "Los personajes tienen siempre expresiones distintas y expresivas, adecuadas a la escena (nunca la misma cara en dos imágenes).")

PERSONAJES = {
    "Cristina": "Cristina, mujer de 26 años, profesora, pelo rubio y rizado, ojos azules. Viste vaqueros, zapatillas, una camiseta clara y una chaqueta ligera, y lleva el pelo recogido con un lápiz.",
    "Alberto": "Alberto, hombre de 27 años, informático, pelo moreno corto, barba cuidada, ojos marrones. Viste vaqueros, zapatillas, una sudadera con capucha y unas gafas de protección subidas en la frente.",
}

HOJA = ("Crea una hoja de personajes (character sheet) con las dos personas de la foto adjunta, de cuerpo entero y de frente, sobre fondo claro y neutro. "
        "Mantén su parecido real con la foto (cara, pelo, barba, ojos). " + " ".join(PERSONAJES.values()) + " Estilo: " + ESTILO)

FOTO = ("Antes de nada, adjunta a ChatGPT una foto de Cristina y Alberto juntos (o una de cada uno, con la cara bien visible). "
        "Pídele que mantenga el parecido real en la cara y que los vista con la ropa cómoda de este juego.")

VIDEO = ("Crea un vídeo vertical 9:16 de 15 segundos, con estilo de animación 3D familiar y luminosa, sin ningún texto, letra ni subtítulo en pantalla. "
         "Escena 1 (0-4 s): en el salón de una casa actual, sobre una mesa, un aparato de latón y cristal con un anillo central apagado; Cristina (mujer de 26 años, rubia de pelo rizado, ojos azules) "
         "y Alberto (hombre de 27 años, moreno con barba, ojos marrones, gafas de protección en la frente) lo miran con una sonrisa nerviosa. "
         "Escena 2 (4-8 s): colocan un cristal azul en el pecho del aparato y el anillo se enciende con un arco de luz azul y dorada. "
         "Escena 3 (8-12 s): el portal los absorbe girando en un túnel de luz y caen en un salón enorme lleno de relojes flotantes. "
         "Escena 4 (12-15 s): primer plano de los dos mirando boquiabiertos los relojes; fundido a negro. "
         "Sonido: zumbido eléctrico creciente, campanadas de relojes y un destello final, sin voz de narrador.")

SIN_GENTE = "Sin ninguna persona en la imagen. "
MOSAICOS = {"plano": dict(filas=2, cols=1, cartas=["19", "21"], titulo="El plano del Umbral")}
POS = {(2, 1): ["mitad de arriba", "mitad de abajo"]}


def codigo(que):
    return f"Carta dibujada por código (herramientas/cronoportal.py; no se pide a ChatGPT): {que}."


def pieza(carta, mosaico, que, pistas):
    m = MOSAICOS[mosaico]
    i = m["cartas"].index(carta)
    pos = POS[(m["filas"], m["cols"])][i]
    return dict(titulo=f"Carta {carta} — {m['titulo']} ({pos})", tipo="gris", mosaico=dict(id=mosaico, filas=m["filas"], cols=m["cols"], fila=i, col=0),
                descripcion=[que], pistas=pistas, arte=codigo(f"{pos} de «{m['titulo']}»"))


def gris(carta, titulo, que, pistas):
    return dict(titulo=f"Carta {carta} — {titulo}", tipo="gris", descripcion=[que], pistas=pistas, arte=codigo(titulo))


def app(carta, titulo, que, sale, pistas, arte):
    return dict(titulo=f"Carta {carta} — {titulo}", tipo="verde", descripcion=[que, f"Al resolverlo, coged la carta {sale}."], pistas=pistas, arte=arte)


def _lista(xs):
    xs = [str(x) for x in xs]
    return ", ".join(xs[:-1]) + " y " + xs[-1] if len(xs) > 1 else xs[0]


def escena(carta, titulo, coge, descarta, texto, pistas, arte):
    partes = []
    if coge:
        partes.append("Coged las cartas " + _lista(coge) + "." if len(coge) > 1 else f"Coged la carta {coge[0]}.")
    if descarta:
        partes.append("Descartad " + ("las cartas " + _lista(descarta) if len(descarta) > 1 else f"la carta {descarta[0]}") + ".")
    lineas = [texto, " ".join(partes)]
    c = dict(titulo=f"Carta {carta} — {titulo}", tipo="gris", descripcion=lineas, pistas=pistas + [lineas[-1]], arte=arte)
    if coge:
        c["coge"] = coge
    if descarta:
        c["descarta"] = descarta
    return c


def combinable(carta, titulo, color, con, da, que, arte):
    return dict(titulo=f"Carta {carta} — {titulo}", tipo=color, combina=[con, da],
                descripcion=[que, f"Combinadla con la carta {con}: sumad sus números ({carta} + {con} = {da}) y coged la carta {da}."],
                pistas=[que.split(".")[0] + ".", f"Se combina con la carta {con}.", f"{carta} + {con} = {da}."], arte=arte)


J = {
    "P": escena("P", "El primer salto", [10, 12], [],
                "BIENVENIDOS AL NIVEL DE PRUEBA. Cada carta se lee entera y dice qué hacer. REGLA 1: donde pone «Coged», se ponen esas cartas en la mesa; donde pone «Descartad», se quitan. "
                "Aquí empieza todo: Cristina y Alberto han montado por fin el Cronoportal en el salón de su casa. Es una máquina de latón y cristal con un anillo central, pero está apagada: le falta el cristal de energía.",
                ["Leed la carta con calma: dice qué hacer.", "Coged las cartas 10 y 12: son las que dice abajo."],
                "El salón de una casa actual, de tarde, con una mesa grande en el centro y sobre ella un aparato de latón y cristal con un anillo central apagado (el Cronoportal) rodeado de herramientas y papeles. "
                "Cristina, con el pelo recogido con un lápiz, lo mira con los brazos en jarras y una sonrisa de orgullo, y Alberto, con las gafas de protección en la frente, ajusta un tornillo con la lengua entre los dientes."),
    "10": escena("10", "El taller del salón", [14, 16, 21, 22], ["P"],
                 "La mesa del salón es ahora el taller. REGLA 2: las cartas con el borde VERDE no se resuelven en el papel, sino en el móvil: se pulsa el botón Acción y se escribe el número de la carta. "
                 "Delante tenéis la vitrina del cristal, cerrada con un candado de tres cifras (carta 14), y la pizarra de Alberto con lo que sobró del montaje (carta 16). "
                 "En el suelo hay media lámina de un plano (carta 21) y la mitad de un cristal (carta 22).",
                 ["La carta 14 tiene borde verde: es de app. Pulsad Acción y escribid 14.", "El candado de la vitrina pide una cifra por cada color de engranaje de la pizarra.", "Rojo, azul y amarillo, en ese orden: contad cuántos hay de cada uno."],
                 "La mesa del salón convertida en taller, con una vitrina de cristal cerrada con un candado, una pizarra verde llena de engranajes de colores apoyada en la pared y un portal de latón al fondo. "
                 "Cristina se inclina hacia la pizarra con el ceño fruncido de concentración y Alberto levanta una mitad de cristal azul a la luz con los ojos muy abiertos de asombro."),
    "12": gris("12", "Cronoportal sin cristal", "El Cronoportal: una máquina de latón y cristal con un anillo central apagado y un hueco vacío en el pecho, donde irá el cristal de energía.",
               ["Es la máquina que han construido.", "Está apagada.", "Le falta el cristal de energía."]),
    "14": app("14", "La vitrina del cristal", "Es un juego de la app: la vitrina que guarda el cristal tiene un candado de tres cifras. La pizarra de Alberto da el código.", 24,
              ["Es una carta verde: se abre con el botón Acción de la app.", "La pizarra es la carta 16. Contad los engranajes de cada color.", f"Hay {CE['cuentas']['rojo']} rojos, {CE['cuentas']['azul']} azules y {CE['cuentas']['amarillo']} amarillos: el código es {CE['codigo']}."],
              SIN_GENTE + "Una vitrina de cristal y latón con un candado de tres ruedas de números, y dentro una pequeña almohadilla de terciopelo azul vacía con la forma de un cristal partido, sobre una mesa de taller."),
    "16": gris("16", "La pizarra de Alberto", "La pizarra verde de Alberto con engranajes rojos, azules y amarillos que sobraron al montar el portal.", ["Es la pizarra de la carta 14.", "Hay engranajes de tres colores.", "Contadlos por color."]),
    "18": gris("18", "La nota de Cristina", "Una nota de Cristina pegada en el plano, que explica cómo se lee.", ["Es la nota del plano de la carta 20.", "Habla de un camino y de cuatro símbolos.", "El plano está en las cartas 19 y 21."]),
    "19": pieza("19", "plano", "REGLA 3: algunas cartas son la mitad de una lámina. Se juntan: esta es la mitad de arriba de un plano; la de abajo es la carta 21.", ["Es la mitad de una lámina: juntadla con la carta 21.", "Colocad la 19 arriba y la 21 abajo.", "El camino cruza de una hoja a la otra."]),
    "21": pieza("21", "plano", "Media lámina de un plano: la mitad de abajo. La de arriba es la carta 19.", ["Es la mitad de una lámina: juntadla con la carta 19.", "Colocad la 19 arriba y la 21 abajo.", "El camino cruza de una hoja a la otra."]),
    "20": app("20", "Calibrar el portal", "Es un juego de la app: el portal se calibra tocando, en orden, los símbolos por los que pasa el camino del plano.", 28,
              ["El plano son las cartas 19 y 21 juntas, y la nota de Cristina es la 18.", "Seguid el camino desde la entrada y apuntad los símbolos de las cuatro casillas de en medio.", f"Los símbolos son: {', '.join(MA['solucion'])}."],
              SIN_GENTE + "Un panel de calibración del Cronoportal con seis botones redondos de latón con símbolos grabados (sol, luna, estrella, llave, reloj y flor) bajo un cristal con un anillo luminoso."),
    "22": combinable("22", "Mitad del cristal", "azul", 35, 57, "La mitad izquierda de un cristal de energía azul, cortada limpiamente por el centro.",
                     SIN_GENTE + "La mitad izquierda de un cristal azul brillante de energía, cortada limpiamente por el centro, sobre una almohadilla de terciopelo."),
    "24": escena("24", "La vitrina se abre", [18, 19, 20], [10, 14, 16],
                 "El candado cede y dentro de la vitrina hay una nota de Cristina (carta 18), la mitad de arriba de un plano (carta 19) y un calibrador del portal (carta 20).",
                 ["Mirad lo que había dentro de la vitrina.", "Hay una carta nueva con borde verde: la 20."],
                 "El interior de una vitrina abierta, con una mitad de cristal azul en un cojín, un plano doblado y un calibrador de latón con botones de símbolos. "
                 "Cristina saca el plano con cuidado y los ojos brillantes de emoción, y Alberto abre los brazos con una gran sonrisa de victoria."),
    "28": escena("28", "El portal se calibra", [86, 35], [18, 19, 20, 21, 24],
                 "Con los símbolos en orden, el anillo del Cronoportal gira y se llena de luz azul. Sobre la mesa, Alberto ha escrito la nota del panel de vuelta (carta 86) y, con la luz del anillo, ha aparecido la otra mitad del cristal (carta 35). "
                 "REGLA 4: las cartas de color AZUL y ROJO se combinan: se suman sus números y se coge la carta que sale; la 35 se combina con la 22. "
                 "REGLA 5: los puzles dejan cifras («Cifra de…»). Apuntadlas, porque las necesitaréis más tarde.",
                 ["Mirad la nota de Alberto.", "Una carta roja y una azul se combinan sumando sus números."],
                 "El Cronoportal con el anillo central girando y lleno de luz azul, rodeado de papeles y herramientas sobre una mesa de taller. "
                 "Alberto escribe una nota con el lápiz en la boca y la ceja levantada de duda, y Cristina, con las manos en las mejillas, mira el anillo con una sonrisa de asombro."),
    "35": combinable("35", "La otra mitad del cristal", "roja", 22, 57, "La mitad derecha del cristal de energía, que estaba en la vitrina.",
                     SIN_GENTE + "La mitad derecha de un cristal azul brillante de energía, cortada limpiamente por el centro, sobre un cojín de terciopelo dentro de una vitrina."),
    "57": escena("57", "¡El primer salto!", [85], [22, 35, 12, 28],
                 "Las dos mitades encajan en una sola luz: el cristal de energía. Cristina lo coloca en el pecho del Cronoportal y la máquina ruge. El anillo se abre y los absorbe en un túnel de destellos azules y dorados: "
                 "caen en el Umbral del Tiempo, un salón inmenso de relojes que flotan, giran y suenan. Es el primer salto de su vida. Para volver hay un panel con dos cifras (carta 85). "
                 "REGLA 6: el botón Pista de la app da ayuda si os atascáis; empieza suave y cada vez dice más.",
                 ["Esta carta dice que cojáis la 85.", "El panel de vuelta se abre con el botón Acción."],
                 "Dentro del Umbral del Tiempo, un salón inmenso y luminoso lleno de relojes de todos los tamaños que flotan en el aire y giran, con un panel de latón con ruedas de cifras en primer plano y, al fondo, un anillo de luz azul. "
                 "Cristina, con los brazos abiertos y una gran sonrisa de maravilla, gira sobre sí misma, y Alberto, boquiabierto y con las gafas de protección resbalando por la frente, mira hacia arriba."),
    "85": app("85", "El panel de vuelta", "Es un juego de la app: un panel con un teclado en el que hay que marcar dos cifras para volver a casa.", 99,
              ["Las dos cifras las dejaron el plano y la vitrina.", "El orden lo dice la carta 86.", f"Primero la del camino ({MA['cifra']}) y luego la del candado ({CE['cifra']}): {ME['codigo']}."],
              SIN_GENTE + "Un panel de latón de una máquina del tiempo con un teclado numérico de teclas redondas, un visor ámbar y dos ruedas de cifras, bajo relojes flotantes."),
    "86": gris("86", "El orden del panel", "Una nota de Alberto con el orden en que se marcan las dos cifras del panel de vuelta.", ["Es el orden de las cifras de la carta 85.", "Primero una cifra, luego la otra.", "Cada una la dejó un puzle."]),
    "99": escena("99", "De vuelta a casa (FIN)", [], [57, 85, 86],
                 "El panel acepta las dos cifras y el anillo se abre otra vez. Cristina y Alberto salen disparados del Umbral y aterrizan, riendo, en el sofá de su salón, otra vez en casa y de su tamaño. "
                 "Alberto mira el aparato todavía humeante: «Funciona. Funciona de verdad». Cristina ya está sacando un mapa: «¿Adónde vamos mañana?». Habéis aprendido las seis reglas del juego: ya estáis listos para el siguiente salto. FIN.",
                 [],
                 "La escena ocurre DENTRO del salón de su casa, de tarde (sofá, estanterías con libros, plantas, una lámpara encendida y luz cálida por la ventana): acaban de VOLVER a casa. "
                 "Cristina y Alberto salen de un portal circular de luz azul y dorada que se abre detrás de ellos y se está cerrando; a través del portal todavía se ven relojes flotantes. "
                 "Cristina ríe a carcajadas con los brazos en alto y Alberto, con las gafas de protección torcidas, se deja caer en el sofá con cara de euforia. "
                 "Están de cara a nosotros, aterrizando en el salón y alejándose del portal, que queda a su espalda; no entran en el portal ni salen de casa: están llegando."),
}

META = dict(juego="El primer salto", estilo=ESTILO, personajes=PERSONAJES, hoja=HOJA, foto=FOTO, video=VIDEO,
            mosaicos={k: dict(filas=m["filas"], cols=m["cols"], cartas=m["cartas"], titulo=m["titulo"]) for k, m in MOSAICOS.items()})

SPEC = dict(final="99", needs={"24": ["14", "16"], "28": ["20", "18", "19", "21"], "57": ["22", "35", "12", "28"], "99": ["85", "86", "57"]}, eventos={})

PARA_QUE = {k: c["titulo"].split("— ", 1)[1] for k, c in J.items()}

_T = [
    ("leer", "P", "El primer salto", "Pon el Modo PC (solo la P en la mesa) y en el móvil pulsa Empezar. Lee la carta P: coge la 10 y la 12."),
    ("leer", "10", "El taller del salón", "Lee la carta 10. Descarta la P y coge 14, 16, 21 y 22."),
    ("app", "14", "La vitrina del cristal", f"En el móvil: Acción, 14. Cuenta los engranajes de la pizarra (16): rojos, azules y amarillos; el código es {CE['codigo']}. El mensaje te dice que cojas la 24. Apunta la cifra de la vitrina: {CE['cifra']}.", "carta 24"),
    ("leer", "24", "La vitrina se abre", "Lee la carta 24. Descarta 10, 14 y 16 y coge 18, 19 y 20. Junta el plano: 19 arriba y 21 abajo."),
    ("app", "20", "Calibrar el portal", f"En el móvil: Acción, 20. Sigue el camino del plano (19 y 21): toca, en orden, {', '.join(MA['solucion'])}. El mensaje te dice que cojas la 28. Apunta la cifra del plano: {MA['cifra']}.", "carta 28"),
    ("leer", "28", "El portal se calibra", "Lee la carta 28. Descarta 18, 19, 20, 21 y 24 y coge 86 y 35."),
    ("combinar", "22", "35", "El cristal", "La mitad del cristal (22) y la otra mitad (35) son combinables: 22 + 35 = 57. Coge la 57."),
    ("leer", "57", "¡El primer salto!", "Lee la carta 57. Descarta 22, 35, 12 y 28 y coge la 85."),
    ("app", "85", "El panel de vuelta", f"En el móvil: Acción, 85. Con el orden de la carta 86 (primero el plano, luego la vitrina), marca {ME['codigo']}. El mensaje te dice que cojas la 99.", "carta 99"),
    ("leer", "99", "Final", "Lee la carta 99. Descarta 57, 85 y 86. En la mesa solo queda la 99. ¡Fin!"),
]
PASOS = []
for _p in _T:
    if _p[0] == "combinar":
        PASOS.append(dict(t=_p[3], que=_p[4], acciones=[("combinar", _p[1], _p[2])]))
    elif _p[0] == "app":
        PASOS.append(dict(t=_p[2], que=_p[3], acciones=[("app", _p[1], _p[4])]))
    else:
        PASOS.append(dict(t=_p[2], que=_p[3], acciones=[("leer", _p[1])]))
_amp.recalcular_mesas(PASOS, J)
