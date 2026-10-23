# Manual de partida — Game Over, 1985 — La Última Moneda

> Este recorrido se ha ejecutado paso a paso en la web (Modo PC + app) con `herramientas/ejecutar_manual.py`: tras cada paso la mesa queda exactamente como se indica y la partida termina con solo la carta final en la mesa.

## Preparación

- **PC:** abre el juego, pulsa *Modo PC* (o *Reiniciar* si ya habías jugado). Debe haber la carta **P** en la mesa y 59 cartas boca abajo en el mazo.
- **Móvil:** abre el juego y pulsa *Empezar* (arranca la hora). *Acción* abre un minijuego con el número de su carta y *Pista* da ayuda de esa carta.
- **Reglas:** «Coge» → a la mesa; «Descarta» → a los descartes (se pueden recuperar). Dos cartas con la etiqueta *Combina* se suman: el resultado es la carta que coges.

## Los 30 pasos

### Paso 1 — Llegada

Pon el Modo PC (solo la P en la mesa) y en el móvil pulsa Empezar. Lee la carta P: coge la 10 y la 12.

- **La mesa queda con:** `P` `10` `12`
- [ ] Hecho

### Paso 2 — La placa base

Lee la carta 10. Descarta la P y coge 14, 16, 18, 19, 20 y 22. Junta el aparcamiento: 19 arriba y 21 abajo.

- **La mesa queda con:** `10` `12` `14` `16` `18` `19` `20` `22`
- [ ] Hecho

### Paso 3 — El panel de interruptores

En el móvil: Acción, 14. Con el esquema (16): interruptores arriba (1): C, D; abajo (0): A, B, E, F. El mensaje te dice que cojas la 24. Anota el byte de la máquina: 6.

- **En el móvil:** Acción → `14`
- **La mesa queda con:** `10` `12` `14` `16` `18` `19` `20` `22` `24`
- [ ] Hecho

### Paso 4 — La placa se enciende

Lee la carta 24. Descarta 14 y 16 y coge 26 y 21 (guárdala para la tabla de récords).

- **La mesa queda con:** `10` `12` `18` `19` `20` `21` `22` `24` `26`
- [ ] Hecho

### Paso 5 — El aparcamiento de naves

En el móvil: Acción, 20. Con el plano (19 y 21) y el acertijo (18), saca la nave 1 en 18 movimientos: nave 2 a la izquierda; nave 4 a la izquierda (2 casillas); nave 5 a la izquierda (2 casillas); nave 7 hacia arriba (2 casillas); nave 6 a la derecha; nave 3 hacia arriba; nave 2 a la izquierda; nave 3 hacia arriba (2 casillas); nave 6 a la izquierda; nave 7 hacia abajo (3 casillas); nave 1 a la derecha (2 casillas). El mensaje te dice que cojas la 28.

- **En el móvil:** Acción → `20`
- **La mesa queda con:** `10` `12` `18` `19` `20` `21` `22` `24` `26` `28`
- [ ] Hecho

### Paso 6 — El aparcamiento despejado

Lee la carta 28. Descarta 18, 19, 20 y 21 y coge la 35.

- **La mesa queda con:** `10` `12` `22` `24` `26` `28` `35`
- [ ] Hecho

### Paso 7 — El joystick

El mango (22) y la bola (35) son combinables: 22 + 35 = 57. Coge la 57.

- **Suma:** `22 + 35 = 57`
- **La mesa queda con:** `10` `12` `22` `24` `26` `28` `35` `57`
- [ ] Hecho

### Paso 8 — El joystick gigante

Lee la carta 57. Descarta 22, 35, 10 y 28 y coge 31 y 32.

- **La mesa queda con:** `12` `24` `26` `31` `32` `57`
- [ ] Hecho

### Paso 9 — El taller de sprites

Lee la carta 31. Coge 40, 41, 43 y 45.

- **La mesa queda con:** `12` `24` `26` `31` `32` `40` `41` `43` `45` `57`
- [ ] Hecho

### Paso 10 — La pantalla de sprites

En el móvil: Acción, 40. Con las tandas (41 y 43) y la regla (45), el fantasmita fila por fila ('#' encendida): ....####.... / ..########.. / .##########. / ###..##..### / ###..##..### / ############ / ############ / ############ / ############ / ##.##..##.## / #...#..#...# / ............. El mensaje te dice que cojas la 30. Anota el byte de la máquina: 11.

- **En el móvil:** Acción → `40`
- **La mesa queda con:** `12` `24` `26` `30` `31` `32` `40` `41` `43` `45` `57`
- [ ] Hecho

### Paso 11 — El sprite aprobado

Lee la carta 30. Descarta 31, 40, 41, 43 y 45 y coge la 38.

- **La mesa queda con:** `12` `24` `26` `30` `32` `38` `57`
- [ ] Hecho

### Paso 12 — La consola de mensajes

Lee la carta 32. Coge 42, 48, 49, 53 y 63.

- **La mesa queda con:** `12` `24` `26` `30` `32` `38` `42` `48` `49` `53` `57` `63`
- [ ] Hecho

### Paso 13 — La consola de mensajes

En el móvil: Acción, 48. Con los bytes (42), la tabla (49) y la regla (53), el mensaje es CONTINUE. El mensaje te dice que cojas la 36.

- **En el móvil:** Acción → `48`
- **La mesa queda con:** `12` `24` `26` `30` `32` `36` `38` `42` `48` `49` `53` `57` `63`
- [ ] Hecho

### Paso 14 — El menú de los fantasmas

Lee la carta 36. Descarta 32, 42, 48, 49 y 53 y coge 52, 54, 55 y 59.

- **La mesa queda con:** `12` `24` `26` `30` `36` `38` `52` `54` `55` `57` `59` `63`
- [ ] Hecho

### Paso 15 — Los cuatro fantasmas

En el móvil: Acción, 52. Con las pistas (54 y 55) y el plano (59): pasillo 1: fantasma rosa, rápido, fruta naranja; pasillo 2: fantasma cian, loco, fruta manzana; pasillo 3: fantasma rojo, lento, fruta cereza; pasillo 4: fantasma naranja, normal, fruta fresa. El mensaje te dice que cojas la 44. Anota el byte de la máquina: 9.

- **En el móvil:** Acción → `52`
- **La mesa queda con:** `12` `24` `26` `30` `36` `38` `44` `52` `54` `55` `57` `59` `63`
- [ ] Hecho

### Paso 16 — La sala de puntuaciones

Lee la carta 44. Descarta 36, 52, 54, 55 y 59 y coge 33, 37, 39, 46, 51 y 61. Junta la tabla de récords: 61 arriba y 63 abajo.

- **La mesa queda con:** `12` `24` `26` `30` `33` `37` `38` `39` `44` `46` `51` `57` `61` `63`
- [ ] Hecho

### Paso 17 — El marcador del jefe

En el móvil: Acción, 46. Con los números puestos (37), la regla (39) y las fichas (33), el cuadrado fila por fila: 16 10 5 3 / 1 7 12 14 / 4 6 9 15 / 13 11 8 2. El mensaje te dice que cojas la 56.

- **En el móvil:** Acción → `46`
- **La mesa queda con:** `12` `24` `26` `30` `33` `37` `38` `39` `44` `46` `51` `56` `57` `61` `63`
- [ ] Hecho

### Paso 18 — La tabla de récords

En el móvil: Acción, 51. Con la nota (26) y la tabla (61 y 63), de arriba abajo: verde, naranja, rosa, amarillo, violeta, cian, rojo, blanco. El mensaje te dice que cojas la 58.

- **En el móvil:** Acción → `51`
- **La mesa queda con:** `12` `24` `26` `30` `33` `37` `38` `39` `44` `46` `51` `56` `57` `58` `61` `63`
- [ ] Hecho

### Paso 19 — La ranura de los récords

Lee la carta 58. Descarta 51, 61, 63, 26 y 24 y coge 69, 70 y 71.

- **La mesa queda con:** `12` `30` `33` `37` `38` `39` `44` `46` `56` `57` `58` `69` `70` `71`
- [ ] Hecho

### Paso 20 — La rana de la autopista

En el móvil: Acción, 69. Con la autopista (70) y las velocidades (71), programa: LULLUWUULUU. El mensaje te dice que cojas la 80. Anota el byte de la máquina: 12.

- **En el móvil:** Acción → `69`
- **La mesa queda con:** `12` `30` `33` `37` `38` `39` `44` `46` `56` `57` `58` `69` `70` `71` `80`
- [ ] Hecho

### Paso 21 — El almacén de monedas

Lee la carta 80. Descarta 58, 69, 70 y 71 y coge 72, 75 y 79.

- **La mesa queda con:** `12` `30` `33` `37` `38` `39` `44` `46` `56` `57` `72` `75` `79` `80`
- [ ] Hecho

### Paso 22 — La máquina de cambio

En el móvil: Acción, 72. Con las monedas (75) y el precio (79): 2 de 1 y 2 de 16. El mensaje te dice que cojas la 82.

- **En el móvil:** Acción → `72`
- **La mesa queda con:** `12` `30` `33` `37` `38` `39` `44` `46` `56` `57` `72` `75` `79` `80` `82`
- [ ] Hecho

### Paso 23 — La ranura de continuar

Lee la carta 82. Descarta 80, 72, 75 y 79 y coge 85, 86, 87 y 67.

- **La mesa queda con:** `12` `30` `33` `37` `38` `39` `44` `46` `56` `57` `67` `82` `85` `86` `87`
- [ ] Hecho

### Paso 24 — La llave del jefe

Las dos mitades de la llave (38 y 56) son combinables: 38 + 56 = 94. Coge la 94.

- **Suma:** `38 + 56 = 94`
- **La mesa queda con:** `12` `30` `33` `37` `38` `39` `44` `46` `56` `57` `67` `82` `85` `86` `87` `94`
- [ ] Hecho

### Paso 25 — La sala del jefe final

Lee la carta 94. Descarta 38, 56, 30, 44, 33, 37, 39 y 46 y coge 64 y 66. Junta el dibujo final: 66 arriba y 67 abajo.

- **La mesa queda con:** `12` `57` `64` `66` `67` `82` `85` `86` `87` `94`
- [ ] Hecho

### Paso 26 — El cerrojo deslizante

En el móvil: Acción, 64. Con el dibujo final (66 y 67), las fichas quedan así: 1 2 3 / 8 _ 4 / 7 6 5. El mensaje te dice que cojas la 62.

- **En el móvil:** Acción → `64`
- **La mesa queda con:** `12` `57` `62` `64` `66` `67` `82` `85` `86` `87` `94`
- [ ] Hecho

### Paso 27 — El cristal

El Cronoportal (12) y el cristal (62) son combinables: 12 + 62 = 74. Coge la 74.

- **Suma:** `12 + 62 = 74`
- **La mesa queda con:** `12` `57` `62` `64` `66` `67` `74` `82` `85` `86` `87` `94`
- [ ] Hecho

### Paso 28 — Cronoportal con el cristal

Lee la carta 74. Descarta 62, 12, 64, 66, 67, 94 y 57.

- **La mesa queda con:** `74` `82` `85` `86` `87`
- [ ] Hecho

### Paso 29 — El arranque de la máquina

En el móvil: Acción, 85. Con las notas (86 y 87): 6 ^ 9 ^ 11 ^ 12 = 8. Apunta los cuatro bytes y la clave. El mensaje te dice que cojas la 99.

- **En el móvil:** Acción → `85`
- **La mesa queda con:** `74` `82` `85` `86` `87` `99`
- [ ] Hecho

### Paso 30 — Final

Lee la carta 99. Descarta 74, 82, 85, 86 y 87. En la mesa solo queda la 99. ¡Fin!

- **La mesa queda con:** `99`
- [ ] Hecho

## Carta a carta

| Carta | Nombre | Tipo | Impreso en la carta | Para qué sirve | Paso |
|---|---|---|---|---|---|
| P | Llegada a la recreativa | Normal | Coge 10, 12 | Llegada a la recreativa | 1 |
| 10 | La placa base | Normal | Coge 14, 16, 18, 19, 20, 22; Descarta P | La placa base | 1 |
| 12 | Cronoportal sin cristal | Combina | Combinable: suma los números | Cronoportal sin cristal | 1 |
| 14 | El panel de interruptores | App | — | El panel de interruptores | 2 |
| 16 | El circuito de la placa | Normal | — | El circuito de la placa | 2 |
| 18 | El acertijo del aparcamiento | Normal | — | El acertijo del aparcamiento | 2 |
| 19 | El aparcamiento de naves (mitad de arriba) | Normal | — | El aparcamiento de naves (mitad de arriba) | 2 |
| 20 | El aparcamiento de naves | App | — | El aparcamiento de naves | 2 |
| 21 | El aparcamiento de naves (mitad de abajo) | Normal | — | El aparcamiento de naves (mitad de abajo) | 4 |
| 22 | Mango de joystick | Combina | Combinable: suma los números | Mango de joystick | 2 |
| 24 | La placa se enciende | Normal | Coge 26, 21; Descarta 14, 16 | La placa se enciende | 3 |
| 26 | La nota del programador | Normal | — | La nota del programador | 4 |
| 28 | El aparcamiento despejado | Normal | Coge 35; Descarta 18, 19, 20, 21 | El aparcamiento despejado | 5 |
| 30 | El sprite aprobado | Normal | Coge 38; Descarta 31, 40, 41, 43, 45 | El sprite aprobado | 10 |
| 31 | El taller de sprites | Normal | Coge 40, 41, 43, 45 | El taller de sprites | 8 |
| 32 | La consola de mensajes | Normal | Coge 42, 48, 49, 53, 63 | La consola de mensajes | 8 |
| 33 | Las fichas de la bolsa | Normal | — | Las fichas de la bolsa | 16 |
| 35 | Bola del joystick | Combina | Combinable: suma los números | Bola del joystick | 6 |
| 36 | El menú de los fantasmas | Normal | Coge 52, 54, 55, 59; Descarta 32, 42, 48, 49, 53 | El menú de los fantasmas | 13 |
| 37 | El marcador del jefe | Normal | — | El marcador del jefe | 16 |
| 38 | Mitad de la llave del jefe | Combina | Combinable: suma los números | Mitad de la llave del jefe | 11 |
| 39 | La regla del marcador | Normal | — | La regla del marcador | 16 |
| 40 | La pantalla de sprites | App | — | La pantalla de sprites | 9 |
| 41 | Las tandas del sprite (I) | Normal | — | Las tandas del sprite (I) | 9 |
| 42 | Los bytes del mensaje | Normal | — | Los bytes del mensaje | 12 |
| 43 | Las tandas del sprite (II) | Normal | — | Las tandas del sprite (II) | 9 |
| 44 | La sala de puntuaciones | Normal | Coge 33, 37, 39, 46, 51, 61; Descarta 36, 52, 54, 55, 59 | La sala de puntuaciones | 15 |
| 45 | La regla de la compresión | Normal | — | La regla de la compresión | 9 |
| 46 | El marcador del jefe | App | — | El marcador del jefe | 16 |
| 48 | La consola de mensajes | App | — | La consola de mensajes | 12 |
| 49 | La tabla de caracteres | Normal | — | La tabla de caracteres | 12 |
| 51 | La tabla de récords | App | — | La tabla de récords | 16 |
| 52 | Los cuatro fantasmas | App | — | Los cuatro fantasmas | 14 |
| 53 | La regla de los bytes | Normal | — | La regla de los bytes | 12 |
| 54 | Las pistas de los fantasmas (I) | Normal | — | Las pistas de los fantasmas (I) | 14 |
| 55 | Las pistas de los fantasmas (II) | Normal | — | Las pistas de los fantasmas (II) | 14 |
| 56 | Otra mitad de la llave | Combina | Combinable: suma los números | Otra mitad de la llave | 17 |
| 57 | El joystick gigante | Normal | Coge 31, 32; Descarta 22, 35, 10, 28 | El joystick gigante | 7 |
| 58 | La ranura de los récords | Normal | Coge 69, 70, 71; Descarta 51, 61, 63, 26, 24 | La ranura de los récords | 18 |
| 59 | El plano de los pasillos | Normal | — | El plano de los pasillos | 14 |
| 61 | La tabla de récords (mitad de arriba) | Normal | — | La tabla de récords (mitad de arriba) | 16 |
| 62 | El cristal del Cronoportal | Combina | Combinable: suma los números | El cristal del Cronoportal | 26 |
| 63 | La tabla de récords (mitad de abajo) | Normal | — | La tabla de récords (mitad de abajo) | 12 |
| 64 | El cerrojo deslizante | App | — | El cerrojo deslizante | 25 |
| 66 | El dibujo final (mitad de arriba) | Normal | — | El dibujo final (mitad de arriba) | 25 |
| 67 | El dibujo final (mitad de abajo) | Normal | — | El dibujo final (mitad de abajo) | 23 |
| 69 | La rana de la autopista | App | — | La rana de la autopista | 19 |
| 70 | La autopista al empezar | Normal | — | La autopista al empezar | 19 |
| 71 | Las velocidades del tráfico | Normal | — | Las velocidades del tráfico | 19 |
| 72 | La máquina de cambio | App | — | La máquina de cambio | 21 |
| 74 | Cronoportal con el cristal | Normal | Descarta 62, 12, 64, 66, 67, 94, 57 | Cronoportal con el cristal | 27 |
| 75 | Las monedas de la máquina | Normal | — | Las monedas de la máquina | 21 |
| 79 | El precio de la partida | Normal | — | El precio de la partida | 21 |
| 80 | El almacén de monedas | Normal | Coge 72, 75, 79; Descarta 58, 69, 70, 71 | El almacén de monedas | 20 |
| 82 | La ranura de continuar | Normal | Coge 85, 86, 87, 67; Descarta 80, 72, 75, 79 | La ranura de continuar | 22 |
| 85 | El arranque de la máquina | App | — | El arranque de la máquina | 23 |
| 86 | La clave del arranque (I) | Normal | — | La clave del arranque (I) | 23 |
| 87 | La clave del arranque (II) | Normal | — | La clave del arranque (II) | 23 |
| 94 | La sala del jefe final | Normal | Coge 64, 66; Descarta 38, 56, 30, 44, 33, 37, 39, 46 | La sala del jefe final | 24 |
| 99 | De vuelta a casa (FIN) | Normal | Descarta 74, 82, 85, 86, 87 | De vuelta a casa (FIN) | 29 |

## Si algo no cuadra

- **«No se pudo cargar el minijuego»:** la web aún no se ha actualizado. Espera un par de minutos y recarga con Ctrl+F5.
- **El Modo PC no deja coger una carta:** ya la tienes en la mesa o está en los descartes.
- **Una carta manda descartar algo que no tienes:** te has saltado un paso; vuelve al último paso hecho.
