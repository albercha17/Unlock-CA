"""Érase una vez: El Libro de los Finales Felices — versión de 60 cartas (21 oct 2026), mucho más difícil y variada que la primera.

Diez puzles de tipos distintos, con las pistas como acertijos o dibujadas (ninguna carta explica cómo se resuelve su puzle): el cartel de
palitos de canela, el puente de los duendes contra la vela del troll, los saltos al pasado, las botas de siete leguas en un bosque a oscuras,
la habichuela que crece día a día, la vidriera de la torre, las hadas que mienten, los rayos de luna, los tarros de colores, la caja de
música y la última página (metapuzle con las letras que deja cada puzle: PERDICES). Solo 15 cartas tienen a Cristina y Alberto (escenas); el
resto son objetos y pistas sin personas. Las cartas-pista las dibuja herramientas/cuento.py (instancias_cuento.py)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ampliacion as _amp  # noqa: E402
import instancias_cuento as I  # noqa: E402

_S_BOTAS = ", ".join(I.BOTAS["solucion"])

ESTILO = ("Ilustración de dibujos animados 2D clásicos de cuento: trazo de tinta limpio, colores vivos y suaves como de acuarela, "
          "personajes con ojos grandes y muy expresivos, fondos pintados con detalle y luz mágica con destellos dorados, "
          "paleta de morados, azules profundos, rosas y oro, formato vertical 2:3. "
          "Sin texto, letras ni números en la imagen; los libros, carteles y pergaminos son solo dibujos decorativos sin escritura legible. "
          "Deja libre de detalles importantes la esquina superior izquierda y el 18 % inferior de la imagen. "
          "Los personajes tienen siempre expresiones distintas y expresivas, adecuadas a la escena (nunca la misma cara en dos imágenes).")

PERSONAJES = {
    "Cristina": "Cristina, versión de dibujos animados 2D clásicos: mujer joven de pelo rubio y rizado recogido en una coleta, ojos azules grandes y expresivos. "
                "Viste de cuento: vestido de aventurera de lana verde con una capa corta con capucha azul, botas marrones y un bolsito de cuero.",
    "Alberto": "Alberto, versión de dibujos animados 2D clásicos: hombre joven de pelo moreno corto, barba cuidada, ojos marrones grandes y expresivos. "
               "Viste de cuento: chaleco de cuero sobre camisa blanca de mangas anchas, pantalón de montar, botas altas y una gorra con una pluma pequeña."
}

HOJA = ("Crea una hoja de personajes (character sheet) con las dos personas de la foto adjunta transformadas en personajes de dibujos animados 2D clásicos, "
        "de cuerpo entero y de frente, sobre fondo claro y neutro. Mantén su parecido con la foto (cara, pelo, barba, ojos), pero dibujados al estilo de una película de animación clásica. "
        "Cristina: mujer joven de pelo rubio y rizado recogido en una coleta, ojos azules grandes, vestido de aventurera de lana verde, capa corta con capucha azul, botas marrones y bolsito de cuero. "
        "Alberto: hombre joven de pelo moreno corto, barba cuidada, ojos marrones grandes, chaleco de cuero sobre camisa blanca de mangas anchas, pantalón de montar, botas altas y gorra con una pluma pequeña. "
        "Muestra a cada uno con varias expresiones faciales distintas (alegría, sorpresa, miedo, duda, concentración, esfuerzo). Estilo: " + ESTILO)

FOTO = ("Antes de nada, adjunta a ChatGPT una foto de Cristina y Alberto juntos (o una de cada uno, con la cara bien visible). "
        "Pídele que mantenga el parecido, pero dibujados como personajes de dibujos animados 2D clásicos, y que en cada imagen tengan EXPRESIONES DISTINTAS.")

VIDEO = ("Crea un vídeo vertical 9:16 de 15 segundos, con animación 2D clásica de cuento, colores vivos, morados y dorados. Sin ningún texto, letra ni subtítulo en pantalla. "
         "Escena 1 (0-4 s): en el salón de una casa actual, Cristina (mujer de 26 años, rubia de pelo rizado, ojos azules) y Alberto (hombre de 27 años, moreno con barba, ojos marrones) rodean un aparato de latón y cristal con un anillo central: el Cronoportal. Sobre la mesa hay un viejo libro de cuentos; Cristina lo abre con ilusión. "
         "Escena 2 (4-8 s): el anillo se enciende con un arco de luz azul y dorada, y los dos son absorbidos por las páginas del libro: sus cuerpos se convierten en dibujos animados 2D de trazo limpio. "
         "Escena 3 (8-12 s): caen sobre la hierba de una aldea de cuento pintada a mano, sin apenas color, con una panadería y un puente; un búho con una pluma en el pico los observa desde una rama. El aparato, también dibujado, humea. "
         "Escena 4 (12-15 s): primer plano de Cristina y Alberto, asombrados, mirándose las manos de dibujo; los colores de la aldea se desvanecen un poco más; fundido a negro. "
         "Sonido: zumbido eléctrico creciente, silbido de páginas que pasan, caída suave sobre la hierba, música de caja de música y arpa, sin voz de narrador.")

SIN_GENTE = "Sin ninguna persona en la imagen. "

MOSAICOS = {
    "vela": dict(filas=2, cols=1, cartas=["19", "21"], titulo="La vela del troll"),
    "botas": dict(filas=1, cols=2, cartas=["42", "49"], titulo="El bosque de las siete leguas"),
    "espejos": dict(filas=1, cols=2, cartas=["66", "67"], titulo="La sala de los espejos"),
}
POS = {(2, 1): ["mitad de arriba", "mitad de abajo"], (1, 2): ["mitad izquierda", "mitad derecha"]}


def codigo(que):
    return f"Carta dibujada por código (herramientas/cuento.py; no se pide a ChatGPT): {que}."


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
    # ------------------------------------------------------------------ La aldea: el cartel y el puente
    "P": escena("P", "Llegada al libro", [10, 12], [],
                "Quinta parada del Cronoportal. Esta vez no caéis en una época, sino dentro de un libro: «El Libro de los Finales Felices». Os miráis las manos: sois dibujos animados, con trazo de tinta y todo. Un búho con una pluma en el pico os da la bienvenida: «Soy el Búho Narrador. El libro se queda sin color y el último cuento no tiene final. Cuando la tinta se seque, el libro se cerrará con vosotros dentro». El Cronoportal, dibujado a lápiz, ha perdido su tintero.",
                ["Mirad a vuestro alrededor y revisad el aparato."],
                "Una aldea de cuento pintada a mano casi sin color, de tonos grises, con tejados torcidos y un puente de piedra al fondo; en una rama, un búho con una pluma en el pico. En primer plano, un aparato de latón y cristal dibujado a lápiz (el Cronoportal) humea sobre la hierba. Cristina y Alberto, dibujados en 2D clásico, se miran las manos con la boca abierta de puro asombro: ella con los ojos como platos y las cejas muy altas, él con la mandíbula caída y un dedo señalando su propia mano dibujada."),
    "10": escena("10", "La aldea sin color", [14, 16, 18, 19, 20, 21, 22], ["P"],
                 "La aldea es gris como un dibujo a medio pintar. La panadería de Doña Hogaza tiene un cartel de palitos de canela que no cuadra con su escaparate. Junto al río, cuatro duendes tiritan ante un puente: el troll solo les deja cruzar de noche, con un farolillo, y su vela ya está encendida. En el suelo, una varita rota, sin estrella.",
                 ["Hay dos puzles: el cartel de la panadería y el puente de los duendes.", "La vela del troll son dos cartas: juntadlas."],
                 "Una plaza de aldea de cuento en tonos grises, al anochecer: una panadería con un cartel torcido hecho de palitos de canela, un puente de piedra sobre un río con cuatro duendecillos esperando con un farolillo, una vela enorme encendida en la ventana de una cueva al otro lado del río y una varita mágica rota sobre los adoquines. Cristina examina el cartel con una ceja levantada y una sonrisa pícara mientras Alberto se rasca la cabeza con gesto de duda y los labios apretados."),
    "12": combinable("12", "Cronoportal sin tintero", "azul", 62, 74,
                     "El Cronoportal, dibujado solo a lápiz: una consola de latón con un anillo central y un hueco vacío donde iba su tintero de energía.",
                     SIN_GENTE + "Primer plano del Cronoportal dibujado a lápiz sobre un libro enorme abierto: una consola de latón con dos antenas, un anillo central apagado y un hueco circular vacío en el pecho del aparato, sobre una mesa de madera de cuento."),
    "14": app("14", "El cartel de la panadería", "Es un juego de la app: un cartel con una cuenta hecha con palitos de canela que no es verdad. Doña Hogaza no os hablará hasta que su cartel diga la verdad.", 24,
              ["El escaparate (carta 16) dice lo que debería contar el cartel.", "Cada pan vale tantas monedas como tiene al lado; el cartel debería sumar los dos. Moved un solo palito.", "Quitad el palito de arriba a la derecha del 9 y ponedlo arriba a la derecha del 5: 5 + 4 = 9."],
              SIN_GENTE + "Un cartel de madera torcido colgado en la fachada de una panadería de cuento, con una cuenta formada por palitos de canela (sin números legibles), rodeado de hogazas y bollos dibujados."),
    "16": gris("16", "El escaparate", "Los panes del escaparate de Doña Hogaza, cada uno con sus monedas.",
               ["Sirve para el cartel (carta 14).", "Contad las monedas de cada pan: el cartel debería sumarlos.", "Hogaza 5 y bollo 4: la cuenta buena es 5 + 4 = 9."], codigo("el escaparate de Doña Hogaza")),
    "18": gris("18", "Los cuatro duendes", "Cuánta arena cae mientras cruza el puente cada duende.",
               ["Sirve para el puente (carta 20).", "Contad los granos de cada reloj: dos granos, un minuto.", "Bigotes 1, Pétalo 2, Gruñón 5 y Abuela Musgo 8 minutos."], codigo("los cuatro duendes y sus relojes de arena")),
    "19": pieza("19", "vela", "Media vela del troll.", ["Es la mitad de una vela: juntadla con la carta 21.", "Contad las rayas de cera.", "La vela dura 15 minutos: ese es el tiempo para cruzar el puente."]),
    "21": pieza("21", "vela", "Media vela del troll.", ["Es la mitad de una vela: juntadla con la carta 19.", "Contad las rayas de cera.", "La vela dura 15 minutos: ese es el tiempo para cruzar el puente."]),
    "20": app("20", "El puente del troll", "Es un juego de la app: los cuatro duendes tienen que cruzar el puente con un solo farolillo antes de que se apague la vela del troll.", 28,
              ["Lo que tarda cada duende está en la carta 18; lo que dura la vela, en las cartas 19 y 21.", "Que los dos más lentos crucen juntos, y que vuelvan con el farolillo los rápidos.", "Bigotes y Pétalo van; vuelve Bigotes; Gruñón y Abuela Musgo van; vuelve Pétalo; Bigotes y Pétalo van (15 minutos)."],
              SIN_GENTE + "Un puente de piedra de cuento sobre un río oscuro, de noche, con un farolillo con una luciérnaga dentro apoyado en el pretil y, al otro lado, la entrada de la cueva de un troll con una vela encendida."),
    "22": combinable("22", "Varita rota", "azul", 35, 57, "Una varita mágica partida, sin su estrella en la punta.",
                     SIN_GENTE + "Una varita mágica de madera blanca con la punta rota y vacía, apoyada sobre unos adoquines grises de una aldea de cuento, con unos pocos destellos dorados apagados a su alrededor."),
    "24": escena("24", "Doña Hogaza", [26], [14, 16],
                 "El cartel por fin dice la verdad y Doña Hogaza sale a la puerta, harina hasta las cejas: «¡Gracias, forasteros! El color se fue cuando se rompió la varita del hada mayor. Desde entonces todo son chismes... y yo me los sé todos». Os da una servilleta llena de garabatos.",
                 ["Los chismes de Doña Hogaza servirán más adelante, con las hadas."],
                 "La puerta de una panadería de cuento en tonos grises, con una panadera regordeta llena de harina que gesticula con un rodillo mientras cuenta un chisme. Alberto escucha mordiendo un bollo con los ojos muy abiertos y Cristina se tapa la boca para no reírse."),
    "26": gris("26", "Los chismes de Doña Hogaza", "Lo que Doña Hogaza sabe de las hadas de la torre.",
               ["Sirve para las hadas (carta 51).", "Las de ala azul dicen siempre la verdad y las de ala roja mienten siempre. Esta frase es de Brisa.", "Brisa y Dalia son de ala azul; Lila y Nube, de ala roja."], codigo("la servilleta de los chismes")),
    "28": escena("28", "El troll se aparta", [35], [18, 19, 20, 21],
                 "Los cuatro duendes llegan al otro lado justo cuando la vela chisporrotea. El troll, de mal humor, se aparta con un bostezo. En el barro del puente brilla algo: una estrella de cinco puntas que se cayó de la varita del hada mayor.",
                 ["Lo que habéis encontrado se puede juntar con algo que ya tenéis."],
                 "Un troll enorme y peludo bostezando junto a un puente de piedra al amanecer, con cuatro duendecillos que celebran al otro lado. Cristina recoge del barro una estrella brillante con cara de triunfo y Alberto hace una reverencia exagerada al troll, con una sonrisa burlona."),
    "35": combinable("35", "Estrella caída", "roja", 22, 57, "Una estrella de cinco puntas que todavía brilla un poco, caída de una varita.",
                     SIN_GENTE + "Una estrellita dorada con cinco puntas, del tamaño de una manzana, que brilla suavemente sobre un paño morado, con unas motas de polvo de estrellas flotando a su alrededor."),
    "57": escena("57", "El bosque despierta", [31, 32], [22, 35, 10, 28],
                 "La estrella encaja en la varita, que suelta una lluvia de chispas: el bosque recupera el verde. El Búho baja a vuestro hombro: «El castillo del gigante guarda el tintero, y la torre de las hadas, la luz. Hay dos caminos: el viejo camino al castillo, que está cortado, y el atajo del bosque, para el que haría falta calzado... de gigante»",
                 ["Hay dos caminos: el del castillo y el del bosque. Podéis seguir los dos."],
                 "Un claro de bosque de cuento que recupera el color en una ola verde y dorada a partir de una varita con una estrella en la punta. Cristina sostiene la varita en alto con una carcajada de alegría y Alberto se protege la cara de las chispas con los ojos entornados, sorprendido; un búho los mira desde una rama."),
    # ------------------------------------------------------------------ Rama 1: el camino del castillo
    "31": escena("31", "El camino cortado", [40, 41, 43, 45], [],
                 "El viejo camino de la aldea al castillo está cortado: zarzas, un río y una roca. Al lado, una fuente de cuento cuyas aguas enseñan el mismo camino «había una vez», hace cien años. Quien toca el agua puede cambiar el pasado... pero solo tres veces.",
                 ["Lo que hagáis en el pasado cambia lo que hay hoy."],
                 SIN_GENTE + "Un camino de cuento que sube hacia un castillo lejano, cortado por un zarzal, un río y una roca enorme; junto al camino, una fuente de piedra cuyas aguas reflejan el mismo paisaje cien años antes, con prados y arbolitos."),
    "40": app("40", "Había una vez... y ahora", "Es un juego de la app: el camino al castillo en el pasado y en el presente. Tres saltos al pasado, una acción en cada casilla.", 30,
              ["Las cartas 41, 43 y 45 enseñan, con ejemplos, lo que hace cada acción.", "Lo que se hace en el pasado se ve en el presente: buscad para cada obstáculo de hoy la acción que lo quite.", "Fuego en la casilla 3, plantar en la 5 y cavar en la 6."],
              SIN_GENTE + "Una fuente mágica de cuento con dos reflejos en el agua: arriba un paisaje del pasado con prados, y abajo el mismo paisaje hoy, con zarzas, río y roca."),
    "41": gris("41", "Plantar una semilla", "Había una vez... y ahora: lo que pasa si se planta una semilla.",
               ["Sirve para los saltos al pasado (carta 40).", "Comparad lo que había con lo que hay hoy.", "Plantar sobre el río da un tronco caído."], codigo("plantar una semilla, antes y ahora")),
    "43": gris("43", "Cavar", "Había una vez... y ahora: lo que pasa si se cava.",
               ["Sirve para los saltos al pasado (carta 40).", "Comparad lo que había con lo que hay hoy.", "Cavar bajo la roca da un túnel."], codigo("cavar, antes y ahora")),
    "45": gris("45", "Encender fuego", "Había una vez... y ahora: lo que pasa si se enciende fuego.",
               ["Sirve para los saltos al pasado (carta 40).", "Comparad lo que había con lo que hay hoy.", "Fuego sobre las zarzas deja ceniza."], codigo("encender fuego, antes y ahora")),
    "30": escena("30", "El castillo dormido", [38], [31, 40, 41, 43, 45],
                 "El camino queda libre y llegáis al castillo del gigante. Todo duerme: el gigante ronca en el patio y las salas están a oscuras. Junto a la puerta del sótano cuelga un farolillo de cristal vacío, sin nada que dé luz.",
                 ["Algo de la torre de las hadas podría encender el farolillo."],
                 "El patio de un castillo de cuento en penumbra, con un gigante que ronca tumbado contra una muralla y una puerta de sótano con un farolillo apagado colgado. Alberto camina de puntillas exageradas con un dedo en los labios y Cristina descuelga el farolillo con cara de susto, mirando de reojo al gigante."),
    "38": combinable("38", "Farolillo vacío", "roja", 56, 94, "Un farolillo de cristal y hierro, sin vela ni luz dentro.",
                     SIN_GENTE + "Un farolillo de hierro forjado con una cúpula vacía y sin luz, colgado de un gancho sobre una baldosa gris de una torre, con unas telarañas apenas visibles."),
    # ------------------------------------------------------------------ Rama 2: el atajo del bosque
    "32": escena("32", "Las botas del gigante", [42, 48, 49, 53], [],
                 "En la linde del bosque hay un par de botas tan grandes que se podría vivir dentro. Alberto mete un pie y sale disparado varias casillas por el aire. El bosque está tan oscuro que no se ve un árbol a dos pasos... pero en la caseta del guarda hay un mapa colgado.",
                 ["Las botas saltan de una forma muy concreta: leed lo bordado en la lengüeta."],
                 "La linde de un bosque oscuro de cuento con un par de botas gigantes de cuero junto a la caseta de un guardabosques con un mapa colgado en la pared. Alberto, con un pie dentro de una bota, sale volando por los aires con cara de pánico y los brazos abiertos, y Cristina lo mira desde abajo partiéndose de risa."),
    "48": app("48", "Las botas de siete leguas", "Es un juego de la app: cruzar el bosque a oscuras con las botas del gigante, de la linde hasta la casa del leñador.", 36,
              ["El mapa del bosque son dos cartas (42 y 49) y el modo de saltar está en la lengüeta (carta 53).", "Las botas saltan por turnos dos y tres casillas en línea recta, por encima de todo, pero no se puede caer en un árbol ni en el agua. Marcad la ruta en el mapa antes de saltar.", f"Los saltos, en orden: {_S_BOTAS}."],
              SIN_GENTE + "Un bosque de cuento completamente a oscuras, visto desde arriba, con solo dos puntos de luz: unas botas gigantes en una esquina y una casita con la ventana encendida en la esquina opuesta."),
    "42": pieza("42", "botas", "Media hoja del mapa del bosque.", ["Es la mitad de un mapa: juntadla con la carta 49.", "Árboles y agua son casillas prohibidas para caer.", f"Los saltos, en orden: {_S_BOTAS}."]),
    "49": pieza("49", "botas", "Media hoja del mapa del bosque.", ["Es la mitad de un mapa: juntadla con la carta 42.", "Árboles y agua son casillas prohibidas para caer.", f"Los saltos, en orden: {_S_BOTAS}."]),
    "53": gris("53", "La lengüeta de las botas", "Un verso bordado en la lengüeta de las botas del gigante.",
               ["Sirve para cruzar el bosque (carta 48).", "Un pie salta dos casillas y el otro tres, siempre por turnos, empezando por el de dos.", "Por encima de todo, sí; caer en un árbol o en el agua, no."], codigo("la lengüeta bordada")),
    "36": escena("36", "La casa del leñador", [52, 54, 55, 59], [32, 42, 48, 49, 53],
                 "Aterrizáis delante de la casita del leñador. Os invita a sopa y señala por la ventana la torre de las hadas, sin puertas: «La única forma de subir es la habichuela mágica que planté. Crece de una manera muy suya; lo apunto todo en mi diario. Si la regáis diciéndole sus hojas, crecerá de golpe hasta la noche que digáis»",
                 ["El diario del leñador son tres cartas: van en orden de lunas."],
                 "El interior de la cabaña de un leñador de cuento, con una chimenea, una sopa humeante y, por la ventana, una torre altísima sin puertas junto a una mata de habichuela. Cristina sopla la cuchara con cara de concentración y Alberto, despeinado del viaje, se señala las botas gigantes con orgullo."),
    "52": app("52", "La habichuela mágica", "Es un juego de la app: regar la habichuela diciéndole cuántas hojas tendrá la noche en que llegue a la ventana de la torre.", 44,
              ["El diario del leñador (cartas 54, 55 y 59) dibuja la mata noche a noche.", "Contad las hojas de cada noche: cada noche salen tantas hojas como tenía la mata la noche de antes de ayer. Seguid la serie hasta la luna 9.", "1, 1, 2, 3, 5, 8, 13, 21, 34: la noche de la luna 9 tiene 34 hojas."],
              SIN_GENTE + "Una pequeña mata de habichuela mágica en un huerto de cuento, de noche, bajo la luna, junto al pie de una torre altísima sin puertas, con una regadera de cobre al lado."),
    "54": gris("54", "Diario del leñador (lunas 1 y 2)", "Dos noches del diario: la mata de habichuela, dibujada.",
               ["Sirve para la habichuela (carta 52).", "Contad hojas y lunas.", "Las tres páginas van seguidas: 1, 1, 2, 3, 5, 8..."], codigo("el diario, lunas 1 y 2")),
    "55": gris("55", "Diario del leñador (lunas 3 y 4)", "Dos noches más del diario: la mata de habichuela, dibujada.",
               ["Sirve para la habichuela (carta 52).", "Comparad cada noche con las dos de antes.", "Cada noche suma las dos anteriores."], codigo("el diario, lunas 3 y 4")),
    "59": gris("59", "Diario del leñador (lunas 5 y 6)", "Las últimas noches del diario: la mata de habichuela, dibujada.",
               ["Sirve para la habichuela (carta 52).", "Seguid la serie hasta la luna 9.", "La luna 9 tiene 34 hojas."], codigo("el diario, lunas 5 y 6")),
    # ------------------------------------------------------------------ La torre de las hadas
    "44": escena("44", "La torre de las hadas", [33, 37, 39, 46, 51, 61, 63], [36, 52, 54, 55, 59],
                 "Trepáis por la habichuela hasta la ventana de la torre. Dentro, cuatro hadas discuten a gritos y el marco de la gran vidriera está vacío, con tres cristales de colores tirados en el suelo. El hada mayor solo os dará su secreto si sabéis quién de ellas dice la verdad.",
                 ["Hay dos puzles: la vidriera y las cuatro hadas. Los chismes de la panadería sirven aquí."],
                 "La sala circular de una torre de hadas de cuento, con un marco de vidriera vacío y tres cristales de colores en el suelo, y cuatro hadas pequeñas con alas de colores discutiendo en el aire. Cristina entra por la ventana agarrada a una hoja gigante, sin aliento y con los ojos brillantes, y Alberto asoma detrás con cara de vértigo, abrazado al tallo."),
    "46": app("46", "La vidriera de la torre", "Es un juego de la app: colocar los tres cristales en el marco de la vidriera para que la torre despierte.", 56,
              ["El dibujo está en la carta 37, los cristales en la 39 y las normas del vidriero en la 33.", "No se pueden girar ni solapar, y no puede quedar ningún hueco del dibujo sin luz.", "El recto abajo, de B5 a E5; la te en A3, B3, C3 y B4; la ese en D3, E3, C4 y D4."],
              SIN_GENTE + "El marco vacío de una gran vidriera de cuento en lo alto de una torre, con tres cristales de colores (uno alargado, uno en forma de te y uno en forma de ese) apoyados en el alféizar."),
    "37": gris("37", "La ventana de la torre", "El dibujo del vidriero: los huecos de la ventana que deben brillar.",
               ["Sirve para la vidriera (carta 46).", "Los cuadros claros son los que deben llevar cristal.", "Doce cuadros: justo tres cristales de cuatro."], codigo("el dibujo de la ventana")),
    "39": gris("39", "Los tres cristales", "Los tres cristales, tal como salieron del horno.",
               ["Sirve para la vidriera (carta 46).", "Fijaos en la forma: no se pueden girar.", "La ese y la te van arriba; el recto, en la fila de abajo."], codigo("los tres cristales")),
    "33": gris("33", "Nota del vidriero", "Una nota del vidriero sobre sus cristales.",
               ["Sirve para la vidriera (carta 46).", "Sin girar, sin solapar y sin dejar huecos.", "El recto abajo, de B5 a E5."], codigo("la nota del vidriero")),
    "51": app("51", "Las cuatro hadas", "Es un juego de la app: marcar el ala de cada hada. Las de un color dicen siempre la verdad y las del otro mienten siempre.", 58,
              ["Lo que dijeron Brisa, Lila y Nube está en las cartas 26, 61 y 63; lo de Dalia, en la app.", "Suponed que Brisa dice la verdad y mirad si todo encaja; si no, probad al revés.", "Brisa y Dalia son de ala azul; Lila y Nube, de ala roja."],
              SIN_GENTE + "Cuatro hadas diminutas de cuento, vistas de espaldas a contraluz para que no se vea el color de sus alas, flotando en una sala circular iluminada por velas."),
    "61": gris("61", "Un papelito de Lila", "Un papelito con la letra de Lila.",
               ["Sirve para las hadas (carta 51).", "Si Lila fuera de ala azul, su frase sería verdad.", "Lila miente: Dalia es de ala azul."], codigo("el papelito de Lila")),
    "63": gris("63", "Un papelito de Nube", "Un papelito con la letra de Nube.",
               ["Sirve para las hadas (carta 51).", "Comparad la frase de Nube con lo que dijo Brisa (carta 26).", "Nube miente: Lila no es de ala azul."], codigo("el papelito de Nube")),
    "56": combinable("56", "Cristal de luna", "roja", 38, 94, "Un cristalito que guarda dentro la luz de la luna, caído de la vidriera al encenderse.",
                     SIN_GENTE + "Un cristal azulado del tamaño de un puño con forma de media luna que brilla con luz plateada, sobre un cojín de terciopelo morado con unas motas de polvo de estrellas."),
    "58": escena("58", "El secreto de las hadas", [69, 70, 71], [51, 61, 63, 26, 24],
                 "Brisa y Dalia, las de ala azul, os cuentan el secreto en voz baja: «Los colores del reino no se perdieron: los guardó la cocinera real en tarros, en la despensa del castillo, para que no se los llevara la tinta seca. Pero los mezcló de cualquier manera»",
                 ["En la despensa hay que devolver cada color a su sitio."],
                 "Dos hadas de ala azul susurrando al oído de Cristina y Alberto en lo alto de una torre de cuento, con la vidriera iluminada detrás. Cristina escucha con la boca abierta en una O de sorpresa y Alberto se inclina con la mano en la oreja y una sonrisa cómplice."),
    "69": app("69", "Tarros de colores", "Es un juego de la app: los tarros de la despensa del castillo, con los colores del reino mezclados en capas.", 80,
              ["El orden de los colores lo dicen el tapiz del salón (carta 70) y la nota de la cocinera (carta 71).", "Solo se vierte sobre un tarro vacío o sobre el mismo color. Cada color, en el tarro del lugar de su estandarte, y los huecos vacíos.", "De izquierda a derecha: dorado, turquesa y rosa; los dos últimos, vacíos."],
              SIN_GENTE + "La despensa de un castillo de cuento con cinco tarros de cristal en una repisa, llenos de capas de pintura brillante rosa, dorada y turquesa mezcladas, junto a cucharones y trapos."),
    "70": gris("70", "El tapiz del salón", "Los estandartes del rey, colgados en la pared del salón.",
               ["Sirve para los tarros (carta 69).", "El orden de los estandartes es el de los tarros.", "Dorado, turquesa y rosa, y dos huecos vacíos."], codigo("el tapiz de los estandartes")),
    "71": gris("71", "Nota de la cocinera real", "Una nota de la cocinera real, pegada a la repisa.",
               ["Sirve para los tarros (carta 69).", "Los tarros van como los estandartes del tapiz (carta 70).", "Dorado, turquesa, rosa, vacío y vacío."], codigo("la nota de la cocinera")),
    "80": escena("80", "El castillo recobra el color", [72, 75, 79], [58, 69, 70, 71],
                 "Al destapar los tarros, los colores salen volando por los pasillos y el castillo se pinta entero. En el salón del trono, sobre un cojín, hay una caja de música de nácar cerrada: el músico del rey dejó su melodía pintada en un papel, y en el jardín hay un xilófono hecho de troncos.",
                 ["La caja se abre con una melodía."],
                 "El salón de un castillo de cuento llenándose de color en remolinos rosas, dorados y turquesa, con una caja de música de nácar sobre un cojín. Alberto da vueltas sobre sí mismo con los brazos abiertos y una risa de niño, y Cristina se queda quieta con las manos en el pecho, emocionada."),
    "72": app("72", "La caja de música", "Es un juego de la app: la caja de música del rey solo se abre con su melodía.", 82,
              ["La melodía, en animales, está en la partitura (carta 75); el xilófono del bosque (carta 79) dice qué nota toca cada animal.", "Leed los animales de la partitura de izquierda a derecha y buscad su tecla en el xilófono.", "Fa, Do, Sol, Mi, Re, La y Fa."],
              SIN_GENTE + "Una caja de música de nácar y oro, cerrada, sobre un cojín de terciopelo morado, con un teclado de siete teclas de colores en la tapa."),
    "75": gris("75", "La partitura de la caja", "La melodía de la caja de música, pintada con animales.",
               ["Sirve para la caja de música (carta 72).", "Cada animal es una nota: buscadlo en el xilófono (carta 79).", "Rana, conejo, ardilla, búho, ciervo, zorro y rana."], codigo("la partitura de animales")),
    "79": gris("79", "El xilófono del bosque", "Un xilófono de troncos con un animal sentado en cada tecla.",
               ["Sirve para la caja de música (carta 72).", "El animal de cada tecla es su nota.", "Conejo Do, ciervo Re, búho Mi, rana Fa, ardilla Sol y zorro La."], codigo("el xilófono del bosque")),
    "82": escena("82", "La caja abierta", [85, 86, 87], [80, 72, 75, 79],
                 "La caja de música se abre como una flor. Dentro hay una página arrancada del libro, en blanco, con ocho huecos para letras, una nota doblada del Búho y una lámina del gran banquete que el rey prepara para el final del cuento.",
                 ["La última página es el último puzle: guarda las letras de todos los demás."],
                 "Una caja de música de nácar abierta como una flor, de la que salen una página en blanco con huecos para letras y una lámina pintada. Cristina saca la página con cuidado y una sonrisa nerviosa, y Alberto se asoma por encima de su hombro con cara de curiosidad."),
    "85": app("85", "La última página", "Es un juego de la app: la última página del libro. Cada puzle que habéis resuelto dejó una letra y el libro las ha guardado. Hay que ordenarlas para escribir la palabra que cierra el cuento.", 99,
              ["La nota del Búho (carta 86) y la lámina del banquete (carta 87) dicen qué palabra es.", "«Y fueron felices y comieron...»: mirad qué hay en las bandejas del banquete.", "La palabra es PERDICES."],
              SIN_GENTE + "La última página de un libro de cuentos enorme, en blanco y brillante, con ocho huecos dorados para letras y una pluma de oro apoyada al lado."),
    "86": gris("86", "Nota del Búho Narrador", "Una nota del Búho sobre el final del cuento.",
               ["Sirve para la última página (carta 85).", "Es el final de todos los cuentos: «y fueron felices y comieron...».", "La palabra es PERDICES."], codigo("la nota del Búho")),
    "87": gris("87", "El banquete del rey", "La lámina del banquete que el rey prepara para el final del cuento.",
               ["Sirve para la última página (carta 85).", "Mirad bien el plato principal de la mesa.", "Son perdices asadas: PERDICES."],
               SIN_GENTE + "Una mesa de banquete real de cuento, larguísima, con manteles bordados, candelabros y, en el centro de cada bandeja dorada, perdices asadas doradas y humeantes con ramitas de romero (el plato principal, muy reconocible); alrededor, frutas, panes y copas, en un gran salón de castillo a todo color."),
    # ------------------------------------------------------------------ La sala de los espejos y el final
    "94": escena("94", "La sala de los espejos", [64, 66, 67], [38, 56, 30, 44, 33, 37, 39, 46],
                 "El cristal de luna enciende el farolillo y bajáis al sótano del castillo: una sala de espejos rotos, a oscuras, con una flor de luna dormida en algún rincón. Si la luz de la luna la toca, se abrirá. Por un ventanuco entra un rayo de luna y, en la pared, cuelga el plano de la sala.",
                 ["El plano son dos cartas: juntadlas. La flor no se ve en la app."],
                 "El sótano de un castillo de cuento con espejos colgados torcidos y rotos, iluminado por un farolillo con luz plateada, y un rayo de luna que entra por un ventanuco. Cristina levanta el farolillo con el ceño fruncido de concentración y Alberto da un respingo al ver su reflejo deformado en un espejo."),
    "64": app("64", "Rayos de luna", "Es un juego de la app: colocar tres espejos para que el rayo de luna llegue a la flor de luna.", 62,
              ["El plano de la sala (cartas 66 y 67) dice dónde están los muros y la flor.", "El rayo tiene que tocar los tres espejos y acabar en la flor, sin chocar con muros.", "Espejo / en A2, \\ en E2 y / en A4."],
              SIN_GENTE + "Una cuadrícula de losas en el suelo de un sótano de cuento, con unos espejos de mano apoyados y un rayo de luz de luna que entra por un ventanuco."),
    "66": pieza("66", "espejos", "Media hoja del plano de la sala de los espejos.", ["Es la mitad de un plano: juntadla con la carta 67.", "La flecha es por donde entra el rayo; los bloques, muros.", "La flor está en E5."]),
    "67": pieza("67", "espejos", "Media hoja del plano de la sala de los espejos.", ["Es la mitad de un plano: juntadla con la carta 66.", "La flecha es por donde entra el rayo; los bloques, muros.", "La flor está en E5."]),
    "62": combinable("62", "Tintero Dorado", "roja", 12, 74, "El Tintero Dorado, que estaba escondido dentro de la flor de luna, lleno de tinta que brilla como el sol.",
                     SIN_GENTE + "Un tintero de cristal y oro lleno de tinta dorada que brilla como el sol, con una pluma de oro apoyada en el borde, sobre una palma abierta con un guante blanco y un fondo de cortinas moradas."),
    "74": escena("74", "Cronoportal con tinta", [], [62, 12, 64, 66, 67, 94, 57],
                 "El Tintero Dorado encaja en el Cronoportal y la consola se llena de color, pero la energía no sube del todo: el Búho tenía razón, falta el final del cuento. Hasta que la última página no tenga su palabra, el portal no se abrirá.",
                 ["Falta escribir el final del cuento en la última página."],
                 "El Cronoportal, ya pintado con todos sus colores, con el tintero dorado encajado en el pecho, sobre un libro enorme abierto. Alberto sonríe aliviado con las manos en las caderas y Cristina, a su lado, mira el libro con la cabeza ladeada y una duda en los ojos."),
    "99": escena("99", "Colorín colorado (FIN)", [], [74, 82, 85, 86, 87],
                 "La palabra aparece en la última página con letras de oro: «...y fueron felices y comieron perdices». El libro se llena de color, la aldea, la torre y el castillo celebran el banquete y el Cronoportal se enciende. El Búho os despide con una reverencia: «Colorín colorado...». Aterrizáis en vuestro salón y el libro se cierra solo con un suspiro. FIN.",
                 [],
                 "Dibujo en 2D clásico. La escena final ocurre DENTRO del salón de su casa actual, en el presente (sofá, estanterías con libros, plantas, una lámpara encendida y luz cálida de tarde por la ventana): acaban de VOLVER a casa. Cristina y Alberto, ya a todo color, acaban de salir de un portal circular de luz azul y dorada que surge de un gran libro de cuentos abierto sobre la mesa del salón; a través del portal todavía se ven la aldea, la torre y el castillo del cuento y al Búho Narrador diciendo adiós con el ala. Ella ríe a carcajadas con los ojos entornados y él lanza un beso hacia el libro, radiante. Están de cara a nosotros, aterrizando en el salón y alejándose del portal, que queda a su espalda y se está cerrando; el mundo de la aventura solo se ve a través del portal, detrás de ellos. No están entrando en el portal ni saliendo de casa: están llegando."),
}

META = dict(juego="Érase una vez — El Libro de los Finales Felices", estilo=ESTILO, personajes=PERSONAJES, hoja=HOJA, foto=FOTO, video=VIDEO,
            mosaicos={k: dict(filas=m["filas"], cols=m["cols"], cartas=m["cartas"], titulo=m["titulo"]) for k, m in MOSAICOS.items()})

SPEC = dict(final="99", needs={
    "24": ["14", "16"], "28": ["20", "18", "19", "21"], "57": ["22", "35"], "30": ["40", "41", "43", "45"], "36": ["48", "42", "49", "53"],
    "44": ["52", "54", "55", "59"], "56": ["46", "37", "39", "33"], "58": ["51", "26", "61", "63"], "80": ["69", "70", "71"], "94": ["38", "56"],
    "62": ["64", "66", "67"], "82": ["72", "75", "79"], "74": ["12", "62"], "99": ["85", "86", "87", "74"]}, eventos={})

PARA_QUE = {k: c["titulo"].split("— ", 1)[1] for k, c in J.items()}

_T = [
    ("leer", "P", "Llegada al libro", "Pon el Modo PC (solo la P en la mesa) y en el móvil pulsa Empezar. Lee la carta P: coge la 10 y la 12."),
    ("leer", "10", "La aldea sin color", "Lee la carta 10. Descarta la P y coge 14, 16, 18, 19, 20, 21 y 22. Junta la vela: 19 arriba y 21 abajo."),
    ("app", "14", "El cartel", "En el móvil: Acción, 14. Los panes del escaparate (16) valen 5 y 4: mueve el palito de arriba a la derecha del 9 al 5 para que diga 5 + 4 = 9. El mensaje te dice que cojas la 24. Letra: C.", "carta 24"),
    ("leer", "24", "Doña Hogaza", "Lee la carta 24. Descarta 14 y 16 y coge la 26 (guárdala para las hadas)."),
    ("app", "20", "El puente del troll", "En el móvil: Acción, 20. La vela (19 y 21) dura 15 minutos y los duendes (18) tardan 1, 2, 5 y 8: pasan Bigotes y Pétalo, vuelve Bigotes, pasan Gruñón y Abuela Musgo, vuelve Pétalo y pasan Bigotes y Pétalo. El mensaje te dice que cojas la 28. Letra: E.", "carta 28"),
    ("leer", "28", "El troll se aparta", "Lee la carta 28. Descarta 18, 19, 20 y 21 y coge la 35."),
    ("combinar", "22", "35", "La varita", "La varita (22) y la estrella (35) son combinables: 22 + 35 = 57. Coge la 57."),
    ("leer", "57", "El bosque despierta", "Lee la carta 57. Descarta 22, 35, 10 y 28 y coge 31 y 32."),
    ("leer", "31", "El camino cortado", "Lee la carta 31. Coge 40, 41, 43 y 45."),
    ("app", "40", "Había una vez", "En el móvil: Acción, 40. Con los ejemplos de 41, 43 y 45: fuego en la casilla 3, plantar en la 5 y cavar en la 6. El mensaje te dice que cojas la 30. Letra: S.", "carta 30"),
    ("leer", "30", "El castillo dormido", "Lee la carta 30. Descarta 31, 40, 41, 43 y 45 y coge la 38."),
    ("leer", "32", "Las botas del gigante", "Lee la carta 32. Coge 42, 48, 49 y 53. Junta el mapa: 42 a la izquierda y 49 a la derecha."),
    ("app", "48", "Las botas", f"En el móvil: Acción, 48. Saltos de 2 y 3 por turnos, sin caer en árboles ni agua: {_S_BOTAS}. El mensaje te dice que cojas la 36.", "carta 36"),
    ("leer", "36", "La casa del leñador", "Lee la carta 36. Descarta 32, 42, 48, 49 y 53 y coge 52, 54, 55 y 59."),
    ("app", "52", "La habichuela", "En el móvil: Acción, 52. Las hojas del diario (54, 55 y 59) son 1, 1, 2, 3, 5, 8...: la luna 9 tiene 34. El mensaje te dice que cojas la 44.", "carta 44"),
    ("leer", "44", "La torre de las hadas", "Lee la carta 44. Descarta 36, 52, 54, 55 y 59 y coge 33, 37, 39, 46, 51, 61 y 63."),
    ("app", "46", "La vidriera", "En el móvil: Acción, 46. Sin girar ni solapar (33), cubre el dibujo (37) con los cristales (39): recto de B5 a E5, te en A3, B3, C3 y B4, ese en D3, E3, C4 y D4. El mensaje te dice que cojas la 56. Letra: D.", "carta 56"),
    ("app", "51", "Las cuatro hadas", "En el móvil: Acción, 51. Con las frases de 26, 61 y 63 y la de Dalia: Brisa y Dalia azules, Lila y Nube rojas. El mensaje te dice que cojas la 58. Letra: I.", "carta 58"),
    ("leer", "58", "El secreto de las hadas", "Lee la carta 58. Descarta 51, 61, 63, 26 y 24 y coge 69, 70 y 71."),
    ("app", "69", "Tarros de colores", "En el móvil: Acción, 69. Como los estandartes del tapiz (70) y la nota (71): dorado, turquesa y rosa, y los dos últimos vacíos. El mensaje te dice que cojas la 80. Letra: E.", "carta 80"),
    ("leer", "80", "El castillo recobra el color", "Lee la carta 80. Descarta 58, 69, 70 y 71 y coge 72, 75 y 79."),
    ("app", "72", "La caja de música", "En el móvil: Acción, 72. Los animales de la partitura (75) en el xilófono (79): Fa, Do, Sol, Mi, Re, La y Fa. El mensaje te dice que cojas la 82. Letra: R.", "carta 82"),
    ("leer", "82", "La caja abierta", "Lee la carta 82. Descarta 80, 72, 75 y 79 y coge 85, 86 y 87."),
    ("combinar", "38", "56", "El farolillo", "El farolillo (38) y el cristal de luna (56) son combinables: 38 + 56 = 94. Coge la 94."),
    ("leer", "94", "La sala de los espejos", "Lee la carta 94. Descarta 38, 56, 30, 44, 33, 37, 39 y 46 y coge 64, 66 y 67. Junta el plano: 66 a la izquierda y 67 a la derecha."),
    ("app", "64", "Rayos de luna", "En el móvil: Acción, 64. La flor está en E5 (plano 66 y 67): espejo / en A2, \\ en E2 y / en A4. El mensaje te dice que cojas la 62. Letra: P.", "carta 62"),
    ("combinar", "12", "62", "El Tintero Dorado", "El Cronoportal (12) y el Tintero Dorado (62) son combinables: 12 + 62 = 74. Coge la 74."),
    ("leer", "74", "Cronoportal con tinta", "Lee la carta 74. Descarta 62, 12, 64, 66, 67, 94 y 57."),
    ("app", "85", "La última página", "En el móvil: Acción, 85. Con la nota (86) y el banquete (87): «felices y comieron... PERDICES». El mensaje te dice que cojas la 99.", "carta 99"),
    ("leer", "99", "Final", "Lee la carta 99. Descarta 74, 82, 85, 86 y 87. En la mesa solo queda la 99. ¡Colorín colorado, fin!"),
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
