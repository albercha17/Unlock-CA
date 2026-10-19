"""Montecarlo, 1965: Operación Cristal. Décima parada del Cronoportal: una película de espías. Los puzles reparten la información entre cartas de formas nuevas:
dos cartas que se SUPERPONEN a contraluz (dos hojas de ruido que revelan un número; una carta negra con ventanas, la rejilla de Cardano, sobre una carta de letras),
un plano con el laberinto cuyas paredes son invisibles en la app, las pistas de un rascacielos 4x4 repartidas en dos cartas y un manual de cables con reglas.
Las cartas que se dibujan por código (14, 15, 30, 31, 40, 52, 53 y 70) las hace herramientas/espia.py (códigos exactos en codigos_espia.json e instancias_espia.json)."""
import json
import os

_AQUI = os.path.dirname(os.path.abspath(__file__))
INST = json.load(open(os.path.join(_AQUI, "instancias_espia.json"), encoding="utf-8"))
COD = json.load(open(os.path.join(_AQUI, "codigos_espia.json"), encoding="utf-8"))

ESTILO = ("Ilustración pictórica semirrealista con aire de película de espías de los años 60 (como James Bond y La Pantera Rosa), paleta pop mediterránea de turquesa, rosa, dorado y blanco, "
          "luz de noche de gala con las luces del puerto de Montecarlo, casino, yates, hotel y terrazas con farolillos, formato vertical 2:3. Sin texto, letras ni números legibles en la imagen; "
          "los papeles, carteles y pantallas solo muestran rayas decorativas. Deja libre de detalles importantes la esquina superior izquierda y el 18 % inferior de la imagen. "
          "Los personajes tienen siempre expresiones distintas y expresivas, adecuadas a la escena (nunca la misma cara en dos imágenes).")

PERSONAJES = {
    "Cristina": "Cristina, mujer de 26 años, profesora, pelo rubio y rizado recogido en un moño alto con una diadema, ojos azules. Viste ropa de espía elegante de los años 60: un vestido corto rosa empolvado con cinturón blanco, guantes cortos blancos, grandes gafas de sol redondas subidas al pelo y zapatos de tacón bajo.",
    "Alberto": "Alberto, hombre de 27 años, informático, pelo moreno engominado, barba cuidada, ojos marrones. Viste ropa de espía elegante de los años 60: un esmoquin negro entallado con pajarita, camisa blanca, un reloj de pulsera grande y un pequeño maletín plateado.",
}

HOJA = ("Crea una hoja de personajes (character sheet) con las dos personas de la foto adjunta, de cuerpo entero y de frente, sobre fondo claro y neutro. "
        "Mantén su parecido real con la foto (cara, pelo, barba, ojos). "
        "Cristina: mujer de 26 años, profesora, pelo rubio y rizado recogido en un moño alto con una diadema, ojos azules, vestido corto rosa empolvado con cinturón blanco, guantes cortos blancos, grandes gafas de sol redondas subidas al pelo y zapatos de tacón bajo. "
        "Alberto: hombre de 27 años, informático, pelo moreno engominado, barba cuidada, ojos marrones, esmoquin negro entallado con pajarita, camisa blanca, reloj de pulsera grande y un pequeño maletín plateado. "
        "Estilo: " + ESTILO)

FOTO = ("Antes de nada, adjunta a ChatGPT una foto de Cristina y Alberto juntos (o una de cada uno, con la cara bien visible). "
        "Pídele que mantenga el parecido real, pero con el estilo de ilustración de este juego.")

VIDEO = ("Crea un vídeo vertical 9:16 de 15 segundos, con estilo cinematográfico de película de espías de los años 60, colores pop de turquesa, rosa y dorado, y mucho contraste. Sin ningún texto, letra ni subtítulo en pantalla. "
         "Escena 1 (0-4 s): en el salón de una casa actual, Cristina (mujer de 26 años, rubia de pelo rizado, ojos azules) y Alberto (hombre de 27 años, moreno con barba, ojos marrones) rodean un aparato de latón y cristal con un anillo central: el Cronoportal. Cristina señala una foto antigua del casino de Montecarlo en un libro. "
         "Escena 2 (4-8 s): el anillo se enciende con un arco de luz azul y dorada y los dos son absorbidos por un túnel de luz. "
         "Escena 3 (8-12 s): caen en la terraza de un casino junto al puerto de Montecarlo, de noche, entre farolillos y yates; el aparato golpea una mesa y su cristal sale rodando, y una mano con guante negro lo recoge. "
         "Escena 4 (12-15 s): primer plano de Cristina y Alberto, con ropa de espías elegantes, asombrados, mirando cómo un yate negro se aleja del puerto; fundido a negro. "
         "Sonido: zumbido eléctrico creciente, silbido del portal, golpe sordo al aterrizar, música de big band con vibráfono y bajo de espías, sin voz de narrador.")


def pieza(titulo, donde):
    return f"Carta dibujada por código (herramientas/espia.py; no se pide a ChatGPT): {donde} de «{titulo}»."


def _camino_texto():
    """El camino del laberinto como «derecha 2, abajo 3, ...» (tramos seguidos en la misma dirección)."""
    ruta = INST["laberinto"]["ruta"]
    pasos = []
    for (f0, c0), (f1, c1) in zip(ruta, ruta[1:]):
        pasos.append("abajo" if f1 > f0 else "arriba" if f1 < f0 else "derecha" if c1 > c0 else "izquierda")
    tramos = []
    for p in pasos:
        if tramos and tramos[-1][0] == p:
            tramos[-1][1] += 1
        else:
            tramos.append([p, 1])
    return ", ".join(f"{p} {n}" for p, n in tramos)


def _skyline_texto():
    return " / ".join(" ".join(str(x) for x in fila) for fila in INST["rascacielos"]["solucion"])


def _cortes_texto():
    return ", ".join(f"carga {i + 1}: el cable {c + 1}" for i, c in enumerate(INST["cables"]["cortes"]))


DIG = "".join(str(d) for d in COD["cripto"]["digitos"])
PAL = COD["rejilla"]["palabra"]

# id del mosaico -> cartas (la de abajo y la de encima), título y cuánto está desplazada al empezar la carta de encima (en mm: derecha y abajo son positivos)
MOSAICOS = {
    "cripto": dict(cartas=["15", "14"], titulo="Las dos hojas transparentes", desfase=[5, -4]),
    "rejilla": dict(cartas=["31", "30"], titulo="La rejilla de cifrado", desfase=[-4, 6]),
}


def _ficha(k):
    return dict(id=k, filas=1, cols=1, fila=0, col=0, capas=True)


J = {
    "P": dict(
        titulo="Carta P — Llegada a Montecarlo", tipo="gris", coge=[10, 12],
        descripcion=[
            "Décima parada del Cronoportal: Montecarlo, 1965, noche de gala. Aterrizáis en la terraza del casino, entre farolillos y copas de champán, y el aparato golpea una mesa. Su cristal de energía sale rodando y una mano con guante negro lo recoge al vuelo: es el Dr. Noche, un villano con capa que colecciona gemas, que susurra «perfecta para mi colección» y desaparece hacia su yate, el Neptuno.",
            "Una mujer con gafas de sol se os acerca: es la Agente Zorro, de una agencia secreta. «Llevamos meses detrás de él. Ayudadnos y recuperaréis vuestra gema, pero el yate zarpa a medianoche: tenéis setenta y cinco minutos». Os da un sobre.",
            "Coged las cartas 10 y 12."],
        pistas=["Mirad a vuestro alrededor y revisad el aparato.", "Coged las cartas 10 y 12."],
        arte="La terraza de un casino de Montecarlo en 1965 de noche, con farolillos, copas de champán y yates en el puerto al fondo; un yate negro se aleja. En primer plano, el Cronoportal, un aparato de latón y cristal, humea contra una mesa con la luz azul apagándose. Cristina, con la boca abierta y los ojos muy abiertos de asombro, y Alberto, con una ceja arqueada y la pajarita torcida de incredulidad, se levantan aturdidos con ropa de espías elegantes."),
    "10": dict(
        titulo="Carta 10 — El sobre de la Agente Zorro", tipo="gris", coge=[14, 15, 20, 22], descarta=["P"],
        descripcion=[
            "En el sobre hay dos hojas transparentes llenas de puntitos (cartas 14 y 15), una nota que dice «sola, cada una es solo ruido» y la llave de una caja de seguridad de la suite del hotel (carta 20), que guarda los papeles de la agencia. Entre los papeles, Alberto encuentra además la mitad de un microfilm (carta 22).",
            "Coged las cartas 14, 15, 20 y 22. Descartad la carta P."],
        pistas=["Hay un puzle: las dos hojas y la caja de seguridad.", "Las dos hojas (14 y 15) se ponen una encima de la otra.", "Coged las cartas 14, 15, 20 y 22. Descartad la carta P."],
        arte="Una suite de hotel de lujo de los años 60 con un sobre abierto sobre una mesa de cristal: dos hojas transparentes con puntitos y una caja de seguridad empotrada en la pared detrás de un cuadro. Cristina sostiene una de las hojas a contraluz de una lámpara con los ojos entrecerrados de concentración y Alberto examina la caja de seguridad con el ceño fruncido."),
    "12": dict(
        titulo="Carta 12 — Cronoportal sin cristal", tipo="azul", combina=[62, 74],
        descripcion=[
            "El Cronoportal: una consola de latón y cristal con un anillo central apagado y un hueco vacío en el pecho, donde iba el cristal de energía. Alberto: «Sin el cristal no hay portal. Se lo ha llevado el Dr. Noche... y no sabe lo que tiene en las manos».",
            "Cuando recuperéis el cristal (carta 62), combinadlo con el Cronoportal: sumad sus números (12 + 62 = 74) y coged la carta 74."],
        pistas=["Le falta una pieza: el cristal de energía.", "Combinad la carta 12 con la carta 62.", "Sumad los números de las dos cartas: 12 + 62 = 74."],
        arte="Primer plano del Cronoportal: una consola portátil de latón y cristal con dos antenas de cobre, un anillo de cristal central apagado y un hueco circular vacío en el pecho del aparato, sobre un mantel blanco de una mesa de terraza, con farolillos desenfocados al fondo."),
    "14": dict(
        titulo="Carta 14 — Hoja transparente A", tipo="gris", mosaico=_ficha("cripto"),
        descripcion=["Una hoja llena de puntitos negros: sola parece solo ruido. Es una pieza suelta: poned la hoja 14 y la hoja 15 una encima de la otra, con los marcos bien alineados (a contraluz en papel o con «Superponer» en el Modo PC) para ver el dibujo."],
        pistas=["Las dos hojas parecen ruido por separado.", "Ponedlas una encima de la otra, con los marcos bien alineados, y miradlas a contraluz o con el Modo PC («Superponer»).", "Se ve un número de tres cifras, en negro sobre el ruido."],
        arte=pieza("Las dos hojas transparentes", "una de las dos hojas")),
    "15": dict(
        titulo="Carta 15 — Hoja transparente B", tipo="gris", mosaico=_ficha("cripto"),
        descripcion=["Una hoja llena de puntitos negros: sola parece solo ruido. Es una pieza suelta: poned la hoja 15 y la hoja 14 una encima de la otra, con los marcos bien alineados (a contraluz en papel o con «Superponer» en el Modo PC) para ver el dibujo."],
        pistas=["Las dos hojas parecen ruido por separado.", "Ponedlas una encima de la otra, con los marcos bien alineados, y miradlas a contraluz o con el Modo PC («Superponer»).", "Se ve un número de tres cifras, en negro sobre el ruido."],
        arte=pieza("Las dos hojas transparentes", "la otra hoja")),
    "20": dict(
        titulo="Carta 20 — La caja de seguridad", tipo="verde",
        descripcion=[
            "Es un juego de la app: una caja de seguridad con un teclado de tres cifras. El número es el que aparece al superponer las dos hojas transparentes (cartas 14 y 15).",
            "Al acertar, la caja se abre. Coged la carta 26."],
        pistas=["Superponed las dos hojas transparentes con los marcos bien alineados.", "Dentro del marco se lee un número de tres cifras, en negro sobre el ruido.", f"El número es {DIG}."],
        arte="Una caja de seguridad de acero empotrada en la pared de una suite de hotel de lujo, con un teclado numérico de teclas grandes y una luz roja, bajo un cuadro apartado. Alberto teclea con el dedo en el aire y los ojos entrecerrados, concentrado, y Cristina vigila la puerta con los brazos cruzados y una ceja arqueada de duda."),
    "22": dict(
        titulo="Carta 22 — Mitad de microfilm", tipo="azul", combina=[35, 57],
        descripcion=["La mitad de un microfilm: una tira de película diminuta cortada por la mitad. Combinadla con la otra mitad (carta 35): sumad sus números (22 + 35 = 57) y coged la carta 57."],
        pistas=["Es solo la mitad de un microfilm.", "Cuando encontréis la otra mitad, combinadlas.", "Sumad los números de las dos cartas: 22 + 35 = 57."],
        arte="Una tira de microfilm diminuta cortada por la mitad, con fotogramas minúsculos, sobre un papel secante verde, vista de cerca con la luz cálida de una lámpara de escritorio."),
    "26": dict(
        titulo="Carta 26 — El despacho de cifrado", tipo="gris", coge=[24, 30, 31], descarta=[14, 15, 20],
        descripcion=[
            "La caja se abre y dentro hay una carta negra con unas ventanas recortadas (carta 30) y una carta llena de letras (carta 31): una rejilla de cifrado, como las que usaban los espías hace siglos. Una nota de la Agente Zorro dice que el Dr. Noche cifra sus mensajes con ella. A su lado, un teletipo (carta 24) espera la palabra.",
            "Coged las cartas 24, 30 y 31. Descartad las cartas 14, 15 y 20."],
        pistas=["Hay un puzle: la rejilla y el teletipo.", "La carta negra (30) se pone encima de la de letras (31).", "Coged las cartas 24, 30 y 31. Descartad las cartas 14, 15 y 20."],
        arte="Un despacho de cifrado de los años 60 con un teletipo de latón, mapas en la pared y una mesa con dos tarjetas grandes sobre un tablero: una negra con ventanas y otra con una cuadrícula de letras. Cristina coloca una tarjeta encima de la otra con cuidado y gesto de concentración, y Alberto mira por encima de su hombro con la boca entreabierta de asombro."),
    "24": dict(
        titulo="Carta 24 — El teletipo", tipo="verde",
        descripcion=[
            "Es un juego de la app: un teletipo con teclado de máquina de escribir. Hay que escribir la palabra que se lee por las ventanas de la carta negra (30) puesta sobre la carta de letras (31), de arriba abajo.",
            "Al acertar, el mensaje sale impreso. Coged la carta 28."],
        pistas=["Poned la carta negra con ventanas (30) encima de la de letras (31), con los marcos alineados.", "Leed las letras que se ven por las ventanas, de arriba abajo.", f"La palabra es {PAL}."],
        arte="Un teletipo de los años 60 con una cinta de papel que sale despacio y un teclado de máquina de escribir, sobre una mesa de despacho de espías. Alberto escribe con dos dedos y la lengua entre los dientes, y Cristina lee la cinta de papel con los ojos muy abiertos de expectación."),
    "30": dict(
        titulo="Carta 30 — La rejilla (carta negra con ventanas)", tipo="gris", mosaico=_ficha("rejilla"),
        descripcion=["Una carta negra con siete ventanas recortadas. Es una pieza suelta: ponedla encima de la carta de letras (31), con los marcos bien alineados (a contraluz en papel o con «Superponer» en el Modo PC)."],
        pistas=["Es una rejilla: solo deja ver lo que hay debajo de sus ventanas.", "Ponedla encima de la carta de letras (31), con los marcos bien alineados, y miradla a contraluz o con el Modo PC («Superponer»).", "Las letras que se ven por las ventanas, leídas de arriba abajo, forman una palabra."],
        arte=pieza("La rejilla de cifrado", "la carta negra con ventanas")),
    "31": dict(
        titulo="Carta 31 — Letras", tipo="gris", mosaico=_ficha("rejilla"),
        descripcion=["Una cuadrícula de letras sin sentido. Es una pieza suelta: poned encima la carta negra con ventanas (30), con los marcos bien alineados (a contraluz en papel o con «Superponer» en el Modo PC)."],
        pistas=["Por sí sola es solo una sopa de letras sin sentido.", "Poned encima la carta negra con ventanas (30), con los marcos bien alineados, y miradlas a contraluz o con el Modo PC («Superponer»).", "Las letras que se ven por las ventanas, leídas de arriba abajo, forman una palabra."],
        arte=pieza("La rejilla de cifrado", "la carta de letras")),
    "28": dict(
        titulo="Carta 28 — El yate Neptuno", tipo="gris", coge=[35, 40, 46], descarta=[26, 30, 31, 24],
        descripcion=[
            "El teletipo imprime: «NEPTUNO», el nombre del yate del Dr. Noche, y la contraseña de su pasarela. Subís al yate a escondidas. En un camarote encontráis la otra mitad del microfilm (carta 35) y el plano del barco (carta 40), pero los pasillos están oscuros y vigilados: solo se puede avanzar a ciegas con el mando de la linterna (carta 46).",
            "Coged las cartas 35, 40 y 46. Descartad las cartas 26, 30, 31 y 24."],
        pistas=["Hay dos cosas: la otra mitad del microfilm y el plano con el mando.", "Las cartas 22 y 35 son combinables. El plano (40) sirve para el mando (46).", "Coged las cartas 35, 40 y 46. Descartad las cartas 26, 30, 31 y 24."],
        arte="La cubierta de un yate de lujo negro de noche, con una pasarela, faroles dorados y el puerto de Montecarlo iluminado al fondo; entre las sombras, un pasillo oscuro con una puerta entreabierta. Cristina avanza de puntillas con el dedo sobre los labios y los ojos muy abiertos de cautela, y Alberto la sigue con una linterna pequeña y gesto tenso."),
    "35": dict(
        titulo="Carta 35 — Otra mitad de microfilm", tipo="roja", combina=[22, 57],
        descripcion=["La otra mitad del microfilm. Combinadla con la primera mitad (carta 22): sumad sus números (35 + 22 = 57) y coged la carta 57."],
        pistas=["Es la otra mitad del microfilm.", "Combinad la carta 35 con la carta 22.", "Sumad los números de las dos cartas: 35 + 22 = 57."],
        arte="La otra mitad de una tira de microfilm, con fotogramas minúsculos, dentro de una cajita de plata sobre una cómoda de un camarote de yate, con un reflejo dorado."),
    "40": dict(
        titulo="Carta 40 — El plano del yate", tipo="gris",
        descripcion=["El plano de los pasillos del yate Neptuno, con la entrada y la salida marcadas. Solo hay un camino de la una a la otra."],
        pistas=["Es el plano del yate: sirve para el mando de la linterna (carta 46).", "En el mando los muros no se ven: seguid el plano desde la entrada, tramo a tramo.", f"Camino completo: {_camino_texto()}."],
        arte=pieza("El plano del yate", "el plano con el laberinto")),
    "46": dict(
        titulo="Carta 46 — El mando de la linterna", tipo="verde",
        descripcion=[
            "Es un juego de la app: os movéis por los pasillos del yate con las flechas, a oscuras: los muros no se ven, solo se nota cuando se choca con uno. El plano del yate (carta 40) muestra el camino desde la entrada, arriba a la izquierda, hasta la salida, abajo a la derecha.",
            "Al llegar a la salida, la puerta de la sala de máquinas se abre. Coged la carta 44."],
        pistas=["Mirad el plano del yate: solo hay un camino de la entrada a la salida.", "Seguid el plano desde la entrada, anotando cada tramo (por ejemplo, «derecha 2, abajo 1...») y repitiéndolo en el mando. Si chocáis con un muro, es que os habéis equivocado de tramo.", f"Camino completo: {_camino_texto()}."],
        arte="Un pasillo estrecho y oscuro de un yate de lujo, con paredes de madera barnizada y una puerta al fondo con una rendija de luz, iluminado solo por una pequeña linterna. Alberto avanza con la mano en la pared y el gesto tenso, y Cristina lo sigue en puntillas, mordiéndose el labio con cara de miedo contenido."),
    "44": dict(
        titulo="Carta 44 — La sala de máquinas", tipo="gris", coge=[38], descarta=[28, 40, 46],
        descripcion=[
            "La puerta se abre y entráis en la sala de máquinas del yate, llena de tuberías y manómetros. En un armario de herramientas, Alberto encuentra unos alicates con mangos aislantes (carta 38).",
            "Coged la carta 38. Descartad las cartas 28, 40 y 46."],
        pistas=["Mirad lo que hay en el armario de herramientas.", "La carta 38 es combinable.", "Coged la carta 38. Descartad las cartas 28, 40 y 46."],
        arte="La sala de máquinas de un yate de lujo: motores brillantes, tuberías de cobre, manómetros y un armario de herramientas abierto. Alberto levanta unos alicates con mangos rojos aislantes con una sonrisa de triunfo y Cristina lo mira con los ojos brillantes de entusiasmo."),
    "38": dict(
        titulo="Carta 38 — Alicates aislantes", tipo="azul", combina=[56, 94],
        descripcion=["Unos alicates cortacables con los mangos aislados, como los que usan los artificieros. Combinadlos con el maletín (carta 56): sumad sus números (38 + 56 = 94) y coged la carta 94."],
        pistas=["Sirven para cortar cables.", "Cuando tengáis el maletín, combinadlo con los alicates.", "Sumad los números de las dos cartas: 38 + 56 = 94."],
        arte="Unos alicates cortacables de acero con mangos rojos aislantes sobre una toalla de taller, junto a un manómetro, en la sala de máquinas de un yate, con luz cálida lateral."),
    "57": dict(
        titulo="Carta 57 — El microfilm completo", tipo="gris", coge=[48, 52, 53], descarta=[22, 35, 10],
        descripcion=[
            "Las dos mitades del microfilm encajan. Alberto lo mete en el proyector del camarote y en la pared aparece una foto aérea de Montecarlo: una torre, la más alta de la ciudad, marcada con un círculo rojo. Pero hay muchas torres y desde la calle se confunden. Un panel (carta 48) pide el perfil de la ciudad y la Agente Zorro ha dejado dos cartas con lo que se ve desde cada lado (cartas 52 y 53).",
            "Coged las cartas 48, 52 y 53. Descartad las cartas 22, 35 y 10."],
        pistas=["Hay un puzle: el panel del skyline y las dos cartas de vistas.", "Las cartas 52 y 53 dan los números del borde de la cuadrícula, repartidos entre las dos.", "Coged las cartas 48, 52 y 53. Descartad las cartas 22, 35 y 10."],
        arte="Un camarote de yate con un proyector de diapositivas antiguo que proyecta en la pared una foto aérea en blanco y negro de una ciudad de rascacielos con una torre marcada con un círculo rojo. Cristina señala la torre con una sonrisa de orgullo y Alberto mira la pared con la boca abierta de sorpresa."),
    "52": dict(
        titulo="Carta 52 — Skyline: arriba e izquierda", tipo="gris",
        descripcion=["Una cuadrícula de 4 × 4 casillas con los números del borde de arriba y de la izquierda: cuántos edificios se ven desde cada lado."],
        pistas=["Es la mitad de las pistas del skyline (carta 48); la otra mitad está en la carta 53.", "En cada fila y en cada columna van las alturas 1, 2, 3 y 4 sin repetir; el número del borde dice cuántos edificios se ven desde ahí.", f"El perfil, de arriba abajo, es: {_skyline_texto()}."],
        arte=pieza("Skyline: arriba e izquierda", "la mitad de las pistas")),
    "53": dict(
        titulo="Carta 53 — Skyline: abajo y derecha", tipo="gris",
        descripcion=["Una cuadrícula de 4 × 4 casillas con los números del borde de abajo y de la derecha, y un ejemplo de cómo se cuentan los edificios."],
        pistas=["Es la otra mitad de las pistas del skyline (carta 48); la primera mitad está en la carta 52.", "Cada número del borde dice cuántos edificios se ven desde ese lado: los altos tapan a los bajos.", f"El perfil, de arriba abajo, es: {_skyline_texto()}."],
        arte=pieza("Skyline: abajo y derecha", "la otra mitad de las pistas")),
    "48": dict(
        titulo="Carta 48 — El panel del skyline", tipo="verde",
        descripcion=[
            "Es un juego de la app: una cuadrícula de 4 × 4 en la que hay que poner la altura (1, 2, 3 o 4) de cada edificio. Los números del borde (cuántos edificios se ven desde cada lado) están repartidos en las cartas 52 y 53.",
            "Al completar el perfil, el panel marca la torre del Dr. Noche. Coged la carta 58."],
        pistas=["Juntad las pistas de las cartas 52 y 53: algunas están arriba, otras abajo, a la izquierda y a la derecha.", "Un 4 en el borde obliga a las cuatro alturas en orden; un 1 pide el edificio más alto pegado a ese borde. Empezad por ahí.", f"El perfil, de arriba abajo, es: {_skyline_texto()}."],
        arte="Un panel de control con una cuadrícula de cuatro por cuatro casillas luminosas que muestra siluetas de edificios de distinta altura, en un camarote de yate con una ventana al puerto. Alberto toca el panel con el dedo y los ojos entrecerrados, y Cristina cuenta con los dedos con cara de ilusión."),
    "58": dict(
        titulo="Carta 58 — La torre del Dr. Noche", tipo="gris", coge=[56], descarta=[48, 52, 53, 57],
        descripcion=[
            "El skyline marca la torre del Dr. Noche, a dos calles del puerto. Subís en un ascensor privado hasta una sala llena de gemas en vitrinas, pero el villano ha huido y ha dejado un maletín plateado sobre una mesa, con una nota que dice: «Si me seguís, lo lamentaréis».",
            "Coged la carta 56. Descartad las cartas 48, 52, 53 y 57."],
        pistas=["Mirad lo que hay sobre la mesa.", "La carta 56 es combinable.", "Coged la carta 56. Descartad las cartas 48, 52, 53 y 57."],
        arte="La sala de una torre de lujo llena de vitrinas con gemas de colores y, en el centro, una mesa con un maletín plateado cerrado con una nota; Cristina lo señala con una ceja arqueada de sospecha y Alberto se asoma con cara de alivio mezclado con inquietud."),
    "56": dict(
        titulo="Carta 56 — Maletín con cuatro cargas", tipo="roja", combina=[38, 94],
        descripcion=["Un maletín plateado que hace tictac. Dentro hay cuatro cargas explosivas con sus cables de colores. Combinadlo con los alicates (carta 38): sumad sus números (56 + 38 = 94) y coged la carta 94."],
        pistas=["Hace tictac: dentro hay cuatro cargas.", "Cuando tengáis los alicates, combinadlos con el maletín.", "Sumad los números de las dos cartas: 56 + 38 = 94."],
        arte="Un maletín plateado entreabierto sobre una mesa con cuatro paquetes con cables de colores y un pequeño reloj con luz roja, visto de cerca con luz dramática lateral."),
    "94": dict(
        titulo="Carta 94 — Las cuatro cargas", tipo="gris", coge=[69, 70], descarta=[56, 38, 44, 58],
        descripcion=[
            "Alberto agarra los alicates y Cristina abre el maletín: cuatro cargas, cada una con cinco cables, y un reloj que corre. En el forro encuentra el manual del desactivador (carta 70) y, sobre la tapa, un panel con las cuatro cargas (carta 69). Solo hay que cortar un cable de cada carga, y el correcto depende de las reglas del manual.",
            "Coged las cartas 69 y 70. Descartad las cartas 56, 38, 44 y 58."],
        pistas=["Hay un puzle: el panel de las cuatro cargas y el manual del desactivador.", "El manual (carta 70) dice qué cable cortar según los colores.", "Coged las cartas 69 y 70. Descartad las cartas 56, 38, 44 y 58."],
        arte="Un maletín plateado abierto sobre una mesa con cuatro cargas con cables de colores y un reloj digital con luz roja, en la sala de una torre. Alberto sostiene unos alicates con el sudor en la frente y gesto de concentración, y Cristina sujeta un librito con las reglas y lee con los ojos muy abiertos de tensión."),
    "70": dict(
        titulo="Carta 70 — El manual del desactivador", tipo="gris",
        descripcion=["El manual del desactivador: cuatro reglas para decidir qué cable cortar en cada carga. Vale la primera que se cumpla."],
        pistas=["Es el manual de las cuatro cargas (carta 69).", "Contad los cables de arriba abajo y comprobad las reglas en orden: vale la primera que se cumple.", f"Los cortes son: {_cortes_texto()}."],
        arte=pieza("El manual del desactivador", "las cuatro reglas de los cables")),
    "69": dict(
        titulo="Carta 69 — El desactivador", tipo="verde",
        descripcion=[
            "Es un juego de la app: las cuatro cargas del maletín, cada una con cinco cables de colores. Hay que cortar un cable de cada carga, el que diga el manual del desactivador (carta 70). Si cortáis el equivocado, la carga se reinicia.",
            "Al desactivar las cuatro cargas, el reloj se detiene. Coged la carta 82."],
        pistas=["Leed el manual del desactivador (carta 70): las reglas se comprueban en orden.", "En cada carga contad los cables de arriba abajo, comprobad las reglas por orden y cortad el cable que dice la primera que se cumpla.", f"Los cortes son: {_cortes_texto()}."],
        arte="Un maletín abierto con cuatro cargas con cables de colores y un reloj con luz roja a punto de llegar a cero. Alberto acerca los alicates a un cable con el pulso temblando y los dientes apretados, y Cristina contiene el aliento con las manos sobre la boca."),
    "82": dict(
        titulo="Carta 82 — La colección del Dr. Noche", tipo="gris", coge=[62], descarta=[69, 70, 94],
        descripcion=[
            "El reloj del maletín se detiene en el último segundo. Al fondo de la sala se abre un panel secreto: la colección privada del Dr. Noche, con gemas del mundo entero, y en el centro, sobre un cojín de terciopelo, el cristal de energía rojo, tal y como cayó.",
            "Coged la carta 62. Descartad las cartas 69, 70 y 94."],
        pistas=["Mirad el cojín de terciopelo del centro.", "La carta 62 es combinable con el Cronoportal.", "Coged la carta 62. Descartad las cartas 69, 70 y 94."],
        arte="Una sala secreta con vitrinas de gemas de colores y, en el centro, un cristal rojo brillante sobre un cojín de terciopelo bajo un foco, con reflejos dorados por todas partes. Cristina lo toma con ambas manos con los ojos llenos de lágrimas de emoción y Alberto la mira con una sonrisa enorme."),
    "62": dict(
        titulo="Carta 62 — Cristal de energía", tipo="roja", combina=[12, 74],
        descripcion=["El cristal de energía del Cronoportal: una gema roja con un fulgor interior. Combinadlo con el Cronoportal (carta 12): sumad sus números (62 + 12 = 74) y coged la carta 74."],
        pistas=["Es la pieza que faltaba.", "Combinad la carta 62 con la carta 12.", "Sumad los números de las dos cartas: 62 + 12 = 74."],
        arte="Un cristal rojo facetado con un fulgor interior de brasa y finas líneas de energía, sostenido sobre la palma de una mano enguantada de blanco, con destellos dorados de fondo."),
    "74": dict(
        titulo="Carta 74 — Cronoportal reconectado", tipo="gris", coge=[99], descarta=[62, 12, 82],
        descripcion=[
            "El cristal encaja con un chasquido y el Cronoportal se enciende. Fuera suenan sirenas y la Agente Zorro grita desde la puerta que la policía llega para detener al Dr. Noche, y que vosotros no podéis estar aquí cuando lleguen. No hay tiempo que perder: activad el aparato.",
            "Coged la carta 99. Descartad las cartas 62, 12 y 82."],
        pistas=["El portal ya funciona. Solo queda activarlo.", "Coged la carta 99. Descartad las cartas 62, 12 y 82."],
        arte="El Cronoportal encendido con un cristal rojo encajado en su pecho, en la sala secreta de una torre, con un arco de luz azul y dorada en el anillo; al fondo, las luces azules de unos coches de policía por una ventana. Cristina, con la cara desencajada de urgencia, tira de Alberto, que carga el aparato con gesto de esfuerzo."),
    "99": dict(
        titulo="Carta 99 — De vuelta a casa (FIN)", tipo="gris", descarta=[74],
        descripcion=[
            "El anillo se abre en un arco de luz justo cuando la policía irrumpe en la sala. Cristina y Alberto salen disparados de Montecarlo y aterrizan en su salón, con el corazón a mil.",
            "Alberto mira el aparato: «Mañana, otro destino». Cristina sonríe y guarda en el bolsillo unas gafas de sol de la Agente Zorro. Descartad la carta 74.",
            "FIN."],
        pistas=[],
        arte="La escena ocurre DENTRO del salón de su casa actual, en el presente (sofá, estanterías con libros, plantas, una lámpara encendida y luz cálida de tarde por la ventana): acaban de VOLVER a casa. Cristina y Alberto acaban de salir de un portal circular de luz azul y dorada que se abre detrás de ellos; a través del portal todavía se ven una sala de lujo con vitrinas de gemas y luces azules de policía. Llevan aún su ropa de espías elegantes de los años 60. Cristina ríe a carcajadas con unas gafas de sol en la mano y Alberto grita de euforia con los brazos en alto. Están de cara a nosotros, aterrizando en el salón y alejándose del portal, que queda a su espalda y se está cerrando; el mundo de la aventura solo se ve a través del portal, detrás de ellos. No están entrando en el portal ni saliendo de casa: están llegando."),
}

META = dict(
    juego="Montecarlo, 1965 — Operación Cristal",
    estilo=ESTILO, personajes=PERSONAJES, hoja=HOJA, foto=FOTO, video=VIDEO,
    mosaicos={k: dict(filas=1, cols=1, cartas=m["cartas"], titulo=m["titulo"], capas=True, desfase=m["desfase"]) for k, m in MOSAICOS.items()},
)

SPEC = dict(
    final="99",
    needs={"26": ["14", "15", "20"], "28": ["30", "31", "24"], "44": ["40", "46"], "57": ["22", "35"],
           "58": ["48", "52", "53"], "94": ["56", "38"], "82": ["69", "70"], "74": ["62", "12"]},
    eventos={},
)

PARA_QUE = {
    "P": "Inicio: llegada a Montecarlo. Te manda coger la 10 y la 12.",
    "10": "El sobre de la Agente Zorro: reparte las dos hojas transparentes, la caja de seguridad y la mitad del microfilm.",
    "12": "El Cronoportal sin cristal: se combina con el cristal de energía (62).",
    "14": "Hoja transparente: se superpone a la 15.", "15": "Hoja transparente: se superpone a la 14.",
    "20": "La caja de seguridad (app): el número que se ve al superponer las hojas.",
    "22": "Mitad de microfilm: se combina con la otra mitad (35).",
    "24": "El teletipo (app): la palabra que se lee por las ventanas de la rejilla.",
    "26": "El despacho de cifrado: reparte la rejilla (30), las letras (31) y el teletipo.",
    "28": "El yate Neptuno: reparte la otra mitad del microfilm, el plano y el mando.",
    "30": "Rejilla de cifrado (carta negra con ventanas): se pone sobre la 31.", "31": "Carta de letras: se pone debajo de la 30.",
    "35": "Otra mitad de microfilm: se combina con la 22.",
    "40": "Plano del yate: el laberinto del mando (46).",
    "46": "El mando de la linterna (app): recorrer el laberinto a ciegas con el plano.",
    "44": "La sala de máquinas: reparte los alicates.",
    "38": "Alicates aislantes: se combinan con el maletín (56).",
    "57": "El microfilm completo (22 + 35): reparte el panel del skyline y sus dos cartas de pistas.",
    "52": "Skyline: pistas de arriba e izquierda.", "53": "Skyline: pistas de abajo y derecha.",
    "48": "El panel del skyline (app): completar el perfil de 4 × 4.",
    "58": "La torre del Dr. Noche: reparte el maletín.",
    "56": "Maletín con cuatro cargas: se combina con los alicates (38).",
    "94": "Las cuatro cargas (56 + 38): reparte el desactivador y su manual.",
    "70": "Manual del desactivador: las reglas de los cables.",
    "69": "El desactivador (app): cortar el cable correcto de cada carga.",
    "82": "La colección del Dr. Noche: reparte el cristal de energía.",
    "62": "Cristal de energía: se combina con el Cronoportal (12).",
    "74": "Cronoportal reconectado (62 + 12): reparte la 99.",
    "99": "Final de la aventura, ya en casa.",
}

# ---------------------------------------------------------------- manual (los estados de la mesa se calculan simulando las cartas)
_TEXTOS = [
    ("leer", "P", "Llegada a Montecarlo", "Pon el Modo PC en el ordenador (solo debe haber la carta P en la mesa y el resto boca abajo en el mazo) y en el móvil abre el juego y pulsa Empezar. Lee la carta P: te manda coger la 10 y la 12."),
    ("leer", "10", "El sobre de la Agente Zorro", "Lee la carta 10. Descarta la P y coge 14, 15, 20 y 22. Superpón las dos hojas transparentes (14 y 15) con los marcos alineados (en el Modo PC, botón «Superponer las cartas»; en papel, a contraluz): aparece un número de tres cifras."),
    ("app", "20", "La caja de seguridad", f"En el móvil: Acción, 20. Escribe el número que se ve al superponer las hojas: {DIG}. El mensaje te dice que cojas la 26.", "carta 26"),
    ("leer", "26", "El despacho de cifrado", "Lee la carta 26. Descarta 14, 15 y 20 y coge 24, 30 y 31. Pon la carta negra con ventanas (30) encima de la de letras (31) con los marcos alineados y lee las letras por las ventanas."),
    ("app", "24", "El teletipo", f"En el móvil: Acción, 24. Escribe la palabra que se lee por las ventanas, de arriba abajo: {PAL}. El mensaje te dice que cojas la 28.", "carta 28"),
    ("leer", "28", "El yate Neptuno", "Lee la carta 28. Descarta 26, 30, 31 y 24 y coge 35, 40 y 46. El plano (40) muestra el camino de la entrada a la salida. Las cartas 22 y 35 son combinables."),
    ("app", "46", "El mando de la linterna", f"En el móvil: Acción, 46. Recorre el laberinto a ciegas siguiendo el plano: {_camino_texto()}. El mensaje te dice que cojas la 44.", "carta 44"),
    ("leer", "44", "La sala de máquinas", "Lee la carta 44. Descarta 28, 40 y 46 y coge la 38, unos alicates."),
    ("combinar", "22", "35", "El microfilm completo", "Las dos mitades del microfilm (22 y 35) son combinables: 22 + 35 = 57. Coge la 57."),
    ("leer", "57", "El microfilm completo", "Lee la carta 57. Descarta 22, 35 y 10 y coge 48, 52 y 53. Las cartas 52 y 53 reparten las pistas del borde de un skyline de 4 × 4."),
    ("app", "48", "El panel del skyline", f"En el móvil: Acción, 48. Completa el perfil con las pistas de las dos cartas (de arriba abajo: {_skyline_texto()}). El mensaje te dice que cojas la 58.", "carta 58"),
    ("leer", "58", "La torre del Dr. Noche", "Lee la carta 58. Descarta 48, 52, 53 y 57 y coge la 56, un maletín con cuatro cargas."),
    ("combinar", "56", "38", "Maletín y alicates", "El maletín (56) y los alicates (38) son combinables: 56 + 38 = 94. Coge la 94."),
    ("leer", "94", "Las cuatro cargas", "Lee la carta 94. Descarta 56, 38, 44 y 58 y coge 69 y 70. La carta 70 es el manual del desactivador."),
    ("app", "69", "El desactivador", f"En el móvil: Acción, 69. Con el manual, corta un cable de cada carga ({_cortes_texto()}). El mensaje te dice que cojas la 82.", "carta 82"),
    ("leer", "82", "La colección del Dr. Noche", "Lee la carta 82. Descarta 69, 70 y 94 y coge la 62, el cristal de energía."),
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
