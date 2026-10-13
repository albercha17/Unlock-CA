# Gráficos de los minijuegos de Dinosaurios (objetos sobre negro puro; se mezclan con `screen`; las texturas van a pantalla completa).
D = "juegos/aventuras-ca/dinosaurios/img/ui/"
EST = " Estilo pintura realista muy detallada, luz cálida de atardecer, aire de película de aventuras de expedición paleontológica."
FILA = " muy separados entre sí, cada uno centrado y del mismo tamaño."
SIN = " Sin texto, letras ni números. Sin personas. Vista plana, sin perspectiva."

PEDIDOS = [
    # ---- texturas generales ----
    dict(destino=D + "panel.jpg", ancho=720,
         prompt="Crea una textura de panel de selva del Cretácico: hojas de helechos gigantes y raíces sobre tierra oscura, con un marco de lianas y hojas en los bordes, "
                "luz cálida de atardecer y el centro liso y limpio para poder poner interfaz encima. Formato vertical 2:3." + SIN),
    dict(destino=D + "papel.jpg", ancho=720,
         prompt="Crea una textura de papel de libreta de campo antigua, color crema con manchas de tierra y de café, bordes desgastados y el centro liso y limpio. Formato vertical 2:3." + SIN),
    dict(destino=D + "barro.jpg", ancho=480,
         prompt="Crea una textura de barro húmedo pardo de orilla de río, de grano fino, con pequeñas piedras, vista cenital plana, iluminación uniforme. Formato cuadrado." + SIN),
    dict(destino=D + "tierra.jpg", ancho=420,
         prompt="Crea una textura de tierra de excavación arqueológica seca y compacta, marrón rojiza, con guijarros y raíces finas, vista cenital plana, iluminación uniforme. Formato cuadrado." + SIN),
    dict(destino=D + "suelo-limpio.jpg", ancho=420,
         prompt="Crea una textura de arena fina clara y suave, recién barrida con una brocha, con unas pocas marcas de cerdas, vista cenital plana, iluminación uniforme. Formato cuadrado." + SIN),
    dict(destino=D + "roca-cueva.jpg", ancho=520,
         prompt="Crea una textura de pared de cueva volcánica oscura, con roca basáltica agrietada y destellos naranjas de calor muy tenues, vista de frente plana. Formato cuadrado." + SIN),
    dict(destino=D + "rio.jpg", ancho=520,
         prompt="Crea una textura de agua de río verdosa con corriente y reflejos del cielo del atardecer, vista cenital plana. Formato cuadrado." + SIN),
    dict(destino=D + "orilla.jpg", ancho=520,
         prompt="Crea una textura de orilla de río con hierba, barro y pequeños helechos, vista cenital plana, luz cálida uniforme. Formato cuadrado." + SIN),
    # ---- huellas (cada cuadrante es una huella impresa en barro) ----
    dict(destino=D + "huellas", ancho=320, hoja=(2, 2), nombres=["tiranosaurio", "edmontosaurio", "triceratops", "anquilosaurio"],
         prompt="Crea UNA SOLA IMAGEN cuadrada dividida en cuatro cuadrantes iguales (2 columnas por 2 filas), cada cuadrante a todo su tamaño, sin márgenes. "
                "Cada cuadrante muestra una única huella de dinosaurio impresa en barro húmedo, vista cenital, centrada, con el mismo barro y la misma luz. "
                "Arriba a la izquierda: huella de tiranosaurio, tres dedos largos y finos con garras afiladas, más larga que ancha. "
                "Arriba a la derecha: huella de edmontosaurio, tres dedos gruesos y romos como un trébol, sin garras. "
                "Abajo a la izquierda: huella de triceratops, casi redonda, con cinco dedos cortos y gruesos. "
                "Abajo a la derecha: huella de anquilosaurio, muy ancha y corta, con cuatro dedos cortos." + SIN),
    # ---- excavación ----
    dict(destino=D + "hueso.jpg", ancho=300,
         prompt="Crea un hueso fósil largo (un fémur de dinosaurio) de color crema con tierra pegada, tumbado en diagonal, visto desde arriba." + EST + NEGRO),
    # ---- balsa ----
    dict(destino=D + "criaturas", ancho=260, hoja=(3, 1), nombres=["compsognato", "driosaurio", "helechos"],
         prompt="Crea UNA SOLA IMAGEN apaisada con TRES elementos vistos en tres cuartos desde arriba, en una fila," + FILA +
                " De izquierda a derecha: 1) un compsognato, un pequeño dinosaurio carnívoro bípedo del tamaño de un pollo, de color verde y marrón; "
                "2) un bebé de driosaurio, un pequeño dinosaurio herbívoro de color arena y rayas oscuras; 3) un cesto de mimbre lleno de hojas de helecho verdes." + EST + NEGRO),
    dict(destino=D + "balsa.jpg", ancho=420,
         prompt="Crea una balsa rectangular de troncos atados con cuerdas, vista en tres cuartos desde arriba, con una pértiga de madera apoyada." + EST + NEGRO),
    # ---- ADN ----
    dict(destino=D + "bases", ancho=200, hoja=(4, 1), nombres=["a", "t", "c", "g"],
         prompt="Crea UNA SOLA IMAGEN apaisada con CUATRO piezas luminosas de cristal con forma de hexágono biselado, en una fila," + FILA +
                " De izquierda a derecha: una verde esmeralda, una roja rubí, una azul zafiro y una amarilla ámbar, con un fulgor interior. SIN ninguna letra ni símbolo grabado." + EST + NEGRO),
    dict(destino=D + "marco-lab.jpg", ancho=640,
         prompt="Crea un marco de pantalla de laboratorio de campaña visto de frente: un bisel grueso de metal verde militar desgastado con tornillos, pequeños botones y luces de estado verdes, "
                "con la pantalla del centro COMPLETAMENTE NEGRA y rectangular. Formato apaisado 4:3." + EST + " Fondo negro puro. Sin texto, letras ni números. Sin personas."),
    dict(destino=D + "ambar.jpg", ancho=300,
         prompt="Crea una pieza de ámbar dorado y translúcido del tamaño de una mano, con un mosquito fosilizado dentro, vista de frente." + EST + NEGRO),
    # ---- estratos (franjas horizontales de arriba abajo) ----
    dict(destino=D + "capas", ancho=520, hoja=(1, 6), nombres=["ceniza", "carbon", "arenisca", "arcilla", "caliza", "conchas"],
         prompt="Crea UNA SOLA IMAGEN apaisada formada por SEIS franjas horizontales del mismo alto, apiladas una debajo de otra sin ninguna separación ni borde, que ocupan toda la imagen. "
                "De arriba abajo: 1) ceniza volcánica gris clara y polvorienta; 2) carbón negro brillante con vetas; 3) arenisca roja con granos visibles; "
                "4) arcilla verdosa húmeda y lisa; 5) caliza blanquecina con pequeños fósiles; 6) arena beige con conchas marinas fosilizadas. "
                "Cada franja es una textura de roca plana vista de frente, sin perspectiva." + SIN),
    # ---- cristales ----
    dict(destino=D + "cristales", ancho=240, hoja=(2, 1), nombres=["apagado", "encendido"],
         prompt="Crea UNA SOLA IMAGEN con DOS racimos de cristales idénticos, lado a lado, vistos de frente," + FILA +
                " A la izquierda uno APAGADO (cristales de roca opacos, grises azulados, sin brillo) y a la derecha el MISMO ENCENDIDO (cristales azules brillantes con un fulgor intenso)." + EST + NEGRO),
    # ---- nidos y huevos ----
    dict(destino=D + "huevos", ancho=200, hoja=(4, 1), nombres=["h1", "h2", "h3", "h4"],
         prompt="Crea UNA SOLA IMAGEN apaisada con CUATRO huevos de dinosaurio ovalados, vistos de frente, en una fila," + FILA +
                " Todos del mismo tamaño en la imagen pero cada uno con un color y moteado distinto: 1) verde oliva con manchas oscuras, 2) beige con manchas marrones, "
                "3) azul grisáceo con puntos claros, 4) marrón rojizo con rayas finas." + EST + NEGRO),
    dict(destino=D + "nidos", ancho=320, hoja=(3, 1), nombres=["ramas", "piedras", "plumas"],
         prompt="Crea UNA SOLA IMAGEN apaisada con TRES nidos vacíos de dinosaurio vistos en tres cuartos desde arriba, en una fila," + FILA +
                " De izquierda a derecha: 1) un nido de ramas y palos entrelazados; 2) un nido de piedras redondas y grava; 3) un nido de plumas grandes de colores." + EST + NEGRO),
    # ---- géiser ----
    dict(destino=D + "valvula.jpg", ancho=300,
         prompt="Crea un volante de válvula de bronce con seis radios, visto exactamente de frente y centrado, oxidado y con vetas verdes, con un eje central." + EST + NEGRO),
    dict(destino=D + "manometro.jpg", ancho=300,
         prompt="Crea un manómetro circular de bronce visto exactamente de frente, con la esfera de color crema con pequeñas marcas de escala SIN NINGÚN NÚMERO NI LETRA y SIN AGUJA, "
                "con un cristal con reflejos y un marco de bronce grueso con remaches." + EST + NEGRO),
    # ---- esqueleto (de izquierda a derecha de la hoja, arriba y abajo) ----
    dict(destino=D + "huesos", ancho=300, hoja=(4, 2), nombres=["craneo", "cuello", "torso", "cadera", "cola", "punta", "intruso1", "intruso2"],
         prompt="Crea UNA SOLA IMAGEN apaisada con OCHO huesos fósiles de color crema con tierra pegada, en dos filas de cuatro, vistos de perfil y colocados en horizontal," + FILA +
                " Fila de arriba, de izquierda a derecha: 1) el cráneo de un tiranosaurio de perfil mirando a la izquierda, 2) cuatro vértebras del cuello unidas, "
                "3) la caja torácica con costillas de perfil, 4) la cadera (pelvis) de perfil. "
                "Fila de abajo, de izquierda a derecha: 5) ocho vértebras de la cola unidas, 6) la punta fina de la cola, 7) un fémur grueso de un saurópodo, 8) una costilla larga y curva suelta." + EST + NEGRO),
]
