# Sprites del «Lejano Oeste, 1878» con ChatGPT: las ocho cosas del almacén del carro, el barril y el tabernero de la bodega y dos texturas del suelo y el muro.
ESTILO = (" Estilo de ilustración del Lejano Oeste pintada a mano, con luz cálida de atardecer, madera, cuero y hierro envejecidos, colores terrosos y detalles claros.")

PEDIDOS = [
    dict(destino="juegos/aventuras-ca/oeste/img/ui", prefijo="art-", hoja=(4, 2), ancho=300, clave="magenta",
         nombres=["0", "1", "2", "3", "4", "5", "6", "7"],
         prompt="Crea una hoja con 8 cosas del almacén de un pueblo del Oeste, en 2 filas de 4, cada una entera y de frente: un barril de whisky de madera con aros de hierro; un saco de harina de tela blanca "
                "atado; una caja de herramientas de madera con un martillo y una llave inglesa; un fardo de pieles de animal atado con correas; un cajón de madera con balas de latón y una tapa abierta; "
                "un rollo de alambre de espino; un bidón metálico de petróleo con tapón y asa; un baúl de madera con herrajes y unas barras de plata brillando." + ESTILO),
    dict(destino="juegos/aventuras-ca/oeste/img/ui", prefijo="bod-", hoja=(2, 1), ancho=300, clave="magenta", nombres=["barril", "tabernero"],
         prompt="Crea dos piezas sueltas para una bodega del Oeste, de frente y a la misma escala: 1) un barril de madera con aros de hierro; 2) un tabernero bajito y de bigote con delantal "
                "blanco, camisa de rayas y manguitos, de pie, con las manos en las caderas, sonriente." + ESTILO),
    dict(destino="juegos/aventuras-ca/oeste/img/ui", prefijo="bod-", hoja=(2, 1), ancho=256, clave="magenta", modo="recorte", nombres=["muro", "suelo"],
         prompt="Crea dos cuadrados de textura vistos exactamente de frente, que llenen cada cuadrado entero: 1) un muro de piedra oscura de bodega, con piedras irregulares y juntas; "
                "2) un suelo de tablones de madera clara de bodega, con vetas y clavos." + ESTILO),
]
