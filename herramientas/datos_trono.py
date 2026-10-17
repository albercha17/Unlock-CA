ESTILO = ("Ilustración digital cinematográfica de fantasía medieval oscura y semirrealista, con aire de gran serie de aventuras: fortalezas de piedra negra, nieve, "
          "ventisca, antorchas y fuego, paleta de azules glaciales, grises de piedra y negros profundos con destellos naranjas de llamas, copos de nieve en el aire, "
          "formato vertical 2:3. Sin texto, letras ni números en la imagen; los mapas, rollos y tapices son solo dibujos decorativos sin escritura legible. "
          "Deja libre de detalles importantes la esquina superior izquierda y el 18 % inferior de la imagen. "
          "Los personajes tienen siempre expresiones distintas y expresivas, adecuadas a la escena (nunca la misma cara en dos imágenes).")

PERSONAJES = {
    "Cristina": "Cristina, mujer de 26 años, profesora, pelo rubio y rizado recogido en una trenza, ojos azules. Viste ropa de viaje medieval de invierno: capa de lana gris con capucha forrada de piel, jubón de cuero ajustado, guantes, falda larga de lana y botas altas.",
    "Alberto": "Alberto, hombre de 27 años, informático, pelo moreno corto, barba cuidada, ojos marrones. Viste ropa medieval de invierno: jubón oscuro de cuero con cinturón, capa larga de piel sobre los hombros, guantes, pantalón de lana y botas altas."
}

HOJA = ("Crea una hoja de personajes (character sheet) con las dos personas de la foto adjunta, de cuerpo entero y de frente, sobre fondo claro y neutro. "
        "Mantén su parecido real con la foto (cara, pelo, barba, ojos). "
        "Cristina: mujer de 26 años, profesora, pelo rubio y rizado recogido en una trenza, ojos azules, capa de lana gris con capucha forrada de piel, jubón de cuero ajustado, guantes, falda larga de lana y botas altas. "
        "Alberto: hombre de 27 años, informático, pelo moreno corto, barba cuidada, ojos marrones, jubón oscuro de cuero con cinturón, capa larga de piel sobre los hombros, guantes, pantalón de lana y botas altas. "
        "Estilo: " + ESTILO)

FOTO = ("Antes de nada, adjunta a ChatGPT una foto de Cristina y Alberto juntos (o una de cada uno, con la cara bien visible). "
        "Pídele que mantenga el parecido real, pero con el estilo de ilustración de este juego.")

VIDEO = ("Crea un vídeo vertical 9:16 de 15 segundos, con estilo cinematográfico de fantasía medieval oscura, colores azules glaciales y destellos naranjas. Sin ningún texto, letra ni subtítulo en pantalla. "
         "Escena 1 (0-4 s): en el salón de una casa actual, Cristina (mujer de 26 años, rubia de pelo rizado, ojos azules) y Alberto (hombre de 27 años, moreno con barba, ojos marrones), con abrigos de invierno, rodean un aparato de latón y cristal con un anillo central: el Cronoportal. Cristina mira emocionada un libro con un dragón en la tapa. "
         "Escena 2 (4-8 s): el anillo se enciende con un arco de luz azul, el salón se deforma y los dos son absorbidos por un túnel de luz con copos de nieve. "
         "Escena 3 (8-12 s): caen sobre la nieve del patio de una fortaleza de piedra negra, en plena ventisca; al fondo, una muralla enorme y torres; un cuervo grazna y, muy arriba, una sombra con alas cruza las nubes; el aparato humea y se apaga. "
         "Escena 4 (12-15 s): primer plano de Cristina y Alberto, con capas de abrigo, mirando al cielo cubierto de nieve; fundido a negro. "
         "Sonido: zumbido eléctrico creciente, silbido del portal, golpe sordo al aterrizar, viento helado, graznido de cuervo, un rugido lejano de dragón, música épica de cuerdas graves y tambores, sin voz de narrador.")

J = {
    "P": dict(
        titulo="Carta P — Llegada a Piedra Negra", tipo="gris", coge=[10, 12],
        descripcion=[
            "Sexta parada del Cronoportal: un reino de hielo y fuego, en pleno invierno. Cristina lleva toda la vida soñando con castillos, caballeros y dragones.",
            "El salto vuelve a salir mal: aterrizáis en el patio de armas de la fortaleza de Piedra Negra, en el norte del reino, en mitad de una ventisca. El aparato golpea una piedra y su anillo de cristal se agrieta: sin una esquirla de dragón, esa piedra de fuego que solo guardan los dragones, no volverá a encenderse. Y la tormenta cierra los pasos de montaña: dentro de cien minutos el último paso quedará sellado hasta la primavera, y vosotros con él.",
            "Coged las cartas 10 y 12."],
        pistas=["Mirad a vuestro alrededor y revisad el aparato.", "Coged las cartas 10 y 12."],
        arte="El patio de armas nevado de una fortaleza de piedra negra en plena ventisca, con torres y una muralla enormes al fondo y una sombra con alas cruzando las nubes. En primer plano, un aparato de latón y cristal retrofuturista (el Cronoportal) humea sobre la nieve con el anillo de cristal agrietado y la luz azul apagándose. Cristina, con capa gris de piel, se levanta con la boca abierta de asombro; Alberto, con capa de piel, frunce el ceño con preocupación mirando el aparato."),
    "10": dict(
        titulo="Carta 10 — Patio de armas", tipo="gris", coge=[14, 16, 18, 20, 22], descarta=["P"],
        descripcion=[
            "El patio de armas de Piedra Negra, cubierto de nieve. Sobre el brocal del pozo, un cuervo con un cilindro de mensaje atado a la pata (carta 14) y, clavada en la puerta del torreón, la rueda de cifrado del maestre (carta 16). Por la puerta entreabierta del gran comedor se ve la mesa puesta para el banquete de las cuatro casas (carta 20) y la lista del senescal (carta 18). Junto a un brasero apagado, una antorcha de brea sin lumbre (carta 22).",
            "Coged las cartas 14, 16, 18, 20 y 22. Descartad la carta P."],
        pistas=["Hay dos puzles: el mensaje del cuervo y el banquete de las casas.", "Coged las cartas 14, 16, 18, 20 y 22. Descartad la carta P."],
        arte="El patio de armas de una fortaleza de piedra negra bajo la nieve: un cuervo posado sobre el brocal de un pozo con un cilindro atado a la pata, una gran puerta de madera entreabierta que deja ver un comedor con una larga mesa preparada, y un brasero apagado con una antorcha de brea al lado. Cristina observa al cuervo con curiosidad y una ceja levantada; Alberto mira hacia el comedor, boquiabierto de sorpresa."),
    "12": dict(
        titulo="Carta 12 — Cronoportal sin energía", tipo="azul", combina=[62, 74],
        descripcion=[
            "El Cronoportal: una consola de latón y cristal con un anillo central agrietado y apagado, y un hueco vacío en el pecho. Alberto: «Necesita algo que arda de verdad. En los libros, solo una esquirla de dragón sirve».",
            "Cuando consigáis la esquirla (carta 62), combinadla con el Cronoportal: sumad sus números (12 + 62 = 74) y coged la carta 74."],
        pistas=["Le falta una fuente de energía muy especial.", "Combinad la carta 12 con la carta 62.", "Sumad los números de las dos cartas: 12 + 62 = 74."],
        arte="Primer plano del Cronoportal medio cubierto de nieve: una consola portátil de latón y cristal con dos antenas de cobre, un anillo de cristal agrietado y apagado y un hueco circular vacío en el pecho del aparato, sobre un suelo de losas negras, con copos de nieve cayendo."),
    "14": dict(
        titulo="Carta 14 — Mensaje del cuervo", tipo="verde",
        descripcion=[
            "Es un juego de la app: el cuervo trae un mensaje del maestre del castillo, pero está escrito en cifra. Hay que leerlo con la rueda de cifrado (carta 16).",
            "Al acertar, comprendéis lo que os pide el maestre y el cuervo se calma. Coged la carta 26."],
        pistas=["El mensaje está en cifra: la rueda del maestre (carta 16) explica cómo leerla.", "Cada letra está corrida tres puestos hacia adelante: para leer hay que retroceder tres. La D es una A.", "El mensaje dice: BAJAD AL ARCHIVO."],
        arte="Primer plano de un cuervo negro posado sobre una piedra nevada con un pequeño cilindro de cuero atado a la pata, y a su lado un trozo de pergamino enrollado con hileras de letras sin sentido (sin texto legible), con la fortaleza borrosa al fondo bajo la ventisca."),
    "16": dict(
        titulo="Carta 16 — Rueda del maestre", tipo="gris",
        descripcion=["La rueda de cifrado del maestre, clavada en la puerta del torreón. Sirve para leer el mensaje del cuervo (carta 14)."],
        pistas=["Es la clave de la cifra.", "Sirve para el mensaje del cuervo (carta 14)."],
        textoCarta=["Cifra del maestre Osric:", "cada letra escrita está tres puestos DESPUÉS de la verdadera.", "Para leer, retroceded tres: la D es una A, la E es una B."],
        arte="Una rueda de cifrado de bronce, con dos anillos concéntricos giratorios cubiertos de runas decorativas sin escritura legible, clavada en una puerta de madera cubierta de escarcha."),
    "18": dict(
        titulo="Carta 18 — Lista del senescal", tipo="gris",
        descripcion=["La lista del senescal con el protocolo del banquete. Sirve para saber quién se sienta dónde (carta 20)."],
        pistas=["Son las primeras pistas del banquete.", "Sirve para el banquete de las casas (carta 20)."],
        textoCarta=["Cuatro casas, cuatro asientos, de izquierda a derecha.", "El Halcón Plateado ocupa el último asiento.", "Quien trae la espada no se sienta en ninguna de las dos puntas de la mesa."],
        arte="Un pergamino colgado de un clavo junto a un gran portón, con un esquema decorativo de una larga mesa vista desde arriba con cuatro sillas dibujadas a lo largo y cuatro escudos de distintos animales, sin texto legible, a la luz de una antorcha."),
    "20": dict(
        titulo="Carta 20 — Banquete de las casas", tipo="verde",
        descripcion=[
            "Es un juego de la app: cuatro casas nobles —Lobo Gris, León Dorado, Halcón Plateado y Oso Pardo— se sientan a la larga mesa del gran comedor y cada una trae un regalo: espada, copa, pieles o cuerno. Hay que averiguar qué casa ocupa cada asiento y qué regalo trae, con la lista del senescal (carta 18) y lo que cuentan los criados.",
            "Al acertar, el banquete se desarrolla en paz y los criados os dan lo que han encontrado. Coged la carta 28."],
        pistas=["La lista del senescal (carta 18) trae solo una parte de las pistas; el resto lo cuentan los criados en la pantalla.", "Empezad por el último asiento y por quién puede llevar la espada: son las dos pistas más seguras.", "De izquierda a derecha: León Dorado con la copa, Lobo Gris con las pieles, Oso Pardo con la espada y Halcón Plateado con el cuerno."],
        arte="El gran comedor de una fortaleza: una larguísima mesa de madera oscura con cuatro lugares preparados, cada uno con un estandarte de un animal distinto (un lobo gris, un león dorado, un halcón plateado, un oso pardo) y objetos sobre la mesa: una espada, una copa, unas pieles y un cuerno de beber. Alberto, con cara de concentración, rodea la mesa contando asientos; Cristina, con una sonrisa traviesa, señala un estandarte."),
    "22": dict(
        titulo="Carta 22 — Antorcha apagada", tipo="azul", combina=[35, 57],
        descripcion=["Una antorcha de brea, seca y sin lumbre. Combinadla con el pedernal que aparezca en el banquete (carta 35): sumad sus números (22 + 35 = 57) y coged la carta 57."],
        pistas=["Necesita fuego.", "Cuando tengáis el pedernal, combinadlo con la antorcha.", "Sumad los números de las dos cartas: 22 + 35 = 57."],
        arte="Una antorcha de madera con la cabeza cubierta de brea negra, apagada, apoyada junto a un brasero de hierro lleno de ceniza y cubierto de escarcha, con copos de nieve cayendo."),
    "26": dict(
        titulo="Carta 26 — Rumores del patio", tipo="gris", descarta=[14, 16],
        descripcion=[
            "El mensaje del maestre os pide que bajéis al archivo de la torre. Mientras el cuervo se calma, oís discutir a dos consejeros del señor del castillo: se acusan de mentir. Lo que dicen os servirá más adelante, para saber a quién creer (carta 51).",
            "Descartad las cartas 14 y 16."],
        pistas=["Son dos frases de dos consejeros.", "Sirven para decidir en quién confiar (carta 51)."],
        textoCarta=["Rumores de los consejeros:", "Aldric: «Brenna y Corvin son leales.»", "Brenna: «Aldric es leal.»"],
        arte="Dos consejeros de un señor medieval, con túnicas ricas y cadenas al cuello, discutiendo en voz baja bajo un soportal nevado de la fortaleza, y al fondo Cristina y Alberto escuchándolos a escondidas: Cristina con los ojos muy abiertos y los labios apretados, Alberto con una mueca de incredulidad."),
    "28": dict(
        titulo="Carta 28 — La mesa del festín", tipo="gris", coge=[35, 37], descarta=[20, 18],
        descripcion=[
            "Con las casas bien sentadas, el banquete se desarrolla en paz. Al retirarse los criados, entre los regalos queda un pedernal de buen tamaño (carta 35) y, olvidado bajo un plato, un rollo con signos extraños: lo dejó una prisionera del pueblo libre, que vive más allá del Muro (carta 37).",
            "Coged las cartas 35 y 37. Descartad las cartas 20 y 18."],
        pistas=["Mirad lo que han dejado sobre la mesa.", "Coged las cartas 35 y 37. Descartad las cartas 20 y 18."],
        arte="Una mesa de banquete medieval ya casi recogida, con copas vacías, huesos y velas; sobre ella, un pedernal grande y un rollo de pergamino atado con una cuerda, lleno de signos decorativos extraños sin texto legible. Cristina lo recoge con asombro y cara de intriga; Alberto sonríe aliviado al ver el pedernal."),
    "35": dict(
        titulo="Carta 35 — Pedernal", tipo="roja", combina=[22, 57],
        descripcion=["Un pedernal de bordes afilados, de los que sacan chispa al golpearlos con acero. Combinadlo con la antorcha (carta 22): sumad sus números (35 + 22 = 57) y coged la carta 57."],
        pistas=["Saca chispas.", "Combinad la carta 35 con la carta 22.", "Sumad los números de las dos cartas: 35 + 22 = 57."],
        arte="Un pedernal gris de bordes afilados junto a un trozo de acero y un puñado de yesca seca, sobre un paño de lana oscura, con la luz cálida de una vela."),
    "37": dict(
        titulo="Carta 37 — Rollo del pueblo libre", tipo="gris",
        descripcion=["Un rollo con frases en la lengua del pueblo libre, con su traducción debajo. Sirve para la lengua de la prisionera (carta 46), junto con la carta 48."],
        pistas=["Son tres frases con su traducción.", "Sirve para la lengua del pueblo libre (carta 46)."],
        textoCarta=["Lengua del pueblo libre:", "kra zeh ven = El cuervo teme al dragón.", "hod mor ur sil = El guerrero grande ve al lobo.", "zehi kra ven = Los dragones temen al cuervo."],
        arte="Un rollo de pergamino viejo medio desenrollado sobre una mesa de madera, con tres líneas de signos angulares decorativos parecidos a runas y, debajo de cada una, otra línea de garabatos, sin texto legible, a la luz de una vela."),
    "57": dict(
        titulo="Carta 57 — La torre del maestre", tipo="gris", coge=[40, 42], descarta=[22, 35, 28, 10],
        descripcion=[
            "Golpeáis el pedernal contra el acero y la antorcha prende con una llama anaranjada. Con ella subís las escaleras en espiral hasta la torre del maestre Osric, a oscuras. Sobre la mesa, el gran mapa de los caminos entre castillos (carta 40) y la crónica donde el maestre anotaba lo que sabía del reino (carta 42).",
            "Coged las cartas 40 y 42. Descartad las cartas 22, 35, 28 y 10."],
        pistas=["Subís a la torre con la antorcha encendida.", "Coged las cartas 40 y 42. Descartad las cartas 22, 35, 28 y 10."],
        arte="Una escalera de caracol de piedra iluminada por una antorcha encendida, que desemboca en una sala circular llena de libros, mapas y pergaminos, con una gran mesa de madera con un mapa desplegado. Cristina sube con cara de pura ilusión, iluminada por la llama; Alberto, detrás, mira un libro abierto con curiosidad y la boca entreabierta."),
    "40": dict(
        titulo="Carta 40 — Caminos entre castillos", tipo="verde",
        descripcion=[
            "Es un juego de la app: el mapa del reino con ocho castillos señalados con letras. Hay que unirlos con caminos para que todos queden conectados. El número de cada castillo dice cuántos caminos salen de él; dos castillos pueden unirse con uno o con dos caminos, y los caminos no pueden cruzarse. De dos castillos no se ve el número: está en la crónica del maestre (carta 42).",
            "Al acertar, el mapa muestra la ruta hasta el salón del consejo. Coged la carta 44."],
        pistas=["La crónica del maestre (carta 42) dice cuántos caminos salen de los dos castillos que no tienen número.", "Empezad por los castillos con un solo camino: solo pueden unirse con un vecino en línea recta.", "Dos caminos entre E y G; los demás caminos son sencillos: A con B, A con E, B con C, C con D, F con G y G con H."],
        arte="Un gran mapa antiguo de pergamino extendido sobre una mesa de madera, con ocho castillos dibujados con torres, unidos por caminos de tinta; sin texto legible; velas y un tintero alrededor. Alberto, con el ceño fruncido y un dedo sobre el mapa, calcula; Cristina lo mira con una sonrisa orgullosa."),
    "42": dict(
        titulo="Carta 42 — Crónica del maestre", tipo="verde",
        descripcion=["Es un juego de la app (solo lectura): la crónica del maestre Osric. Contiene los datos de los castillos del mapa (carta 40) y la historia del reino."],
        pistas=["Pasad las páginas con calma.", "En la crónica están los caminos que salen de dos de los castillos del mapa (carta 40).", "El castillo E tiene tres caminos y el castillo G tiene cuatro."],
        arte="Un libro enorme de tapas de cuero y cierres de bronce, abierto sobre un atril de madera en una torre, con ilustraciones decorativas de castillos y dragones, sin texto legible, y una pluma y un tintero al lado."),
    "44": dict(
        titulo="Carta 44 — El salón del consejo", tipo="gris", coge=[46, 48, 51, 52], descarta=[40, 42, 57],
        descripcion=[
            "El mapa os muestra el camino hasta el salón del consejo, bajo la torre. En un rincón, encadenada a un banco, una mujer del pueblo libre os observa con desconfianza: es la dueña del rollo (carta 46). Su traducción empieza en un trozo de pergamino (carta 48). En el centro, frente al trono vacío, discuten los consejeros del señor (carta 51) y sus palabras han quedado anotadas en otra hoja (carta 52).",
            "Coged las cartas 46, 48, 51 y 52. Descartad las cartas 40, 42 y 57."],
        pistas=["Hay dos puzles: la lengua de la prisionera y los consejeros.", "Coged las cartas 46, 48, 51 y 52. Descartad las cartas 40, 42 y 57."],
        arte="El salón del consejo de una fortaleza: un trono vacío de espadas oscuras al fondo, una mujer del pueblo libre con pieles y cabello trenzado encadenada a un banco, y cuatro consejeros discutiendo junto a una mesa. Cristina mira a la prisionera con compasión, con las cejas inclinadas; Alberto observa a los consejeros con una expresión recelosa."),
    "46": dict(
        titulo="Carta 46 — Lengua del pueblo libre", tipo="verde",
        descripcion=[
            "Es un juego de la app: la prisionera del pueblo libre solo confiará en vosotros si sabéis decir una frase en su lengua. Su lengua tiene reglas fijas: el orden de las palabras, la posición del adjetivo y cómo se hace el plural. Todo está en los ejemplos de los rollos (cartas 48 y 37).",
            "Al acertar, la prisionera os da su confianza. Coged la carta 54."],
        pistas=["Hay frases de ejemplo en las dos cartas (48 y 37): hacen falta las dos.", "Fijaos en dónde va el verbo, en dónde va el adjetivo y en cómo cambian las palabras en plural.", "La frase es: krai skai hod ven."],
        arte="Primer plano de una mujer del pueblo libre, con pieles y trenzas, sentada en un banco de piedra con una cadena en la muñeca, que señala con un dedo un rollo con signos angulares decorativos sin texto legible; luz de antorchas en una sala de piedra."),
    "48": dict(
        titulo="Carta 48 — Pergamino de la prisionera", tipo="gris",
        descripcion=["Un trozo de pergamino con otras tres frases en la lengua del pueblo libre. Sirve para la lengua de la prisionera (carta 46), junto con la carta 37."],
        pistas=["Son tres frases con su traducción.", "Sirve para la lengua del pueblo libre (carta 46)."],
        textoCarta=["Lengua del pueblo libre:", "ur kra sil = El lobo ve al cuervo.", "zeh ska ur sil = El dragón negro ve al lobo.", "uri mori kra sil = Los lobos grandes ven al cuervo."],
        arte="Un trozo de pergamino arrugado y manchado, sujeto con una piedra sobre un banco de madera, con tres líneas de signos angulares decorativos y otras tres líneas de garabatos debajo, sin texto legible, a la luz de una antorcha."),
    "51": dict(
        titulo="Carta 51 — Los consejeros", tipo="verde",
        descripcion=[
            "Es un juego de la app: cuatro consejeros del señor —Aldric, Brenna, Corvin y Dalia— hablan unos de otros. Los leales siempre dicen la verdad y los traidores siempre mienten. Hay que descubrir quién es leal y quién es traidor, con sus frases (cartas 26 y 52).",
            "Al acertar, los traidores quedan al descubierto. Coged la carta 58."],
        pistas=["Las frases de los cuatro consejeros están repartidas en dos cartas (26 y 52).", "Suponed que uno de ellos es leal y comprobad si lo que dice puede ser verdad; si hay contradicción, ese es un traidor.", "Aldric y Brenna son traidores; Corvin y Dalia son leales."],
        arte="Cuatro consejeros de un señor medieval, de pie en semicírculo frente a un trono vacío de espadas oscuras: una mujer de cabello gris, un anciano calvo con cadenas, un hombre joven con capa de piel y una mujer de ojos oscuros, todos con gestos y miradas muy distintos (desconfianza, miedo, orgullo, astucia). Cristina y Alberto los observan desde un lado, ella con gesto escéptico y él con los brazos cruzados."),
    "52": dict(
        titulo="Carta 52 — Declaraciones", tipo="gris",
        descripcion=["Las palabras de otros dos consejeros del señor, anotadas por un escribano. Sirven para decidir en quién confiar (carta 51), junto con la carta 26."],
        pistas=["Son dos frases de dos consejeros.", "Sirven para decidir en quién confiar (carta 51)."],
        textoCarta=["Declaraciones de los consejeros:", "Corvin: «Brenna es un traidor.»", "Dalia: «Corvin es leal.»"],
        arte="Una hoja de pergamino con la letra apretada de un escribano, sujeta sobre un atril de madera junto a un tintero y una pluma, con dibujos decorativos de cuatro escudos pequeños, sin texto legible, a la luz de una vela."),
    "54": dict(
        titulo="Carta 54 — La confianza de la prisionera", tipo="gris", coge=[56], descarta=[46, 48, 37],
        descripcion=[
            "La mujer del pueblo libre sonríe por primera vez: habéis hablado como los suyos. Os cuenta que el sello que cierra la cripta del dragón se partió en dos mitades y que ella guarda una: os la entrega, cosida al forro de su capa de pieles.",
            "Coged la carta 56. Descartad las cartas 46, 48 y 37."],
        pistas=["Mirad lo que os da la prisionera.", "Coged la carta 56. Descartad las cartas 46, 48 y 37."],
        arte="La mujer del pueblo libre, con una sonrisa cálida y los ojos brillantes, entrega a Cristina un medallón metálico partido por la mitad, desde una capa de pieles; Cristina lo recibe con los ojos muy abiertos y una gran sonrisa; Alberto, detrás, suspira aliviado. Sala de piedra iluminada por antorchas."),
    "56": dict(
        titulo="Carta 56 — Mitad del sello", tipo="azul", combina=[38, 94],
        descripcion=["La mitad izquierda de un sello de metal negro con el relieve de un dragón: la mitad que guardaba la prisionera. Combinadla con la otra mitad (carta 38): sumad sus números (56 + 38 = 94) y coged la carta 94."],
        pistas=["Es solo una mitad de algo.", "Cuando tengáis la otra mitad, combinadlas.", "Sumad los números de las dos cartas: 56 + 38 = 94."],
        arte="La mitad izquierda de un sello circular de metal negro, con el relieve del lado izquierdo de un dragón enroscado, sobre un paño de lana gris, con una vela al lado."),
    "58": dict(
        titulo="Carta 58 — La traición", tipo="gris", coge=[38], descarta=[51, 52, 26],
        descripcion=[
            "Los consejeros desleales quedan al descubierto: Aldric y Brenna intentaban abrir la cripta del dragón para robar su tesoro. Sin embargo, en el forro del manto de Brenna, que se desmaya del susto, aparece la otra mitad del sello.",
            "Coged la carta 38. Descartad las cartas 51, 52 y 26."],
        pistas=["Los traidores han perdido algo.", "Coged la carta 38. Descartad las cartas 51, 52 y 26."],
        arte="Una consejera cae desmayada sobre el suelo del salón del consejo, con la capa abierta y una mitad de sello brillante asomando del forro; otro consejero retrocede aterrado hacia la pared. Cristina se agacha con cara de sorpresa y la mano en la boca; Alberto levanta la mitad del sello con una sonrisa de triunfo."),
    "38": dict(
        titulo="Carta 38 — Mitad del sello", tipo="roja", combina=[56, 94],
        descripcion=["La mitad derecha del sello de metal negro con el relieve del dragón. Combinadla con la otra mitad (carta 56): sumad sus números (38 + 56 = 94) y coged la carta 94."],
        pistas=["Es solo una mitad de algo.", "Combinad la carta 38 con la carta 56.", "Sumad los números de las dos cartas: 38 + 56 = 94."],
        arte="La mitad derecha de un sello circular de metal negro, con el relieve del lado derecho de un dragón enroscado, sobre un paño de lana gris, con un hilo del forro de una capa aún pegado."),
    "94": dict(
        titulo="Carta 94 — La cripta del dragón", tipo="gris", coge=[64, 66], descarta=[56, 38, 44, 54, 58],
        descripcion=[
            "El sello completo encaja en una puerta de piedra al fondo del salón y la abre con un crujido. Una escalera baja a la cripta: una sala de columnas a oscuras, de donde sube un calor extraño. Hay antorchas en las paredes, pero apagadas (carta 64), y en el suelo, un plano del maestre con indicaciones sobre cómo iluminarla (carta 66).",
            "Coged las cartas 64 y 66. Descartad las cartas 56, 38, 44, 54 y 58."],
        pistas=["Hay un puzle: las antorchas de la cripta.", "Coged las cartas 64 y 66. Descartad las cartas 56, 38, 44, 54 y 58."],
        arte="Una puerta circular de piedra negra que se abre con un sello metálico encajado, y tras ella una escalera de caracol que baja a una cripta de columnas inmensas en la oscuridad, con un resplandor naranja muy débil al fondo. Cristina baja con un gesto de miedo contenido y los ojos muy abiertos; Alberto, delante, alza una linterna de aceite con expresión decidida."),
    "64": dict(
        titulo="Carta 64 — Antorchas de la cripta", tipo="verde",
        descripcion=[
            "Es un juego de la app: el plano de la cripta, con pilares y muchas casillas libres. Hay que colocar antorchas en casillas libres. Cada antorcha ilumina su fila y su columna hasta un pilar, ninguna antorcha puede iluminar a otra, y todo el suelo debe quedar iluminado. El número de un pilar dice cuántas antorchas tiene pegadas. De algunos pilares no se ve el número: está en el plano del maestre (carta 66).",
            "Al acertar, la cripta se ilumina por completo. Coged la carta 78."],
        pistas=["El plano del maestre (carta 66) da el número de dos pilares que la pantalla no muestra.", "Un pilar con 0 no tiene ninguna antorcha pegada: empezad por ahí y por los pilares con números altos.", "Las antorchas están en B1, D1, E2, A3, F3, B4, E4, C5 y A6."],
        arte="Una cripta de columnas inmensas de piedra negra sumida en la penumbra, con antorchas de pared apagadas y otras recién encendidas que iluminan franjas del suelo con una luz naranja. Alberto, de puntillas, acerca una antorcha a la pared con expresión concentrada; Cristina lo observa con los labios apretados y los ojos brillantes."),
    "66": dict(
        titulo="Carta 66 — Plano de la cripta", tipo="gris",
        descripcion=["El plano del maestre con los números de dos pilares. Sirve para las antorchas de la cripta (carta 64)."],
        pistas=["Son datos de dos pilares.", "Sirve para las antorchas de la cripta (carta 64)."],
        textoCarta=["Plano del maestre. Columnas de A a F, filas de 1 a 6.", "El pilar C1 tiene dos antorchas pegadas.", "El pilar C3 no tiene ninguna."],
        arte="Un plano dibujado en pergamino amarillento sobre el suelo de piedra de una cripta, con una cuadrícula de líneas y varios círculos negros que marcan pilares, junto a una antorcha apagada, sin texto legible, con luz naranja débil."),
    "78": dict(
        titulo="Carta 78 — La puerta de bronce", tipo="gris", coge=[69, 70], descarta=[64, 66, 94],
        descripcion=[
            "La cripta ilumina una inmensa puerta de bronce al fondo: es la entrada a la guarida del dragón. Pero está atascada por un amasijo de troncos y carros viejos que alguien amontonó para impedir que se abriera (carta 69). Una nota del maestre (carta 70) dice cuál de ellos es el ariete, el único que puede romper la barricada.",
            "Coged las cartas 69 y 70. Descartad las cartas 64, 66 y 94."],
        pistas=["Hay un puzle: el atasco ante la puerta.", "Coged las cartas 69 y 70. Descartad las cartas 64, 66 y 94."],
        arte="Una inmensa puerta de bronce con relieves de dragones al fondo de una cripta iluminada por antorchas, bloqueada por un amasijo de troncos, carros y vigas amontonados. Cristina mira la barricada con las cejas levantadas y la boca abierta; Alberto se arremanga con una media sonrisa desafiante."),
    "69": dict(
        titulo="Carta 69 — Atasco ante la puerta", tipo="verde",
        descripcion=[
            "Es un juego de la app: un atasco de troncos y carros ante la puerta de bronce. Cada pieza solo se desliza en la dirección en la que apunta. Hay que sacar el ariete por el lado derecho. La nota del maestre (carta 70) dice cuál es.",
            "Al acertar, la puerta queda libre y se abre. Coged la carta 80."],
        pistas=["La nota del maestre (carta 70) dice cuál es el ariete.", "Empezad por la pieza que bloquea directamente el paso del ariete y pensad hacia dónde puede apartarse.", "Se resuelve en diez movimientos; el primero es mover hacia la izquierda el carro de la fila de abajo del ariete."],
        arte="Un atasco de troncos largos y carros de madera amontonados ante una gran puerta de bronce, vistos desde arriba, con un tronco largo de punta metálica (el ariete) en primer plano; luz de antorchas."),
    "70": dict(
        titulo="Carta 70 — Nota del maestre", tipo="gris",
        descripcion=["Una nota del maestre sobre el ariete. Sirve para el atasco ante la puerta (carta 69)."],
        pistas=["Dice cuál es el ariete.", "Sirve para el atasco ante la puerta (carta 69)."],
        textoCarta=["El ariete es el tronco de la tercera fila", "que está pegado al borde izquierdo.", "Debe salir por el lado derecho."],
        arte="Una nota de papel clavada con una daga en una viga de madera, con un dibujo decorativo de un tronco con punta de metal y una flecha hacia la derecha, sin texto legible, a la luz de una antorcha."),
    "80": dict(
        titulo="Carta 80 — El dragón dormido", tipo="gris", coge=[72, 76], descarta=[69, 70, 78],
        descripcion=[
            "La puerta de bronce se abre y el calor os golpea el rostro: la guarida del dragón. Ceniza, un dragón viejísimo de escamas negras, duerme enroscado sobre su tesoro, y entre sus garras brilla una esquirla roja. Junto a la entrada, un viejo tapiz sin terminar con el sigilo de la casa que lo domó (carta 72) y las notas de las tejedoras (carta 76).",
            "Coged las cartas 72 y 76. Descartad las cartas 69, 70 y 78."],
        pistas=["Hay que terminar el tapiz con el sigilo antes de acercarse al dragón.", "Coged las cartas 72 y 76. Descartad las cartas 69, 70 y 78."],
        arte="Una guarida enorme y caliente con un dragón de escamas negras dormido y enroscado sobre montones de oro, con una esquirla roja brillante entre sus garras, y en primer plano un tapiz sin terminar colgado de un bastidor. Cristina, paralizada, se lleva las manos a la boca con los ojos como platos; Alberto, con los hombros tensos, hace un gesto de silencio con el dedo sobre los labios."),
    "72": dict(
        titulo="Carta 72 — Tapiz del sigilo", tipo="verde",
        descripcion=[
            "Es un juego de la app: un tapiz de seis por seis casillas. Hay que pintar las casillas necesarias para que aparezca el sigilo del dragón. Los números de cada fila (a la izquierda) y de cada columna (arriba) dicen cuántas casillas seguidas hay pintadas, y entre bloques hay al menos una vacía. En la pantalla están los números de las filas; los de las columnas están en las notas de las tejedoras (carta 76).",
            "Al acertar, el sigilo brilla y el dragón se apacigua. Coged la carta 82."],
        pistas=["Los números de las columnas están en las notas de las tejedoras (carta 76).", "Una fila con un solo 6 está pintada del todo: empezad por ahí.", "El dibujo es una llama: la tercera fila está pintada entera y la cuarta tiene un hueco en el medio."],
        arte="Un tapiz medieval sin terminar con el dibujo de una llama formada por cuadrados de hilo rojo y dorado, tensado sobre un bastidor de madera, con ovillos de lana y agujas al lado, a la luz de una antorcha."),
    "76": dict(
        titulo="Carta 76 — Notas de las tejedoras", tipo="gris",
        descripcion=["Las notas de las tejedoras con los números de las columnas del tapiz. Sirven para el tapiz del sigilo (carta 72)."],
        pistas=["Son los números de las columnas.", "Sirven para el tapiz del sigilo (carta 72)."],
        textoCarta=["Columnas del tapiz, de izquierda a derecha:", "A: 2 · B: 4 · C: 3 y 2", "D: 3 y 2 · E: 4 · F: 2"],
        arte="Una hoja de notas de tejedora con columnas de pequeños puntos de colores y números decorativos sin texto legible, sujeta con una aguja a un bastidor de madera, con ovillos de lana al lado."),
    "82": dict(
        titulo="Carta 82 — La esquirla", tipo="gris", coge=[62], descarta=[72, 76, 80],
        descripcion=[
            "El sigilo del tapiz brilla y el dragón, sin despertar, suelta la garra con un suspiro de humo: entre sus uñas queda una esquirla de cristal rojo, tibia y vibrante. Cristina la recoge con la capa y retrocede de puntillas.",
            "Coged la carta 62. Descartad las cartas 72, 76 y 80."],
        pistas=["Recoged la esquirla.", "Coged la carta 62. Descartad las cartas 72, 76 y 80."],
        arte="Cristina, de puntillas, recoge con el borde de su capa una esquirla de cristal rojo brillante de la garra de un dragón negro dormido; su cara muestra una concentración extrema, con la lengua entre los dientes; Alberto, detrás, aguanta la respiración con los ojos como platos."),
    "62": dict(
        titulo="Carta 62 — Esquirla de dragón", tipo="roja", combina=[12, 74],
        descripcion=["Una esquirla de cristal rojo, tibia, con un fulgor interior como de brasa. Combinadla con el Cronoportal (carta 12): sumad sus números (62 + 12 = 74) y coged la carta 74."],
        pistas=["Es la energía que faltaba.", "Combinad la carta 62 con la carta 12.", "Sumad los números de las dos cartas: 62 + 12 = 74."],
        arte="Una esquirla de cristal rojo con un fulgor interior de brasa, sostenida sobre la palma de una mano enguantada, sobre un fondo oscuro de guarida con destellos dorados."),
    "74": dict(
        titulo="Carta 74 — Cronoportal reconectado", tipo="gris", coge=[84, 86], descarta=[62, 12, 82],
        descripcion=[
            "La esquirla encaja con un chasquido y el Cronoportal se enciende... pero no abre el paso: en el anillo, el aparato repite una y otra vez unas palabras sueltas, las que habéis ido encontrando por el castillo, como si pidiera que las pongáis en orden antes de abrir el portal. Es la profecía del reino (carta 84). El maestre dejó en su torre unas pistas para ordenarla (carta 86).",
            "Coged las cartas 84 y 86. Descartad las cartas 62, 12 y 82."],
        pistas=["El portal pide ordenar unas palabras.", "Coged las cartas 84 y 86. Descartad las cartas 62, 12 y 82."],
        arte="El Cronoportal encendido con una esquirla roja encajada en su pecho, sobre las losas de la guarida del dragón dormido, con el anillo girando y proyectando palabras de luz dorada en el aire. Cristina sonríe con un ojo cerrado, medio incrédula; Alberto mira el anillo con expresión de curiosidad y la cabeza ladeada."),
    "84": dict(
        titulo="Carta 84 — La profecía", tipo="verde",
        descripcion=[
            "Es un juego de la app: el Cronoportal muestra las ocho palabras de la profecía del reino que habéis ido recuperando al resolver los puzles del castillo, pero mezcladas. Hay que ponerlas en orden con las pistas del maestre (carta 86). Si falta alguna palabra, la app dice qué carta hay que volver a resolver.",
            "Al acertar, el portal se abre. Coged la carta 99."],
        pistas=["Las palabras están en el anillo; las pistas para ordenarlas, en las notas del maestre (carta 86).", "Empezad por las palabras que tienen un lugar fijo: la primera y la última.", "La profecía dice: SOLO EL FUEGO VENCERÁ AL HIELO DEL NORTE."],
        arte="Ocho palabras de luz dorada flotando sin orden en un círculo sobre el anillo de cristal de un Cronoportal encendido, en la penumbra de una guarida con un dragón dormido al fondo; sin texto legible, solo formas de letras difusas."),
    "86": dict(
        titulo="Carta 86 — Pistas del maestre", tipo="gris",
        descripcion=["Las notas del maestre Osric para ordenar las palabras de la profecía. Sirven para la profecía (carta 84)."],
        pistas=["Son las reglas para ordenar las palabras.", "Sirven para la profecía (carta 84)."],
        textoCarta=["Pistas del maestre:", "La profecía empieza con SOLO. FUEGO va justo después de EL.", "VENCERÁ va justo después de FUEGO y antes que HIELO.", "AL va justo antes de HIELO. DEL va justo antes de NORTE.", "NORTE es la última palabra."],
        arte="Una hoja de notas de un viejo maestre con ocho círculos pequeños unidos por flechas decorativas, sin texto legible, sobre una mesa de madera con una pluma y un tintero, a la luz de una vela."),
    "99": dict(
        titulo="Carta 99 — De vuelta a casa (FIN)", tipo="gris", descarta=[74, 84, 86],
        descripcion=[
            "Las palabras se ordenan en el aire y el anillo del Cronoportal las pronuncia en voz alta: «Solo el fuego vencerá al hielo del norte». El portal se abre en un estallido de luz justo cuando el dragón abre un ojo dorado y os mira, sin enfado. Cristina le dedica una reverencia.",
            "Aterrizan en su salón, con copos de nieve aún en el pelo. Alberto mira el aparato: «Mañana, otro destino». Cristina sonríe. Descartad las cartas 74, 84 y 86.",
            "FIN."],
        pistas=[],
        arte="La escena ocurre DENTRO del salón de su casa actual, en el presente (sofá, estanterías con libros, plantas, una lámpara encendida y luz cálida de tarde por la ventana): acaban de VOLVER a casa. Cristina y Alberto acaban de salir de un portal circular de luz azul y dorada que se abre detrás de ellos; a través del portal todavía se ve la guarida de un dragón negro que abre un ojo dorado. Llevan aún su ropa medieval de invierno con copos de nieve que se derriten. Cristina sonríe radiante y Alberto se ríe sacudiéndose la nieve. Están de cara a nosotros, aterrizando en el salón y alejándose del portal, que queda a su espalda y se está cerrando; el mundo de la aventura solo se ve a través del portal, detrás de ellos. No están entrando en el portal ni saliendo de casa: están llegando."),
}

META = dict(
    juego="Reino de Hielo y Fuego — La Corona del Dragón",
    estilo=ESTILO, personajes=PERSONAJES, hoja=HOJA, foto=FOTO, video=VIDEO,
)

SPEC = dict(
    final="99",
    needs={"26": ["14", "16"], "28": ["20", "18"], "57": ["22", "35"], "44": ["40", "42"], "54": ["46", "48", "37"],
           "58": ["51", "52", "26"], "94": ["56", "38"], "78": ["64", "66"], "80": ["69", "70"], "82": ["72", "76"],
           "74": ["62", "12"], "99": ["84", "86"]},
    eventos={},
)

PARA_QUE = {
    "P": "Inicio: llegada a la fortaleza. Te manda coger la 10 y la 12.",
    "10": "El patio de armas: reparte el cuervo, la rueda, la lista del senescal, el banquete y la antorcha.",
    "12": "El Cronoportal sin energía: se combina con la esquirla de dragón (62).",
    "14": "Mensaje del cuervo (app): descifrar un mensaje con la cifra del maestre (César).",
    "16": "Rueda del maestre: la regla de la cifra (retroceder tres letras).",
    "18": "Lista del senescal: las dos primeras pistas del banquete.",
    "20": "Banquete de las casas (app): tabla lógica de casas, asientos y regalos.",
    "22": "Antorcha apagada: se combina con el pedernal (35).",
    "26": "Rumores del patio: dos frases de consejeros; te manda descartar el cuervo y la rueda.",
    "28": "La mesa del festín: reparte el pedernal y el rollo del pueblo libre.",
    "35": "Pedernal: se combina con la antorcha (22).",
    "37": "Rollo del pueblo libre: tres frases de ejemplo de su lengua.",
    "57": "La torre del maestre: resultado de 22 + 35; reparte el mapa y la crónica.",
    "40": "Caminos entre castillos (app): unir castillos con caminos (puentes, estilo hashi).",
    "42": "Crónica del maestre (app de lectura): los caminos de dos castillos del mapa.",
    "44": "El salón del consejo: reparte la lengua de la prisionera y los consejeros.",
    "46": "Lengua del pueblo libre (app): traducir una frase con las reglas de los ejemplos.",
    "48": "Pergamino de la prisionera: otras tres frases de ejemplo.",
    "51": "Los consejeros (app): deducir quién es leal y quién traidor.",
    "52": "Declaraciones: dos frases más de consejeros.",
    "54": "La confianza de la prisionera: reparte la primera mitad del sello.",
    "56": "Mitad del sello: se combina con la otra mitad (38).",
    "58": "La traición: reparte la segunda mitad del sello.",
    "38": "Mitad del sello: se combina con la otra mitad (56).",
    "94": "La cripta del dragón: resultado de 56 + 38; reparte las antorchas y el plano.",
    "64": "Antorchas de la cripta (app): iluminar el suelo sin que se vean entre sí (akari).",
    "66": "Plano de la cripta: el número de dos pilares.",
    "78": "La puerta de bronce: reparte el atasco y la nota.",
    "69": "Atasco ante la puerta (app): bloques deslizantes; sacar el ariete.",
    "70": "Nota del maestre: cuál es el ariete.",
    "80": "El dragón dormido: reparte el tapiz y las notas.",
    "72": "Tapiz del sigilo (app): nonograma que dibuja una llama.",
    "76": "Notas de las tejedoras: los números de las columnas del tapiz.",
    "82": "La esquirla: reparte la esquirla de dragón.",
    "62": "Esquirla de dragón: se combina con el Cronoportal (12).",
    "74": "Cronoportal reconectado: resultado de 62 + 12; reparte la profecía y las pistas.",
    "84": "La profecía (app): ordenar las ocho palabras recuperadas en los puzles (metapuzle final).",
    "86": "Pistas del maestre: reglas para ordenar las palabras.",
    "99": "Final de la aventura.",
}

PASOS = [
    dict(t="Llegada a Piedra Negra", que="Pon el Modo PC en el ordenador (solo debe haber la carta P en la mesa y el resto boca abajo en el mazo) y en el móvil abre el juego y pulsa Empezar. Lee la carta P: te manda coger la 10 y la 12.",
         acciones=[("leer", "P")], mesa=["P", "10", "12"]),
    dict(t="El patio de armas", que="Lee la carta 10. Descarta la P y coge 14, 16, 18, 20 y 22. Hay dos puzles: el mensaje del cuervo (14, con la rueda 16) y el banquete (20, con la lista 18).",
         acciones=[("leer", "10")], mesa=["10", "12", "14", "16", "18", "20", "22"]),
    dict(t="Lee el mensaje del cuervo", que="En el móvil: Acción, 14. La rueda (16) dice que cada letra está tres puestos adelantada. El mensaje dice BAJAD AL ARCHIVO. El mensaje te dice que cojas la 26 y anota la palabra de la profecía que aparece (HIELO).",
         acciones=[("app", "14", "carta 26")], mesa=["10", "12", "14", "16", "18", "20", "22", "26"]),
    dict(t="Los rumores", que="Lee la carta 26. Te manda descartar la 14 y la 16. Guárdala: sus frases sirven para los consejeros más adelante.",
         acciones=[("leer", "26")], mesa=["10", "12", "18", "20", "22", "26"]),
    dict(t="El banquete de las casas", que="En el móvil: Acción, 20. Con la lista del senescal (18): de izquierda a derecha, León Dorado con la copa, Lobo Gris con las pieles, Oso Pardo con la espada y Halcón Plateado con el cuerno. El mensaje te dice que cojas la 28.",
         acciones=[("app", "20", "carta 28")], mesa=["10", "12", "18", "20", "22", "26", "28"]),
    dict(t="La mesa del festín", que="Lee la carta 28. Descarta 20 y 18 y coge 35 y 37. El pedernal (35) es combinable; el rollo (37) trae tres frases de la lengua del pueblo libre.",
         acciones=[("leer", "28")], mesa=["10", "12", "22", "26", "28", "35", "37"]),
    dict(t="Antorcha con pedernal", que="La antorcha (22) y el pedernal (35) son combinables: 22 + 35 = 57. Coge la 57.",
         acciones=[("combinar", "22", "35")], mesa=["10", "12", "22", "26", "28", "35", "37", "57"]),
    dict(t="La torre del maestre", que="Lee la carta 57. Descarta 22, 35, 28 y 10 y coge 40 y 42.",
         acciones=[("leer", "57")], mesa=["12", "26", "37", "57", "40", "42"]),
    dict(t="La crónica del maestre", que="En el móvil: Acción, 42. Pasa las páginas: dicen cuántos caminos salen de los castillos E y G (tres y cuatro).",
         acciones=[("app", "42", "")], mesa=["12", "26", "37", "57", "40", "42"]),
    dict(t="Une los castillos", que="En el móvil: Acción, 40. Une los castillos: A con B, A con E, B con C, C con D, F con G, G con H y dos caminos entre E y G. El mensaje te dice que cojas la 44 y anota la palabra de la profecía (VENCERÁ).",
         acciones=[("app", "40", "carta 44")], mesa=["12", "26", "37", "57", "40", "42", "44"]),
    dict(t="El salón del consejo", que="Lee la carta 44. Descarta 40, 42 y 57 y coge 46, 48, 51 y 52. Hay dos puzles: la lengua de la prisionera (46, con 37 y 48) y los consejeros (51, con 26 y 52).",
         acciones=[("leer", "44")], mesa=["12", "26", "37", "44", "46", "48", "51", "52"]),
    dict(t="Habla como el pueblo libre", que="En el móvil: Acción, 46. Con las frases de los rollos (37 y 48), escribe: krai skai hod ven. El mensaje te dice que cojas la 54 y anota la palabra de la profecía (DEL).",
         acciones=[("app", "46", "carta 54")], mesa=["12", "26", "37", "44", "46", "48", "51", "52", "54"]),
    dict(t="La confianza de la prisionera", que="Lee la carta 54. Descarta 46, 48 y 37 y coge la 56, una mitad del sello.",
         acciones=[("leer", "54")], mesa=["12", "26", "44", "51", "52", "54", "56"]),
    dict(t="Leales y traidores", que="En el móvil: Acción, 51. Con las frases de las cartas 26 y 52: Aldric y Brenna son traidores; Corvin y Dalia, leales. El mensaje te dice que cojas la 58 y anota la palabra de la profecía (FUEGO).",
         acciones=[("app", "51", "carta 58")], mesa=["12", "26", "44", "51", "52", "54", "56", "58"]),
    dict(t="La traición", que="Lee la carta 58. Descarta 51, 52 y 26 y coge la 38, la otra mitad del sello.",
         acciones=[("leer", "58")], mesa=["12", "44", "54", "56", "58", "38"]),
    dict(t="El sello completo", que="Las dos mitades del sello (56 y 38) son combinables: 56 + 38 = 94. Coge la 94.",
         acciones=[("combinar", "56", "38")], mesa=["12", "44", "54", "56", "58", "38", "94"]),
    dict(t="La cripta del dragón", que="Lee la carta 94. Descarta 56, 38, 44, 54 y 58 y coge 64 y 66. El plano (66) da el número de dos pilares de la cripta (64).",
         acciones=[("leer", "94")], mesa=["12", "94", "64", "66"]),
    dict(t="Enciende las antorchas", que="En el móvil: Acción, 64. Con el plano (66): antorchas en B1, D1, E2, A3, F3, B4, E4, C5 y A6. El mensaje te dice que cojas la 78 y anota la palabra de la profecía (NORTE).",
         acciones=[("app", "64", "carta 78")], mesa=["12", "94", "64", "66", "78"]),
    dict(t="La puerta de bronce", que="Lee la carta 78. Descarta 64, 66 y 94 y coge 69 y 70. La nota (70) dice cuál es el ariete.",
         acciones=[("leer", "78")], mesa=["12", "78", "69", "70"]),
    dict(t="Libera la puerta", que="En el móvil: Acción, 69. Saca el ariete (el tronco largo de la tercera fila) por la derecha en diez movimientos. El mensaje te dice que cojas la 80 y anota la palabra de la profecía (AL).",
         acciones=[("app", "69", "carta 80")], mesa=["12", "78", "69", "70", "80"]),
    dict(t="El dragón dormido", que="Lee la carta 80. Descarta 69, 70 y 78 y coge 72 y 76. Las notas (76) dan los números de las columnas del tapiz.",
         acciones=[("leer", "80")], mesa=["12", "80", "72", "76"]),
    dict(t="Termina el tapiz", que="En el móvil: Acción, 72. Pinta el sigilo (una llama) con los números de las filas de la pantalla y los de las columnas de la carta 76. El mensaje te dice que cojas la 82 y anota la palabra de la profecía (EL).",
         acciones=[("app", "72", "carta 82")], mesa=["12", "80", "72", "76", "82"]),
    dict(t="La esquirla", que="Lee la carta 82. Descarta 72, 76 y 80 y coge la 62, la esquirla de dragón.",
         acciones=[("leer", "82")], mesa=["12", "82", "62"]),
    dict(t="Esquirla en el Cronoportal", que="El Cronoportal (12) y la esquirla (62) son combinables: 12 + 62 = 74. Coge la 74.",
         acciones=[("combinar", "12", "62")], mesa=["12", "82", "62", "74"]),
    dict(t="Cronoportal reconectado", que="Lee la carta 74. Descarta 62, 12 y 82 y coge 84 y 86. Las notas (86) explican cómo ordenar la profecía.",
         acciones=[("leer", "74")], mesa=["74", "84", "86"]),
    dict(t="Ordena la profecía", que="En el móvil: Acción, 84. Con las notas (86), ordena las palabras: SOLO EL FUEGO VENCERÁ AL HIELO DEL NORTE. El mensaje te dice que cojas la 99.",
         acciones=[("app", "84", "carta 99")], mesa=["74", "84", "86", "99"]),
    dict(t="Final", que="Lee la carta 99. Descarta 74, 84 y 86. En la mesa solo queda la 99. ¡Fin!",
         acciones=[("leer", "99")], mesa=["99"]),
]
