"""Game Over, 1985: La Última Moneda — versión de 60 cartas (22 oct 2026), mucho más difícil y variada.

Once puzles de tipos que no salen en ningún otro juego de la serie, con las pistas dibujadas o en acertijo (ninguna carta explica cómo se
resuelve su puzle): un circuito de puertas lógicas, un aparcamiento de naves (Rush Hour), un sprite comprimido por tandas, bytes en hexadecimal,
cuatro fantasmas (lógica), un cuadrado mágico 4 x 4, una tabla de récords por intercambios de vecinas, un puzle deslizante, una rana que cruza el
tráfico programando los pasos, monedas con cambio mínimo y el arranque final con la «o exclusiva» de cuatro bytes. Solo 16 cartas tienen a Cristina y
Alberto (escenas); el resto son objetos y pistas sin personas. Las cartas-pista las dibuja herramientas/arcade.py (instancias_arcade.py)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ampliacion as _amp  # noqa: E402
import instancias_arcade as I  # noqa: E402

ESTILO = ("Ilustración semirrealista con aire de película de ciencia ficción de los años 80 (como Tron y Stranger Things), luz de neón cian, magenta y amarilla "
          "sobre fondos oscuros, interior de una gigantesca máquina recreativa: circuitos, pantallas CRT con rayas de barrido, píxeles de colores flotando en el aire, "
          "cables luminosos y joysticks enormes, formato vertical 2:3. Sin texto, letras ni números legibles en la imagen (las pantallas muestran solo dibujos de píxeles). "
          "Deja libre de detalles importantes la esquina superior izquierda y el 18 % inferior de la imagen. "
          "Los personajes tienen siempre expresiones distintas y expresivas, adecuadas a la escena (nunca la misma cara en dos imágenes).")

PERSONAJES = {
    "Cristina": "Cristina, mujer de 26 años, profesora, pelo rubio y rizado recogido en una coleta alta a un lado con una cinta de colores, ojos azules. Viste ropa de los años 80: chaqueta vaquera con hombreras y las mangas remangadas, camiseta rosa neón, mallas negras con calentadores de colores y zapatillas altas.",
    "Alberto": "Alberto, hombre de 27 años, informático, pelo moreno corto, barba cuidada, ojos marrones. Viste ropa de los años 80: camiseta de rayas de colores, chaleco acolchado, vaqueros claros, gafas de sol de aviador subidas a la frente, riñonera y zapatillas deportivas.",
}

HOJA = ("Crea una hoja de personajes (character sheet) con las dos personas de la foto adjunta, de cuerpo entero y de frente, sobre fondo claro y neutro. "
        "Mantén su parecido real con la foto (cara, pelo, barba, ojos). "
        "Cristina: mujer de 26 años, profesora, pelo rubio y rizado recogido en una coleta alta a un lado con una cinta de colores, ojos azules, chaqueta vaquera con hombreras, camiseta rosa neón, mallas negras con calentadores de colores y zapatillas altas. "
        "Alberto: hombre de 27 años, informático, pelo moreno corto, barba cuidada, ojos marrones, camiseta de rayas de colores, chaleco acolchado, vaqueros claros, gafas de sol de aviador subidas a la frente, riñonera y zapatillas deportivas. "
        "Estilo: " + ESTILO)

FOTO = ("Antes de nada, adjunta a ChatGPT una foto de Cristina y Alberto juntos (o una de cada uno, con la cara bien visible). "
        "Pídele que mantenga el parecido real, pero con el estilo de ilustración de este juego.")

VIDEO = ("Crea un vídeo vertical 9:16 de 15 segundos, con estilo cinematográfico de ciencia ficción de los años 80, luces de neón cian, magenta y amarillo y mucho contraste. Sin ningún texto, letra ni subtítulo en pantalla. "
         "Escena 1 (0-4 s): en el salón de una casa actual, Cristina (mujer de 26 años, rubia de pelo rizado, ojos azules) y Alberto (hombre de 27 años, moreno con barba, ojos marrones) rodean un aparato de latón y cristal con un anillo central: el Cronoportal. Cristina señala una foto de un salón recreativo antiguo en una revista. "
         "Escena 2 (4-8 s): el anillo se enciende con un arco de luz azul y dorada y los dos son absorbidos por un túnel de luz. "
         "Escena 3 (8-12 s): caen en un salón recreativo de 1985, entre filas de máquinas encendidas, el aparato golpea una máquina y su cristal sale rodando hasta la ranura de las fichas; la pantalla se enciende y los absorbe. "
         "Escena 4 (12-15 s): primer plano de Cristina y Alberto, con ropa de los 80, asombrados, dentro de un mundo de píxeles de colores que se arma a su alrededor; fundido a negro. "
         "Sonido: zumbido eléctrico creciente, silbido del portal, sonidos de máquina recreativa (moneda, láser, 'ping') y música sintetizada de ocho bits, sin voz de narrador.")


ESTILO += " Los personajes tienen siempre expresiones distintas y expresivas, adecuadas a la escena (nunca la misma cara en dos imágenes)."
SIN_GENTE = "Sin ninguna persona en la imagen. "

MOSAICOS = {
    "aparcamiento": dict(filas=2, cols=1, cartas=["19", "21"], titulo="El aparcamiento de naves"),
    "record": dict(filas=2, cols=1, cartas=["61", "63"], titulo="La tabla de récords"),
    "deslizante": dict(filas=2, cols=1, cartas=["66", "67"], titulo="El dibujo final"),
}
POS = {(2, 1): ["mitad de arriba", "mitad de abajo"], (1, 2): ["mitad izquierda", "mitad derecha"]}
_NOM = ["rojo", "cian", "verde", "amarillo", "rosa", "naranja", "violeta", "blanco"]


def _ruta_atasco():
    partes, ult, n = [], None, 0
    for i, d in I.ATASCO["ruta"]:
        hor = I.ATASCO["naves"][i][3]
        mov = (f"nave {i + 1} " + (("a la derecha" if d > 0 else "a la izquierda") if hor else ("hacia abajo" if d > 0 else "hacia arriba")))
        if mov == ult:
            n += 1
        else:
            if ult:
                partes.append(ult + (f" ({n} casillas)" if n > 1 else ""))
            ult, n = mov, 1
    partes.append(ult + (f" ({n} casillas)" if n > 1 else ""))
    return "; ".join(partes)


_S_CIR = "interruptores arriba (1): " + ", ".join("ABCDEF"[i] for i, v in enumerate(I.CIRCUITO["solucion"]) if v) + "; abajo (0): " + ", ".join("ABCDEF"[i] for i, v in enumerate(I.CIRCUITO["solucion"]) if not v)
_S_ATA = _ruta_atasco()
_S_SPR = " / ".join("".join("#" if v else "." for v in f) for f in I.SPRITE_D["pixeles"])
_S_ASC = I.ASCII["claro"]
_S_FAN = "; ".join(f"pasillo {s['pasillo']}: fantasma {s['fantasma']}, {s['velocidad']}, fruta {s['fruta']}" for s in sorted(I.FANTASMAS["solucion"], key=lambda s: s["pasillo"]))
_S_MAG = " / ".join(" ".join(str(v) for v in f) for f in I.MAGICO["solucion"])
_S_RAN = ", ".join(_NOM[i] for i in sorted(range(8), key=lambda i: I.RANKING["puntos"][i]))
_S_DES = " / ".join(" ".join(str(v) if v else "_" for v in f) for f in I.DESLIZANTE["objetivo"])
_S_RANA = I.RANA["solucion"]
_S_MON = " y ".join(f"{n} de {v}" for n, v in zip(I.MONEDAS["solucion"], I.MONEDAS["monedas"]) if n)
_S_XOR = f"{I.BYTES['14']} ^ {I.BYTES['52']} ^ {I.BYTES['40']} ^ {I.BYTES['69']} = {I.RESULTADO}"


def codigo(que):
    return f"Carta dibujada por código (herramientas/arcade.py; no se pide a ChatGPT): {que}."


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
    # ------------------------------------------------------------------ La placa base
    "P": escena("P", "Llegada a la recreativa", [10, 12], [],
                "Octava parada del Cronoportal: un salón recreativo de 1985. Cristina lleva años con ganas de jugar a los clásicos en sus máquinas originales. El salto vuelve a salir mal: el aparato choca contra una máquina, su cristal sale rodando hasta la ranura de las fichas y desaparece dentro. La pantalla se enciende con un parpadeo y os absorbe: estáis DENTRO de la máquina, entre circuitos gigantes, y en el cielo de píxeles se enciende una cuenta atrás de cien minutos. Alberto lo tiene claro: si la máquina se apaga, os apagáis con ella.",
                ["Mirad a vuestro alrededor y revisad el aparato."],
                "El interior de una gigantesca máquina recreativa de 1985, con circuitos enormes, cables luminosos y pantallas CRT con rayas de barrido, bajo un cielo de píxeles de colores. En primer plano, un aparato de latón y cristal (el Cronoportal) humea sin su cristal central. Cristina, con chaqueta vaquera con hombreras y camiseta rosa neón, mira alrededor con la boca abierta de asombro; Alberto, con chaleco acolchado y gafas de aviador en la frente, frunce el ceño con preocupación."),
    "10": escena("10", "La placa base", [14, 16, 18, 19, 20, 21, 22], ["P"],
                 "Estáis sobre una placa base gigante. A un lado, un panel con seis interruptores unidos por puertas lógicas a dos lámparas (carta 14) y su esquema grabado en el cobre (carta 16). Al otro, un aparcamiento de naves de píxeles atascado: lo que pintó el programador en el suelo (carta 18) y el plano del tablero, que ocupa dos láminas, así que juntad la 19 arriba y la 21 abajo (carta 20). En un rincón, el mango de un joystick de tamaño humano (carta 22).",
                 ["Hay dos puzles: el panel de interruptores y el aparcamiento de naves.", "El aparcamiento son dos cartas: juntadlas, una encima de otra."],
                 "Una placa base enorme vista desde arriba, con pistas de cobre luminosas, un panel con seis interruptores grandes unidos por cables a dos lámparas, y más allá un aparcamiento de pequeñas naves de píxeles de colores todas atascadas; en un rincón, el mango de un joystick gigante. Cristina toca los interruptores con una ceja arqueada de curiosidad; Alberto señala el aparcamiento, boquiabierto de sorpresa."),
    "12": combinable("12", "Cronoportal sin cristal", "azul", 62, 74,
                     "El Cronoportal con el anillo central apagado: le falta el cristal que se tragó la ranura de las fichas.",
                     SIN_GENTE + "Primer plano del Cronoportal: una consola portátil de latón y cristal con dos antenas de cobre, un anillo central apagado y un hueco circular vacío en el pecho del aparato, sobre una placa de circuitos con luces de neón."),
    "14": app("14", "El panel de interruptores", "Es un juego de la app: seis interruptores unidos por puertas lógicas a dos lámparas; hay que dejarlas como pide el esquema de la carta 16.", 24,
              ["El esquema de la carta 16 dice cómo están unidas las puertas. Hay que dejar la lámpara X encendida y la Y apagada.", "Empezad por las puertas del final (la 6 y la 7) y retroceded: ¿qué tienen que valer sus entradas?", f"Solución: {_S_CIR}. Byte de la máquina: {I.BYTES['14']}."],
              SIN_GENTE + "Un panel de control de neón con seis grandes interruptores de palanca, cables de colores que se juntan en cajas con símbolos de puertas lógicas y dos lámparas redondas al final, sobre una placa base luminosa."),
    "16": gris("16", "El circuito de la placa", "El esquema grabado en el cobre de la placa: cómo se unen los seis interruptores, las siete puertas y las dos lámparas.",
               ["Es el esquema del panel de interruptores (carta 14).", "Cada puerta mira sus dos entradas y decide su salida. Los cables llevan un color por origen.", "Lámpara X encendida y lámpara Y apagada."]),
    "18": gris("18", "El acertijo del aparcamiento", "Un acertijo pintado en el suelo por el programador.",
               ["Es la regla del aparcamiento de naves (carta 20).", "Las naves solo avanzan y retroceden por donde apuntan.", "La nave 1, la roja, es la que tiene que salir por la derecha."]),
    "19": pieza("19", "aparcamiento", "Media lámina del aparcamiento de naves.", ["Es la mitad de una lámina: juntadla con la carta 21.", "Cada nave lleva su número.", "La puerta de salida está a la derecha."]),
    "21": pieza("21", "aparcamiento", "Media lámina del aparcamiento de naves.", ["Es la mitad de una lámina: juntadla con la carta 19.", "Cada nave lleva su número.", "La puerta de salida está a la derecha."]),
    "20": app("20", "El aparcamiento de naves", "Es un juego de la app: un aparcamiento de naves de píxeles; hay que sacar la nave 1 por la puerta de la derecha moviendo las demás.", 28,
              ["El plano está en las cartas 19 y 21, y la regla en la 18.", "Hay que ir moviendo las naves que bloquean el camino de la nave 1; algunas hay que apartarlas dos veces.", f"Una solución en {I.ATASCO['minimo']} movimientos: {_S_ATA}."],
              SIN_GENTE + "Un aparcamiento de naves espaciales de píxeles de colores, aparcadas muy juntas en una cuadrícula de neón, con una salida iluminada en un lado, sobre una placa base."),
    "22": combinable("22", "Mango de joystick", "azul", 35, 57, "Un mango de joystick de tamaño humano, de plástico negro, sin bola en la punta.",
                     SIN_GENTE + "Un joystick gigante de recreativa de los 80, con la base y el mango negros, sin la bola roja de la punta, sobre una placa de circuitos con luces de neón."),
    "24": escena("24", "La placa se enciende", [26], [14, 16],
                 "Las dos lámparas se encienden como dictaba el esquema y la placa empieza a zumbar: un panel se abre y deja ver una nota de papel, pegada con cinta por el programador (carta 26), que habla de cómo ordena la máquina sus récords. Un número parpadea en la pantalla del panel: guardadlo, lo pedirá el arranque.",
                 ["Mirad el panel que se ha abierto."],
                 "Un panel de una placa base que se abre hacia fuera con un destello, dejando ver una nota de papel pegada con cinta adhesiva, bajo dos lámparas redondas encendidas. Cristina, con una sonrisa de triunfo, levanta el puño; Alberto, con las gafas de aviador en la frente, mira la nota con curiosidad."),
    "26": gris("26", "La nota del programador", "Una nota de papel pegada por el programador: cómo ordena la máquina su tabla de récords.",
               ["Habla de cómo se puede reordenar la tabla (carta 51).", "Solo se pueden cambiar dos entradas vecinas, y hay un máximo de cambios.", "Los puntos de cada entrada están en la tabla de las cartas 61 y 63."]),
    "28": escena("28", "El aparcamiento despejado", [35], [18, 19, 20, 21],
                 "La nave roja sale disparada por la puerta y el aparcamiento se despeja. Entre dos plazas, un reflejo rojo: la bola del joystick (carta 35), que se había caído de la nave.",
                 ["Mirad entre las plazas del aparcamiento."],
                 "Un aparcamiento de naves de píxeles ya casi vacío, con una nave roja desapareciendo por una puerta iluminada al fondo y, entre dos plazas, una gran bola roja de joystick brillando. Cristina la recoge con cara de asombro y los ojos muy abiertos; Alberto sonríe aliviado con los pulgares arriba."),
    "35": combinable("35", "Bola del joystick", "roja", 22, 57, "Una bola roja de joystick, brillante, con la rosca de la base al aire.",
                     SIN_GENTE + "Una bola roja brillante de joystick de recreativa con una rosca metálica en la base, sobre una placa de circuitos con luces de neón."),
    "57": escena("57", "El joystick gigante", [31, 32], [22, 35, 10, 28],
                 "Enroscáis la bola en el mango y el joystick gigante cobra vida: al empujarlo, la placa se divide en dos pasillos. A la izquierda, el taller de sprites, donde se dibujan los personajes del juego (carta 31). A la derecha, la consola de mensajes de la máquina (carta 32).",
                 ["Dos pasillos: el taller de sprites y la consola de mensajes."],
                 "Un joystick gigante de recreativa con una bola roja, inclinado hacia delante, y delante de él una placa base que se abre en dos pasillos de neón: a la izquierda uno con pantallas de píxeles y a la derecha otro con una consola con una pantalla negra. Cristina tira del joystick con los dientes apretados por el esfuerzo; Alberto, detrás, la sujeta riendo."),
    # ------------------------------------------------------------------ Rama 1: el taller de sprites
    "31": escena("31", "El taller de sprites", [40, 41, 43, 45], [],
                 "Una pantalla enorme, apagada, con una rejilla de doce por doce casillas (carta 40). En el suelo, dos tiras de papel con las tandas de casillas del dibujo, fila por fila (cartas 41 y 43), y una nota con la regla de la compresión (carta 45).",
                 ["Un único puzle: dibujar un sprite que está comprimido."],
                 "Un taller de dibujo de píxeles dentro de una máquina recreativa: una pantalla enorme con una rejilla de casillas apagadas, tiras de papel con hileras de cifras en el suelo y pinceles de luz. Cristina examina una tira con la cabeza ladeada; Alberto se rasca la barbilla pensando."),
    "40": app("40", "La pantalla de sprites", "Es un juego de la app: dibujar en una rejilla de doce por doce casillas el sprite que describen las tandas de las cartas 41 y 43.", 30,
              ["Las tandas están en las cartas 41 y 43 y la regla de la compresión, en la 45.", "Cada fila se cuenta de izquierda a derecha, alternando casillas apagadas y encendidas, empezando por las apagadas.", f"El dibujo es un fantasmita, fila por fila ('#' encendida): {_S_SPR}. Byte de la máquina: {I.BYTES['40']}."],
              SIN_GENTE + "Una pantalla enorme de recreativa con una rejilla de casillas de píxeles en la que se dibuja un sprite de colores, con cables luminosos y reflejos de neón."),
    "41": gris("41", "Las tandas del sprite (I)", "Las tandas de casillas de las filas 1 a 6 del sprite.",
               ["Cada fila del dibujo mide doce casillas.", "Las tandas se cuentan de izquierda a derecha: primero apagadas, luego encendidas, y así.", "Si una fila empieza por casillas encendidas, el primer número es un cero."]),
    "43": gris("43", "Las tandas del sprite (II)", "Las tandas de casillas de las filas 7 a 12 del sprite.",
               ["Cada fila del dibujo mide doce casillas.", "Las tandas se cuentan de izquierda a derecha: primero apagadas, luego encendidas, y así.", "La última fila no tiene ceros al principio: empieza por una tanda de apagadas o de encendidas."]),
    "45": gris("45", "La regla de la compresión", "Una nota con la regla de la compresión de los sprites.",
               ["Explica cómo leer las tandas de las cartas 41 y 43.", "Las tandas alternan apagadas y encendidas.", "Empiezan siempre por las apagadas."]),
    "30": escena("30", "El sprite aprobado", [38], [31, 40, 41, 43, 45],
                 "El fantasmita cobra vida, hace una reverencia y se desvanece; la pantalla del taller escupe una pieza de metal: la mitad de una llave en forma de moneda (carta 38). Otro número parpadea en la pantalla del taller: guardadlo también.",
                 ["Mirad lo que ha escupido la pantalla."],
                 "Una pantalla gigante en la que un fantasmita de píxeles amarillos se despide con una reverencia y, en una bandeja de metal debajo, una mitad de llave con forma de moneda dorada. Cristina aplaude con los ojos brillantes; Alberto se ríe a carcajadas."),
    "38": combinable("38", "Mitad de la llave del jefe", "roja", 56, 94, "Una mitad de una llave dorada con forma de ficha de recreativa.",
                     SIN_GENTE + "La mitad izquierda de una llave dorada con forma de ficha de recreativa con ranuras, sobre una bandeja de metal con luces de neón."),
    # ------------------------------------------------------------------ Rama 2: la consola de mensajes
    "32": escena("32", "La consola de mensajes", [42, 48, 49, 53], [],
                 "Una consola con una pantalla negra y un cursor parpadeante: espera un mensaje (carta 48). Junto a ella, una pantalla pequeña con ocho bytes en hexadecimal (carta 42), la tabla de caracteres de la máquina (carta 49) y una nota con la regla de los bytes (carta 53).",
                 ["Un único puzle: leer un mensaje escrito en bytes."],
                 "Una consola antigua de ordenador con una gran pantalla negra y un cursor verde parpadeante, junto a una tira de papel de impresora con hileras de pares de símbolos. Cristina tamborilea con los dedos en la consola mirando la pantalla; Alberto, con el ceño fruncido, sigue la tira con el dedo."),
    "48": app("48", "La consola de mensajes", "Es un juego de la app: escribir el mensaje de la pantalla, que está en ocho bytes (carta 42) y se lee con la tabla de la carta 49.", 36,
              ["Los bytes están en la carta 42, la tabla en la 49 y la regla en la 53.", "Cada byte son dos cifras en base dieciséis; la tabla dice qué letra es cada uno.", f"El mensaje es {_S_ASC}."],
              SIN_GENTE + "Una consola de ordenador antigua con una pantalla negra de letras verdes, un teclado grande y una tira de papel de impresora, dentro de una placa base de neón."),
    "42": gris("42", "Los bytes del mensaje", "La pantalla pequeña de la consola, con los ocho bytes del mensaje en hexadecimal.",
               ["Son ocho bytes: ocho letras.", "Se leen de izquierda a derecha y de arriba abajo.", "Cada byte son dos cifras en base dieciséis."]),
    "49": gris("49", "La tabla de caracteres", "La tabla de caracteres de la máquina: cada letra con su byte.",
               ["Sirve para traducir los bytes de la carta 42 a letras.", "Es una tabla de A a Z.", "Cada letra tiene un byte de dos cifras."]),
    "53": gris("53", "La regla de los bytes", "Una nota con la regla de los bytes en hexadecimal.",
               ["Explica cómo se escribe un byte.", "Cada byte son dos cifras en base dieciséis: del 0 al 9 y de la A a la F.", "La tabla de la carta 49 hace el resto."]),
    "36": escena("36", "El menú de los fantasmas", [52, 54, 55, 59], [32, 42, 48, 49, 53],
                 "El mensaje desbloquea el menú de la máquina: cuatro fantasmas, uno por pasillo, patrullan una sala de neón, cada uno a su velocidad y persiguiendo su fruta. Alberto comprueba el panel (carta 52). En un cartel están las pistas del guardián, en dos tiras (cartas 54 y 55), y el plano de los cuatro pasillos (carta 59).",
                 ["Un único puzle: averiguar qué fantasma patrulla cada pasillo."],
                 "Una sala de neón con cuatro pasillos paralelos y un fantasma de píxeles distinto en cada uno (rojo, rosa, cian y naranja), con frutas flotando sobre ellos, y un cartel con tiras de papel con pistas. Cristina señala a los fantasmas con los ojos muy abiertos y una gran sonrisa; Alberto se tapa la boca para disimular la risa."),
    "52": app("52", "Los cuatro fantasmas", "Es un juego de la app: averiguar qué fantasma patrulla cada pasillo, a qué velocidad y qué fruta persigue.", 44,
              ["Las pistas están en las cartas 54 y 55 y el plano de los pasillos en la 59.", "Empezad por las pistas que sitúan a un fantasma en un extremo o junto a otro; vais llenando el plano.", f"Solución: {_S_FAN}. Byte de la máquina: {I.BYTES['52']}."],
              SIN_GENTE + "Una sala de neón con cuatro pasillos y un fantasma de píxeles distinto en cada uno, rojo, rosa, cian y naranja, con frutas flotando sobre ellos y un panel de control con cuatro columnas."),
    "54": gris("54", "Las pistas de los fantasmas (I)", "La primera tira de pistas del guardián de la sala.", ["Son las primeras pistas sobre los fantasmas.", "Cada frase compara a dos fantasmas.", "Las frases con «izquierda» se leen de izquierda a derecha del plano."]),
    "55": gris("55", "Las pistas de los fantasmas (II)", "La segunda tira de pistas del guardián de la sala.", ["Son las últimas pistas sobre los fantasmas.", "Hacen falta todas las frases juntas.", "Las frases con «izquierda» se leen de izquierda a derecha del plano."]),
    "59": gris("59", "El plano de los pasillos", "El plano de la sala: cuatro pasillos, de izquierda a derecha, y cuatro fantasmas, cuatro velocidades y cuatro frutas.", ["Son cuatro pasillos numerados de izquierda a derecha.", "Cada pasillo tiene un fantasma, una velocidad y una fruta, todos distintos.", "Los extremos son el pasillo 1 y el pasillo 4."]),
    # ------------------------------------------------------------------ El marcador y las salas del jefe
    "44": escena("44", "La sala de puntuaciones", [33, 37, 39, 46, 51, 61, 63], [36, 52, 54, 55, 59],
                 "Los fantasmas se retiran y se abre la sala de puntuaciones del jefe. Un marcador gigante con dieciséis casillas, la mayoría vacías (carta 46), con seis números ya puestos (carta 37), una nota con la regla de la suma (carta 39) y una bolsa de fichas (carta 33). Al fondo, una tabla de récords desordenada (carta 51) que ocupa dos láminas: juntad la 61 arriba y la 63 abajo.",
                 ["Hay dos puzles: el marcador y la tabla de récords."],
                 "Una sala enorme de neón con un marcador gigante de dieciséis casillas en la pared, una bolsa de fichas numeradas en el suelo y, al fondo, una tabla de récords con barras de colores desordenadas. Cristina cuenta con los dedos mirando el marcador; Alberto, boquiabierto, señala la tabla de récords."),
    "46": app("46", "El marcador del jefe", "Es un juego de la app: rellenar con los números del 1 al 16 un marcador de cuatro por cuatro para que todas las filas, columnas y diagonales sumen lo mismo.", 56,
              ["Los seis números puestos, en la carta 37; la regla de la suma, en la 39; las fichas que faltan, en la 33.", "Cada fila, cada columna y las dos diagonales suman 34. Empezad por una línea con tres números ya puestos.", f"Solución, fila por fila: {_S_MAG}."],
              SIN_GENTE + "Un marcador gigante de recreativa con una cuadrícula de cuatro por cuatro casillas numeradas con luces de neón, en una sala oscura con cables luminosos."),
    "37": gris("37", "El marcador del jefe", "El marcador con seis de sus dieciséis casillas ya rellenas.", ["Son seis números ya puestos del marcador (carta 46).", "Ni una casilla de las vacías tiene nada puesto.", "La regla de la suma, en la carta 39."]),
    "39": gris("39", "La regla del marcador", "La regla grabada en la carcasa del marcador.", ["Dice cuánto suma cada fila, columna y diagonal.", "Los números van del 1 al 16, una vez cada uno.", "Todas las líneas suman treinta y cuatro."]),
    "33": gris("33", "Las fichas de la bolsa", "Las fichas que aún no están en el marcador.", ["Son las fichas que faltan en el marcador (carta 46).", "Coinciden con los números que no están puestos en la carta 37.", "Cada ficha se usa una sola vez."]),
    "56": combinable("56", "Otra mitad de la llave", "roja", 38, 94, "La otra mitad de la llave del jefe, con forma de ficha de recreativa, que escupe el marcador al encenderse.",
                     SIN_GENTE + "La mitad derecha de una llave dorada con forma de ficha de recreativa con ranuras, que sale de la boca de un marcador gigante, con luces de neón."),
    "51": app("51", "La tabla de récords", "Es un juego de la app: ordenar la tabla de récords de menos a más puntos cambiando solo entradas vecinas, con un máximo de cambios.", 58,
              ["La regla está en la carta 26 y los puntos de cada entrada, en las cartas 61 y 63.", "Cada cambio solo mueve una entrada un puesto. Pensad en cuántos cambios hacen falta para colocar cada una.", f"De arriba abajo, los colores en este orden: {_S_RAN}."],
              SIN_GENTE + "Una tabla de récords de recreativa con ocho barras de colores de distinto largo apiladas, en desorden, con una pantalla negra detrás y luces de neón."),
    "61": pieza("61", "record", "Media lámina de la tabla de récords.", ["Es la mitad de una lámina: juntadla con la carta 63.", "Cada color tiene su puntuación.", "Los puntos de la tabla se usan para ordenar los bloques de la carta 51."]),
    "63": pieza("63", "record", "Media lámina de la tabla de récords.", ["Es la mitad de una lámina: juntadla con la carta 61.", "Cada color tiene su puntuación.", "Los puntos de la tabla se usan para ordenar los bloques de la carta 51."]),
    "58": escena("58", "La ranura de los récords", [69, 70, 71], [51, 61, 63, 26, 24],
                 "La tabla de récords se ordena y de su hueco sale un pasillo con una autopista de ocho carriles: el nivel de la rana. Cruzarla requiere programar los pasos de antemano (carta 69). En el arcén, la foto de la autopista tal y como está al empezar (carta 70) y las velocidades de cada carril (carta 71).",
                 ["Un único puzle: programar el cruce de la rana."],
                 "Una autopista de neón de cinco carriles con coches de colores de píxeles que pasan a distinta velocidad, con una rana verde de píxeles esperando en el arcén. Cristina, de rodillas, mira los coches con las manos en la cabeza; Alberto, con los brazos cruzados, calcula con los ojos entrecerrados."),
    "69": app("69", "La rana de la autopista", "Es un juego de la app: programar los pasos de una rana (arriba, izquierda, derecha o esperar) para cruzar cinco carriles de tráfico sin que la atropellen.", 80,
              ["La autopista al empezar está en la carta 70 y las velocidades de los carriles, en la 71.", "En cada turno la rana se mueve primero y luego los coches. Solo cuenta dónde están los coches al final del turno. Los coches que se salen por un lado entran por el otro.", f"Una solución en {I.RANA['minimo']} turnos: {_S_RANA}. Byte de la máquina: {I.BYTES['69']}."],
              SIN_GENTE + "Una autopista de neón de cinco carriles con coches de píxeles de colores y una rana verde de píxeles al borde, sobre una placa base luminosa."),
    "70": gris("70", "La autopista al empezar", "Una foto de la autopista al empezar el nivel.", ["Muestra la posición de los coches y de la rana en el turno cero.", "Los números de la izquierda son los carriles.", "La rana empieza en la fila de abajo."]),
    "71": gris("71", "Las velocidades del tráfico", "Cuántas casillas avanza cada carril por turno, y hacia dónde.", ["Cada flecha es una casilla por turno.", "Los coches que se salen por un lado entran por el otro.", "En cada turno la rana se mueve primero y luego se mueven los coches."]),
    "80": escena("80", "El almacén de monedas", [72, 75, 79], [58, 69, 70, 71],
                 "La rana cruza y se queda esperando al otro lado, dando saltitos. Detrás de ella, el almacén de monedas de la máquina: una máquina de cambio con cuatro ranuras, cada una con su moneda (carta 72). Los valores de las monedas, en un cartel (carta 75), y el precio de la partida y la regla de la máquina, en la pantalla de continuar (carta 79).",
                 ["Un único puzle: pagar justo con las menos monedas."],
                 "Un almacén de neón con una máquina de cambio con cuatro ranuras de monedas de distinto tamaño y colores, una pantalla con un precio y montones de monedas doradas en el suelo. Cristina sostiene una moneda a la luz con los ojos entrecerrados, calculando; Alberto se pone las manos en la cintura con cara de satisfacción."),
    "72": app("72", "La máquina de cambio", "Es un juego de la app: pagar el precio exacto de la partida con la máquina de cambio, usando las menos monedas posibles, con cuatro clases de moneda.", 82,
              ["Los valores de las monedas están en la carta 75 y el precio, en la 79.", "La máquina no da cambio. No sirve echar siempre la moneda mayor que quepa: hay un pago con menos monedas.", f"Solución: {_S_MON} (cuatro monedas en total)."],
              SIN_GENTE + "Una máquina de cambio de recreativa con cuatro ranuras de monedas de distinto tamaño y colores y una pantalla con luces de neón, con monedas doradas apiladas en el suelo."),
    "75": gris("75", "Las monedas de la máquina", "Las cuatro clases de moneda de la máquina de cambio, con su valor.", ["Son cuatro monedas distintas, de la menor a la mayor.", "De cada clase hay cuantas se quiera.", "El precio de la partida está en la carta 79."]),
    "79": gris("79", "El precio de la partida", "La pantalla de continuar: el precio de la partida y la regla de la máquina.", ["Dice cuánto hay que pagar.", "La máquina no da cambio: se paga justo.", "Hay que pagarlo con el menor número posible de monedas."]),
    "82": escena("82", "La ranura de continuar", [85, 86, 87], [80, 72, 75, 79],
                 "La máquina de cambio escupe una ficha de continuar y, con ella, se abre la puerta del núcleo de la máquina: el arranque. Cristina lee en una pantalla: «Introduce la clave». La clave es la combinación de cuatro números que os dejaron los puzles del panel, los fantasmas, el taller de sprites y la rana (carta 85). Dos láminas explican cómo se combinan (cartas 86 y 87).",
                 ["Un único puzle: arrancar la máquina con la clave."],
                 "La sala del núcleo de una máquina recreativa, con un panel con cuatro ranuras, una pantalla negra con un cursor parpadeante y una gran palanca de arranque, con cables luminosos de neón por todas partes. Cristina, con una ficha en la mano, mira la pantalla con los labios apretados; Alberto, a su lado, se muerde el labio pensativo."),
    "85": app("85", "El arranque de la máquina", "Es un juego de la app: la clave de arranque sale de combinar con la «o exclusiva» los cuatro números que os dejaron los puzles del panel, los fantasmas, el taller de sprites y la rana.", 99,
              ["Los números que anotasteis: el del panel de interruptores, el de los fantasmas, el del taller de sprites y el de la rana. Las reglas, en las cartas 86 y 87.", "La «o exclusiva» se aplica cifra a cifra, con los números en binario: 0 y 0 da 0, 1 y 1 da 0, y 0 y 1 (o 1 y 0) da 1.", f"Los bytes son {I.BYTES['14']}, {I.BYTES['52']}, {I.BYTES['40']} y {I.BYTES['69']}: {_S_XOR}."],
              SIN_GENTE + "Un panel de arranque de una máquina recreativa con cuatro ranuras para números, una gran palanca de arranque y una pantalla con un cursor parpadeante, con cables luminosos de neón."),
    "86": gris("86", "La clave del arranque (I)", "Una nota del programador: de dónde sale cada número de la clave (primera parte).", ["Explica los dos primeros números de la clave.", "Hay que combinar los cuatro números con la «o exclusiva».", "El orden en que se combinan no importa."]),
    "87": gris("87", "La clave del arranque (II)", "Una nota del programador: los otros dos números, y la tabla de la «o exclusiva».", ["Explica los otros dos números de la clave.", "La tabla de la «o exclusiva» dice qué da cada pareja de cifras.", "Se aplica cifra a cifra, con los números en binario."]),
    # ------------------------------------------------------------------ La sala del jefe y el final
    "94": escena("94", "La sala del jefe final", [64, 66, 67], [38, 56, 30, 44, 33, 37, 39, 46],
                 "Las dos mitades encajan: la llave del jefe, una ficha dorada completa, abre la sala del jefe final. En el centro, un tablero deslizante de nueve casillas con una ficha menos (carta 64) cierra el cerrojo. El dibujo final que tiene que formar ocupa dos láminas: juntad la 66 arriba y la 67 abajo.",
                 ["Un único puzle: el puzle deslizante."],
                 "Una sala enorme con un tablero deslizante gigante de nueve casillas, con ocho fichas de colores numeradas y un hueco, que sirve de cerrojo de una puerta dorada, bajo luces de neón. Cristina, de puntillas, estudia el tablero con la lengua entre los dientes; Alberto, a su lado, levanta las cejas sorprendido."),
    "64": app("64", "El cerrojo deslizante", "Es un juego de la app: un tablero de tres por tres casillas con un hueco; hay que deslizar las fichas hasta formar el dibujo final.", 62,
              ["El dibujo final, en las cartas 66 y 67 (dos mitades).", "Colocad primero la fila de arriba y luego bajad a las otras dos; las últimas fichas son las más difíciles.", f"El dibujo final, fila por fila: {_S_DES}."],
              SIN_GENTE + "Un tablero deslizante gigante de nueve casillas con ocho fichas de colores numeradas y un hueco, sobre un cerrojo dorado, con luces de neón."),
    "66": pieza("66", "deslizante", "Media lámina del dibujo final del cerrojo.", ["Es la mitad de una lámina: juntadla con la carta 67.", "Muestra cómo tienen que quedar las ocho fichas.", "El hueco va en el centro."]),
    "67": pieza("67", "deslizante", "Media lámina del dibujo final del cerrojo.", ["Es la mitad de una lámina: juntadla con la carta 66.", "Muestra cómo tienen que quedar las ocho fichas.", "El hueco va en el centro."]),
    "62": combinable("62", "El cristal del Cronoportal", "roja", 12, 74, "El cristal del Cronoportal, que el cerrojo escupe al abrirse: se tragó la ranura de las fichas y acabó escondido en la sala del jefe.",
                     SIN_GENTE + "Un cristal redondo de color azul brillante, del tamaño de una ficha de recreativa, con destellos de luz, sobre una bandeja metálica con luces de neón."),
    "74": escena("74", "Cronoportal con el cristal", [], [62, 12, 64, 66, 67, 94, 57],
                 "Encajáis el cristal en el pecho del Cronoportal y el anillo se enciende con un arco de luz azul: la cuenta atrás se detiene en seguida. Solo falta la clave para arrancar la máquina y abrir la salida: cuatro números combinados con la «o exclusiva» (carta 85).",
                 ["Ya solo queda arrancar la máquina."],
                 "Cristina y Alberto encajan un cristal azul brillante en el hueco del Cronoportal, un aparato de latón y cristal con un anillo central que se enciende con un arco de luz azul, entre circuitos gigantes de neón. Cristina lo sostiene con las dos manos con una enorme sonrisa; Alberto contiene el aliento, mirando el anillo con la boca abierta."),
    "99": escena("99", "De vuelta a casa (FIN)", [], [74, 82, 85, 86, 87],
                 "La clave activa el arranque: la máquina arranca con un chasquido, la pantalla enseña «GAME OVER» y, al instante, una moneda enorme cae por la ranura y abre el portal. Cristina se despide del fantasmita con la mano. Aterrizáis en vuestro salón. Alberto mira el aparato: «Mañana, otro destino». Cristina sonríe. FIN.",
                 [],
                 "La escena ocurre DENTRO del salón de su casa actual, en el presente (sofá, estanterías con libros, plantas, una lámpara encendida y luz cálida de tarde por la ventana): acaban de VOLVER a casa. Cristina y Alberto acaban de salir de un portal circular de luz azul y magenta que se abre detrás de ellos; a través del portal todavía se ven el interior de una máquina recreativa y una gran moneda dorada cayendo. Llevan aún la ropa de los años 80. Cristina sonríe, Alberto dice «Mañana, otro destino»; el Cronoportal humea sobre la mesa."),
}

META = dict(juego="Game Over, 1985 — La Última Moneda", estilo=ESTILO, personajes=PERSONAJES, hoja=HOJA, foto=FOTO, video=VIDEO,
            mosaicos={k: dict(filas=m["filas"], cols=m["cols"], cartas=m["cartas"], titulo=m["titulo"]) for k, m in MOSAICOS.items()})

SPEC = dict(final="99", needs={
    "24": ["14", "16"], "28": ["20", "18", "19", "21"], "57": ["22", "35"], "30": ["40", "41", "43", "45"], "36": ["48", "42", "49", "53"],
    "44": ["52", "54", "55", "59"], "56": ["46", "37", "39", "33"], "58": ["51", "26", "61", "63"], "80": ["69", "70", "71"], "94": ["38", "56"],
    "62": ["64", "66", "67"], "82": ["72", "75", "79"], "74": ["12", "62"], "99": ["85", "86", "87", "74"]}, eventos={})

PARA_QUE = {k: c["titulo"].split("— ", 1)[1] for k, c in J.items()}

_T = [
    ("leer", "P", "Llegada", "Pon el Modo PC (solo la P en la mesa) y en el móvil pulsa Empezar. Lee la carta P: coge la 10 y la 12."),
    ("leer", "10", "La placa base", "Lee la carta 10. Descarta la P y coge 14, 16, 18, 19, 20, 21 y 22. Junta el aparcamiento: 19 arriba y 21 abajo."),
    ("app", "14", "El panel de interruptores", f"En el móvil: Acción, 14. Con el esquema (16): {_S_CIR}. El mensaje te dice que cojas la 24. Anota el byte de la máquina: {I.BYTES['14']}.", "carta 24"),
    ("leer", "24", "La placa se enciende", "Lee la carta 24. Descarta 14 y 16 y coge la 26 (guárdala para la tabla de récords)."),
    ("app", "20", "El aparcamiento de naves", f"En el móvil: Acción, 20. Con el plano (19 y 21) y el acertijo (18), saca la nave 1 en {I.ATASCO['minimo']} movimientos: {_S_ATA}. El mensaje te dice que cojas la 28.", "carta 28"),
    ("leer", "28", "El aparcamiento despejado", "Lee la carta 28. Descarta 18, 19, 20 y 21 y coge la 35."),
    ("combinar", "22", "35", "El joystick", "El mango (22) y la bola (35) son combinables: 22 + 35 = 57. Coge la 57."),
    ("leer", "57", "El joystick gigante", "Lee la carta 57. Descarta 22, 35, 10 y 28 y coge 31 y 32."),
    ("leer", "31", "El taller de sprites", "Lee la carta 31. Coge 40, 41, 43 y 45."),
    ("app", "40", "La pantalla de sprites", f"En el móvil: Acción, 40. Con las tandas (41 y 43) y la regla (45), el fantasmita fila por fila ('#' encendida): {_S_SPR}. El mensaje te dice que cojas la 30. Anota el byte de la máquina: {I.BYTES['40']}.", "carta 30"),
    ("leer", "30", "El sprite aprobado", "Lee la carta 30. Descarta 31, 40, 41, 43 y 45 y coge la 38."),
    ("leer", "32", "La consola de mensajes", "Lee la carta 32. Coge 42, 48, 49 y 53."),
    ("app", "48", "La consola de mensajes", f"En el móvil: Acción, 48. Con los bytes (42), la tabla (49) y la regla (53), el mensaje es {_S_ASC}. El mensaje te dice que cojas la 36.", "carta 36"),
    ("leer", "36", "El menú de los fantasmas", "Lee la carta 36. Descarta 32, 42, 48, 49 y 53 y coge 52, 54, 55 y 59."),
    ("app", "52", "Los cuatro fantasmas", f"En el móvil: Acción, 52. Con las pistas (54 y 55) y el plano (59): {_S_FAN}. El mensaje te dice que cojas la 44. Anota el byte de la máquina: {I.BYTES['52']}.", "carta 44"),
    ("leer", "44", "La sala de puntuaciones", "Lee la carta 44. Descarta 36, 52, 54, 55 y 59 y coge 33, 37, 39, 46, 51, 61 y 63. Junta la tabla de récords: 61 arriba y 63 abajo."),
    ("app", "46", "El marcador del jefe", f"En el móvil: Acción, 46. Con los números puestos (37), la regla (39) y las fichas (33), el cuadrado fila por fila: {_S_MAG}. El mensaje te dice que cojas la 56.", "carta 56"),
    ("app", "51", "La tabla de récords", f"En el móvil: Acción, 51. Con la nota (26) y la tabla (61 y 63), de arriba abajo: {_S_RAN}. El mensaje te dice que cojas la 58.", "carta 58"),
    ("leer", "58", "La ranura de los récords", "Lee la carta 58. Descarta 51, 61, 63, 26 y 24 y coge 69, 70 y 71."),
    ("app", "69", "La rana de la autopista", f"En el móvil: Acción, 69. Con la autopista (70) y las velocidades (71), programa: {_S_RANA}. El mensaje te dice que cojas la 80. Anota el byte de la máquina: {I.BYTES['69']}.", "carta 80"),
    ("leer", "80", "El almacén de monedas", "Lee la carta 80. Descarta 58, 69, 70 y 71 y coge 72, 75 y 79."),
    ("app", "72", "La máquina de cambio", f"En el móvil: Acción, 72. Con las monedas (75) y el precio (79): {_S_MON}. El mensaje te dice que cojas la 82.", "carta 82"),
    ("leer", "82", "La ranura de continuar", "Lee la carta 82. Descarta 80, 72, 75 y 79 y coge 85, 86 y 87."),
    ("combinar", "38", "56", "La llave del jefe", "Las dos mitades de la llave (38 y 56) son combinables: 38 + 56 = 94. Coge la 94."),
    ("leer", "94", "La sala del jefe final", "Lee la carta 94. Descarta 38, 56, 30, 44, 33, 37, 39 y 46 y coge 64, 66 y 67. Junta el dibujo final: 66 arriba y 67 abajo."),
    ("app", "64", "El cerrojo deslizante", f"En el móvil: Acción, 64. Con el dibujo final (66 y 67), las fichas quedan así: {_S_DES}. El mensaje te dice que cojas la 62.", "carta 62"),
    ("combinar", "12", "62", "El cristal", "El Cronoportal (12) y el cristal (62) son combinables: 12 + 62 = 74. Coge la 74."),
    ("leer", "74", "Cronoportal con el cristal", "Lee la carta 74. Descarta 62, 12, 64, 66, 67, 94 y 57."),
    ("app", "85", "El arranque de la máquina", f"En el móvil: Acción, 85. Con las notas (86 y 87): {_S_XOR}. Apunta los cuatro bytes y la clave. El mensaje te dice que cojas la 99.", "carta 99"),
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
