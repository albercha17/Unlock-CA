"""El Cuarto de Leo, 1995: La Noche de los Juguetes. Decimotercera parada del Cronoportal, de dificultad FÁCIL: el aparato falla y Cristina y
Alberto se despiertan convertidos en juguetes (una muñeca de trapo y un robot de hojalata de cuerda) en el cuarto de un niño, la noche antes
de la mudanza. La mecánica de cartas nueva es el FOLIOSCOPIO: cinco cartas son páginas del cuaderno de Leo que se ordenan y se hojean como una
animación (botón «Hojear» del Modo PC). Puzles nuevos: buscar las diferencias con una foto Polaroid, construir una torre a partir de sus
vistas, seguir los hilos enredados de una marioneta, cargar un tren con el orden del folioscopio y una pista de canicas con balancines.
Las cartas dibujadas por código (20, 30, 31, 41, 43, 45, 49, 51, 52, 53 y 70) las hace herramientas/juguetes.py (instancias_juguetes.json)."""
import json
import os

_AQUI = os.path.dirname(os.path.abspath(__file__))
INST = json.load(open(os.path.join(_AQUI, "instancias_juguetes.json"), encoding="utf-8"))
TORRE = INST["torre"]
MARIO = INST["marioneta"]
FOLIO = INST["folioscopio"]
PISTA = INST["pista"]
EST = INST["estanteria"]

_NOMBRE_MANDO = {"rojo": "rojo (círculo)", "azul": "azul (cuadrado)", "amarillo": "amarillo (triángulo)", "verde": "verde (estrella)"}
_MANDOS = " y ".join(_NOMBRE_MANDO[m] for m in MARIO["solucion"])
_DIFS = "; ".join(c["texto"] for c in EST["cambios"])
_TREN = ", ".join(FOLIO["orden"])
_PAGINAS = ", ".join(FOLIO["cartas_en_orden"])
_FILAS = ["delante", "en medio", "detrás"]
_TORRE = "; ".join(f"fila de {_FILAS[f]}: {', '.join(str(x) for x in TORRE['alturas'][f])}" for f in range(3))
_LADO = {"izq": "izquierda", "der": "derecha"}
_BAL = ", ".join(f"balancín {k[1]} a la {_LADO[v]}" for k, v in PISTA["solucion"].items())
_PAGS = [int(c) for c in FOLIO["cartas_en_orden"]]

ESTILO = ("Ilustración de animación 3D de estilo familiar y amable, como una película de juguetes que cobran vida: colores vivos y saturados, "
          "plástico brillante, tela con costuras, madera pintada, luz cálida de lamparita de noche y rayos de luna azulados entrando por la ventana; "
          "el cuarto de un niño de los años 90 visto a la altura de los juguetes, con los muebles enormes. Formato vertical 2:3. "
          "Sin texto, letras ni números legibles en la imagen; los libros, cajas y carteles solo muestran rayas o manchas de color. "
          "Deja libre de detalles importantes la esquina superior izquierda y el 18 % inferior de la imagen. "
          "Los personajes tienen siempre expresiones distintas y expresivas, adecuadas a la escena (nunca la misma cara en dos imágenes).")

PERSONAJES = {
    "Cristina": "Cristina convertida en juguete: una muñeca de trapo con su misma cara reconocible (mujer de 26 años, ojos azules de botón brillante, pecas pintadas), pelo de lana amarilla muy rizado, vestido de tela de cuadros rojos y blancos, delantal azul, costuras visibles en brazos y piernas y zapatitos de fieltro.",
    "Alberto": "Alberto convertido en juguete: un robot de hojalata de cuerda con su misma cara reconocible (hombre de 27 años, ojos marrones pintados, pelo moreno corto y barba pintados en la cabeza de lata), cuerpo de lata azul con remaches dorados, antenita con una bolita roja, pinzas por manos y una gran llave de cuerda en la espalda.",
}

HOJA = ("Crea una hoja de personajes (character sheet) con las dos personas de la foto adjunta convertidas en JUGUETES, de cuerpo entero y de frente, sobre fondo claro y neutro. "
        "Mantén su parecido real con la foto (cara, pelo, barba, ojos), como si un juguetero los hubiera hecho a su imagen. "
        "Cristina: muñeca de trapo con su cara, ojos azules de botón, pecas pintadas, pelo de lana amarilla muy rizado, vestido de cuadros rojos y blancos, delantal azul, costuras visibles y zapatitos de fieltro. "
        "Alberto: robot de hojalata de cuerda con su cara pintada en la cabeza de lata, ojos marrones, pelo moreno corto y barba pintados, cuerpo de lata azul con remaches dorados, antenita con bolita roja, pinzas por manos y una llave de cuerda en la espalda. "
        "Estilo: " + ESTILO)

FOTO = ("Antes de nada, adjunta a ChatGPT una foto de Cristina y Alberto juntos (o una de cada uno, con la cara bien visible). "
        "Pídele que mantenga el parecido real, pero convertidos en juguetes con el estilo de ilustración de este juego.")

VIDEO = ("Crea un vídeo vertical 9:16 de 15 segundos, con estilo de película de animación 3D familiar, luz cálida de lamparita y luna azul. Sin ningún texto, letra ni subtítulo en pantalla. "
         "Escena 1 (0-4 s): en el salón de una casa actual, Cristina (mujer de 26 años, rubia de pelo rizado, ojos azules) y Alberto (hombre de 27 años, moreno con barba, ojos marrones) rodean un aparato de latón y cristal con un anillo central: el Cronoportal, que chisporrotea. "
         "Escena 2 (4-8 s): el anillo se enciende con un arco de luz azul y dorada, el aparato se encoge y ellos con él, girando en un túnel de luz. "
         "Escena 3 (8-12 s): caen sobre la alfombra del cuarto de un niño de los años 90, entre cajas de mudanza; ya son una muñeca de trapo y un robot de hojalata, y un cristal rojo rueda hasta un tarro de canicas. "
         "Escena 4 (12-15 s): primer plano de los dos juguetes mirándose las manos de trapo y de lata, boquiabiertos, mientras un oso de peluche con un parche se acerca a saludarles; fundido a negro. "
         "Sonido: zumbido eléctrico creciente, silbido del portal, un 'boing' al aterrizar, cuerda de juguete, una cajita de música y un perro que ronca, sin voz de narrador.")


def pieza(titulo, que):
    return f"Carta dibujada por código (herramientas/juguetes.py; no se pide a ChatGPT): {que} de «{titulo}»."


def _pagina(carta):
    return dict(
        titulo=f"Carta {carta} — Página del cuaderno de Leo", tipo="gris",
        descripcion=["Una página del cuaderno de Leo, con la ventana de su cuarto y cinco juguetes en el suelo; en cada página Leo ha rodeado uno con su cera roja. Es una página de un FOLIOSCOPIO: las cinco páginas (41, 43, 45, 49 y 51) se ordenan y se hojean como una animación. En el Modo PC, botón «Hojear»."],
        pistas=["Es una de las cinco páginas del cuaderno de Leo (el folioscopio).", "Ordenad las cinco páginas mirando el sol de la ventana: se va poniendo de una página a la siguiente.", f"El orden de las páginas es {_PAGINAS}."],
        arte=pieza("Página del cuaderno de Leo", "una página del folioscopio"))


J = {
    "P": dict(
        titulo="Carta P — Del tamaño de un juguete", tipo="gris", coge=[10, 12],
        descripcion=[
            "Decimotercera parada del Cronoportal... o eso pretendíais. El aparato chisporrotea, os encoge y os escupe sobre la alfombra del cuarto de Leo, un niño de 1995, rodeados de cajas de mudanza. Cristina es una muñeca de trapo y Alberto, un robot de hojalata con una llave de cuerda en la espalda.",
            "El cristal de energía ha rodado por el suelo y Leo, antes de dormirse, lo ha guardado creyendo que era una canica. Al amanecer llega el camión de la mudanza y todo acabará en una caja. Un oso de peluche con un parche os saluda: «Soy el Capitán Pelusa. Os ayudaremos».",
            "Coged las cartas 10 y 12."],
        pistas=["Mirad a vuestro alrededor y revisad el aparato.", "Coged las cartas 10 y 12."],
        arte="El cuarto de un niño de los años 90 por la noche, visto a ras de suelo: cajas de mudanza enormes, una alfombra con carreteras dibujadas y la luz de la luna por la ventana. En primer plano, el Cronoportal, un aparato de latón diminuto, echa chispas. Cristina, convertida en muñeca de trapo, se mira las manos de tela con los ojos de botón muy abiertos de asombro, y Alberto, convertido en robot de hojalata, se toca la cabeza de lata con cara de pánico. Un oso de peluche con un parche se acerca sonriendo."),
    "10": dict(
        titulo="Carta 10 — La estantería de Leo", tipo="gris", coge=[20, 22, 24], descarta=["P"],
        descripcion=[
            "El Capitán Pelusa os lleva a la estantería: «Trufo, el perro, ha estado olisqueando aquí y lo ha revuelto todo. Leo hizo una foto de la estantería cuando la ordenó (carta 20). Lo que el perro ha cambiado esconde algo». La estantería de ahora es la carta 24. En el suelo, Cristina encuentra el mando de un coche teledirigido, sin pilas (carta 22).",
            "Coged las cartas 20, 22 y 24. Descartad la carta P."],
        pistas=["Hay un puzle: la estantería de ahora y la foto de antes.", "Comparad la foto Polaroid (carta 20) con la estantería de la app (carta 24).", "Coged las cartas 20, 22 y 24. Descartad la carta P."],
        arte="Una estantería de madera enorme vista desde el suelo, llena de juguetes de los años 90 (un tambor, un cohete, un osito, un barco), con una foto Polaroid pegada con celo en el lateral. Cristina, la muñeca de trapo, señala la foto con la boca abierta de sorpresa y Alberto, el robot de hojalata, recoge del suelo un mando a distancia de juguete con gesto de curiosidad."),
    "12": dict(
        titulo="Carta 12 — Cronoportal sin cristal", tipo="azul", combina=[62, 74],
        descripcion=[
            "El Cronoportal, ahora del tamaño de una caja de cerillas: una consola de latón con un anillo central apagado y un hueco vacío donde iba el cristal. Alberto, con voz de lata: «Sin el cristal no volvemos... ni recuperamos nuestro tamaño».",
            "Cuando recuperéis el cristal (carta 62), combinadlo con el Cronoportal: sumad sus números (12 + 62 = 74) y coged la carta 74."],
        pistas=["Le falta una pieza: el cristal de energía.", "Combinad la carta 12 con la carta 62.", "Sumad los números de las dos cartas: 12 + 62 = 74."],
        arte="Primer plano del Cronoportal en miniatura: una consola de latón y cristal con dos antenas de cobre, un anillo central apagado y un hueco circular vacío, apoyado sobre una alfombra infantil junto a una pieza de construcción gigante, con luz de lamparita."),
    "20": dict(
        titulo="Carta 20 — Foto Polaroid", tipo="gris",
        descripcion=["Una foto Polaroid de la estantería de Leo el día que la ordenó: tres baldas con doce juguetes."],
        pistas=["Es la estantería como estaba antes (carta 24).", "Comparad juguete por juguete, balda por balda: hay cinco cosas distintas.", f"Las diferencias: {_DIFS}."],
        arte=pieza("Foto Polaroid", "la foto de la estantería")),
    "22": dict(
        titulo="Carta 22 — Mando sin pilas", tipo="azul", combina=[35, 57],
        descripcion=["El mando de un coche teledirigido, con la tapa de las pilas abierta y vacía. Combinadlo con las pilas (carta 35): sumad sus números (22 + 35 = 57) y coged la carta 57."],
        pistas=["Es un mando de coche teledirigido, pero no tiene pilas.", "Cuando encontréis las pilas, combinadlas con el mando.", "Sumad los números de las dos cartas: 22 + 35 = 57."],
        arte="El mando de un coche teledirigido de juguete de los años 90, con dos palancas y la tapa de las pilas abierta y vacía, sobre una alfombra infantil, visto de cerca con luz de lamparita."),
    "24": dict(
        titulo="Carta 24 — La estantería", tipo="verde",
        descripcion=[
            "Es un juego de la app: la estantería de Leo tal como está ahora. Hay que tocar las cinco cosas que han cambiado desde la foto Polaroid (carta 20).",
            "Al encontrar las cinco, aparece lo que escondía el perro. Coged la carta 26."],
        pistas=["Hace falta la foto Polaroid (carta 20): así estaba la estantería antes.", "Mirad colores, juguetes que faltan o que sobran, juguetes del revés y juguetes que han cambiado de balda.", f"Las cinco diferencias: {_DIFS}."],
        arte="Una estantería de juguetes revuelta, vista desde abajo, con algún juguete caído y la marca de un hocico de perro en la madera. Alberto, el robot de hojalata, compara la estantería con una foto con los ojos entrecerrados de concentración y Cristina, la muñeca de trapo, cuenta con los dedos de tela sacando la lengua."),
    "26": dict(
        titulo="Carta 26 — La caja de bloques", tipo="gris", coge=[30, 31, 35, 46], descarta=[10, 20, 24],
        descripcion=[
            "Detrás de los juguetes cambiados, el Capitán Pelusa encuentra la caja de bloques de Leo con sus instrucciones (cartas 30 y 31): «Si construimos la torre de Leo junto a la cama, podremos subir». La base de la torre es la carta 46. Dentro de la caja, Alberto encuentra dos pilas (carta 35).",
            "Coged las cartas 30, 31, 35 y 46. Descartad las cartas 10, 20 y 24."],
        pistas=["Hay un puzle: la torre de bloques y sus instrucciones.", "Las instrucciones están en dos cartas: vistas de frente y de lado (30) y desde arriba (31). Las pilas (35) son combinables.", "Coged las cartas 30, 31, 35 y 46. Descartad las cartas 10, 20 y 24."],
        arte="Una caja de bloques de construcción de colores volcada sobre la alfombra, junto a la pata de una cama enorme, con una hoja de instrucciones dibujadas. Cristina, la muñeca de trapo, levanta un bloque más grande que ella con cara de esfuerzo y Alberto, el robot de hojalata, sostiene dos pilas gigantes con una sonrisa de triunfo."),
    "30": dict(
        titulo="Carta 30 — Instrucciones (1 de 2)", tipo="gris",
        descripcion=["Las instrucciones de la torre de Leo: cómo se ve la torre de frente y desde la derecha. La base es de 3 × 3 casillas y nada puede flotar."],
        pistas=["Son las instrucciones de la torre (carta 46), junto con la carta 31.", "De frente se ve la columna más alta de cada fila de izquierda a derecha; desde la derecha, la más alta de delante a detrás.", f"Alturas: {_TORRE}."],
        arte=pieza("Instrucciones (1 de 2)", "las vistas de frente y de lado")),
    "31": dict(
        titulo="Carta 31 — Instrucciones (2 de 2)", tipo="gris",
        descripcion=["Las instrucciones de la torre de Leo: la torre vista desde arriba (qué casillas tienen algún bloque) y cuántos bloques lleva en total."],
        pistas=["Son las instrucciones de la torre (carta 46), junto con la carta 30.", "Desde arriba se ve qué casilla queda vacía. Después, ajustad las alturas con las vistas de la carta 30 y contad los bloques.", f"Alturas: {_TORRE}."],
        arte=pieza("Instrucciones (2 de 2)", "la vista desde arriba")),
    "35": dict(
        titulo="Carta 35 — Dos pilas", tipo="roja", combina=[22, 57],
        descripcion=["Dos pilas de las grandes, casi tan altas como Cristina. Combinadlas con el mando sin pilas (carta 22): sumad sus números (35 + 22 = 57) y coged la carta 57."],
        pistas=["Son pilas para algo que no funciona.", "Combinad la carta 35 con el mando (carta 22).", "Sumad los números de las dos cartas: 35 + 22 = 57."],
        arte="Dos pilas grandes de juguete, una roja y otra negra, apoyadas en un bloque de construcción sobre una alfombra infantil, vistas de cerca y enormes, con luz de lamparita."),
    "46": dict(
        titulo="Carta 46 — La torre de bloques", tipo="verde",
        descripcion=[
            "Es un juego de la app: una base de 3 × 3 casillas junto a la cama. Tocando una casilla se le añade un bloque (hasta 3; uno más y vuelve a 0). Hay que construir la torre de las instrucciones (cartas 30 y 31).",
            "Al acertar, la torre llega al borde de la cama. Coged la carta 44."],
        pistas=["Hacen falta las dos cartas de instrucciones (30 y 31).", "Empezad por la vista desde arriba (qué casilla va vacía) y usad las vistas de frente y de lado para las alturas. El total de bloques ayuda a comprobar.", f"Alturas: {_TORRE}."],
        arte="Una torre de bloques de construcción de colores a medio montar junto a la pata de una cama, con una base de nueve casillas. Alberto, el robot de hojalata, coloca un bloque con las pinzas y cara de concentración y Cristina, la muñeca de trapo, le enseña la hoja de instrucciones con la lengua entre los dientes."),
    "44": dict(
        titulo="Carta 44 — Encima de la cama", tipo="gris", coge=[38], descarta=[26, 30, 31, 46],
        descripcion=[
            "Trepáis por la torre hasta la cama de Leo, que duerme abrazado a su almohada. Junto a él, entre las sábanas, hay una llave de cuerda dorada (carta 38) que no es la de Alberto: es de algún otro juguete.",
            "Coged la carta 38. Descartad las cartas 26, 30, 31 y 46."],
        pistas=["Mirad lo que hay entre las sábanas.", "La carta 38 es combinable.", "Coged la carta 38. Descartad las cartas 26, 30, 31 y 46."],
        arte="Una cama infantil enorme vista desde el colchón, con un niño dormido abrazado a la almohada, un edredón de cohetes y la luz de la luna. Cristina, la muñeca de trapo, se tapa la boca con la mano para no reír y Alberto, el robot de hojalata, levanta de puntillas una llave de cuerda dorada con cara de sigilo."),
    "38": dict(
        titulo="Carta 38 — Llave de cuerda", tipo="azul", combina=[56, 94],
        descripcion=["Una llave de cuerda dorada, pequeña, de un juguete que no es Alberto. Combinadla con el ratón de cuerda (carta 56): sumad sus números (38 + 56 = 94) y coged la carta 94."],
        pistas=["Es la llave de cuerda de algún juguete.", "Cuando encontréis el juguete al que le falta la llave, combinadlos.", "Sumad los números de las dos cartas: 38 + 56 = 94."],
        arte="Una llave de cuerda dorada de juguete, con forma de mariposa, sobre una sábana con dibujos de cohetes, vista de cerca con luz de luna."),
    "57": dict(
        titulo="Carta 57 — El coche teledirigido", tipo="gris", coge=[48, 52, 53], descarta=[22, 35],
        descripcion=[
            "Con las pilas puestas, el coche teledirigido arranca con un zumbido y os lleva por la alfombra hasta el teatrillo de marionetas de Leo. Pipo, la marioneta, está colgada de su cruceta, con los hilos enredados (carta 52). El cartel de la función (carta 53) enseña cómo saluda Pipo; el teatrillo es la carta 48.",
            "Coged las cartas 48, 52 y 53. Descartad las cartas 22 y 35."],
        pistas=["Hay un puzle: la marioneta, sus hilos y el cartel.", "Los hilos (carta 52) dicen qué mando mueve cada brazo y cada pierna; el cartel (53), la postura.", "Coged las cartas 48, 52 y 53. Descartad las cartas 22 y 35."],
        arte="Un coche teledirigido de juguete corriendo por una alfombra con carreteras dibujadas, con Cristina, la muñeca de trapo, al volante riendo a carcajadas y Alberto, el robot de hojalata, agarrado al alerón con los ojos como platos; al fondo, un teatrillo de marionetas de madera con cortinas rojas."),
    "52": dict(
        titulo="Carta 52 — Los hilos de Pipo", tipo="gris",
        descripcion=["La cruceta de Pipo con cuatro mandos (rojo con círculo, azul con cuadrado, amarillo con triángulo y verde con estrella) y sus hilos enredados hasta las manos y los pies de la marioneta."],
        pistas=["Son los hilos de la marioneta (carta 48).", "Seguid cada hilo con el dedo desde su mando hasta la mano o el pie donde acaba.", f"Para el saludo del cartel hay que tirar de los mandos {_MANDOS}."],
        arte=pieza("Los hilos de Pipo", "la cruceta y los hilos")),
    "53": dict(
        titulo="Carta 53 — Cartel de la función", tipo="gris",
        descripcion=["El cartel de la función del teatrillo de Leo: Pipo saluda al público con una mano y un pie levantados."],
        pistas=["Es la postura que tiene que hacer la marioneta (carta 48).", "Fijaos en qué mano y qué pie levanta Pipo en el dibujo, tal como lo veis vosotros.", f"Hay que tirar de los mandos {_MANDOS}."],
        arte=pieza("Cartel de la función", "el cartel con la postura")),
    "48": dict(
        titulo="Carta 48 — La marioneta", tipo="verde",
        descripcion=[
            "Es un juego de la app: Pipo, la marioneta, y los cuatro mandos de su cruceta. Tocando un mando se tira de su hilo (y tocándolo otra vez se suelta). Hay que dejar a Pipo en la postura del cartel (carta 53); qué mando mueve cada mano y cada pie está en los hilos enredados (carta 52).",
            "Al saludar, se abre el cajón del teatrillo. Coged la carta 58."],
        pistas=["Hacen falta las dos cartas: los hilos (52) y el cartel (53).", "Primero mirad qué mano y qué pie levanta Pipo en el cartel; después seguid los hilos para saber de qué mandos tirar.", f"Tirad de los mandos {_MANDOS} y saludad."],
        arte="Un teatrillo de marionetas de madera con cortinas rojas y una marioneta de madera con gorro verde colgando de una cruceta. Alberto, el robot de hojalata, tira de un hilo con todas sus fuerzas y la lengua fuera y Cristina, la muñeca de trapo, aplaude con los ojos brillantes de ilusión."),
    "58": dict(
        titulo="Carta 58 — El cajón del teatrillo", tipo="gris", coge=[41, 43, 45, 49, 51, 66], descarta=[48, 52, 53, 57],
        descripcion=[
            "Pipo saluda y el cajón del teatrillo se abre. Dentro está el cuaderno de dibujos de Leo, con las hojas sueltas: cinco páginas de un folioscopio (cartas 41, 43, 45, 49 y 51) que se ordenan y se hojean como una animación. Junto al cajón, el tren de juguete de Leo (carta 66) espera su carga.",
            "Coged las cartas 41, 43, 45, 49, 51 y 66. Descartad las cartas 48, 52, 53 y 57."],
        pistas=["Hay un puzle: el tren y las cinco páginas del cuaderno.", "Las páginas se ordenan por el sol de la ventana (en el Modo PC, botón «Hojear»).", "Coged las cartas 41, 43, 45, 49, 51 y 66. Descartad las cartas 48, 52, 53 y 57."],
        arte="El cajón de un teatrillo de marionetas abierto, con un cuaderno de dibujos infantil de espiral y hojas sueltas, y al lado las vías y un tren de juguete de madera con cinco vagones vacíos. Cristina, la muñeca de trapo, hojea las páginas con cara de curiosidad y Alberto, el robot de hojalata, se asoma al tren con una ceja de lata levantada."),
    "41": _pagina("41"), "43": _pagina("43"), "45": _pagina("45"), "49": _pagina("49"), "51": _pagina("51"),
    "66": dict(
        titulo="Carta 66 — El tren de Leo", tipo="verde",
        descripcion=[
            "Es un juego de la app: el tren de juguete de Leo con cinco vagones y cinco juguetes en el andén. Hay que cargar un juguete en cada vagón, del primero al último, en el orden en que Leo los rodeó en su cuaderno: las cinco páginas del folioscopio ordenadas (cartas 41, 43, 45, 49 y 51).",
            "Al cargarlo bien, el tren arranca. Coged la carta 72."],
        pistas=["El orden está en el folioscopio: las cinco páginas del cuaderno de Leo.", "Ordenad las páginas por el sol de la ventana, del más alto al que ya se ha puesto, y apuntad qué juguete rodea Leo en cada una.", f"Vagones, del primero al último: {_TREN}."],
        arte="Un tren de juguete de madera con locomotora roja y cinco vagones de colores sobre unas vías que recorren la alfombra, con juguetes pequeños esperando en un andén de cartón. Cristina, la muñeca de trapo, sube un juguete a un vagón con cara de esfuerzo y Alberto, el robot de hojalata, consulta unas hojas de cuaderno con gesto pensativo."),
    "72": dict(
        titulo="Carta 72 — La estación", tipo="gris", coge=[56], descarta=[58, 41, 43, 45, 49, 51, 66],
        descripcion=[
            "El tren silba y da la vuelta al cuarto hasta la estación de cartón, junto al escritorio. Allí os espera Tic, un ratón de cuerda que ha perdido su llave (carta 56): «Yo sé trepar por el cable de la lámpara hasta el escritorio, pero sin cuerda no me muevo».",
            "Coged la carta 56. Descartad las cartas 58, 41, 43, 45, 49, 51 y 66."],
        pistas=["Mirad quién os espera en la estación.", "La carta 56 es combinable.", "Coged la carta 56. Descartad las cartas 58, 41, 43, 45, 49, 51 y 66."],
        arte="Una estación de tren de cartón pintado junto a la pata de un escritorio enorme, con un tren de juguete parado y un ratón de cuerda gris sin llave sentado en el andén con cara triste. Cristina, la muñeca de trapo, le acaricia la cabeza con ternura y Alberto, el robot de hojalata, mira hacia lo alto del escritorio con la boca abierta."),
    "56": dict(
        titulo="Carta 56 — Tic, el ratón de cuerda", tipo="roja", combina=[38, 94],
        descripcion=["Tic, un ratón de cuerda gris con orejas rosas, con un agujero en el lomo donde iba su llave. Combinadlo con la llave de cuerda (carta 38): sumad sus números (56 + 38 = 94) y coged la carta 94."],
        pistas=["Es un ratón de cuerda sin llave.", "Combinad la carta 56 con la llave de cuerda (carta 38).", "Sumad los números de las dos cartas: 56 + 38 = 94."],
        arte="Un ratón de cuerda de hojalata gris con orejas rosas y un agujero vacío en el lomo, sentado sobre un andén de cartón, visto de cerca con luz de lamparita."),
    "94": dict(
        titulo="Carta 94 — Arriba, al escritorio", tipo="gris", coge=[69, 70], descarta=[38, 56, 44, 72],
        descripcion=[
            "Con la llave puesta, Tic trepa por el cable de la lámpara con vosotros en el lomo. En el escritorio está la pista de canicas de Leo (carta 69): arriba, en la rampa de salida, esperan tres canicas, y la tercera es vuestro cristal. Las instrucciones de la caja (carta 70) explican los balancines. Si el cristal no cae en el tarro, rodará hasta una caja de la mudanza.",
            "Coged las cartas 69 y 70. Descartad las cartas 38, 56, 44 y 72."],
        pistas=["Hay un puzle: la pista de canicas y sus instrucciones.", "Las instrucciones (carta 70) dicen cómo se mueven los balancines y dónde está el tarro.", "Coged las cartas 69 y 70. Descartad las cartas 38, 56, 44 y 72."],
        arte="Un ratón de cuerda trepando por el cable de una lámpara hasta un escritorio infantil, con Cristina, la muñeca de trapo, y Alberto, el robot de hojalata, montados en su lomo: ella grita de emoción con el pelo de lana al viento y él se agarra con las pinzas con cara de vértigo. En el escritorio se ve una pista de canicas de madera con un cristal rojo brillando arriba."),
    "70": dict(
        titulo="Carta 70 — Instrucciones de la pista", tipo="gris",
        descripcion=["Las instrucciones de la pista de canicas: tres balancines que mandan la canica al lado al que apuntan y que, al pasar ella, cambian de lado; cuatro salidas (A, B, C y D) y el tarro en una de ellas. El cristal es la tercera canica."],
        pistas=["Son las instrucciones de la pista (carta 69).", "Seguid las tres canicas una a una, cambiando cada balancín por el que pasa. Lo que importa es dónde cae la tercera.", f"Colocad: {_BAL}."],
        arte=pieza("Instrucciones de la pista", "el tablero y la regla de los balancines")),
    "69": dict(
        titulo="Carta 69 — La pista de canicas", tipo="verde",
        descripcion=[
            "Es un juego de la app: la pista de canicas de Leo con tres balancines. Tocando un balancín se cambia de lado; con «Soltar las canicas» caen las tres, una tras otra, y cada balancín cambia de lado cuando pasa una. El cristal es la tercera y tiene que caer en el tarro (instrucciones, carta 70).",
            "Al caer el cristal en el tarro, lo recuperáis. Coged la carta 82."],
        pistas=["Hacen falta las instrucciones (carta 70): la regla de los balancines y dónde está el tarro.", "Probad con la cabeza: seguid las tres canicas y cambiad cada balancín por el que pasan. Podéis soltar las canicas todas las veces que queráis.", f"Colocad: {_BAL}."],
        arte="Una pista de canicas de madera sobre un escritorio, con tres balancines de colores, cuatro salidas y un tarro de cristal, y canicas brillantes rodando; arriba, un cristal rojo. Alberto, el robot de hojalata, gira un balancín con las pinzas y cara de concentración y Cristina, la muñeca de trapo, sigue una canica con la mirada y la boca abierta de emoción."),
    "82": dict(
        titulo="Carta 82 — El cristal en el tarro", tipo="gris", coge=[62], descarta=[69, 70, 94],
        descripcion=[
            "El cristal cae en el tarro con un tintineo y los juguetes estallan en vítores en voz baja, para no despertar a Leo. El Capitán Pelusa os lo saca con su pata de peluche: «Buen viaje, amigos. Y cuidad de que no os confundan con una canica».",
            "Coged la carta 62. Descartad las cartas 69, 70 y 94."],
        pistas=["El cristal está a salvo.", "La carta 62 es combinable con el Cronoportal.", "Coged la carta 62. Descartad las cartas 69, 70 y 94."],
        arte="Un tarro de canicas de cristal sobre un escritorio infantil con un cristal rojo brillante dentro, rodeado de juguetes que celebran: un oso de peluche con un parche, una marioneta y un ratón de cuerda. Cristina, la muñeca de trapo, abraza el tarro con los ojos llenos de lágrimas de alegría y Alberto, el robot de hojalata, salta de alegría con la antenita temblando."),
    "62": dict(
        titulo="Carta 62 — Cristal de energía", tipo="roja", combina=[12, 74],
        descripcion=["El cristal de energía del Cronoportal: una gema roja con un fulgor interior. Combinadlo con el Cronoportal (carta 12): sumad sus números (62 + 12 = 74) y coged la carta 74."],
        pistas=["Es la pieza que faltaba.", "Combinad la carta 62 con la carta 12.", "Sumad los números de las dos cartas: 62 + 12 = 74."],
        arte="Un cristal rojo facetado con un fulgor interior de brasa, sostenido por una pata de oso de peluche, entre canicas de colores, con luz de lamparita."),
    "74": dict(
        titulo="Carta 74 — Cronoportal reconectado", tipo="gris", coge=[99], descarta=[62, 12, 82],
        descripcion=[
            "El cristal encaja y el Cronoportal se enciende. Por la ventana empieza a clarear y se oye el motor del camión de la mudanza en la calle. Los juguetes os dicen adiós desde la estantería. Activad el aparato antes de que Leo abra los ojos.",
            "Coged la carta 99. Descartad las cartas 62, 12 y 82."],
        pistas=["El portal ya funciona. Solo queda activarlo.", "Coged la carta 99. Descartad las cartas 62, 12 y 82."],
        arte="El Cronoportal diminuto encendido, con un cristal rojo encajado y un arco de luz azul y dorada, sobre un escritorio infantil al amanecer; por la ventana se ve un camión de mudanzas. Cristina, la muñeca de trapo, dice adiós con la mano de tela a un oso de peluche con cara de pena y alegría a la vez, y Alberto, el robot de hojalata, pulsa el botón del aparato con decisión."),
    "99": dict(
        titulo="Carta 99 — De vuelta a casa (FIN)", tipo="gris", descarta=[74],
        descripcion=[
            "El anillo se abre en un arco de luz justo cuando Leo se despereza. Cristina y Alberto salen disparados del cuarto de 1995 y aterrizan en su salón... otra vez de su tamaño y de carne y hueso.",
            "Alberto se toca la cara: ya no es de lata. Cristina se ríe: en el bolsillo lleva una canica de colores de Leo. Descartad la carta 74.",
            "FIN."],
        pistas=[],
        arte="La escena ocurre DENTRO del salón de su casa actual, en el presente (sofá, estanterías con libros, plantas, una lámpara encendida y luz cálida de tarde por la ventana): acaban de VOLVER a casa. Cristina y Alberto, otra vez personas de su tamaño normal, acaban de salir de un portal circular de luz azul y dorada que se abre detrás de ellos; a través del portal todavía se ve el cuarto de un niño de los años 90 con juguetes que dicen adiós. Cristina ríe a carcajadas con una canica de colores en la mano y Alberto se palpa la cara y la barba con alivio y una sonrisa enorme. Están de cara a nosotros, aterrizando en el salón y alejándose del portal, que queda a su espalda y se está cerrando; el mundo de la aventura solo se ve a través del portal, detrás de ellos. No están entrando en el portal ni saliendo de casa: están llegando."),
}

META = dict(
    juego="El Cuarto de Leo, 1995 — La Noche de los Juguetes",
    estilo=ESTILO, personajes=PERSONAJES, hoja=HOJA, foto=FOTO, video=VIDEO,
    folioscopios={"cuaderno": {"titulo": "El cuaderno de Leo", "cartas": FOLIO["cartas_en_orden"]}},
)

SPEC = dict(
    final="99",
    needs={"26": ["24", "20"], "44": ["46", "30", "31"], "57": ["22", "35"], "58": ["48", "52", "53"],
           "72": ["66", "41", "43", "45", "49", "51"], "94": ["38", "56"], "82": ["69", "70"], "74": ["62", "12"]},
    eventos={},
)

PARA_QUE = {
    "P": "Inicio: os convertís en juguetes. Te manda coger la 10 y la 12.",
    "10": "La estantería: reparte la foto Polaroid, la estantería de ahora y el mando.",
    "12": "El Cronoportal sin cristal: se combina con el cristal de energía (62).",
    "20": "Foto Polaroid: la estantería de antes.",
    "22": "Mando sin pilas: se combina con las pilas (35).",
    "24": "La estantería (app): las cinco diferencias.",
    "26": "La caja de bloques: reparte las instrucciones, la torre y las pilas.",
    "30": "Instrucciones: vistas de frente y de lado.",
    "31": "Instrucciones: vista desde arriba y total de bloques.",
    "35": "Dos pilas: se combinan con el mando (22).",
    "38": "Llave de cuerda: se combina con el ratón (56).",
    "41": "Página del folioscopio.", "43": "Página del folioscopio.", "45": "Página del folioscopio.",
    "49": "Página del folioscopio.", "51": "Página del folioscopio.",
    "44": "Encima de la cama: reparte la llave de cuerda.",
    "46": "La torre de bloques (app): construirla con sus vistas.",
    "48": "La marioneta (app): tirar de los mandos de la postura del cartel.",
    "52": "Los hilos de Pipo: qué mando mueve cada mano y cada pie.",
    "53": "Cartel de la función: la postura.",
    "56": "Tic, el ratón de cuerda: se combina con la llave (38).",
    "57": "El coche teledirigido (22 + 35): reparte la marioneta, los hilos y el cartel.",
    "58": "El cajón del teatrillo: reparte el folioscopio y el tren.",
    "62": "Cristal de energía: se combina con el Cronoportal (12).",
    "66": "El tren de Leo (app): cargar los juguetes en el orden del folioscopio.",
    "69": "La pista de canicas (app): colocar los balancines para que el cristal caiga en el tarro.",
    "70": "Instrucciones de la pista: los balancines y el tarro.",
    "72": "La estación: reparte el ratón de cuerda.",
    "74": "Cronoportal reconectado (62 + 12): reparte la 99.",
    "82": "El cristal en el tarro: reparte el cristal.",
    "94": "Arriba, al escritorio (38 + 56): reparte la pista de canicas y sus instrucciones.",
    "99": "Final de la aventura, ya en casa.",
}

_TEXTOS = [
    ("leer", "P", "Del tamaño de un juguete", "Pon el Modo PC en el ordenador (solo debe haber la carta P en la mesa y el resto boca abajo en el mazo) y en el móvil abre el juego y pulsa Empezar. Lee la carta P: te manda coger la 10 y la 12."),
    ("leer", "10", "La estantería de Leo", "Lee la carta 10. Descarta la P y coge 20, 22 y 24."),
    ("app", "24", "La estantería", f"En el móvil: Acción, 24. Toca las cinco diferencias con la foto (carta 20): {_DIFS}. El mensaje te dice que cojas la 26.", "carta 26"),
    ("leer", "26", "La caja de bloques", "Lee la carta 26. Descarta 10, 20 y 24 y coge 30, 31, 35 y 46. Las cartas 22 y 35 son combinables."),
    ("app", "46", "La torre de bloques", f"En el móvil: Acción, 46. Con las instrucciones (cartas 30 y 31), las alturas son: {_TORRE}. El mensaje te dice que cojas la 44.", "carta 44"),
    ("leer", "44", "Encima de la cama", "Lee la carta 44. Descarta 26, 30, 31 y 46 y coge la 38, una llave de cuerda."),
    ("combinar", "22", "35", "El coche teledirigido", "El mando (22) y las pilas (35) son combinables: 22 + 35 = 57. Coge la 57."),
    ("leer", "57", "El coche teledirigido", "Lee la carta 57. Descarta 22 y 35 y coge 48, 52 y 53."),
    ("app", "48", "La marioneta", f"En el móvil: Acción, 48. Siguiendo los hilos (carta 52) para la postura del cartel (carta 53), tira de los mandos {_MANDOS} y saluda. El mensaje te dice que cojas la 58.", "carta 58"),
    ("leer", "58", "El cajón del teatrillo", "Lee la carta 58. Descarta 48, 52, 53 y 57 y coge 41, 43, 45, 49, 51 y 66. Las cinco páginas son un folioscopio: en el Modo PC, botón «Hojear»."),
    ("app", "66", "El tren de Leo", f"En el móvil: Acción, 66. Ordenadas por el sol, las páginas son {_PAGINAS}; los juguetes rodeados, en ese orden: {_TREN}. Cárgalos así. El mensaje te dice que cojas la 72.", "carta 72"),
    ("leer", "72", "La estación", "Lee la carta 72. Descarta 58, 41, 43, 45, 49, 51 y 66 y coge la 56, el ratón de cuerda."),
    ("combinar", "38", "56", "Arriba, al escritorio", "La llave (38) y el ratón (56) son combinables: 38 + 56 = 94. Coge la 94."),
    ("leer", "94", "Arriba, al escritorio", "Lee la carta 94. Descarta 38, 56, 44 y 72 y coge 69 y 70."),
    ("app", "69", "La pista de canicas", f"En el móvil: Acción, 69. Con las instrucciones (carta 70): {_BAL}. Suelta las canicas. El mensaje te dice que cojas la 82.", "carta 82"),
    ("leer", "82", "El cristal en el tarro", "Lee la carta 82. Descarta 69, 70 y 94 y coge la 62, el cristal de energía."),
    ("combinar", "12", "62", "Cristal en el Cronoportal", "El Cronoportal (12) y el cristal (62) son combinables: 12 + 62 = 74. Coge la 74."),
    ("leer", "74", "Cronoportal reconectado", "Lee la carta 74. Descarta 62, 12 y 82 y coge la 99."),
    ("leer", "99", "Final", "Lee la carta 99. Descarta la 74. En la mesa solo queda la 99. ¡Fin!"),
]


def _orden(m):
    return sorted(m, key=lambda x: (x != "P", int(x) if x != "P" else 0))


def _pasos():
    mesa = set()
    pasos = []
    for p in _TEXTOS:
        if p[0] == "leer":
            c = J[p[1]]
            for d in c.get("descarta", []):
                mesa.discard(str(d))
            for h in c.get("coge", []):
                mesa.add(str(h))
            if p[1] == "P":
                mesa = {"P", "10", "12"}
            pasos.append(dict(t=p[2], que=p[3], acciones=[("leer", p[1])], mesa=_orden(mesa)))
        elif p[0] == "app":
            mesa.add(p[4].split()[-1])
            pasos.append(dict(t=p[2], que=p[3], acciones=[("app", p[1], p[4])], mesa=_orden(mesa)))
        else:
            mesa.add(str(int(p[1]) + int(p[2])))
            pasos.append(dict(t=p[3], que=p[4], acciones=[("combinar", p[1], p[2])], mesa=_orden(mesa)))
    return pasos


PASOS = _pasos()
