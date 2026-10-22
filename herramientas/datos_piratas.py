"""Mar de las Brumas, 1715: El Tesoro de la Isla Calavera — versión de 60 cartas (22 oct 2026), mucho más difícil y variada.

La mecánica de cartas propia siguen siendo las CARTAS QUE SE PLIEGAN (como los «fold-in» de la revista MAD): una carta náutica, un testamento y un mapa que,
plegados en acordeón hasta que la línea A toque la B (y la C, la D), enseñan lo que desplegados esconden. Once puzles de tipos que no salen en ningún otro
juego de la serie, con las pistas dibujadas o en acertijo: una bitácora de guardias y campanadas, una persecución de fragata con regla fija (como el
Minotauro), una constelación girada entre treinta y seis estrellas, un suelo de losas que sigue los símbolos de un testamento plegado, una tabla de tiro
de cañón, el reparto del botín entre siete piratas (inducción hacia atrás), las mareas y las barras de arena, un timón con la aguja torcida, una balanza
con pesas en los dos platillos, el mapa plegado de una isla y un último viaje con cinco rumbos. Solo 16 cartas tienen a Cristina y Alberto (escenas); el
resto son objetos y pistas sin personas. Las cartas-pista las dibuja herramientas/piratas.py (instancias_piratas.py)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ampliacion as _amp  # noqa: E402
import instancias_piratas as I  # noqa: E402

INST = I.INST
RUMBO = INST["rumbo"]
LOSAS = INST["losas"]
RUTA = INST["ruta"]
_W, _H = INST["lamina"]


def _plegado(k):
    p = INST["pliegues"][k]
    out = {}
    if "x" in p:
        out["x"] = [round(p["x"][0] / _W, 4), round(p["x"][1] / _W, 4)]
    if "y" in p:
        out["y"] = [round(p["y"][0] / _H, 4), round(p["y"][1] / _H, 4)]
    return out


ESTILO = ("Ilustración pictórica semirrealista de aventuras de piratas, como una portada de novela de aventuras clásica: mar turquesa del Caribe, "
          "velas blancas y remendadas, madera gastada, cuerdas, faroles de aceite, luz cálida de atardecer y brumas suaves sobre el agua, formato vertical 2:3. "
          "Sin texto, letras ni números legibles en la imagen; los mapas, banderas y papeles solo muestran rayas o manchas decorativas. "
          "Deja libre de detalles importantes la esquina superior izquierda y el 18 % inferior de la imagen. "
          "Los personajes tienen siempre expresiones distintas y expresivas, adecuadas a la escena (nunca la misma cara en dos imágenes).")

PERSONAJES = {
    "Cristina": "Cristina, mujer de 26 años, profesora, pelo rubio y rizado suelto bajo un pañuelo azul atado en la cabeza, ojos azules. Viste de pirata del siglo XVIII: camisa blanca de lino con mangas amplias, chaleco de cuero granate, fajín rojo en la cintura, pantalón de lona y botas altas de cuero, con un catalejo de latón al cinto.",
    "Alberto": "Alberto, hombre de 27 años, informático, pelo moreno corto, barba cuidada, ojos marrones. Viste de pirata del siglo XVIII: camisa crema, casaca azul marino con botones dorados, tricornio negro, cinturón ancho con hebilla de latón, pantalón bombacho y botas de cuero, con una brújula colgada al cuello.",
}

HOJA = ("Crea una hoja de personajes (character sheet) con las dos personas de la foto adjunta, de cuerpo entero y de frente, sobre fondo claro y neutro. "
        "Mantén su parecido real con la foto (cara, pelo, barba, ojos). "
        "Cristina: mujer de 26 años, profesora, pelo rubio y rizado suelto bajo un pañuelo azul atado en la cabeza, ojos azules, camisa blanca de lino con mangas amplias, chaleco de cuero granate, fajín rojo, pantalón de lona, botas altas y un catalejo de latón al cinto. "
        "Alberto: hombre de 27 años, informático, pelo moreno corto, barba cuidada, ojos marrones, camisa crema, casaca azul marino con botones dorados, tricornio negro, cinturón ancho con hebilla de latón, pantalón bombacho, botas de cuero y una brújula colgada al cuello. "
        "Estilo: " + ESTILO)

FOTO = ("Antes de nada, adjunta a ChatGPT una foto de Cristina y Alberto juntos (o una de cada uno, con la cara bien visible). "
        "Pídele que mantenga el parecido real, pero con el estilo de ilustración de este juego.")

VIDEO = ("Crea un vídeo vertical 9:16 de 15 segundos, con estilo cinematográfico de película de piratas, luz cálida de atardecer y mar turquesa. Sin ningún texto, letra ni subtítulo en pantalla. "
         "Escena 1 (0-4 s): en el salón de una casa actual, Cristina (mujer de 26 años, rubia de pelo rizado, ojos azules) y Alberto (hombre de 27 años, moreno con barba, ojos marrones) rodean un aparato de latón y cristal con un anillo central: el Cronoportal. Alberto señala un viejo mapa del tesoro. "
         "Escena 2 (4-8 s): el anillo se enciende con un arco de luz azul y dorada y los dos son absorbidos por un túnel de luz. "
         "Escena 3 (8-12 s): caen sobre la cubierta de un barco pirata entre cuerdas y barriles; un loro verde y rojo baja en picado y se lleva en el pico el cristal rojo del aparato. "
         "Escena 4 (12-15 s): primer plano de Cristina y Alberto, ya vestidos de piratas, boquiabiertos, mientras una capitana con sombrero de plumas recoge el cristal del loro y sonríe; fundido a negro. "
         "Sonido: zumbido eléctrico creciente, silbido del portal, golpe de madera al aterrizar, olas, gaviotas, graznido de loro y una música de acordeón marinero, sin voz de narrador.")

SIN_GENTE = "Sin ninguna persona en la imagen. "

MOSAICOS = {
    "aguas": dict(filas=2, cols=1, cartas=["19", "21"], titulo="La carta de aguas de la bahía"),
    "cielo": dict(filas=1, cols=2, cartas=["41", "43"], titulo="El cielo de la tapa del cofre"),
    "suelo": dict(filas=1, cols=2, cartas=["42", "49"], titulo="El suelo de la cueva"),
    "mareas": dict(filas=2, cols=1, cartas=["61", "63"], titulo="La tabla de la marea"),
}
POS = {(2, 1): ["mitad de arriba", "mitad de abajo"], (1, 2): ["mitad izquierda", "mitad derecha"]}

_B = INST["bitacora"]
_S_BIT = f"{_B['entre_horas']} horas" + (f" y {_B['entre_min']} minutos" if _B["entre_min"] else "")
_S_PER = ", ".join(INST["persecucion"]["solucion"])
_S_CIE = ", ".join(str(n) for n in INST["cielo"]["solucion"])
_S_CICLO = ", ".join(LOSAS["ciclo"])
_S_SUE = ", ".join(f"{LOSAS['suelo'][y][x]} (fila {LOSAS['n'] - y}, columna {x + 1})" for x, y in LOSAS["camino"])
_C = INST["canon"]
_S_CAN = "; ".join(f"barco {i + 1}: {c + 1} sacos y {_C['elevaciones'][a]}°" for i, (c, a) in enumerate(_C["solucion"]))
_S_BOT = ", ".join(str(x) for x in INST["botin"]["solucion"])
_M = INST["mareas"]
_S_MAR = f"{_M['salida']:02d}:00"
_S_RUM = str(RUMBO["aguja"])
_P = INST["pesas"]
_S_PES = "; ".join(f"cofre {o + 1} ({w} lb): " + (", ".join(f"{p} {'con el cofre' if c < 0 else 'enfrente'}" for p, c in zip(_P["pesas"], s) if c) or "ninguna") for o, (w, s) in enumerate(zip(_P["objetos"], _P["solucion"])))
_xm, _ym = RUTA["celdas"][-1]
_xp, _yp = RUTA["inicio"]
_S_GRU = f"{_xm - _xp} casillas al este y {_ym - _yp} al sur de la palmera"
_ISL = INST["isla"]
_S_ISL = f"columna {_ISL['final'][0] + 1}, fila {_ISL['final'][1] + 1}"
_D = dict(zip(_ISL["orden"], _ISL["distancias"]))


def codigo(que):
    return f"Carta dibujada por código (herramientas/piratas.py; no se pide a ChatGPT): {que}."


def pieza(carta, mosaico, que, pistas):
    m = MOSAICOS[mosaico]
    i = m["cartas"].index(carta)
    pos = POS[(m["filas"], m["cols"])][i]
    return dict(titulo=f"Carta {carta} — {m['titulo']} ({pos})", tipo="gris",
                mosaico=dict(id=mosaico, filas=m["filas"], cols=m["cols"], fila=i // m["cols"], col=i % m["cols"]),
                descripcion=[que], pistas=pistas, arte=codigo(f"{pos} de «{m['titulo']}»"))


def gris(carta, titulo, que, pistas):
    return dict(titulo=f"Carta {carta} — {titulo}", tipo="gris", descripcion=[que], pistas=pistas, arte=codigo(titulo))


def plegable(carta, titulo, que, pistas):
    c = gris(carta, titulo, que, pistas)
    c["plegado"] = _plegado(carta)
    return c


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
    # ------------------------------------------------------------------ La cubierta
    "P": escena("P", "Llegada a bordo", [10, 12], [],
                "Duodécima parada del Cronoportal: el Mar de las Brumas, en 1715. Aterrizáis sobre la cubierta de La Gaviota, un bergantín pirata, entre cuerdas y barriles. Antes de que os pongáis en pie, un loro verde y rojo baja en picado y se lleva en el pico el cristal de energía del aparato. Se lo lleva a su dueña, la capitana Bruma, que lo guarda en un cofre y os propone un trato: «Os lo devuelvo cuando me traigáis el tesoro del capitán Calavera, antes de que la marea cubra su cueva. Tenéis noventa minutos».",
                ["Mirad a vuestro alrededor y revisad el aparato."],
                "La cubierta de un bergantín pirata al atardecer, con cuerdas, barriles y velas remendadas. Un loro verde y rojo vuela con un cristal rojo brillante en el pico. En primer plano, el Cronoportal, un aparato de latón y cristal, humea en el suelo de madera. Cristina, despeinada y con la boca abierta de sorpresa, señala al loro, y Alberto, en el suelo, se sujeta el tricornio con cara de incredulidad."),
    "10": escena("10", "La cubierta de La Gaviota", [14, 16, 18, 19, 20, 21, 22], ["P"],
                 "La capitana Bruma os lleva al timón: «El piloto se ha bebido el ron de la semana. Ayudadme». Sobre una caja de pólvora, la bitácora del barco (carta 16): hay que echar cuentas con sus campanadas. Una fragata de la Armada se acerca y solo se puede escapar hacia un banco de niebla: la ordenanza de la Armada (carta 18) y la carta de aguas de la bahía, en dos láminas: juntad la 19 arriba y la 21 abajo (carta 20). Junto al timón, Cristina encuentra una lente de catalejo suelta (carta 22).",
                 ["Hay dos puzles: la bitácora y la persecución.", "La carta de aguas son dos cartas: juntadlas, una encima de otra."],
                 "La cubierta de un bergantín pirata con un gran timón de madera, el mástil y las velas hinchadas por el viento; una capitana con sombrero de plumas y casaca roja señala el horizonte con un loro en el hombro. Cristina recoge del suelo una lente de cristal con curiosidad y los ojos entrecerrados, y Alberto sujeta una carta de aguas enrollada con gesto de preocupación."),
    "12": combinable("12", "Cronoportal sin cristal", "azul", 62, 74,
                     "El Cronoportal: una consola de latón y cristal con un anillo central apagado y un hueco vacío en el pecho, donde iba el cristal de energía.",
                     SIN_GENTE + "Primer plano del Cronoportal: una consola portátil de latón y cristal con dos antenas de cobre, un anillo de cristal central apagado y un hueco circular vacío en el pecho del aparato, sobre las tablas de madera de una cubierta de barco pirata, con cuerdas enrolladas al fondo."),
    "14": app("14", "La bitácora", "Es un juego de la app: tres anotaciones de la bitácora dicen cuántas campanadas sonaron en qué guardia. Hay que decir cuánto tiempo pasó entre el aviso 1 y el aviso 3.", 24,
              ["La bitácora está en la carta 16.", "Cada guardia empieza a su hora y dura cuatro horas; la primera campanada suena media hora después de empezar. Pasad cada aviso a hora de reloj y restad.", f"Pasaron {_S_BIT}. Distancia de la bitácora: {_D['14']}."],
              SIN_GENTE + "Una bitácora de a bordo abierta sobre una caja de madera, con un tintero, una pluma y una campana de latón colgada al fondo, a la luz de un farol de aceite."),
    "16": gris("16", "La bitácora", "La bitácora de La Gaviota: las seis guardias del día con su hora de comienzo y tres anotaciones con las campanadas de cada aviso.",
               ["Es la bitácora de la carta 14.", "Cada media hora suena una campanada más dentro de la guardia.", "La pregunta está al pie de la hoja."]),
    "18": gris("18", "La ordenanza de la Armada", "La ordenanza de la Armada con la regla de la persecución de una fragata y un ejemplo dibujado.",
               ["Es la regla de la persecución (carta 20).", "Por cada casilla que avanzáis, la fragata da dos pasos.", "El ejemplo dibujado enseña qué hace cuando hay una roca."]),
    "19": pieza("19", "aguas", "Media lámina de la carta de aguas de la bahía.", ["Es la mitad de una lámina: juntadla con la carta 21.", "Es una cuadrícula con rocas, La Gaviota, la fragata y un banco de niebla.", "La ordenanza está en la carta 18."]),
    "21": pieza("21", "aguas", "Media lámina de la carta de aguas de la bahía.", ["Es la mitad de una lámina: juntadla con la carta 19.", "Es una cuadrícula con rocas, La Gaviota, la fragata y un banco de niebla.", "La ordenanza está en la carta 18."]),
    "20": app("20", "La persecución", "Es un juego de la app: llevar La Gaviota al banco de niebla sin que la alcance la fragata, que da dos pasos por cada uno vuestro con una regla fija.", 28,
              ["La carta de aguas está en las cartas 19 y 21 y la ordenanza, en la 18. Las rocas no se ven en la app.", "No vale ir en línea recta: la fragata os alcanza. Esperad a que una roca la frene, o cambiad de lado para que tenga que dar un rodeo.", f"Una salida (19 turnos): {_S_PER}."],
              SIN_GENTE + "Un bergantín pirata de velas blancas en un mar turquesa con rocas y bancos de niebla, con una fragata de la Armada de velas grises al fondo, al atardecer."),
    "22": combinable("22", "Media lente de catalejo", "azul", 35, 57, "Una mitad de la lente de un catalejo de latón, con un aro de metal y el cristal partido.",
                     SIN_GENTE + "La mitad izquierda de la lente de un catalejo de latón, con su aro de metal, sobre las tablas de madera de una cubierta de barco."),
    "24": escena("24", "El pañol de la capitana", [26], [14, 16],
                 "Con las cuentas de las guardias claras, la capitana Bruma os abre el pañol, un cuartito lleno de cartas y compases, y os da una carta con el paso de las barras de arena del puerto de la Isla Calavera: la usaréis para entrar con el barco (carta 26).",
                 ["Mirad lo que os da la capitana."],
                 "El pañol de un barco pirata, un cuartito con estantes llenos de cartas náuticas enrolladas, compases y sextantes, y una lámpara de aceite. La capitana Bruma, con sombrero de plumas, entrega una carta a Cristina y Alberto. Cristina la recibe con una reverencia exagerada y una sonrisa traviesa; Alberto la desenrolla con las cejas arqueadas de sorpresa."),
    "26": gris("26", "El paso de las barras", "Una carta con el calado de La Gaviota y tres barras de arena del puerto, con las horas que tarda el barco en llegar a cada una y su fondo propio.",
               ["Es la carta de las mareas (carta 51).", "El agua sobre cada barra es la marea más su fondo propio.", "La tabla de la marea está en las cartas 61 y 63."]),
    "28": escena("28", "El banco de niebla", [35], [18, 19, 20, 21],
                 "La Gaviota se mete en el banco de niebla y la fragata pasa de largo, perdida. Cuando la bruma se levanta un poco, en una caja de pólvora vacía hay un paquete envuelto en lona: la otra mitad de la lente del catalejo (carta 35).",
                 ["Mirad en la caja de pólvora."],
                 "El interior de un banco de niebla blanca alrededor de la cubierta de un bergantín pirata, con una caja de madera abierta y un paquete de lona. Cristina saca el paquete con los ojos muy abiertos de emoción; Alberto, con la mano de visera, escruta la niebla con la boca torcida de desconfianza."),
    "35": combinable("35", "Otra media lente de catalejo", "roja", 22, 57, "La otra mitad de la lente del catalejo, con el resto del cristal.",
                     SIN_GENTE + "La mitad derecha de la lente de un catalejo de latón, con el resto del cristal, sobre un paño de lona en una caja de pólvora."),
    "57": escena("57", "El catalejo", [31, 32], [22, 35, 10, 28],
                 "Montáis las dos mitades en el catalejo y, al mirar por él, la niebla se abre: a un lado, el cofre del capitán Calavera, con la tapa de cielo estrellado (carta 31); al otro, la entrada de una cueva con el testamento del capitán (carta 32). Hay que visitar los dos.",
                 ["Dos sitios: el cofre de la tapa estrellada y la cueva."],
                 "Cristina mira por un catalejo de latón en la cubierta de un bergantín pirata, con la niebla abriéndose a su alrededor, y el cofre de un capitán sobre una roca de una isla a lo lejos y una cueva oscura. Cristina, con el ojo pegado al catalejo y la boca abierta, señala hacia la isla; Alberto, a su lado, sonríe de oreja a oreja y levanta un puño."),
    # ------------------------------------------------------------------ Rama 1: el cofre de la tapa estrellada
    "31": escena("31", "El cofre del capitán Calavera", [40, 41, 43, 45], [],
                 "Sobre una roca de la playa, el cofre del capitán Calavera: su tapa es un cielo de tachuelas numeradas, en dos láminas (cartas 41 y 43), y el capitán dejó su carta celeste con la constelación que abre el cofre (carta 45). Una pantalla de madera (carta 40) espera los números.",
                 ["Un único puzle: la constelación de la tapa."],
                 "Una playa del Caribe al atardecer con un cofre de madera sobre una roca; la tapa del cofre está cubierta de tachuelas doradas que forman un cielo estrellado. Cristina compara una carta celeste con la tapa del cofre con el ceño fruncido; Alberto, de rodillas, sigue las tachuelas con el dedo con los ojos entrecerrados."),
    "40": app("40", "La tapa del cofre", "Es un juego de la app: la tapa del cofre es un cielo de treinta y seis tachuelas numeradas. Hay que tocar las seis que forman la Calavera de la carta celeste, que aparece girada y más pequeña.", 30,
              ["El cielo está en las cartas 41 y 43 y la carta celeste, en la 45.", "La Calavera tiene dos estrellas arriba, una a cada lado, y dos abajo, unidas por una más. En el cielo está girada: buscad primero un grupo de seis estrellas que se parezca a su forma.", f"Son las estrellas {_S_CIE}. Distancia de las estrellas: {_D['40']}."],
              SIN_GENTE + "La tapa de un cofre de madera cubierta de tachuelas doradas que forman un cielo estrellado, sobre una roca de una playa al atardecer."),
    "41": pieza("41", "cielo", "Media lámina del cielo de la tapa del cofre.", ["Es la mitad de una lámina: juntadla con la carta 43.", "Son treinta y seis estrellas numeradas.", "La carta celeste está en la carta 45."]),
    "43": pieza("43", "cielo", "Media lámina del cielo de la tapa del cofre.", ["Es la mitad de una lámina: juntadla con la carta 41.", "Son treinta y seis estrellas numeradas.", "La carta celeste está en la carta 45."]),
    "45": gris("45", "La carta celeste", "La carta celeste del capitán Calavera, con la constelación de la Calavera: seis estrellas unidas por líneas de puntos.", ["Es la constelación de la tapa del cofre (carta 40).", "Tiene seis estrellas.", "En la tapa está más pequeña y girada."]),
    "30": escena("30", "El cofre abierto", [38], [31, 40, 41, 43, 45],
                 "La tapa se levanta sola y, en el cofre, sobre un lecho de arena, hay media llave de hierro con una calavera grabada en el ojo (carta 38). Una pareja de cifras queda grabada en el interior de la tapa: guardadla.",
                 ["Mirad dentro del cofre."],
                 "Un cofre de madera abierto sobre una roca de una playa, con media llave de hierro con una calavera en el ojo sobre la arena del fondo. Cristina la levanta con dos dedos con los ojos brillantes; Alberto aplaude con las manos sobre la cabeza y una sonrisa enorme."),
    "38": combinable("38", "Mitad de la llave de la capitana", "roja", 56, 94, "Una mitad de una llave de hierro con una calavera grabada en el ojo, de las del cofre de la capitana Bruma.",
                     SIN_GENTE + "La mitad izquierda de una llave de hierro pesada con una calavera grabada en el ojo, sobre la arena de una playa."),
    # ------------------------------------------------------------------ Rama 2: la cueva
    "32": escena("32", "La entrada de la cueva", [42, 48, 49, 53], [],
                 "La entrada de la cueva está cerrada por un suelo de losas: solo se cruza pisando las que siguen el testamento del capitán Calavera, un papel que hay que plegar (carta 53). El suelo, visto desde la entrada, ocupa dos láminas: juntad la 42 a la izquierda y la 49 a la derecha. Una pantalla de piedra (carta 48) espera vuestros pasos.",
                 ["Un único puzle: el suelo de la cueva.", "El suelo son dos cartas: juntadlas, una al lado de la otra."],
                 "La boca de una cueva marina con un suelo de grandes losas con símbolos grabados, con la luz del atardecer entrando por la entrada. Cristina sostiene un papel doblado y mira el suelo con la cabeza ladeada; Alberto da un paso con precaución, con un pie en el aire y cara de miedo."),
    "48": app("48", "El suelo de la cueva", "Es un juego de la app: el suelo de la entrada de la cueva, de seis por seis losas. Se entra por abajo y hay que llegar a la fila de arriba pisando solo losas vecinas cuyos símbolos sigan, una y otra vez, el orden del testamento plegado.", 36,
              ["El testamento está en la carta 53, pero solo se lee plegado. Los símbolos de las losas están en las cartas 42 y 49.", f"Empezad en una losa de la fila de abajo con el primer símbolo ({_S_CICLO.split(', ')[0]}) y buscad siempre, al lado, el siguiente; tras el cuarto vuelve el primero. Solo un camino llega arriba.", f"Pisad, desde abajo: {_S_SUE}."],
              SIN_GENTE + "El suelo de la entrada de una cueva marina hecho de grandes losas de piedra con símbolos grabados (ancla, calavera, luna, llave, corona), con un resplandor dorado al fondo."),
    "42": pieza("42", "suelo", "Media lámina del suelo de la cueva.", ["Es la mitad de una lámina: juntadla con la carta 49.", "Son las losas con sus símbolos.", "El orden de los símbolos está en el testamento (carta 53)."]),
    "49": pieza("49", "suelo", "Media lámina del suelo de la cueva.", ["Es la mitad de una lámina: juntadla con la carta 42.", "Son las losas con sus símbolos.", "El orden de los símbolos está en el testamento (carta 53)."]),
    "53": plegable("53", "Testamento (se pliega)", "El testamento del capitán Calavera. Se pliega en acordeón hasta que la línea A toque la B: desplegado, los símbolos del centro son quimeras de dos mitades distintas; plegado, se ven cuatro símbolos de verdad, de arriba abajo. El texto dice que se pisan en ese orden, una y otra vez, de losa en losa vecina. En el Modo PC, botón «Plegar».",
                   ["Es el orden de las losas del suelo de la cueva (carta 48).", "Hay que doblarla en acordeón hasta que A toque B: la franja de en medio queda escondida detrás.", "Plegada, se ven cuatro símbolos en columna."]),
    "36": escena("36", "La santabárbara", [52, 54, 55, 59], [32, 42, 48, 49, 53],
                 "El pasadizo baja a la santabárbara, la bodega de la pólvora de La Gaviota, donde tres barcos enemigos aparecen a lo lejos. Hay que cargar y apuntar el cañón para cada uno (carta 52): la tabla de tiro por la carga está en la carta 54 y por la elevación, en la 55, y los tres barcos con su viento y la pólvora que queda, en la 59.",
                 ["Un único puzle: apuntar el cañón."],
                 "La santabárbara de un bergantín pirata, una bodega con barriles de pólvora, balas de hierro apiladas y un gran cañón de bronce asomando por una portilla, con un farol de aceite colgado. Cristina carga el cañón con una bala con la lengua entre los dientes y los ojos muy abiertos; Alberto mira por la portilla con el catalejo y cara de susto."),
    "52": app("52", "El cañón", "Es un juego de la app: tres barcos enemigos a tiro. Para cada uno hay que elegir los sacos de pólvora y la elevación del cañón de modo que el tiro caiga justo en él, sin repetir carga y sin pasarse de la pólvora que queda.", 44,
              ["Las tablas están en las cartas 54 y 55 y los barcos, el viento y la pólvora, en la 59.", "El alcance es la suma de lo que da la carga, lo que da la elevación y el viento. Para cada barco, buscad las parejas carga-elevación que dan su distancia; luego, que no se repita carga y que la pólvora alcance.", f"{_S_CAN}. Distancia del cañón: {_D['52']}."],
              SIN_GENTE + "Un gran cañón de bronce sobre su cureña, apuntando por una portilla de un barco pirata hacia tres barcos lejanos, con barriles de pólvora y balas de hierro apiladas al lado."),
    "54": gris("54", "La tabla de tiro (I)", "La tabla del artillero con el alcance, en cables, de cada carga de pólvora, de uno a seis sacos.", ["Es el alcance por la carga (carta 52).", "Más sacos, más alcance.", "La elevación y el viento se suman aparte."]),
    "55": gris("55", "La tabla de tiro (II)", "La tabla del artillero con lo que suma o resta cada elevación del cañón al alcance, en cables.", ["Es la corrección por la elevación (carta 52).", "Algunas elevaciones restan.", "La carga está en la carta 54."]),
    "59": gris("59", "Las tres presas", "Tres barcos enemigos con su distancia en cables, el viento que les afecta y los sacos de pólvora que quedan.", ["Son los tres barcos del cañón (carta 52).", "El viento suma, o resta, al alcance.", "Cada barco necesita una carga distinta."]),
    # ------------------------------------------------------------------ La toldilla
    "44": escena("44", "La toldilla", [33, 37, 39, 46, 51, 61, 63], [36, 52, 54, 55, 59],
                 "Los tres barcos huyen y la tripulación sube a la toldilla pidiendo cuentas: quieren su parte. La tripulación, por orden de antigüedad, está en la carta 37, el Código de la Hermandad en la 39 y el botín, en la 33 (carta 46). Mientras, la marea baja: para salir del puerto, La Gaviota debe cruzar tres barras de arena (carta 51); la tabla de la marea ocupa dos láminas: juntad la 61 arriba y la 63 abajo.",
                 ["Hay dos puzles: el reparto del botín y las mareas."],
                 "La toldilla de un bergantín pirata con siete piratas con pañuelos de colores alrededor de un pequeño montón de doblones de oro, junto al timón, con el puerto de una isla al fondo y la marea bajando. Cristina, con las manos en la cintura, mira a los piratas con una ceja arqueada; Alberto cuenta monedas con los dedos y cara de agobio."),
    "46": app("46", "El reparto del botín", "Es un juego de la app: siete piratas por orden de antigüedad reparten los doblones del botín según el Código de la Hermandad. Hay que proponer el reparto que se aprueba y en el que el capitán se queda con lo máximo.", 56,
              ["La tripulación está en la carta 37, el Código en la 39 y el botín, en la 33.", "Pensad en el último pirata: si quedan solo dos, ¿qué pasa? Y con tres, cuatro... Cada pirata solo vota a favor si recibe más de lo que tendría si el capitán se fuera por la borda.", f"El reparto: {_S_BOT}."],
              SIN_GENTE + "Un montón de doblones de oro sobre una mesa de capitán, con un cuaderno de cuentas abierto y un tintero, a la luz de un farol de aceite, en la toldilla de un barco pirata."),
    "37": gris("37", "La tripulación", "Los siete piratas de La Gaviota, con un pañuelo de cada color y su número de antigüedad; el 1 es el capitán.", ["Son los siete piratas del reparto (carta 46).", "Cuanto más bajo el número, más antiguo.", "El Código de la Hermandad está en la carta 39."]),
    "39": gris("39", "El Código de la Hermandad", "El Código de la Hermandad pirata, colgado en el palo mayor, en versos.", ["Explica cómo se vota el reparto (carta 46).", "Hacen falta, por lo menos, la mitad de los votos.", "Cada pirata quiere vivir, luego tener más doblones."]),
    "33": gris("33", "El botín", "El botín de la Isla Calavera, en doblones, y cuántos piratas hay a bordo.", ["Es el botín que se reparte (carta 46).", "Todos votan, también el capitán.", "La tripulación está en la carta 37."]),
    "56": combinable("56", "Otra mitad de la llave", "roja", 38, 94, "La otra mitad de la llave de hierro con la calavera, que el cocinero guardaba en la panera y os da tras ver el reparto.",
                     SIN_GENTE + "La mitad derecha de una llave de hierro pesada con una calavera grabada en el ojo, sobre una panera de madera con un paño blanco."),
    "51": app("51", "Las mareas", "Es un juego de la app: La Gaviota tiene que cruzar tres barras de arena, una al salir, otra dos horas después y otra cinco horas después de salir. Hay que elegir la hora de salida.", 58,
              ["El calado y las barras están en la carta 26 y la tabla de la marea, en las cartas 61 y 63.", "El agua sobre cada barra es la altura de la marea a la hora en que se cruza, más el fondo propio de la barra. Tiene que ser, por lo menos, el calado. Probad una hora de salida y mirad si pasáis las tres.", f"Hay que salir a las {_S_MAR}."],
              SIN_GENTE + "Un bergantín pirata varado en la arena de una barra al bajar la marea, con las olas lamiendo el casco, un faro lejano y gaviotas, a la luz del atardecer."),
    "61": pieza("61", "mareas", "Media lámina de la tabla de la marea.", ["Es la mitad de una lámina: juntadla con la carta 63.", "Son las alturas del agua de las horas 0 a 11.", "El calado y las barras están en la carta 26."]),
    "63": pieza("63", "mareas", "Media lámina de la tabla de la marea.", ["Es la mitad de una lámina: juntadla con la carta 61.", "Son las alturas del agua de las horas 12 a 23.", "El calado y las barras están en la carta 26."]),
    "58": escena("58", "La bodega", [69, 70, 71], [51, 61, 63, 26, 24],
                 "La Gaviota cruza las barras con el agua justa y fondea. En la bodega, tres cofres del botín esperan a ser pesados (carta 70) y solo hay cuatro pesas de hierro (carta 71): hay que equilibrar la balanza de cada uno (carta 69).",
                 ["Un único puzle: pesar los tres cofres."],
                 "La bodega de un bergantín pirata con tres cofres de madera con herrajes sobre una balanza de dos platillos grande, cuatro pesas de hierro en una caja y un farol de aceite. Cristina coloca una pesa en un platillo con mucho cuidado y los labios apretados; Alberto sujeta el fiel de la balanza con una mano y una mueca de concentración."),
    "69": app("69", "La balanza", "Es un juego de la app: tres cofres del botín y cuatro pesas de hierro de 1, 3, 9 y 27 libras. Cada pesa puede ir en el mismo platillo que el cofre, en el otro o quedarse fuera. Hay que equilibrar la balanza de cada cofre.", 80,
              ["Los pesos de los cofres están en la carta 70 y las pesas, en la 71.", "Las pesas pueden ir en los dos platillos: poner una con el cofre es como restarla. Empezad por la pesa más grande que no se pase del peso del cofre.", f"{_S_PES}. Distancia de la balanza: {_D['69']}."],
              SIN_GENTE + "Una gran balanza de dos platillos con un cofre de madera en un platillo y varias pesas de hierro en el otro, en la bodega de un barco pirata, con luz de farol."),
    "70": gris("70", "Los cofres del botín", "Tres cofres del botín con el peso de cada uno, en libras.", ["Son los tres cofres de la balanza (carta 69).", "Cada cofre se pesa por separado.", "Las pesas están en la carta 71."]),
    "71": gris("71", "Las pesas de hierro", "Cuatro pesas de hierro de 1, 3, 9 y 27 libras sobre una balanza, con una regla en versos.", ["Son las pesas de la balanza (carta 69).", "Solo hay una pesa de cada.", "Se pueden poner en cualquiera de los dos platillos."]),
    "80": escena("80", "La playa", [72, 75, 79], [58, 69, 70, 71],
                 "Los cofres quedan pesados y desembarcáis en la playa de la Isla Calavera, donde la marea ya sube. En un papel, el mapa de la isla, que hay que plegar por los dos lados como hacía el capitán (carta 75); y, en la roca, el plano de la entrada de la gruta (carta 79). Un candado de flechas guarda el tesoro (carta 72).",
                 ["Un único puzle: la X del mapa."],
                 "Una playa de arena blanca de una isla del Caribe al atardecer, con palmeras y una gran roca con forma de calavera, y la marea subiendo. Cristina despliega un mapa de pergamino con los ojos entrecerrados y una sonrisa de emoción; Alberto cava un hoyo con una pala, sudoroso y con el tricornio ladeado."),
    "72": app("72", "Cavar en la gruta", "Es un juego de la app: el suelo de arena de la gruta repite la cuadrícula del mapa de la isla, pero se entra por el este, así que se ve girado. Hay que cavar en la casilla de la X del mapa plegado por los dos lados.", 82,
              ["El mapa está en la carta 75 y el plano de la entrada de la gruta, en la 79. El mapa solo se lee plegado por los dos lados.", "Contad las casillas desde la palmera hasta la X en el mapa plegado, y pasadlas a la gruta: allí el norte queda a la derecha.", f"La X está {_S_GRU}. Distancia de la gruta: {_D['72']}."],
              SIN_GENTE + "El suelo de arena de una gruta marina vista desde la entrada, con una palmera de piedra en una esquina y la marea entrando por el fondo, con luz dorada de atardecer."),
    "75": plegable("75", "Mapa de la isla (se pliega)", "El mapa de la Isla Calavera con una cuadrícula y el camino de la palmera a la X. Se pliega por los dos lados (A sobre B y C sobre D): plegado, la roca calavera aparece entera y la cuadrícula tiene las mismas casillas que el suelo de la gruta. En el Modo PC, botón «Plegar».",
                   ["Es el mapa de la gruta (carta 72).", "Hay que doblarlo por los dos lados: A sobre B y C sobre D.", "Plegado, el camino de la palmera a la X tiene las casillas justas."]),
    "79": gris("79", "La entrada de la gruta", "El plano de la entrada de la gruta con una cuadrícula, el norte a la derecha y la entrada por el este, con unos versos.", ["Es el plano de la gruta (carta 72).", "Se entra por el este.", "El norte cae a la derecha."]),
    "82": escena("82", "El camarote de la capitana", [85, 86, 87], [80, 72, 75, 79],
                 "La trampilla del tesoro se abre y el oro brilla: el tesoro del capitán Calavera. Con él a bordo, la capitana Bruma os lleva a su camarote: el anillo del Cronoportal solo se abrirá en el sitio del mar donde la niebla es más espesa, y su carta marca cinco rumbos desde la salida (carta 86), con las distancias que os dejaron cinco puzles. La carta de la isla, con la casilla de salida, es la 87 y el punto se marca en la 85.",
                 ["Un único puzle: el punto de la niebla."],
                 "El camarote de una capitana pirata con una mesa cubierta de cartas, un compás de latón y un gran ventanal que da al mar, y un cofre abierto con oro. La capitana Bruma, con sombrero de plumas, señala una carta con un dedo con una sonrisa de orgullo; Cristina y Alberto la miran, ella con los ojos muy abiertos y él con las cejas arqueadas."),
    "85": app("85", "El punto de la niebla", "Es un juego de la app: cinco rumbos de rosa de los vientos con las distancias, en casillas, que dejaron otros puzles. Hay que marcar la casilla donde acaba el viaje desde la salida.", 99,
              ["Los rumbos están en la carta 86 y la carta de la isla, con la salida, en la 87.", "Las cinco distancias las dejaron la bitácora, las estrellas, el cañón, la balanza y la gruta. Cada rumbo es una flecha de rosa de los vientos (el norte, arriba): avanzad en esa dirección tantas casillas como diga la distancia, en diagonal si la flecha lo es.", f"Acabáis en la {_S_ISL}."],
              SIN_GENTE + "Una carta náutica extendida sobre una mesa con un compás de latón, una regla y un lápiz, con unas rosas de los vientos dibujadas y una cuadrícula en el mar, a la luz de un farol."),
    "86": gris("86", "Los cinco rumbos", "Cinco rumbos dibujados con una rosa de los vientos, cada uno con el dibujo del puzle que deja su distancia y una raya para escribirla.", ["Explica los cinco rumbos del viaje (carta 85).", "Cada rumbo lleva el dibujo de un puzle: la bitácora, las estrellas, el cañón, la balanza y la gruta.", "La flecha de cada rosa va hacia donde hay que ir; el norte, arriba."]),
    "87": gris("87", "La carta de la Isla Calavera", "La carta de la Isla Calavera: una cuadrícula de diez por diez con la casilla de salida de La Gaviota.", ["Es la carta del viaje (carta 85).", "Las casillas están numeradas.", "La salida está marcada con el barco."]),
    # ------------------------------------------------------------------ El cofre de la capitana y el final
    "94": escena("94", "El cofre de la capitana", [64, 66, 67], [38, 56, 30, 44, 33, 37, 39, 46],
                 "Las dos mitades de la llave encajan en el cofre de la capitana Bruma, donde el loro dejó el cristal. Pero el cofre está sobre el timón y se cierra con un candado de brújula: hay que fijar el rumbo que debe marcar la aguja para ir a la isla (carta 64). La carta náutica plegada está en la carta 66 y el cuaderno del piloto, en la 67.",
                 ["Un único puzle: el rumbo de la aguja."],
                 "El timón de un bergantín pirata con un gran cofre de la capitana encima, con un candado en forma de brújula de latón, y el mar al fondo. Cristina gira la rueda de la brújula con la lengua entre los dientes y los ojos muy abiertos; Alberto sostiene la carta náutica con las dos manos y cara de mucha concentración."),
    "64": app("64", "El timón", "Es un juego de la app: fijar en la brújula el rumbo que debe marcar la aguja, que en este mar se tuerce. La carta náutica plegada da el rumbo verdadero y el cuaderno del piloto, cuánto se tuerce la aguja.", 62,
              ["La carta náutica plegada está en la carta 66 y el cuaderno del piloto, en la 67.", "Hay que doblar la carta náutica hasta que A toque B: los arrecifes dibujan entonces el rumbo verdadero con dos cifras. La aguja se tuerce hacia el oeste tantas rayitas (5 grados cada una) como dibuja el arco: ese tanto hay que sumar.", f"El rumbo de la aguja: {_S_RUM}."],
              SIN_GENTE + "Un compás de latón sobre el timón de madera de un bergantín pirata, con una rosa de los vientos pintada y la aguja temblando, y el mar turquesa al fondo."),
    "66": plegable("66", "Carta náutica (se pliega)", "La carta náutica del Mar de las Brumas. Es una carta que SE PLIEGA: hay que doblarla en acordeón hasta que la línea A toque la línea B, de modo que la franja de en medio quede escondida detrás. Plegada, los arrecifes dibujan el rumbo verdadero a la Isla Calavera. En el Modo PC, botón «Plegar».",
                   ["Es la carta del rumbo (carta 64).", "Hay que doblarla en acordeón hasta que A toque B.", "Plegada, los arrecifes forman dos cifras."]),
    "67": gris("67", "El cuaderno del piloto", "El cuaderno del piloto: una brújula con la aguja torcida hacia el oeste y un arco con rayitas entre la estrella polar y la aguja.", ["Es el desvío de la aguja (carta 64).", "Cada rayita del arco son 5 grados.", "El timón obedece a la aguja."]),
    "62": combinable("62", "El cristal del Cronoportal", "roja", 12, 74, "El cristal del Cronoportal, que el loro dejó en el cofre de la capitana Bruma.",
                     SIN_GENTE + "Un cristal redondo de color azul brillante, del tamaño de una moneda grande, con destellos de luz, sobre un lecho de terciopelo rojo en un cofre de madera con herrajes abierto, a la luz de un farol."),
    "74": escena("74", "Cronoportal con el cristal", [], [62, 12, 64, 66, 67, 94, 57],
                 "Encajáis el cristal en el pecho del Cronoportal y el anillo se enciende con un arco de luz azul. Fuera, la marea sube: el agua ya cubre la gruta y solo falta llegar al punto de la niebla donde se abre el anillo (carta 85).",
                 ["Ya solo queda llegar al punto de la niebla."],
                 "Cristina y Alberto encajan un cristal azul brillante en el hueco del Cronoportal, un aparato de latón y cristal con un anillo que se enciende con un arco de luz azul, sobre la cubierta de un bergantín pirata al atardecer. Cristina lo sostiene con las dos manos con una enorme sonrisa; Alberto contiene el aliento mirando el anillo con la boca abierta."),
    "99": escena("99", "De vuelta a casa (FIN)", [], [74, 82, 85, 86, 87],
                 "La Gaviota llega al punto de la niebla, el anillo se abre en un arco de luz justo cuando el agua cubre la gruta y la capitana Bruma os despide con el sombrero en alto. Aterrizáis en vuestro salón, empapados y con olor a mar. Alberto mira el aparato: «Mañana, otro destino». Cristina sonríe y guarda en el bolsillo un doblón de oro. FIN.",
                 [],
                 "La escena ocurre DENTRO del salón de su casa actual, en el presente (sofá, estanterías con libros, plantas, una lámpara encendida y luz cálida de tarde por la ventana): acaban de VOLVER a casa. Cristina y Alberto acaban de salir de un portal circular de luz azul y dorada que se abre detrás de ellos; a través del portal todavía se ven un barco pirata en medio de la niebla, una gruta marina y la capitana Bruma saludando con el sombrero. Llevan aún su ropa de pirata, empapados y goteando sobre la alfombra. Cristina ríe a carcajadas enseñando un doblón de oro en la palma de la mano y Alberto, con el tricornio torcido, escurre agua de su casaca con cara de alivio. Están de cara a nosotros, aterrizando en el salón y alejándose del portal, que queda a su espalda y se está cerrando; el mundo de la aventura solo se ve a través del portal, detrás de ellos. No están entrando en el portal ni saliendo de casa: están llegando."),
}

META = dict(juego="Mar de las Brumas, 1715 — El Tesoro de la Isla Calavera", estilo=ESTILO, personajes=PERSONAJES, hoja=HOJA, foto=FOTO, video=VIDEO,
            mosaicos={k: dict(filas=m["filas"], cols=m["cols"], cartas=m["cartas"], titulo=m["titulo"]) for k, m in MOSAICOS.items()})

SPEC = dict(final="99", needs={
    "24": ["14", "16"], "28": ["20", "18", "19", "21"], "57": ["22", "35"], "30": ["40", "41", "43", "45"], "36": ["48", "42", "49", "53"],
    "44": ["52", "54", "55", "59"], "56": ["46", "37", "39", "33"], "58": ["51", "26", "61", "63"], "80": ["69", "70", "71"], "94": ["38", "56"],
    "62": ["64", "66", "67"], "82": ["72", "75", "79"], "74": ["12", "62"], "99": ["85", "86", "87", "74"]}, eventos={})

PARA_QUE = {k: c["titulo"].split("— ", 1)[1] for k, c in J.items()}

_T = [
    ("leer", "P", "Llegada", "Pon el Modo PC (solo la P en la mesa) y en el móvil pulsa Empezar. Lee la carta P: coge la 10 y la 12."),
    ("leer", "10", "La cubierta de La Gaviota", "Lee la carta 10. Descarta la P y coge 14, 16, 18, 19, 20, 21 y 22. Junta la carta de aguas: 19 arriba y 21 abajo."),
    ("app", "14", "La bitácora", f"En el móvil: Acción, 14. Con la bitácora (16), el tiempo entre el aviso 1 y el aviso 3 es de {_S_BIT}. El mensaje te dice que cojas la 24. Anota la distancia de la bitácora: {_D['14']}.", "carta 24"),
    ("leer", "24", "El pañol de la capitana", "Lee la carta 24. Descarta 14 y 16 y coge la 26 (guárdala para las mareas)."),
    ("app", "20", "La persecución", f"En el móvil: Acción, 20. Con la carta de aguas (19 y 21) y la ordenanza (18), una salida es: {_S_PER}. El mensaje te dice que cojas la 28.", "carta 28"),
    ("leer", "28", "El banco de niebla", "Lee la carta 28. Descarta 18, 19, 20 y 21 y coge la 35."),
    ("combinar", "22", "35", "El catalejo", "Las dos mitades de la lente (22 y 35) son combinables: 22 + 35 = 57. Coge la 57."),
    ("leer", "57", "El catalejo", "Lee la carta 57. Descarta 22, 35, 10 y 28 y coge 31 y 32."),
    ("leer", "31", "El cofre del capitán Calavera", "Lee la carta 31. Coge 40, 41, 43 y 45. Junta el cielo: 41 a la izquierda y 43 a la derecha."),
    ("app", "40", "La tapa del cofre", f"En el móvil: Acción, 40. Con el cielo (41 y 43) y la carta celeste (45), las estrellas de la Calavera son {_S_CIE}. El mensaje te dice que cojas la 30. Anota la distancia de las estrellas: {_D['40']}.", "carta 30"),
    ("leer", "30", "El cofre abierto", "Lee la carta 30. Descarta 31, 40, 41, 43 y 45 y coge la 38."),
    ("leer", "32", "La entrada de la cueva", "Lee la carta 32. Coge 42, 48, 49 y 53. Junta el suelo: 42 a la izquierda y 49 a la derecha. Pliega el testamento (53): A sobre B."),
    ("app", "48", "El suelo de la cueva", f"En el móvil: Acción, 48. Con el testamento plegado (53) y el suelo (42 y 49), el orden de los símbolos es {_S_CICLO} y el camino, desde abajo: {_S_SUE}. El mensaje te dice que cojas la 36.", "carta 36"),
    ("leer", "36", "La santabárbara", "Lee la carta 36. Descarta 32, 42, 48, 49 y 53 y coge 52, 54, 55 y 59."),
    ("app", "52", "El cañón", f"En el móvil: Acción, 52. Con las tablas (54 y 55) y las presas (59): {_S_CAN}. El mensaje te dice que cojas la 44. Anota la distancia del cañón: {_D['52']}.", "carta 44"),
    ("leer", "44", "La toldilla", "Lee la carta 44. Descarta 36, 52, 54, 55 y 59 y coge 33, 37, 39, 46, 51, 61 y 63. Junta la tabla de la marea: 61 arriba y 63 abajo."),
    ("app", "46", "El reparto del botín", f"En el móvil: Acción, 46. Con la tripulación (37), el Código (39) y el botín (33), el reparto es: {_S_BOT}. El mensaje te dice que cojas la 56.", "carta 56"),
    ("app", "51", "Las mareas", f"En el móvil: Acción, 51. Con el calado (26) y la tabla de la marea (61 y 63), hay que salir a las {_S_MAR}. El mensaje te dice que cojas la 58.", "carta 58"),
    ("leer", "58", "La bodega", "Lee la carta 58. Descarta 51, 61, 63, 26 y 24 y coge 69, 70 y 71."),
    ("app", "69", "La balanza", f"En el móvil: Acción, 69. Con los cofres (70) y las pesas (71): {_S_PES}. El mensaje te dice que cojas la 80. Anota la distancia de la balanza: {_D['69']}.", "carta 80"),
    ("leer", "80", "La playa", "Lee la carta 80. Descarta 58, 69, 70 y 71 y coge 72, 75 y 79. Pliega el mapa (75): A sobre B y C sobre D."),
    ("app", "72", "Cavar en la gruta", f"En el móvil: Acción, 72. Con el mapa plegado (75) y el plano de la gruta (79), la X está {_S_GRU}. El mensaje te dice que cojas la 82. Anota la distancia de la gruta: {_D['72']}.", "carta 82"),
    ("leer", "82", "El camarote de la capitana", "Lee la carta 82. Descarta 80, 72, 75 y 79 y coge 85, 86 y 87."),
    ("combinar", "38", "56", "La llave de la capitana", "Las dos mitades de la llave (38 y 56) son combinables: 38 + 56 = 94. Coge la 94."),
    ("leer", "94", "El cofre de la capitana", "Lee la carta 94. Descarta 38, 56, 30, 44, 33, 37, 39 y 46 y coge 64, 66 y 67. Pliega la carta náutica (66): A sobre B."),
    ("app", "64", "El timón", f"En el móvil: Acción, 64. Con la carta náutica plegada (66) y el cuaderno del piloto (67), el rumbo de la aguja es {_S_RUM}. El mensaje te dice que cojas la 62.", "carta 62"),
    ("combinar", "12", "62", "El cristal", "El Cronoportal (12) y el cristal (62) son combinables: 12 + 62 = 74. Coge la 74."),
    ("leer", "74", "Cronoportal con el cristal", "Lee la carta 74. Descarta 62, 12, 64, 66, 67, 94 y 57."),
    ("app", "85", "El punto de la niebla", f"En el móvil: Acción, 85. Con los rumbos (86) y la carta de la isla (87), y las distancias de la bitácora, las estrellas, el cañón, la balanza y la gruta, el ancla se echa en la {_S_ISL}. El mensaje te dice que cojas la 99.", "carta 99"),
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
