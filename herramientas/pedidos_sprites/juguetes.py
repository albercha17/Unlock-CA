# Sprites de «El Cuarto de Leo, 1995» con ChatGPT: juguetes, dibujos de los cubos, estantería vacía y piezas de la marioneta.
ESTILO = (" Estilo de ilustración de animación 3D familiar y amable, como una película de juguetes que cobran vida: colores vivos y saturados, plástico brillante, "
          "madera pintada, tela con costuras, sin texto.")

PEDIDOS = [
    dict(destino="juegos/aventuras-ca/juguetes/img/ui", prefijo="spr-", hoja=(4, 4), ancho=360, clave="magenta",
         nombres=["patito", "tambor", "cohete", "libro", "pelota", "coche", "osito", "barco", "cubos", "cometa", "trompo", "xilofono", "dado", "robot", "caballito", "trenecito"],
         prompt="Crea una hoja con 16 juguetes de los años 90, en 4 filas de 4, cada uno entero y de frente. Fila 1: un patito de goma amarillo; un tambor rojo con rayas amarillas; "
                "un cohete de juguete blanco con aletas rojas y una ventanilla azul (apuntando hacia arriba); un libro de cuentos morado cerrado, puesto de pie. "
                "Fila 2: una pelota de playa roja y blanca; un coche de carreras azul visto de lado; un osito de peluche marrón sentado; un barco de vela rojo con una vela blanca. "
                "Fila 3: tres cubos de madera apilados con letras sin forma (colores rojo, azul y amarillo); una cometa de papel en forma de rombo con cola de lazos (colores naranja y blanco); "
                "un trompo de madera de colores; un xilófono de juguete de siete barras de colores con dos macillos. "
                "Fila 4: un dado grande blanco de seis caras con puntos negros; un robot de hojalata plateado; un caballito de madera balancín; un tren de juguete pequeño de madera." + ESTILO),
    dict(destino="juegos/aventuras-ca/juguetes/img/ui", prefijo="dib-", hoja=(3, 2), ancho=420, clave="magenta", modo="recorte",
         nombres=["perro", "barco", "casa", "sol", "cohete", "arbol"],
         prompt="Crea una hoja con 6 dibujos infantiles hechos con ceras de colores por un niño de cinco años, cada uno sobre su propia hoja de papel blanco CUADRADA, en 2 filas de 3. "
                "Dibujos: un perro marrón sobre la hierba con el sol; un barco rojo sobre olas azules; una casa amarilla con tejado rojo y chimenea; un sol amarillo sonriente con rayos; "
                "un cohete rojo y blanco con estrellas; un árbol verde con manzanas rojas. Trazos de cera gruesos, un poco torpes, colores vivos, que llenan toda la hoja de papel."),
    dict(destino="juegos/aventuras-ca/juguetes/img/ui", prefijo="", hoja=(1, 1), ancho=900, clave="magenta", modo="recorte", nombres=["estanteria-vacia"],
         prompt="Crea una estantería de madera pintada de color crema de un cuarto infantil de los años 90, vista exactamente de frente y sin perspectiva, con TRES baldas horizontales "
                "perfectamente rectas e igualmente espaciadas (la de abajo a ras del suelo, sin patas), con los laterales a ambos lados, completamente VACÍA, ocupando todo el encuadre. "
                "Fondo interior liso de madera clara. Formato horizontal 3:2." + ESTILO),
    dict(destino="juegos/aventuras-ca/juguetes/img/ui", prefijo="", hoja=(3, 1), ancho=360, clave="magenta", nombres=["pipo-cuerpo", "pipo-brazo", "pipo-pierna"],
         prompt="Crea tres piezas sueltas de un títere de cuerda de teatrillo infantil totalmente original llamado Pipo, todas del mismo tamaño relativo y de frente: "
                "1) el CUERPO: una cabeza redonda y sonriente de madera clara con mejillas rosadas, el pelo de lana naranja, una pequeña nariz redonda, un cuello fino, y un torso con una "
                "camiseta de rayas verdes y amarillas, hasta la cintura, SIN brazos ni piernas; 2) UN BRAZO: una manga a rayas verdes y amarillas con una mano de madera redonda, "
                "colgando recto hacia abajo (largo, vertical); 3) UNA PIERNA: un pantalón azul con un zapato naranja, colgando recta hacia abajo (larga, vertical). "
                "Todas con articulaciones redondas de madera visibles." + ESTILO),
]
