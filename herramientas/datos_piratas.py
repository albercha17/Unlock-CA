"""Mar de las Brumas, 1715: El Tesoro de la Isla Calavera. Duodécima parada del Cronoportal: un barco pirata en el Caribe. La mecánica de cartas
nueva son las CARTAS QUE SE PLIEGAN (como los «fold-in» de la revista MAD): una carta náutica, un testamento y un mapa que, plegados en acordeón
hasta que la línea A toque la B (y la C, la D), enseñan lo que desplegados esconden. Los puzles de la app tampoco se han usado antes: timón con
brújula y desvío de la aguja, bodega de barriles (empujar), persecución de una fragata con regla fija (como el Minotauro), constelación
girada en la tapa de un cofre, suelo de losas que se cruza siguiendo un ciclo de símbolos y cavar en un mapa visto girado. Las cartas que se dibujan por código (30, 31, 40, 52, 64, 70 y 76) las hace herramientas/piratas.py
(a partir de instancias_piratas.json)."""
import json
import os

_AQUI = os.path.dirname(os.path.abspath(__file__))
INST = json.load(open(os.path.join(_AQUI, "instancias_piratas.json"), encoding="utf-8"))
RUMBO = INST["rumbo"]
PERSIGUE = INST["persecucion"]
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


_PERSIGUE = ", ".join(PERSIGUE["solucion"])
_CICLO = ", ".join(LOSAS["ciclo"])
_SUELO = ", ".join(f"{LOSAS['suelo'][y][x]} (fila {LOSAS['n'] - y}, columna {x + 1})" for x, y in LOSAS["camino"])
_xm, _ym = RUTA["celdas"][-1]
_xp, _yp = RUTA["inicio"]
_X = f"{_xm - _xp} casillas al este y {_ym - _yp} al sur de la palmera"
_XG = f"fila {_xm + 1} desde arriba, columna {RUTA['filas'] - _ym} desde la izquierda"

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


def pieza(titulo, que):
    return f"Carta dibujada por código (herramientas/piratas.py; no se pide a ChatGPT): {que} de «{titulo}»."


J = {
    "P": dict(
        titulo="Carta P — Llegada a bordo", tipo="gris", coge=[10, 12],
        descripcion=[
            "Duodécima parada del Cronoportal: el Mar de las Brumas, en 1715. Aterrizáis sobre la cubierta de La Gaviota, un bergantín pirata, entre cuerdas y barriles. Antes de que os pongáis en pie, un loro verde y rojo baja en picado y se lleva en el pico el cristal de energía del aparato.",
            "El loro se llama Doblón y es de la capitana Leonor Bruma, que guarda el cristal en su cofre: «Una gema así paga el pasaje de dos polizones... salvo que me ayudéis a encontrar el tesoro del capitán Calavera antes de que la marea cubra su cueva, al ponerse el sol».",
            "Coged las cartas 10 y 12."],
        pistas=["Mirad a vuestro alrededor y revisad el aparato.", "Coged las cartas 10 y 12."],
        arte="La cubierta de un bergantín pirata al atardecer, con cuerdas, barriles y velas remendadas. Un loro verde y rojo vuela con un cristal rojo brillante en el pico. En primer plano, el Cronoportal, un aparato de latón y cristal, humea en el suelo de madera. Cristina, despeinada y con la boca abierta de sorpresa, señala al loro, y Alberto, en el suelo, se sujeta el tricornio con cara de incredulidad."),
    "10": dict(
        titulo="Carta 10 — La cubierta de La Gaviota", tipo="gris", coge=[22, 24, 30, 31], descarta=["P"],
        descripcion=[
            "La capitana Bruma os lleva al timón: «El piloto se ha bebido el ron de la semana. Fijad vosotros el rumbo a la Isla Calavera». Os da la carta náutica (carta 30), que hay que plegar como hacía su piloto, y el cuaderno del piloto (carta 31). Junto al timón (carta 24), Cristina encuentra una lente de catalejo suelta (carta 22).",
            "Coged las cartas 22, 24, 30 y 31. Descartad la carta P."],
        pistas=["Hay un puzle: el timón, la carta náutica y el cuaderno del piloto.", "La carta náutica (30) es una carta que se pliega: buscad las líneas A y B.", "Coged las cartas 22, 24, 30 y 31. Descartad la carta P."],
        arte="La cubierta de un bergantín pirata con un gran timón de madera, el mástil y las velas hinchadas por el viento; una capitana con sombrero de plumas y casaca roja señala el horizonte con un loro en el hombro. Cristina recoge del suelo una lente de cristal con curiosidad y los ojos entrecerrados, y Alberto sujeta un mapa enrollado con gesto de preocupación."),
    "12": dict(
        titulo="Carta 12 — Cronoportal sin cristal", tipo="azul", combina=[62, 74],
        descripcion=[
            "El Cronoportal: una consola de latón y cristal con un anillo central apagado y un hueco vacío en el pecho, donde iba el cristal de energía. Alberto: «Sin el cristal no hay vuelta a casa. Y la capitana no lo soltará sin su tesoro».",
            "Cuando recuperéis el cristal (carta 62), combinadlo con el Cronoportal: sumad sus números (12 + 62 = 74) y coged la carta 74."],
        pistas=["Le falta una pieza: el cristal de energía.", "Combinad la carta 12 con la carta 62.", "Sumad los números de las dos cartas: 12 + 62 = 74."],
        arte="Primer plano del Cronoportal: una consola portátil de latón y cristal con dos antenas de cobre, un anillo de cristal central apagado y un hueco circular vacío en el pecho del aparato, apoyado sobre la madera mojada de la cubierta de un barco, con cuerdas y un barril desenfocados al fondo."),
    "22": dict(
        titulo="Carta 22 — Lente de catalejo", tipo="azul", combina=[35, 57],
        descripcion=["Una lente de cristal gruesa, con un aro de latón: es de un catalejo. Combinadla con el tubo del catalejo (carta 35): sumad sus números (22 + 35 = 57) y coged la carta 57."],
        pistas=["Es la lente de un catalejo, pero le falta el tubo.", "Cuando encontréis el tubo, combinadlo con la lente.", "Sumad los números de las dos cartas: 22 + 35 = 57."],
        arte="Una lente de catalejo de cristal grueso con un aro de latón, sobre las tablas mojadas de la cubierta de un barco, con un reflejo del atardecer en el cristal, vista de cerca."),
    "30": dict(
        titulo="Carta 30 — Carta náutica (se pliega)", tipo="gris", plegado=_plegado("30"),
        descripcion=["La carta náutica del Mar de las Brumas. Es una carta que SE PLIEGA: hay que doblarla en acordeón hasta que la línea A toque la línea B, de modo que la franja de en medio quede escondida detrás. Plegada, los arrecifes dibujan el rumbo verdadero a la Isla Calavera. En el Modo PC, botón «Plegar»."],
        pistas=["Desplegada engaña: los arrecifes forman otros números. Buscad las líneas A y B.", "Plegadla en acordeón hasta que A toque B (en el Modo PC, botón «Plegar»): los arrecifes de los dos lados se juntan. Leed de arriba abajo.", f"Plegada, la carta dice {RUMBO['carta']}: es el rumbo verdadero."],
        arte=pieza("Carta náutica", "la carta plegable con los arrecifes")),
    "31": dict(
        titulo="Carta 31 — Cuaderno del piloto", tipo="gris",
        descripcion=["El cuaderno del piloto: una brújula dibujada en la que la aguja no apunta a la estrella polar (el norte verdadero), sino un poco al oeste. Entre la estrella y la aguja hay un arco con rayitas de 5 grados. Para gobernar con la aguja: rumbo de la carta + desvío."],
        pistas=["Es lo que hay que corregir al rumbo de la carta náutica (carta 30).", "Contad los huecos entre las rayitas del arco, entre la estrella y la aguja: cada uno son 5 grados. Ese es el desvío, y se suma.", f"El desvío es de {RUMBO['desvio']} grados: el rumbo de la aguja es {RUMBO['carta']} + {RUMBO['desvio']} = {RUMBO['aguja']}."],
        arte=pieza("Cuaderno del piloto", "la brújula con el desvío")),
    "24": dict(
        titulo="Carta 24 — El timón", tipo="verde",
        descripcion=[
            "Es un juego de la app: un timón con su brújula. Se gira la rosa de 5 en 5 grados hasta el rumbo que debe marcar la aguja y se fija. El rumbo verdadero sale de la carta náutica plegada (carta 30) y el desvío de la aguja, del cuaderno del piloto (carta 31).",
            "Al acertar, La Gaviota pone proa a la Isla Calavera. Coged la carta 26."],
        pistas=["Hacen falta las dos cartas: la carta náutica plegada (30) y el cuaderno del piloto (31).", "Plegad la carta 30 para leer el rumbo verdadero y sumadle el desvío de la aguja que dibuja la carta 31.", f"Fijad el timón en {RUMBO['aguja']} grados ({RUMBO['carta']} + {RUMBO['desvio']})."],
        arte="El gran timón de madera de un bergantín pirata con una bitácora de latón y una brújula iluminada por un farol, el mar al atardecer al fondo. Alberto gira el timón con fuerza y la mandíbula apretada de esfuerzo y Cristina mira la brújula con la nariz arrugada de concentración."),
    "26": dict(
        titulo="Carta 26 — Rumbo a la Isla Calavera", tipo="gris", coge=[35, 40, 46], descarta=[10, 24, 30, 31],
        descripcion=[
            "La Gaviota vira y navega a toda vela. Pero una ola de costado hace crujir el casco: en la bodega, los barriles de pólvora se han soltado y ruedan junto a la cocina. El contramaestre os da el plano de estiba (carta 40) y os manda abajo (carta 46). Entre los cabos, Alberto encuentra el tubo de un catalejo sin lente (carta 35).",
            "Coged las cartas 35, 40 y 46. Descartad las cartas 10, 24, 30 y 31."],
        pistas=["Hay dos cosas: la bodega y el tubo del catalejo.", "Las cartas 22 y 35 son combinables. El plano de estiba (40) sirve para la bodega (46).", "Coged las cartas 35, 40 y 46. Descartad las cartas 10, 24, 30 y 31."],
        arte="Un bergantín pirata navegando a toda vela por un mar picado al atardecer, con espuma saltando por la borda y gaviotas. Cristina se agarra a un cabo con el pelo al viento y una carcajada de emoción, y Alberto, empapado por una ola, levanta un tubo de catalejo de latón con cara de sorpresa."),
    "35": dict(
        titulo="Carta 35 — Tubo de catalejo", tipo="roja", combina=[22, 57],
        descripcion=["El tubo de latón de un catalejo, con sus anillas, pero sin la lente de delante. Combinadlo con la lente (carta 22): sumad sus números (35 + 22 = 57) y coged la carta 57."],
        pistas=["Es un catalejo al que le falta la lente.", "Combinad la carta 35 con la carta 22.", "Sumad los números de las dos cartas: 35 + 22 = 57."],
        arte="El tubo de latón de un catalejo plegable, sin lente delantera, enredado entre cabos y redes sobre la cubierta de un barco, con gotas de agua de mar y luz dorada, visto de cerca."),
    "40": dict(
        titulo="Carta 40 — Plano de estiba", tipo="gris",
        descripcion=["El plano de la bodega de La Gaviota, con la proa arriba: las cuadernas por donde no se puede pasar y unas X rojas donde deben ir los barriles de pólvora, lejos de la cocina."],
        pistas=["Es el plano de la bodega (carta 46).", "En la app no se ven las X: marcadlas con tiza (tocad las casillas) copiándolas del plano, con la proa arriba.", "Hay que dejar un barril sobre cada X del plano."],
        arte=pieza("Plano de estiba", "el plano de la bodega")),
    "46": dict(
        titulo="Carta 46 — La bodega", tipo="verde",
        descripcion=[
            "Es un juego de la app: la bodega vista desde arriba, con tres barriles de pólvora sueltos. Se mueve al marinero con las flechas y empuja los barriles (no se puede tirar de ellos). Hay que dejarlos sobre las X del plano de estiba (carta 40), que en la app no se ven: se pueden marcar con tiza.",
            "Al estibarlos, el contramaestre respira tranquilo. Coged la carta 44."],
        pistas=["Copiad las X del plano de estiba (carta 40) con la tiza: tocad esas casillas.", "Los barriles solo se pueden empujar: no dejéis ninguno en un rincón ni pegado a una cuaderna si no es su X. Hay botones para deshacer y empezar de nuevo.", "Llevad primero a su X el barril que está más lejos de la cocina y despejad el camino de los otros dos."],
        arte="La bodega de un barco pirata a la luz de un farol, con barriles de pólvora tumbados que ruedan entre sacos y cuadernas de madera. Cristina empuja un barril con el hombro y los dientes apretados de esfuerzo y Alberto señala un hueco con el farol en alto y cara de alarma."),
    "44": dict(
        titulo="Carta 44 — La bodega estibada", tipo="gris", coge=[38], descarta=[26, 40, 46],
        descripcion=[
            "Los barriles quedan bien sujetos sobre sus X. El contramaestre os da las gracias y una antorcha apagada (carta 38): «En la Isla Calavera hay una cueva, y dentro no se ve ni la mano».",
            "Coged la carta 38. Descartad las cartas 26, 40 y 46."],
        pistas=["Mirad lo que os da el contramaestre.", "La carta 38 es combinable.", "Coged la carta 38. Descartad las cartas 26, 40 y 46."],
        arte="La bodega de un barco pirata con los barriles de pólvora bien atados con cuerdas, a la luz de un farol; un contramaestre tuerto y fornido entrega una antorcha apagada. Alberto la coge con una sonrisa de orgullo y Cristina se seca el sudor de la frente con cara de alivio."),
    "38": dict(
        titulo="Carta 38 — Antorcha apagada", tipo="azul", combina=[56, 94],
        descripcion=["Una antorcha de madera envuelta en trapos con brea, apagada. Combinadla con el pedernal y el eslabón (carta 56): sumad sus números (38 + 56 = 94) y coged la carta 94."],
        pistas=["Es una antorcha, pero no tenéis con qué encenderla.", "Cuando tengáis el pedernal, combinadlo con la antorcha.", "Sumad los números de las dos cartas: 38 + 56 = 94."],
        arte="Una antorcha de madera envuelta en trapos negros de brea, apagada, apoyada en un barril de un barco, con cuerdas alrededor y luz de farol, vista de cerca."),
    "57": dict(
        titulo="Carta 57 — El catalejo", tipo="gris", coge=[48, 52], descarta=[22, 35],
        descripcion=[
            "Con la lente en su sitio, Cristina mira por el catalejo y se le corta la respiración: una fragata de la Armada viene a por vosotros. La capitana Bruma no se inmuta: «Esa fragata navega siempre igual, según su ordenanza (carta 52). Si llegamos al banco de niebla, no nos verá». La carta de navegación de la persecución es la 48.",
            "Coged las cartas 48 y 52. Descartad las cartas 22 y 35."],
        pistas=["Hay un puzle: la persecución y la ordenanza de la fragata.", "La ordenanza (carta 52) dice exactamente cómo se mueve la fragata.", "Coged las cartas 48 y 52. Descartad las cartas 22 y 35."],
        arte="Cristina mira por un catalejo de latón desde la borda de un barco pirata, con la boca abierta de alarma; en el horizonte, una fragata de guerra con muchas velas se acerca entre islotes rocosos y, a lo lejos, un banco de niebla blanca. Alberto, a su lado, se lleva las manos a la cabeza con cara de pánico."),
    "52": dict(
        titulo="Carta 52 — Ordenanza de la Armada", tipo="gris",
        descripcion=["La ordenanza de la Armada con la regla de persecución de sus fragatas: por cada casilla que avanza el pirata (o cada turno que se queda quieto), la fragata da dos pasos; en cada paso se acerca primero en horizontal y, si no puede, en vertical; si tampoco, se queda quieta. No cruza las rocas. Trae un ejemplo dibujado."],
        pistas=["Es la regla de la fragata de la persecución (carta 48).", "Como la fragata siempre intenta primero acercarse en horizontal, una roca puede dejarla atascada: buscad dónde se queda quieta.", f"Una solución: {_PERSIGUE}."],
        arte=pieza("Ordenanza de la Armada", "la regla de la fragata con su ejemplo")),
    "48": dict(
        titulo="Carta 48 — La persecución", tipo="verde",
        descripcion=[
            "Es un juego de la app: un mar con rocas en cuadrícula, La Gaviota, la fragata y el banco de niebla. Por cada casilla que avanzáis (o cada turno que esperáis), la fragata da dos pasos según su ordenanza (carta 52). Hay que meterse en la niebla sin que os alcance. Se puede deshacer.",
            "Al llegar a la niebla, la fragata os pierde. Coged la carta 58."],
        pistas=["Leed la ordenanza (carta 52): la fragata es rápida, pero muy previsible.", "Ir derecho a la niebla no funciona. Atraed a la fragata a un sitio donde una roca la deje atascada y usad «Esperar» cuando os convenga.", f"Una solución: {_PERSIGUE}."],
        arte="Un barco pirata huye a toda vela entre islotes rocosos perseguido por una fragata de guerra que dispara un cañonazo de aviso, hacia un banco de niebla blanca. Alberto, al timón, gira la rueda con los dientes apretados de tensión y Cristina, agarrada a un cabo, mira hacia atrás con los ojos muy abiertos de miedo."),
    "58": dict(
        titulo="Carta 58 — Desembarco en la Isla Calavera", tipo="gris", coge=[64, 66], descarta=[48, 52, 57],
        descripcion=[
            "La fragata se pierde en la niebla y La Gaviota fondea frente a la Isla Calavera. En el viejo campamento del capitán Calavera, entre palmeras, hay un cofre cuya tapa es un cielo de tachuelas con forma de estrella (carta 66). Clavada en un poste, la carta celeste del capitán (carta 64).",
            "Coged las cartas 64 y 66. Descartad las cartas 48, 52 y 57."],
        pistas=["Hay un puzle: la tapa del cofre y la carta celeste.", "La carta celeste (64) dibuja la constelación de la Calavera.", "Coged las cartas 64 y 66. Descartad las cartas 48, 52 y 57."],
        arte="Una playa de arena blanca con palmeras al atardecer y un viejo campamento pirata: un cofre grande con la tapa cuajada de tachuelas doradas en forma de estrellas y un poste con un pergamino clavado. Cristina salta de un bote al agua con una sonrisa radiante y Alberto, todavía en el bote, mira el cofre con una ceja levantada de duda."),
    "64": dict(
        titulo="Carta 64 — Carta celeste", tipo="gris",
        descripcion=["La carta celeste del capitán Calavera: la constelación de la Calavera, de seis estrellas, con sus líneas. En la tapa del cofre aparece más pequeña y girada, entre muchas otras estrellas."],
        pistas=["Es la constelación de la tapa del cofre (carta 66).", "Fijaos en la forma: una estrella arriba, dos a los lados, otras dos más abajo y una sola en la punta. En la tapa está girada: buscad esa forma de lado.", "En la tapa, la Calavera está girada un tercio de vuelta (120 grados), en la parte de arriba a la derecha del centro."],
        arte=pieza("Carta celeste", "la constelación de la Calavera")),
    "66": dict(
        titulo="Carta 66 — La tapa del cofre", tipo="verde",
        descripcion=[
            "Es un juego de la app: la tapa del cofre del capitán Calavera, con treinta tachuelas en forma de estrella. Hay que tocar las seis que forman la constelación de la Calavera de la carta celeste (carta 64), que en la tapa está girada y es más pequeña.",
            "Al acertar, el cofre se abre. Coged la carta 72."],
        pistas=["Hace falta la carta celeste (carta 64): la forma de la Calavera.", "La forma es la misma pero girada: buscad seis tachuelas con una arriba, dos a los lados, dos más abajo y una en la punta, y girad la carta hasta que encaje.", "Está girada un tercio de vuelta, arriba a la derecha del centro de la tapa: es la única forma así en toda la tapa."],
        arte="La tapa de un cofre pirata de madera oscura cuajada de tachuelas doradas en forma de estrella, como un cielo nocturno, en una playa al atardecer. Alberto acerca la nariz a la tapa con los ojos entrecerrados de concentración y Cristina gira una carta celeste en las manos con la lengua entre los dientes."),
    "72": dict(
        titulo="Carta 72 — El cofre del capitán Calavera", tipo="gris", coge=[76, 79], descarta=[58, 64, 66],
        descripcion=[
            "Las seis tachuelas se hunden y el cofre se abre. Dentro no hay oro, sino el testamento del capitán Calavera (carta 76), un papel que también se pliega. Detrás del campamento, en la boca de la cueva, el suelo está hecho de losas con símbolos (carta 79).",
            "Coged las cartas 76 y 79. Descartad las cartas 58, 64 y 66."],
        pistas=["Hay un puzle: el suelo de la cueva y el testamento.", "El testamento (carta 76) se pliega como la carta náutica.", "Coged las cartas 76 y 79. Descartad las cartas 58, 64 y 66."],
        arte="Un cofre pirata abierto en la arena, con un pergamino enrollado y atado con un lazo rojo en su interior en lugar de oro; al fondo, la boca de una cueva entre rocas con forma de calavera y un suelo de losas talladas. Cristina sostiene el pergamino con la boca torcida de decepción y Alberto se asoma al cofre vacío con cara de chasco."),
    "76": dict(
        titulo="Carta 76 — Testamento (se pliega)", tipo="gris", plegado=_plegado("76"),
        descripcion=["El testamento del capitán Calavera. Se pliega en acordeón hasta que la línea A toque la B: desplegado, los símbolos del centro son quimeras de dos mitades distintas; plegado, se ven cuatro símbolos de verdad, de arriba abajo. El texto dice que se pisan en ese orden, una y otra vez, de losa en losa vecina. En el Modo PC, botón «Plegar»."],
        pistas=["Los símbolos del centro están rotos: plegad el testamento (líneas A y B).", "Plegado, quedan cuatro símbolos en columna: es el orden de las losas del suelo (carta 79), que se repite en bucle.", f"Plegado, el orden es: {_CICLO}, y vuelta a empezar."],
        arte=pieza("Testamento", "el testamento plegable")),
    "79": dict(
        titulo="Carta 79 — El suelo de la cueva", tipo="verde",
        descripcion=[
            "Es un juego de la app: el suelo de la entrada de la cueva, de cinco por cinco losas con símbolos. Se entra por abajo y hay que llegar a la fila de arriba pisando solo losas vecinas (arriba, abajo o a los lados) cuyos símbolos sigan, una y otra vez, el orden del testamento del capitán Calavera (carta 76) plegado. Una pisada en falso hunde la losa y se vuelve a la entrada.",
            "Al llegar al fondo, la pared se abre. Coged la carta 80."],
        pistas=["El orden está en el testamento (carta 76), pero solo se lee plegado.", "Empezad en una losa de la fila de abajo con el primer símbolo y buscad siempre, al lado, el siguiente; tras el cuarto vuelve el primero. Solo un camino llega arriba.", f"Pisad, desde abajo: {_SUELO}."],
        arte="La entrada de una cueva marina con el suelo de grandes losas de piedra talladas con símbolos, iluminada por la luz del atardecer que entra desde el mar; algunas losas se han hundido en un agujero oscuro. Cristina salta de una losa a otra de puntillas con los brazos abiertos y cara de miedo, y Alberto le señala la siguiente desde atrás, mordiéndose el labio."),
    "80": dict(
        titulo="Carta 80 — La boca de la cueva", tipo="gris", coge=[56], descarta=[72, 76, 79],
        descripcion=[
            "La pared de roca se abre con un ruido de piedra y aparece un pasadizo que baja a la oscuridad. En un nicho de la pared, el capitán Calavera dejó un pedernal y un eslabón para encender fuego (carta 56).",
            "Coged la carta 56. Descartad las cartas 72, 76 y 79."],
        pistas=["Mirad lo que hay en el nicho de la pared.", "La carta 56 es combinable.", "Coged la carta 56. Descartad las cartas 72, 76 y 79."],
        arte="Un pasadizo de piedra que baja a la oscuridad en una cueva marina, con escalones tallados y un nicho en la pared con un pedernal y un eslabón de hierro. Alberto alarga la mano hacia el nicho con los ojos muy abiertos de cautela y Cristina se asoma al pasadizo oscuro con un escalofrío."),
    "56": dict(
        titulo="Carta 56 — Pedernal y eslabón", tipo="roja", combina=[38, 94],
        descripcion=["Un pedernal y un eslabón de hierro para sacar chispas. Combinadlos con la antorcha (carta 38): sumad sus números (56 + 38 = 94) y coged la carta 94."],
        pistas=["Sirven para sacar chispas y encender fuego.", "Combinad la carta 56 con la antorcha (carta 38).", "Sumad los números de las dos cartas: 56 + 38 = 94."],
        arte="Un pedernal gris y un eslabón de hierro curvado sobre una piedra húmeda de una cueva, con unas chispas saltando, visto de cerca en la penumbra."),
    "94": dict(
        titulo="Carta 94 — La antorcha encendida", tipo="gris", coge=[69, 70], descarta=[38, 56, 44, 80],
        descripcion=[
            "La antorcha prende con un chisporroteo y alumbra una gruta enorme con el suelo de arena y el mar entrando por abajo: la marea ya está subiendo. El suelo de arena (carta 69) repite la cuadrícula del mapa de la isla, pero entráis por el este. En la pared, clavado con un puñal, el mapa de la isla del capitán Calavera (carta 70), que se pliega por los dos lados.",
            "Coged las cartas 69 y 70. Descartad las cartas 38, 56, 44 y 80."],
        pistas=["Hay un puzle: cavar en la gruta con el mapa.", "El mapa (carta 70) se pliega por los dos lados: A sobre B y C sobre D.", "Coged las cartas 69 y 70. Descartad las cartas 38, 56, 44 y 80."],
        arte="Una gruta marina enorme iluminada por una antorcha, con el suelo de arena surcado de rayas como una cuadrícula, una palmera tallada en piedra, el agua del mar entrando y subiendo y estalactitas; un mapa viejo clavado a la pared con un puñal. Cristina sostiene la antorcha en alto con cara de asombro y Alberto, con una pala, mira el agua que sube con gesto de preocupación."),
    "70": dict(
        titulo="Carta 70 — Mapa de la isla (se pliega)", tipo="gris", plegado=_plegado("70"),
        descripcion=["El mapa de la Isla Calavera con una cuadrícula y el camino de la palmera a la X. Se pliega por los dos lados (A sobre B y C sobre D): plegado, la roca calavera aparece entera y la cuadrícula tiene las mismas casillas que el suelo de la gruta. En el Modo PC, botón «Plegar»."],
        pistas=["Desplegado, el mapa tiene casillas de más: plegadlo por los dos lados.", "Plegado, contad dónde está la X respecto a la palmera. En la gruta entráis por el este: el norte del mapa queda a vuestra derecha.", f"Plegado, la X está {_X}."],
        arte=pieza("Mapa de la isla", "el mapa plegable")),
    "69": dict(
        titulo="Carta 69 — Cavar en la gruta", tipo="verde",
        descripcion=[
            "Es un juego de la app: el suelo de arena de la gruta, con la misma cuadrícula que el mapa de la isla (carta 70) plegado y una palmera de piedra donde el mapa tiene la palmera. Pero se entra por el este, así que se ve girado: el norte queda a la derecha. Hay que tocar la casilla de la X.",
            "Al acertar, aparece el tesoro. Coged la carta 82."],
        pistas=["La casilla está en el mapa de la isla (carta 70), pero desplegado engaña.", "Plegad el mapa por los dos lados y contad desde la palmera. Después girad el mapa un cuarto de vuelta para que el norte quede a la derecha, como en la gruta.", f"Plegado, la X está {_X}. En la gruta (norte a la derecha): {_XG}."],
        arte="Una gruta marina con el suelo de arena dividido en casillas y una palmera tallada en piedra, iluminada por una antorcha; el agua sube por la entrada. Alberto cava con una pala con todas sus fuerzas y la frente sudada y Cristina, con el mapa girado en las manos, le señala el sitio con cara de urgencia."),
    "82": dict(
        titulo="Carta 82 — El tesoro de Calavera", tipo="gris", coge=[62], descarta=[69, 70, 94],
        descripcion=[
            "La reja se abre: montañas de doblones, joyas y copas brillan a la luz de la antorcha. La capitana Bruma llega justo antes de que el agua cubra la entrada, ríe a carcajadas y cumple su palabra: os devuelve el cristal de energía de su cofre. Doblón, el loro, os lo trae en el pico.",
            "Coged la carta 62. Descartad las cartas 69, 70 y 94."],
        pistas=["La capitana cumple su palabra.", "La carta 62 es combinable con el Cronoportal.", "Coged la carta 62. Descartad las cartas 69, 70 y 94."],
        arte="Una cámara de tesoro en una gruta marina, con montañas de doblones de oro, joyas y copas brillando a la luz de una antorcha y el agua del mar subiendo por la entrada. Una capitana pirata con sombrero de plumas ríe a carcajadas y un loro verde y rojo vuela hacia Cristina con un cristal rojo en el pico; Cristina extiende la mano con los ojos brillantes de emoción y Alberto se lanza sobre las monedas con una carcajada."),
    "62": dict(
        titulo="Carta 62 — Cristal de energía", tipo="roja", combina=[12, 74],
        descripcion=["El cristal de energía del Cronoportal: una gema roja con un fulgor interior. Combinadlo con el Cronoportal (carta 12): sumad sus números (62 + 12 = 74) y coged la carta 74."],
        pistas=["Es la pieza que faltaba.", "Combinad la carta 62 con la carta 12.", "Sumad los números de las dos cartas: 62 + 12 = 74."],
        arte="Un cristal rojo facetado con un fulgor interior de brasa y finas líneas de energía, sobre un montón de doblones de oro, a la luz de una antorcha en una cueva."),
    "74": dict(
        titulo="Carta 74 — Cronoportal reconectado", tipo="gris", coge=[99], descarta=[62, 12, 82],
        descripcion=[
            "El cristal encaja con un chasquido y el Cronoportal se enciende. El agua os llega ya a las rodillas y la capitana Bruma, con los bolsillos llenos, os grita desde la reja: «¡Si alguna vez queréis un barco, La Gaviota es vuestra!». Activad el aparato antes de que la marea cubra la gruta.",
            "Coged la carta 99. Descartad las cartas 62, 12 y 82."],
        pistas=["El portal ya funciona. Solo queda activarlo.", "Coged la carta 99. Descartad las cartas 62, 12 y 82."],
        arte="El Cronoportal encendido con un cristal rojo encajado en su pecho, en una gruta marina que se inunda, con un arco de luz azul y dorada en el anillo y el agua por las rodillas. Cristina, con la cara desencajada de urgencia, tira de Alberto, que carga el aparato con gesto de esfuerzo, mientras una capitana pirata les dice adiós con el sombrero desde el fondo."),
    "99": dict(
        titulo="Carta 99 — De vuelta a casa (FIN)", tipo="gris", descarta=[74],
        descripcion=[
            "El anillo se abre en un arco de luz justo cuando el agua cubre la gruta. Cristina y Alberto salen disparados del Caribe y aterrizan en su salón, empapados y con olor a mar.",
            "Alberto se quita el tricornio: «Mañana, otro destino». Cristina abre la mano: lleva un doblón de oro. Descartad la carta 74.",
            "FIN."],
        pistas=[],
        arte="La escena ocurre DENTRO del salón de su casa actual, en el presente (sofá, estanterías con libros, plantas, una lámpara encendida y luz cálida de tarde por la ventana): acaban de VOLVER a casa. Cristina y Alberto acaban de salir de un portal circular de luz azul y dorada que se abre detrás de ellos; a través del portal todavía se ven una gruta marina con oro y agua que sube. Llevan aún su ropa de pirata, empapados y goteando sobre la alfombra. Cristina ríe a carcajadas enseñando un doblón de oro en la palma de la mano y Alberto, con el tricornio torcido, escurre agua de su casaca con cara de alivio y risa. Están de cara a nosotros, aterrizando en el salón y alejándose del portal, que queda a su espalda y se está cerrando; el mundo de la aventura solo se ve a través del portal, detrás de ellos. No están entrando en el portal ni saliendo de casa: están llegando."),
}

META = dict(
    juego="Mar de las Brumas, 1715 — El Tesoro de la Isla Calavera",
    estilo=ESTILO, personajes=PERSONAJES, hoja=HOJA, foto=FOTO, video=VIDEO,
)

SPEC = dict(
    final="99",
    needs={"26": ["24", "30", "31"], "44": ["46", "40"], "57": ["22", "35"], "58": ["48", "52"], "72": ["66", "64"],
           "80": ["79", "76"], "94": ["38", "56"], "82": ["69", "70"], "74": ["62", "12"]},
    eventos={},
)

PARA_QUE = {
    "P": "Inicio: llegada a bordo. Te manda coger la 10 y la 12.",
    "10": "La cubierta: reparte el timón, la carta náutica, el cuaderno del piloto y la lente.",
    "12": "El Cronoportal sin cristal: se combina con el cristal de energía (62).",
    "22": "Lente de catalejo: se combina con el tubo (35).",
    "24": "El timón (app): rumbo de la carta plegada + desvío de la aguja.",
    "26": "Rumbo a la isla: reparte la bodega, el plano y el tubo del catalejo.",
    "30": "Carta náutica que se pliega: el rumbo verdadero.",
    "31": "Cuaderno del piloto: el desvío de la aguja.",
    "35": "Tubo de catalejo: se combina con la lente (22).",
    "38": "Antorcha apagada: se combina con el pedernal (56).",
    "40": "Plano de estiba: las X de los barriles.",
    "44": "La bodega estibada: reparte la antorcha.",
    "46": "La bodega (app): empujar los barriles a las X.",
    "48": "La persecución (app): llegar a la niebla sin que la fragata os alcance.",
    "52": "Ordenanza de la Armada: cómo se mueve la fragata.",
    "56": "Pedernal y eslabón: se combina con la antorcha (38).",
    "57": "El catalejo (22 + 35): reparte la persecución y la ordenanza.",
    "58": "Desembarco: reparte la tapa del cofre y la carta celeste.",
    "62": "Cristal de energía: se combina con el Cronoportal (12).",
    "64": "Carta celeste: la constelación de la Calavera.",
    "66": "La tapa del cofre (app): las seis tachuelas de la Calavera girada.",
    "69": "Cavar en la gruta (app): la X del mapa plegado, con el suelo girado.",
    "70": "Mapa de la isla que se pliega por los dos lados: dónde está la X.",
    "72": "El cofre de Calavera: reparte el testamento y el suelo de la cueva.",
    "74": "Cronoportal reconectado (62 + 12): reparte la 99.",
    "76": "Testamento que se pliega: el ciclo de símbolos del suelo.",
    "79": "El suelo de la cueva (app): cruzar por losas vecinas siguiendo el ciclo.",
    "80": "La boca de la cueva: reparte el pedernal.",
    "82": "El tesoro: reparte el cristal de energía.",
    "94": "La antorcha encendida (38 + 56): reparte la gruta y el mapa.",
    "99": "Final de la aventura, ya en casa.",
}

# ---------------------------------------------------------------- manual (los estados de la mesa se calculan simulando las cartas)
_TEXTOS = [
    ("leer", "P", "Llegada a bordo", "Pon el Modo PC en el ordenador (solo debe haber la carta P en la mesa y el resto boca abajo en el mazo) y en el móvil abre el juego y pulsa Empezar. Lee la carta P: te manda coger la 10 y la 12."),
    ("leer", "10", "La cubierta de La Gaviota", "Lee la carta 10. Descarta la P y coge 22, 24, 30 y 31. La carta náutica (30) se pliega: en papel, en acordeón hasta que A toque B; en el Modo PC, botón «Plegar»."),
    ("app", "24", "El timón", f"En el móvil: Acción, 24. Plegada, la carta 30 dice {RUMBO['carta']}; el cuaderno del piloto (31) dibuja un desvío de {RUMBO['desvio']} grados. Fija el timón en {RUMBO['aguja']}. El mensaje te dice que cojas la 26.", "carta 26"),
    ("leer", "26", "Rumbo a la Isla Calavera", "Lee la carta 26. Descarta 10, 24, 30 y 31 y coge 35, 40 y 46. Las cartas 22 y 35 son combinables."),
    ("app", "46", "La bodega", "En el móvil: Acción, 46. Marca con tiza las X del plano de estiba (carta 40) y empuja los tres barriles hasta ellas (hay botones para deshacer y empezar de nuevo). El mensaje te dice que cojas la 44.", "carta 44"),
    ("leer", "44", "La bodega estibada", "Lee la carta 44. Descarta 26, 40 y 46 y coge la 38, una antorcha apagada."),
    ("combinar", "22", "35", "El catalejo", "La lente (22) y el tubo (35) son combinables: 22 + 35 = 57. Coge la 57."),
    ("leer", "57", "El catalejo", "Lee la carta 57. Descarta 22 y 35 y coge 48 y 52. El código de señales está en la 52."),
    ("app", "48", "La persecución", f"En el móvil: Acción, 48. La fragata se mueve según la ordenanza (carta 52). Una solución: {_PERSIGUE}. El mensaje te dice que cojas la 58.", "carta 58"),
    ("leer", "58", "Desembarco en la Isla Calavera", "Lee la carta 58. Descarta 48, 52 y 57 y coge 64 y 66."),
    ("app", "66", "La tapa del cofre", "En el móvil: Acción, 66. Busca en la tapa la Calavera de la carta celeste (64), girada un tercio de vuelta, arriba a la derecha del centro; toca sus seis tachuelas y abre. El mensaje te dice que cojas la 72.", "carta 72"),
    ("leer", "72", "El cofre del capitán Calavera", "Lee la carta 72. Descarta 58, 64 y 66 y coge 76 y 79. El testamento (76) también se pliega."),
    ("app", "79", "El suelo de la cueva", f"En el móvil: Acción, 79. Plegado, el testamento enseña, de arriba abajo: {_CICLO}. Cruza el suelo de losa vecina en losa vecina siguiendo ese ciclo: {_SUELO}. El mensaje te dice que cojas la 80.", "carta 80"),
    ("leer", "80", "La boca de la cueva", "Lee la carta 80. Descarta 72, 76 y 79 y coge la 56, el pedernal y el eslabón."),
    ("combinar", "38", "56", "La antorcha encendida", "La antorcha (38) y el pedernal (56) son combinables: 38 + 56 = 94. Coge la 94."),
    ("leer", "94", "La antorcha encendida", "Lee la carta 94. Descarta 38, 56, 44 y 80 y coge 69 y 70. El mapa (70) se pliega por los dos lados."),
    ("app", "69", "Cavar en la gruta", f"En el móvil: Acción, 69. Plegado el mapa (A sobre B y C sobre D), la X está {_X}. En la gruta, con el norte a la derecha: {_XG}. El mensaje te dice que cojas la 82.", "carta 82"),
    ("leer", "82", "El tesoro de Calavera", "Lee la carta 82. Descarta 69, 70 y 94 y coge la 62, el cristal de energía."),
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


# ================================================================== ampliación a 36 cartas (20 oct 2026)
# Entre la persecución y el desembarco: la marea entre los arrecifes. El diario de la capitana dice cuándo pasar en campanadas de una
# guardia; dos cartas explican las guardias y las campanadas, y la app es el reloj de bitácora. Láminas: dibujos_ampliacion.py.
import json as _json  # noqa: E402
import os as _os  # noqa: E402
import ampliacion as _amp  # noqa: E402

_AMP = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "instancias_ampliacion.json"), encoding="utf-8"))
_HORA = "{:02d}:{:02d}".format(*_AMP["piratas_campanas"]["hora"])


def _pieza2(que):
    return f"Carta dibujada por código (herramientas/dibujos_ampliacion.py; no se pide a ChatGPT): {que}."


J["48"]["descripcion"][1] = J["48"]["descripcion"][1].replace("Coged la carta 58", "Coged la carta 59")
J.update({
    "59": dict(
        titulo="Carta 59 — Al pairo frente a la isla", tipo="gris", coge=[61, 63, 65, 67],
        descripcion=[
            "La Gaviota sale de la niebla frente a la Isla Calavera, pero un cinturón de arrecifes rodea la playa. La capitana Bruma busca en su diario (carta 67): solo se puede pasar con la marea justa, y ella lo apuntó a la manera de los marinos, en campanadas. Hay que poner en hora el reloj de bitácora (carta 61) con el cuadro de guardias (carta 63) y el de campanadas (carta 65).",
            "Coged las cartas 61, 63, 65 y 67."],
        pistas=["Hay un puzle: el reloj de bitácora, el diario y dos cuadros.", "El diario (67) dice la guardia y las campanadas; las cartas 63 y 65 explican cómo se cuentan.", "Coged las cartas 61, 63, 65 y 67."],
        arte="Un barco pirata al pairo al atardecer frente a una isla con palmeras rodeada de arrecifes con espuma, con una campana de bronce colgada junto al timón. Cristina mira las rocas por encima de la borda con cara de preocupación y Alberto sostiene un diario abierto, rascándose la cabeza confundido."),
    "61": dict(
        titulo="Carta 61 — El reloj de bitácora", tipo="verde",
        descripcion=[
            "Es un juego de la app: el reloj de bitácora de La Gaviota, que se adelanta o se atrasa de media en media hora. Hay que ponerlo a la hora que apuntó la capitana en su diario (carta 67), convirtiendo la guardia y las campanadas con los cuadros de las cartas 63 y 65.",
            "Al acertar, la marea abre el paso entre los arrecifes. Coged la carta 58."],
        pistas=["Hacen falta el diario (67), las guardias (63) y las campanadas (65).", "La guardia de la tarde empieza a las 12; cada campanada es media hora desde que empezó la guardia.", f"Poned el reloj a las {_HORA}."],
        arte="Un reloj de bitácora de latón con esfera de veinticuatro horas, montado junto a la rueda del timón de un barco pirata, con la luz dorada del atardecer. Alberto gira la corona del reloj con cuidado, sacando la lengua, y Cristina cuenta campanadas con los dedos, muy seria."),
    "63": dict(titulo="Carta 63 — Las guardias", tipo="gris",
               descripcion=["El cuadro de las seis guardias de a bordo: cómo se reparte el día en turnos de cuatro horas y a qué hora empieza cada uno."],
               pistas=["Sirve para el reloj de bitácora (carta 61).", "Buscad la guardia que dice el diario (carta 67) y mirad a qué hora empieza.", f"La hora es las {_HORA}."],
               arte=_pieza2("el cuadro de las guardias")),
    "65": dict(titulo="Carta 65 — Las campanadas", tipo="gris",
               descripcion=["El cuadro de las campanadas: cada media hora de guardia suena una campanada más, de una a ocho."],
               pistas=["Sirve para el reloj de bitácora (carta 61).", "Contad las campanas del diario (carta 67): cada una es media hora desde el principio de la guardia.", f"La hora es las {_HORA}."],
               arte=_pieza2("el cuadro de las campanadas")),
    "67": dict(titulo="Carta 67 — Diario de la capitana", tipo="gris",
               descripcion=["Una página del diario de la capitana Bruma: el paso entre los arrecifes se abre en la guardia de la tarde, con las campanadas dibujadas."],
               pistas=["Sirve para el reloj de bitácora (carta 61).", "El sol dice la guardia; las campanas, cuántas medias horas han pasado desde que empezó.", f"La hora es las {_HORA}."],
               arte=_pieza2("la página del diario")),
})
J["58"]["descarta"] = [48, 52, 57, 59, 61, 63, 65, 67]
J["58"]["descripcion"][0] = J["58"]["descripcion"][0].replace("La fragata se pierde en la niebla y La Gaviota fondea", "La marea abre el paso y La Gaviota fondea")
J["58"]["descripcion"][1] = "Coged las cartas 64 y 66. Descartad las cartas 48, 52, 57, 59, 61, 63, 65 y 67."
J["58"]["pistas"][2] = "Coged las cartas 64 y 66. Descartad las cartas 48, 52, 57, 59, 61, 63, 65 y 67."

SPEC["needs"]["59"] = SPEC["needs"].pop("58")
SPEC["needs"]["58"] = ["61", "63", "65", "67"]
PARA_QUE.update({
    "59": "Al pairo frente a la isla: reparte el reloj, los cuadros y el diario.", "61": "El reloj de bitácora (app): la hora de la marea.",
    "63": "Cuadro de las guardias.", "65": "Cuadro de las campanadas.", "67": "Diario de la capitana: guardia y campanadas.",
    "58": "Desembarco: aparece al pasar los arrecifes.",
})

_i = next(i for i, p in enumerate(PASOS) if p["acciones"][0][:2] == ("app", "48"))
PASOS[_i]["que"] = PASOS[_i]["que"].replace("cojas la 58", "cojas la 59")
PASOS[_i]["acciones"] = [("app", "48", "carta 59")]
PASOS[_i + 1:_i + 1] = [
    dict(t="Al pairo frente a la isla", que="Lee la carta 59. Coge 61, 63, 65 y 67.", acciones=[("leer", "59")]),
    dict(t="El reloj de bitácora", que=f"En el móvil: Acción, 61. La guardia de la tarde empieza a las 12 y cada campanada es media hora: pon el reloj a las {_HORA}. El mensaje te dice que cojas la 58.",
         acciones=[("app", "61", "carta 58")]),
]
_j = next(i for i, p in enumerate(PASOS) if p["acciones"][0][:2] == ("leer", "58"))
PASOS[_j]["que"] = PASOS[_j]["que"].replace("Descarta 48, 52 y 57", "Descarta 48, 52, 57, 59, 61, 63, 65 y 67")
_amp.recalcular_mesas(PASOS, J)
