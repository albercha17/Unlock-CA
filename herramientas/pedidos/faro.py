# Gráficos de los minijuegos de El Faro de Cabo Niebla. Objetos sobre negro puro (se mezclan con `screen` en la app).
D = "juegos/el-faro/img/ui/"
ESTILO = " Estilo pintura realista muy detallada, latón envejecido, cristal y madera de faro marino, luz cálida de farol."

PEDIDOS = [
    # --- carta 70: espejos de la lente (tablero 8x6) ---
    dict(destino=D + "espejos/tablero.jpg", ancho=900,
         prompt="Crea una vista cenital de un tablero de latón y madera oscura dentro de la linterna de un faro, con raíles finos grabados, tornillos y esquinas "
                "de latón envejecido, iluminación cálida suave y el centro liso y limpio. Formato apaisado 3:2. Sin texto, letras ni números. Sin personas."),
    dict(destino=D + "espejos/espejo.jpg", ancho=320,
         prompt="Crea UN espejo de bronce rectangular alargado y estrecho, visto desde arriba, colocado en diagonal a 45 grados (de la esquina inferior izquierda a la "
                "superior derecha), con marco ornamentado de latón y cristal plateado muy brillante que refleja destellos dorados." + NEGRO),
    dict(destino=D + "espejos/lampara-apagada.jpg", ancho=320,
         prompt="Crea la gran lámpara de aceite de un faro vista desde arriba: anillos concéntricos de cristal tipo Fresnel y un quemador de latón en el centro, apagada y oscura." + NEGRO),
    dict(destino=D + "espejos/lampara-encendida.jpg", ancho=320,
         prompt="Crea la gran lámpara de aceite de un faro vista desde arriba: anillos concéntricos de cristal tipo Fresnel y un quemador de latón en el centro, encendida con una luz dorada intensa y un halo cálido." + NEGRO),
    dict(destino=D + "espejos/galeria.jpg", ancho=320,
         prompt="Crea un farolillo marino de latón con cristal y una llama pequeña, como los de la galería exterior de un faro, visto desde arriba." + NEGRO),
    dict(destino=D + "espejos/lente.jpg", ancho=320,
         prompt="Crea una lente de Fresnel pequeña: un disco de cristal con anillos concéntricos y soporte de latón, vista desde arriba, brillando suavemente." + NEGRO),
    dict(destino=D + "espejos/foco.jpg", ancho=320,
         prompt="Crea un foco de linterna de latón con un cono de luz dorada saliendo hacia la derecha, visto desde arriba." + NEGRO),
    dict(destino=D + "espejos/roca.jpg", ancho=320,
         prompt="Crea una roca oscura, húmeda y rugosa con un poco de musgo, vista desde arriba." + NEGRO),
    # --- carta 95: panel de arranque (5 pasos) ---
    dict(destino=D + "arranque", ancho=260, hoja=(5, 1), nombres=["valvula", "mecha", "engranaje", "piloto", "freno"],
         prompt="Crea UNA SOLA IMAGEN apaisada con CINCO objetos en una sola fila horizontal, muy separados entre sí, cada uno centrado y del mismo tamaño, de izquierda a derecha: "
                "1) el volante de latón de una válvula de aceite con un trozo de tubería, 2) una mecha de algodón trenzada en un soporte de latón, "
                "3) un engranaje grande de latón, 4) un pequeño quemador de gas con una llama piloto azul y amarilla, 5) una palanca de freno de hierro con zapata. "
                "Vistos de frente, estilo pintura realista detallada." + NEGRO),
    # --- carta 52: ventana de señales (lámpara que parpadea) ---
    dict(destino=D + "morse", ancho=360, hoja=(2, 1), nombres=["linterna-apagada", "linterna-encendida"],
         prompt="Crea UNA SOLA IMAGEN apaisada con DOS objetos lado a lado, muy separados, del mismo tamaño: a la izquierda una linterna de señales de barco de latón con "
                "una gran lente redonda delantera, APAGADA y oscura; a la derecha la MISMA linterna ENCENDIDA, con la lente brillando blanco-amarillo y un halo de luz intenso. "
                "Vistas de frente, estilo pintura realista detallada." + NEGRO),
    # --- carta 85: radio de onda corta ---
    dict(destino=D + "radio-madera.jpg", ancho=720,
         prompt="Crea una textura de chapa de madera de nogal lustrada, vista de frente y plana, con un marco fino de latón en los bordes y el centro liso y limpio, como el frente de una radio antigua. "
                "Sin texto, letras ni números. Sin personas. Formato apaisado 3:2."),
    dict(destino=D + "radio-perilla.jpg", ancho=240,
         prompt="Crea una perilla de radio antigua de baquelita oscura con un anillo de latón y marcas finas en el borde, vista desde arriba." + NEGRO),
    # --- papel del cuaderno (lectores) ---
    dict(destino=D + "papel.jpg", ancho=720,
         prompt="Crea una textura de página de cuaderno antiguo de marino: papel amarillento con manchas de humedad y líneas finas, borde envejecido y el centro liso y limpio. "
                "Vista cenital plana. Sin texto, letras ni números. Sin personas. Formato vertical 2:3."),
    # --- carta 36: puerta de la escalera (teclado) ---
    dict(destino=D + "f36.jpg", ancho=720,
         prompt="Crea una textura de puerta de hierro de faro, vista de frente y plana, con una gran placa de latón rectangular con remaches en el centro, óxido y salitre en los bordes. "
                "Sin texto, letras ni números. Sin personas. Formato vertical 2:3."),
]
