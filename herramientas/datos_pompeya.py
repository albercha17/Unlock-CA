"""Pompeya, 79 d.C.: El Mosaico del Mundo. Primer juego con PUZLES VISUALES EN LAS CARTAS: varias cartas se juntan para formar un mosaico romano
(2x2 o apiladas) y del dibujo entero sale el código. Los mosaicos los dibuja herramientas/mosaicos.py (códigos exactos en codigos_pompeya.json)."""

ESTILO = ("Ilustración pictórica semirrealista con aire de película histórica, luz cálida y dorada de primera hora de la mañana en Pompeya, "
          "arquitectura romana (columnas, mosaicos, frescos rojos y ocres, patios con impluvio), paleta de terracotas, ocres, azules marinos y blancos de mármol, "
          "con una columna de humo gris del Vesubio al fondo, formato vertical 2:3. Sin texto, letras ni números en la imagen; los rollos, tablillas y frescos son solo dibujos "
          "decorativos sin escritura legible. Deja libre de detalles importantes la esquina superior izquierda y el 18 % inferior de la imagen. "
          "Los personajes tienen siempre expresiones distintas y expresivas, adecuadas a la escena (nunca la misma cara en dos imágenes).")

PERSONAJES = {
    "Cristina": "Cristina, mujer de 26 años, profesora, pelo rubio y rizado recogido con una cinta, ojos azules. Viste ropa romana de época: una stola larga de lino verde oliva con un manto (palla) azul sobre los hombros, sandalias de cuero y un brazalete de bronce.",
    "Alberto": "Alberto, hombre de 27 años, informático, pelo moreno corto, barba cuidada, ojos marrones. Viste ropa romana de época: una túnica corta color arena con cinturón de cuero, una capa corta sobre un hombro, sandalias de correas y una bolsa de cuero.",
}

HOJA = ("Crea una hoja de personajes (character sheet) con las dos personas de la foto adjunta, de cuerpo entero y de frente, sobre fondo claro y neutro. "
        "Mantén su parecido real con la foto (cara, pelo, barba, ojos). "
        "Cristina: mujer de 26 años, profesora, pelo rubio y rizado recogido con una cinta, ojos azules, stola larga de lino verde oliva con manto azul, sandalias de cuero y brazalete de bronce. "
        "Alberto: hombre de 27 años, informático, pelo moreno corto, barba cuidada, ojos marrones, túnica corta color arena con cinturón de cuero, capa corta, sandalias de correas y bolsa de cuero. "
        "Estilo: " + ESTILO)

FOTO = ("Antes de nada, adjunta a ChatGPT una foto de Cristina y Alberto juntos (o una de cada uno, con la cara bien visible). "
        "Pídele que mantenga el parecido real, pero con el estilo de ilustración de este juego.")

VIDEO = ("Crea un vídeo vertical 9:16 de 15 segundos, con estilo cinematográfico semirrealista de película histórica, luz dorada de amanecer y tonos terracota y azul marino. Sin ningún texto, letra ni subtítulo en pantalla. "
         "Escena 1 (0-4 s): en el salón de una casa actual, Cristina (mujer de 26 años, rubia de pelo rizado, ojos azules) y Alberto (hombre de 27 años, moreno con barba, ojos marrones) rodean un aparato de latón y cristal con un anillo central: el Cronoportal. Cristina señala una foto de las ruinas de Pompeya en un libro. "
         "Escena 2 (4-8 s): el anillo se enciende con un arco de luz azul y dorada y los dos son absorbidos por un túnel de luz. "
         "Escena 3 (8-12 s): caen sobre el suelo de mosaico de un atrio romano al amanecer, entre columnas; al fondo, sobre la ciudad, el Vesubio lanza una columna de humo. El aparato humea y un cristal rojo sale rodando. "
         "Escena 4 (12-15 s): primer plano de Cristina y Alberto, con ropa romana, asombrados, mirando al volcán; la ceniza empieza a caer; fundido a negro. "
         "Sonido: zumbido eléctrico creciente, silbido del portal, golpe sordo al aterrizar, retumbar lejano del volcán, lira y flauta con percusión suave, sin voz de narrador.")


def pieza(mosaico, nombre_pieza):
    return f"Pieza del mosaico (se dibuja por código con herramientas/mosaicos.py; no se pide a ChatGPT): {nombre_pieza} del mosaico «{mosaico}»."


# ---------------------------------------------------------------- mosaicos: id -> (filas, columnas, [ids de las piezas en orden de lectura: izquierda→derecha, arriba→abajo])
MOSAICOS = {
    "atrio": dict(filas=2, cols=2, cartas=["16", "14", "17", "15"], titulo="Mosaico del atrio"),
    "peristilo": dict(filas=2, cols=2, cartas=["32", "30", "33", "31"], titulo="Fresco del peristilo"),
    "rosetas": dict(filas=2, cols=2, cartas=["42", "40", "43", "41"], titulo="Suelo del triclinio"),
    "digitos": dict(filas=2, cols=1, cartas=["53", "52"], titulo="Fresco del cubiculum"),
    "reloj": dict(filas=2, cols=2, cartas=["65", "67", "64", "66"], titulo="Mosaico del hipocausto"),
}
POS4 = ["arriba a la izquierda", "arriba a la derecha", "abajo a la izquierda", "abajo a la derecha"]


def _ficha_pieza(carta, nombre):
    for k, m in MOSAICOS.items():
        if carta in m["cartas"]:
            i = m["cartas"].index(carta)
            filas, cols = m["filas"], m["cols"]
            return dict(id=k, filas=filas, cols=cols, fila=i // cols, col=i % cols)
    raise KeyError(carta)


def _pieza_carta(carta, mosaico, que_es, pistas_extra):
    m = MOSAICOS[mosaico]
    i = m["cartas"].index(carta)
    pos = POS4[i] if m["filas"] * m["cols"] == 4 else ("arriba" if i == 0 else "abajo")
    mapa = (f"Arriba, de izquierda a derecha: {m['cartas'][0]} y {m['cartas'][1]}. Abajo: {m['cartas'][2]} y {m['cartas'][3]}." if m["filas"] * m["cols"] == 4
            else f"Arriba, la {m['cartas'][0]}; abajo, la {m['cartas'][1]}.")
    juntas = ", ".join(m["cartas"][:-1]) + " y " + m["cartas"][-1]
    return dict(
        titulo=f"Carta {carta} — Placa del mosaico ({pos})" if m["filas"] * m["cols"] == 4 else f"Carta {carta} — Mitad del fresco ({pos})",
        tipo="gris", mosaico=_ficha_pieza(carta, mosaico),
        descripcion=[f"{que_es} Es una pieza suelta: juntad las cartas {juntas} para ver el dibujo entero."],
        pistas=pistas_extra + [mapa],
        arte=pieza(m["titulo"], pos))


J = {
    "P": dict(
        titulo="Carta P — Llegada a Pompeya", tipo="gris", coge=[10, 12],
        descripcion=[
            "Séptima parada del Cronoportal: Pompeya, 24 de agosto del año 79 d.C. Aterrizáis al amanecer en el atrio de una rica villa, entre columnas, con un estanque de lluvia en el centro y el suelo cubierto de mosaicos. Al fondo, sobre la ciudad, el Vesubio lanza al cielo una columna de humo.",
            "El aterrizaje sale mal otra vez: el aparato golpea el borde del estanque y su cristal de energía sale volando y desaparece por la casa. Sin él, el Cronoportal está muerto. Tenéis hora y media antes de que la ceniza lo cubra todo.",
            "Coged las cartas 10 y 12."],
        pistas=["Mirad a vuestro alrededor y revisad el aparato.", "Coged las cartas 10 y 12."],
        arte="El atrio de una villa romana de Pompeya al amanecer: columnas, un estanque de lluvia (impluvio) y un suelo de mosaico, y al fondo, sobre los tejados, la columna de humo del Vesubio. En primer plano, un aparato de latón y cristal retrofuturista (el Cronoportal) humea sobre el suelo con una luz azul que se apaga. Cristina, con los ojos muy abiertos y la boca entreabierta de asombro, y Alberto, con una ceja arqueada y gesto de incredulidad, se levantan aturdidos con ropa romana."),
    "10": dict(
        titulo="Carta 10 — El atrio de la villa", tipo="gris", coge=[14, 15, 16, 17, 18, 20, 22], descarta=["P"],
        descripcion=[
            "El atrio de la villa de Lucrecia, comerciante de aceite y de vino. El mosaico del suelo se ha roto con el golpe en cuatro placas sueltas (cartas 14, 15, 16 y 17): hay que juntarlas para ver el dibujo entero. A su lado, una nota del mosaiquista Lucio (carta 18), la puerta cerrada del tablinum con un panel de formas (carta 20) y, brillando en el fondo del estanque, la mitad de una llave de bronce (carta 22).",
            "Coged las cartas 14, 15, 16, 17, 18, 20 y 22. Descartad la carta P."],
        pistas=["Hay un puzle: el mosaico del suelo y la puerta del tablinum.", "Las cuatro placas (14 a 17) se juntan formando un solo dibujo.", "Coged las cartas 14, 15, 16, 17, 18, 20 y 22. Descartad la carta P."],
        arte="Un suelo de mosaico romano roto en cuatro grandes placas sueltas sobre las losas de un atrio, junto a un estanque de lluvia; al fondo, una puerta de madera cerrada con un panel de bronce y, en el agua, el brillo de una llave de bronce partida. Cristina se agacha con el ceño fruncido de concentración y Alberto levanta una de las placas con gesto de esfuerzo."),
    "12": dict(
        titulo="Carta 12 — Cronoportal sin cristal", tipo="azul", combina=[62, 74],
        descripcion=[
            "El Cronoportal: una consola de latón y cristal con un anillo central apagado y un hueco vacío en el pecho, donde iba el cristal de energía. Alberto: «Sin el cristal no hay portal. Tiene que haber rodado por aquí cerca».",
            "Cuando recuperéis el cristal (carta 62), combinadlo con el Cronoportal: sumad sus números (12 + 62 = 74) y coged la carta 74."],
        pistas=["Le falta una pieza: el cristal de energía.", "Combinad la carta 12 con la carta 62.", "Sumad los números de las dos cartas: 12 + 62 = 74."],
        arte="Primer plano del Cronoportal: una consola portátil de latón y cristal con dos antenas de cobre, un anillo de cristal central apagado y un hueco circular vacío en el pecho del aparato, sobre las losas de un atrio romano, con una columna y un fresco rojo borroso al fondo."),
    "18": dict(
        titulo="Carta 18 — Nota del mosaiquista", tipo="gris",
        descripcion=["Una tablilla de cera con una nota de Lucio, el mosaiquista que hizo el suelo. Sirve para leer el mosaico del atrio y abrir la puerta del tablinum (carta 20)."],
        pistas=["Es una nota sobre cómo leer el mosaico.", "Sirve para la puerta del tablinum (carta 20)."],
        textoCarta=["Seguid el camino de piedras blancas", "desde la estrella de oro.", "Solo cuentan las figuras que toca el camino."],
        arte="Una tablilla de cera con marco de madera y un estilete apoyados sobre las losas de un atrio romano, junto a unas teselas sueltas de colores y una pequeña paleta; la superficie de cera tiene solo rayas decorativas, sin escritura legible."),
    "20": dict(
        titulo="Carta 20 — La puerta del tablinum", tipo="verde",
        descripcion=[
            "Es un juego de la app: la puerta del despacho de Lucrecia tiene un panel con seis figuras y cuatro huecos. Hay que poner las figuras en el orden que dice el mosaico del atrio (juntad las placas 14, 15, 16 y 17) siguiendo la nota de Lucio (carta 18).",
            "Al acertar, la puerta se abre. Coged la carta 26."],
        pistas=["Juntad las cuatro placas del mosaico y seguid el camino desde la estrella de oro.", "Anotad, por orden, la figura de cada medallón por el que pasa el camino. Los medallones fuera del camino no cuentan.", "Triángulo, estrella, círculo y cruz."],
        arte="Una puerta de madera de roble con herrajes de bronce y, en el centro, un panel de bronce con seis figuras geométricas en relieve (círculo, triángulo, cuadrado, rombo, estrella y cruz) y cuatro huecos; a un lado, una lámpara de aceite encendida. Cristina examina el panel con la lengua entre los dientes, concentrada, y Alberto sostiene la lámpara con una sonrisa de expectación."),
    "22": dict(
        titulo="Carta 22 — Mitad de llave", tipo="azul", combina=[35, 57],
        descripcion=["La mitad de una llave de bronce, con un ojo y la mitad del paletón. Combinadla con la otra mitad (carta 35): sumad sus números (22 + 35 = 57) y coged la carta 57."],
        pistas=["Es solo la mitad de una llave.", "Cuando encontréis la otra mitad, combinadlas.", "Sumad los números de las dos cartas: 22 + 35 = 57."],
        arte="Una mitad de llave romana de bronce, con un ojo redondo y la mitad de un paletón dentado, sobre una tela de lino, junto al agua de un estanque de lluvia; la luz de la mañana la hace brillar."),
    "24": dict(
        titulo="Carta 24 — La verja del peristilo", tipo="verde",
        descripcion=[
            "Es un juego de la app: una verja de hierro que cierra el jardín con cuatro botones de flecha (arriba, abajo, izquierda y derecha). El orden lo dan las estatuas del fresco del jardín (juntad las placas 30, 31, 32 y 33) y la nota de la carta 36.",
            "Al acertar, la verja se abre. Coged la carta 28."],
        pistas=["Juntad las cuatro placas del fresco: es el jardín visto desde arriba.", "Cada estatua señala una dirección con su flecha. Empezad por la de la antorcha y seguid el sentido de las agujas del reloj.", "Abajo, abajo, derecha y arriba."],
        arte="Una verja de hierro forjado con cuatro grandes botones de bronce con forma de flecha en un pilar de piedra, cerrando la entrada de un jardín con columnas; entre las rejas se ve una fuente. Alberto empuja la verja con los dos brazos y cara de esfuerzo y Cristina señala los botones con los ojos muy abiertos de emoción."),
    "26": dict(
        titulo="Carta 26 — El tablinum", tipo="gris", coge=[24, 30, 31, 32, 33, 36], descarta=[14, 15, 16, 17, 18, 20],
        descripcion=[
            "La puerta cede y entráis en el tablinum, el despacho de Lucrecia, lleno de rollos y tablillas. En la pared del fondo, un fresco del jardín se ha desprendido en cuatro placas de yeso (cartas 30, 31, 32 y 33). Una nota de Lucrecia (carta 36) y una verja de hierro con flechas (carta 24) cierran el paso al peristilo.",
            "Coged las cartas 24, 30, 31, 32, 33 y 36. Descartad las cartas 14, 15, 16, 17, 18 y 20."],
        pistas=["Hay un puzle: el fresco del jardín y la verja.", "Coged las cartas 24, 30, 31, 32, 33 y 36. Descartad las cartas 14, 15, 16, 17, 18 y 20."],
        arte="El despacho de una rica romana: una mesa con rollos de papiro, tablillas de cera, una estantería con cajas de bronce y, en la pared del fondo, un fresco rojo y verde de un jardín roto en cuatro placas de yeso caídas en el suelo. Cristina mira el fresco con la boca abierta de admiración y Alberto, a su lado, se rasca la barba con gesto de duda."),
    "28": dict(
        titulo="Carta 28 — El peristilo", tipo="gris", coge=[35, 40, 41, 42, 43, 45, 46], descarta=[26, 30, 31, 32, 33, 24, 36],
        descripcion=[
            "La verja se abre y salís al peristilo, el jardín de columnas con una fuente en el centro. Junto a la fuente brilla la otra mitad de la llave de bronce (carta 35). Al fondo, el triclinio, el comedor de la villa, cuyo suelo muestra tres rosetas rotas en cuatro placas (cartas 40, 41, 42 y 43); sobre la mesa hay una nota del jardinero (carta 45) y en la puerta, un candado de rosetas (carta 46).",
            "Coged las cartas 35, 40, 41, 42, 43, 45 y 46. Descartad las cartas 26, 30, 31, 32, 33, 24 y 36."],
        pistas=["Hay dos cosas: la otra mitad de la llave y el comedor con su candado.", "Las cartas 22 y 35 son combinables. Las placas 40 a 43 forman el suelo del comedor.", "Coged las cartas 35, 40, 41, 42, 43, 45 y 46. Descartad las cartas 26, 30, 31, 32, 33, 24 y 36."],
        arte="Un peristilo romano, un jardín rodeado de columnas con una fuente de mármol en el centro, setos recortados y estatuas; al fondo, la puerta de un comedor con un candado de bronce con forma de flor. Cristina corre hacia la fuente con una sonrisa de alegría y Alberto la sigue con gesto de alivio, secándose la frente."),
    "30": _pieza_carta("30", "peristilo", "Una placa del fresco del jardín del tablinum.", ["Las cuatro placas encajan formando un solo dibujo.", "Es una cuadrícula de dos por dos: los bordes del dibujo continúan de una placa a otra."]),
    "31": _pieza_carta("31", "peristilo", "Una placa del fresco del jardín del tablinum.", ["Las cuatro placas encajan formando un solo dibujo.", "Es una cuadrícula de dos por dos: los bordes del dibujo continúan de una placa a otra."]),
    "32": _pieza_carta("32", "peristilo", "Una placa del fresco del jardín del tablinum.", ["Las cuatro placas encajan formando un solo dibujo.", "Es una cuadrícula de dos por dos: los bordes del dibujo continúan de una placa a otra."]),
    "33": _pieza_carta("33", "peristilo", "Una placa del fresco del jardín del tablinum.", ["Las cuatro placas encajan formando un solo dibujo.", "Es una cuadrícula de dos por dos: los bordes del dibujo continúan de una placa a otra."]),
    "14": _pieza_carta("14", "atrio", "Una placa del mosaico del atrio.", ["Las cuatro placas encajan formando un solo dibujo.", "Es una cuadrícula de dos por dos: los bordes del dibujo continúan de una placa a otra."]),
    "15": _pieza_carta("15", "atrio", "Una placa del mosaico del atrio.", ["Las cuatro placas encajan formando un solo dibujo.", "Es una cuadrícula de dos por dos: los bordes del dibujo continúan de una placa a otra."]),
    "16": _pieza_carta("16", "atrio", "Una placa del mosaico del atrio.", ["Las cuatro placas encajan formando un solo dibujo.", "Es una cuadrícula de dos por dos: los bordes del dibujo continúan de una placa a otra."]),
    "17": _pieza_carta("17", "atrio", "Una placa del mosaico del atrio.", ["Las cuatro placas encajan formando un solo dibujo.", "Es una cuadrícula de dos por dos: los bordes del dibujo continúan de una placa a otra."]),
    "35": dict(
        titulo="Carta 35 — Otra mitad de llave", tipo="roja", combina=[22, 57],
        descripcion=["La otra mitad de la llave de bronce, con el resto del paletón. Combinadla con la primera mitad (carta 22): sumad sus números (35 + 22 = 57) y coged la carta 57."],
        pistas=["Es la otra mitad de la llave.", "Combinad la carta 35 con la carta 22.", "Sumad los números de las dos cartas: 35 + 22 = 57."],
        arte="La otra mitad de una llave romana de bronce, con el resto del paletón dentado, sobre el borde de mármol de una fuente de jardín, con gotas de agua y la luz del sol sobre el metal."),
    "36": dict(
        titulo="Carta 36 — Nota de Lucrecia", tipo="gris",
        descripcion=["Una nota de Lucrecia clavada en la verja del peristilo. Sirve para leer el fresco del jardín y abrir la verja (carta 24)."],
        pistas=["Es una nota sobre las estatuas del jardín.", "Sirve para la verja del peristilo (carta 24)."],
        textoCarta=["Las estatuas del jardín indican el camino.", "Empezad por la que lleva la antorcha", "y seguid el sentido de las agujas del reloj."],
        arte="Una hoja de papiro sujeta con un clavo a un pilar de piedra junto a una verja, con el borde quemado y manchas de aceite; al lado, una pequeña lámpara de arcilla. El papiro solo muestra rayas decorativas, sin escritura legible."),
    "40": _pieza_carta("40", "rosetas", "Una placa del suelo del triclinio, el comedor de la villa.", ["Las cuatro placas encajan formando un solo dibujo.", "Es una cuadrícula de dos por dos: los bordes del dibujo continúan de una placa a otra."]),
    "41": _pieza_carta("41", "rosetas", "Una placa del suelo del triclinio, el comedor de la villa.", ["Las cuatro placas encajan formando un solo dibujo.", "Es una cuadrícula de dos por dos: los bordes del dibujo continúan de una placa a otra."]),
    "42": _pieza_carta("42", "rosetas", "Una placa del suelo del triclinio, el comedor de la villa.", ["Las cuatro placas encajan formando un solo dibujo.", "Es una cuadrícula de dos por dos: los bordes del dibujo continúan de una placa a otra."]),
    "43": _pieza_carta("43", "rosetas", "Una placa del suelo del triclinio, el comedor de la villa.", ["Las cuatro placas encajan formando un solo dibujo.", "Es una cuadrícula de dos por dos: los bordes del dibujo continúan de una placa a otra."]),
    "45": dict(
        titulo="Carta 45 — Nota del jardinero", tipo="gris",
        descripcion=["Una nota del jardinero sobre las rosetas del comedor. Sirve para el candado de rosetas (carta 46)."],
        pistas=["Es una nota sobre cómo leer las rosetas.", "Sirve para el candado de rosetas (carta 46)."],
        textoCarta=["Contad los pétalos de cada roseta,", "de arriba abajo", "y de izquierda a derecha."],
        arte="Una tablilla de madera con un puñado de pétalos de colores y una podadera de jardinero sobre una mesa de mármol del comedor de una villa romana, junto a una copa de vino; la tablilla solo muestra rayas decorativas, sin escritura legible."),
    "46": dict(
        titulo="Carta 46 — El candado de rosetas", tipo="verde",
        descripcion=[
            "Es un juego de la app: un candado de bronce con tres ruedas que van del 1 al 9. Hay que poner en cada rueda el número de pétalos de cada roseta del suelo del comedor (juntad las placas 40, 41, 42 y 43), en el orden que dice la nota del jardinero (carta 45).",
            "Al acertar, el candado se abre. Coged la carta 44."],
        pistas=["Juntad las cuatro placas del suelo: son tres rosetas.", "Contad los pétalos de cada roseta, de arriba abajo y de izquierda a derecha, y poned cada número en su rueda.", "Cinco, tres y siete."],
        arte="Un candado de bronce con forma de flor y tres ruedas numeradas (sin cifras legibles, solo muescas) en una puerta de madera de un comedor romano, con una lámpara de aceite al lado. Alberto gira una rueda con la lengua entre los dientes, concentrado, y Cristina cuenta con los dedos con cara de ilusión."),
    "44": dict(
        titulo="Carta 44 — El triclinio", tipo="gris", coge=[38], descarta=[28, 40, 41, 42, 43, 45, 46],
        descripcion=[
            "El candado cede y entráis en el triclinio, el comedor, donde aún están puestas las copas y las lámparas de una cena que no se acabó. Entre las copas, Alberto encuentra un pedernal con el que hacer fuego (carta 38).",
            "Coged la carta 38. Descartad las cartas 28, 40, 41, 42, 43, 45 y 46."],
        pistas=["Mirad lo que quedó en la mesa de la cena.", "La carta 38 es combinable.", "Coged la carta 38. Descartad las cartas 28, 40, 41, 42, 43, 45 y 46."],
        arte="El triclinio de una villa romana: tres lechos para comer alrededor de una mesa baja con copas de vino, fruta y lámparas de aceite apagadas, y las paredes con frescos rojos. Alberto levanta un pedernal entre las copas con una sonrisa de triunfo y Cristina lo mira con los ojos brillantes de entusiasmo."),
    "38": dict(
        titulo="Carta 38 — Pedernal", tipo="azul", combina=[56, 94],
        descripcion=["Un pedernal y un trozo de yesca para hacer fuego. Combinadlo con la lámpara de aceite (carta 56): sumad sus números (38 + 56 = 94) y coged la carta 94."],
        pistas=["Sirve para hacer fuego.", "Cuando tengáis la lámpara de aceite, combinadla con el pedernal.", "Sumad los números de las dos cartas: 38 + 56 = 94."],
        arte="Un pedernal gris y un trozo de yesca seca sobre una servilleta de lino, junto a una copa de vino, en una mesa del comedor de una villa romana; la luz de una ventana cae sobre ellos."),
    "57": dict(
        titulo="Carta 57 — El cubiculum", tipo="gris", coge=[48, 52, 53], descarta=[22, 35, 10],
        descripcion=[
            "Las dos mitades de la llave encajan y giran: la llave de bronce abre el cubiculum, el dormitorio de Lucrecia. A los pies de la cama hay un cofre con un ábaco (carta 48) y, en la pared, un fresco partido en dos mitades, la de arriba y la de abajo (cartas 52 y 53).",
            "Coged las cartas 48, 52 y 53. Descartad las cartas 22, 35 y 10."],
        pistas=["Hay un puzle: el fresco partido y el cofre con ábaco.", "Las dos mitades del fresco (52 y 53) se juntan una encima de la otra.", "Coged las cartas 48, 52 y 53. Descartad las cartas 22, 35 y 10."],
        arte="Un dormitorio romano con una cama de madera, un cofre de bronce a sus pies con un ábaco de varillas sobre la tapa, y en la pared un fresco azul partido en dos mitades. Cristina gira la llave de bronce en la cerradura con una sonrisa de orgullo y Alberto observa por encima de su hombro con cara de impaciencia."),
    "52": _pieza_carta("52", "digitos", "Una mitad de un fresco con un número.", ["Las dos mitades se juntan una encima de la otra.", "Las dos mitades no se pueden leer por separado: el número solo se ve con las dos juntas."]),
    "53": _pieza_carta("53", "digitos", "Una mitad de un fresco con un número.", ["Las dos mitades se juntan una encima de la otra.", "Las dos mitades no se pueden leer por separado: el número solo se ve con las dos juntas."]),
    "48": dict(
        titulo="Carta 48 — El cofre del ábaco", tipo="verde",
        descripcion=[
            "Es un juego de la app: un cofre cerrado con un ábaco de tres varillas, unidades, decenas y centenas, con nueve cuentas cada una. Hay que dejar en el ábaco el número que muestra el fresco partido del cubiculum (juntad las cartas 52 y 53).",
            "Al acertar, el cofre se abre. Coged la carta 58."],
        pistas=["Juntad las dos mitades del fresco: se lee un número de tres cifras.", "Cada varilla es una cifra: centenas, decenas y unidades. Subid tantas cuentas como diga la cifra.", "El número es cuatrocientos setenta y dos."],
        arte="Un cofre de bronce con un ábaco romano de tres varillas con cuentas de piedra sobre su tapa, en un dormitorio con una lámpara de aceite encendida. Alberto cuenta las cuentas con el dedo, con la boca fruncida de concentración, y Cristina sostiene la lámpara con los ojos muy abiertos de expectación."),
    "58": dict(
        titulo="Carta 58 — El cofre abierto", tipo="gris", coge=[56], descarta=[48, 52, 53, 57],
        descripcion=[
            "El cofre se abre con un chasquido. Dentro, sobre un paño, hay una lámpara de aceite de bronce, perfecta para bajar a oscuras.",
            "Coged la carta 56. Descartad las cartas 48, 52, 53 y 57."],
        pistas=["Mirad lo que había en el cofre.", "La carta 56 es combinable.", "Coged la carta 56. Descartad las cartas 48, 52, 53 y 57."],
        arte="Un cofre de bronce abierto con una lámpara de aceite de bronce sobre un paño rojo, en un dormitorio romano de piedra; Cristina sostiene la tapa con una sonrisa radiante de alegría y Alberto se asoma con cara de alivio."),
    "56": dict(
        titulo="Carta 56 — Lámpara de aceite", tipo="roja", combina=[38, 94],
        descripcion=["Una lámpara de aceite de bronce, con aceite pero sin llama. Combinadla con el pedernal (carta 38): sumad sus números (56 + 38 = 94) y coged la carta 94."],
        pistas=["Es una lámpara: necesita fuego.", "Cuando tengáis el pedernal, combinadlo con la lámpara.", "Sumad los números de las dos cartas: 56 + 38 = 94."],
        arte="Una lámpara de aceite romana de bronce con un asa y un pico largo, con aceite pero sin llama, sobre un paño rojo, vista de cerca, con una luz cálida lateral."),
    "94": dict(
        titulo="Carta 94 — El hipocausto", tipo="gris", coge=[64, 65, 66, 67, 69, 70], descarta=[56, 38, 44, 58],
        descripcion=[
            "Con la lámpara encendida, bajáis por una escalera al hipocausto, el sótano de columnillas por donde circulaba el aire caliente. El suelo de la sala principal es un mosaico enorme, roto en cuatro placas (cartas 64, 65, 66 y 67), con un reloj de sol en el centro. Junto a él, una nota (carta 70) y una rueda de bronce que mueve la sombra del reloj (carta 69).",
            "Coged las cartas 64, 65, 66, 67, 69 y 70. Descartad las cartas 56, 38, 44 y 58."],
        pistas=["Hay un puzle: el mosaico del reloj y la rueda de bronce.", "Las cuatro placas (64 a 67) forman un reloj de sol.", "Coged las cartas 64, 65, 66, 67, 69 y 70. Descartad las cartas 56, 38, 44 y 58."],
        arte="Un sótano romano de columnillas de ladrillo (hipocausto) iluminado por la llama de una lámpara de aceite; en el suelo, un enorme mosaico roto en cuatro placas con un círculo central, y una rueda de bronce en la pared. Cristina avanza con la lámpara en alto, con cara de miedo contenido, y Alberto la sigue con los ojos muy abiertos y la boca entreabierta de asombro."),
    "64": _pieza_carta("64", "reloj", "Una placa del mosaico del hipocausto.", ["Las cuatro placas encajan formando un solo dibujo.", "Es una cuadrícula de dos por dos: los bordes del dibujo continúan de una placa a otra."]),
    "65": _pieza_carta("65", "reloj", "Una placa del mosaico del hipocausto.", ["Las cuatro placas encajan formando un solo dibujo.", "Es una cuadrícula de dos por dos: los bordes del dibujo continúan de una placa a otra."]),
    "66": _pieza_carta("66", "reloj", "Una placa del mosaico del hipocausto.", ["Las cuatro placas encajan formando un solo dibujo.", "Es una cuadrícula de dos por dos: los bordes del dibujo continúan de una placa a otra."]),
    "67": _pieza_carta("67", "reloj", "Una placa del mosaico del hipocausto.", ["Las cuatro placas encajan formando un solo dibujo.", "Es una cuadrícula de dos por dos: los bordes del dibujo continúan de una placa a otra."]),
    "70": dict(
        titulo="Carta 70 — Nota del relojero", tipo="gris",
        descripcion=["Una nota del relojero que trazó el reloj de sol. Sirve para leer el mosaico del hipocausto y mover la rueda (carta 69)."],
        pistas=["Es una nota sobre cómo leer el reloj.", "Sirve para la rueda del reloj de sol (carta 69)."],
        textoCarta=["La estrella marca el comienzo de las horas.", "Contad las marcas en el sentido de las agujas", "del reloj hasta donde llega la sombra."],
        arte="Una tablilla de cera con un gnomon de bronce dibujado y un compás de bronce apoyados en una piedra del suelo de un sótano romano, iluminados por la luz de una lámpara; la tablilla solo muestra rayas decorativas, sin escritura legible."),
    "69": dict(
        titulo="Carta 69 — La rueda del reloj de sol", tipo="verde",
        descripcion=[
            "Es un juego de la app: una rueda de bronce con doce marcas que gira un puntero. Hay que girarlo hasta la marca a la que llega la sombra del reloj de sol del mosaico (juntad las placas 64, 65, 66 y 67), contando desde la estrella como dice la nota del relojero (carta 70).",
            "Al acertar, el mosaico se ilumina y se abre la sala del altar. Coged la carta 82."],
        pistas=["Juntad las cuatro placas del mosaico: es un reloj de sol con su sombra.", "Contad las marcas en el sentido de las agujas del reloj desde la estrella (la estrella no cuenta) hasta donde llega la sombra.", "La sombra llega a la séptima marca."],
        arte="Una gran rueda de bronce con doce muescas y un puntero giratorio en una pared de ladrillo de un sótano romano, junto a una lámpara de aceite encendida. Cristina gira la rueda con las dos manos, con los ojos entrecerrados de esfuerzo, y Alberto sostiene la lámpara con una ceja arqueada de duda."),
    "82": dict(
        titulo="Carta 82 — El lararium", tipo="gris", coge=[62], descarta=[64, 65, 66, 67, 69, 70, 94],
        descripcion=[
            "El mosaico se ilumina, la pared se abre y entráis en el lararium, el pequeño altar de los dioses de la casa. En el nicho, entre pequeñas estatuas de bronce, brilla un cristal rojo: el cristal de energía.",
            "Coged la carta 62. Descartad las cartas 64, 65, 66, 67, 69, 70 y 94."],
        pistas=["Mirad dentro del nicho del altar.", "La carta 62 es combinable con el Cronoportal.", "Coged la carta 62. Descartad las cartas 64, 65, 66, 67, 69, 70 y 94."],
        arte="Un pequeño altar doméstico romano (lararium) en un nicho de pared pintado de rojo, con estatuillas de bronce y un cristal rojo brillante en el centro. Cristina lo toma con ambas manos con los ojos llenos de lágrimas de emoción y Alberto la mira con una sonrisa enorme."),
    "62": dict(
        titulo="Carta 62 — Cristal de energía", tipo="roja", combina=[12, 74],
        descripcion=["El cristal de energía del Cronoportal: una gema roja con un fulgor interior. Combinadlo con el Cronoportal (carta 12): sumad sus números (62 + 12 = 74) y coged la carta 74."],
        pistas=["Es la pieza que faltaba.", "Combinad la carta 62 con la carta 12.", "Sumad los números de las dos cartas: 62 + 12 = 74."],
        arte="Un cristal rojo facetado con un fulgor interior de brasa y finas líneas de energía, sostenido sobre la palma de una mano, sobre un fondo de ladrillo romano con luz cálida."),
    "74": dict(
        titulo="Carta 74 — Cronoportal reconectado", tipo="gris", coge=[99], descarta=[62, 12, 82],
        descripcion=[
            "El cristal encaja con un chasquido y el Cronoportal se enciende, pero fuera ya cae la ceniza y el suelo tiembla. No hay tiempo que perder: sacad el aparato al atrio y activadlo.",
            "Coged la carta 99. Descartad las cartas 62, 12 y 82."],
        pistas=["El portal ya funciona. Solo queda activarlo.", "Coged la carta 99. Descartad las cartas 62, 12 y 82."],
        arte="El Cronoportal encendido con un cristal rojo encajado en su pecho, en un atrio romano cubierto de ceniza gris que cae del cielo, con un arco de luz azul y dorada en el anillo. Cristina, con la cara desencajada de urgencia, tira de Alberto, que carga el aparato con gesto de esfuerzo."),
    "99": dict(
        titulo="Carta 99 — De vuelta a casa (FIN)", tipo="gris", descarta=[74],
        descripcion=[
            "El anillo se abre en un arco de luz justo cuando la primera lluvia de ceniza cubre el atrio. Cristina se despide con la mano de la casa y de su mosaico, que quedará sepultado casi dos mil años.",
            "Aterrizan en su salón. Alberto mira el aparato: «Mañana, otro destino». Cristina sonríe y guarda en el bolsillo una pequeña tesela de oro. Descartad la carta 74.",
            "FIN."],
        pistas=[],
        arte="La escena ocurre DENTRO del salón de su casa actual, en el presente (sofá, estanterías con libros, plantas, una lámpara encendida y luz cálida de tarde por la ventana): acaban de VOLVER a casa. Cristina y Alberto acaban de salir de un portal circular de luz azul y dorada que se abre detrás de ellos; a través del portal todavía se ven un atrio romano cubierto de ceniza y el Vesubio con su columna de humo. Llevan aún su ropa romana manchada de ceniza. Cristina ríe a carcajadas con una tesela de oro en la mano y Alberto grita de euforia con los brazos en alto. Están de cara a nosotros, aterrizando en el salón y alejándose del portal, que queda a su espalda y se está cerrando; el mundo de la aventura solo se ve a través del portal, detrás de ellos. No están entrando en el portal ni saliendo de casa: están llegando."),
}

META = dict(
    juego="Pompeya, 79 d.C. — El Mosaico del Mundo",
    estilo=ESTILO, personajes=PERSONAJES, hoja=HOJA, foto=FOTO, video=VIDEO,
    mosaicos={k: dict(filas=m["filas"], cols=m["cols"], cartas=m["cartas"], titulo=m["titulo"]) for k, m in MOSAICOS.items()},
)

SPEC = dict(
    final="99",
    needs={"26": ["14", "15", "16", "17", "18", "20"], "28": ["30", "31", "32", "33", "24", "36"], "44": ["40", "41", "42", "43", "45", "46"],
           "57": ["22", "35"], "58": ["48", "52", "53"], "94": ["56", "38"], "82": ["64", "65", "66", "67", "69", "70"], "74": ["62", "12"]},
    eventos={},
)

PARA_QUE = {
    "P": "Inicio: llegada al atrio. Te manda coger la 10 y la 12.",
    "10": "El atrio: reparte las placas del mosaico, la nota, la puerta y la mitad de la llave.",
    "12": "El Cronoportal sin cristal: se combina con el cristal de energía (62).",
    "14": "Placa del mosaico del atrio: se junta con la 15, 16 y 17.", "15": "Placa del mosaico del atrio: se junta con la 14, 16 y 17.",
    "16": "Placa del mosaico del atrio: se junta con la 14, 15 y 17.", "17": "Placa del mosaico del atrio: se junta con la 14, 15 y 16.",
    "18": "Nota de Lucio: cómo leer el mosaico del atrio.",
    "20": "La puerta del tablinum (app): poner cuatro figuras en el orden del camino del mosaico.",
    "22": "Mitad de llave: se combina con la otra mitad (35).",
    "24": "La verja del peristilo (app): cuatro flechas en el orden de las estatuas.",
    "26": "El tablinum: reparte las placas del fresco, la nota y la verja; te manda descartar el atrio.",
    "28": "El peristilo: reparte la otra mitad de la llave y el comedor.",
    "30": "Placa del fresco del jardín.", "31": "Placa del fresco del jardín.", "32": "Placa del fresco del jardín.", "33": "Placa del fresco del jardín.",
    "35": "Otra mitad de llave: se combina con la 22.",
    "36": "Nota de Lucrecia: cómo leer el fresco de las estatuas.",
    "40": "Placa del suelo del triclinio.", "41": "Placa del suelo del triclinio.", "42": "Placa del suelo del triclinio.", "43": "Placa del suelo del triclinio.",
    "45": "Nota del jardinero: cómo contar los pétalos.",
    "46": "El candado de rosetas (app): tres ruedas con el número de pétalos.",
    "44": "El triclinio: reparte el pedernal.",
    "38": "Pedernal: se combina con la lámpara (56).",
    "57": "El cubiculum: resultado de 22 + 35; reparte el fresco partido y el ábaco.",
    "52": "Mitad del fresco con un número.", "53": "Mitad del fresco con un número.",
    "48": "El cofre del ábaco (app): dejar en el ábaco el número del fresco.",
    "58": "El cofre abierto: reparte la lámpara.",
    "56": "Lámpara de aceite: se combina con el pedernal (38).",
    "94": "El hipocausto: resultado de 56 + 38; reparte el mosaico del reloj, la nota y la rueda.",
    "64": "Placa del mosaico del reloj de sol.", "65": "Placa del mosaico del reloj de sol.", "66": "Placa del mosaico del reloj de sol.", "67": "Placa del mosaico del reloj de sol.",
    "70": "Nota del relojero: cómo leer la sombra del reloj.",
    "69": "La rueda del reloj de sol (app): girar el puntero a la marca de la sombra.",
    "82": "El lararium: reparte el cristal de energía.",
    "62": "Cristal de energía: se combina con el Cronoportal (12).",
    "74": "Cronoportal reconectado: resultado de 62 + 12; reparte la 99.",
    "99": "Final de la aventura.",
}

# ---------------------------------------------------------------- manual (los estados de la mesa se calculan simulando las cartas)
_TEXTOS = [
    ("leer", "P", "Llegada a Pompeya", "Pon el Modo PC en el ordenador (solo debe haber la carta P en la mesa y el resto boca abajo en el mazo) y en el móvil abre el juego y pulsa Empezar. Lee la carta P: te manda coger la 10 y la 12."),
    ("leer", "10", "El atrio de la villa", "Lee la carta 10. Descarta la P y coge 14, 15, 16, 17, 18, 20 y 22. Junta las cuatro placas (14 a 17) para ver el mosaico entero (en el Modo PC, botón «Mesa de montaje»: toca dos piezas para cambiarlas de sitio) y sigue el camino desde la estrella de oro (nota 18)."),
    ("app", "20", "La puerta del tablinum", "En el móvil: Acción, 20. Las figuras del camino, por orden, son triángulo, estrella, círculo y cruz. El mensaje te dice que cojas la 26.", "carta 26"),
    ("leer", "26", "El tablinum", "Lee la carta 26. Descarta 14, 15, 16, 17, 18 y 20 y coge 24, 30, 31, 32, 33 y 36. Junta las cuatro placas del fresco (30 a 33): son las estatuas del jardín."),
    ("app", "24", "La verja del peristilo", "En el móvil: Acción, 24. Desde la estatua de la antorcha, en el sentido de las agujas del reloj: abajo, abajo, derecha y arriba. El mensaje te dice que cojas la 28.", "carta 28"),
    ("leer", "28", "El peristilo", "Lee la carta 28. Descarta 26, 30, 31, 32, 33, 24 y 36 y coge 35, 40, 41, 42, 43, 45 y 46. Las cartas 22 y 35 son combinables."),
    ("combinar", "22", "35", "La llave de bronce", "Las dos mitades de la llave (22 y 35) son combinables: 22 + 35 = 57. Coge la 57."),
    ("leer", "57", "El cubiculum", "Lee la carta 57. Descarta 22, 35 y 10 y coge 48, 52 y 53. Junta las dos mitades del fresco (52 y 53): se lee un número de tres cifras."),
    ("app", "48", "El cofre del ábaco", "En el móvil: Acción, 48. Deja en el ábaco el número del fresco: 4 en las centenas, 7 en las decenas y 2 en las unidades. El mensaje te dice que cojas la 58.", "carta 58"),
    ("leer", "58", "El cofre abierto", "Lee la carta 58. Descarta 48, 52, 53 y 57 y coge la 56, una lámpara de aceite."),
    ("app", "46", "El candado de rosetas", "En el móvil: Acción, 46. Junta las placas 40 a 43 (tres rosetas) y, con la nota 45, pon en las ruedas los pétalos de cada roseta: 5, 3 y 7. El mensaje te dice que cojas la 44.", "carta 44"),
    ("leer", "44", "El triclinio", "Lee la carta 44. Descarta 28, 40, 41, 42, 43, 45 y 46 y coge la 38, un pedernal."),
    ("combinar", "56", "38", "Lámpara con pedernal", "La lámpara (56) y el pedernal (38) son combinables: 56 + 38 = 94. Coge la 94."),
    ("leer", "94", "El hipocausto", "Lee la carta 94. Descarta 56, 38, 44 y 58 y coge 64, 65, 66, 67, 69 y 70. Junta las cuatro placas (64 a 67): es un reloj de sol con su sombra."),
    ("app", "69", "La rueda del reloj de sol", "En el móvil: Acción, 69. Con la nota 70, cuenta desde la estrella en el sentido de las agujas del reloj hasta donde llega la sombra: la séptima marca. El mensaje te dice que cojas la 82.", "carta 82"),
    ("leer", "82", "El lararium", "Lee la carta 82. Descarta 64, 65, 66, 67, 69, 70 y 94 y coge la 62, el cristal de energía."),
    ("combinar", "12", "62", "Cristal en el Cronoportal", "El Cronoportal (12) y el cristal (62) son combinables: 12 + 62 = 74. Coge la 74."),
    ("leer", "74", "Cronoportal reconectado", "Lee la carta 74. Descarta 62, 12 y 82 y coge la 99."),
    ("leer", "99", "Final", "Lee la carta 99. Descarta la 74. En la mesa solo queda la 99. ¡Fin!"),
]


def _pasos():
    mesa = set()
    pasos = []
    for p in _TEXTOS:
        if p[0] == "leer":
            c = J[p[1]]
            mesa |= {"P"} if p[1] == "P" and not mesa else set()
            for d in c.get("descarta", []):
                mesa.discard(str(d))
            for h in c.get("coge", []):
                mesa.add(str(h))
            if p[1] == "P":
                mesa = {"P", "10", "12"}
            pasos.append(dict(t=p[2], que=p[3], acciones=[("leer", p[1])], mesa=_orden(mesa)))
        elif p[0] == "app":
            res = p[4].split()[-1]
            mesa.add(res)
            pasos.append(dict(t=p[2], que=p[3], acciones=[("app", p[1], p[4])], mesa=_orden(mesa)))
        else:
            mesa.add(str(int(p[1]) + int(p[2])))
            pasos.append(dict(t=p[3], que=p[4], acciones=[("combinar", p[1], p[2])], mesa=_orden(mesa)))
    return pasos


def _orden(m):
    return sorted(m, key=lambda x: (x != "P", int(x) if x != "P" else 0))


PASOS = _pasos()
