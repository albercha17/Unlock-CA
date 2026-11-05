# Sprites de «El primer salto» (nivel de prueba) con ChatGPT: los seis símbolos del plano y los engranajes de la pizarra.
ESTILO = (" Estilo de ilustración de aventura de ciencia ficción amable y luminosa: latón pulido, cristal azul brillante y detalles de relojería, colores vivos y limpios.")

PEDIDOS = [
    dict(destino="juegos/aventuras-ca/cronoportal/img/ui", prefijo="sim-", hoja=(3, 2), ancho=300, clave="magenta",
         nombres=["sol", "luna", "estrella", "llave", "reloj", "flor"],
         prompt="Crea una hoja con 6 símbolos grabados en relieve sobre medallones circulares de latón, en 2 filas de 3, cada uno entero, de frente y bien separado: "
                "un sol con rayos; una luna en cuarto creciente; una estrella de cinco puntas; una llave antigua; un reloj de bolsillo; una flor de cinco pétalos. "
                "Cada medallón de un color de fondo distinto y vivo (amarillo, azul oscuro, rojo, verde, naranja, rosa)." + ESTILO),
    dict(destino="juegos/aventuras-ca/cronoportal/img/ui", prefijo="eng-", hoja=(3, 1), ancho=300, clave="magenta", nombres=["rojo", "azul", "amarillo"],
         prompt="Crea tres engranajes de relojería idénticos en forma y tamaño, de frente, en una fila y bien separados, que solo se diferencian en el color: uno ROJO brillante, uno AZUL brillante "
                "y uno AMARILLO brillante, todos con 12 dientes, un eje de latón en el centro y un acabado metálico lacado." + ESTILO),
]
