"""Marte, 2157: Cúpula Aurora — versión de 60 cartas (21 oct 2026), mucho más difícil y variada.

Once puzles de tipos que no salen en ningún otro juego de la serie, con las pistas dibujadas o en acertijo (ninguna carta explica cómo se
resuelve su puzle): la ventana de comunicaciones de tres satélites, el «juego de la vida» del invernadero, el cableado de una placa
(Numberlink), un campo de rocas (buscaminas), el equilibrio del brazo de una antena, una cuenta de cifras, el circuito del reactor
(Slitherlink), el programa de un rover con bucles, los paneles de refrigeración (Lights Out), una sopa de letras con clave y la consola
final con los datos de la misión de cuatro puzles. Solo 15 cartas tienen a Cristina y Alberto (escenas); el resto son objetos y pistas
sin personas. Las cartas-pista las dibuja herramientas/marte.py (instancias_marte.py)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ampliacion as _amp  # noqa: E402
import instancias_marte as I  # noqa: E402

ESTILO = ("Ilustración digital de ciencia ficción realista con estética de película, paleta de óxido anaranjado, grises metálicos, "
          "destellos de cian y luces de emergencia rojas, formato vertical 2:3. Sin texto, letras ni números en la imagen. "
          "Deja libre de detalles importantes la esquina superior izquierda y el 18 % inferior de la imagen.")

PERSONAJES = {
    "Cristina": "Cristina, mujer de 26 años, profesora, pelo rubio y rizado, ojos azules. Lleva ropa de colonia marciana: mono técnico ajustado blanco con detalles naranjas, parches de la colonia Aurora, botas de suela gruesa y guantes cortos (el casco solo cuando la escena lo pida).",
    "Alberto": "Alberto, hombre de 27 años, informático, pelo moreno corto, barba cuidada, ojos marrones. Lleva ropa de colonia marciana: mono técnico gris oscuro con detalles naranjas, parches de la colonia Aurora, botas de suela gruesa y una mochila de herramientas (el casco solo cuando la escena lo pida)."
}

HOJA = ("Crea una hoja de personajes (character sheet) con las dos personas de la foto adjunta, de cuerpo entero y de frente, sobre fondo claro y neutro. "
        "Mantén su parecido real con la foto (cara, pelo, barba, ojos). "
        "Cristina: mujer de 26 años, profesora, pelo rubio y rizado, ojos azules, mono técnico ajustado blanco con detalles naranjas y botas de colonia marciana. "
        "Alberto: hombre de 27 años, informático, pelo moreno corto, barba cuidada, ojos marrones, mono técnico gris oscuro con detalles naranjas, botas de colonia marciana y mochila de herramientas. "
        "Estilo: " + ESTILO)

FOTO = ("Antes de nada, adjunta a ChatGPT una foto de Cristina y Alberto juntos (o una de cada uno, con la cara bien visible). "
        "Pídele que mantenga el parecido real, pero con el estilo de ilustración de este juego.")

VIDEO = ("Crea un vídeo vertical 9:16 de 15 segundos, con estética de película de ciencia ficción realista, colores de óxido anaranjado y destellos cian. Sin ningún texto, letra ni subtítulo en pantalla. "
         "Escena 1 (0-4 s): en el salón de una casa actual, Cristina (mujer de 26 años, rubia de pelo rizado, ojos azules) y Alberto (hombre de 27 años, moreno con barba, ojos marrones) rodean un aparato de latón y cristal con un anillo central: el Cronoportal. Alberto teclea en el aparato y Cristina sonríe. "
         "Escena 2 (4-8 s): el anillo se enciende con un arco de luz azul, el salón se deforma y los dos son absorbidos por un túnel de luz. "
         "Escena 3 (8-12 s): caen en un hangar oscuro de una colonia en Marte, con luces de emergencia rojas parpadeando y polvo rojizo flotando; por una ventana se ve una tormenta de polvo; el aparato humea y se apaga. "
         "Escena 4 (12-15 s): primer plano de Cristina y Alberto, asombrados, levantándose; fundido a negro. "
         "Sonido: zumbido eléctrico creciente, silbido del portal, golpe sordo al aterrizar, alarma lejana y viento marciano, música de ciencia ficción tensa, sin voz de narrador.")

ESTILO += " Los personajes tienen siempre expresiones distintas y expresivas, adecuadas a la escena (nunca la misma cara en dos imágenes)."
SIN_GENTE = "Sin ninguna persona en la imagen. "
DOCTORA = "la doctora Reyes, botánica y jefa de la colonia, de unos cincuenta años, piel morena curtida, pelo corto y canoso, mono técnico verde con parches de la colonia Aurora y una pequeña tomatera sujeta a la mochila"

MOSAICOS = {
    "invernadero": dict(filas=2, cols=1, cartas=["19", "21"], titulo="El invernadero"),
    "cableado": dict(filas=1, cols=2, cartas=["41", "43"], titulo="La placa de bornes"),
    "rocas": dict(filas=1, cols=2, cartas=["42", "49"], titulo="El radar del campo de rocas"),
    "reactor": dict(filas=1, cols=2, cartas=["61", "63"], titulo="El esquema del reactor"),
    "paneles": dict(filas=2, cols=1, cartas=["66", "67"], titulo="Los paneles de refrigeración"),
    "sopa": dict(filas=1, cols=2, cartas=["75", "79"], titulo="La base de datos de la colonia"),
}
POS = {(2, 1): ["mitad de arriba", "mitad de abajo"], (1, 2): ["mitad izquierda", "mitad derecha"]}
_COL = "ABCDEFGH"
_c = lambda x, y: f"{_COL[x]}{y + 1}"


def _ciclo_anillo():
    ady = {}
    for t, x, y in I.ANILLO["solucion"]:
        a, b = ((x, y), (x + 1, y)) if t == "h" else ((x, y), (x, y + 1))
        ady.setdefault(a, []).append(b)
        ady.setdefault(b, []).append(a)
    ini = min(ady)
    ruta, prev, cur = [ini], None, ini
    while True:
        sig = next(q for q in ady[cur] if q != prev) if prev is not None else ady[cur][0]
        if sig == ini:
            break
        ruta.append(sig)
        prev, cur = cur, sig
    return ruta


_S_SAT = f"dentro de {I.SATELITES['solucion']} horas"
_S_VIDA = ", ".join(_c(x, y) for y, f in enumerate(I.VIDA["solucion"]) for x, v in enumerate(f) if v)
_S_CAB = " / ".join(f"fila {y + 1}: " + " ".join(str(c + 1) for c in f) for y, f in enumerate(I.CABLEADO["solucion"]))
_S_ROC = ", ".join(_c(x, y) for x, y in I.ROCAS["solucion"])
_FORMA = ["el círculo", "el cuadrado", "el triángulo"]
_S_BRA = "; ".join(f"{_FORMA[k]} (pesa {w}) en la marca {'izquierda' if p < 0 else 'derecha'} {abs(p)}" for k, (w, p) in enumerate(zip(I.BALANCIN["libres"], I.BALANCIN["solucion"])))
_S_CUE = ", ".join(f"{a} {op} {b} = {r}" for a, op, b, r in I.solucion_cifras(I.CIFRAS["numeros"], I.CIFRAS["objetivo"]))
_S_ANI = " → ".join(_c(x, y) for x, y in _ciclo_anillo())
_S_PRO = "repetir 3 veces: avanzar, girar a la izquierda, avanzar, girar a la derecha, avanzar"
_S_PAN = ", ".join(_c(x, y) for x, y in I.PANELES["toques"])
_S_SOP = I.SOPA["secreta"]
_S_COD = ", ".join(str(x) for x in I.CODIGO)
_PAL = ", ".join(I.SOPA["palabras"])


def codigo(que):
    return f"Carta dibujada por código (herramientas/marte.py; no se pide a ChatGPT): {que}."


def pieza(carta, mosaico, que, pistas):
    m = MOSAICOS[mosaico]
    i = m["cartas"].index(carta)
    pos = POS[(m["filas"], m["cols"])][i]
    return dict(titulo=f"Carta {carta} — {m['titulo']} ({pos})", tipo="gris",
                mosaico=dict(id=mosaico, filas=m["filas"], cols=m["cols"], fila=i // m["cols"], col=i % m["cols"]),
                descripcion=[que], pistas=pistas, arte=codigo(f"{pos} de «{m['titulo']}»"))


def gris(carta, titulo, que, pistas, arte):
    return dict(titulo=f"Carta {carta} — {titulo}", tipo="gris", descripcion=[que], pistas=pistas, arte=arte)


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
    # ------------------------------------------------------------------ El hangar
    "P": escena("P", "Llegada a la cúpula", [10, 12], [],
                "Segunda parada del Cronoportal: Marte, año 2157. El salto sale mal otra vez y aterrizáis en el hangar de la cúpula Aurora, la primera colonia, a oscuras por una tormenta de polvo. El aparato se queda sin energía. Dentro de hora y media la tormenta cortará las comunicaciones y el soporte vital se apagará del todo: hay que recargar el Cronoportal antes.",
                ["Mirad a vuestro alrededor y revisad el aparato."],
                "El hangar de una colonia en Marte, a oscuras, con luces de emergencia rojas parpadeando, polvo rojizo flotando y una ventana por la que se ve una tormenta de polvo. En el suelo, un aparato de latón y cristal (el Cronoportal) humea y se apaga. Cristina y Alberto, con monos técnicos de la colonia Aurora, se levantan del suelo: ella con los ojos como platos y la boca abierta, él con el ceño fruncido y una ceja arqueada de incredulidad."),
    "10": escena("10", "El hangar de la cúpula", [14, 16, 18, 19, 20, 21, 22], ["P"],
                 "En la pared del hangar, una pantalla de comunicaciones muestra los pasos de tres satélites y espera que alguien programe la llamada a la Tierra. Al otro lado de un cristal, el módulo del invernadero sigue con sus plantas vivas, y en una taquilla cuelga un traje espacial sin casco.",
                 ["Hay dos puzles: la ventana de comunicaciones y el invernadero.", "El invernadero son dos cartas: juntadlas, una encima de otra."],
                 "El hangar de una colonia marciana con una pantalla de comunicaciones en la pared, un cristal que deja ver un invernadero verde y, en una taquilla, un traje espacial sin casco. Cristina examina la pantalla con el dedo apoyado en la barbilla y Alberto pega la nariz al cristal del invernadero con una sonrisa de asombro."),
    "12": combinable("12", "Cronoportal sin energía", "azul", 62, 74,
                     "El Cronoportal con el anillo central apagado y el hueco de su núcleo de fusión vacío.",
                     SIN_GENTE + "Primer plano del Cronoportal: una consola portátil de latón y cristal con dos antenas de cobre, un anillo central apagado y un hueco circular vacío en el pecho del aparato, sobre el suelo metálico de un hangar con polvo rojizo."),
    "14": app("14", "La ventana de comunicaciones", "Es un juego de la app: la antena solo puede llamar a la Tierra cuando los tres satélites pasan a la vez; hay que decir dentro de cuántas horas.", 24,
              ["Los pasos de cada satélite, dibujados, están en la carta 16.", "Mirad cada satélite por separado: cada cuánto pasa y cuándo pasó la primera vez. Después buscad la primera hora en que coinciden.", f"Los tres pasan a la vez {_S_SAT}."],
              SIN_GENTE + "Una antena parabólica en el techo de una cúpula marciana, apuntando a un cielo rojizo con tres puntos de luz."),
    "16": gris("16", "Pasos de los satélites", "Los pasos de los tres satélites por la antena, hora a hora.",
               ["Sirve para la ventana de comunicaciones (carta 14).", "Cada satélite pasa cada tantas horas, siempre igual.", f"Los tres pasan a la vez {_S_SAT}."], codigo("los pasos de los satélites")),
    "18": gris("18", "Las reglas del invernadero", "Las reglas del invernadero, pegadas en la puerta.",
               ["Sirve para el invernadero (carta 20).", "Cada planta se cuenta con sus ocho vecinas. Aplicad las reglas casilla a casilla.", f"Mañana estarán vivas: {_S_VIDA}."], codigo("las reglas del invernadero")),
    "19": pieza("19", "invernadero", "Media lámina del invernadero, tal como está hoy.", ["Es la mitad de una lámina: juntadla con la carta 21.", "Las plantas vivas son las que se ven; el resto, suelo vacío.", f"Mañana estarán vivas: {_S_VIDA}."]),
    "21": pieza("21", "invernadero", "Media lámina del invernadero, tal como está hoy.", ["Es la mitad de una lámina: juntadla con la carta 19.", "Las plantas vivas son las que se ven; el resto, suelo vacío.", f"Mañana estarán vivas: {_S_VIDA}."]),
    "20": app("20", "El invernadero", "Es un juego de la app: marcar qué plantas estarán vivas mañana, aplicando las reglas del invernadero.", 28,
              ["Cómo está hoy, en las cartas 19 y 21; las reglas, en la carta 18.", "Contad, para cada casilla, cuántas vecinas vivas tiene (las ocho de alrededor) y aplicad las reglas.", f"Mañana estarán vivas: {_S_VIDA}."],
              SIN_GENTE + "Un invernadero de una colonia marciana con bancales cuadrados de tierra roja y plantas verdes, bajo luces moradas."),
    "22": combinable("22", "Traje sin casco", "azul", 35, 57, "Un traje espacial blanco con parches de la colonia Aurora, sin casco.",
                     SIN_GENTE + "Un traje espacial blanco de colono marciano con parches naranjas colgado de una taquilla metálica, sin casco."),
    "24": escena("24", "La voz de la doctora Reyes", [26], [14, 16],
                 "La antena conecta y por el altavoz sale una voz entrecortada: «Aquí la doctora Reyes, jefa de la colonia. Estoy atrapada en el anexo, con el reactor al lado. Sin su núcleo de fusión no hay soporte vital ni nada. Os dejo una nota con lo que sé del reactor...» y la voz se pierde. En la impresora cae una hoja.",
                 ["La nota de la doctora servirá más adelante."],
                 "El hangar de la colonia con la antena de comunicaciones activa, un altavoz crepitando y una impresora que escupe una hoja. Alberto sostiene la hoja con los ojos muy abiertos, sorprendido, y Cristina se inclina hacia el altavoz con las manos en las orejas, tensa y atenta."),
    "26": gris("26", "Nota de la doctora Reyes", "Una nota de la doctora Reyes sobre el circuito del reactor.",
               ["Sirve para el circuito del reactor (carta 51).", "El circuito es un solo bucle cerrado; los números dicen por cuántos lados de su casilla pasa.", f"El anillo pasa por los puntos: {_S_ANI}."], codigo("la nota de la doctora Reyes")),
    "28": escena("28", "El módulo del invernadero", [35], [18, 19, 20, 21],
                 "La puerta del módulo se abre con un siseo. Dentro, entre bancales de tierra roja, una tomatera con tomates enormes y, colgado de un gancho, un casco de astronauta con un parche a medio coser.",
                 ["Lo que habéis encontrado se puede juntar con algo que ya tenéis."],
                 "El interior de un invernadero marciano, con bancales de tierra roja, luces moradas y una tomatera cargada de tomates; de un gancho cuelga un casco de astronauta. Cristina acaricia un tomate con una sonrisa maravillada y Alberto descuelga el casco con cara de triunfo."),
    "35": combinable("35", "Casco de astronauta", "roja", 22, 57, "Un casco de astronauta con la visera empañada y un parche de la colonia Aurora.",
                     SIN_GENTE + "Un casco de astronauta con la visera empañada y un parche de la colonia Aurora, colgado de un gancho en un invernadero."),
    "57": escena("57", "El traje completo", [31, 32], [22, 35, 10, 28],
                 "Con el casco puesto, el traje ya sirve. El hangar tiene dos salidas: una puerta interior a la sala de cableado, donde la tormenta ha cortado la energía, y la esclusa exterior, que lleva al campo de rocas y al anexo. Hay que hacer las dos cosas.",
                 ["Hay dos caminos: la sala de cableado y la esclusa exterior. Podéis seguir los dos."],
                 "Un hangar marciano con dos puertas: una interior de metal y la gran esclusa exterior con una luz roja. Cristina, con el traje completo y el casco bajo el brazo, hace un gesto decidido con el puño; Alberto, ya con el casco puesto, mira por la visera con los ojos muy abiertos y la boca en una O."),
    # ------------------------------------------------------------------ Rama 1: el cableado
    "31": escena("31", "La sala de cableado", [40, 41, 43, 45], [],
                 "Una sala con paredes de cables y una gran placa de bornes sin conectar: la tormenta ha arrancado todos los cables de sus sitios y la cúpula funciona con baterías. Cada borne tiene un gemelo en otro punto de la placa.",
                 ["La placa son dos cartas: juntadlas."],
                 SIN_GENTE + "Una sala técnica de una colonia marciana con una gran placa de bornes de colores en la pared, cables sueltos colgando y chispas ocasionales."),
    "40": app("40", "La placa de bornes", "Es un juego de la app: unir cada pareja de bornes del mismo color con un cable, sin cruzarse y sin dejar casillas vacías.", 30,
              ["La placa, con sus bornes gemelos, está en las cartas 41 y 43; la norma, en la 45.", "Empezad por los bornes que tienen pocas salidas posibles (en una esquina o contra un borde) y seguid desde ahí.", f"La placa por filas: {_S_CAB}."],
              SIN_GENTE + "Una placa de bornes de colores en una pared técnica, con cables de colores sin conectar colgando de ella."),
    "41": pieza("41", "cableado", "Media lámina de la placa de bornes.", ["Es la mitad de una placa: juntadla con la carta 43.", "Cada color y número aparece dos veces en toda la placa.", f"La placa por filas: {_S_CAB}."]),
    "43": pieza("43", "cableado", "Media lámina de la placa de bornes.", ["Es la mitad de una placa: juntadla con la carta 41.", "Cada color y número aparece dos veces en toda la placa.", f"La placa por filas: {_S_CAB}."]),
    "45": gris("45", "La norma de los cables", "Lo que dice el manual de la cúpula sobre la placa.",
               ["Sirve para la placa de bornes (carta 40).", "Ningún cable comparte casilla con otro y no queda ninguna vacía.", f"La placa por filas: {_S_CAB}."], codigo("la norma de los cables")),
    "30": escena("30", "La energía vuelve", [38], [31, 40, 41, 43, 45],
                 "La placa se enciende y las luces del pasillo vuelven con un zumbido. Una de las lámparas del techo cae: es un soldador de mano, con la batería agotada. Servirá para soldar el núcleo cuando lo encontréis.",
                 ["Al soldador le falta energía: buscad una batería."],
                 "Un pasillo de una colonia marciana que se ilumina de golpe, con luces blancas parpadeantes; un soldador de mano cae de un soporte del techo. Alberto lo caza al vuelo con cara de susto y Cristina aplaude con una sonrisa de alivio."),
    "38": combinable("38", "Soldador sin batería", "roja", 56, 94, "Un soldador de mano con el compartimento de la batería vacío.",
                     SIN_GENTE + "Un soldador de mano con una punta de cobre y el compartimento de la batería abierto y vacío, sobre una mesa de trabajo metálica."),
    # ------------------------------------------------------------------ Rama 2: el exterior
    "32": escena("32", "La esclusa exterior", [42, 48, 49, 53], [],
                 "La esclusa se abre y salís a la superficie bajo un cielo anaranjado. A lo lejos se ve el anexo, pero entre él y vosotros hay un campo de rocas ocultas por la arena: el radar del traje solo sabe decir cuántas hay cerca de cada casilla despejada. El mapa del radar son dos láminas.",
                 ["El radar son dos cartas: juntadlas."],
                 "La superficie de Marte bajo un cielo anaranjado, con la cúpula de la colonia detrás y, a lo lejos, una pequeña construcción (el anexo); en primer plano, un campo de arena con rocas medio enterradas. Alberto mira el radar de la muñeca con los ojos entornados y Cristina, a su lado, tantea el suelo con una pierna estirada y cara de cautela."),
    "48": app("48", "El campo de rocas", "Es un juego de la app: marcar las rocas escondidas en el campo, con los números del radar.", 36,
              ["El radar, partido en dos láminas, son las cartas 42 y 49; el aviso del radar, la carta 53.", "Un número cuenta las rocas de las ocho casillas de alrededor; una casilla con número nunca tiene roca. Empezad por los números más bajos o los más altos.", f"Las rocas están en: {_S_ROC}."],
              SIN_GENTE + "Un campo de arena rojiza visto desde arriba, dividido en casillas, con unas pocas rocas sobresaliendo del polvo."),
    "42": pieza("42", "rocas", "Media lámina del radar del campo de rocas.", ["Es la mitad de un radar: juntadla con la carta 49.", "Las casillas con número están despejadas; las grises son las desconocidas.", f"Las rocas están en: {_S_ROC}."]),
    "49": pieza("49", "rocas", "Media lámina del radar del campo de rocas.", ["Es la mitad de un radar: juntadla con la carta 42.", "Las casillas con número están despejadas; las grises son las desconocidas.", f"Las rocas están en: {_S_ROC}."]),
    "53": gris("53", "El aviso del radar", "El mensaje automático del radar del traje.",
               ["Sirve para el campo de rocas (carta 48).", "Dice qué cuentan los números y cuántas rocas hay en total.", f"Las rocas están en: {_S_ROC}."], codigo("el aviso del radar")),
    "36": escena("36", "El anexo", [52, 54, 55, 59], [32, 42, 48, 49, 53],
                 "El rover os espera en la puerta del anexo, un edificio bajo con una antena de brazo largo en el techo. La antena está torcida por la tormenta: hay que equilibrar su brazo con pesos de repuesto para que apunte bien a la Tierra. En el garaje, una caja de herramientas con piezas.",
                 ["El brazo de la antena son varias cartas."],
                 "El anexo de una colonia marciana, un edificio bajo con una antena de brazo largo en el techo, ligeramente inclinada; un pequeño rover aparcado en la puerta. Cristina señala la antena con el brazo estirado y la cabeza hacia atrás, y Alberto abre una caja de herramientas y saca una pesa con cara de esfuerzo."),
    "52": app("52", "El brazo de la antena", "Es un juego de la app: colgar tres pesos de repuesto del brazo de la antena para que quede en equilibrio.", 44,
              ["El brazo, con lo que ya cuelga, es la carta 54; lo que pesa cada pieza de repuesto, la 55; la norma, la 59.", "Calculad cuánto empuja cada lado: peso por distancia al eje. Lo que falta para igualar lo tienen que aportar las tres piezas.", f"Las piezas: {_S_BRA}."],
              SIN_GENTE + "Una antena de comunicaciones con un largo brazo horizontal sobre un eje central, con unos pesos colgados en distintos puntos."),
    "54": gris("54", "El brazo de la antena", "El brazo de la antena, con los pesos que ya cuelgan.",
               ["Sirve para el brazo (carta 52).", "Cada marca está a una distancia del eje, a un lado o al otro.", f"Las piezas: {_S_BRA}."], codigo("el brazo de la antena")),
    "55": gris("55", "Los pesos de repuesto", "Las tres piezas de repuesto de la caja de herramientas, con lo que pesa cada una.",
               ["Sirve para el brazo (carta 52).", "La forma de cada pieza es la que veréis en la app.", f"Las piezas: {_S_BRA}."], codigo("los pesos de repuesto")),
    "59": gris("59", "La norma del brazo", "Lo que dice el manual de la antena sobre su equilibrio.",
               ["Sirve para el brazo (carta 52).", "Cada peso empuja su lado tanto como pesa por lo lejos que está del eje.", f"Las piezas: {_S_BRA}."], codigo("la norma del brazo")),
    # ------------------------------------------------------------------ La sala de control
    "44": escena("44", "La sala de control", [33, 37, 39, 46, 51, 61, 63], [36, 52, 54, 55, 59],
                 "La antena apunta bien y una puerta se abre en el anexo: es la sala de control de la doctora Reyes, llena de pantallas. Tiene dos pantallas con trabajo para vosotros: el ordenador de a bordo está calculando la trayectoria del cohete de rescate y necesita una cuenta que no sale, y el esquema del reactor tiene el circuito borrado. La doctora no está, pero su nota os servirá.",
                 ["Hay dos puzles: la cuenta de cifras y el circuito del reactor. La nota de la doctora sirve aquí."],
                 "Una sala de control de una colonia marciana, con pantallas verdes y naranjas, teclados y un gran esquema en la pared. Cristina escribe en un teclado con los ojos muy concentrados y la lengua entre los dientes, y Alberto se rasca la barba frente al esquema, perplejo."),
    "46": app("46", "La cuenta de cifras", "Es un juego de la app: llegar al objetivo de la trayectoria con las piezas del ordenador y las cuatro operaciones.", 56,
              ["Las piezas están en la carta 37, el objetivo en la 39 y la norma en la 33.", "Probad a juntar primero dos piezas pequeñas y pensad qué producto o suma os acerca al objetivo. Cada resultado vale como pieza nueva.", f"Una cuenta que vale: {_S_CUE}."],
              SIN_GENTE + "La pantalla de un ordenador de a bordo con seis fichas numeradas y una cifra grande de objetivo en el centro, en una sala de control."),
    "37": gris("37", "Las piezas de la cuenta", "Las seis piezas del ordenador de a bordo.",
               ["Sirve para la cuenta (carta 46).", "Cada pieza se usa una vez como mucho.", f"Una cuenta que vale: {_S_CUE}."], codigo("las piezas de la cuenta")),
    "39": gris("39", "El objetivo", "El número que pide el ordenador para la trayectoria.",
               ["Sirve para la cuenta (carta 46).", "Es el resultado al que hay que llegar.", f"Una cuenta que vale: {_S_CUE}."], codigo("el objetivo de la cuenta")),
    "33": gris("33", "La norma de la cuenta", "Lo que dice el ordenador sobre las operaciones.",
               ["Sirve para la cuenta (carta 46).", "Todos los resultados son enteros y mayores que cero.", f"Una cuenta que vale: {_S_CUE}."], codigo("la norma de la cuenta")),
    "56": combinable("56", "Batería de la cúpula", "roja", 38, 94, "Una batería de la cúpula, todavía cargada, que el ordenador libera al calcular la trayectoria.",
                     SIN_GENTE + "Una batería grande de color gris con detalles naranjas y dos bornes brillantes, sobre una bandeja de una sala de control."),
    "51": app("51", "El circuito del reactor", "Es un juego de la app: trazar un solo bucle cerrado que respete los números del esquema del reactor.", 58,
              ["El esquema, partido en dos láminas, son las cartas 61 y 63; la nota de la doctora, la carta 26.", "Un número dice por cuántos lados de su casilla pasa el anillo. Empezad por los ceros y por las casillas con el 3 o por otras con números altos.", f"El anillo pasa por los puntos: {_S_ANI}."],
              SIN_GENTE + "El esquema de un reactor de fusión dibujado como una rejilla de puntos con un cable naranja formando un bucle cerrado, en una pantalla."),
    "61": pieza("61", "reactor", "Media lámina del esquema del reactor.", ["Es la mitad de un esquema: juntadla con la carta 63.", "Los números están en las casillas, entre los puntos.", f"El anillo pasa por los puntos: {_S_ANI}."]),
    "63": pieza("63", "reactor", "Media lámina del esquema del reactor.", ["Es la mitad de un esquema: juntadla con la carta 61.", "Los números están en las casillas, entre los puntos.", f"El anillo pasa por los puntos: {_S_ANI}."]),
    "58": escena("58", "El acceso al reactor", [69, 70, 71], [51, 61, 63, 26, 24],
                 "El circuito se enciende y la puerta blindada del reactor se abre un palmo. El pasillo que lleva a la sala del reactor está lleno de escombros y de radiación: no podéis pasar vosotros, pero el rover pequeño sí. Hay que programarlo.",
                 ["El rover se programa con comandos."],
                 "Una puerta blindada de un reactor de una colonia marciana, entreabierta, con un pasillo oscuro tras ella lleno de escombros; un pequeño rover con ruedas espera a los pies de los personajes. Alberto acaricia la carcasa del rover con una sonrisa y Cristina mira el pasillo con gesto preocupado."),
    "69": app("69", "El programa del rover", "Es un juego de la app: programar el rover con comandos y bucles para que llegue a la bandera del fondo del pasillo.", 80,
              ["El terreno del pasillo es la carta 70; los comandos y el límite de bloques, la 71.", "El camino sube en escalera. Si se repite un mismo trozo, un bucle ahorra muchos bloques.", f"Un programa que vale: {_S_PRO}."],
              SIN_GENTE + "Un pequeño rover de ruedas con una antena en un pasillo de una colonia marciana, y una bandera roja al fondo."),
    "70": gris("70", "El terreno del rover", "El pasillo visto desde el dron: muros, camino, el rover y la bandera.",
               ["Sirve para el programa (carta 69).", "El rover sale mirando hacia la derecha.", f"Un programa que vale: {_S_PRO}."], codigo("el terreno del rover")),
    "71": gris("71", "Los comandos del rover", "Los comandos del rover y el límite de bloques.",
               ["Sirve para el programa (carta 69).", "El bloque de «repetir» cuenta como uno y cada comando de dentro, también.", f"Un programa que vale: {_S_PRO}."], codigo("los comandos del rover")),
    "80": escena("80", "El archivo de la colonia", [72, 75, 79], [58, 69, 70, 71],
                 "El rover llega al fondo del pasillo y abre desde dentro un panel con un archivo de la colonia: la base de datos con los planes del cohete de rescate. Está protegida con una clave que la doctora Reyes pensó que solo recordarían los que miraran con atención la sopa de letras que dejó.",
                 ["La base de datos son dos cartas."],
                 "Una pequeña sala de archivo de una colonia marciana con una pantalla encendida y un rover de ruedas con un cable conectado a un panel. Cristina mira la pantalla con una sonrisa de asombro y los ojos muy abiertos, y Alberto agita los brazos, eufórico, al ver llegar al rover sano y salvo."),
    "72": app("72", "La base de datos", "Es un juego de la app: la clave de acceso es la palabra que forman las letras sobrantes de la sopa de letras.", 82,
              ["La sopa y la lista de palabras, en las cartas 75 y 79 (dos mitades).", "Tachad en la sopa todas las palabras de la lista: las letras que quedan, leídas en orden de lectura, forman la clave.", f"La clave es {_S_SOP}."],
              SIN_GENTE + "Una pantalla de un ordenador de colonia con una sopa de letras y un campo vacío para escribir una clave de acceso."),
    "75": pieza("75", "sopa", "Media lámina de la base de datos de la colonia.", ["Es la mitad de una lámina: juntadla con la carta 79.", "Las palabras de la lista están en la rejilla, en cualquier dirección.", f"La clave es {_S_SOP}."]),
    "79": pieza("79", "sopa", "Media lámina de la base de datos de la colonia.", ["Es la mitad de una lámina: juntadla con la carta 75.", "Las palabras de la lista están en la rejilla, en cualquier dirección.", f"La clave es {_S_SOP}."]),
    "82": escena("82", "El control de lanzamiento", [85, 86, 87], [80, 72, 75, 79],
                 "Los archivos se abren y entre ellos hay un pequeño aparato de latón y cristal, idéntico al vuestro: la doctora Reyes lo guardó sin saber de dónde venía. Os da una idea: sus comandos de lanzamiento, que conectan con el Cronoportal, piden una clave de cuatro cifras. Y la doctora ha dejado dos acertijos.",
                 ["La consola es el último puzle."],
                 "Una sala de control de lanzamiento de una colonia marciana con una gran consola de botones y pantallas, y sobre ella un aparato de latón y cristal. Cristina lo sostiene en alto con los ojos como platos y Alberto se tapa la boca con la mano, boquiabierto, mirando de él al suyo."),
    "85": app("85", "La consola de lanzamiento", "Es un juego de la app: la clave de lanzamiento son cuatro cifras, los datos de la misión de otros puzles, en el orden de los acertijos.", 99,
              ["Los acertijos están en las cartas 86 y 87; cada puzle que habéis resuelto mostró un «dato de la misión» en su mensaje.", "Cada acertijo describe un puzle por lo que hacía: lo que une con cobre, lo que da vueltas sobre nuestras cabezas, lo que se equilibra con pesos, lo que crece o se seca.", f"La clave: {_S_COD}."],
              SIN_GENTE + "La consola de lanzamiento de una colonia marciana: un panel con cuatro ruedas numeradas y un gran botón rojo, bajo una luz naranja."),
    "86": gris("86", "Primera parte de la clave", "Los dos primeros datos de la clave, en un acertijo de la doctora Reyes.",
               ["Sirve para la consola (carta 85).", "Dos puzles: el que unía bornes con cobre y el que miraba pasar satélites.", f"La clave: {_S_COD}."], codigo("los dos primeros datos")),
    "87": gris("87", "Segunda parte de la clave", "Los dos últimos datos de la clave, en otro acertijo de la doctora Reyes.",
               ["Sirve para la consola (carta 85).", "Dos puzles: el que se equilibraba con pesos y el que crecía o se secaba.", f"La clave: {_S_COD}."], codigo("los dos últimos datos")),
    # ------------------------------------------------------------------ El reactor y el final
    "94": escena("94", "La sala del reactor", [64, 66, 67], [38, 56, 30, 44, 33, 37, 39, 46],
                 "Con el soldador cargado, los dos entráis por fin en la sala del reactor: un círculo de metal con el núcleo de fusión en el centro, rodeado de paneles de refrigeración apagados. Si no se enfrían, el núcleo no se deja tocar. El patrón de los paneles está dibujado en una pantalla.",
                 ["El patrón son dos cartas: juntadlas."],
                 "La sala circular de un reactor de fusión en una colonia marciana, con un núcleo brillante en el centro y paneles de refrigeración en las paredes, iluminada por luz azul. Cristina sostiene el soldador con ambas manos, con gesto cauteloso, y Alberto observa los paneles con la cabeza ladeada y los labios apretados."),
    "64": app("64", "Los paneles de refrigeración", "Es un juego de la app: encender el patrón de la pantalla; cada panel que se toca cambia él y sus cuatro vecinos en cruz.", 62,
              ["El patrón, con la regla, es el de las cartas 66 y 67.", "Se empieza con todos apagados. Un mismo panel tocado dos veces es como no tocarlo; el orden de los toques da igual.", f"Podéis tocar: {_S_PAN}."],
              SIN_GENTE + "Una pared de la sala de un reactor con una cuadrícula de paneles cuadrados de refrigeración, algunos apagados y otros con luz cian."),
    "66": pieza("66", "paneles", "Media lámina de los paneles de refrigeración.", ["Es la mitad de una lámina: juntadla con la carta 67.", "Los paneles encendidos son los círculos luminosos.", f"Podéis tocar: {_S_PAN}."]),
    "67": pieza("67", "paneles", "Media lámina de los paneles de refrigeración.", ["Es la mitad de una lámina: juntadla con la carta 66.", "Los paneles encendidos son los círculos luminosos.", f"Podéis tocar: {_S_PAN}."]),
    "62": combinable("62", "Núcleo de fusión", "roja", 12, 74, "El núcleo de fusión del reactor, soldado y frío, del tamaño de un puño, con una luz cian en su interior.",
                     SIN_GENTE + "Una esfera de metal y cristal del tamaño de un puño con una luz cian palpitando en su interior, sostenida sobre una palma con guante blanco, en una sala de reactor."),
    "74": escena("74", "Cronoportal cargado", [], [62, 12, 64, 66, 67, 94, 57],
                 "El núcleo encaja en el pecho del Cronoportal y el aparato se llena de luz cian... pero el salto pide una clave de lanzamiento. Hay que despertarlo desde la consola.",
                 ["Falta la clave de lanzamiento."],
                 "El Cronoportal con el núcleo de fusión encajado en el pecho, brillando con luz cian, en una sala de control marciana. Alberto ajusta los diales con la lengua entre los dientes y Cristina lleva una tomatera bajo el brazo con una sonrisa de alivio."),
    "99": escena("99", "De vuelta a casa (FIN)", [], [74, 82, 85, 86, 87],
                 "La clave es correcta y el Cronoportal se enciende. Se abre un portal de luz azul y saltáis justo cuando el soporte vital termina de reactivarse en toda la cúpula. Aterrizáis en vuestro salón. Cristina deja una tomatera sobre la mesa: «¡Me la he traído!». Alberto, riendo: «Mañana, otro destino». FIN.",
                 [],
                 "La escena ocurre DENTRO del salón de su casa actual, en el presente (sofá, estanterías con libros, plantas, una lámpara encendida y luz cálida de tarde por la ventana): acaban de VOLVER a casa. Cristina y Alberto acaban de salir de un portal circular de luz azul que se abre detrás de ellos; a través del portal todavía se ven el hangar de la colonia marciana y el polvo rojizo. Llevan aún los monos técnicos de colonos marcianos y Cristina deja una pequeña tomatera sobre la mesa del salón. Cristina ríe a carcajadas, orgullosa; Alberto ríe con la cabeza echada hacia atrás, aliviado. Están de cara a nosotros, aterrizando en el salón y alejándose del portal, que queda a su espalda y se está cerrando; el mundo de la aventura solo se ve a través del portal, detrás de ellos. No están entrando en el portal ni saliendo de casa: están llegando."),
}

META = dict(juego="Marte, 2157 — Cúpula Aurora", estilo=ESTILO, personajes=PERSONAJES, hoja=HOJA, foto=FOTO, video=VIDEO,
            mosaicos={k: dict(filas=m["filas"], cols=m["cols"], cartas=m["cartas"], titulo=m["titulo"]) for k, m in MOSAICOS.items()})

SPEC = dict(final="99", needs={
    "24": ["14", "16"], "28": ["20", "18", "19", "21"], "57": ["22", "35"], "30": ["40", "41", "43", "45"], "36": ["48", "42", "49", "53"],
    "44": ["52", "54", "55", "59"], "56": ["46", "37", "39", "33"], "58": ["51", "26", "61", "63"], "80": ["69", "70", "71"], "94": ["38", "56"],
    "62": ["64", "66", "67"], "82": ["72", "75", "79"], "74": ["12", "62"], "99": ["85", "86", "87", "74"]}, eventos={})

PARA_QUE = {k: c["titulo"].split("— ", 1)[1] for k, c in J.items()}

_T = [
    ("leer", "P", "Llegada", "Pon el Modo PC (solo la P en la mesa) y en el móvil pulsa Empezar. Lee la carta P: coge la 10 y la 12."),
    ("leer", "10", "El hangar", "Lee la carta 10. Descarta la P y coge 14, 16, 18, 19, 20, 21 y 22. Junta el invernadero: 19 arriba y 21 abajo."),
    ("app", "14", "La ventana de comunicaciones", f"En el móvil: Acción, 14. Los pasos de los satélites (16): coinciden los tres {_S_SAT}. El mensaje te dice que cojas la 24. Anota el dato de la misión: 3.", "carta 24"),
    ("leer", "24", "La voz de la doctora", "Lee la carta 24. Descarta 14 y 16 y coge la 26 (guárdala para el reactor)."),
    ("app", "20", "El invernadero", f"En el móvil: Acción, 20. Con las reglas (18) y el invernadero de hoy (19 y 21): mañana estarán vivas {_S_VIDA}. El mensaje te dice que cojas la 28. Anota el dato de la misión: 8.", "carta 28"),
    ("leer", "28", "El módulo del invernadero", "Lee la carta 28. Descarta 18, 19, 20 y 21 y coge la 35."),
    ("combinar", "22", "35", "El traje", "El traje (22) y el casco (35) son combinables: 22 + 35 = 57. Coge la 57."),
    ("leer", "57", "El traje completo", "Lee la carta 57. Descarta 22, 35, 10 y 28 y coge 31 y 32."),
    ("leer", "31", "La sala de cableado", "Lee la carta 31. Coge 40, 41, 43 y 45. Junta la placa: 41 a la izquierda y 43 a la derecha."),
    ("app", "40", "La placa de bornes", f"En el móvil: Acción, 40. Cables que unen sus bornes sin cruzarse (41, 43 y 45): {_S_CAB}. El mensaje te dice que cojas la 30. Anota el dato de la misión: 5.", "carta 30"),
    ("leer", "30", "La energía vuelve", "Lee la carta 30. Descarta 31, 40, 41, 43 y 45 y coge la 38."),
    ("leer", "32", "La esclusa exterior", "Lee la carta 32. Coge 42, 48, 49 y 53. Junta el radar: 42 a la izquierda y 49 a la derecha."),
    ("app", "48", "El campo de rocas", f"En el móvil: Acción, 48. Con los números del radar (42, 49 y 53): rocas en {_S_ROC}. El mensaje te dice que cojas la 36.", "carta 36"),
    ("leer", "36", "El anexo", "Lee la carta 36. Descarta 32, 42, 48, 49 y 53 y coge 52, 54, 55 y 59."),
    ("app", "52", "El brazo de la antena", f"En el móvil: Acción, 52. Con el brazo (54), las piezas (55) y la norma (59): {_S_BRA}. El mensaje te dice que cojas la 44. Anota el dato de la misión: 2.", "carta 44"),
    ("leer", "44", "La sala de control", "Lee la carta 44. Descarta 36, 52, 54, 55 y 59 y coge 33, 37, 39, 46, 51, 61 y 63. Junta el esquema: 61 a la izquierda y 63 a la derecha."),
    ("app", "46", "La cuenta de cifras", f"En el móvil: Acción, 46. Con las piezas (37), el objetivo (39) y la norma (33): {_S_CUE}. El mensaje te dice que cojas la 56.", "carta 56"),
    ("app", "51", "El circuito del reactor", f"En el móvil: Acción, 51. Con el esquema (61 y 63) y la nota (26): el anillo pasa por {_S_ANI}. El mensaje te dice que cojas la 58.", "carta 58"),
    ("leer", "58", "El acceso al reactor", "Lee la carta 58. Descarta 51, 61, 63, 26 y 24 y coge 69, 70 y 71."),
    ("app", "69", "El programa del rover", f"En el móvil: Acción, 69. Con el terreno (70) y los comandos (71): {_S_PRO}. El mensaje te dice que cojas la 80.", "carta 80"),
    ("leer", "80", "El archivo de la colonia", "Lee la carta 80. Descarta 58, 69, 70 y 71 y coge 72, 75 y 79. Junta la sopa: 75 a la izquierda y 79 a la derecha."),
    ("app", "72", "La base de datos", f"En el móvil: Acción, 72. Las letras que no pertenecen a ninguna palabra de la lista (75 y 79) forman {_S_SOP}. El mensaje te dice que cojas la 82.", "carta 82"),
    ("leer", "82", "El control de lanzamiento", "Lee la carta 82. Descarta 80, 72, 75 y 79 y coge 85, 86 y 87."),
    ("combinar", "38", "56", "El soldador", "El soldador (38) y la batería (56) son combinables: 38 + 56 = 94. Coge la 94."),
    ("leer", "94", "La sala del reactor", "Lee la carta 94. Descarta 38, 56, 30, 44, 33, 37, 39 y 46 y coge 64, 66 y 67. Junta el patrón: 66 arriba y 67 abajo."),
    ("app", "64", "Los paneles", f"En el móvil: Acción, 64. Con el patrón (66 y 67), tocando {_S_PAN}. El mensaje te dice que cojas la 62.", "carta 62"),
    ("combinar", "12", "62", "El núcleo", "El Cronoportal (12) y el núcleo de fusión (62) son combinables: 12 + 62 = 74. Coge la 74."),
    ("leer", "74", "Cronoportal cargado", "Lee la carta 74. Descarta 62, 12, 64, 66, 67, 94 y 57."),
    ("app", "85", "La consola", f"En el móvil: Acción, 85. Con los acertijos (86 y 87) y los datos de la misión de los puzles: {_S_COD}. El mensaje te dice que cojas la 99.", "carta 99"),
    ("leer", "99", "Final", "Lee la carta 99. Descarta 74, 82, 85, 86 y 87. En la mesa solo queda la 99. ¡Fin!"),
]
PASOS = []
for _p in _T:
    if _p[0] == "combinar":
        PASOS.append(dict(t=_p[3], que=_p[4], acciones=[("combinar", _p[1], _p[2])]))
    elif _p[0] == "app":
        PASOS.append(dict(t=_p[2], que=_p[3], acciones=[("app", _p[1], _p[4])]))
    else:
        PASOS.append(dict(t=_p[2], que=_p[3], acciones=[("leer", _p[1])]))
_amp.separar_mosaicos(J, PASOS)
_amp.recalcular_mesas(PASOS, J)
