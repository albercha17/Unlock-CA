"""Reino de Hielo y Fuego: La Corona del Dragón — versión de 60 cartas (21 oct 2026), mucho más difícil y variada.

Once puzles de tipos que no salen en ningún otro juego de la serie, con las pistas dibujadas o en acertijo (ninguna carta explica cómo se
resuelve su puzle): las jarras de hidromiel, los ocho centinelas de la muralla (problema de las damas), el viaje de los cuervos (viajante), el
cifrado de Playfair, el juego de las piedras (Nim) contra el carcelero, los puentes entre castillos (Hashi), la sucesión al trono, el sudoku de las
seis casas, las torres de hielo (Hanói), el tapiz del sigilo (nonograma) y la profecía final, una cuenta con las cifras de cuatro puzles.
Solo 15 cartas tienen a Cristina y Alberto (escenas); el resto son objetos y pistas sin personas.
Las cartas-pista las dibuja herramientas/trono.py (instancias_trono.py)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ampliacion as _amp  # noqa: E402
import instancias_trono as I  # noqa: E402

ESTILO = ("Ilustración digital cinematográfica de fantasía medieval oscura y semirrealista, con aire de gran serie de aventuras: fortalezas de piedra negra, nieve, "
          "ventisca, antorchas y fuego, paleta de azules glaciales, grises de piedra y negros profundos con destellos naranjas de llamas, copos de nieve en el aire, "
          "formato vertical 2:3. Sin texto, letras ni números en la imagen; los mapas, rollos y tapices son solo dibujos decorativos sin escritura legible. "
          "Deja libre de detalles importantes la esquina superior izquierda y el 18 % inferior de la imagen. "
          "Los personajes tienen siempre expresiones distintas y expresivas, adecuadas a la escena (nunca la misma cara en dos imágenes).")

PERSONAJES = {
    "Cristina": "Cristina, mujer de 26 años, profesora, pelo rubio y rizado recogido en una trenza, ojos azules. Viste ropa de viaje medieval de invierno: capa de lana gris con capucha forrada de piel, jubón de cuero ajustado, guantes, falda larga de lana y botas altas.",
    "Alberto": "Alberto, hombre de 27 años, informático, pelo moreno corto, barba cuidada, ojos marrones. Viste ropa medieval de invierno: jubón oscuro de cuero con cinturón, capa larga de piel sobre los hombros, guantes, pantalón de lana y botas altas."
}

HOJA = ("Crea una hoja de personajes (character sheet) con las dos personas de la foto adjunta, de cuerpo entero y de frente, sobre fondo claro y neutro. "
        "Mantén su parecido real con la foto (cara, pelo, barba, ojos). "
        "Cristina: mujer de 26 años, profesora, pelo rubio y rizado recogido en una trenza, ojos azules, capa de lana gris con capucha forrada de piel, jubón de cuero ajustado, guantes, falda larga de lana y botas altas. "
        "Alberto: hombre de 27 años, informático, pelo moreno corto, barba cuidada, ojos marrones, jubón oscuro de cuero con cinturón, capa larga de piel sobre los hombros, guantes, pantalón de lana y botas altas. "
        "Estilo: " + ESTILO)

FOTO = ("Antes de nada, adjunta a ChatGPT una foto de Cristina y Alberto juntos (o una de cada uno, con la cara bien visible). "
        "Pídele que mantenga el parecido real, pero con el estilo de ilustración de este juego.")

VIDEO = ("Crea un vídeo vertical 9:16 de 15 segundos, con estilo cinematográfico de fantasía medieval oscura, colores azules glaciales y destellos naranjas. Sin ningún texto, letra ni subtítulo en pantalla. "
         "Escena 1 (0-4 s): en el salón de una casa actual, Cristina (mujer de 26 años, rubia de pelo rizado, ojos azules) y Alberto (hombre de 27 años, moreno con barba, ojos marrones), con abrigos de invierno, rodean un aparato de latón y cristal con un anillo central: el Cronoportal. Cristina mira emocionada un libro con un dragón en la tapa. "
         "Escena 2 (4-8 s): el anillo se enciende con un arco de luz azul, el salón se deforma y los dos son absorbidos por un túnel de luz con copos de nieve. "
         "Escena 3 (8-12 s): caen sobre la nieve del patio de una fortaleza de piedra negra, en plena ventisca; al fondo, una muralla enorme y torres; un cuervo grazna y, muy arriba, una sombra con alas cruza las nubes; el aparato humea y se apaga. "
         "Escena 4 (12-15 s): primer plano de Cristina y Alberto, con capas de abrigo, mirando al cielo cubierto de nieve; fundido a negro. "
         "Sonido: zumbido eléctrico creciente, silbido del portal, golpe sordo al aterrizar, viento helado, graznido de cuervo, un rugido lejano de dragón, música épica de cuerdas graves y tambores, sin voz de narrador.")

ESTILO += " Los personajes tienen siempre expresiones distintas y expresivas, adecuadas a la escena (nunca la misma cara en dos imágenes)."
SIN_GENTE = "Sin ninguna persona en la imagen. "

MOSAICOS = {
    "muralla": dict(filas=2, cols=1, cartas=["19", "21"], titulo="La muralla de Piedra Negra"),
    "castillos": dict(filas=1, cols=2, cartas=["37", "39"], titulo="Los castillos del reino"),
    "arbol": dict(filas=1, cols=2, cartas=["61", "63"], titulo="El árbol del rey Aerion"),
    "casas": dict(filas=2, cols=1, cartas=["70", "71"], titulo="El tablero de las seis casas"),
}
POS = {(2, 1): ["mitad de arriba", "mitad de abajo"], (1, 2): ["mitad izquierda", "mitad derecha"]}
_c = lambda x, y: f"{'ABCDEFGH'[x]}{y + 1}"
_JT = {"llenar A": "llenad la jarra I", "llenar B": "llenad la jarra II", "vaciar A": "vaciad la jarra I", "vaciar B": "vaciad la jarra II",
       "A a B": "pasad de la I a la II", "B a A": "pasad de la II a la I"}
_S_JAR = "Una forma: " + ", ".join(_JT[m] for m in I.JARRAS["ruta"])
_S_CEN = "Los centinelas van en " + ", ".join(_c(x, y) for x, y in I.CENTINELAS["solucion"])
_S_CUE = "La ruta más corta (" + str(I.CUERVOS["minimo"]) + " leguas): " + " → ".join(str(i + 1) for i in I.CUERVOS["solucion"]) + " → 1"
_S_PLA = f"El mensaje es {I.PLAYFAIR['claro']}"
_S_PIE = "Tomad 1 piedra al empezar (quedan 20) y, tras cada jugada del carcelero, tomad lo que haga que queden 16, 12, 8, 4 y 0"
_LET = {k: "ABCDEFGHIJKLMNOP"[i] for i, k in enumerate(sorted([tuple(map(int, s.split(","))) for s in I.CAMINOS["islas"]], key=lambda t: (t[1], t[0])))}
_S_HAS = "; ".join(f"{_LET[tuple(a)]}–{_LET[tuple(b)]}: {'un puente' if c == 1 else 'dos puentes'}" for a, b, c in I.CAMINOS["puentes"])
_S_SUC = "Hereda Daemon: es el hijo del hijo mayor, Baelor, y los hijos del primer hijo van antes aunque este haya muerto; Maegor no puede por sus votos"
_S_SUD = "Con 1 lobo, 2 león, 3 kraken, 4 rosa, 5 sol y 6 trucha: " + " / ".join(" ".join(str(v) for v in f) for f in I.SUDOKU["solucion"])
_S_TAP = " / ".join("".join("#" if v else "." for v in f) for f in I.TAPIZ["solucion"])


def _hanoi(n, a, b, c, out):
    if n:
        _hanoi(n - 1, a, c, b, out)
        out.append(f"{a}→{c}")
        _hanoi(n - 1, b, a, c, out)


_H = []
_hanoi(I.TORRES["discos"], "I", "II", "III", _H)
_S_TOR = "Los 15 movimientos, de torre a torre: " + ", ".join(_H)
_S_PRO = f"{I.DATOS['40']} × {I.DATOS['14']} − {I.DATOS['52']} + {I.DATOS['20']} = {I.RESULTADO}"


def codigo(que):
    return f"Carta dibujada por código (herramientas/trono.py; no se pide a ChatGPT): {que}."


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
    # ------------------------------------------------------------------ El patio de armas
    "P": escena("P", "Llegada a Piedra Negra", [10, 12], [],
                "Sexta parada del Cronoportal: un reino de hielo y fuego, en pleno invierno. Cristina lleva toda la vida soñando con castillos, caballeros y dragones. El salto vuelve a salir mal: aterrizáis en el patio de armas de la fortaleza de Piedra Negra, en el norte del reino, en mitad de una ventisca. El aparato golpea una piedra y su anillo de cristal se agrieta: sin una esquirla de dragón, esa piedra de fuego que solo guardan los dragones, no volverá a encenderse. Y la tormenta cierra los pasos de montaña: dentro de cien minutos el último paso quedará sellado hasta la primavera, y vosotros con él.",
                ["Mirad a vuestro alrededor y revisad el aparato."],
                "El patio de armas de una fortaleza medieval de piedra negra en mitad de una ventisca, con torres, antorchas apagadas por el viento y nieve por todas partes. En el suelo, un aparato de latón y cristal con el anillo agrietado (el Cronoportal) humea sobre la nieve. Cristina, con capa gris de lana con capucha forrada de piel, mira las torres con los ojos brillantes y la boca abierta de pura emoción; Alberto, con capa larga de piel, se sacude la nieve con una mueca de frío y una ceja arqueada."),
    "10": escena("10", "El patio de armas", [14, 16, 18, 19, 20, 21, 22], ["P"],
                 "Los guardias de Piedra Negra os miran con recelo, pero el senescal, un viejo con una gran llave al cinto, tiene un trato: «Si me ayudáis con dos encargos, os dejo ir a la torre del maestre. Primero, necesito medir hidromiel con dos jarras sin marcas. Y segundo, los centinelas de la muralla están mal puestos y se ven unos a otros». En el suelo, una antorcha apagada.",
                 ["Hay dos encargos: las jarras del senescal y los centinelas de la muralla.", "La muralla son dos cartas: juntadlas, una encima de otra."],
                 "El patio de armas de una fortaleza medieval nevada con unos guardias de armadura mirando con recelo y un senescal anciano con una gran llave al cinto, que señala una muralla. Cristina habla con el senescal con las manos abiertas y gesto conciliador; Alberto examina con el ceño fruncido una antorcha apagada que ha cogido del suelo."),
    "12": combinable("12", "Cronoportal sin energía", "azul", 62, 74,
                     "El Cronoportal con el anillo de cristal agrietado y apagado, sin energía.",
                     SIN_GENTE + "Primer plano del Cronoportal: una consola portátil de latón y cristal con dos antenas de cobre, un anillo de cristal central agrietado y apagado, sobre la nieve del patio de una fortaleza."),
    "14": app("14", "Las jarras del senescal", "Es un juego de la app: medir en el cuenco del rey justo lo que marca el fuego, con dos jarras sin marcas.", 24,
              ["Lo que cabe en cada jarra y lo que se quiere en el cuenco, en la carta 16.", "Las jarras no tienen marcas: pasad hidromiel de una a otra hasta que quede una cantidad exacta. Llenad siempre la pequeña y pasadla a la grande.", f"{_S_JAR}."],
              SIN_GENTE + "Dos jarras de barro sin marcas y un cuenco de madera sobre un barril de hidromiel en la cocina de una fortaleza medieval."),
    "16": gris("16", "El encargo del senescal", "Dos jarras con sus rayas y el cuenco del rey, con la medida que se quiere.",
               ["Sirve para las jarras (carta 14).", "Cada raya vale un cuenco pequeño de hidromiel.", f"{_S_JAR}."], codigo("las jarras y el cuenco")),
    "18": gris("18", "El acertijo de la muralla", "Un acertijo pintado en la puerta de la torre.",
               ["Sirve para los centinelas (carta 20).", "Ningún centinela ve a otro: ni en fila, ni en columna, ni en diagonal.", f"{_S_CEN}."], codigo("el acertijo de la muralla")),
    "19": pieza("19", "muralla", "Media lámina de la muralla de Piedra Negra.", ["Es la mitad de una lámina: juntadla con la carta 21.", "Hay tres centinelas ya puestos.", f"{_S_CEN}."]),
    "21": pieza("21", "muralla", "Media lámina de la muralla de Piedra Negra.", ["Es la mitad de una lámina: juntadla con la carta 19.", "Hay tres centinelas ya puestos.", f"{_S_CEN}."]),
    "20": app("20", "Los centinelas de la muralla", "Es un juego de la app: poner ocho centinelas en una muralla de ocho por ocho sin que ninguno vea a otro.", 28,
              ["La muralla, con los tres centinelas ya puestos, son las cartas 19 y 21; el acertijo, la 18.", "Cada fila y cada columna llevan un solo centinela. Empezad por los puestos y tachad todas las casillas que ven.", f"{_S_CEN}."],
              SIN_GENTE + "Una muralla de piedra negra vista desde arriba como un tablero de casillas, con torres de vigía de tejado rojo y nieve."),
    "22": combinable("22", "Antorcha apagada", "azul", 35, 57, "Una antorcha de la muralla, apagada por la ventisca, con la brea todavía fresca.",
                     SIN_GENTE + "Una antorcha de madera con la brea fresca, apagada y cubierta de copos de nieve, apoyada en una muralla de piedra negra."),
    "24": escena("24", "El senescal os cree", [26], [14, 16],
                 "El senescal prueba el hidromiel con cara de satisfacción: «Medida exacta. No sois espías de los de más allá del Muro». Hurga entre sus llaves y os da una hoja arrugada con las leyes del reino, copiadas por el maestre, que él nunca ha sabido leer del todo.",
                 ["Las leyes del reino servirán más adelante."],
                 "Una cocina de fortaleza medieval con barriles de hidromiel y un senescal anciano de barba blanca que entrega a Cristina una hoja arrugada con una sonrisa socarrona. Ella la recoge con las dos manos y una mirada de agradecimiento; Alberto, detrás, prueba el hidromiel de un cuenco con los ojos cerrados de placer."),
    "26": gris("26", "Las leyes del reino", "Las leyes de sucesión del reino, copiadas por el maestre.",
               ["Sirve para la sucesión (carta 51).", "Apartad a quien no puede heredar y mirad la línea del hijo mayor, aunque haya muerto.", f"{_S_SUC}."], codigo("las leyes del reino")),
    "28": escena("28", "La muralla", [35], [18, 19, 20, 21],
                 "Los centinelas ocupan sus nuevos puestos y la muralla queda sin puntos ciegos. Un capitán agradecido os entrega un pedernal que lleva colgado al cuello: «Sirve para encender cualquier cosa, incluso con este viento».",
                 ["Lo que habéis recibido se puede juntar con algo que ya tenéis."],
                 "La muralla de una fortaleza medieval nevada con centinelas armados con lanzas en sus puestos de vigía y un capitán que entrega un pedernal a Alberto. Él lo recibe con una sonrisa de triunfo y la cabeza alta, y Cristina observa a los centinelas con las manos en las caderas y un gesto de satisfacción."),
    "35": combinable("35", "Pedernal", "roja", 22, 57, "Un pedernal de borde afilado, con el que salen chispas aun con viento.",
                     SIN_GENTE + "Un pedernal de borde afilado y un eslabón de acero sobre un guante de cuero, soltando chispas."),
    "57": escena("57", "La torre del maestre", [31, 32], [22, 35, 10, 28],
                 "La antorcha se enciende con las chispas del pedernal y os abre el camino por una escalera de caracol a la torre del maestre, un anciano de barba larga con una gran cadena al cuello. «Os esperaba, viajeros... Hay un cuervo que no llega y una prisionera que no habla. Haced las dos cosas y os daré la pista de la esquirla».",
                 ["Hay dos caminos: la torre de los cuervos y el calabozo de la prisionera. Podéis seguir los dos."],
                 "La torre de un maestre medieval, con una escalera de caracol de piedra iluminada por una antorcha, libros por todas partes y un anciano de barba larga y cadena al cuello. Cristina sostiene la antorcha encendida con gesto decidido; Alberto sube de dos en dos los escalones, con la boca abierta de pasmo al ver los libros."),
    # ------------------------------------------------------------------ Rama 1: los cuervos
    "31": escena("31", "La torre de los cuervos", [40, 41, 43, 45], [],
                 "En lo alto de la torre hay un palomar lleno de cuervos negros. El maestre tiene que mandar uno con cartas a las seis fortalezas del reino, y cada legua se paga en trigo: quiere la ruta más corta. En la pared, un mapa y un libro con las leguas entre cada dos fortalezas.",
                 ["El mapa y las leguas son cartas distintas."],
                 SIN_GENTE + "Un palomar en lo alto de una torre medieval, lleno de cuervos negros, con un mapa clavado en la pared y un libro grueso abierto sobre un atril."),
    "40": app("40", "Los cuervos mensajeros", "Es un juego de la app: elegir la ruta más corta para que un cuervo visite las seis fortalezas y vuelva a Piedra Negra.", 30,
              ["Dónde está cada fortaleza, en la carta 41; las leguas entre cada dos, en la 43; el acertijo, en la 45.", "Probad a ir siempre a la fortaleza más cercana y ved si al final queda un tramo largo. Después buscad cómo mejorarlo.", f"{_S_CUE}."],
              SIN_GENTE + "Un cuervo negro volando sobre un mapa de montañas nevadas con seis fortalezas pequeñas dibujadas."),
    "41": gris("41", "El mapa de los siete reinos", "Las seis fortalezas, dibujadas y numeradas.",
               ["Sirve para los cuervos (carta 40).", "La fortaleza 1 es Piedra Negra, de donde parte el cuervo.", f"{_S_CUE}."], codigo("el mapa de las fortalezas")),
    "43": gris("43", "Las leguas entre fortalezas", "Una tabla con las leguas que hay entre cada dos fortalezas.",
               ["Sirve para los cuervos (carta 40).", "Cada número es el camino entre dos fortalezas, por su fila y su columna.", f"{_S_CUE}."], codigo("la tabla de leguas")),
    "45": gris("45", "El acertijo de los cuervos", "Un acertijo grabado en el palomar.",
               ["Sirve para los cuervos (carta 40).", "Se visita cada fortaleza una vez y se vuelve a casa.", f"{_S_CUE}."], codigo("el acertijo de los cuervos")),
    "30": escena("30", "El cuervo vuela", [38], [31, 40, 41, 43, 45],
                 "El cuervo sale por la ventana, negro como el carbón, y el maestre sonríe: «Ruta perfecta». Como pago os da una mitad de un sello de cera partido por la mitad: «El sello del dragón. La otra mitad la tiene quien guarda la cripta. Juntas, abren la puerta del dragón».",
                 ["Lo que habéis recibido se puede juntar con otra mitad."],
                 "Un maestre medieval anciano que suelta un cuervo negro por una ventana de la torre en mitad de la nieve, y entrega a Cristina una mitad de un sello de cera. Ella sostiene la mitad del sello contra la luz de una vela con una sonrisa curiosa; Alberto sigue al cuervo con la mirada por la ventana, con la boca entreabierta."),
    "38": combinable("38", "Mitad del sello", "roja", 56, 94, "Una mitad de un sello de cera roja con la cabeza de un dragón, partido en dos.",
                     SIN_GENTE + "La mitad de un sello de cera roja con la cabeza de un dragón en relieve, partido por la mitad, sobre un pergamino."),
    # ------------------------------------------------------------------ Rama 2: el calabozo
    "32": escena("32", "El calabozo de la prisionera", [42, 48, 49, 53], [],
                 "En el calabozo hay una mujer de más allá del Muro, de pelo rojo, encadenada. No habla con nadie, pero ha dejado una carta cifrada para quien sepa leerla, con un cuadrado de letras y una regla. La carta, el cuadrado y la regla, tres papeles.",
                 ["La carta, el cuadrado y la regla son cartas distintas."],
                 "Un calabozo de piedra de una fortaleza medieval con una mujer de pelo rojo encadenada a la pared y unos pergaminos cifrados sobre un taburete. Alberto lee los pergaminos con el ceño muy fruncido y los labios apretados; Cristina mira a la prisionera con gesto amable y compasivo."),
    "48": app("48", "La carta de la prisionera", "Es un juego de la app: descifrar el mensaje de la prisionera, cifrado con el método de las parejas de letras.", 36,
              ["La carta cifrada es la 42, el cuadrado de la clave es la 49 y la regla para cifrar es la 53.", "Para descifrar hay que hacer lo contrario que la regla: misma fila, la de la izquierda; misma columna, la de arriba; rectángulo, las esquinas en su fila.", f"{_S_PLA}."],
              SIN_GENTE + "Una carta de pergamino cifrada con parejas de letras, un cuadrado de veinticinco letras dibujado y una vela, sobre un taburete en un calabozo."),
    "42": gris("42", "La carta de la prisionera", "La carta cifrada: letras escritas por parejas.",
               ["Sirve para el mensaje (carta 48).", "Se descifra pareja a pareja, con el cuadrado de la carta 49.", f"{_S_PLA}."], codigo("la carta cifrada")),
    "49": gris("49", "El cuadrado de la clave", "Un cuadrado de veinticinco letras (la I y la J comparten casilla).",
               ["Sirve para el mensaje (carta 48).", "Es el cuadrado con el que se cifró la carta.", f"{_S_PLA}."], codigo("el cuadrado de la clave")),
    "53": gris("53", "La regla del cuadrado", "La regla para cifrar de dos en dos.",
               ["Sirve para el mensaje (carta 48).", "Es la regla de cifrar; hay que hacerla al revés para descifrar.", f"{_S_PLA}."], codigo("la regla del cuadrado")),
    "36": escena("36", "El carcelero", [52, 54, 55, 59], [32, 42, 48, 49, 53],
                 "La prisionera susurra por fin: «DRAGONES. Eso es lo que buscáis». Pero para salir del calabozo hay que pasar ante el carcelero, un hombretón que siempre gana a un juego de piedras a los que quieren pasar. En la mesa, las reglas y las partidas de otros que lo intentaron.",
                 ["Hay que ganar al carcelero. Las partidas de otros retadores son una pista."],
                 "El corredor de un calabozo medieval con un carcelero enorme de barba negra sentado ante una mesa con piedras, y unos papeles con partidas anotadas. Cristina observa las partidas con el dedo sobre la barbilla, pensativa; Alberto se arremanga con una sonrisa desafiante ante el carcelero."),
    "52": app("52", "El juego de las piedras", "Es un juego de la app: ganar al carcelero en el juego de las piedras, tomando 1, 2 o 3 por turno hasta llevarse la última.", 44,
              ["Las reglas, en la carta 54; las partidas de otros retadores, en la 55; el dicho del carcelero, en la 59.", "Mirad en las partidas cuántas piedras quedaban tras cada jugada del carcelero y qué tienen en común esos números.", f"{_S_PIE}."],
              SIN_GENTE + "Una mesa de madera con veintiuna piedras grises en fila, un cuenco y unas manos grandes de carcelero asomando."),
    "54": gris("54", "El juego de las piedras", "Las reglas del juego: veintiuna piedras, de 1 a 3 por turno, gana quien se lleva la última.",
               ["Sirve para el juego de las piedras (carta 52).", "Empieza el retador.", f"{_S_PIE}."], codigo("las reglas del juego de las piedras")),
    "55": gris("55", "Las partidas del carcelero", "Tres partidas del carcelero contra otros retadores, con las piedras que quedaban tras cada jugada.",
               ["Sirve para el juego de las piedras (carta 52).", "Mirad solo las piedras que quedan tras jugar el carcelero.", f"{_S_PIE}."], codigo("las partidas del carcelero")),
    "59": gris("59", "El dicho del carcelero", "Un dicho que repiten los guardias.",
               ["Sirve para el juego de las piedras (carta 52).", "Habla de contar de cuatro en cuatro.", f"{_S_PIE}."], codigo("el dicho del carcelero")),
    # ------------------------------------------------------------------ La biblioteca
    "44": escena("44", "La biblioteca del maestre", [33, 37, 39, 46, 51, 61, 63], [36, 52, 54, 55, 59],
                 "El carcelero se aparta con un gruñido y subís a la biblioteca del maestre, una sala redonda llena de libros con un gran mapa de castillos y, en la pared, un árbol de familia pintado. Dos puertas selladas con dos acertijos: el mapa de los castillos, con sus puentes por tender, y el árbol de la familia real, de quien depende quién se sienta en el trono. Las leyes del reino que os dio el senescal servirán aquí.",
                 ["Hay dos puzles: los castillos del reino y la sucesión. Las leyes del reino sirven aquí."],
                 "Una biblioteca circular de un castillo medieval con estanterías de libros hasta el techo, un gran mapa de castillos sobre una mesa y un árbol genealógico pintado en la pared. Cristina examina el árbol con una sonrisa de curiosidad, con el dedo siguiendo una de las ramas; Alberto estudia el mapa de los castillos con los ojos entornados."),
    "46": app("46", "Los castillos del reino", "Es un juego de la app: unir los castillos con puentes rectos, tantos como dice el número de cada uno, sin cruces y todos conectados.", 56,
              ["Los números, en el mapa de las cartas 37 y 39; el acertijo, en la 33.", "Empezad por los castillos con el número más alto o con pocos vecinos posibles: sus puentes se deducen.", f"Los puentes: {_S_HAS}."],
              SIN_GENTE + "Un mapa de castillos pequeños de piedra gris dibujados sobre una cuadrícula, unidos por puentes de madera rectos, sobre un fondo de nieve."),
    "37": pieza("37", "castillos", "Media lámina del mapa de los castillos del reino.", ["Es la mitad de un mapa: juntadla con la carta 39.", "Cada castillo lleva su número de puentes y una letra.", f"Los puentes: {_S_HAS}."]),
    "39": pieza("39", "castillos", "Media lámina del mapa de los castillos del reino.", ["Es la mitad de un mapa: juntadla con la carta 37.", "Cada castillo lleva su número de puentes y una letra.", f"Los puentes: {_S_HAS}."]),
    "33": gris("33", "El acertijo de los puentes", "Un acertijo grabado en el mapa del maestre.",
               ["Sirve para los castillos (carta 46).", "Los puentes van rectos, sin cruzarse, uno o dos entre cada par, y todos los castillos conectados.", f"Los puentes: {_S_HAS}."], codigo("el acertijo de los puentes")),
    "56": combinable("56", "Mitad del sello", "roja", 38, 94, "La otra mitad del sello de cera roja, con la cola del dragón, guardada en un hueco de la biblioteca.",
                     SIN_GENTE + "La otra mitad de un sello de cera roja con la cola de un dragón en relieve, partida por la mitad, sobre un atril de madera."),
    "51": app("51", "La sucesión", "Es un juego de la app: elegir quién hereda la corona de Piedra Negra según las leyes y el árbol de la familia real.", 58,
              ["Las leyes, en la carta 26; el árbol de la familia, en las cartas 61 y 63.", "Tachad primero a quien no puede heredar (muertos y septones) y después mirad la línea del hijo mayor.", f"{_S_SUC}."],
              SIN_GENTE + "Una corona de hierro con picos sobre un cojín de terciopelo, y un árbol genealógico pintado al fondo de una sala del trono."),
    "61": pieza("61", "arbol", "Media lámina del árbol del rey Aerion.", ["Es la mitad de un árbol: juntadla con la carta 63.", "Cada persona lleva su edad, su sexo y si ha muerto o tiene votos.", f"{_S_SUC}."]),
    "63": pieza("63", "arbol", "Media lámina del árbol del rey Aerion.", ["Es la mitad de un árbol: juntadla con la carta 61.", "Cada persona lleva su edad, su sexo y si ha muerto o tiene votos.", f"{_S_SUC}."]),
    "58": escena("58", "La verdad del trono", [69, 70, 71], [51, 61, 63, 26, 24],
                 "El consejo, reunido en la biblioteca, aclama al heredero. El maestre os guía ahora por una escalera oculta al piso de abajo, donde hay un tablero de ajedrez enorme con los escudos de las seis casas del reino, que se abre solo si se ponen todos en su sitio.",
                 ["Hay un tablero con los escudos de las casas."],
                 "Una sala de consejo medieval con nobles en pie que aclaman a un niño de unos nueve años con una pequeña corona, y una escalera de caracol que baja a un sótano. Cristina sonríe al niño con ternura; Alberto, a su lado, aplaude con una ceja levantada de sorpresa."),
    "69": app("69", "El tablero de las seis casas", "Es un juego de la app: colocar los seis escudos de las casas en cada fila, columna y recuadro sin repetir.", 80,
              ["El tablero, con los escudos ya puestos, son las cartas 70 y 71.", "Empezad por la fila, columna o recuadro que tenga más escudos y deducid el que falta.", f"{_S_SUD}."],
              SIN_GENTE + "Un tablero cuadrado de seis por seis casillas, con escudos de seis casas medievales (lobo, león, kraken, rosa, sol y trucha) en algunas casillas."),
    "70": pieza("70", "casas", "Media lámina del tablero de las seis casas.", ["Es la mitad de un tablero: juntadla con la carta 71.", "Los escudos ya puestos están en las casillas; las reglas, arriba.", f"{_S_SUD}."]),
    "71": pieza("71", "casas", "Media lámina del tablero de las seis casas.", ["Es la mitad de un tablero: juntadla con la carta 70.", "Los escudos ya puestos están en las casillas; las reglas, arriba.", f"{_S_SUD}."]),
    "80": escena("80", "Las criptas", [72, 75, 79], [58, 69, 70, 71],
                 "El tablero se abre y baja a unas criptas heladas, con el suelo cubierto de escarcha. Al fondo, una torre de hielo con cuatro discos de piedra que sostienen la corona del dragón: hay que llevarlos a otro pie de la torre antes de que se agote un reloj de arena.",
                 ["Las torres de hielo son otro puzle."],
                 "Unas criptas de piedra cubiertas de escarcha, iluminadas por antorchas azuladas, con tres torres de hielo y cuatro discos de piedra apilados en la primera. Cristina contempla las torres con el ceño fruncido y las manos en las caderas; Alberto se frota las manos heladas con aliento de vaho y una sonrisa nerviosa."),
    "72": app("72", "Las torres de hielo", "Es un juego de la app: llevar los cuatro discos de la torre I a la III, de uno en uno y sin poner uno grande sobre uno pequeño.", 82,
              ["Las torres, en la carta 75; las reglas y el reloj de arena, en la 79.", "El disco más pequeño se mueve cada dos movimientos, siempre en el mismo sentido. Para mover el mayor, los demás deben estar en la torre intermedia.", f"{_S_TOR}."],
              SIN_GENTE + "Tres torres de hielo con cuatro discos de piedra de tamaños distintos apilados en la primera, en una cripta helada."),
    "75": gris("75", "Las torres de hielo", "Las tres torres de la cripta y los cuatro discos de la corona, apilados en la primera.",
               ["Sirve para las torres (carta 72).", "El disco menor está arriba.", f"{_S_TOR}."], codigo("las torres de hielo")),
    "79": gris("79", "El reloj de arena", "Las reglas de la torre y el reloj de arena, con sus vueltas.",
               ["Sirve para las torres (carta 72).", "Cada movimiento es una vuelta del reloj, y solo da 15.", f"{_S_TOR}."], codigo("el reloj de arena")),
    "82": escena("82", "El altar de la profecía", [85, 86, 87], [80, 72, 75, 79],
                 "Los discos quedan en su sitio y la corona del dragón brilla sobre un altar de hielo. Pero el altar está protegido por una puerta con una profecía del maestre, un acertijo que pide números: «Cuatro cifras, cuatro pruebas». Para abrirla necesitáis las cifras que dejaron las pruebas que habéis superado.",
                 ["La puerta es el último puzle."],
                 "Un altar de hielo en una cripta con una corona de hierro oscuro de picos sobre un cojín y, detrás, una gran puerta de piedra con inscripciones. Cristina lee los acertijos de un pergamino con los labios moviéndose; Alberto cuenta con los dedos de una mano y un gesto de concentración."),
    "85": app("85", "La puerta de la profecía", "Es un juego de la app: la puerta se abre con el número que sale de una cuenta con las cifras de cuatro puzles resueltos.", 99,
              ["Los acertijos, en las cartas 86 y 87; cada puzle dijo su «cifra de la profecía» al resolverse.", "Cada acertijo describe un puzle por lo que hacía: lo que lleva cartas, lo que reparte hidromiel, lo que quita piedras, los ocho que vigilan.", f"La cuenta: {_S_PRO}."],
              SIN_GENTE + "Una puerta de piedra con un panel de dos ruedas de números talladas y un relieve de dragón dormido."),
    "86": gris("86", "La profecía del maestre (I)", "La primera parte de la profecía: dos de las cuatro pruebas.",
               ["Sirve para la puerta (carta 85).", "Dos pruebas: la del cuervo y la de las jarras.", f"La cuenta: {_S_PRO}."], codigo("la profecía, primera parte")),
    "87": gris("87", "La profecía del maestre (II)", "La segunda parte de la profecía: las otras dos pruebas y la cuenta.",
               ["Sirve para la puerta (carta 85).", "Dos pruebas: la de las piedras y la de los centinelas. Después, la cuenta.", f"La cuenta: {_S_PRO}."], codigo("la profecía, segunda parte")),
    # ------------------------------------------------------------------ La cripta del dragón y el final
    "94": escena("94", "La cripta del dragón", [64, 66, 67], [38, 56, 30, 44, 33, 37, 39, 46],
                 "Las dos mitades del sello se juntan en la puerta de la cripta con un chasquido y la puerta de bronce se abre. Dentro, un salón enorme y oscuro donde duerme un dragón de escamas rojas. Entre vosotros y él, un tapiz del sigilo: un dibujo que las tejedoras escondieron en números. Si se pinta bien, el dragón no se despierta. Las pistas, en dos cartas.",
                 ["Las pistas del tapiz son dos cartas: filas y columnas."],
                 "Un enorme salón de piedra oscura y fría con un dragón de escamas rojas dormido al fondo y un gran tapiz en la pared. Cristina da pasitos de puntillas con el dedo sobre los labios y los ojos como platos, y Alberto, tras ella, se tapa la boca con la mano para no hacer ruido, con cara de pánico."),
    "64": app("64", "El tapiz del sigilo", "Es un juego de la app: pintar el tapiz según los números de filas y columnas para que dibuje el sigilo del dragón.", 62,
              ["Las pistas de las filas, en la carta 66; las de las columnas, en la 67.", "Empezad por las filas o columnas con números grandes: dejan pocas posibilidades de colocación.", f"El tapiz, por filas (# pintada): {_S_TAP}."],
              SIN_GENTE + "Un gran tapiz de lana con un dibujo de cuadrícula y un dragón estilizado bordado en negro sobre fondo gris, colgado de una pared de piedra."),
    "66": gris("66", "El tapiz del sigilo (filas)", "Las pistas de las filas del tapiz.",
               ["Sirve para el tapiz (carta 64).", "Cada número es un grupo de casillas pintadas seguidas.", f"El tapiz, por filas (# pintada): {_S_TAP}."], codigo("las pistas de las filas")),
    "67": gris("67", "El tapiz del sigilo (columnas)", "Las pistas de las columnas del tapiz.",
               ["Sirve para el tapiz (carta 64).", "Cada número es un grupo de casillas pintadas seguidas.", f"El tapiz, por filas (# pintada): {_S_TAP}."], codigo("las pistas de las columnas")),
    "62": combinable("62", "Esquirla de dragón", "roja", 12, 74, "Una esquirla de piedra de fuego del tamaño de un puño, que cae de una escama del dragón y arde sin quemar.",
                     SIN_GENTE + "Una esquirla de piedra de fuego roja y naranja del tamaño de un puño, con una luz interior palpitante, sobre una palma con guante de cuero."),
    "74": escena("74", "Cronoportal reconectado", [], [62, 12, 64, 66, 67, 94, 57],
                 "La esquirla encaja en el anillo del Cronoportal, que se enciende de rojo a dorado. Pero el aparato aún no abre el portal: la puerta del altar de la profecía lo bloquea con su cuenta, una puerta que también cierra el último paso de la montaña. Hay que abrirla.",
                 ["Falta abrir la puerta de la profecía."],
                 "El Cronoportal con una esquirla de piedra de fuego encajada en su anillo agrietado, que brilla con luz roja y dorada en una cripta de hielo. Alberto ajusta los diales con la lengua entre los dientes y Cristina sostiene la corona de hierro con las dos manos, con gesto de asombro."),
    "99": escena("99", "De vuelta a casa (FIN)", [], [74, 82, 85, 86, 87],
                 "La puerta de piedra se abre y la luz de la corona baña la cripta. El anillo del Cronoportal pronuncia en voz alta una frase: «Solo el fuego vencerá al hielo del norte». El portal se abre en un estallido de luz justo cuando el dragón abre un ojo dorado y os mira, sin enfado. Cristina le dedica una reverencia. Aterrizáis en vuestro salón, con copos de nieve aún en el pelo. Alberto mira el aparato: «Mañana, otro destino». Cristina sonríe. FIN.",
                 [],
                 "La escena ocurre DENTRO del salón de su casa actual, en el presente (sofá, estanterías con libros, plantas, una lámpara encendida y luz cálida de tarde por la ventana): acaban de VOLVER a casa. Cristina y Alberto acaban de salir de un portal circular de luz azul y dorada que se abre detrás de ellos; a través del portal todavía se ve la cripta oscura con un dragón rojo que les mira con un ojo dorado. Llevan aún su ropa medieval de invierno con copos de nieve en el pelo y la capa. Cristina ríe con las manos en la boca, emocionada; Alberto mira el aparato con una sonrisa cansada y satisfecha. Están de cara a nosotros, aterrizando en el salón y alejándose del portal, que queda a su espalda y se está cerrando; el mundo de la aventura solo se ve a través del portal, detrás de ellos. No están entrando en el portal ni saliendo de casa: están llegando."),
}

META = dict(juego="Reino de Hielo y Fuego — La Corona del Dragón", estilo=ESTILO, personajes=PERSONAJES, hoja=HOJA, foto=FOTO, video=VIDEO,
            mosaicos={k: dict(filas=m["filas"], cols=m["cols"], cartas=m["cartas"], titulo=m["titulo"]) for k, m in MOSAICOS.items()})

SPEC = dict(final="99", needs={
    "24": ["14", "16"], "28": ["20", "18", "19", "21"], "57": ["22", "35"], "30": ["40", "41", "43", "45"], "36": ["48", "42", "49", "53"],
    "44": ["52", "54", "55", "59"], "56": ["46", "37", "39", "33"], "58": ["51", "26", "61", "63"], "80": ["69", "70", "71"], "94": ["38", "56"],
    "62": ["64", "66", "67"], "82": ["72", "75", "79"], "74": ["12", "62"], "99": ["85", "86", "87", "74"]}, eventos={})

PARA_QUE = {k: c["titulo"].split("— ", 1)[1] for k, c in J.items()}

_T = [
    ("leer", "P", "Llegada", "Pon el Modo PC (solo la P en la mesa) y en el móvil pulsa Empezar. Lee la carta P: coge la 10 y la 12."),
    ("leer", "10", "El patio de armas", "Lee la carta 10. Descarta la P y coge 14, 16, 18, 19, 20, 21 y 22. Junta la muralla: 19 arriba y 21 abajo."),
    ("app", "14", "Las jarras", f"En el móvil: Acción, 14. Con las jarras y el cuenco (16): {_S_JAR}. El mensaje te dice que cojas la 24. Anota la cifra de la profecía: {I.DATOS['14']}.", "carta 24"),
    ("leer", "24", "El senescal os cree", "Lee la carta 24. Descarta 14 y 16 y coge la 26 (guárdala para la sucesión)."),
    ("app", "20", "Los centinelas", f"En el móvil: Acción, 20. Con la muralla (19 y 21) y el acertijo (18): {_S_CEN}. El mensaje te dice que cojas la 28. Anota la cifra de la profecía: {I.DATOS['20']}.", "carta 28"),
    ("leer", "28", "La muralla", "Lee la carta 28. Descarta 18, 19, 20 y 21 y coge la 35."),
    ("combinar", "22", "35", "La antorcha", "La antorcha (22) y el pedernal (35) son combinables: 22 + 35 = 57. Coge la 57."),
    ("leer", "57", "La torre del maestre", "Lee la carta 57. Descarta 22, 35, 10 y 28 y coge 31 y 32."),
    ("leer", "31", "La torre de los cuervos", "Lee la carta 31. Coge 40, 41, 43 y 45."),
    ("app", "40", "Los cuervos", f"En el móvil: Acción, 40. Con el mapa (41), las leguas (43) y el acertijo (45): {_S_CUE}. El mensaje te dice que cojas la 30. Anota la cifra de la profecía: {I.DATOS['40']}.", "carta 30"),
    ("leer", "30", "El cuervo vuela", "Lee la carta 30. Descarta 31, 40, 41, 43 y 45 y coge la 38."),
    ("leer", "32", "El calabozo", "Lee la carta 32. Coge 42, 48, 49 y 53."),
    ("app", "48", "La carta de la prisionera", f"En el móvil: Acción, 48. Con la carta (42), el cuadrado (49) y la regla (53): {_S_PLA}. El mensaje te dice que cojas la 36.", "carta 36"),
    ("leer", "36", "El carcelero", "Lee la carta 36. Descarta 32, 42, 48, 49 y 53 y coge 52, 54, 55 y 59."),
    ("app", "52", "Las piedras", f"En el móvil: Acción, 52. Con las partidas (55) y el dicho (59): {_S_PIE}. El mensaje te dice que cojas la 44. Anota la cifra de la profecía: {I.DATOS['52']}.", "carta 44"),
    ("leer", "44", "La biblioteca del maestre", "Lee la carta 44. Descarta 36, 52, 54, 55 y 59 y coge 33, 37, 39, 46, 51, 61 y 63. Junta el mapa: 37 a la izquierda y 39 a la derecha; y el árbol: 61 a la izquierda y 63 a la derecha."),
    ("app", "46", "Los castillos", f"En el móvil: Acción, 46. Con el mapa (37 y 39) y el acertijo (33): {_S_HAS}. El mensaje te dice que cojas la 56.", "carta 56"),
    ("app", "51", "La sucesión", f"En el móvil: Acción, 51. Con las leyes (26) y el árbol (61 y 63): {_S_SUC}. El mensaje te dice que cojas la 58.", "carta 58"),
    ("leer", "58", "La verdad del trono", "Lee la carta 58. Descarta 51, 61, 63, 26 y 24 y coge 69, 70 y 71. Junta el tablero: 70 arriba y 71 abajo."),
    ("app", "69", "El tablero de las casas", f"En el móvil: Acción, 69. Con el tablero (70 y 71): {_S_SUD}. El mensaje te dice que cojas la 80.", "carta 80"),
    ("leer", "80", "Las criptas", "Lee la carta 80. Descarta 58, 69, 70 y 71 y coge 72, 75 y 79."),
    ("app", "72", "Las torres de hielo", f"En el móvil: Acción, 72. Con las torres (75) y el reloj de arena (79): {_S_TOR}. El mensaje te dice que cojas la 82.", "carta 82"),
    ("leer", "82", "El altar de la profecía", "Lee la carta 82. Descarta 80, 72, 75 y 79 y coge 85, 86 y 87."),
    ("combinar", "38", "56", "El sello", "Las dos mitades del sello (38 y 56) son combinables: 38 + 56 = 94. Coge la 94."),
    ("leer", "94", "La cripta del dragón", "Lee la carta 94. Descarta 38, 56, 30, 44, 33, 37, 39 y 46 y coge 64, 66 y 67."),
    ("app", "64", "El tapiz", f"En el móvil: Acción, 64. Con las filas (66) y las columnas (67): {_S_TAP}. El mensaje te dice que cojas la 62.", "carta 62"),
    ("combinar", "12", "62", "La esquirla", "El Cronoportal (12) y la esquirla (62) son combinables: 12 + 62 = 74. Coge la 74."),
    ("leer", "74", "Cronoportal reconectado", "Lee la carta 74. Descarta 62, 12, 64, 66, 67, 94 y 57."),
    ("app", "85", "La puerta", f"En el móvil: Acción, 85. Con las cifras de las pruebas y los acertijos (86 y 87): {_S_PRO}. El mensaje te dice que cojas la 99.", "carta 99"),
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
