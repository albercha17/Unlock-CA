"""Dry Gulch, 1878: El Tren del Oro — versión de 60 cartas (22 oct 2026), mucho más difícil y variada.

Once puzles de tipos que no salen en ningún otro juego de la serie, con las pistas dibujadas o en acertijo (ninguna carta explica cómo se
resuelve su puzle): un telegrama en zigzag (cifrado de la valla), un cuadro de Hitori, un tablero de pentominós, un cuadro de Kakuro, la carga de
un carro (mochila), un duelo en corro (problema de Josefo), una bodega de barriles (Sokoban), una bomba de agua (tuberías giratorias), una maniobra
de vagones con apartadero, unos hierros de ganado (simetrías) y una válvula final con el cuadrado de Polibio y cinco coordenadas que dejan otros
puzles. Solo 16 cartas tienen a Cristina y Alberto (escenas); el resto son objetos y pistas sin personas. Las cartas-pista las dibuja
herramientas/oeste_cartas.py (instancias_oeste.py)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ampliacion as _amp  # noqa: E402
import instancias_oeste as I  # noqa: E402

ESTILO = ("Ilustración pictórica semirrealista con aire de película del Oeste (western clásico y spaghetti western), luz dorada y polvorienta de atardecer, tonos ocres, rojos y azules "
          "pálidos, pueblo de madera con saloon, estación de tren, mina y desierto con mesetas al fondo, formato vertical 2:3. Sin texto, letras ni números legibles en la imagen; los carteles, "
          "papeles y letreros solo muestran rayas decorativas. Deja libre de detalles importantes la esquina superior izquierda y el 18 % inferior de la imagen. "
          "Los personajes tienen siempre expresiones distintas y expresivas, adecuadas a la escena (nunca la misma cara en dos imágenes).")

PERSONAJES = {
    "Cristina": "Cristina, mujer de 26 años, profesora, pelo rubio y rizado con trenza lateral, ojos azules. Viste ropa del Oeste de 1878: camisa de cuadros con las mangas remangadas, falda larga de lona marrón, chaleco de cuero, pañuelo rojo al cuello, botas y un sombrero vaquero de ala ancha colgado a la espalda.",
    "Alberto": "Alberto, hombre de 27 años, informático, pelo moreno corto, barba cuidada, ojos marrones. Viste ropa del Oeste de 1878: camisa blanca remangada, chaleco de cuero, pañuelo azul al cuello, pantalones de lona, cinturón con hebilla grande, botas con espuelas y un sombrero marrón de ala ancha.",
}

HOJA = ("Crea una hoja de personajes (character sheet) con las dos personas de la foto adjunta, de cuerpo entero y de frente, sobre fondo claro y neutro. "
        "Mantén su parecido real con la foto (cara, pelo, barba, ojos). "
        "Cristina: mujer de 26 años, profesora, pelo rubio y rizado con trenza lateral, ojos azules, camisa de cuadros con las mangas remangadas, falda larga de lona marrón, chaleco de cuero, pañuelo rojo al cuello, botas y sombrero vaquero colgado a la espalda. "
        "Alberto: hombre de 27 años, informático, pelo moreno corto, barba cuidada, ojos marrones, camisa blanca remangada, chaleco de cuero, pañuelo azul al cuello, pantalones de lona, cinturón con hebilla grande, botas con espuelas y sombrero marrón de ala ancha. "
        "Estilo: " + ESTILO)

FOTO = ("Antes de nada, adjunta a ChatGPT una foto de Cristina y Alberto juntos (o una de cada uno, con la cara bien visible). "
        "Pídele que mantenga el parecido real, pero con el estilo de ilustración de este juego.")

VIDEO = ("Crea un vídeo vertical 9:16 de 15 segundos, con estilo cinematográfico de western clásico, luz dorada de atardecer y mucho polvo en el aire. Sin ningún texto, letra ni subtítulo en pantalla. "
         "Escena 1 (0-4 s): en el salón de una casa actual, Cristina (mujer de 26 años, rubia de pelo rizado, ojos azules) y Alberto (hombre de 27 años, moreno con barba, ojos marrones) rodean un aparato de latón y cristal con un anillo central: el Cronoportal. Cristina señala una foto antigua de un tren de vapor en un libro. "
         "Escena 2 (4-8 s): el anillo se enciende con un arco de luz azul y dorada y los dos son absorbidos por un túnel de luz. "
         "Escena 3 (8-12 s): caen sobre el apartadero de una estación del Oeste en 1878, entre barriles y sacos; el aparato golpea un barril y su cristal sale rodando mientras un jinete con pañuelo en la cara huye a galope. "
         "Escena 4 (12-15 s): primer plano de Cristina y Alberto, con ropa del Oeste, asombrados, mirando cómo se aleja el jinete entre una nube de polvo; fundido a negro. "
         "Sonido: zumbido eléctrico creciente, silbido del portal, golpe sordo al aterrizar, silbato de tren, galope y armónica con guitarra, sin voz de narrador.")

ESTILO += " Los personajes tienen siempre expresiones distintas y expresivas, adecuadas a la escena (nunca la misma cara en dos imágenes)."
SIN_GENTE = "Sin ninguna persona en la imagen. "

MOSAICOS = {
    "banco": dict(filas=2, cols=1, cartas=["19", "21"], titulo="El cuadro del banco"),
    "caja": dict(filas=1, cols=2, cartas=["41", "43"], titulo="La caja del carro"),
    "apuestas": dict(filas=1, cols=2, cartas=["42", "49"], titulo="El cuadro de apuestas"),
    "bodega": dict(filas=1, cols=2, cartas=["61", "63"], titulo="El suelo de la bodega"),
    "bomba": dict(filas=2, cols=1, cartas=["66", "67"], titulo="El plano de la bomba"),
}
POS = {(2, 1): ["mitad de arriba", "mitad de abajo"], (1, 2): ["mitad izquierda", "mitad derecha"]}

_TUBO = {0: " ", 1: "╹", 2: "╺", 3: "┗", 4: "╻", 5: "┃", 6: "┏", 7: "┣", 8: "╸", 9: "┛", 10: "━", 11: "┻", 12: "┓", 13: "┫", 14: "┳", 15: "╋"}
_S_VAL = I.VALLAS["claro"]
_S_HIT = "; ".join(f"fila {r + 1}: " + (", ".join(f"columna {c + 1}" for c, v in enumerate(f) if v) or "ninguno") for r, f in enumerate(I.HITORI["tachones"]))


def _grid_pentomino():
    g = [["."] * I.PENTOMINO["cols"] for _ in range(I.PENTOMINO["filas"])]
    for k, letra in enumerate(I.PENTOMINO["piezas"]):
        for r, c in I.PENTOMINO["solucion"][letra]:
            g[r][c] = "ABCDEF"[k]
    return " / ".join("".join(f) for f in g)


def _grid_kakuro():
    g = {tuple(map(int, k.split(","))): v for k, v in I.KAKURO["solucion"].items()}
    return " / ".join("fila " + str(r + 1) + ": " + " ".join(str(g[(r, c)]) if (r, c) in g else "-" for c in range(I.KAKURO["n"])) for r in range(I.KAKURO["n"]))


_S_PEN = _grid_pentomino()
_S_KAK = _grid_kakuro()
_S_MOC = ", ".join(["barril de whisky", "saco de harina", "caja de herramientas", "fardo de pieles", "cajón de balas", "rollo de alambre", "bidón de petróleo", "baúl de plata"][i] for i in I.MOCHILA["solucion"])
_S_JOS = f"el asiento {I.JOSEFO['sobrevive']}"
_S_SOK = I.SOKOBAN["solucion"]
_S_TUB = " / ".join("".join(_TUBO[m] for m in f) for f in I.TUBERIAS["solucion"])
_S_VAG = I.VAGONES["ops"]
_S_HIE = ", ".join(str(i + 1) for i in I.HIERROS["autenticos"])
_S_POL = " ".join(I.COORD[k] for k in I.ORDEN)


def codigo(que):
    return f"Carta dibujada por código (herramientas/oeste_cartas.py; no se pide a ChatGPT): {que}."


def pieza(carta, mosaico, que, pistas):
    m = MOSAICOS[mosaico]
    i = m["cartas"].index(carta)
    pos = POS[(m["filas"], m["cols"])][i]
    return dict(titulo=f"Carta {carta} — {m['titulo']} ({pos})", tipo="gris",
                mosaico=dict(id=mosaico, filas=m["filas"], cols=m["cols"], fila=i // m["cols"], col=i % m["cols"]),
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
    # ------------------------------------------------------------------ La estación
    "P": escena("P", "Llegada a Dry Gulch", [10, 12], [],
                "Novena parada del Cronoportal: Dry Gulch, un pueblo del Lejano Oeste en 1878. Cristina lleva años soñando con cabalgar por un western de verdad. El salto vuelve a salir mal: aterrizáis en el apartadero de la estación, el aparato golpea un barril y su cristal de energía sale rodando. Un jinete con un pañuelo en la cara, que cree haber encontrado una joya, lo recoge sin bajarse del caballo y huye al galope hacia el tren del oro, que sale dentro de hora y media. Sin el cristal, no hay regreso.",
                ["Mirad a vuestro alrededor y revisad el aparato."],
                "El apartadero de una estación del Lejano Oeste en 1878, al atardecer, entre barriles y sacos, con una locomotora de vapor al fondo. En primer plano, un aparato de latón y cristal (el Cronoportal) humea sin su cristal central, y a lo lejos un jinete con pañuelo en la cara se aleja al galope entre una nube de polvo. Cristina, con camisa de cuadros y sombrero vaquero colgado a la espalda, levanta un puño y grita con rabia; Alberto, con pañuelo azul, se agarra la cabeza con las dos manos."),
    "10": escena("10", "La estación de Dry Gulch", [14, 16, 18, 19, 20, 21, 22], ["P"],
                 "La estación es un hervidero. En la oficina de telégrafos, un telegrama urgente en un papel sin sentido (carta 14) con el aviso del telegrafista (carta 16). En la ventanilla del banco, el acertijo del banquero (carta 18) y el cuadro de números que cuelga tras la reja, que ocupa dos láminas: juntad la 19 arriba y la 21 abajo (carta 20). Sobre el mostrador del sheriff, media estrella de latón (carta 22).",
                 ["Hay dos puzles: el telegrama y el cuadro del banco.", "El cuadro son dos cartas: juntadlas, una encima de otra."],
                 "El interior de una estación del Lejano Oeste con una oficina de telégrafos con una ventanilla y un telégrafo, una reja de banco con un cuadro de cifras colgado al fondo y un mostrador de madera con media estrella de sheriff de latón. Cristina lee un telegrama con una ceja levantada de extrañeza; Alberto mira el cuadro del banco con la boca abierta."),
    "12": combinable("12", "Cronoportal sin cristal", "azul", 62, 74,
                     "El Cronoportal con el anillo central apagado: le falta el cristal que se llevó el jinete.",
                     SIN_GENTE + "Primer plano del Cronoportal: una consola portátil de latón y cristal con dos antenas de cobre, un anillo central apagado y un hueco circular vacío en el pecho del aparato, sobre un barril de madera, con polvo del desierto."),
    "14": app("14", "El telegrama en zigzag", "Es un juego de la app: el telegrafista escribió el mensaje bajando y subiendo por cuatro rieles y luego lo leyó por pisos. Hay que escribir el mensaje original.", 24,
              ["El telegrama está en la carta 16, con el zigzag dibujado.", "Hay cuatro rieles. Contad cuántas letras caen en cada riel, y colocadlas por pisos: el primer piso se lee primero, luego el segundo...", f"El mensaje dice: {_S_VAL}. Coordenada de Polibio: {I.COORD['14']}."],
              SIN_GENTE + "Una oficina de telégrafos del Oeste con un telégrafo de latón y una cinta de papel, una tira de telegrama con letras sin sentido y un lápiz, con luz de quinqué."),
    "16": gris("16", "El telegrama", "Un telegrama urgente, con el mensaje en grupos de cinco letras, y un zigzag de cuatro rieles dibujado debajo.",
               ["Es el mensaje del telegrama (carta 14).", "El zigzag tiene cuatro rieles: baja y sube.", "El mensaje se escribió siguiendo el zigzag y se leyó piso por piso."]),
    "18": gris("18", "El acertijo del banquero", "Un acertijo colgado en la ventanilla del banco.",
               ["Es la regla del cuadro del banco (carta 20).", "No puede quedar ninguna cifra repetida en su fila ni en su columna, tachando las que sobran.", "Dos manchas no pueden tocarse por un lado, y las casillas en blanco han de estar todas unidas."]),
    "19": pieza("19", "banco", "Media lámina del cuadro del banco.", ["Es la mitad de una lámina: juntadla con la carta 21.", "Es un cuadro de cinco por cinco cifras.", "Hay que tachar las cifras sobrantes (carta 18)."]),
    "21": pieza("21", "banco", "Media lámina del cuadro del banco.", ["Es la mitad de una lámina: juntadla con la carta 19.", "Es un cuadro de cinco por cinco cifras.", "Hay que tachar las cifras sobrantes (carta 18)."]),
    "20": app("20", "El cuadro del banquero", "Es un juego de la app: el cuadro de cifras de la reja del banco; hay que tachar las que sobran para que no quede ninguna repetida en su fila ni en su columna.", 28,
              ["Las cifras están en las cartas 19 y 21 y la regla, en la 18.", "Si una cifra aparece dos veces en una fila, una de las dos hay que tacharla. Dos tachones no pueden tocarse y lo blanco ha de quedar unido.", f"Los tachones: {_S_HIT}."],
              SIN_GENTE + "Una reja de banco del Oeste con un cuadro de cifras escritas en tiza colgado tras ella, un mostrador de madera y una caja fuerte entreabierta, con luz de quinqué."),
    "22": combinable("22", "Media estrella", "azul", 35, 57, "Una mitad de una estrella de sheriff de latón, con cinco puntas.",
                     SIN_GENTE + "La mitad izquierda de una estrella de sheriff de latón con cinco puntas, sobre un mostrador de madera con polvo del desierto."),
    "24": escena("24", "El telégrafo habla", [26], [14, 16],
                 "El telegrafista lee el mensaje y se pone pálido: avisa del jinete que se llevó el cristal. Mientras tanto, entre las cintas del telégrafo aparece un papel doblado con un refrán que el tabernero grabó a fuego en un barril de su bodega (carta 26). Una pareja de cifras se queda grabada en la cinta: guardadla, el telegrafista la usa para abrir la válvula de la locomotora.",
                 ["Mirad entre las cintas del telégrafo."],
                 "Un telegrafista del Oeste con visera verde y manguitos leyendo una cinta de telégrafo con la boca abierta de sorpresa, y entre las cintas, un papel doblado. Cristina señala el papel con una sonrisa de triunfo; Alberto tiene la oreja pegada al telégrafo y los ojos en blanco de concentración."),
    "26": gris("26", "El refrán del tabernero", "Un refrán grabado a fuego en un barril.",
               ["Habla de cómo se mueven los barriles de la bodega (carta 51).", "Los barriles solo se empujan, de uno en uno.", "Los huecos del suelo están dibujados en las cartas 61 y 63."]),
    "28": escena("28", "La reja abierta", [35], [18, 19, 20, 21],
                 "El banquero abre la reja y deja ver la caja del banco. Dentro, junto a unas monedas, la otra mitad de la estrella de sheriff (carta 35).",
                 ["Mirad dentro de la caja del banco."],
                 "Un banquero con visera y chaleco abriendo una reja de banco que deja ver una caja fuerte con monedas y media estrella de sheriff de latón brillando dentro. Cristina la coge con cara de asombro y los ojos muy abiertos; Alberto da un puñetazo al aire de alegría."),
    "35": combinable("35", "Otra media estrella", "roja", 22, 57, "La otra mitad de la estrella de sheriff, con las otras cinco puntas.",
                     SIN_GENTE + "La mitad derecha de una estrella de sheriff de latón con cinco puntas, sobre un fondo de monedas de plata."),
    "57": escena("57", "La estrella del sheriff", [31, 32], [22, 35, 10, 28],
                 "Juntáis las dos mitades y la estrella os convierte en ayudantes del sheriff: el pueblo entero os abre sus puertas. A la izquierda, el patio del carretero, con su carro y una caja por llenar (carta 31). A la derecha, el saloon, con una mesa de apuestas (carta 32).",
                 ["Dos sitios: el patio del carretero y el saloon."],
                 "Cristina y Alberto con una estrella de sheriff de latón completa prendida en el chaleco, en la calle principal de un pueblo del Lejano Oeste, con un patio con un carro a la izquierda y las puertas batientes de un saloon a la derecha. Cristina se la señala con orgullo y una gran sonrisa; Alberto se pone un sombrero de ala ancha con aire de duro."),
    # ------------------------------------------------------------------ Rama 1: el patio del carretero
    "31": escena("31", "El patio del carretero", [40, 41, 43, 45], [],
                 "Un patio de tierra con un carro sin ruedas y una caja de madera enorme sin llenar (carta 40). El tablero de la caja, con dos piezas ya puestas, ocupa dos láminas: juntad la 41 a la izquierda y la 43 a la derecha. Colgadas de un clavo, las seis piezas de carga que hay que encajar (carta 45).",
                 ["Un único puzle: llenar la caja del carro."],
                 "Un patio de tierra con un carro del Oeste sin ruedas y una enorme caja de madera de fondo plano, con seis piezas de madera de formas distintas colgadas de un clavo. Cristina estudia las piezas con la cabeza ladeada; Alberto se rasca la barbilla pensando."),
    "40": app("40", "La caja del carro", "Es un juego de la app: llenar una caja de cinco por seis casillas con seis piezas de cinco cuadros, cada una una sola vez, giradas o dadas la vuelta como haga falta.", 30,
              ["El tablero con dos piezas ya puestas está en las cartas 41 y 43 y las seis piezas, en la 45.", "Las dos piezas puestas marcan por dónde empezar. Colocad primero las piezas más raras (la que parece una zeta o una pe).", f"Por filas, con las letras de las piezas: {_S_PEN}. Coordenada de Polibio: {I.COORD['40']}."],
              SIN_GENTE + "Una caja de madera enorme de fondo plano, llena a medias de piezas de madera de formas distintas de cinco cuadros encajadas como un puzle, con serrín en el suelo y luz de atardecer."),
    "41": pieza("41", "caja", "Media lámina del tablero de la caja del carro.", ["Es la mitad de una lámina: juntadla con la carta 43.", "Dos piezas están ya puestas en el tablero.", "Las seis piezas están en la carta 45."]),
    "43": pieza("43", "caja", "Media lámina del tablero de la caja del carro.", ["Es la mitad de una lámina: juntadla con la carta 41.", "Dos piezas están ya puestas en el tablero.", "Las seis piezas están en la carta 45."]),
    "45": gris("45", "Las seis piezas", "Las seis piezas de cinco cuadros de la carga del carro.", ["Son las piezas del puzle de la caja (carta 40).", "Se pueden girar y dar la vuelta.", "Cada pieza se usa una sola vez."]),
    "30": escena("30", "La caja cerrada", [38], [31, 40, 41, 43, 45],
                 "La caja queda llena y la tapa se cierra sola. Debajo, pegada al fondo de madera, la mitad de una llave de hierro (carta 38). Una pareja de cifras queda grabada en la tapa: guardadla.",
                 ["Mirad debajo de la caja."],
                 "Una caja de madera enorme cerrada, con la tapa encajada, y debajo, pegada a la madera, la mitad de una llave de hierro grande. Cristina la despega con cuidado y los labios apretados; Alberto sonríe de oreja a oreja."),
    "38": combinable("38", "Mitad de la llave del furgón", "roja", 56, 94, "Una mitad de una llave de hierro, grande y pesada, de las de los furgones blindados.",
                     SIN_GENTE + "La mitad izquierda de una llave de hierro grande y pesada, de las de los furgones blindados de tren, sobre una tabla de madera."),
    # ------------------------------------------------------------------ Rama 2: el saloon
    "32": escena("32", "El saloon", [42, 48, 49, 53], [],
                 "En el saloon, una mesa de apuestas con un tahúr que reparte cartas. Sobre la mesa, el cuadro de apuestas del tahúr (carta 48), que ocupa dos láminas: juntad la 42 a la izquierda y la 49 a la derecha. En el reverso de una baraja, la regla del tahúr (carta 53).",
                 ["Un único puzle: el cuadro de apuestas."],
                 "El interior de un saloon del Oeste con una mesa de póker de fieltro verde, un tahúr con visera repartiendo cartas y un cuadro de sumas escrito con tiza en una pizarra. Cristina mira las cartas con los ojos entrecerrados; Alberto, de brazos cruzados, sigue las sumas con la vista."),
    "48": app("48", "El cuadro de apuestas", "Es un juego de la app: rellenar con cifras del 1 al 9 un cuadro de apuestas para que cada racha, hacia la derecha o hacia abajo, sume lo que dice su número y no repita cifra.", 36,
              ["El cuadro con los números está en las cartas 42 y 49 y la regla, en la 53.", "Empezad por las rachas de dos casillas con sumas extremas (3, 4, 16 o 17): solo tienen una descomposición.", f"Solución: {_S_KAK}."],
              SIN_GENTE + "Una pizarra de un saloon con un cuadro de casillas con sumas escritas con tiza, una mesa de póker y una baraja desparramada, con luz de quinqué."),
    "42": pieza("42", "apuestas", "Media lámina del cuadro de apuestas.", ["Es la mitad de una lámina: juntadla con la carta 49.", "Los números en las casillas oscuras son las sumas.", "La regla del tahúr está en la carta 53."]),
    "49": pieza("49", "apuestas", "Media lámina del cuadro de apuestas.", ["Es la mitad de una lámina: juntadla con la carta 42.", "Los números en las casillas oscuras son las sumas.", "La regla del tahúr está en la carta 53."]),
    "53": gris("53", "La regla del tahúr", "Una nota en el reverso de una baraja con la regla del cuadro de apuestas.", ["Explica cómo se rellena el cuadro (carta 48).", "Son cifras del 1 al 9.", "En una misma racha no se repite ninguna cifra."]),
    "36": escena("36", "El almacén del tendero", [52, 54, 55, 59], [32, 42, 48, 49, 53],
                 "El tahúr recoge sus cartas y os deja pasar al almacén del tendero de al lado. Hay que cargar el carro del abuelo con lo que más valga sin romper el eje (carta 52). Las listas del herrador y del tendero, con lo que pesa y lo que vale cada cosa, están en dos hojas (cartas 54 y 55), y la nota del carretero, en la 59.",
                 ["Un único puzle: cargar el carro."],
                 "El almacén de un tendero del Oeste lleno de barriles, sacos, cajas y fardos hasta el techo, con un carro viejo de madera en la puerta, y el tendero detrás del mostrador con un lápiz en la oreja. Cristina levanta un saco con una mueca de esfuerzo; Alberto cuenta con los dedos las cosas del almacén con aire de concentración."),
    "52": app("52", "La carga del carro", "Es un juego de la app: elegir qué cosas cargar, una vez cada una, para llevar el mayor valor sin pasar el peso que aguanta el eje.", 44,
              ["Los pesos están en la carta 54, los valores en la 55 y lo que aguanta el eje, en la 59.", "No sirve cargar siempre lo que más vale ni lo que mejor sale por peso: la mejor carga es otra.", f"La mejor carga: {_S_MOC}. Coordenada de Polibio: {I.COORD['52']}."],
              SIN_GENTE + "Un carro viejo de madera, de eje fino, cargado a medias con barriles, sacos y cajas, ante la puerta de un almacén del Oeste, con luz de atardecer."),
    "54": gris("54", "Lo que pesa cada cosa", "La lista del herrador con el peso de cada cosa, en arrobas.", ["Son los pesos de las ocho cosas del almacén.", "Cada cosa lleva su color.", "El peso que aguanta el eje está en la carta 59."]),
    "55": gris("55", "Lo que vale cada cosa", "La lista del tendero con el valor de cada cosa, en dólares.", ["Son los valores de las ocho cosas del almacén.", "Cada cosa lleva su color.", "El peso que aguanta el eje está en la carta 59."]),
    "59": gris("59", "El carro del abuelo", "Una nota del carretero: hasta dónde aguanta el eje.", ["Dice cuánto aguanta el eje.", "Pasado ese peso, el eje se rompe.", "Hay que llevar el mayor valor posible."]),
    # ------------------------------------------------------------------ La plaza y la estación
    "44": escena("44", "La plaza de Dry Gulch", [33, 37, 39, 46, 51, 61, 63], [36, 52, 54, 55, 59],
                 "El carro sale cargado y llegáis a la plaza. Diecisiete pistoleros se han sentado en corro a la mesa del saloon para un duelo a muerte (carta 46): el corro está en la carta 37 y la regla de la cuenta, en las cartas 39 y 33. Al otro lado, la bodega del tabernero, con tres barriles que hay que meter en su sitio (carta 51), cuyo suelo ocupa dos láminas: juntad la 61 a la izquierda y la 63 a la derecha.",
                 ["Hay dos puzles: el duelo en corro y la bodega."],
                 "La plaza de un pueblo del Lejano Oeste, con una mesa redonda en el centro rodeada de diecisiete pistoleros sentados y, al fondo, la puerta de una bodega con barriles apilados. Cristina, con una mano en la cadera, observa el corro con ojos desorbitados; Alberto se muerde el labio sin quitar ojo a la bodega."),
    "46": app("46", "El duelo en corro", "Es un juego de la app: diecisiete pistoleros en corro, numerados; cae cada cuarto y la cuenta sigue desde el siguiente. Hay que sentarse en el asiento del último que queda en pie.", 56,
              ["El corro está en la carta 37 y la regla de la cuenta, en las cartas 39 y 33.", "Contad desde el sombrero rojo, de cuatro en cuatro, y tachad al que cae. Seguid desde el siguiente tras cada caída.", f"El último que queda es {_S_JOS}."],
              SIN_GENTE + "Una mesa redonda de saloon vista desde arriba, con diecisiete sillas alrededor, y un sombrero rojo sobre una de ellas, con luz de quinqué."),
    "37": gris("37", "El corro de pistoleros", "Los diecisiete pistoleros, sentados en corro, con su número.", ["Son los asientos del duelo (carta 46).", "El sombrero rojo marca el uno.", "Los números crecen hacia la derecha."]),
    "39": gris("39", "La cuenta del sheriff", "La regla de la cuenta del duelo, del libro del sheriff.", ["Explica cómo cae un pistolero en cada ronda.", "Se cuenta desde el sombrero rojo, hacia la derecha.", "Cae cada cuarto número; la cuenta sigue desde el siguiente."]),
    "33": gris("33", "La nota del juez", "Una nota del juez clavada en la puerta.", ["Explica cuándo termina el duelo.", "Termina cuando solo queda uno.", "Quien queda se lleva el botín."]),
    "56": combinable("56", "Otra mitad de la llave", "roja", 38, 94, "La otra mitad de la llave del furgón, que el juez os entrega al terminar el duelo.",
                     SIN_GENTE + "La mitad derecha de una llave de hierro grande y pesada, de las de los furgones blindados de tren, que un juez con sombrero negro entrega con la mano."),
    "51": app("51", "La bodega de barriles", "Es un juego de la app: empujar tres barriles hasta sus huecos del suelo de la bodega del tabernero, de uno en uno y siempre hacia delante.", 58,
              ["El refrán del tabernero está en la carta 26 y los huecos del suelo, en las cartas 61 y 63.", "Los huecos no se ven en la app: están dibujados solo en las cartas. Empujad primero el barril que está pegado a la pared.", f"Una solución en {I.SOKOBAN['minimo']} pasos (U arriba, D abajo, L izquierda, R derecha): {_S_SOK}. Coordenada de Polibio: {I.COORD['51']}."],
              SIN_GENTE + "El interior de la bodega de una taberna del Oeste, con barriles de madera apilados contra una pared, el suelo de tablas con tres huecos cuadrados y una lámpara de aceite."),
    "61": pieza("61", "bodega", "Media lámina del suelo de la bodega.", ["Es la mitad de una lámina: juntadla con la carta 63.", "Los huecos oscuros son los sitios de los barriles.", "El refrán está en la carta 26."]),
    "63": pieza("63", "bodega", "Media lámina del suelo de la bodega.", ["Es la mitad de una lámina: juntadla con la carta 61.", "Los huecos oscuros son los sitios de los barriles.", "El refrán está en la carta 26."]),
    "58": escena("58", "El apartadero", [69, 70, 71], [51, 61, 63, 26, 24],
                 "Los tres barriles encajan y bajo el suelo de la bodega aparece un pasadizo que sale al apartadero de la estación. Allí hay siete vagones de colores en fila que bloquean la vía de la locomotora (carta 69). El peso de cada color está en una hoja pegada al furgón (carta 70) y la regla de la maniobra, en un cartel del jefe de estación (carta 71).",
                 ["Un único puzle: ordenar los vagones con el apartadero."],
                 "El apartadero de una estación del Oeste con siete vagones de colores distintos en fila, una vía muerta a un lado, y una locomotora de vapor al fondo. Cristina, con las manos en jarras, mira los vagones con una ceja levantada; Alberto se rasca la nuca mirando la vía muerta."),
    "69": app("69", "La maniobra de vagones", "Es un juego de la app: siete vagones de colores esperan en fila; hay un apartadero ciego y el tren tiene que salir ordenado del más ligero al más pesado.", 80,
              ["Los pesos de cada color están en la carta 70 y la regla, en la 71.", "El último vagón que entra al apartadero es el primero que sale. Metéis vagones hasta que el siguiente que necesitáis es el de arriba del apartadero, y entonces lo sacáis.", f"Una maniobra (E entrar, S sacar): {_S_VAG}. Coordenada de Polibio: {I.COORD['69']}."],
              SIN_GENTE + "Una vía de estación del Oeste con siete vagones de colores distintos en fila, una vía muerta a un lado a modo de apartadero y una locomotora de vapor al fondo, con luz de atardecer."),
    "70": gris("70", "Los vagones de la estación", "Los siete vagones de la estación, con su color y su peso en toneladas.", ["Son los pesos de los vagones (carta 69).", "Cada vagón lleva su color.", "El orden de la fila es el orden de llegada."]),
    "71": gris("71", "La maniobra", "Un cartel del jefe de estación con la regla de la maniobra.", ["Explica cómo funciona el apartadero.", "El último que entra es el primero que sale.", "El tren sale del más ligero al más pesado."]),
    "80": escena("80", "El despacho del jefe de estación", [72, 75, 79], [58, 69, 70, 71],
                 "El tren queda ordenado y el jefe de estación os deja pasar a su despacho. Una carta del ganadero Don Abel le pide ayuda: unos ladrones le han marcado las reses con hierros falsos y las han vendido en la subasta. Hay que reconocer qué reses son suyas (carta 72). Las ocho marcas, en el cartel de la subasta (carta 75), y el hierro verdadero, grabado en la puerta de Don Abel (carta 79).",
                 ["Un único puzle: reconocer los hierros de Don Abel."],
                 "El despacho de un jefe de estación del Oeste, con un escritorio de madera, un reloj de pared, un cartel de subasta de ganado clavado a la pared y una carta abierta sobre la mesa. Cristina lee la carta con la boca entreabierta; Alberto, con un dedo en el cartel, parece indignado."),
    "72": app("72", "Los hierros del ganado", "Es un juego de la app: de ocho reses de la subasta, marcar las que llevan el hierro de Don Abel, visto derecho, de lado, boca abajo o en espejo; los falsos cambian un solo cuadrito.", 82,
              ["Las ocho marcas están en la carta 75 y el hierro de Don Abel, en la 79.", "Girad y dad la vuelta mentalmente al hierro de Don Abel. Los falsos tienen un cuadrito de más o de menos.", f"Son las reses {_S_HIE}."],
              SIN_GENTE + "Un cuero de vaca con una marca a fuego en forma de cuadrícula de cuadritos, junto a un hierro de marcar de hierro candente, sobre una cerca de madera de un corral, con luz de atardecer."),
    "75": gris("75", "Los hierros de la subasta", "El cartel de la subasta, con las ocho marcas a fuego de las reses.", ["Son las ocho marcas de las reses (carta 72).", "Cada marca lleva su número.", "El hierro de Don Abel está en la carta 79."]),
    "79": gris("79", "El hierro de Don Abel", "El hierro de Don Abel, grabado a fuego en su puerta, con un refrán.", ["Es el hierro verdadero (carta 72).", "Los hierros auténticos son el mismo hierro de otro modo.", "Los falsos cambian un solo cuadrito."]),
    "82": escena("82", "La locomotora", [85, 86, 87], [80, 72, 75, 79],
                 "Don Abel recupera sus reses y os acompaña a la locomotora del tren del oro. La válvula de vapor está cerrada y se abre con una palabra que el telegrafista guardó en cinco coordenadas, las que os dejaron cinco de vuestros puzles (carta 85). Dos hojas explican en qué orden están (carta 86) y cómo se leen (carta 87).",
                 ["Un único puzle: abrir la válvula de la locomotora."],
                 "El interior de la cabina de una locomotora de vapor del Oeste, con una caldera, un panel de manómetros y una gran válvula de bronce con un cierre de combinación. Cristina, con las manos negras de hollín, mira la válvula con los labios apretados; Alberto, a su lado, se limpia el sudor de la frente y observa."),
    "85": app("85", "La válvula de la locomotora", "Es un juego de la app: cinco coordenadas de Polibio, las que dejaron otros cinco puzles, forman una palabra con el cuadrado de la carta 87.", 99,
              ["Las coordenadas son las que anotasteis tras el telegrama, la caja, el carro, la maniobra y la bodega. El orden, en la carta 86, y el cuadrado, en la 87.", "Cada pareja de cifras es un piso y una puerta del cuadrado: la primera cifra, la fila; la segunda, la columna.", f"Las coordenadas son {_S_POL}: la palabra es {I.PALABRA}."],
              SIN_GENTE + "Una gran válvula de bronce de una locomotora de vapor, con un cierre de combinación y una nube de vapor saliendo por una rendija, entre manómetros y tuberías."),
    "86": gris("86", "Las cinco coordenadas", "Una hoja del libro del telegrafista que dice en qué orden están las cinco coordenadas.", ["Explica el orden de las cinco coordenadas.", "Cada coordenada la dejó un puzle distinto.", "La primera cifra es la fila y la segunda, la columna."]),
    "87": gris("87", "El cuadrado de Polibio", "El cuadrado de Polibio: cinco filas y cinco columnas de letras.", ["Sirve para leer las coordenadas (carta 85).", "Cada letra tiene una fila y una columna.", "La I y la J comparten casilla."]),
    # ------------------------------------------------------------------ El furgón y el final
    "94": escena("94", "El furgón del oro", [64, 66, 67], [38, 56, 30, 44, 33, 37, 39, 46],
                 "Las dos mitades de la llave encajan y abren la puerta del furgón del oro. Dentro, ni rastro del jinete: solo un depósito de agua de la locomotora, con una bomba atascada (carta 64) y un plano del fontanero con tubos ya colocados (cartas 66 y 67, dos mitades: juntad la 66 arriba y la 67 abajo). Dicen que el cristal cayó dentro del depósito.",
                 ["Un único puzle: arreglar la bomba de agua."],
                 "El interior de un furgón blindado de tren, con las paredes de hierro y una escotilla abierta en el suelo que da a un depósito de agua con tuberías de hierro cruzadas. Cristina se asoma al depósito con ojos como platos; Alberto, con una llave grande de hierro en la mano, mira las tuberías con la boca abierta."),
    "64": app("64", "La bomba de agua", "Es un juego de la app: girar los tubos de la bomba hasta que todos queden unidos en una sola red sin ningún extremo abierto.", 62,
              ["Algunos tubos tienen que quedar como en el plano de las cartas 66 y 67.", "Empezad por los tubos con un solo extremo y por los del borde: solo pueden mirar hacia dentro. Los tubos del plano son un buen punto de partida.", f"La red, fila por fila: {_S_TUB}."],
              SIN_GENTE + "Una bomba de agua de hierro con una red de tuberías cruzadas sobre un depósito en el interior de un furgón blindado, con goteras y luz de quinqué."),
    "66": pieza("66", "bomba", "Media lámina del plano de la bomba.", ["Es la mitad de una lámina: juntadla con la carta 67.", "Seis tubos están ya dibujados en su posición.", "Los tubos sin dibujar están por decidir."]),
    "67": pieza("67", "bomba", "Media lámina del plano de la bomba.", ["Es la mitad de una lámina: juntadla con la carta 66.", "Seis tubos están ya dibujados en su posición.", "Los tubos sin dibujar están por decidir."]),
    "62": combinable("62", "El cristal del Cronoportal", "roja", 12, 74, "El cristal del Cronoportal, que el jinete tiró al depósito al verse acorralado y que sube a la superficie al arrancar la bomba.",
                     SIN_GENTE + "Un cristal redondo de color azul brillante, del tamaño de una moneda grande, con destellos de luz, flotando en un depósito de agua turbia de un furgón de tren, con luz de quinqué."),
    "74": escena("74", "Cronoportal con el cristal", [], [62, 12, 64, 66, 67, 94, 57],
                 "Encajáis el cristal en el pecho del Cronoportal y el anillo se enciende con un arco de luz azul. El tren del oro pita en la estación: la locomotora está lista y solo falta la palabra para abrir la válvula (carta 85).",
                 ["Ya solo queda abrir la válvula de la locomotora."],
                 "Cristina y Alberto encajan un cristal azul brillante en el hueco del Cronoportal, un aparato de latón y cristal con un anillo que se enciende con un arco de luz azul, sobre el techo del furgón de un tren al atardecer. Cristina lo sostiene con las dos manos con una enorme sonrisa; Alberto contiene el aliento mirando el anillo con la boca abierta."),
    "99": escena("99", "De vuelta a casa (FIN)", [], [74, 82, 85, 86, 87],
                 "La palabra abre la válvula: el vapor escapa en una nube, la locomotora arranca y el anillo del Cronoportal se abre en un arco de luz justo cuando el jinete llega a caballo al apartadero, con las manos vacías. Aterrizáis en vuestro salón. Alberto mira el aparato: «Mañana, otro destino». Cristina sonríe y guarda en el bolsillo una pequeña estrella de sheriff. FIN.",
                 [],
                 "La escena ocurre DENTRO del salón de su casa actual, en el presente (sofá, estanterías con libros, plantas, una lámpara encendida y luz cálida de tarde por la ventana): acaban de VOLVER a casa. Cristina y Alberto acaban de salir de un portal circular de luz azul y dorada que se abre detrás de ellos; a través del portal todavía se ven una locomotora de vapor, una nube de vapor y un jinete a caballo a lo lejos. Llevan aún su ropa del Oeste cubierta de polvo. Cristina ríe a carcajadas con una estrella de sheriff en la mano y Alberto grita de euforia con los brazos en alto. Están de cara a nosotros, aterrizando en el salón y alejándose del portal, que queda a su espalda y se está cerrando; el mundo de la aventura solo se ve a través del portal, detrás de ellos. No están entrando en el portal ni saliendo de casa: están llegando."),
}

META = dict(juego="Dry Gulch, 1878 — El Tren del Oro", estilo=ESTILO, personajes=PERSONAJES, hoja=HOJA, foto=FOTO, video=VIDEO,
            mosaicos={k: dict(filas=m["filas"], cols=m["cols"], cartas=m["cartas"], titulo=m["titulo"]) for k, m in MOSAICOS.items()})

SPEC = dict(final="99", needs={
    "24": ["14", "16"], "28": ["20", "18", "19", "21"], "57": ["22", "35"], "30": ["40", "41", "43", "45"], "36": ["48", "42", "49", "53"],
    "44": ["52", "54", "55", "59"], "56": ["46", "37", "39", "33"], "58": ["51", "26", "61", "63"], "80": ["69", "70", "71"], "94": ["38", "56"],
    "62": ["64", "66", "67"], "82": ["72", "75", "79"], "74": ["12", "62"], "99": ["85", "86", "87", "74"]}, eventos={})

PARA_QUE = {k: c["titulo"].split("— ", 1)[1] for k, c in J.items()}

_T = [
    ("leer", "P", "Llegada", "Pon el Modo PC (solo la P en la mesa) y en el móvil pulsa Empezar. Lee la carta P: coge la 10 y la 12."),
    ("leer", "10", "La estación", "Lee la carta 10. Descarta la P y coge 14, 16, 18, 19, 20, 21 y 22. Junta el cuadro del banco: 19 arriba y 21 abajo."),
    ("app", "14", "El telegrama en zigzag", f"En el móvil: Acción, 14. Con el telegrama (16) y su zigzag de cuatro rieles, el mensaje es {_S_VAL}. El mensaje te dice que cojas la 24. Anota la coordenada: {I.COORD['14']}.", "carta 24"),
    ("leer", "24", "El telégrafo habla", "Lee la carta 24. Descarta 14 y 16 y coge la 26 (guárdala para la bodega)."),
    ("app", "20", "El cuadro del banquero", f"En el móvil: Acción, 20. Con el cuadro (19 y 21) y el acertijo (18), los tachones son: {_S_HIT}. El mensaje te dice que cojas la 28.", "carta 28"),
    ("leer", "28", "La reja abierta", "Lee la carta 28. Descarta 18, 19, 20 y 21 y coge la 35."),
    ("combinar", "22", "35", "La estrella del sheriff", "Las dos mitades de la estrella (22 y 35) son combinables: 22 + 35 = 57. Coge la 57."),
    ("leer", "57", "La estrella del sheriff", "Lee la carta 57. Descarta 22, 35, 10 y 28 y coge 31 y 32."),
    ("leer", "31", "El patio del carretero", "Lee la carta 31. Coge 40, 41, 43 y 45. Junta el tablero: 41 a la izquierda y 43 a la derecha."),
    ("app", "40", "La caja del carro", f"En el móvil: Acción, 40. Con el tablero (41 y 43) y las seis piezas (45), por filas con las letras de las piezas: {_S_PEN}. El mensaje te dice que cojas la 30. Anota la coordenada: {I.COORD['40']}.", "carta 30"),
    ("leer", "30", "La caja cerrada", "Lee la carta 30. Descarta 31, 40, 41, 43 y 45 y coge la 38."),
    ("leer", "32", "El saloon", "Lee la carta 32. Coge 42, 48, 49 y 53. Junta el cuadro: 42 a la izquierda y 49 a la derecha."),
    ("app", "48", "El cuadro de apuestas", f"En el móvil: Acción, 48. Con el cuadro (42 y 49) y la regla (53): {_S_KAK}. El mensaje te dice que cojas la 36.", "carta 36"),
    ("leer", "36", "El almacén del tendero", "Lee la carta 36. Descarta 32, 42, 48, 49 y 53 y coge 52, 54, 55 y 59."),
    ("app", "52", "La carga del carro", f"En el móvil: Acción, 52. Con los pesos (54), los valores (55) y el eje (59), la mejor carga es: {_S_MOC}. El mensaje te dice que cojas la 44. Anota la coordenada: {I.COORD['52']}.", "carta 44"),
    ("leer", "44", "La plaza de Dry Gulch", "Lee la carta 44. Descarta 36, 52, 54, 55 y 59 y coge 33, 37, 39, 46, 51, 61 y 63. Junta el suelo de la bodega: 61 a la izquierda y 63 a la derecha."),
    ("app", "46", "El duelo en corro", f"En el móvil: Acción, 46. Con el corro (37) y la cuenta (39 y 33), el último que queda es {_S_JOS}. El mensaje te dice que cojas la 56.", "carta 56"),
    ("app", "51", "La bodega de barriles", f"En el móvil: Acción, 51. Con el refrán (26) y los huecos del suelo (61 y 63): {_S_SOK}. El mensaje te dice que cojas la 58. Anota la coordenada: {I.COORD['51']}.", "carta 58"),
    ("leer", "58", "El apartadero", "Lee la carta 58. Descarta 51, 61, 63, 26 y 24 y coge 69, 70 y 71."),
    ("app", "69", "La maniobra de vagones", f"En el móvil: Acción, 69. Con los pesos (70) y la regla (71), la maniobra (E entrar, S sacar): {_S_VAG}. El mensaje te dice que cojas la 80. Anota la coordenada: {I.COORD['69']}.", "carta 80"),
    ("leer", "80", "El despacho del jefe de estación", "Lee la carta 80. Descarta 58, 69, 70 y 71 y coge 72, 75 y 79."),
    ("app", "72", "Los hierros del ganado", f"En el móvil: Acción, 72. Con las marcas (75) y el hierro (79): las reses {_S_HIE}. El mensaje te dice que cojas la 82.", "carta 82"),
    ("leer", "82", "La locomotora", "Lee la carta 82. Descarta 80, 72, 75 y 79 y coge 85, 86 y 87."),
    ("combinar", "38", "56", "La llave del furgón", "Las dos mitades de la llave (38 y 56) son combinables: 38 + 56 = 94. Coge la 94."),
    ("leer", "94", "El furgón del oro", "Lee la carta 94. Descarta 38, 56, 30, 44, 33, 37, 39 y 46 y coge 64, 66 y 67. Junta el plano: 66 arriba y 67 abajo."),
    ("app", "64", "La bomba de agua", f"En el móvil: Acción, 64. Con el plano (66 y 67), la red queda así (fila por fila): {_S_TUB}. El mensaje te dice que cojas la 62.", "carta 62"),
    ("combinar", "12", "62", "El cristal", "El Cronoportal (12) y el cristal (62) son combinables: 12 + 62 = 74. Coge la 74."),
    ("leer", "74", "Cronoportal con el cristal", "Lee la carta 74. Descarta 62, 12, 64, 66, 67, 94 y 57."),
    ("app", "85", "La válvula de la locomotora", f"En el móvil: Acción, 85. Con el orden (86) y el cuadrado (87), las coordenadas {_S_POL} dan la palabra {I.PALABRA}. El mensaje te dice que cojas la 99.", "carta 99"),
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
