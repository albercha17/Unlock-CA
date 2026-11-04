# Sprites de Fútbol (escudos y camiseta), Espía (cables) y Arcade (monedas, espectros y frutas) con ChatGPT.
PEDIDOS = [
    dict(destino="juegos/aventuras-ca/futbol/img/ui", prefijo="esc-", hoja=(3, 3), ancho=260, clave="magenta",
         nombres=["estrella", "rayos", "halcones", "tigres", "delfines", "lobos", "osos", "condores", "camiseta"],
         prompt="Crea una hoja con 9 piezas de un juego de fútbol de los años 70, en 3 filas de 3, cada una entera y de frente: ocho escudos de equipo (redondeados, con borde dorado, "
                "diseño sencillo y original, sin letras): 1) una estrella dorada sobre fondo azul; 2) dos rayos amarillos sobre fondo negro y rojo; 3) la cabeza de un halcón sobre fondo verde; "
                "4) la cabeza de un tigre sobre fondo naranja; 5) un delfín saltando sobre fondo celeste; 6) la cabeza de un lobo gris sobre fondo morado; 7) un oso pardo sobre fondo marrón; "
                "8) un cóndor con las alas abiertas sobre fondo blanco y rojo; y la novena pieza: 9) una camiseta de fútbol retro de rayas verticales rojas y blancas, de frente, sin número ni escudo. "
                "Estilo de ilustración pintada a mano, colores vivos."),
    dict(destino="juegos/aventuras-ca/espia/img/ui", prefijo="cab-", hoja=(1, 5), ancho=420, clave="verde",
         nombres=["rojo", "azul", "amarillo", "negro", "blanco"],
         prompt="Crea cinco cables eléctricos gruesos, rectos y horizontales, cada uno en su fila (5 filas) y de un solo color: uno rojo, uno azul, uno amarillo, uno negro y uno blanco, "
                "con un terminal metálico plateado en cada extremo y un poco de cobre pelado, estilo de ilustración de espionaje de los años 60, bien separados entre sí."),
    dict(destino="juegos/aventuras-ca/arcade/img/ui", prefijo="mon-", hoja=(4, 1), ancho=240, clave="magenta", nombres=["0", "1", "2", "3"],
         prompt="Crea cuatro monedas de metal de una máquina recreativa de los años 80, de frente, en una fila y de tamaños CRECIENTES de izquierda a derecha (la primera la más pequeña y la cuarta "
                "la más grande, con una diferencia de tamaño clara), de color plata con un rayo grabado en el centro y borde dentado. Estilo de ilustración brillante de neón."),
    dict(destino="juegos/aventuras-ca/arcade/img/ui", prefijo="arc-", hoja=(4, 2), ancho=260, clave="verde",
         nombres=["fant-rojo", "fant-rosa", "fant-cian", "fant-naranja", "fruta-cereza", "fruta-fresa", "fruta-naranja", "fruta-manzana"],
         prompt="Crea una hoja con 8 sprites originales de un juego recreativo de neón de los años 80, en 2 filas de 4, grandes y bien separados: fila 1, cuatro espectros redondeados con forma "
                "de gota y una cola ondulada, con dos ojos grandes y brillantes, uno rojo, uno rosa, uno cian y uno naranja; fila 2, cuatro frutas brillantes: una cereza, una fresa, una naranja y una manzana roja, todas SIN ninguna hoja ni tallo verde (tallos marrones). "
                "Estilo de pixel art grande y limpio con brillos de neón."),
]
