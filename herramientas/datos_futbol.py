"""La Final del Siglo, 1970: La Copa de Cristal. Undécima parada del Cronoportal: un estadio de fútbol. Los puzles usan formas nuevas de repartir la información:
cartas con DOS CARAS (los seis cromos del Club Estrella: por delante el dorsal, por detrás la ficha técnica), una alineación que se deduce de pistas repartidas en dos cartas,
cuatro jugadas del VAR con su reglamento, una liguilla cuyos marcadores se reconstruyen con una clasificación y unos resultados, y una tanda de penaltis contra un portero con manías.
Las cartas que se dibujan por código (14 a 19 con sus reversos, 30, 31, 40, 41, 42, 52, 53 y 70) las hace herramientas/futbol.py (a partir de instancias_futbol.json)."""
import json
import os

_AQUI = os.path.dirname(os.path.abspath(__file__))
INST = json.load(open(os.path.join(_AQUI, "instancias_futbol.json"), encoding="utf-8"))
LIG = INST["liguilla"]
CROMOS = INST["cromos"]
RES = LIG["resultados"]
EQ = LIG["equipos"]

ESTILO = ("Ilustración pictórica semirrealista con aire de póster de fútbol de los años 70, colores saturados de césped verde, rojo, azul y amarillo, estadio con la grada llena de bufandas y banderines, "
          "luz dorada de tarde, balones de cuero con paneles blancos y negros, redes y porterías de madera, formato vertical 2:3. Sin texto, letras ni números legibles en la imagen; los carteles, "
          "marcadores y papeles solo muestran rayas decorativas. Deja libre de detalles importantes la esquina superior izquierda y el 18 % inferior de la imagen. "
          "Los personajes tienen siempre expresiones distintas y expresivas, adecuadas a la escena (nunca la misma cara en dos imágenes).")

PERSONAJES = {
    "Cristina": "Cristina, mujer de 26 años, profesora, pelo rubio y rizado recogido en una coleta alta, ojos azules. Viste ropa deportiva de los años 70: chándal retro rojo con rayas blancas en las mangas, un silbato colgado al cuello, un cronómetro en la muñeca y zapatillas blancas.",
    "Alberto": "Alberto, hombre de 27 años, informático, pelo moreno corto, barba cuidada, ojos marrones. Viste ropa deportiva de los años 70: chándal retro azul con rayas blancas, una gorra de visera, una bufanda roja y blanca del club al cuello y una pizarra táctica bajo el brazo.",
}

HOJA = ("Crea una hoja de personajes (character sheet) con las dos personas de la foto adjunta, de cuerpo entero y de frente, sobre fondo claro y neutro. "
        "Mantén su parecido real con la foto (cara, pelo, barba, ojos). "
        "Cristina: mujer de 26 años, profesora, pelo rubio y rizado recogido en una coleta alta, ojos azules, chándal retro rojo con rayas blancas en las mangas, silbato colgado al cuello, cronómetro en la muñeca y zapatillas blancas. "
        "Alberto: hombre de 27 años, informático, pelo moreno corto, barba cuidada, ojos marrones, chándal retro azul con rayas blancas, gorra de visera, bufanda roja y blanca del club y una pizarra táctica bajo el brazo. "
        "Estilo: " + ESTILO)

FOTO = ("Antes de nada, adjunta a ChatGPT una foto de Cristina y Alberto juntos (o una de cada uno, con la cara bien visible). "
        "Pídele que mantenga el parecido real, pero con el estilo de ilustración de este juego.")

VIDEO = ("Crea un vídeo vertical 9:16 de 15 segundos, con estilo cinematográfico de película deportiva de los años 70, luz dorada de tarde y colores saturados. Sin ningún texto, letra ni subtítulo en pantalla. "
         "Escena 1 (0-4 s): en el salón de una casa actual, Cristina (mujer de 26 años, rubia de pelo rizado, ojos azules) y Alberto (hombre de 27 años, moreno con barba, ojos marrones) rodean un aparato de latón y cristal con un anillo central: el Cronoportal. Cristina señala la foto de un estadio antiguo en un álbum de cromos. "
         "Escena 2 (4-8 s): el anillo se enciende con un arco de luz azul y dorada y los dos son absorbidos por un túnel de luz. "
         "Escena 3 (8-12 s): caen en el túnel de vestuarios de un estadio de 1970 con el rugido de la grada al fondo; el aparato golpea un carro de balones y su cristal sale rodando hacia el campo. "
         "Escena 4 (12-15 s): primer plano de Cristina y Alberto, con chándales retro, asombrados, mientras un entrenador con gabardina les da una pizarra táctica; fundido a negro. "
         "Sonido: zumbido eléctrico creciente, silbido del portal, golpe sordo al aterrizar, rugido de una grada, silbato de árbitro y organillo, sin voz de narrador.")


def pieza(titulo, donde):
    return f"Carta dibujada por código (herramientas/futbol.py; no se pide a ChatGPT): {donde} de «{titulo}»."


def _cromo(carta):
    c = CROMOS[carta]
    return dict(
        titulo=f"Carta {carta} — Cromo de {c['nombre']}", tipo="gris", reverso=True,
        descripcion=[f"Un cromo del Club Estrella: la camiseta con el dorsal {c['dorsal']} y el nombre del jugador. Es una carta de dos caras: por delante solo se ve la camiseta y, dándole la vuelta (en papel, con la hoja de reversos impresa a doble cara), se ve la ficha técnica del jugador."],
        pistas=["Es un cromo de dos caras.", "Dadle la vuelta para ver la ficha técnica: posición, pie, altura y edad.", "Comparad las fichas de los seis cromos con lo que busca el míster (carta 20)."],
        arte=pieza(f"Cromo de {c['nombre']}", "el anverso y el reverso"))


J = {
    "P": dict(
        titulo="Carta P — Llegada al estadio", tipo="gris", coge=[10, 12],
        descripcion=[
            "Undécima parada del Cronoportal: el estadio del Club Estrella, en 1970, una hora y media antes de la final del siglo. Aterrizáis en el túnel de vestuarios con el rugido de la grada al fondo, y el aparato golpea un carro de balones. Su cristal de energía sale rodando por el túnel hasta caer, de rebote, dentro de la Copa de cristal que un mozo lleva en ese momento al palco. No se podrá recuperar hasta que acabe la final.",
            "Don Remigio, el entrenador del Estrella, ve vuestros chándales y os confunde con su cuerpo técnico: «¡Por fin, los ayudantes que me mandó la federación! Faltan noventa minutos para el pitido inicial». Ayudadle a ganar la final y la Copa será suya... y vuestro cristal también.",
            "Coged las cartas 10 y 12."],
        pistas=["Mirad a vuestro alrededor y revisad el aparato.", "Coged las cartas 10 y 12."],
        arte="El túnel de vestuarios de un estadio de fútbol de 1970, con la luz del campo y el rugido de la grada al fondo; un carro de balones de cuero volcado y balones por el suelo. En primer plano, el Cronoportal, un aparato de latón y cristal, humea con la luz azul apagándose. Cristina, con la boca abierta y los ojos muy abiertos de asombro, y Alberto, con la gorra torcida y gesto de incredulidad, se levantan aturdidos con chándales retro, mientras un entrenador con gabardina y bigote les hace señas desde un lado."),
    "10": dict(
        titulo="Carta 10 — El vestuario del Estrella", tipo="gris", coge=[14, 15, 16, 17, 18, 19, 20, 22], descarta=["P"],
        descripcion=[
            "El vestuario del Estrella, con las camisetas rojas y blancas colgadas en sus perchas. Don Remigio ha perdido la hoja de convocatoria y solo recuerda cómo es el jugador que necesita: lo cuenta en el tablón (carta 20). Sobre el banco están los seis cromos de la plantilla (cartas 14 a 19) y, entre las botas, Cristina encuentra la mitad de un pase de prensa (carta 22).",
            "Coged las cartas 14, 15, 16, 17, 18, 19, 20 y 22. Descartad la carta P."],
        pistas=["Hay un puzle: los seis cromos y la convocatoria.", "Los cromos tienen dos caras: dadles la vuelta.", "Coged las cartas 14, 15, 16, 17, 18, 19, 20 y 22. Descartad la carta P."],
        arte="Un vestuario de fútbol de 1970: bancos de madera, camisetas rojas y blancas colgadas en perchas, botas de cuero y un tablón de corcho. Sobre el banco, seis cromos de jugadores boca arriba y boca abajo. Cristina da la vuelta a un cromo con curiosidad y los ojos entrecerrados y Alberto examina otro con la gorra echada hacia atrás y gesto de duda."),
    "12": dict(
        titulo="Carta 12 — Cronoportal sin cristal", tipo="azul", combina=[62, 74],
        descripcion=[
            "El Cronoportal: una consola de latón y cristal con un anillo central apagado y un hueco vacío en el pecho, donde iba el cristal de energía. Alberto: «Sin el cristal no hay portal. Se ha ido dentro de la Copa... y la Copa solo sale del palco para el campeón».",
            "Cuando recuperéis el cristal (carta 62), combinadlo con el Cronoportal: sumad sus números (12 + 62 = 74) y coged la carta 74."],
        pistas=["Le falta una pieza: el cristal de energía.", "Combinad la carta 12 con la carta 62.", "Sumad los números de las dos cartas: 12 + 62 = 74."],
        arte="Primer plano del Cronoportal: una consola portátil de latón y cristal con dos antenas de cobre, un anillo de cristal central apagado y un hueco circular vacío en el pecho del aparato, apoyado sobre un banco de madera de un vestuario de fútbol, con camisetas rojas y blancas desenfocadas al fondo."),
    "14": _cromo("14"), "15": _cromo("15"), "16": _cromo("16"), "17": _cromo("17"), "18": _cromo("18"), "19": _cromo("19"),
    "20": dict(
        titulo="Carta 20 — La convocatoria", tipo="verde",
        descripcion=[
            "Es un juego de la app: seis botones con los dorsales de la plantilla. Don Remigio busca a un jugador y solo recuerda esto: es ZURDO, mide MÁS de 1,75 m y MENOS de 1,80 m, y NO juega de defensa. Las fichas técnicas están por detrás de los cromos (cartas 14 a 19).",
            "Al acertar, el míster lo anota en la hoja. Coged la carta 26."],
        pistas=["Dad la vuelta a los cromos: la ficha técnica está por detrás de cada uno.", "Buscad al jugador que cumple las tres condiciones a la vez: pie zurdo, altura entre 1,75 m y 1,80 m, y posición que no sea defensa.", "Es Beto Pase, el del dorsal 10."],
        arte="Un tablón de corcho en un vestuario de fútbol con una hoja de convocatoria casi en blanco y seis chinchetas de colores, bajo la luz de un fluorescente. Alberto señala el tablón con el dedo y los ojos muy abiertos de expectación, y Cristina cuenta con los dedos con la lengua entre los dientes, concentrada."),
    "22": dict(
        titulo="Carta 22 — Mitad de pase de prensa", tipo="azul", combina=[35, 57],
        descripcion=["La mitad de un pase de prensa plastificado, con una foto en blanco y negro y un cordón. Combinadla con la otra mitad (carta 35): sumad sus números (22 + 35 = 57) y coged la carta 57."],
        pistas=["Es solo la mitad de un pase de prensa.", "Cuando encontréis la otra mitad, combinadlas.", "Sumad los números de las dos cartas: 22 + 35 = 57."],
        arte="La mitad de un pase de prensa plastificado de un estadio, con un cordón rojo, una foto en blanco y negro y una raya de rotura limpia, sobre un banco de madera con unas botas de fútbol de cuero, vista de cerca con luz dorada."),
    "26": dict(
        titulo="Carta 26 — La pizarra del míster", tipo="gris", coge=[24, 30, 31], descarta=[14, 15, 16, 17, 18, 19, 20],
        descripcion=[
            "Don Remigio apunta el dorsal 10 en su hoja, satisfecho, y os lleva a su pizarra táctica: hay que adivinar la alineación de Los Rayos, el rival, con las pistas que ha apuntado un espía (cartas 30 y 31) sobre el campo dibujado. Una pizarra interactiva (carta 24) espera la alineación.",
            "Coged las cartas 24, 30 y 31. Descartad las cartas 14, 15, 16, 17, 18, 19 y 20."],
        pistas=["Hay un puzle: las pistas del espía y la pizarra.", "Las pistas están repartidas en dos cartas.", "Coged las cartas 24, 30 y 31. Descartad las cartas 14, 15, 16, 17, 18, 19 y 20."],
        arte="La pizarra táctica de un entrenador de fútbol en un despacho de estadio de 1970, con un campo dibujado con tiza verde, fichas redondas de colores y un trofeo de cartón en una estantería. Cristina compara dos hojas con anotaciones con el ceño fruncido de concentración y Alberto mueve una ficha en la pizarra con la lengua entre los dientes."),
    "24": dict(
        titulo="Carta 24 — La pizarra", tipo="verde",
        descripcion=[
            "Es un juego de la app: un campo en formación 1-2-2-1 con seis puestos y seis dorsales (1, 2, 5, 6, 8 y 11). Hay que colocar a cada jugador en su sitio con las pistas del espía (cartas 30 y 31). Izquierda y derecha se miran desde la portería propia hacia el ataque.",
            "Al acertar, el míster tiene la alineación del rival. Coged la carta 28."],
        pistas=["Mirad el campo de la pizarra: tiene seis puestos y las pistas están repartidas en dos cartas.", "Empezad por las pistas que dan un puesto exacto (el portero) y seguid con las de la izquierda y la derecha.", "Portero: el 1. Defensas: el 6 (izquierda) y el 2 (derecha). Medios: el 11 (izquierda) y el 5 (derecha). Delantero: el 8."],
        arte="Una pizarra táctica magnética con un campo de fútbol dibujado y seis fichas redondas numeradas colocadas en formación, con tiza y un borrador. Alberto coloca una ficha con cuidado y gesto de concentración y Cristina señala otra con la cara iluminada por una idea."),
    "30": dict(
        titulo="Carta 30 — Pizarra del rival (pistas 1 de 2)", tipo="gris",
        descripcion=["La pizarra del rival con el campo de Los Rayos en formación 1-2-2-1 y las primeras pistas de nuestro espía sobre los dorsales."],
        pistas=["Es la primera mitad de las pistas de la pizarra (carta 24).", "La otra mitad de las pistas está en la carta 31.", "Cada pista habla de uno o dos dorsales: su puesto, su lado o su línea."],
        arte=pieza("Pizarra del rival (pistas 1 de 2)", "la primera mitad de las pistas")),
    "31": dict(
        titulo="Carta 31 — Pizarra del rival (pistas 2 de 2)", tipo="gris",
        descripcion=["La pizarra del rival con el campo de Los Rayos en formación 1-2-2-1 y las demás pistas de nuestro espía sobre los dorsales."],
        pistas=["Es la segunda mitad de las pistas de la pizarra (carta 24).", "La otra mitad de las pistas está en la carta 30.", "Cada pista habla de uno o dos dorsales: su puesto, su lado o su línea."],
        arte=pieza("Pizarra del rival (pistas 2 de 2)", "la segunda mitad de las pistas")),
    "28": dict(
        titulo="Carta 28 — La sala del VAR", tipo="gris", coge=[35, 40, 41, 42, 46], descarta=[26, 30, 31, 24],
        descripcion=[
            "Con la alineación del rival en la mano, Don Remigio os manda a la sala del VAR, donde los árbitros revisan cuatro jugadas polémicas de los entrenamientos (cartas 40 y 41) y necesitan a alguien que conozca el reglamento del fuera de juego (carta 42). En una mesa, Alberto encuentra la otra mitad del pase de prensa (carta 35). Una pantalla (carta 46) espera vuestro veredicto.",
            "Coged las cartas 35, 40, 41, 42 y 46. Descartad las cartas 26, 30, 31 y 24."],
        pistas=["Hay dos cosas: la otra mitad del pase y las jugadas del VAR.", "Las cartas 22 y 35 son combinables. El reglamento (42) sirve para decidir las jugadas (40 y 41).", "Coged las cartas 35, 40, 41, 42 y 46. Descartad las cartas 26, 30, 31 y 24."],
        arte="Una sala de vídeo-arbitraje de los años 70 con un gran televisor de tubo, una consola con botones y cintas de vídeo, y dos árbitros con camiseta negra de espaldas, mirando un campo dibujado en la pantalla. Cristina, con las manos en la cabeza y los ojos muy abiertos de emoción, y Alberto, con el mando en la mano y una sonrisa de alivio, encuentran un pase de prensa a medias sobre la mesa."),
    "35": dict(
        titulo="Carta 35 — Otra mitad de pase de prensa", tipo="roja", combina=[22, 57],
        descripcion=["La otra mitad del pase de prensa, con el resto de la foto y el sello del club. Combinadla con la primera mitad (carta 22): sumad sus números (35 + 22 = 57) y coged la carta 57."],
        pistas=["Es la otra mitad del pase de prensa.", "Combinad la carta 35 con la carta 22.", "Sumad los números de las dos cartas: 35 + 22 = 57."],
        arte="La otra mitad de un pase de prensa plastificado de un estadio, con el sello del club y el resto de una foto en blanco y negro, sobre una mesa de la sala de vídeo-arbitraje junto a una cinta de vídeo, con un reflejo azulado del televisor."),
    "40": dict(
        titulo="Carta 40 — VAR: jugadas A y B", tipo="gris",
        descripcion=["Dos jugadas del entrenamiento dibujadas sobre un campo, vistas desde arriba: los atacantes (azul) atacan hacia la derecha y los defensores (rojo) y el portero (amarillo) defienden. Una flecha discontinua marca el pase y un puntito blanco, el balón."],
        pistas=["Son las jugadas A y B del VAR (carta 46).", "Leed el reglamento (carta 42): fijaos en el penúltimo defensor, en quien recibe y en el balón.", "La jugada A es fuera de juego y la B es válida."],
        arte=pieza("VAR: jugadas A y B", "las dos primeras jugadas")),
    "41": dict(
        titulo="Carta 41 — VAR: jugadas C y D", tipo="gris",
        descripcion=["Otras dos jugadas del entrenamiento dibujadas sobre un campo, vistas desde arriba: los atacantes (azul) atacan hacia la derecha y los defensores (rojo) y el portero (amarillo) defienden. Una flecha discontinua marca el pase y un puntito blanco, el balón."],
        pistas=["Son las jugadas C y D del VAR (carta 46).", "Leed el reglamento (carta 42): fijaos en el penúltimo defensor, en quien recibe y en el balón.", "La jugada C es válida y la D es fuera de juego."],
        arte=pieza("VAR: jugadas C y D", "las dos últimas jugadas")),
    "42": dict(
        titulo="Carta 42 — Reglamento: el fuera de juego", tipo="gris",
        descripcion=["El reglamento del fuera de juego, con un ejemplo dibujado: para que sea fuera de juego, quien recibe tiene que estar más cerca de la portería rival que el penúltimo defensor y que el balón, en el momento del pase."],
        pistas=["Es el reglamento de las jugadas del VAR (cartas 40 y 41).", "El portero cuenta como defensor: el penúltimo es el segundo defensor más cercano a su portería. Si quien recibe está detrás del balón, no hay fuera de juego.", "Jugadas: A fuera de juego, B válida, C válida y D fuera de juego."],
        arte=pieza("Reglamento: el fuera de juego", "las reglas y el ejemplo")),
    "46": dict(
        titulo="Carta 46 — El veredicto del VAR", tipo="verde",
        descripcion=[
            "Es un juego de la app: cuatro jugadas (A, B, C y D) con un botón cada una para marcarla como gol válido o como fuera de juego. Las jugadas están dibujadas en las cartas 40 y 41 y el reglamento, en la 42.",
            "Al dar el veredicto correcto, el árbitro os da las gracias. Coged la carta 44."],
        pistas=["Leed el reglamento (carta 42): hay dos condiciones a la vez.", "En cada jugada mirad al penúltimo defensor (el portero cuenta) y comparad su posición con la de quien recibe y con la del balón.", "Jugada A: fuera de juego. B: gol válido. C: gol válido. D: fuera de juego."],
        arte="Una pantalla de vídeo-arbitraje de los años 70 con cuatro recuadros que muestran jugadas de fútbol, con una luz verde y otra roja encima de cada uno. Alberto señala un recuadro con el dedo y una ceja arqueada de seguridad y Cristina mira otro con el ceño fruncido de duda."),
    "44": dict(
        titulo="Carta 44 — El banquillo", tipo="gris", coge=[38], descarta=[28, 40, 41, 42, 46],
        descripcion=[
            "El árbitro da por buenos vuestros veredictos y os lleva al banquillo, donde descansan los suplentes. Entre las toallas y los botiquines, Alberto encuentra un silbato de árbitro de metal (carta 38) olvidado por un linier.",
            "Coged la carta 38. Descartad las cartas 28, 40, 41, 42 y 46."],
        pistas=["Mirad lo que han olvidado entre las toallas.", "La carta 38 es combinable.", "Coged la carta 38. Descartad las cartas 28, 40, 41, 42 y 46."],
        arte="El banquillo de un estadio de fútbol de 1970: un banco largo de madera con toallas, botiquines y botellas de cristal, con el campo de césped al fondo. Alberto levanta un silbato de metal entre las toallas con una sonrisa de triunfo y Cristina lo mira con los ojos brillantes de entusiasmo."),
    "38": dict(
        titulo="Carta 38 — Silbato de árbitro", tipo="azul", combina=[56, 94],
        descripcion=["Un silbato de árbitro de metal con una cadenita. Combinadlo con el balón de la final (carta 56): sumad sus números (38 + 56 = 94) y coged la carta 94."],
        pistas=["Es el silbato de un árbitro.", "Cuando tengáis el balón de la final, combinadlo con el silbato.", "Sumad los números de las dos cartas: 38 + 56 = 94."],
        arte="Un silbato de árbitro de metal plateado con una cadenita sobre una toalla blanca, con el borde de un campo de césped desenfocado al fondo y luz dorada de tarde, visto de cerca."),
    "57": dict(
        titulo="Carta 57 — El pase de prensa", tipo="gris", coge=[48, 52, 53], descarta=[22, 35, 10],
        descripcion=[
            "Las dos mitades del pase de prensa encajan y abren la puerta del palco de autoridades, en lo alto del estadio. Desde allí se ve todo el campo y, sobre una mesa, la Copa de cristal. Hay un tablero de clasificación de la liguilla clasificatoria (carta 52), una hoja con los resultados conocidos (carta 53) y un panel donde reconstruir los marcadores que faltan (carta 48).",
            "Coged las cartas 48, 52 y 53. Descartad las cartas 22, 35 y 10."],
        pistas=["Hay un puzle: el panel de la liguilla con la clasificación y los resultados.", "La clasificación (52) y los resultados conocidos (53) se necesitan los dos.", "Coged las cartas 48, 52 y 53. Descartad las cartas 22, 35 y 10."],
        arte="El palco de autoridades de un estadio de 1970, con butacas de madera, banderines y una gran copa de cristal sobre una mesa con un mantel rojo; por la ventana, el campo de césped lleno de gente. Cristina muestra el pase de prensa a un portero uniformado con una sonrisa de orgullo y Alberto mira la copa con los ojos muy abiertos."),
    "52": dict(
        titulo="Carta 52 — La clasificación", tipo="gris",
        descripcion=["La clasificación de una liguilla de cuatro equipos que se enfrentan todos contra todos: partidos jugados, puntos, goles a favor y goles en contra de cada uno. Victoria: 3 puntos; empate: 1."],
        pistas=["Es la clasificación de la liguilla (carta 48).", "Los resultados conocidos están en la carta 53. Con los puntos y los goles de cada equipo se calculan los marcadores que faltan.", f"Faltan estos marcadores: {EQ[0]}–{EQ[1]} {RES[0][0]}-{RES[0][1]}, {EQ[0]}–{EQ[3]} {RES[2][0]}-{RES[2][1]} y {EQ[1]}–{EQ[2]} {RES[3][0]}-{RES[3][1]}."],
        arte=pieza("La clasificación", "la tabla de la liguilla")),
    "53": dict(
        titulo="Carta 53 — Resultados conocidos", tipo="gris",
        descripcion=["Tres resultados ya conocidos de la liguilla y los tres partidos de los que faltan los marcadores, con el equipo local a la izquierda."],
        pistas=["Son los resultados que ya se conocen (carta 48); la clasificación está en la carta 52.", "Cada equipo ha jugado tres partidos: restad a sus goles y puntos lo que ya sabéis y lo que queda es de los partidos por jugar.", f"Faltan estos marcadores: {EQ[0]}–{EQ[1]} {RES[0][0]}-{RES[0][1]}, {EQ[0]}–{EQ[3]} {RES[2][0]}-{RES[2][1]} y {EQ[1]}–{EQ[2]} {RES[3][0]}-{RES[3][1]}."],
        arte=pieza("Resultados conocidos", "la hoja de resultados")),
    "48": dict(
        titulo="Carta 48 — El panel de la liguilla", tipo="verde",
        descripcion=[
            "Es un juego de la app: los tres partidos de la liguilla de los que faltan los marcadores, con un contador de goles para cada equipo. Hay que poner los marcadores de forma que, junto con los resultados conocidos (carta 53), salga exactamente la clasificación de la carta 52.",
            "Al acertar, el locutor anuncia la clasificación. Coged la carta 58."],
        pistas=["Juntad la clasificación (carta 52) y los resultados conocidos (carta 53).", "Cada equipo ha jugado tres partidos y conocéis dos o tres de ellos: restad a sus goles y puntos lo que ya sabéis y lo que queda es de los partidos por jugar.", f"{EQ[0]}–{EQ[1]} {RES[0][0]}-{RES[0][1]}, {EQ[0]}–{EQ[3]} {RES[2][0]}-{RES[2][1]} y {EQ[1]}–{EQ[2]} {RES[3][0]}-{RES[3][1]}."],
        arte="Un panel de marcadores de estadio de los años 70, con contadores mecánicos de números blancos sobre fondo negro y una tabla de equipos pintada, visto desde el palco con el campo al fondo. Alberto gira un contador con el dedo y los ojos entrecerrados de concentración y Cristina cuenta goles con los dedos con cara de ilusión."),
    "58": dict(
        titulo="Carta 58 — El palco", tipo="gris", coge=[56], descarta=[48, 52, 53, 57],
        descripcion=[
            "La clasificación queda clara y el locutor os da paso al túnel de salida del campo, donde un mozo reparte los balones oficiales de la final. Uno, con las costuras de cuero y el escudo del Estrella, es el balón de la final.",
            "Coged la carta 56. Descartad las cartas 48, 52, 53 y 57."],
        pistas=["Mirad lo que reparte el mozo.", "La carta 56 es combinable.", "Coged la carta 56. Descartad las cartas 48, 52, 53 y 57."],
        arte="El túnel de salida al campo de un estadio de fútbol de 1970, con un carro de balones de cuero y un mozo uniformado; el campo de césped lleno de gente brilla al fondo. Cristina toma un balón con una sonrisa radiante de alegría y Alberto lo mira con cara de alivio."),
    "56": dict(
        titulo="Carta 56 — Balón de la final", tipo="roja", combina=[38, 94],
        descripcion=["El balón de la final: de cuero, con los paneles blancos y negros y el escudo del Estrella. Combinadlo con el silbato (carta 38): sumad sus números (56 + 38 = 94) y coged la carta 94."],
        pistas=["Es el balón oficial de la final.", "Cuando tengáis el silbato, combinadlo con el balón.", "Sumad los números de las dos cartas: 56 + 38 = 94."],
        arte="Un balón de fútbol de cuero de los años 70, con paneles blancos y negros y un escudo rojo, sobre el césped con la línea de cal blanca, visto de cerca con luz dorada de tarde."),
    "94": dict(
        titulo="Carta 94 — La tanda de penaltis", tipo="gris", coge=[69, 70], descarta=[56, 38, 44, 58],
        descripcion=[
            "Con el balón y el silbato, el árbitro os deja pitar en el entrenamiento previo: el Estrella y Los Rayos están empatados y se van a decidir por penaltis, y Don Remigio quiere que ensayéis con vosotros el lanzamiento. El informe del entrenador (carta 70) cuenta las manías del portero rival y un panel (carta 69) simula la tanda.",
            "Coged las cartas 69 y 70. Descartad las cartas 56, 38, 44 y 58."],
        pistas=["Hay un puzle: la tanda de penaltis y el informe del entrenador.", "El informe (carta 70) cuenta cómo se lanza el portero.", "Coged las cartas 69 y 70. Descartad las cartas 56, 38, 44 y 58."],
        arte="El punto de penalti de un estadio de fútbol de 1970 con un balón de cuero sobre la cal blanca y una portería con red de cuerda; una grada llena y borrosa al fondo. Cristina sujeta un silbato con gesto de concentración y Alberto coloca el balón con cuidado, sacando la lengua."),
    "70": dict(
        titulo="Carta 70 — El informe del entrenador", tipo="gris",
        descripcion=["El informe del entrenador sobre el portero rival y sus manías, con las tres zonas de la portería: izquierda, centro y derecha."],
        pistas=["Es el informe sobre el portero (carta 69).", "El portero se lanza según el penalti anterior: planificad cada tiro para chutar a un lado distinto del suyo.", "Un ejemplo válido es: derecha, izquierda, centro, derecha, izquierda."],
        arte=pieza("El informe del entrenador", "el informe sobre el portero")),
    "69": dict(
        titulo="Carta 69 — La tanda de penaltis", tipo="verde",
        descripcion=[
            "Es un juego de la app: una tanda de cinco penaltis contra un portero con manías. Para cada penalti hay que elegir hacia dónde chutar (izquierda, centro o derecha). El informe del entrenador (carta 70) explica cómo decide el portero hacia dónde se lanza. Hay que marcar los cinco y chutar al menos una vez al centro.",
            "Al marcar la tanda, el estadio estalla. Coged la carta 82."],
        pistas=["Leed el informe del entrenador (carta 70): el portero se lanza según el penalti anterior.", "Antes de cada tiro, calculad a dónde se va a lanzar el portero y chutad a otro lado. Recordad que hay que chutar una vez al centro.", "Un ejemplo válido es: derecha, izquierda, centro, derecha, izquierda."],
        arte="Una portería de fútbol de 1970 con red de cuerda y un portero con jersey gris y guantes de lana lanzándose hacia un lado, con un balón de cuero entrando por el otro lado. Alberto levanta los brazos en el área con una sonrisa enorme y Cristina grita de alegría con los puños apretados."),
    "82": dict(
        titulo="Carta 82 — La Copa de cristal", tipo="gris", coge=[62], descarta=[69, 70, 94],
        descripcion=[
            "El Estrella gana la final por penaltis y la grada se vuelve loca. En la ceremonia, Don Remigio levanta la Copa de cristal y, en su interior, entre destellos, brilla el cristal de energía rojo, tal y como cayó.",
            "Coged la carta 62. Descartad las cartas 69, 70 y 94."],
        pistas=["Mirad dentro de la Copa.", "La carta 62 es combinable con el Cronoportal.", "Coged la carta 62. Descartad las cartas 69, 70 y 94."],
        arte="Un entrenador con gabardina levantando una copa de cristal sobre el campo de un estadio lleno, con un cristal rojo brillando dentro de la copa, entre confeti y bufandas. Cristina lo mira con los ojos llenos de lágrimas de emoción y Alberto aplaude con una sonrisa enorme."),
    "62": dict(
        titulo="Carta 62 — Cristal de energía", tipo="roja", combina=[12, 74],
        descripcion=["El cristal de energía del Cronoportal: una gema roja con un fulgor interior. Combinadlo con el Cronoportal (carta 12): sumad sus números (62 + 12 = 74) y coged la carta 74."],
        pistas=["Es la pieza que faltaba.", "Combinad la carta 62 con la carta 12.", "Sumad los números de las dos cartas: 62 + 12 = 74."],
        arte="Un cristal rojo facetado con un fulgor interior de brasa y finas líneas de energía, sostenido sobre la palma de una mano, con confeti rojo y blanco flotando alrededor."),
    "74": dict(
        titulo="Carta 74 — Cronoportal reconectado", tipo="gris", coge=[99], descarta=[62, 12, 82],
        descripcion=[
            "El cristal encaja con un chasquido y el Cronoportal se enciende. Don Remigio, abrazado a la Copa, os busca para daros las gracias, pero ya no hay tiempo: la grada invade el campo y cuando os alcance os habrá visto desaparecer. Activad el aparato.",
            "Coged la carta 99. Descartad las cartas 62, 12 y 82."],
        pistas=["El portal ya funciona. Solo queda activarlo.", "Coged la carta 99. Descartad las cartas 62, 12 y 82."],
        arte="El Cronoportal encendido con un cristal rojo encajado en su pecho, en el túnel de vestuarios de un estadio, con un arco de luz azul y dorada en el anillo; al fondo, una multitud con bufandas corre hacia ellos. Cristina, con la cara desencajada de urgencia, tira de Alberto, que carga el aparato con gesto de esfuerzo."),
    "99": dict(
        titulo="Carta 99 — De vuelta a casa (FIN)", tipo="gris", descarta=[74],
        descripcion=[
            "El anillo se abre en un arco de luz justo cuando la multitud llega al túnel. Cristina y Alberto salen disparados del estadio y aterrizan en su salón, con el corazón a mil.",
            "Alberto mira el aparato: «Mañana, otro destino». Cristina sonríe y guarda en el bolsillo el cromo del dorsal 10. Descartad la carta 74.",
            "FIN."],
        pistas=[],
        arte="La escena ocurre DENTRO del salón de su casa actual, en el presente (sofá, estanterías con libros, plantas, una lámpara encendida y luz cálida de tarde por la ventana): acaban de VOLVER a casa. Cristina y Alberto acaban de salir de un portal circular de luz azul y dorada que se abre detrás de ellos; a través del portal todavía se ven un túnel de estadio y una multitud con bufandas. Llevan aún sus chándales retro de los años 70. Cristina ríe a carcajadas con un cromo de fútbol en la mano y Alberto grita de euforia con los brazos en alto y la bufanda ondeando. Están de cara a nosotros, aterrizando en el salón y alejándose del portal, que queda a su espalda y se está cerrando; el mundo de la aventura solo se ve a través del portal, detrás de ellos. No están entrando en el portal ni saliendo de casa: están llegando."),
}

META = dict(
    juego="La Final del Siglo, 1970 — La Copa de Cristal",
    estilo=ESTILO, personajes=PERSONAJES, hoja=HOJA, foto=FOTO, video=VIDEO,
)

SPEC = dict(
    final="99",
    needs={"26": ["14", "15", "16", "17", "18", "19", "20"], "28": ["30", "31", "24"], "44": ["40", "41", "42", "46"], "57": ["22", "35"],
           "58": ["48", "52", "53"], "94": ["56", "38"], "82": ["69", "70"], "74": ["62", "12"]},
    eventos={},
)

PARA_QUE = {
    "P": "Inicio: llegada al estadio. Te manda coger la 10 y la 12.",
    "10": "El vestuario: reparte los seis cromos, la convocatoria y la mitad del pase.",
    "12": "El Cronoportal sin cristal: se combina con el cristal de energía (62).",
    "14": "Cromo con dos caras.", "15": "Cromo con dos caras.", "16": "Cromo con dos caras.", "17": "Cromo con dos caras.", "18": "Cromo con dos caras.", "19": "Cromo con dos caras.",
    "20": "La convocatoria (app): el jugador que describe el míster, con las fichas de los reversos.",
    "22": "Mitad de pase de prensa: se combina con la otra mitad (35).",
    "24": "La pizarra (app): la alineación del rival con las pistas.",
    "26": "La pizarra del míster: reparte las pistas del espía y la pizarra.",
    "28": "La sala del VAR: reparte las jugadas, el reglamento y el veredicto.",
    "30": "Pistas del espía (1 de 2).", "31": "Pistas del espía (2 de 2).",
    "35": "Otra mitad de pase de prensa: se combina con la 22.",
    "40": "Jugadas A y B del VAR.", "41": "Jugadas C y D del VAR.", "42": "Reglamento del fuera de juego.",
    "46": "El veredicto del VAR (app): gol válido o fuera de juego en cada jugada.",
    "44": "El banquillo: reparte el silbato.",
    "38": "Silbato: se combina con el balón de la final (56).",
    "57": "El pase de prensa (22 + 35): reparte el panel de la liguilla y sus dos cartas.",
    "52": "Clasificación de la liguilla.", "53": "Resultados conocidos de la liguilla.",
    "48": "El panel de la liguilla (app): reconstruir tres marcadores.",
    "58": "El palco: reparte el balón de la final.",
    "56": "Balón de la final: se combina con el silbato (38).",
    "94": "La tanda de penaltis (56 + 38): reparte el panel y el informe.",
    "70": "Informe del entrenador sobre el portero.",
    "69": "La tanda de penaltis (app): marcar los cinco chutando según el informe.",
    "82": "La Copa de cristal: reparte el cristal de energía.",
    "62": "Cristal de energía: se combina con el Cronoportal (12).",
    "74": "Cronoportal reconectado (62 + 12): reparte la 99.",
    "99": "Final de la aventura, ya en casa.",
}

_RES = f"{EQ[0]}–{EQ[1]} {RES[0][0]}-{RES[0][1]}, {EQ[0]}–{EQ[3]} {RES[2][0]}-{RES[2][1]} y {EQ[1]}–{EQ[2]} {RES[3][0]}-{RES[3][1]}"

# ---------------------------------------------------------------- manual (los estados de la mesa se calculan simulando las cartas)
_TEXTOS = [
    ("leer", "P", "Llegada al estadio", "Pon el Modo PC en el ordenador (solo debe haber la carta P en la mesa y el resto boca abajo en el mazo) y en el móvil abre el juego y pulsa Empezar. Lee la carta P: te manda coger la 10 y la 12."),
    ("leer", "10", "El vestuario del Estrella", "Lee la carta 10. Descarta la P y coge 14, 15, 16, 17, 18, 19, 20 y 22. Los seis cromos tienen dos caras: en el Modo PC, botón «Dar la vuelta»; en papel, hoja de reversos a doble cara."),
    ("app", "20", "La convocatoria", "En el móvil: Acción, 20. Con las fichas de los reversos, el jugador zurdo, de entre 1,75 m y 1,80 m y que no es defensa es el dorsal 10. El mensaje te dice que cojas la 26.", "carta 26"),
    ("leer", "26", "La pizarra del míster", "Lee la carta 26. Descarta 14, 15, 16, 17, 18, 19 y 20 y coge 24, 30 y 31. Las pistas del espía están repartidas entre las cartas 30 y 31."),
    ("app", "24", "La pizarra", "En el móvil: Acción, 24. Coloca a Los Rayos: portero 1, defensas 6 (izquierda) y 2 (derecha), medios 11 (izquierda) y 5 (derecha) y delantero 8. El mensaje te dice que cojas la 28.", "carta 28"),
    ("leer", "28", "La sala del VAR", "Lee la carta 28. Descarta 26, 30, 31 y 24 y coge 35, 40, 41, 42 y 46. Las cartas 22 y 35 son combinables. El reglamento está en la 42."),
    ("app", "46", "El veredicto del VAR", "En el móvil: Acción, 46. Jugada A: fuera de juego; B: gol válido; C: gol válido; D: fuera de juego. El mensaje te dice que cojas la 44.", "carta 44"),
    ("leer", "44", "El banquillo", "Lee la carta 44. Descarta 28, 40, 41, 42 y 46 y coge la 38, un silbato."),
    ("combinar", "22", "35", "El pase de prensa", "Las dos mitades del pase (22 y 35) son combinables: 22 + 35 = 57. Coge la 57."),
    ("leer", "57", "El pase de prensa", "Lee la carta 57. Descarta 22, 35 y 10 y coge 48, 52 y 53. La clasificación está en la 52 y los resultados conocidos en la 53."),
    ("app", "48", "El panel de la liguilla", f"En el móvil: Acción, 48. Marcadores que faltan: {_RES}. El mensaje te dice que cojas la 58.", "carta 58"),
    ("leer", "58", "El palco", "Lee la carta 58. Descarta 48, 52, 53 y 57 y coge la 56, el balón de la final."),
    ("combinar", "56", "38", "Balón y silbato", "El balón (56) y el silbato (38) son combinables: 56 + 38 = 94. Coge la 94."),
    ("leer", "94", "La tanda de penaltis", "Lee la carta 94. Descarta 56, 38, 44 y 58 y coge 69 y 70. La carta 70 es el informe del entrenador sobre el portero."),
    ("app", "69", "La tanda de penaltis", "En el móvil: Acción, 69. Chuta, por ejemplo, a derecha, izquierda, centro, derecha e izquierda (el portero se lanza según el penalti anterior). El mensaje te dice que cojas la 82.", "carta 82"),
    ("leer", "82", "La Copa de cristal", "Lee la carta 82. Descarta 69, 70 y 94 y coge la 62, el cristal de energía."),
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
