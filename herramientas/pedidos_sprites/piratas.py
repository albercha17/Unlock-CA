# Sprites de «Mar de las Brumas, 1715» con ChatGPT: barcos, barril, palmera, rosa de los vientos y los nueve símbolos grabados.
ESTILO = (" Estilo de ilustración de aventura pirata pintada a mano, con luz cálida, colores ricos, y detalles de madera, latón y cuerda.")

PEDIDOS = [
    dict(destino="juegos/aventuras-ca/piratas/img/ui", prefijo="spr-", hoja=(3, 2), ancho=360, clave="magenta",
         nombres=["fragata", "gaviota", "barril", "palmera", "rosa", "cofre"],
         prompt="Crea una hoja con 6 objetos de un juego de piratas, en 2 filas de 3, cada uno entero y de frente (o de tres cuartos), bien separados. Fila 1: una fragata de guerra enemiga "
                "de tres mástiles con velas rojizas oscuras y una bandera negra, vista de lado; una pequeña goleta pirata llamada La Gaviota con velas blancas y casco de madera dorada, vista de lado; "
                "un barril de madera con aros de hierro. Fila 2: una palmera tropical; una rosa de los vientos antigua de latón y pergamino con la N marcada (sin otras letras ni números); "
                "un cofre del tesoro de madera con herrajes cerrado." + ESTILO),
    dict(destino="juegos/aventuras-ca/piratas/img/ui", prefijo="sim-", hoja=(3, 3), ancho=300, clave="magenta",
         nombres=["ancla", "calavera", "campana", "corona", "espada", "estrella", "llave", "luna", "pez"],
         prompt="Crea una hoja con 9 símbolos de oro viejo grabados en relieve, en 3 filas de 3, cada uno de frente y bien separado: un ancla; una calavera; una campana; una corona; "
                "una espada recta en vertical; una estrella de cinco puntas; una llave antigua; una luna en cuarto creciente; un pez. Metal dorado desgastado con brillos cálidos." + ESTILO),
]
