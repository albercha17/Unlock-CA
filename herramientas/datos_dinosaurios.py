"""Cretácico, hace 66 millones de años: El Valle de los Gigantes — versión de 61 cartas (21 oct 2026), mucho más difícil y variada.

Once puzles que no salen en ningún otro juego de la serie, con las pistas dibujadas o en acertijo (ninguna carta explica cómo se resuelve
su puzle): huellas pisadas unas sobre otras, cabezas y patas tras los helechos, nidos y helechos (tipo «Tents»), triangulación del cráter,
desvío de la lava, la ruta de la manada (camino de Euler), el árbol de rasgos, el corral de quién se come a quién, planear con un
pterosaurio aprovechando las térmicas, la balsa que resbala por el barro y la datación por anillos de tres troncos fósiles.
Solo 15 cartas tienen a Cristina y Alberto (escenas); el resto son objetos y pistas sin personas.
Las cartas-pista las dibuja herramientas/dinosaurios.py (instancias_dinosaurios.py)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ampliacion as _amp  # noqa: E402
import instancias_dinosaurios as I  # noqa: E402

ESTILO = ("Ilustración digital semirrealista con aire de película de aventuras, luz dorada de atardecer entre vegetación exuberante del Cretácico "
          "(helechos gigantes, cícadas, coníferas), paleta de verdes profundos, ocres y naranja volcánico, con destellos azules del Cronoportal, formato vertical 2:3. "
          "Sin texto, letras ni números en la imagen; los mapas, cuadernos y paneles son solo dibujos decorativos sin escritura legible. "
          "Deja libre de detalles importantes la esquina superior izquierda y el 18 % inferior de la imagen.")

PERSONAJES = {
    "Cristina": "Cristina, mujer de 26 años, profesora, pelo rubio y rizado recogido en una coleta, ojos azules. Viste ropa de expedición paleontológica: camisa caqui remangada, chaleco de explorador con bolsillos, pantalón de campo, botas de montaña y sombrero de ala ancha.",
    "Alberto": "Alberto, hombre de 27 años, informático, pelo moreno corto, barba cuidada, ojos marrones. Viste ropa de expedición paleontológica: camiseta verde oliva, chaleco caqui con muchos bolsillos, pantalón cargo, botas de montaña, gorra y una mochila."
}

HOJA = ("Crea una hoja de personajes (character sheet) con las dos personas de la foto adjunta, de cuerpo entero y de frente, sobre fondo claro y neutro. "
        "Mantén su parecido real con la foto (cara, pelo, barba, ojos). "
        "Cristina: mujer de 26 años, profesora, pelo rubio y rizado recogido en una coleta, ojos azules, camisa caqui remangada, chaleco de explorador con bolsillos, pantalón de campo, botas de montaña y sombrero de ala ancha. "
        "Alberto: hombre de 27 años, informático, pelo moreno corto, barba cuidada, ojos marrones, camiseta verde oliva, chaleco caqui con muchos bolsillos, pantalón cargo, botas de montaña, gorra y mochila. "
        "Estilo: " + ESTILO)

FOTO = ("Antes de nada, adjunta a ChatGPT una foto de Cristina y Alberto juntos (o una de cada uno, con la cara bien visible). "
        "Pídele que mantenga el parecido real, pero con el estilo de ilustración de este juego.")

VIDEO = ("Crea un vídeo vertical 9:16 de 15 segundos, con animación semirrealista de película de aventuras, luz dorada y colores verdes y naranjas. Sin ningún texto, letra ni subtítulo en pantalla. "
         "Escena 1 (0-4 s): en el salón de una casa actual, Cristina (mujer de 26 años, rubia de pelo rizado, ojos azules) y Alberto (hombre de 27 años, moreno con barba, ojos marrones), vestidos de exploradores, rodean un aparato de latón y cristal con un anillo central: el Cronoportal. Cristina sonríe emocionada ante la foto de un fósil de dinosaurio. "
         "Escena 2 (4-8 s): el anillo se enciende con un arco de luz azul, el salón se deforma y los dos son absorbidos por un túnel de luz con destellos dorados. "
         "Escena 3 (8-12 s): caen sobre la hierba de un valle del Cretácico al atardecer, entre helechos gigantes; un enorme saurópodo cruza al fondo y un punto de luz brillante, un asteroide, cruza el cielo; el aparato humea y se apaga. "
         "Escena 4 (12-15 s): primer plano de Cristina y Alberto, asombrados, mirando al cielo; fundido a negro. "
         "Sonido: zumbido eléctrico creciente, silbido del portal, golpe sordo al aterrizar, rugidos lejanos, insectos y viento entre los helechos, música de aventura con percusión, sin voz de narrador.")

ESTILO += " Los personajes tienen siempre expresiones distintas y expresivas, adecuadas a la escena (nunca la misma cara en dos imágenes)."
SIN_GENTE = "Sin ninguna persona en la imagen. "
DOCTORA = ("la doctora Ibarra, paleontóloga de unos sesenta años, piel curtida por el sol, pelo gris recogido en una trenza, gafas remendadas con cuerda, "
           "chaqueta de expedición de hace diecisiete años llena de parches y un sombrero de ala ancha muy gastado")

MOSAICOS = {
    "manada": dict(filas=2, cols=1, cartas=["19", "21"], titulo="La manada del abrevadero"),
    "valle": dict(filas=1, cols=2, cartas=["42", "49"], titulo="El valle, de ladera a ladera"),
    "ladera": dict(filas=1, cols=2, cartas=["54", "55"], titulo="La ladera del volcán"),
    "senderos": dict(filas=1, cols=2, cartas=["37", "39"], titulo="Los senderos del valle"),
}
POS = {(2, 1): ["mitad de arriba", "mitad de abajo"], (1, 2): ["mitad izquierda", "mitad derecha"]}
_S_BARRO = ", ".join(I.BARRO["solucion"])
_S_PLANEAR = ", ".join(I.PLANEAR["solucion"])
_S_SENDEROS = " → ".join(I.SENDEROS["claros"][k] for k in I.euler(I.SENDEROS, "R"))
_NOM = {"triceratops": "tricerátops", "tiranosaurio": "tiranosaurio", "anquilosaurio": "anquilosaurio", "edmontosaurio": "edmontosaurio",
        "velociraptor": "velocirraptor", "compsognato": "compsognato", "protoceratops": "protoceratops", "pez": "pez", "cocodrilo": "cocodrilo",
        "ave primitiva": "ave primitiva"}
_S_HUELLAS = ", ".join(_NOM[e] for e in I.HUELLAS["orden"])
_S_NIDOS = ", ".join("ABCDEF"[x] + str(y + 1) for x, y in I.NIDOS["solucion"])
_S_CRATER = "ABCDEFGH"[I.CRATER["solucion"][0]] + str(I.CRATER["solucion"][1] + 1)
_S_LAVA = "ABCDEF"[I.LAVA["solucion"][0]] + str(I.LAVA["solucion"][1] + 1)
_S_ARBOL = ", ".join(_NOM[a] for a in I.ARBOL["solucion"])
_FILA = ["arriba", "abajo"]
_S_CORRAL = "; ".join(f"{_NOM[a]} {_FILA[c[1]]} {['a la izquierda', 'en el centro', 'a la derecha'][c[0]]}" for a, c in I.CORRAL["solucion"].items())
_M = I.MANADA


def codigo(que):
    return f"Carta dibujada por código (herramientas/dinosaurios.py; no se pide a ChatGPT): {que}."


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
    # ------------------------------------------------------------------ El vado
    "P": escena("P", "Llegada al Cretácico", [10, 12], [],
                "Cuarto salto del Cronoportal: el Cretácico, hace sesenta y seis millones de años. Aterrizáis en un valle de helechos gigantes y el aparato escupe su núcleo de energía, que sale rodando ladera abajo hacia un vado de barro. En el cielo brilla un punto de luz que no debería estar ahí: el asteroide. Y de vez en cuando cae alguna piedra de fuego.",
                ["Mirad a vuestro alrededor y revisad el aparato."],
                "Un valle del Cretácico superior al atardecer, con helechos gigantes, cícadas y un río; al fondo un enorme saurópodo cruza entre la bruma y en el cielo naranja brilla un punto de luz muy intenso, un asteroide. En primer plano, un aparato de latón y cristal retrofuturista (el Cronoportal) humea sobre la hierba con una luz azul que se apaga. Cristina y Alberto, con ropa de expedición, se levantan desconcertados mirando el cielo."),
    "10": escena("10", "El vado del barro", [14, 16, 18, 19, 20, 21, 22], ["P"],
                 "El rastro del núcleo acaba en un vado de barro pisoteado: esta mañana han cruzado cinco dinosaurios y uno de ellos se lo ha llevado pegado a la pata. Junto al vado, en un tronco, alguien clavó una guía de huellas dibujada a mano. Al otro lado, en el abrevadero, se oyen bufidos detrás de un muro de helechos. Y en el suelo, un rollo de cuerda que no es vuestro.",
                 ["Hay dos puzles: el orden de las huellas del barro y la manada del abrevadero.", "La manada son dos cartas: juntadlas, una encima de otra."],
                 "Un vado de barro junto a un río del Cretácico, lleno de huellas de dinosaurio pisadas unas sobre otras; en un tronco, un papel clavado con dibujos de huellas; al fondo, un muro de helechos altísimos con cabezas de dinosaurio asomando. Cristina, agachada, mide una huella con la mano abierta y cara de asombro; Alberto levanta un rollo de cuerda del suelo con el ceño fruncido de sospecha."),
    "12": combinable("12", "Cronoportal sin núcleo", "azul", 62, 74,
                     "El Cronoportal, con el anillo apagado y el hueco del núcleo de energía vacío.",
                     SIN_GENTE + "Primer plano del Cronoportal: una consola portátil de latón y cristal con dos antenas de cobre, un anillo de cristal central apagado y un hueco circular vacío en el pecho del aparato, sobre una roca cubierta de musgo, con helechos al fondo."),
    "14": app("14", "El barro del vado", "Es un juego de la app: decir en qué orden cruzaron el vado los cinco dinosaurios.", 24,
              ["El barro está en la carta 16 y la guía de huellas, con su nota, en la 18.", "Una huella que pisa a otra es de quien pasó después. Empezad por la que no pisa a ninguna.", f"En orden: {_S_HUELLAS}."],
              SIN_GENTE + "El barro de un vado del Cretácico visto desde arriba, con varias huellas grandes de dinosaurio de formas distintas pisadas unas encima de otras."),
    "16": gris("16", "El barro del vado", "El barro del vado, tal como lo encontrasteis.",
               ["Sirve para el orden de las huellas (carta 14).", "Fijaos en qué huella tapa a cuál.", f"En orden: {_S_HUELLAS}."], codigo("el barro con las huellas")),
    "18": gris("18", "Guía de huellas", "Una guía de huellas dibujada a mano, con una nota al pie.",
               ["Sirve para el orden de las huellas (carta 14).", "Cada forma de huella es de un dinosaurio distinto.", "Lo que pisa después queda encima."], codigo("la guía de huellas")),
    "19": pieza("19", "manada", "Media lámina de la manada del abrevadero.", ["Es la mitad de una lámina: juntadla con la carta 21.", "Arriba se cuentan cabezas; abajo, patas.", f"{_M['cabezas']} cabezas y {_M['patas']} patas: {_M['solucion']['triceratops']} tricerátops y {_M['solucion']['velociraptor']} velocirraptores."]),
    "21": pieza("21", "manada", "Media lámina de la manada del abrevadero.", ["Es la mitad de una lámina: juntadla con la carta 19.", "Arriba se cuentan cabezas; abajo, patas.", f"{_M['cabezas']} cabezas y {_M['patas']} patas: {_M['solucion']['triceratops']} tricerátops y {_M['solucion']['velociraptor']} velocirraptores."]),
    "20": app("20", "La manada del abrevadero", "Es un juego de la app: saber cuántos animales de cada clase hay detrás de los helechos antes de cruzar.", 28,
              ["Las cabezas y las patas están en las cartas 19 y 21.", "Los tricerátops andan a cuatro patas y los raptores a dos. Contad cabezas y patas y repartid.", f"{_M['solucion']['triceratops']} tricerátops y {_M['solucion']['velociraptor']} velocirraptores."],
              SIN_GENTE + "Un abrevadero del Cretácico tapado por un muro de helechos gigantes, con cuellos y cabezas de dinosaurio asomando por encima y patas por debajo."),
    "22": combinable("22", "Cuerda", "azul", 35, 57, "Un rollo grande de cuerda trenzada, abandonado en el vado.",
                     SIN_GENTE + "Un rollo grande de cuerda trenzada de cáñamo sobre un baúl de madera de campamento, con un mosquetón y un nudo marinero, luz cálida del atardecer."),
    "24": escena("24", "El campamento escondido", [26], [14, 16, 18],
                 "El rastro del último en cruzar os lleva a un campamento escondido entre helechos: una lona remendada, cacharros de hojalata y un cuaderno con tapas de cuero. En la primera página, una firma: «Dra. Ibarra, expedición de 2009». Alguien vino del futuro antes que vosotros... y se quedó. El cuaderno guarda un árbol dibujado con mucho cariño.",
                 ["El árbol del cuaderno servirá más adelante."],
                 "Un campamento escondido entre helechos gigantes con una lona remendada, cacharros de hojalata y un cuaderno de tapas de cuero abierto sobre una caja. Cristina lee el cuaderno con la boca abierta de sorpresa y Alberto sostiene una taza de hojalata oxidada con cara de no entender nada."),
    "26": gris("26", "El árbol de la doctora", "Un árbol de parentesco dibujado en el cuaderno, con cinco ramas vacías.",
               ["Sirve para el árbol (carta 51).", "Cada marca roja del tronco es un rasgo que tienen todos los que quedan por encima de ella.", f"De la rama 1 a la 5: {_S_ARBOL}."], codigo("el árbol de la doctora")),
    "28": escena("28", "Al otro lado del abrevadero", [35], [19, 20, 21],
                 "Cruzáis el abrevadero entre tricerátops que ni os miran. En la otra orilla hay una pared de roca, y clavado en una grieta, un garfio de escalada de hierro con las iniciales M. I. grabadas.",
                 ["Lo que habéis encontrado se puede juntar con algo que ya tenéis."],
                 "La orilla de un abrevadero del Cretácico con tricerátops bebiendo al fondo y una pared de roca con un garfio de escalada clavado en una grieta. Alberto tira del garfio con todas sus fuerzas, los dientes apretados, y Cristina vigila a los tricerátops por encima del hombro, conteniendo la respiración."),
    "35": combinable("35", "Garfio de escalada", "roja", 22, 57, "Un garfio de escalada de hierro de tres uñas, con unas iniciales grabadas.",
                     SIN_GENTE + "Un garfio de escalada de hierro de tres uñas con un anillo, sobre un paño de lona, junto a un hueso fosilizado, con tierra aún pegada."),
    "57": escena("57", "Lo alto del acantilado", [31, 32], [22, 35, 10, 28],
                 "Con la cuerda y el garfio trepáis a lo alto del acantilado. Desde arriba se ve todo el valle: a un lado, una playa llena de nidos y, detrás, una tienda de lona; al otro, la ladera humeante del volcán y un claro donde acaba de caer una piedra de fuego.",
                 ["Hay dos caminos: la playa de los nidos y el valle del volcán. Podéis seguir los dos."],
                 "Lo alto de un acantilado del Cretácico al atardecer, con una cuerda y un garfio enganchados al borde; abajo, una playa con nidos y al fondo un volcán humeante y una columna de humo donde ha caído un meteorito. Cristina, agarrada a la cuerda, asoma la cabeza con una sonrisa de triunfo; Alberto, ya arriba, señala el humo con el brazo extendido y cara de alarma."),
    # ------------------------------------------------------------------ Rama 1: la playa de los nidos
    "31": escena("31", "La playa de los nidos", [40, 41, 43, 45], [],
                 "Una playa de arena negra salpicada de helechos, donde las madres maiasaura entierran sus huevos. Para llegar a la tienda del fondo hay que pasar entre los nidos sin pisar ninguno, y están tan bien tapados que no se ven. La doctora los vigilaba desde dos sitios distintos.",
                 ["Hay que saber dónde está cada nido sin verlos."],
                 SIN_GENTE + "Una playa de arena negra con helechos dispersos y madres maiasaura vigilando montículos de arena; al fondo, una tienda de lona; a un lado un acantilado y al sur una duna."),
    "40": app("40", "La playa de los nidos", "Es un juego de la app: marcar dónde están los nidos de la playa.", 30,
              ["Cuántos huevos se ven por fila y por columna: cartas 41 y 43. La costumbre de las madres: carta 45.", "Cada nido, pegado de lado a su helecho, y ningún nido toca a otro ni en diagonal. Empezad por las columnas sin huevos.", f"Nidos en {_S_NIDOS}."],
              SIN_GENTE + "Una playa de arena negra vista desde arriba como un tablero, con helechos dispersos y la arena lisa, sin que se vean los nidos."),
    "41": gris("41", "Desde el acantilado oeste", "Los huevos que se veían en cada fila de la playa.",
               ["Sirve para los nidos (carta 40).", "Cada fila, tantos nidos como huevos.", f"Nidos en {_S_NIDOS}."], codigo("la playa desde el oeste")),
    "43": gris("43", "Desde la duna del sur", "Los huevos que se veían en cada columna de la playa.",
               ["Sirve para los nidos (carta 40).", "Cada columna, tantos nidos como huevos.", f"Nidos en {_S_NIDOS}."], codigo("la playa desde el sur")),
    "45": gris("45", "Las madres maiasaura", "Lo que anotó la doctora sobre las madres.",
               ["Sirve para los nidos (carta 40).", "Un nido por helecho, de lado; los nidos no se tocan ni en diagonal.", f"Nidos en {_S_NIDOS}."], codigo("la costumbre de las madres")),
    "30": escena("30", "La tienda de la playa", [38], [31, 40, 41, 43, 45],
                 "Llegáis a la tienda sin despertar a ninguna madre. Dentro hay un catre, un mapa de una ciénaga clavado en un poste y una nota: «El raptor guarda lo brillante en su cueva de la ciénaga. De noche no se ve nada: linterna». La linterna está ahí, pero sin pilas.",
                 ["La linterna necesita energía: buscad una batería."],
                 "El interior de una tienda de lona remendada con un catre, un mapa clavado en un poste y una linterna de metal sobre una caja. Cristina enciende y apaga la linterna sin éxito, con un mohín de fastidio, y Alberto lee la nota del poste rascándose la barba, pensativo."),
    "38": combinable("38", "Linterna sin pilas", "roja", 56, 94, "Una linterna de campaña grande, con el compartimento de las pilas vacío.",
                     SIN_GENTE + "Una linterna de campaña grande de metal oxidado con un foco ancho y un compartimento de pilas abierto y vacío, sobre una roca cubierta de musgo."),
    # ------------------------------------------------------------------ Rama 2: el valle del volcán
    "32": escena("32", "La atalaya", [42, 48, 49, 53], [],
                 "Bajáis hacia el humo y encontráis una atalaya de troncos con un mapa del valle cuadriculado y un cuaderno de vigías: tres puestos vieron caer la piedra de fuego anoche, cada uno desde su sitio. Quien la vio caer quizá siga allí.",
                 ["El mapa son dos cartas: juntadlas. Los tres vigías os dicen hacia dónde miraron."],
                 "Una atalaya de troncos atados con lianas en lo alto de una colina del Cretácico, con un mapa cuadriculado clavado en una tabla y una brújula colgando; al fondo, una columna de humo. Alberto sube por la escalerilla con el gesto tenso de vértigo y Cristina, abajo, sostiene la brújula muy concentrada, mordiéndose el labio."),
    "48": app("48", "El cráter", "Es un juego de la app: marcar en el valle la casilla donde cayó la piedra de fuego.", 36,
              ["El mapa del valle, con los tres puestos, está en las cartas 42 y 49; lo que vio cada vigía, en la carta 53.", "Trazad en el mapa una línea recta desde cada vigía hacia donde apunta su flecha: las tres se cruzan en un solo sitio.", f"El cráter está en {_S_CRATER}."],
              SIN_GENTE + "Un valle del Cretácico visto desde lo alto de una colina, cuadriculado como un tablero, con una columna de humo lejana."),
    "42": pieza("42", "valle", "Media hoja del mapa del valle.", ["Es la mitad de un mapa: juntadla con la carta 49.", "Las letras van de oeste a este y los números de norte a sur.", f"El cráter está en {_S_CRATER}."]),
    "49": pieza("49", "valle", "Media hoja del mapa del valle.", ["Es la mitad de un mapa: juntadla con la carta 42.", "Las letras van de oeste a este y los números de norte a sur.", f"El cráter está en {_S_CRATER}."]),
    "53": gris("53", "Los tres vigías", "Lo que vio cada vigía, cada uno desde su sitio.",
               ["Sirve para el cráter (carta 48).", "Cada flecha marca una dirección desde su puesto, en línea recta, también en diagonal.", f"El cráter está en {_S_CRATER}."], codigo("las tres rosas de los vientos")),
    "36": escena("36", "La doctora Ibarra", [52, 54, 55, 59], [32, 42, 48, 49, 53],
                 "Al borde del cráter os espera una mujer de pelo gris, con gafas remendadas: «¡Gente del futuro! Soy la doctora Ibarra. Mi portal se rompió hace años y aquí sigo». No hay tiempo para abrazos: la piedra de fuego ha despertado al volcán y va a escupir lava por la ladera, justo hacia los nidos. Ella apuntó la altura de cada palmo de la ladera.",
                 ["Las alturas de la ladera son dos cartas: juntadlas."],
                 "El borde de un cráter humeante en un valle del Cretácico, con un volcán rugiendo al fondo. " + DOCTORA[0].upper() + DOCTORA[1:] + ", abraza a Cristina, que se ha quedado con los ojos como platos de la emoción, mientras Alberto, con la boca abierta, mira alternativamente a la doctora y al volcán."),
    "52": app("52", "La lava", "Es un juego de la app: poner una roca para que la lava no llegue a los nidos.", 44,
              ["Las alturas están en las cartas 54 y 55; cómo baja la lava, en la carta 59.", "Seguid la lava desde el volcán: de cada casilla va a la vecina más baja de las cuatro. La roca tiene que estar en su camino y obligarla a ir por otro.", f"La roca va en {_S_LAVA}."],
              SIN_GENTE + "La ladera de un volcán del Cretácico vista desde arriba, cuadriculada, con un cráter humeante arriba y unos nidos de huevos abajo."),
    "54": pieza("54", "ladera", "Media hoja de las alturas de la ladera.", ["Es la mitad de un mapa: juntadla con la carta 55.", "Los números son alturas: la lava va siempre a la vecina más baja.", f"La roca va en {_S_LAVA}."]),
    "55": pieza("55", "ladera", "Media hoja de las alturas de la ladera.", ["Es la mitad de un mapa: juntadla con la carta 54.", "Los números son alturas: la lava va siempre a la vecina más baja.", f"La roca va en {_S_LAVA}."]),
    "59": gris("59", "La canción de los volcanes", "Una canción de la doctora sobre la lava.",
               ["Sirve para la lava (carta 52).", "De cada casilla, a la vecina más baja de las cuatro; si ninguna es más baja, se para.", f"La roca va en {_S_LAVA}."], codigo("la canción de los volcanes")),
    "44": escena("44", "El refugio de la doctora", [33, 37, 39, 46, 51, 61, 63], [36, 52, 54, 55, 59],
                 "La lava se enfría lejos de los nidos y la doctora os lleva a su refugio, una cueva seca llena de dibujos. Os cuenta que guarda una batería de su viejo portal escondida donde duermen los edmontosaurios, y que su corral lo encontraréis en su cofre... cuyo cierre es el árbol de su cuaderno.",
                 ["Hay dos puzles: la ruta de la manada y el árbol del cofre. El árbol del cuaderno sirve aquí."],
                 "El interior de una cueva seca con las paredes llenas de dibujos de dinosaurios a carbón, un cofre de madera con cinco huecos en la tapa y una lámpara de aceite. " + DOCTORA[0].upper() + DOCTORA[1:] + ", dibuja un mapa con un palo; Alberto la escucha con una sonrisa admirada y Cristina examina el cofre con la nariz casi pegada, intrigada."),
    "46": app("46", "La ruta de la manada", "Es un juego de la app: seguir a los edmontosaurios por todo el valle hasta donde duermen.", 56,
              ["El mapa de los senderos está en las cartas 37 y 39; la costumbre de la manada, en la carta 33.", "Salen de la Roca Alta y pisan todos los senderos una sola vez. Un claro con un número impar de senderos solo puede ser el principio o el final.", f"Un recorrido que vale: {_S_SENDEROS}."],
              SIN_GENTE + "Un valle del Cretácico al alba con una manada de edmontosaurios en fila por un sendero entre helechos y varios claros a lo lejos."),
    "37": pieza("37", "senderos", "Media hoja del mapa de los senderos.", ["Es la mitad de un mapa: juntadla con la carta 39.", "Contad los senderos que salen de cada claro.", f"Un recorrido que vale: {_S_SENDEROS}."]),
    "39": pieza("39", "senderos", "Media hoja del mapa de los senderos.", ["Es la mitad de un mapa: juntadla con la carta 37.", "Contad los senderos que salen de cada claro.", f"Un recorrido que vale: {_S_SENDEROS}."]),
    "33": gris("33", "La ruta de los edmontosaurios", "Lo que anotó la doctora sobre la manada.",
               ["Sirve para la ruta de la manada (carta 46).", "Todos los senderos, ninguno dos veces, empezando en la Roca Alta.", f"Un recorrido que vale: {_S_SENDEROS}."], codigo("la costumbre de la manada")),
    "56": combinable("56", "Batería de campaña", "roja", 38, 94, "La batería del viejo portal de la doctora, todavía con algo de carga.",
                     SIN_GENTE + "Una batería de campaña de color verde militar con dos bornes de latón y un asa, sobre una mesa de madera, con luz de lámpara."),
    "51": app("51", "El cofre del árbol", "Es un juego de la app: el cierre del cofre de la doctora, con cinco ramas donde va un animal cada una.", 58,
              ["El árbol está en la carta 26 y los animales, con sus rasgos dibujados, en las fichas 61 y 63.", "Cada marca roja del tronco es un rasgo que tienen todos los de las ramas que salen por encima de ella. La rama 1 no tiene ninguno.", f"De la rama 1 a la 5: {_S_ARBOL}."],
              SIN_GENTE + "La tapa de un cofre de madera con un árbol tallado de cinco ramas vacías y cinco fichas de hueso con animales grabados al lado."),
    "61": gris("61", "Fichas de la doctora (I)", "Tres animales dibujados por la doctora, con sus rasgos.",
               ["Sirve para el árbol (carta 51).", "Contad los rasgos de cada animal.", f"De la rama 1 a la 5: {_S_ARBOL}."], codigo("fichas I")),
    "63": gris("63", "Fichas de la doctora (II)", "Dos animales más dibujados por la doctora, con sus rasgos.",
               ["Sirve para el árbol (carta 51).", "Contad los rasgos de cada animal.", f"De la rama 1 a la 5: {_S_ARBOL}."], codigo("fichas II")),
    "58": escena("58", "El cofre abierto", [69, 70, 71], [51, 61, 63, 26, 24],
                 "El cofre se abre con un chasquido. Dentro, el plano del corral donde la doctora encierra de noche a los animales que ha criado, y su regla de oro dibujada en la tapa. Ya anochece y los animales andan sueltos: hay que encerrarlos antes de que alguno acabe en el estómago de otro.",
                 ["Hay que encerrar a cada animal en su cercado."],
                 "Un cofre de madera abierto en una cueva, con un plano dibujado y una tapa llena de flechas pintadas; por la entrada se ve el atardecer y siluetas de dinosaurios pequeños. Cristina despliega el plano con una sonrisa traviesa y Alberto mira hacia la entrada con cara de preocupación, sujetando una antorcha."),
    "69": app("69", "El corral", "Es un juego de la app: meter a los seis animales en los seis cercados para pasar la noche.", 80,
              ["Quién come a quién está en la carta 70; el plano, con quien ya estaba dentro, en la 71.", "El tiranosaurio y el velocirraptor son los más peligrosos: ponedlos lejos de sus presas.", f"{_S_CORRAL}."],
              SIN_GENTE + "Un corral de troncos con seis cercados de noche, a la luz de la luna, con dinosaurios pequeños y grandes esperando fuera."),
    "70": gris("70", "Quién se come a quién", "Las flechas que la doctora pintó en la tapa del cofre.",
               ["Sirve para el corral (carta 69).", "La flecha va del que come al que se come: esos dos no pueden compartir pared.", f"{_S_CORRAL}."], codigo("la red de quién se come a quién")),
    "71": gris("71", "El plano del corral", "El plano de los seis cercados, con un animal que ya estaba dentro.",
               ["Sirve para el corral (carta 69).", "El compsognato ya está en su sitio: empezad por él.", f"{_S_CORRAL}."], codigo("el plano del corral")),
    "80": escena("80", "El Quetzal", [72, 75, 79], [58, 69, 70, 71],
                 "Noche tranquila. Al amanecer, un pterosaurio enorme se posa en la cerca: es el Quetzal, la montura de la doctora. «La cueva del raptor solo se ve bien desde su nido, en lo alto del acantilado. Él os llevará, pero no sabe aletear: solo planea». En la cueva hay un dibujo del cielo con los remolinos de aire caliente.",
                 ["Para llegar al nido hay que aprovechar el aire caliente."],
                 "Un enorme pterosaurio de cresta roja posado en la cerca de un corral de troncos al amanecer. Alberto le acaricia el pico con una mezcla de miedo y fascinación y Cristina, ya subida a su lomo, se agarra con fuerza y suelta una carcajada nerviosa; " + DOCTORA + ", les hace señas desde abajo."),
    "72": app("72", "Planear con el Quetzal", "Es un juego de la app: llevar al Quetzal planeando del acantilado hasta su nido sin tocar el suelo.", 82,
              ["El cielo, con montañas y remolinos, está en la carta 75; cómo planea, en la carta 79.", "Cada casilla cuesta un palmo y cada remolino da tantos palmos como vueltas tiene, solo la primera vez. Pasad por varios.", f"Un vuelo que vale: {_S_PLANEAR}."],
              SIN_GENTE + "Un pterosaurio planeando sobre un valle del Cretácico al amanecer, entre montañas, con remolinos de aire caliente que suben del suelo."),
    "75": gris("75", "El cielo del acantilado", "El cielo del valle dibujado desde lo alto: montañas, remolinos y el nido.",
               ["Sirve para planear (carta 72).", "Contad las vueltas de cada remolino: son los palmos que sube.", f"Un vuelo que vale: {_S_PLANEAR}."], codigo("el cielo con las térmicas")),
    "79": gris("79", "Cómo planea el Quetzal", "Lo que sabe la doctora del vuelo de su pterosaurio.",
               ["Sirve para planear (carta 72).", "Cada casilla, un palmo menos; cada remolino, la primera vez, palmos de más.", "Las montañas no se cruzan."], codigo("cómo planea el Quetzal")),
    "82": escena("82", "El nido en lo alto", [85, 86, 87, 76], [80, 72, 75, 79],
                 "El Quetzal se posa en su nido, en lo alto del acantilado. Desde aquí se ve la boca de la cueva del raptor, en mitad de la ciénaga. Entre las ramas del nido, la doctora escondió lo que le queda de su portal: un calibrador de latón. «Para volver a casa, el portal tiene que saber cuántos años llevo aquí. Perdí la cuenta... pero los árboles no la pierden». Al lado, tres cortes de tronco.",
                 ["El calibrador se resuelve con los tres troncos, pero necesitará el Cronoportal en marcha."],
                 "Un gran nido de ramas en lo alto de un acantilado del Cretácico con un pterosaurio posado, un calibrador de latón entre las ramas y tres rodajas de tronco fósil. Cristina sostiene el calibrador contra el sol con cara de asombro y Alberto, despeinado por el vuelo, mira hacia abajo con vértigo, abrazado a una rama."),
    "85": app("85", "El calibrador", "Es un juego de la app: decirle al calibrador cuántos años lleva la doctora en el Cretácico, para que el Cronoportal se la lleve con vosotros.", 99,
              ["Los tres troncos están en las cartas 86, 87 y 76. Cada anillo es un año.", "El tronco del río tiene trozos con el mismo dibujo de anillos que los otros dos: alineadlos y contad los años desde el último anillo del tronco del volcán hasta el último del de la entrada.", f"Lleva {I.ANILLOS['solucion']} años."],
              SIN_GENTE + "Un calibrador de latón con dos ruedas de números y una aguja, apoyado entre tres rodajas de tronco fósil con anillos marcados."),
    "86": gris("86", "Tronco fósil del volcán", "El corte de un tronco quemado en la gran erupción.",
               ["Sirve para el calibrador (carta 85).", "Su último anillo es el año en que llegó la doctora.", f"Lleva {I.ANILLOS['solucion']} años."], codigo("tronco del volcán")),
    "87": gris("87", "Tronco fósil del río", "El corte de un tronco que arrastró el río.",
               ["Sirve para el calibrador (carta 85).", "Buscad en él el final del tronco del volcán y el principio del de la entrada.", f"Lleva {I.ANILLOS['solucion']} años."], codigo("tronco del río")),
    "76": gris("76", "Tronco de la entrada", "El corte del tronco que cayó esta mañana en la entrada de la cueva.",
               ["Sirve para el calibrador (carta 85).", "Su último anillo es este mismo año.", f"Lleva {I.ANILLOS['solucion']} años."], codigo("tronco de la entrada")),
    # ------------------------------------------------------------------ La ciénaga y el final
    "94": escena("94", "La ciénaga de noche", [64, 66, 67], [38, 56, 30, 44, 33, 37, 39, 46],
                 "Con la batería, la linterna da una luz potente. Bajáis a la ciénaga al caer la noche: el barro es tan resbaladizo que solo se puede cruzar en una balsa de troncos, y la cueva del raptor no se ve desde la orilla. La doctora dibujó la ciénaga desde un árbol.",
                 ["La cueva solo está dibujada en la carta 66."],
                 "Una ciénaga del Cretácico de noche, con barro brillante, rocas y una balsa de troncos en la orilla, iluminada por el haz de una linterna. Cristina sostiene la linterna en alto con gesto decidido y Alberto empuja la balsa con un palo, resbalando, con cara de susto cómico."),
    "64": app("64", "La balsa en el barro", "Es un juego de la app: llevar la balsa por el barro hasta la boca de la cueva.", 62,
              ["La cueva está en la carta 66; cómo resbala la balsa, en la carta 67.", "La balsa solo se para al chocar: buscad qué roca la detiene justo en la cueva y llegad a ella hacia atrás.", f"Los empujones: {_S_BARRO}."],
              SIN_GENTE + "Una ciénaga de barro brillante de noche vista desde arriba, con rocas dispersas y una balsa de troncos en una esquina."),
    "66": gris("66", "La ciénaga desde el árbol", "El dibujo de la ciénaga que hizo la doctora, con la cueva.",
               ["Sirve para la balsa (carta 64).", "La boca de la cueva es el círculo negro.", f"Los empujones: {_S_BARRO}."], codigo("la ciénaga desde el árbol")),
    "67": gris("67", "Grabado en la balsa", "Una advertencia grabada en los troncos de la balsa.",
               ["Sirve para la balsa (carta 64).", "Resbala hasta chocar; hay que pararse en la cueva, no pasar por encima.", f"Los empujones: {_S_BARRO}."], codigo("la advertencia de la balsa")),
    "62": combinable("62", "Núcleo de energía", "roja", 12, 74, "El núcleo de energía del Cronoportal, rescatado de la cueva del raptor, todavía brillante.",
                     SIN_GENTE + "Una esfera de cristal azul con un fulgor interior y finas líneas de energía, sostenida sobre la palma de una mano con un guante, sobre un fondo de cueva con luz de linterna."),
    "74": escena("74", "Cronoportal reconectado", [], [62, 12, 64, 66, 67, 94, 57],
                 "El núcleo encaja con un zumbido y el anillo del Cronoportal se enciende. En el cielo, el asteroide ya es una bola de fuego. La doctora os mira con los ojos húmedos: «¿Hay sitio para una más?». El portal la llevará... en cuanto el calibrador sepa cuántos años lleva aquí.",
                 ["Falta el calibrador."],
                 "El Cronoportal encendido con el núcleo azul encajado en su pecho, en lo alto de un acantilado del Cretácico de noche, con un asteroide enorme ardiendo en el cielo. Alberto ajusta las antenas con una sonrisa de alivio y Cristina toma de la mano a " + DOCTORA + ", que mira el aparato con lágrimas en los ojos."),
    "99": escena("99", "De vuelta a casa (FIN)", [], [74, 82, 85, 86, 87, 76],
                 "El calibrador marca los años exactos y el portal se abre de golpe. Saltáis los tres justo cuando el cielo se vuelve blanco. Aterrizáis en vuestro salón, cubiertos de barro, con una paleontóloga que no ve su siglo desde hace diecisiete años. La doctora Ibarra mira el sofá, la lámpara, la nevera... y se echa a reír. FIN.",
                 [],
                 "La escena ocurre DENTRO del salón de su casa actual, en el presente (sofá, estanterías con libros, plantas, una lámpara encendida y luz cálida de tarde por la ventana): acaban de VOLVER a casa. Cristina y Alberto acaban de salir de un portal circular de luz azul y dorada que se abre detrás de ellos, junto a " + DOCTORA + "; a través del portal todavía se ven el cielo naranja del Cretácico, el asteroide y un pterosaurio. Llevan aún su ropa de expedición con barro. Cristina ríe a carcajadas, Alberto suelta un suspiro de alivio divertido y la doctora se ríe mirando la lámpara del techo. Están de cara a nosotros, aterrizando en el salón y alejándose del portal, que queda a su espalda y se está cerrando; el mundo de la aventura solo se ve a través del portal, detrás de ellos. No están entrando en el portal ni saliendo de casa: están llegando."),
}

META = dict(juego="Cretácico — El Valle de los Gigantes", estilo=ESTILO, personajes=PERSONAJES, hoja=HOJA, foto=FOTO, video=VIDEO,
            mosaicos={k: dict(filas=m["filas"], cols=m["cols"], cartas=m["cartas"], titulo=m["titulo"]) for k, m in MOSAICOS.items()})

SPEC = dict(final="99", needs={
    "24": ["14", "16", "18"], "28": ["20", "19", "21"], "57": ["22", "35"], "30": ["40", "41", "43", "45"], "36": ["48", "42", "49", "53"],
    "44": ["52", "54", "55", "59"], "56": ["46", "37", "39", "33"], "58": ["51", "26", "61", "63"], "80": ["69", "70", "71"], "94": ["38", "56"],
    "62": ["64", "66", "67"], "82": ["72", "75", "79"], "74": ["12", "62"], "99": ["85", "86", "87", "76", "74"]}, eventos={})

PARA_QUE = {k: c["titulo"].split("— ", 1)[1] for k, c in J.items()}

_T = [
    ("leer", "P", "Llegada", "Pon el Modo PC (solo la P en la mesa) y en el móvil pulsa Empezar. Lee la carta P: coge la 10 y la 12."),
    ("leer", "10", "El vado del barro", "Lee la carta 10. Descarta la P y coge 14, 16, 18, 19, 20, 21 y 22. Junta la manada: 19 arriba y 21 abajo."),
    ("app", "14", "El barro del vado", f"En el móvil: Acción, 14. Por las huellas que pisan a otras (16 y 18): {_S_HUELLAS}. El mensaje te dice que cojas la 24.", "carta 24"),
    ("leer", "24", "El campamento escondido", "Lee la carta 24. Descarta 14, 16 y 18 y coge la 26 (guárdala para el árbol)."),
    ("app", "20", "La manada", f"En el móvil: Acción, 20. {_M['cabezas']} cabezas y {_M['patas']} patas (19 y 21): {_M['solucion']['triceratops']} tricerátops y {_M['solucion']['velociraptor']} velocirraptores. El mensaje te dice que cojas la 28.", "carta 28"),
    ("leer", "28", "Al otro lado", "Lee la carta 28. Descarta 19, 20 y 21 y coge la 35."),
    ("combinar", "22", "35", "Cuerda y garfio", "La cuerda (22) y el garfio (35) son combinables: 22 + 35 = 57. Coge la 57."),
    ("leer", "57", "Lo alto del acantilado", "Lee la carta 57. Descarta 22, 35, 10 y 28 y coge 31 y 32."),
    ("leer", "31", "La playa de los nidos", "Lee la carta 31. Coge 40, 41, 43 y 45."),
    ("app", "40", "Los nidos", f"En el móvil: Acción, 40. Con las vistas (41 y 43) y la costumbre (45): nidos en {_S_NIDOS}. El mensaje te dice que cojas la 30.", "carta 30"),
    ("leer", "30", "La tienda de la playa", "Lee la carta 30. Descarta 31, 40, 41, 43 y 45 y coge la 38."),
    ("leer", "32", "La atalaya", "Lee la carta 32. Coge 42, 48, 49 y 53. Junta el mapa: 42 a la izquierda y 49 a la derecha."),
    ("app", "48", "El cráter", f"En el móvil: Acción, 48. Las tres flechas de los vigías (53) se cruzan en el mapa (42 y 49) en {_S_CRATER}. El mensaje te dice que cojas la 36.", "carta 36"),
    ("leer", "36", "La doctora Ibarra", "Lee la carta 36. Descarta 32, 42, 48, 49 y 53 y coge 52, 54, 55 y 59. Junta la ladera: 54 a la izquierda y 55 a la derecha."),
    ("app", "52", "La lava", f"En el móvil: Acción, 52. Siguiendo siempre la vecina más baja (54, 55 y 59), la roca va en {_S_LAVA}. El mensaje te dice que cojas la 44.", "carta 44"),
    ("leer", "44", "El refugio", "Lee la carta 44. Descarta 36, 52, 54, 55 y 59 y coge 33, 37, 39, 46, 51, 61 y 63. Junta los senderos: 37 a la izquierda y 39 a la derecha."),
    ("app", "46", "La ruta de la manada", f"En el móvil: Acción, 46. Todos los senderos una vez desde la Roca Alta (37, 39 y 33): {_S_SENDEROS}. El mensaje te dice que cojas la 56.", "carta 56"),
    ("app", "51", "El cofre del árbol", f"En el móvil: Acción, 51. Con el árbol (26) y las fichas (61 y 63): {_S_ARBOL}. El mensaje te dice que cojas la 58.", "carta 58"),
    ("leer", "58", "El cofre abierto", "Lee la carta 58. Descarta 51, 61, 63, 26 y 24 y coge 69, 70 y 71."),
    ("app", "69", "El corral", f"En el móvil: Acción, 69. Sin depredador pared con pared con su presa (70) y con el compsognato en su sitio (71): {_S_CORRAL}. El mensaje te dice que cojas la 80.", "carta 80"),
    ("leer", "80", "El Quetzal", "Lee la carta 80. Descarta 58, 69, 70 y 71 y coge 72, 75 y 79."),
    ("app", "72", "Planear", f"En el móvil: Acción, 72. Pasando por los remolinos (75 y 79): {_S_PLANEAR}. El mensaje te dice que cojas la 82.", "carta 82"),
    ("leer", "82", "El nido en lo alto", "Lee la carta 82. Descarta 80, 72, 75 y 79 y coge 85, 86, 87 y 76."),
    ("combinar", "38", "56", "La linterna", "La linterna (38) y la batería (56) son combinables: 38 + 56 = 94. Coge la 94."),
    ("leer", "94", "La ciénaga de noche", "Lee la carta 94. Descarta 38, 56, 30, 44, 33, 37, 39 y 46 y coge 64, 66 y 67."),
    ("app", "64", "La balsa", f"En el móvil: Acción, 64. Hasta la cueva de la carta 66, resbalando hasta chocar (67): {_S_BARRO}. El mensaje te dice que cojas la 62.", "carta 62"),
    ("combinar", "12", "62", "El núcleo", "El Cronoportal (12) y el núcleo (62) son combinables: 12 + 62 = 74. Coge la 74."),
    ("leer", "74", "Cronoportal reconectado", "Lee la carta 74. Descarta 62, 12, 64, 66, 67, 94 y 57."),
    ("app", "85", "El calibrador", f"En el móvil: Acción, 85. Alineando los anillos de los tres troncos (86, 87 y 76): {I.ANILLOS['solucion']} años. El mensaje te dice que cojas la 99.", "carta 99"),
    ("leer", "99", "Final", "Lee la carta 99. Descarta 74, 82, 85, 86, 87 y 76. En la mesa solo queda la 99. ¡Fin!"),
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
