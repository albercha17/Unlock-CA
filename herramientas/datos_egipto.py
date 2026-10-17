ESTILO = ("Ilustración digital pintada con estética de película de aventuras, luz cálida de antorchas y rayos de sol dorados, "
          "paleta de ocres, turquesa y azul lapislázuli, formato vertical 2:3. Sin texto, letras ni números en la imagen; "
          "los jeroglíficos solo como decoración sin significado legible. Deja libre de detalles importantes la esquina "
          "superior izquierda y el 18 % inferior de la imagen.")

PERSONAJES = {
    "Cristina": "Cristina, mujer de 26 años, profesora, pelo rubio y rizado, ojos azules. Lleva ropa actual y cómoda (vaqueros, zapatillas, camiseta y una chaqueta ligera).",
    "Alberto": "Alberto, hombre de 27 años, informático, pelo moreno corto, barba cuidada, ojos marrones. Lleva ropa actual (vaqueros, zapatillas, sudadera con capucha y una mochila)."
}

HOJA = ("Crea una hoja de personajes (character sheet) con las dos personas de la foto adjunta, de cuerpo entero y de frente, sobre fondo claro y neutro. "
        "Mantén su parecido real con la foto (cara, pelo, barba, ojos). "
        "Cristina: mujer de 26 años, profesora, pelo rubio y rizado, ojos azules, vaqueros, zapatillas, camiseta y chaqueta ligera. "
        "Alberto: hombre de 27 años, informático, pelo moreno corto, barba cuidada, ojos marrones, vaqueros, zapatillas, sudadera con capucha y mochila. "
        "Estilo: " + ESTILO)

FOTO = ("Antes de nada, adjunta a ChatGPT una foto de Cristina y Alberto juntos (o una de cada uno, con la cara bien visible). "
        "Pídele que mantenga el parecido real, pero con el estilo de ilustración de este juego.")

VIDEO = ("Crea un vídeo vertical 9:16 de 15 segundos, con animación de estilo ilustración pintada de película de aventuras, luz cálida y colores dorados y turquesa. Sin ningún texto, letra ni subtítulo en pantalla. "
         "Escena 1 (0-4 s): en el salón de una casa actual, Cristina (mujer de 26 años, rubia de pelo rizado, ojos azules) y Alberto (hombre de 27 años, moreno con barba, ojos marrones) rodean un aparato de latón y cristal con un anillo central: el Cronoportal. Alberto gira un dial con una sonrisa nerviosa. "
         "Escena 2 (4-8 s): el anillo se enciende con un arco de luz azul, el salón se deforma y los dos son absorbidos por un túnel de luz con destellos dorados. "
         "Escena 3 (8-12 s): caen sobre un suelo de piedra en una cámara oscura bajo un templo del antiguo Egipto, con jeroglíficos en las paredes y rayos de luz por una rendija; el aparato humea y se apaga. "
         "Escena 4 (12-15 s): primer plano de Cristina y Alberto, asombrados, mirando alrededor; fundido a negro. "
         "Sonido: zumbido eléctrico creciente, silbido del portal, golpe sordo al aterrizar, eco de piedra y música de aventura con tambores suaves, sin voz de narrador.")

J = {
    "P": dict(
        titulo="Carta P — Llegada al templo", tipo="gris", coge=[8, 14],
        descripcion=[
            "Cristina y Alberto estrenan el Cronoportal, el aparato de portales que Alberto ha construido con la ayuda de Cristina. Primera parada: Tebas, Egipto, año 1274 a.C.",
            "El salto sale mal: aterrizáis en una cámara secreta bajo el templo de Karnak y el Cronoportal se queda sin energía. Los sacerdotes entrarán al salir el sol, dentro de una hora: hay que recargar el aparato antes.",
            "Coged las cartas 8 y 14."],
        pistas=["Mirad a vuestro alrededor y revisad el aparato.", "Coged las cartas 8 y 14."],
        arte="Cámara de piedra secreta bajo un templo egipcio de Tebas, oscura, con columnas pintadas con jeroglíficos decorativos y rayos de sol que entran por una rendija. En el suelo, una consola de latón y cristal de aspecto retrofuturista (el Cronoportal) humea y parpadea con luces azules. Cristina y Alberto, con ropa actual, se incorporan sorprendidos entre el polvo."),
    "14": dict(
        titulo="Carta 14 — Cronoportal sin energía", tipo="azul", combina=[60, 74],
        descripcion=[
            "El Cronoportal: una consola de latón y cristal con un anillo central apagado y un indicador de batería casi vacío (un 3 %).",
            "Cristina recuerda haber leído que el Ojo de Horus brillaba con luz propia. Quizá sirva de fuente de energía.",
            "Combinad esta carta con el Ojo de Horus (carta 60): sumad sus números (14 + 60 = 74) y coged la carta 74."],
        pistas=["Necesita una fuente de energía muy especial.", "Combinad la carta 14 con la carta 60.", "Sumad los números de las dos cartas: 14 + 60 = 74."],
        arte="Primer plano del Cronoportal: una consola portátil de latón y cristal con dos antenas de cobre, un anillo de cristal central apagado y un indicador de batería casi vacío con una luz roja tenue, sobre una losa de piedra."),
    "8": dict(
        titulo="Carta 8 — Cámara oculta", tipo="gris", coge=[23, 31, 15, 22], descarta=["P"],
        descripcion=[
            "La cámara secreta: paredes cubiertas de jeroglíficos, una estatua de Anubis, una mesa con un papiro, una tablilla de piedra con signos y, en un muro, cinco grandes signos tallados (carta 23). Alberto encuentra además medio medallón de oro en un nicho (carta 22).",
            "Coged las cartas 23, 31, 15 y 22. Descartad la carta P."],
        pistas=["Recorred la cámara con la mirada.", "Coged las cartas 23, 31, 15 y 22. Descartad la carta P."],
        arte="Cámara secreta de piedra con paredes cubiertas de jeroglíficos decorativos, una pequeña estatua de Anubis en un nicho, una mesa de piedra con un papiro enrollado y una tablilla, y un gran muro con una hornacina cerrada; luz de antorchas. Cristina examina las paredes y Alberto sostiene una linterna del móvil."),
    "31": dict(
        titulo="Carta 31 — Piedra de traducción", tipo="gris",
        descripcion=["Una tablilla de piedra con signos y la letra que corresponde a cada uno. Cristina, que ha estudiado jeroglíficos, reconoce el sistema: sirve para leer el muro (carta 23)."],
        pistas=["Cada signo equivale a una letra.", "Sirve para el muro de jeroglíficos (carta 23)."],
        textoCarta=["🏺 = H   👁️ = O   ☀️ = R   🐞 = U", "🐍 = S   🦅 = A   🌊 = N   🐂 = T"],
        arte="Tablilla de piedra caliza con símbolos grabados en dos columnas ordenadas (vasija, ojo, sol, escarabajo, serpiente, halcón, ondas de agua, toro), iluminada por una antorcha."),
    "15": dict(
        titulo="Carta 15 — Papiro del escriba", tipo="verde",
        descripcion=[
            "El papiro del escriba Nebamón. Es un juego de la app, pero no hay nada que resolver: es un lector con varias páginas (no pausa el temporizador).",
            "Contiene los colores de los cuatro cristales del templo, una explicación del juicio de Maat y avisos sobre el amanecer.",
            "Podéis volver a abrirlo siempre que lo necesitéis."],
        pistas=["Abrid la carta 15 en la app y pasad las páginas.", "Los colores de los cristales os harán falta al final (carta 95).", "El orden de los cristales lo da la estatua del guardián (carta 44)."],
        arte="Un papiro desenrollado sobre una mesa de piedra, con pinturas de dioses egipcios y columnas de signos decorativos, junto a un cálamo y un tintero de barro; sin texto legible."),
    "23": dict(
        titulo="Carta 23 — Muro de jeroglíficos", tipo="verde",
        descripcion=[
            "Es un juego de la app: un muro con una fila de cinco signos grandes. Hay que traducirlos con la piedra de traducción (carta 31) y escribir la palabra.",
            "Al acertar se abre una hornacina con medio medallón. Coged la carta 18."],
        pistas=["Cada signo equivale a una letra: mirad la piedra de traducción.", "La palabra tiene cinco letras y es el nombre de un dios con cabeza de halcón.", "La palabra es HORUS."],
        arte="Gran muro de piedra con una fila de cinco grandes jeroglíficos tallados y pintados (vasija, ojo, sol, escarabajo, serpiente) enmarcados por una cartela dorada, con una hornacina cerrada debajo; luz de antorcha. Cristina señala los signos y Alberto toma notas en su móvil."),
    "18": dict(
        titulo="Carta 18 — Medallón izquierdo", tipo="roja", combina=[22, 40],
        descripcion=[
            "La mitad izquierda de un medallón de oro con la forma del Ojo de Horus. El borde roto en zigzag encaja con la otra mitad (carta 22).",
            "Combinadlas: sumad sus números (18 + 22 = 40) y coged la carta 40."],
        pistas=["Una mitad sola no sirve de nada.", "Combinad la carta 18 con la carta 22.", "Sumad los números de las dos cartas: 18 + 22 = 40."],
        arte="La mitad izquierda de un medallón de oro con forma del Ojo de Horus, con el borde roto en zigzag, dentro de una hornacina de piedra abierta."),
    "22": dict(
        titulo="Carta 22 — Medallón derecho", tipo="azul", combina=[18, 40],
        descripcion=[
            "La mitad derecha del medallón de oro, con el borde roto en zigzag. Encaja con la otra mitad (carta 18).",
            "Combinadlas: sumad sus números (22 + 18 = 40) y coged la carta 40."],
        pistas=["Falta la otra mitad.", "Combinad la carta 22 con la carta 18.", "Sumad los números de las dos cartas: 22 + 18 = 40."],
        arte="La mitad derecha de un medallón de oro con forma del Ojo de Horus, con el borde roto en zigzag, sobre un cojín de lino."),
    "40": dict(
        titulo="Carta 40 — Sala de las balanzas", tipo="gris", coge=[47, 52], descarta=[18, 22, 8, 23, 31],
        descripcion=[
            "El medallón completo abre una puerta oculta. Detrás hay una sala con una gran balanza de oro (carta 47) y un papiro pintado con el juicio de Maat (carta 52).",
            "Coged las cartas 47 y 52. Descartad las cartas 18, 22, 8, 23 y 31."],
        pistas=["Mirad la balanza y el papiro.", "Coged las cartas 47 y 52. Descartad las cartas 18, 22, 8, 23 y 31."],
        arte="Sala amplia con una gran balanza de oro de dos platos en el centro, estatuas de chacales, columnas con flores de loto y un pasillo oscuro al fondo; luz dorada. Alberto empuja una puerta de piedra mientras Cristina mira la balanza."),
    "47": dict(
        titulo="Carta 47 — Balanza de Maat", tipo="verde",
        descripcion=[
            "Es un juego de la app: una balanza con un corazón de piedra en un plato. Hay que poner pesas en el otro hasta equilibrarla. El peso del corazón está en el papiro del juicio (carta 52).",
            "Al equilibrarla se abre la puerta de la sala. Coged la carta 63."],
        pistas=["Fijaos en lo que dice el papiro del juicio.", "El corazón pesa 17 deben. Combinad pesas hasta sumar 17.", "Por ejemplo, 11 + 6."],
        arte="Primer plano de la gran balanza de oro: en un plato, un corazón de piedra pulida; el otro vacío; una pluma de avestruz blanca sobre el travesaño; pesas de piedra de distintos tamaños sobre una mesa."),
    "52": dict(
        titulo="Carta 52 — Papiro del juicio", tipo="gris",
        descripcion=["Un papiro con una pintura del juicio de Maat: un escriba, una balanza y un corazón. Anota cuánto pesa el corazón del escriba. Sirve para la balanza (carta 47)."],
        pistas=["Leed la anotación del papiro.", "Sirve para la balanza de Maat (carta 47)."],
        textoCarta=["El corazón del escriba", "pesa 17 deben"],
        arte="Papiro con una pintura del juicio de Maat: un escriba, una balanza y un corazón, con bordes quemados; sin texto legible."),
    "63": dict(
        titulo="Carta 63 — Pasillo de los anillos", tipo="gris", coge=[71, 26], descarta=[40, 47, 52],
        descripcion=[
            "Un estrecho pasillo termina en una gran puerta circular de piedra con tres anillos concéntricos (carta 71). Junto a ella, una cartela con un acertijo (carta 26).",
            "Coged las cartas 71 y 26. Descartad las cartas 40, 47 y 52."],
        pistas=["Hay un acertijo junto a la puerta.", "Coged las cartas 71 y 26. Descartad las cartas 40, 47 y 52."],
        arte="Pasillo estrecho de piedra que termina en una gran puerta circular de piedra con tres anillos concéntricos de símbolos, antorchas en las paredes. Cristina y Alberto delante de la puerta."),
    "71": dict(
        titulo="Carta 71 — Anillos de Ra", tipo="verde",
        descripcion=[
            "Es un juego de la app: tres anillos giratorios con símbolos. Hay que dejar arriba los tres que indica el acertijo de la cartela (carta 26).",
            "Al encajarlos se abre la puerta de la sala del sarcófago. Coged la carta 33."],
        pistas=["Leed el acertijo de la cartela.", "Sol, ojo y escarabajo, en ese orden.", "Poned ☀️, 👁️ y 🐞 de izquierda a derecha."],
        arte="Primer plano de tres anillos de piedra concéntricos girables, grabados con símbolos (sol, ojo, escarabajo, serpiente, agua, halcón) alrededor de un disco central dorado."),
    "26": dict(
        titulo="Carta 26 — Cartela del acertijo", tipo="gris",
        descripcion=["Una cartela con un acertijo de tres versos. Cada verso describe uno de los tres símbolos de los anillos (carta 71)."],
        pistas=["Cada verso es un símbolo.", "Sol, ojo y escarabajo."],
        textoCarta=["Nace en el horizonte.", "Todo lo ve.", "Renace cada día."],
        arte="Cartela de piedra con una tablilla tallada con tres pequeñas imágenes sin texto, junto a un pebetero de bronce."),
    "80": dict(
        titulo="Carta 80 — Cámara del tesoro", tipo="gris", coge=[60, 44], descarta=[33, 37, 28, 34, 46, 55, 25],
        descripcion=[
            "La llave-escarabajo gira en la cerradura y la puerta de la cámara del tesoro se abre: oro, vasijas y estatuas. Sobre un pedestal brilla el Ojo de Horus (carta 60) y, vigilando, una estatua colosal de un guardián (carta 44).",
            "Coged las cartas 60 y 44. Descartad las cartas 33, 37, 28, 34, 46, 55 y 25."],
        pistas=["Un haz de luz señala lo que buscáis.", "Coged las cartas 60 y 44. Descartad las cartas 33, 37, 28, 34, 46, 55 y 25."],
        arte="Cámara del tesoro llena de oro, vasijas, cofres y estatuas, con un haz de luz solar que cae sobre un pedestal central; al fondo, la estatua de un guardián. Cristina y Alberto asombrados en la entrada."),
    "60": dict(
        titulo="Carta 60 — Ojo de Horus", tipo="roja", combina=[14, 74],
        descripcion=[
            "El Ojo de Horus: un amuleto de oro y lapislázuli que irradia una luz azulada. Es la fuente de energía que necesita el Cronoportal.",
            "Combinadlo con el Cronoportal (carta 14): sumad sus números (60 + 14 = 74) y coged la carta 74."],
        pistas=["Es lo que el aparato necesita.", "Combinad la carta 60 con la carta 14.", "Sumad los números de las dos cartas: 60 + 14 = 74."],
        arte="El Ojo de Horus: amuleto de oro y lapislázuli, grande y brillante, sobre un cojín rojo, irradiando una luz azulada suave."),
    "44": dict(
        titulo="Carta 44 — Estatua del guardián", tipo="gris",
        descripcion=["Una estatua colosal de un guardián con cabeza de chacal. En su pecho hay cuatro cristales de colores y una inscripción: el orden en que despiertan. Os hará falta para la consola (carta 95)."],
        pistas=["Leed la inscripción del pecho.", "Los colores de cada cristal están en el papiro del escriba (carta 15)."],
        textoCarta=["Los cristales despiertan:", "Nilo, Sol, Sangre, Papiro, Sol"],
        arte="Estatua colosal de un guardián con cabeza de chacal, de piedra negra y oro, con cuatro cristales de colores (amarillo, azul, verde, rojo) engastados en su pecho."),
    "74": dict(
        titulo="Carta 74 — Cronoportal cargado", tipo="gris", coge=[95], descarta=[14, 60, 80],
        descripcion=[
            "El Ojo de Horus encaja en el anillo central y el Cronoportal despierta con un zumbido. Falta activarlo con la consola (carta 95).",
            "Coged la carta 95. Descartad las cartas 14, 60 y 80."],
        pistas=["El aparato ya tiene energía.", "Coged la carta 95. Descartad las cartas 14, 60 y 80."],
        arte="El Cronoportal con el Ojo de Horus encajado en su anillo central, brillando con luz azul intensa y arcos de energía. Alberto ajusta un dial y Cristina mira la puerta por si llegan los sacerdotes."),
    "95": dict(
        titulo="Carta 95 — Consola del Cronoportal", tipo="verde",
        descripcion=[
            "Es un juego de la app: cuatro cristales de colores que hay que tocar en el orden que indica la estatua del guardián (carta 44), usando los colores que da el papiro (carta 15).",
            "Al acertar, el portal de vuelta se abre. Coged la carta 99."],
        pistas=["Juntad el papiro (carta 15) y la estatua (carta 44).", "Nilo, Sol, Sangre, Papiro, Sol.", "Azul, amarillo, rojo, verde, amarillo."],
        arte="Primer plano de la consola del Cronoportal con cuatro cristales de colores (amarillo, azul, verde, rojo) dispuestos alrededor del Ojo de Horus, apagados."),
    "33": dict(
        titulo="Carta 33 — Sala del sarcófago", tipo="gris", coge=[37, 28, 34, 46], descarta=[63, 71, 26],
        descripcion=[
            "Los anillos giran y la puerta de piedra se abre a la sala del sarcófago: un sarcófago dorado sellado (carta 34), una tablilla rota sobre un pedestal (carta 37) y, en las paredes, dos inscripciones: una con el orden de los dioses (carta 28) y otra con una cifra grabada (carta 46).",
            "Coged las cartas 37, 28, 34 y 46. Descartad las cartas 63, 71 y 26."],
        pistas=["Hay dos puzles en esta sala: la tablilla y el sarcófago.", "Coged las cartas 37, 28, 34 y 46. Descartad las cartas 63, 71 y 26."],
        arte="Sala funeraria de piedra con un sarcófago dorado sellado en el centro, una tablilla de piedra rota sobre un pedestal y dos inscripciones talladas en las paredes; luz de antorchas. Cristina y Alberto examinan el sarcófago."),
    "37": dict(
        titulo="Carta 37 — Tablilla rota", tipo="verde",
        descripcion=[
            "Es un juego de la app: una tablilla de piedra dividida en 9 casillas con una pieza ausente. Hay que deslizar las piezas hasta ordenarla como indica el orden de los dioses (carta 28).",
            "Al recomponerla cae un escarabajo de oro. Coged la carta 55."],
        pistas=["Mirad el modelo que hay grabado en la pared (carta 28).", "Colocad primero la fila de arriba y después la del medio.", "Arriba: sol, ojo, escarabajo. En medio: serpiente, agua, halcón. Abajo: vasija, toro y el hueco."],
        arte="Una tablilla de piedra rota en nueve piezas cuadradas con símbolos grabados (sol, ojo, escarabajo, serpiente, agua, halcón, vasija, toro) y una pieza ausente, sobre un pedestal."),
    "28": dict(
        titulo="Carta 28 — Orden de los dioses", tipo="gris",
        descripcion=["Una inscripción en la pared con nueve casillas que muestra el orden en que van los símbolos de la tablilla rota (carta 37)."],
        pistas=["Es el modelo de la tablilla.", "Sirve para la tablilla rota (carta 37)."],
        textoCarta=["☀️ 👁️ 🐞", "🐍 🌊 🦅", "🏺 🐂 (hueco)"],
        arte="Una inscripción tallada en la pared con una cuadrícula de tres por tres casillas con símbolos (sol, ojo, escarabajo, serpiente, agua, halcón, vasija, toro) y una casilla vacía."),
    "34": dict(
        titulo="Carta 34 — Sarcófago sellado", tipo="verde",
        descripcion=[
            "Es un juego de la app: el sarcófago está sellado con un código de 4 cifras. La cifra está grabada en la pared con signos del sistema de numeración egipcio (carta 46).",
            "Al romper el sello aparece una cerradura de bronce. Coged la carta 25."],
        pistas=["Leed la inscripción de la pared (carta 46).", "Cada clase de signo vale una potencia de diez: sumad los de cada clase.", "❀❀ ◎◎◎ ∩∩∩∩ ||| = 2343. El código es 2343."],
        arte="Sarcófago dorado de un faraón, cerrado con un sello de cera, en el centro de una sala funeraria; sobre la tapa, un hueco con una cerradura de bronce."),
    "46": dict(
        titulo="Carta 46 — Inscripción numérica", tipo="gris",
        descripcion=["Una inscripción con signos del sistema de numeración egipcio: cada clase de signo vale una potencia de diez. Es la cifra que abre el sarcófago (carta 34)."],
        pistas=["Sumad los signos de cada clase.", "Sirve para el sarcófago sellado (carta 34)."],
        textoCarta=["| = 1   ∩ = 10   ◎ = 100   ❀ = 1000", "❀❀  ◎◎◎", "∩∩∩∩  |||"],
        arte="Una inscripción tallada en la pared con signos numéricos del antiguo Egipto (flores de loto, espirales, arcos y trazos verticales) en filas ordenadas; sin texto legible."),
    "55": dict(
        titulo="Carta 55 — Escarabajo de oro", tipo="roja", combina=[25, 80],
        descripcion=[
            "Un escarabajo de oro con las alas desplegadas que cayó de la tablilla. Su parte inferior es plana y está grabada como una llave: encaja en una cerradura de bronce (carta 25).",
            "Combinadlos: sumad sus números (55 + 25 = 80) y coged la carta 80."],
        pistas=["Es una llave con forma de escarabajo.", "Combinad la carta 55 con la carta 25.", "Sumad los números de las dos cartas: 55 + 25 = 80."],
        arte="Un escarabajo de oro con las alas desplegadas, con la parte inferior plana y grabada como una llave, sobre un cojín de lino."),
    "25": dict(
        titulo="Carta 25 — Cerradura de bronce", tipo="azul", combina=[55, 80],
        descripcion=[
            "Una cerradura de bronce con una cavidad en forma de escarabajo, sacada del sarcófago. Le falta la llave (carta 55).",
            "Combinadlas: sumad sus números (25 + 55 = 80) y coged la carta 80."],
        pistas=["Una cerradura sin llave no abre nada.", "Combinad la carta 25 con la carta 55.", "Sumad los números de las dos cartas: 25 + 55 = 80."],
        arte="Una cerradura de bronce con una cavidad en forma de escarabajo, atornillada a una puerta de piedra."),
    "99": dict(
        titulo="Carta 99 — De vuelta a casa (FIN)", tipo="gris", descarta=[74, 95, 15, 44],
        descripcion=[
            "El Ojo de Horus brilla y se abre un portal de luz azul. Cristina y Alberto saltan justo cuando se oyen las voces de los sacerdotes en el pasillo.",
            "Aterrizan en su salón. Alberto mira el aparato: «Mañana, otro destino». Cristina sonríe. Descartad las cartas 74, 95, 15 y 44.",
            "FIN."],
        pistas=[],
        arte="La escena ocurre DENTRO del salón de su casa actual, en el presente (sofá, estanterías con libros, plantas, una lámpara encendida y luz cálida de tarde por la ventana): acaban de VOLVER a casa. Cristina y Alberto acaban de salir de un portal circular de luz azul que se abre detrás de ellos; a través del portal todavía se ven la cámara del templo de Karnak y el tesoro dorado. Llevan aún su ropa de la aventura, cubierta de arena, y caen sobre la alfombra entre risas. Están de cara a nosotros, aterrizando en el salón y alejándose del portal, que queda a su espalda y se está cerrando; el mundo de la aventura solo se ve a través del portal, detrás de ellos. No están entrando en el portal ni saliendo de casa: están llegando."),
}

META = dict(
    juego="Egipto, 1274 a.C. — El Ojo de Horus",
    estilo=ESTILO, personajes=PERSONAJES, hoja=HOJA, foto=FOTO, video=VIDEO,
)

SPEC = dict(
    final="99",
    needs={"18": ["23", "31"], "40": ["18", "22"], "63": ["47", "52"], "33": ["71", "26"], "55": ["37", "28"], "25": ["34", "46"], "80": ["55", "25"], "74": ["14", "60"], "99": ["95", "15", "44"]},
    eventos={},
)

PARA_QUE = {
    "P": "Inicio: llegada al templo. Te manda coger la 8 y la 14.",
    "14": "El Cronoportal sin energía: se combina con el Ojo de Horus (60).",
    "8": "La cámara oculta: reparte las cartas de la cámara y te quita la P.",
    "31": "Piedra de traducción: signo → letra. Sirve para el muro (23).",
    "15": "Papiro del escriba (app, solo lectura): los colores de los cuatro cristales.",
    "23": "Muro de jeroglíficos (app): traducir cinco signos; la palabra es HORUS.",
    "18": "Mitad izquierda del medallón: se combina con la 22.",
    "22": "Mitad derecha del medallón: se combina con la 18.",
    "40": "Sala de las balanzas: resultado de 18 + 22. Descarta lo ya usado.",
    "47": "Balanza de Maat (app): sumar pesas hasta equilibrar el corazón.",
    "52": "Papiro del juicio: dice cuánto pesa el corazón (17 deben).",
    "63": "Pasillo de los anillos: aparece al equilibrar la balanza.",
    "71": "Anillos de Ra (app): dejar arriba sol, ojo y escarabajo.",
    "26": "Cartela con el acertijo de los tres símbolos.",
    "33": "Sala del sarcófago: aparece al encajar los anillos; reparte las cartas de la sala.",
    "37": "Tablilla rota (app): puzle deslizante 3×3.",
    "28": "Orden de los dioses: el modelo de la tablilla (37).",
    "34": "Sarcófago sellado (app): código de 4 cifras.",
    "46": "Inscripción numérica: la cifra del sarcófago (34) en numeración egipcia.",
    "55": "Escarabajo de oro: llave; se combina con la cerradura (25).",
    "25": "Cerradura de bronce: se combina con el escarabajo (55).",
    "80": "Cámara del tesoro: resultado de 55 + 25.",
    "60": "Ojo de Horus: se combina con el Cronoportal (14).",
    "44": "Estatua del guardián: orden de los cristales (Nilo, Sol, Sangre, Papiro, Sol).",
    "74": "Cronoportal cargado: resultado de 14 + 60.",
    "95": "Consola del Cronoportal (app): tocar los cristales en orden.",
    "99": "Final de la aventura.",
}

# Modo manual: pasos ejecutables (ver ejecutar_manual.py)
PASOS = [
    dict(t="Llegada al templo", que="Pon el Modo PC en el ordenador (solo debe haber la carta P en la mesa y el resto boca abajo en el mazo) y en el móvil abre el juego y pulsa Empezar. Lee la carta P: te manda coger la 8 y la 14.",
         acciones=[("leer", "P")], mesa=["P", "8", "14"]),
    dict(t="La cámara oculta", que="Lee la carta 8. Descarta la P y coge 23, 31, 15 y 22.",
         acciones=[("leer", "8")], mesa=["8", "14", "23", "31", "15", "22"]),
    dict(t="Lee el papiro en la app", que="En el móvil: Acción, 15. Pasa las 4 páginas: ahí están los colores de los cuatro cristales. No hay nada que resolver y no pausa el tiempo.",
         acciones=[("app", "15", "lector")], mesa=["8", "14", "23", "31", "15", "22"]),
    dict(t="Descifra el muro", que="La piedra de traducción (31) dice qué letra es cada signo. En el móvil: Acción, 23 y traduce los cinco signos que ves: la palabra es HORUS. El mensaje te dice que cojas la 18.",
         acciones=[("app", "23", "carta 18")], mesa=["8", "14", "23", "31", "15", "22", "18"]),
    dict(t="Combina el medallón", que="Las dos mitades del medallón (18 y 22) son combinables: 18 + 22 = 40. Coge la 40.",
         acciones=[("combinar", "18", "22")], mesa=["8", "14", "23", "31", "15", "22", "18", "40"]),
    dict(t="La sala de las balanzas", que="Lee la carta 40. Descarta 18, 22, 8, 23 y 31 y coge 47 y 52. El papiro del juicio (52) dice que el corazón pesa 17 deben.",
         acciones=[("leer", "40")], mesa=["14", "15", "40", "47", "52"]),
    dict(t="Equilibra la balanza", que="En el móvil: Acción, 47. Pon pesas en el plato hasta que sumen 17 (por ejemplo 11 + 6). El mensaje te dice que cojas la 63.",
         acciones=[("app", "47", "carta 63")], mesa=["14", "15", "40", "47", "52", "63"]),
    dict(t="El pasillo de los anillos", que="Lee la carta 63. Descarta 40, 47 y 52 y coge 71 y 26. La cartela (26) dice: «Nace en el horizonte. Todo lo ve. Renace cada día»: sol, ojo y escarabajo.",
         acciones=[("leer", "63")], mesa=["14", "15", "63", "71", "26"]),
    dict(t="Gira los anillos", que="En el móvil: Acción, 71. Deja arriba el sol, el ojo y el escarabajo, en ese orden, y pulsa Comprobar. El mensaje te dice que cojas la 33.",
         acciones=[("app", "71", "carta 33")], mesa=["14", "15", "63", "71", "26", "33"]),
    dict(t="La sala del sarcófago", que="Lee la carta 33. Descarta 63, 71 y 26 y coge 37, 28, 34 y 46. Hay dos puzles: la tablilla (37, con el modelo de la 28) y el sarcófago (34, con la cifra de la 46).",
         acciones=[("leer", "33")], mesa=["14", "15", "33", "37", "28", "34", "46"]),
    dict(t="Recompón la tablilla", que="En el móvil: Acción, 37. Desliza las piezas hasta dejarlas como en la carta 28: arriba sol, ojo, escarabajo; en medio serpiente, agua, halcón; abajo vasija, toro y el hueco. El mensaje te dice que cojas la 55.",
         acciones=[("app", "37", "carta 55")], mesa=["14", "15", "33", "37", "28", "34", "46", "55"]),
    dict(t="Abre el sarcófago", que="La inscripción (46) usa la numeración egipcia: ❀ = 1000, ◎ = 100, ∩ = 10, | = 1. Dos ❀, tres ◎, cuatro ∩ y tres | son 2343. En el móvil: Acción, 34, código 2343. El mensaje te dice que cojas la 25.",
         acciones=[("app", "34", "carta 25")], mesa=["14", "15", "33", "37", "28", "34", "46", "55", "25"]),
    dict(t="Combina la llave y la cerradura", que="El escarabajo de oro (55) y la cerradura de bronce (25) son combinables: 55 + 25 = 80. Coge la 80.",
         acciones=[("combinar", "55", "25")], mesa=["14", "15", "33", "37", "28", "34", "46", "55", "25", "80"]),
    dict(t="La cámara del tesoro", que="Lee la carta 80. Descarta 33, 37, 28, 34, 46, 55 y 25 y coge 60 (Ojo de Horus) y 44 (estatua del guardián). Lee la estatua: «Los cristales despiertan: Nilo, Sol, Sangre, Papiro, Sol».",
         acciones=[("leer", "80")], mesa=["14", "15", "80", "60", "44"]),
    dict(t="Carga el Cronoportal", que="El Cronoportal (14) y el Ojo de Horus (60) son combinables: 14 + 60 = 74. Coge la 74 y léela: te manda descartar 14, 60 y 80 y coger la 95.",
         acciones=[("combinar", "14", "60"), ("leer", "74")], mesa=["15", "44", "74", "95"]),
    dict(t="Despierta los cristales", que="En el móvil: Acción, 95. Los colores salen del papiro (Sol amarillo, Nilo azul, Papiro verde, Sangre rojo) y el orden, de la estatua: Nilo, Sol, Sangre, Papiro, Sol. Es decir: azul, amarillo, rojo, verde, amarillo. El mensaje te dice que cojas la 99.",
         acciones=[("app", "95", "carta 99")], mesa=["15", "44", "74", "95", "99"]),
    dict(t="Final", que="Lee la carta 99. Descarta 74, 95, 15 y 44. En la mesa solo queda la 99. ¡Fin!",
         acciones=[("leer", "99")], mesa=["99"]),
]
