"""El Cuarto de Leo, 1995: La Noche de los Juguetes — versión de 62 cartas (22 oct 2026), de dificultad fácil-media (sigue siendo el juego más amable).

La mecánica de cartas propia sigue siendo el FOLIOSCOPIO: cinco páginas del cuaderno de Leo que se ordenan por el sol que se pone en la ventana y se
hojean como una animación (en el Modo PC, botón «Hojear»). Once puzles que no se parecen a los de ningún otro juego de la serie: un baúl con cuatro
cubos de dibujos, las siete diferencias entre una foto Polaroid y una estantería, un tren que se carga en el orden del folioscopio, una marioneta con los
hilos enredados, el juego de la oca de Leo, un solitario de clavijas, el collar de cuentas de mamá, una torre de bloques por sus vistas, una pista de
canicas con balancines, un juego de memoria y una nana de xilófono. Solo 16 cartas tienen a Cristina (muñeca de trapo) y Alberto (robot de hojalata);
el resto son objetos y pistas sin personas. Las cartas-pista las dibuja herramientas/juguetes.py (instancias_juguetes.py)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ampliacion as _amp  # noqa: E402
import instancias_juguetes as I  # noqa: E402

INST = I.INST
FOLIO = INST["folioscopio"]

ESTILO = ("Ilustración de animación 3D de estilo familiar y amable, como una película de juguetes que cobran vida: colores vivos y saturados, plástico brillante, tela con costuras, madera pintada, luz cálida de lamparita de noche y rayos de luna azulados entrando por la ventana; "
          "el cuarto de un niño de los años 90 visto a la altura de los juguetes, con los muebles enormes. Formato vertical 2:3. Sin texto, letras ni números legibles en la imagen; los libros, cajas y carteles solo muestran rayas o manchas de color. "
          "Deja libre de detalles importantes la esquina superior izquierda y el 18 % inferior de la imagen. "
          "Los personajes tienen siempre expresiones distintas y expresivas, adecuadas a la escena (nunca la misma cara en dos imágenes).")

PERSONAJES = {
    "Cristina": "Cristina convertida en juguete: una muñeca de trapo con su misma cara reconocible (mujer de 26 años, ojos azules de botón brillante, pecas pintadas), pelo de lana amarilla muy rizado, vestido de tela de cuadros rojos y blancos, delantal azul, costuras visibles en brazos y piernas y zapatitos de fieltro.",
    "Alberto": "Alberto convertido en juguete: un robot de hojalata de cuerda con su misma cara reconocible (hombre de 27 años, ojos marrones pintados, pelo moreno corto y barba pintados en la cabeza de lata), cuerpo de lata azul con remaches dorados, antenita con una bolita roja, pinzas por manos y una gran llave de cuerda en la espalda.",
}

HOJA = ("Crea una hoja de personajes (character sheet) con las dos personas de la foto adjunta convertidas en juguetes, de cuerpo entero y de frente, sobre fondo claro y neutro. "
        "Mantén su parecido real con la foto en la cara. "
        "Cristina: muñeca de trapo con su misma cara reconocible (mujer de 26 años, ojos azules de botón brillante, pecas pintadas), pelo de lana amarilla muy rizado, vestido de tela de cuadros rojos y blancos, delantal azul, costuras visibles en brazos y piernas y zapatitos de fieltro. "
        "Alberto: robot de hojalata de cuerda con su misma cara reconocible (hombre de 27 años, ojos marrones pintados, pelo moreno corto y barba pintados en la cabeza de lata), cuerpo de lata azul con remaches dorados, antenita con una bolita roja, pinzas por manos y una gran llave de cuerda en la espalda. "
        "Estilo: " + ESTILO)

FOTO = ("Antes de nada, adjunta a ChatGPT una foto de Cristina y Alberto juntos (o una de cada uno, con la cara bien visible). "
        "Pídele que mantenga el parecido real en la cara, pero con el aspecto de juguete (muñeca de trapo y robot de hojalata) de este juego.")

VIDEO = ("Crea un vídeo vertical 9:16 de 15 segundos, con estilo de película de animación 3D familiar, luz cálida de lamparita y luna azul. Sin ningún texto, letra ni subtítulo en pantalla. "
         "Escena 1 (0-4 s): en el salón de una casa actual, Cristina (mujer de 26 años, rubia de pelo rizado, ojos azules) y Alberto (hombre de 27 años, moreno con barba, ojos marrones) rodean un aparato de latón y cristal con un anillo central: el Cronoportal, que chisporrotea. "
         "Escena 2 (4-8 s): el anillo se enciende con un arco de luz azul y dorada, el aparato se encoge y ellos con él, girando en un túnel de luz. "
         "Escena 3 (8-12 s): caen sobre la alfombra del cuarto de un niño de los años 90, entre cajas de mudanza; ya son una muñeca de trapo y un robot de hojalata, y un cristal rojo rueda hasta un tarro de canicas. "
         "Escena 4 (12-15 s): primer plano de los dos juguetes mirándose las manos de trapo y de lata, boquiabiertos, mientras un oso de peluche con un parche se acerca a saludarles; fundido a negro. "
         "Sonido: zumbido eléctrico creciente, silbido del portal, un 'boing' al aterrizar, cuerda de juguete, una cajita de música y un perro que ronca, sin voz de narrador.")

SIN_GENTE = "Sin ninguna persona en la imagen. "

MOSAICOS = {
    "polaroid": dict(filas=2, cols=1, cartas=["19", "21"], titulo="La foto Polaroid de la estantería"),
    "hilos": dict(filas=2, cols=1, cartas=["42", "49"], titulo="Los hilos de Pipo"),
    "oca": dict(filas=2, cols=1, cartas=["54", "55"], titulo="El tablero de la oca de Leo"),
    "collar": dict(filas=2, cols=1, cartas=["61", "63"], titulo="Las primeras cuentas del collar"),
}
POS = {(2, 1): ["mitad de arriba", "mitad de abajo"], (1, 2): ["mitad izquierda", "mitad derecha"]}

_CU = INST["cubos"]
_S_CUB = "; ".join(f"cubo {i + 1}: {(_CU['solucion'][i] - _CU['inicial'][i]) % 6} toques" for i in range(4))
_S_DIF = "; ".join(c["texto"] for c in INST["estanteria"]["cambios"])
_S_TRE = ", ".join(f"{i + 1}.º {j}" for i, j in enumerate(FOLIO["orden"]))
_MA = INST["marioneta"]
_S_MAR = " y ".join(_MA["solucion"])
_OC = INST["oca"]
_S_OCA = ", ".join(str(x) for x in _OC["ruta"])
_CL = INST["clavijas"]
_S_CLA = "; ".join(f"{i + 1}.º de la fila {a[0] + 1}, columna {a[1] + 1} a la fila {c[0] + 1}, columna {c[1] + 1}" for i, (a, c) in enumerate(_CL["solucion"]))
_CO = INST["collar"]
_S_COL = f"el patrón (de siete cuentas) es {', '.join(_CO['patron'])}; la cuenta 100 es {_CO['ultimo']} y hay {_CO['azules']} azules"
_TO = INST["torre"]
_S_TOR = "; ".join(f"fila {n}: {' '.join(str(x) for x in f)}" for n, f in zip(("de delante", "de en medio", "de detrás"), _TO["alturas"]))
_PI = INST["pista"]
_S_CAN = ", ".join(f"balancín {b[1:]} a la {'izquierda' if v == 'izq' else 'derecha'}" for b, v in _PI["solucion"].items())
_ME = INST["memoria"]
_ET = lambda i: "ABCD"[i % 4] + str(i // 4 + 1)
_S_MEM = ", ".join(f"{_ET(a)}-{_ET(b)}" for a, b in _ME["solucion"])
_NA = INST["nana"]
_S_NANA = ", ".join(_NA["melodia"])
_N = _NA["notas"]


def codigo(que):
    return f"Carta dibujada por código (herramientas/juguetes.py; no se pide a ChatGPT): {que}."


def pieza(carta, mosaico, que, pistas):
    m = MOSAICOS[mosaico]
    i = m["cartas"].index(carta)
    pos = POS[(m["filas"], m["cols"])][i]
    return dict(titulo=f"Carta {carta} — {m['titulo']} ({pos})", tipo="gris",
                mosaico=dict(id=mosaico, filas=m["filas"], cols=m["cols"], fila=i // m["cols"], col=i % m["cols"]),
                descripcion=[que], pistas=pistas, arte=codigo(f"{pos} de «{m['titulo']}»"))


def gris(carta, titulo, que, pistas):
    return dict(titulo=f"Carta {carta} — {titulo}", tipo="gris", descripcion=[que], pistas=pistas, arte=codigo(titulo))


def pagina(carta):
    return gris(carta, "Página del cuaderno de Leo", "Una página del cuaderno de dibujos de Leo, parte de un folioscopio: una ventana con el sol, el suelo con cinco juguetes en fila y uno rodeado con cera roja. Se ordena con las otras cuatro páginas; en el Modo PC, botón «Hojear».",
                ["Es una de las cinco páginas del cuaderno de Leo (el folioscopio).", "Ordenad las cinco páginas mirando el sol de la ventana: se va poniendo de una página a la siguiente.", f"El orden de los juguetes rodeados es: {', '.join(FOLIO['orden'])}."])


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
    # ------------------------------------------------------------------ La estantería
    "P": escena("P", "Del tamaño de un juguete", [10, 12], [],
                "Decimotercera parada del Cronoportal... o eso pretendíais. El aparato chisporrotea, os encoge y os escupe sobre la alfombra del cuarto de Leo, un niño de 1995, rodeados de cajas de mudanza. Cristina es una muñeca de trapo y Alberto, un robot de hojalata con una llave de cuerda en la espalda. El cristal de energía rueda hasta caer en un tarro de canicas, muy arriba. Un oso de peluche con un parche en el ojo se acerca saludando: es el Capitán Pelusa. «Leo se muda mañana y esta noche los juguetes vamos a despedirnos del cuarto. Os ayudaremos a recuperar el cristal antes de que amanezca, pero hay que hacer silencio».",
                ["Mirad a vuestro alrededor y revisad el aparato."],
                "El cuarto de un niño de los años 90 por la noche, visto a ras de suelo: cajas de mudanza enormes, una alfombra con carreteras dibujadas y la luz de la luna por la ventana. En primer plano, el Cronoportal, un aparato de latón diminuto, echa chispas. Cristina, convertida en muñeca de trapo, se levanta con la boca abierta y los ojos de botón muy abiertos de asombro, y Alberto, un robot de hojalata con una llave de cuerda, se mira las pinzas con una ceja arqueada de incredulidad."),
    "10": escena("10", "La estantería de Leo", [14, 16, 18, 19, 20, 21, 22], ["P"],
                 "El Capitán Pelusa os lleva a la estantería: «Trufo, el perro, ha estado olisqueando aquí y lo ha revuelto todo. Leo dejó una nota (carta 18) y una foto Polaroid de la estantería ordenada, que ocupa dos láminas: juntad la 19 arriba y la 21 abajo (carta 20). Y detrás hay un baúl que Leo cierra con cuatro cubos de dibujos: la tapa de su caja de cubos enseña el dibujo (carta 16) que hay que formar (carta 14)». En el suelo, Cristina encuentra el mando de un coche teledirigido, sin pilas (carta 22).",
                 ["Hay dos puzles: el baúl de los cubos y las diferencias de la estantería.", "La foto son dos cartas: juntadlas, una encima de otra."],
                 "Una estantería de madera enorme vista desde el suelo, llena de juguetes de los años 90 (un tambor, un cohete, un osito, un barco), con una foto Polaroid pegada con celo en el lateral y un baúl cerrado detrás. Cristina, la muñeca de trapo, señala la foto con la boca abierta de sorpresa y Alberto, el robot de hojalata, sujeta una nota con los ojos entrecerrados de concentración."),
    "12": combinable("12", "Cronoportal sin cristal", "azul", 62, 74,
                     "El Cronoportal: una consola de latón y cristal con un anillo central apagado y un hueco vacío en el pecho, donde iba el cristal de energía.",
                     SIN_GENTE + "Primer plano del Cronoportal diminuto: una consola de latón y cristal con dos antenas de cobre, un anillo central apagado y un hueco circular vacío en el pecho del aparato, sobre la alfombra del cuarto de un niño, con una caja de mudanza gigante al fondo."),
    "14": app("14", "El baúl de los cubos", "Es un juego de la app: el baúl de Leo se cierra con cuatro cubos de madera; cada cara lleva un cuarto de un dibujo. Hay que girar los cubos hasta formar el dibujo de la tapa de su caja.", 24,
              ["El dibujo está en la carta 16.", "Cada cubo tiene seis caras con trozos de dibujos distintos. Buscad en cada cubo el cuarto que corresponde a su sitio (arriba a la izquierda, arriba a la derecha...).", f"Tocques por cubo: {_S_CUB}. Nota de los cubos: {_N['14']}."],
              SIN_GENTE + "Un baúl de juguetes de madera pintado con estrellas, cerrado, con cuatro cubos de madera con dibujos encajados en la tapa, sobre la alfombra del cuarto de un niño por la noche."),
    "16": gris("16", "La tapa de la caja de cubos", "El dibujo de la tapa de la caja de cubos de Leo, hecho con ceras: un perro marrón sobre la hierba con el sol.", ["Es el dibujo que forman los cubos (carta 14).", "Es un dibujo de Leo.", "Cada cubo lleva un cuarto de este dibujo en alguna de sus caras."]),
    "18": gris("18", "La nota de Leo", "Una nota de Leo pegada en la estantería, que habla de lo que ha revuelto Trufo.", ["Es la nota de las diferencias (carta 20).", "Dice cuántas cosas han cambiado.", "La foto de la estantería ordenada está en las cartas 19 y 21."]),
    "19": pieza("19", "polaroid", "Media lámina de la foto Polaroid de la estantería.", ["Es la mitad de una lámina: juntadla con la carta 21.", "Es la estantería ordenada, como estaba antes.", "La nota de Leo está en la carta 18."]),
    "21": pieza("21", "polaroid", "Media lámina de la foto Polaroid de la estantería.", ["Es la mitad de una lámina: juntadla con la carta 19.", "Es la estantería ordenada, como estaba antes.", "La nota de Leo está en la carta 18."]),
    "20": app("20", "Las diferencias", "Es un juego de la app: así está ahora la estantería de Leo. Hay que compararla con la foto Polaroid y tocar las siete cosas que han cambiado.", 28,
              ["La foto está en las cartas 19 y 21 y la nota de Leo, en la 18.", "Hay cambios de color, cosas que faltan o sobran, una que está del revés y otra que ha cambiado de balda. Mirad balda por balda.", f"Los cambios: {_S_DIF}. Nota de las diferencias: {_N['20']}."],
              SIN_GENTE + "Una estantería de madera enorme vista desde el suelo, llena de juguetes de los años 90 (un tambor, un cohete, un osito, una pelota, un coche), con los juguetes revueltos por un perro."),
    "22": combinable("22", "Mando sin pilas", "azul", 35, 57, "El mando de un coche teledirigido de juguete, con la antena doblada y el hueco de las pilas vacío.",
                     SIN_GENTE + "El mando de un coche teledirigido de juguete con una antena y dos palancas, con el compartimento de las pilas abierto y vacío, sobre la alfombra de un cuarto de niño."),
    "24": escena("24", "El baúl abierto", [26], [14, 16],
                 "El baúl se abre con un clic y dentro hay un collar de cuentas roto, de un color distinto cada una, y una nota de la mamá de Leo (carta 26). El Capitán Pelusa os lo explica: «Leo se la guardó antes de la mudanza. Lo enhebraremos cuando haga falta».",
                 ["Mirad lo que hay dentro del baúl."],
                 "Un baúl de juguetes de madera abierto, con un collar de cuentas de colores roto y un papel doblado dentro, sobre la alfombra del cuarto de un niño. Cristina, la muñeca de trapo, saca el collar con cuidado y los ojos muy abiertos; Alberto, el robot de hojalata, lee la nota con las pinzas sujetando el papel y una ceja arqueada."),
    "26": gris("26", "La nota del collar", "Una nota de la mamá de Leo sobre su collar de cien cuentas, con dos preguntas.", ["Son las preguntas del collar (carta 51).", "Habla de la última cuenta y de las cuentas azules.", "Las primeras cuentas están dibujadas en las cartas 61 y 63."]),
    "28": escena("28", "Detrás de la estantería", [35], [18, 19, 20, 21],
                 "Con las siete diferencias encontradas, los juguetes se apartan y detrás de la estantería hay un hueco con un paquetito: dos pilas de botón y un papel (carta 35). «¡Las pilas del coche!», grita el Capitán Pelusa.",
                 ["Mirad en el hueco de detrás de la estantería."],
                 "El hueco oscuro detrás de una estantería de madera enorme, con un paquetito de papel con dos pilas de botón brillantes dentro, visto a ras de suelo. Cristina, la muñeca de trapo, saca el paquetito con las dos manos de tela y una gran sonrisa; Alberto, el robot de hojalata, da un salto de alegría con las pinzas en el aire."),
    "35": combinable("35", "Pilas de botón", "roja", 22, 57, "Dos pilas de botón de las que usa un mando de coche teledirigido, con un trozo de papel pegado.",
                     SIN_GENTE + "Dos pilas de botón plateadas con un trozo de papel pegado, sobre la palma de una mano de trapo, con una caja de mudanza gigante al fondo."),
    "57": escena("57", "El coche teledirigido", [31, 32], [22, 35, 10, 28],
                 "Con las pilas puestas, el coche teledirigido arranca con un zumbido y os lleva por la alfombra hasta el teatrillo de marionetas de Leo. A un lado, el cajón del teatrillo, con un cuaderno de dibujos de Leo y su tren de juguete (carta 31); al otro, Pipo, la marioneta, colgada de su cruceta con los hilos enredados (carta 32).",
                 ["Dos sitios: el cajón del teatrillo y Pipo."],
                 "Un coche teledirigido de juguete corriendo por una alfombra con carreteras dibujadas, con Cristina, la muñeca de trapo, al volante riendo a carcajadas y Alberto, el robot de hojalata, agarrado al alerón con los ojos como platos; al fondo, un teatrillo de marionetas con una marioneta colgada."),
    # ------------------------------------------------------------------ Rama 1: el cajón y el folioscopio
    "31": escena("31", "El cajón del teatrillo", [40, 41, 43, 45, 27, 23], [],
                 "Dentro del cajón está el cuaderno de dibujos de Leo, con las hojas sueltas: cinco páginas de un folioscopio (cartas 41, 43, 45, 27 y 23) que se ordenan y se hojean como una animación. Junto al cajón, el tren de juguete de Leo (carta 40) espera su carga.",
                 ["Un único puzle: el tren de Leo.", "Las cinco páginas se ordenan y se hojean: en el Modo PC, botón «Hojear»."],
                 "El cajón de un teatrillo de marionetas abierto, con un cuaderno de dibujos infantil de espiral y hojas sueltas, y al lado las vías y un tren de juguete de madera con cinco vagones vacíos. Cristina, la muñeca de trapo, hojea las páginas con cara de curiosidad y Alberto, el robot de hojalata, mira el tren con las pinzas en la cintura y una sonrisa de aprobación."),
    "40": app("40", "El tren de Leo", "Es un juego de la app: el tren de juguete de Leo con cinco vagones y cinco juguetes en el andén. Hay que cargar un juguete en cada vagón, del primero al último, en el orden en que Leo los rodeó en su cuaderno.", 30,
              ["El orden está en el folioscopio: las cinco páginas del cuaderno de Leo (cartas 41, 43, 45, 27 y 23).", "Ordenad las páginas por el sol de la ventana, del más alto al que ya se ha puesto, y apuntad qué juguete rodea Leo en cada una.", f"Vagones, del primero al último: {_S_TRE}. Nota del tren: {_N['40']}."],
              SIN_GENTE + "Un tren de juguete de madera con cinco vagones de colores sobre unas vías en una alfombra, con juguetes (un patito, una pelota, un tambor, un cohete, una cometa) en un andén de cartón."),
    "41": pagina("41"), "43": pagina("43"), "45": pagina("45"), "27": pagina("27"), "23": pagina("23"),
    "30": escena("30", "La estación", [38], [31, 40, 41, 43, 45, 27, 23],
                 "El tren silba y da la vuelta al cuarto hasta la estación de cartón, junto al escritorio. Allí os espera Tic, un ratón de cuerda que ha perdido su llave: «Yo sé trepar por el cable de la lámpara hasta el escritorio, pero sin cuerda no me muevo». En el andén, media llave de cuerda dorada (carta 38).",
                 ["Mirad en el andén."],
                 "Una estación de tren de cartón pintado junto a la pata de un escritorio enorme, con un tren de juguete parado y un ratón de cuerda gris sin llave sentado en el andén con cara triste. Cristina, la muñeca de trapo, le acaricia la cabeza con ternura y Alberto, el robot de hojalata, recoge del suelo media llave dorada con una gran sonrisa."),
    "38": combinable("38", "Mitad de la llave de cuerda", "roja", 56, 94, "Una mitad de una llave de cuerda dorada de las de un ratón de juguete.",
                     SIN_GENTE + "La mitad izquierda de una llave de cuerda dorada de las de un ratón de juguete, sobre el andén de cartón de una estación."),
    # ------------------------------------------------------------------ Rama 2: Pipo
    "32": escena("32", "El teatrillo de Pipo", [42, 48, 49, 53], [],
                 "Pipo, la marioneta, está colgada de su cruceta con cuatro mandos de colores; los hilos están tan enredados que ocupan dos láminas: juntad la 42 arriba y la 49 abajo. El cartel de la función (carta 53) enseña cómo saluda Pipo y el teatrillo es la carta 48.",
                 ["Un único puzle: los hilos de Pipo.", "Los hilos son dos cartas: juntadlas, una encima de otra."],
                 "Un teatrillo de marionetas de juguete con una cortina roja y una marioneta de madera colgada de una cruceta con cuatro mandos de colores y los hilos enredados. Cristina, la muñeca de trapo, sigue un hilo con el dedo y la lengua entre los dientes; Alberto, el robot de hojalata, mira los mandos con la cabeza ladeada y una antena torcida."),
    "48": app("48", "La marioneta", "Es un juego de la app: tirar de los mandos de la cruceta para que Pipo haga la postura del cartel. Qué mando mueve cada mano y cada pie se ve siguiendo los hilos enredados.", 36,
              ["Los hilos están en las cartas 42 y 49 y el cartel de la función, en la 53.", "Seguid cada hilo con el dedo desde su mando hasta el miembro de Pipo. Luego, tirad solo de los mandos de los miembros que el cartel tiene levantados.", f"Hay que tirar de los mandos {_S_MAR}. Nota de la marioneta: {_N['48']}."],
              SIN_GENTE + "Un teatrillo de marionetas de juguete con una cortina roja y una marioneta de madera haciendo una pose con un brazo y una pierna levantados, colgada de una cruceta con hilos."),
    "42": pieza("42", "hilos", "Media lámina de los hilos enredados de Pipo.", ["Es la mitad de una lámina: juntadla con la carta 49.", "Los hilos salen de los cuatro mandos de colores.", "El cartel de la función está en la carta 53."]),
    "49": pieza("49", "hilos", "Media lámina de los hilos enredados de Pipo.", ["Es la mitad de una lámina: juntadla con la carta 42.", "Los hilos llegan a las manos y los pies de Pipo.", "El cartel de la función está en la carta 53."]),
    "53": gris("53", "El cartel de la función", "El cartel de la función de Pipo, con la pose con que saluda al público.", ["Es la postura que hay que conseguir (carta 48).", "Fijaos en qué manos y qué pies tiene levantados.", "Los hilos están en las cartas 42 y 49."]),
    "36": escena("36", "Bajo la cama", [52, 54, 55, 59], [32, 42, 48, 49, 53],
                 "Una trampilla del teatrillo da a un pasadizo que sale bajo la cama de Leo, donde guarda su juego de la oca. El tablero, de sesenta casillas con escaleras y toboganes, ocupa dos láminas: juntad la 54 arriba y la 55 abajo. Su hermana Marta jugó con él y dejó sus diez tiradas de dado apuntadas (carta 59): hay que saber dónde quedó la ficha (carta 52).",
                 ["Un único puzle: la oca de Leo.", "El tablero son dos cartas: juntadlas, una encima de otra."],
                 "El espacio bajo una cama infantil enorme, con un tablero de la oca desplegado en el suelo, una ficha roja y un dado gigante, y una caja de zapatos al lado. Cristina, la muñeca de trapo, cuenta casillas con los dedos y los ojos muy abiertos; Alberto, el robot de hojalata, empuja el dado con las pinzas con cara de concentración."),
    "52": app("52", "La oca de Leo", "Es un juego de la app: el tablero de la oca de Leo tiene sesenta casillas con escaleras que suben y toboganes que bajan. Hay que decir en qué casilla acaba la ficha tras las diez tiradas de su hermana, empezando fuera del tablero.", 44,
              ["El tablero está en las cartas 54 y 55 y las tiradas, en la 59.", "Id tirada a tirada: sumad el dado a la casilla donde estáis. Si caéis en el pie de una escalera, subís a su cima; si caéis en la cabeza de un tobogán, bajáis a su cola.", f"Pasa por las casillas {_S_OCA}. Nota de la oca: {_N['52']}."],
              SIN_GENTE + "Un tablero del juego de la oca de colores desplegado sobre el suelo, con una ficha roja y un dado grande, con escaleras de madera y toboganes verdes pintados, bajo una cama."),
    "54": pieza("54", "oca", "Media lámina del tablero de la oca de Leo.", ["Es la mitad de una lámina: juntadla con la carta 55.", "Son las casillas de la 31 a la 60.", "Las tiradas de Marta están en la carta 59."]),
    "55": pieza("55", "oca", "Media lámina del tablero de la oca de Leo.", ["Es la mitad de una lámina: juntadla con la carta 54.", "Son las casillas de la 1 a la 30.", "Las tiradas de Marta están en la carta 59."]),
    "59": gris("59", "Las tiradas de Marta", "Las diez tiradas de dado de la hermana de Leo, en orden, con una leyenda de la escalera y el tobogán.", ["Son las tiradas de la oca (carta 52).", "Se tiran en orden: la 1, la 2...", "El tablero está en las cartas 54 y 55."]),
    # ------------------------------------------------------------------ Encima de la cama
    "44": escena("44", "Encima de la cama", [33, 37, 39, 46, 51, 61, 63], [36, 52, 54, 55, 59],
                 "Trepáis por una escalera de la oca hasta la cama de Leo, que duerme abrazado a su almohada. A un lado, su solitario de clavijas, con las clavijas desordenadas (carta 37), la regla de la caja (carta 39) y la meta (carta 33): hay que ganarlo (carta 46). Al otro, colgado del cabecero, el collar de mamá, que ya sabéis enhebrar: las primeras cuentas, en dos láminas (juntad la 61 arriba y la 63 abajo) y las preguntas de su nota (carta 26), para el collar (carta 51).",
                 ["Hay dos puzles: el solitario de clavijas y el collar."],
                 "Una cama infantil enorme vista desde el colchón, con un niño dormido abrazado a su almohada, un edredón de cohetes, un tablero de solitario de clavijas junto a su mano y un collar de cuentas colgado del cabecero. Cristina, la muñeca de trapo, se tapa la boca con la mano para no reír y Alberto, el robot de hojalata, levanta una clavija de puntillas con cara de mucha atención."),
    "46": app("46", "El solitario de clavijas", "Es un juego de la app: un tablero en cruz de 33 agujeros con nueve clavijas. Una clavija salta sobre otra, en línea recta, a un agujero vacío y se come a la saltada. Hay que dejar una sola clavija, en el agujero del medio.", 56,
              ["El tablero está en la carta 37, la regla en la 39 y la meta, en la 33.", "Empezad por los saltos que dejan clavijas en el centro del tablero y evitad dejar clavijas aisladas, lejos de las demás: ya no podrán saltar ni ser saltadas.", f"Una solución: {_S_CLA}."],
              SIN_GENTE + "Un tablero de solitario de clavijas de madera, en forma de cruz, con clavijas rojas colocadas en algunos agujeros, sobre una cama infantil con un edredón de cohetes."),
    "37": gris("37", "El solitario de Leo", "El tablero en cruz del solitario de clavijas con las nueve clavijas en su sitio de partida.", ["Es el solitario de la carta 46.", "Hay nueve clavijas rojas.", "La regla está en la carta 39 y la meta, en la 33."]),
    "39": gris("39", "La regla del solitario", "La regla del solitario de clavijas, de la caja del juego, en versos.", ["Explica cómo salta una clavija (carta 46).", "Siempre en línea recta, nunca en diagonal.", "A la clavija saltada se la come."]),
    "33": gris("33", "La meta", "El tablero del solitario con una sola clavija amarilla, en el agujero del medio.", ["Es el final del solitario (carta 46).", "Tiene que quedar una sola clavija.", "Y justo en el agujero del medio."]),
    "56": combinable("56", "Otra mitad de la llave de cuerda", "roja", 38, 94, "La otra mitad de la llave de cuerda dorada, que estaba escondida bajo la tapa del solitario.",
                     SIN_GENTE + "La mitad derecha de una llave de cuerda dorada de las de un ratón de juguete, sobre el tablero de madera de un solitario de clavijas."),
    "51": app("51", "El collar de mamá", "Es un juego de la app: un collar de cien cuentas cuyos colores se repiten siempre igual. Hay que decir de qué color es la última cuenta y cuántas son azules.", 58,
              ["La nota de mamá está en la carta 26 y las primeras cuentas, en las cartas 61 y 63.", "Buscad cuántas cuentas tiene el patrón antes de repetirse y contad cuántas vueltas completas caben en cien; las cuentas que sobran se leen en el principio del patrón.", f"{_S_COL}."],
              SIN_GENTE + "Un collar de cuentas de colores (rojas, azules, verdes, amarillas y moradas) colgado del cabecero de una cama infantil, con las cuentas bien enhebradas, a la luz de una lamparita."),
    "61": pieza("61", "collar", "Media lámina de las primeras cuentas del collar.", ["Es la mitad de una lámina: juntadla con la carta 63.", "Son las cuentas de la 1 a la 20.", "Las preguntas de mamá están en la carta 26."]),
    "63": pieza("63", "collar", "Media lámina de las primeras cuentas del collar.", ["Es la mitad de una lámina: juntadla con la carta 61.", "Son las cuentas de la 21 a la 40.", "Las preguntas de mamá están en la carta 26."]),
    # ------------------------------------------------------------------ El escritorio
    "58": escena("58", "El escritorio", [69, 70, 71], [51, 61, 63, 26, 24],
                 "Tic, con media llave puesta, no puede trepar todavía, pero el collar colgado del cabecero os sirve de cuerda y subís al escritorio de Leo. Allí está su pista de canicas (carta 70): el tarro de las canicas está al final y la regla (carta 71) dice cómo funcionan los balancines. Si la tercera canica cae en el tarro, un resorte abrirá un cajoncito (carta 69).",
                 ["Un único puzle: la pista de canicas."],
                 "Un escritorio infantil enorme con una pista de canicas de plástico con tres balancines naranjas y un tarro de cristal al final, y una lámpara con el cable colgando. Cristina, la muñeca de trapo, coloca un balancín con los ojos entrecerrados de concentración; Alberto, el robot de hojalata, sujeta una canica con sus pinzas con cara de duda."),
    "69": app("69", "La pista de canicas", "Es un juego de la app: colocar los tres balancines para que la tercera canica caiga en el tarro. Cada balancín manda la canica al lado al que apunta y cambia de lado cuando ella pasa.", 80,
              ["La pista está en la carta 70 y la regla, en la 71.", "Seguid una canica entera: cada vez que pasa por un balancín, este se gira. La segunda canica encuentra los balancines cambiados por la primera.", f"Una posición buena: {_S_CAN}."],
              SIN_GENTE + "Una pista de canicas de plástico con tres balancines naranjas y un tarro de cristal al final, con tres canicas listas arriba, sobre un escritorio infantil."),
    "70": gris("70", "La pista de canicas", "El tablero de la pista de canicas con tres balancines numerados, cuatro salidas (A, B, C y D) y un tarro.", ["Es la pista de la carta 69.", "El tarro está bajo una de las salidas.", "La regla de los balancines está en la carta 71."]),
    "71": gris("71", "La regla de la pista", "Una nota pegada en la tapa de la caja de la pista de canicas, con la regla de los balancines.", ["Es la regla de la carta 69.", "Cada balancín cambia de lado al pasar una canica.", "La tercera canica es la que tiene que caer en el tarro."]),
    "80": escena("80", "El cajoncito", [72, 75, 79], [58, 69, 70, 71],
                 "La tercera canica cae en el tarro y un resorte abre un cajoncito del escritorio. Dentro, un juego de memoria de dieciséis cartas (de la A1 a la D4) y dos hojas con los doce intentos de Leo para encontrar las parejas (cartas 75 y 79). Hay que formar las ocho parejas (carta 72).",
                 ["Un único puzle: el juego de memoria."],
                 "Un cajoncito de escritorio abierto con dieciséis cartas de memoria boca abajo en cuatro filas y dos hojas de papel con dibujos de intentos, y una lámpara encendida. Cristina, la muñeca de trapo, da la vuelta a una carta con los ojos muy abiertos y una sonrisa de sorpresa; Alberto, el robot de hojalata, anota con una pinza en una hoja con la lengua entre los dientes."),
    "72": app("72", "La memoria de Leo", "Es un juego de la app: dieciséis cartas boca abajo con ocho dibujos, cada uno dos veces. Los doce intentos de Leo enseñan quince posiciones. Hay que formar las ocho parejas.", 82,
              ["Los intentos están en las cartas 75 y 79.", "Apuntad qué dibujo sale en cada posición, intento a intento. Las parejas son las dos posiciones con el mismo dibujo; una posición no se ve nunca, pero su dibujo solo sale una vez.", f"Las parejas: {_S_MEM}."],
              SIN_GENTE + "Dieciséis cartas de memoria boca abajo en cuatro filas sobre un escritorio, con una de ellas levantada enseñando el dibujo de un cohete."),
    "75": gris("75", "Los intentos de Leo (I)", "Los seis primeros intentos de Leo, con las dos cartas que dio la vuelta y su posición (de la A1 a la D4).", ["Son los primeros seis intentos del juego de memoria (carta 72).", "Cada intento enseña dos cartas y sus posiciones.", "Los otros seis intentos están en la carta 79."]),
    "79": gris("79", "Los intentos de Leo (II)", "Los seis últimos intentos de Leo, con las dos cartas que dio la vuelta y su posición (de la A1 a la D4).", ["Son los últimos seis intentos del juego de memoria (carta 72).", "Cada intento enseña dos cartas y sus posiciones.", "Los otros seis intentos están en la carta 75."]),
    "82": escena("82", "La cajita de música", [85, 86, 87], [80, 72, 75, 79],
                 "Las cartas dejan ver el fondo del cajoncito: la cajita de música de Leo, con un xilófono de siete barras. Leo se mueve en la cama: para que no se despierte, hay que tocarle su nana (carta 85). Las cinco notas las dejaron cinco puzles; el orden está en una hoja con dibujos (carta 86) y los colores de las notas, en otra (carta 87).",
                 ["Un único puzle: la nana del xilófono."],
                 "El interior de una cajita de música abierta con un xilófono de siete barras de colores y un mecanismo de cilindro con púas, sobre un escritorio infantil, mientras al fondo un niño se mueve en su cama. Cristina, la muñeca de trapo, se lleva un dedo a los labios pidiendo silencio con los ojos muy abiertos; Alberto, el robot de hojalata, golpea una barra con una pinza con mucho cuidado y cara de susto."),
    "85": app("85", "La nana", "Es un juego de la app: el xilófono de la cajita de música tiene siete barras de colores. Hay que tocar las cinco notas de la nana, en orden, las que dejaron cinco puzles.", 99,
              ["El orden de las cinco notas está en la carta 86 y los colores de las notas, en la 87.", "Cada dibujo de la carta 86 es un puzle: los cubos, las diferencias, el tren, la marioneta y la oca. Cada uno os dejó una nota; pasad cada nota a su color con la carta 87.", f"La nana: {_S_NANA}."],
              SIN_GENTE + "Un xilófono de siete barras de colores (rojo, naranja, amarillo, verde, azul, añil y violeta) con dos macillos de madera, sobre un escritorio infantil, con la luz de la luna."),
    "86": gris("86", "La nana de Leo", "Una hoja con cinco dibujos, de arriba abajo: unos cubos, una lupa, un tren, una marioneta y unos dados, cada uno con una raya al lado para escribir una nota.", ["Es el orden de las notas de la nana (carta 85).", "Cada dibujo es un puzle que dejó una nota.", "Las notas se pasan a colores con la carta 87."]),
    "87": gris("87", "El xilófono", "El xilófono de la cajita de música, con sus siete barras de colores y el nombre de cada nota debajo.", ["Sirve para pasar las notas a colores (carta 85).", "Hay siete notas y siete colores.", "Las notas van de la más grave a la más aguda."]),
    # ------------------------------------------------------------------ La torre y el final
    "94": escena("94", "La llave de Tic", [64, 66, 67], [38, 56, 30, 44, 33, 37, 39, 46],
                 "Las dos mitades de la llave de cuerda encajan en la espalda de Tic y el ratón sale disparado hasta lo alto de la estantería: allí está el tarro de canicas con vuestro cristal. Pero la estantería es demasiado alta para vosotros: hay que construir con los bloques de Leo una torre que llegue hasta el tarro (carta 64). Las instrucciones de la caja de bloques, con las vistas de la torre, están en dos hojas (cartas 66 y 67).",
                 ["Un único puzle: la torre de bloques."],
                 "Un ratón de cuerda gris con una llave dorada en la espalda corriendo por una alfombra hacia una caja de bloques de construcción de colores, con una estantería altísima al fondo con un tarro de canicas. Cristina, la muñeca de trapo, levanta un bloque más grande que ella con cara de esfuerzo y Alberto, el robot de hojalata, mira la estantería hacia arriba con la cabeza echada hacia atrás y la boca abierta."),
    "64": app("64", "La torre de bloques", "Es un juego de la app: construir en una base de 3 × 3 la torre de las instrucciones. Cada casilla puede llevar de 0 a 3 bloques y hay vistas de frente, de lado y desde arriba.", 62,
              ["Las vistas de frente y de lado están en la carta 66; la vista desde arriba y el total de bloques, en la 67.", "La vista de frente dice la altura máxima de cada columna y la de lado, la de cada fila. La vista desde arriba dice qué casillas llevan algún bloque.", f"Alturas por filas: {_S_TOR}."],
              SIN_GENTE + "Una torre de bloques de construcción de colores (amarillos, naranjas y rojos) construida junto a una estantería alta de un cuarto de niño, vista desde abajo."),
    "66": gris("66", "Las instrucciones de la torre (I)", "La hoja de instrucciones de la torre de bloques, con la vista de frente y la vista desde la derecha.", ["Es la primera hoja de instrucciones (carta 64).", "Los números de bloques de cada columna y cada fila se ven en el dibujo.", "La vista desde arriba está en la carta 67."]),
    "67": gris("67", "Las instrucciones de la torre (II)", "La hoja de instrucciones de la torre de bloques, con la vista desde arriba y el total de bloques.", ["Es la segunda hoja de instrucciones (carta 64).", "Las casillas amarillas llevan algún bloque.", "El total de bloques tiene que salir justo."]),
    "62": combinable("62", "El cristal del Cronoportal", "roja", 12, 74, "El cristal del Cronoportal, que estaba entre las canicas del tarro y brilla como un caramelo rojo.",
                     SIN_GENTE + "Un cristal redondo de color rojo brillante, del tamaño de una canica grande, con destellos de luz, entre canicas de cristal de colores dentro de un tarro de vidrio, sobre una estantería, con la luz de la luna."),
    "74": escena("74", "Cronoportal con el cristal", [], [62, 12, 64, 66, 67, 94, 57],
                 "El cristal encaja y el Cronoportal se enciende. Por la ventana empieza a clarear y se oye el motor del camión de la mudanza en la calle. Los juguetes os dicen adiós desde la estantería. Activad el aparato antes de que Leo abra los ojos: solo falta tocar su nana en el xilófono para que siga durmiendo (carta 85).",
                 ["Ya solo queda tocar la nana."],
                 "El Cronoportal diminuto encendido, con un cristal rojo encajado y un arco de luz azul y dorada, sobre un escritorio infantil al amanecer; por la ventana se ve un camión de mudanzas. Cristina, la muñeca de trapo, dice adiós con la mano de tela a un oso de peluche con un parche, con una sonrisa triste y los ojos brillantes, y Alberto, el robot de hojalata, se agarra a la antena del aparato con cara de prisa."),
    "99": escena("99", "De vuelta a casa (FIN)", [], [74, 82, 85, 86, 87],
                 "La nana suena entera, Leo se da la vuelta y sigue durmiendo, y el anillo se abre en un arco de luz justo cuando el sol asoma. Cristina y Alberto salen disparados del cuarto de 1995 y aterrizan en su salón... otra vez de su tamaño y de carne y hueso. Alberto mira el aparato: «Mañana, otro destino». Cristina sonríe y guarda en el bolsillo una canica roja. FIN.",
                 [],
                 "La escena ocurre DENTRO del salón de su casa actual, en el presente (sofá, estanterías con libros, plantas, una lámpara encendida y luz cálida de tarde por la ventana): acaban de VOLVER a casa. Cristina y Alberto, otra vez personas de su tamaño normal, acaban de salir de un portal circular de luz azul y dorada que se abre detrás de ellos; a través del portal todavía se ven un cuarto de niño con juguetes, un oso de peluche con un parche saludando y la luz del amanecer. Cristina lleva puesto su vestido de cuadros y su delantal azul de muñeca de trapo y Alberto, su casaca azul con remaches dorados de robot. Cristina ríe a carcajadas con una canica roja en la mano y Alberto grita de euforia con los brazos en alto. Están de cara a nosotros, aterrizando en el salón y alejándose del portal, que queda a su espalda y se está cerrando; el mundo de la aventura solo se ve a través del portal, detrás de ellos. No están entrando en el portal ni saliendo de casa: están llegando."),
}

META = dict(juego="El Cuarto de Leo, 1995 — La Noche de los Juguetes", estilo=ESTILO, personajes=PERSONAJES, hoja=HOJA, foto=FOTO, video=VIDEO,
            mosaicos={k: dict(filas=m["filas"], cols=m["cols"], cartas=m["cartas"], titulo=m["titulo"]) for k, m in MOSAICOS.items()},
            folioscopios={"cuaderno": {"titulo": "El cuaderno de Leo", "cartas": FOLIO["cartas_en_orden"]}})

SPEC = dict(final="99", needs={
    "24": ["14", "16"], "28": ["20", "18", "19", "21"], "57": ["22", "35"], "30": ["40", "41", "43", "45", "27", "23"], "36": ["48", "42", "49", "53"],
    "44": ["52", "54", "55", "59"], "56": ["46", "37", "39", "33"], "58": ["51", "26", "61", "63"], "80": ["69", "70", "71"], "94": ["38", "56"],
    "62": ["64", "66", "67"], "82": ["72", "75", "79"], "74": ["12", "62"], "99": ["85", "86", "87", "74"]}, eventos={})

PARA_QUE = {k: c["titulo"].split("— ", 1)[1] for k, c in J.items()}

_T = [
    ("leer", "P", "Llegada", "Pon el Modo PC (solo la P en la mesa) y en el móvil pulsa Empezar. Lee la carta P: coge la 10 y la 12."),
    ("leer", "10", "La estantería de Leo", "Lee la carta 10. Descarta la P y coge 14, 16, 18, 19, 20, 21 y 22. Junta la foto: 19 arriba y 21 abajo."),
    ("app", "14", "El baúl de los cubos", f"En el móvil: Acción, 14. Con el dibujo de la tapa (16), hay que girar los cubos así: {_S_CUB}. El mensaje te dice que cojas la 24. Anota la nota de los cubos: {_N['14']}.", "carta 24"),
    ("leer", "24", "El baúl abierto", "Lee la carta 24. Descarta 14 y 16 y coge la 26 (guárdala para el collar)."),
    ("app", "20", "Las diferencias", f"En el móvil: Acción, 20. Con la foto (19 y 21) y la nota (18): {_S_DIF}. El mensaje te dice que cojas la 28. Anota la nota de las diferencias: {_N['20']}.", "carta 28"),
    ("leer", "28", "Detrás de la estantería", "Lee la carta 28. Descarta 18, 19, 20 y 21 y coge la 35."),
    ("combinar", "22", "35", "El coche teledirigido", "El mando (22) y las pilas (35) son combinables: 22 + 35 = 57. Coge la 57."),
    ("leer", "57", "El coche teledirigido", "Lee la carta 57. Descarta 22, 35, 10 y 28 y coge 31 y 32."),
    ("leer", "31", "El cajón del teatrillo", "Lee la carta 31. Coge 40, 41, 43, 45, 27 y 23. Las cinco páginas (41, 43, 45, 27 y 23) son un folioscopio: en el Modo PC, botón «Hojear»."),
    ("app", "40", "El tren de Leo", f"En el móvil: Acción, 40. Ordena las páginas por el sol de la ventana (41, 43, 45, 27 y 23) y carga los juguetes en los vagones: {_S_TRE}. El mensaje te dice que cojas la 30. Anota la nota del tren: {_N['40']}.", "carta 30"),
    ("leer", "30", "La estación", "Lee la carta 30. Descarta 31, 40, 41, 43, 45, 27 y 23 y coge la 38."),
    ("leer", "32", "El teatrillo de Pipo", "Lee la carta 32. Coge 42, 48, 49 y 53. Junta los hilos: 42 arriba y 49 abajo."),
    ("app", "48", "La marioneta", f"En el móvil: Acción, 48. Con los hilos (42 y 49) y el cartel (53), hay que tirar de los mandos {_S_MAR}. El mensaje te dice que cojas la 36. Anota la nota de la marioneta: {_N['48']}.", "carta 36"),
    ("leer", "36", "Bajo la cama", "Lee la carta 36. Descarta 32, 42, 48, 49 y 53 y coge 52, 54, 55 y 59. Junta el tablero: 54 arriba y 55 abajo."),
    ("app", "52", "La oca de Leo", f"En el móvil: Acción, 52. Con el tablero (54 y 55) y las tiradas (59), la ficha pasa por las casillas {_S_OCA} y acaba en la {_OC['final']}. El mensaje te dice que cojas la 44. Anota la nota de la oca: {_N['52']}.", "carta 44"),
    ("leer", "44", "Encima de la cama", "Lee la carta 44. Descarta 36, 52, 54, 55 y 59 y coge 33, 37, 39, 46, 51, 61 y 63. Junta el collar: 61 arriba y 63 abajo."),
    ("app", "46", "El solitario de clavijas", f"En el móvil: Acción, 46. Con el tablero (37), la regla (39) y la meta (33): {_S_CLA}. El mensaje te dice que cojas la 56.", "carta 56"),
    ("app", "51", "El collar de mamá", f"En el móvil: Acción, 51. Con la nota (26) y las cuentas (61 y 63): {_S_COL}. El mensaje te dice que cojas la 58.", "carta 58"),
    ("leer", "58", "El escritorio", "Lee la carta 58. Descarta 51, 61, 63, 26 y 24 y coge 69, 70 y 71."),
    ("app", "69", "La pista de canicas", f"En el móvil: Acción, 69. Con la pista (70) y la regla (71): {_S_CAN}. El mensaje te dice que cojas la 80.", "carta 80"),
    ("leer", "80", "El cajoncito", "Lee la carta 80. Descarta 58, 69, 70 y 71 y coge 72, 75 y 79."),
    ("app", "72", "La memoria de Leo", f"En el móvil: Acción, 72. Con los intentos de Leo (75 y 79), las parejas son {_S_MEM}. El mensaje te dice que cojas la 82.", "carta 82"),
    ("leer", "82", "La cajita de música", "Lee la carta 82. Descarta 80, 72, 75 y 79 y coge 85, 86 y 87."),
    ("combinar", "38", "56", "La llave de cuerda", "Las dos mitades de la llave (38 y 56) son combinables: 38 + 56 = 94. Coge la 94."),
    ("leer", "94", "La llave de Tic", "Lee la carta 94. Descarta 38, 56, 30, 44, 33, 37, 39 y 46 y coge 64, 66 y 67."),
    ("app", "64", "La torre de bloques", f"En el móvil: Acción, 64. Con las instrucciones (66 y 67): {_S_TOR}. El mensaje te dice que cojas la 62.", "carta 62"),
    ("combinar", "12", "62", "El cristal", "El Cronoportal (12) y el cristal (62) son combinables: 12 + 62 = 74. Coge la 74."),
    ("leer", "74", "Cronoportal con el cristal", "Lee la carta 74. Descarta 62, 12, 64, 66, 67, 94 y 57."),
    ("app", "85", "La nana", f"En el móvil: Acción, 85. Con el orden (86) y los colores de las notas (87), la nana es {_S_NANA}. El mensaje te dice que cojas la 99.", "carta 99"),
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
_amp.recalcular_mesas(PASOS, J)
