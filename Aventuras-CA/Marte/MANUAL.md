# Manual de partida — Marte, 2157 — Cúpula Aurora

> Este recorrido se ha ejecutado paso a paso en la web (Modo PC + app) con `herramientas/ejecutar_manual.py`: tras cada paso la mesa queda exactamente como se indica y la partida termina con solo la carta final en la mesa.

## Preparación

- **PC:** abre el juego, pulsa *Modo PC* (o *Reiniciar* si ya habías jugado). Debe haber la carta **P** en la mesa y 18 cartas boca abajo en el mazo.
- **Móvil:** abre el juego y pulsa *Empezar* (arranca la hora). *Acción* abre un minijuego con el número de su carta y *Pista* da ayuda de esa carta.
- **Reglas:** «Coge» → a la mesa; «Descarta» → a los descartes (se pueden recuperar). Dos cartas con la etiqueta *Combina* se suman: el resultado es la carta que coges.

## Los 12 pasos

### Paso 1 — Llegada al hangar

Pon el Modo PC en el ordenador (solo debe haber la carta P en la mesa y el resto boca abajo en el mazo) y en el móvil abre el juego y pulsa Empezar. Lee la carta P: te manda coger la 10 y la 16.

- **La mesa queda con:** `P` `10` `16`
- [ ] Hecho

### Paso 2 — El hangar

Lee la carta 10. Descarta la P y coge 21, 25, 17, 23, 33 y 36. La nota (25) dice que el código no lleva el 2 ni el 5 y la tomatera (36), «Cada rama: 5 hojas».

- **La mesa queda con:** `10` `16` `17` `21` `23` `25` `33` `36`
- [ ] Hecho

### Paso 3 — Lee el diario en la app

En el móvil: Acción, 33. Pasa las 4 páginas: ahí está la amplitud de calibración. No hay nada que resolver y no pausa el tiempo.

- **En el móvil:** Acción → `33`
- **La mesa queda con:** `10` `16` `17` `21` `23` `25` `33` `36`
- [ ] Hecho

### Paso 4 — Hackea la terminal

En el móvil: Acción, 21. Con la pista de la nota (el código no lleva 2 ni 5, así que solo usa 1, 3, 4 y 6, sin repetir) prueba códigos y fíjate en ● y ○. El código es 4 1 6 3. El mensaje te dice que cojas la 44.

- **En el móvil:** Acción → `21`
- **La mesa queda con:** `10` `16` `17` `21` `23` `25` `33` `36` `44`
- [ ] Hecho

### Paso 5 — El pasillo

Lee la carta 44. Descarta 10, 21 y 25 y coge 52 y 28. El plano (28) dice que el código de la esclusa es 173.

- **La mesa queda con:** `16` `17` `23` `28` `33` `36` `44` `52`
- [ ] Hecho

### Paso 6 — Restaura el oxígeno

En el móvil: Acción, 52. Gira las tuberías hasta que el oxígeno llegue de la entrada (izquierda) a la salida (derecha). El mensaje te dice que cojas la 66.

- **En el móvil:** Acción → `52`
- **La mesa queda con:** `16` `17` `23` `28` `33` `36` `44` `52` `66`
- [ ] Hecho

### Paso 7 — Combina el traje

El traje sin casco (17) y el casco (23) son combinables: 17 + 23 = 40. Coge la 40 y léela: te manda descartar 17 y 23.

- **Suma:** `17 + 23 = 40`
- **La mesa queda con:** `16` `28` `33` `36` `40` `44` `52` `66`
- [ ] Hecho

### Paso 8 — Abre la esclusa

En el móvil: Acción, 66. El plano dice 173; en binario con 8 interruptores es 128 + 32 + 8 + 4 + 1 (10101101). Con el traje puesto, el mensaje te dice que cojas la 79.

- **En el móvil:** Acción → `66`
- **La mesa queda con:** `16` `28` `33` `36` `40` `44` `52` `66` `79`
- [ ] Hecho

### Paso 9 — La sala del reactor

Lee la carta 79. Descarta 44, 52, 66, 28 y 40 y coge la 54 (núcleo de fusión).

- **La mesa queda con:** `16` `33` `36` `54` `79`
- [ ] Hecho

### Paso 10 — Carga el Cronoportal

El Cronoportal (16) y el núcleo de fusión (54) son combinables: 16 + 54 = 70. Coge la 70 y léela: te manda descartar 16, 54 y 79 y coger la 88.

- **Suma:** `16 + 54 = 70`
- **La mesa queda con:** `33` `36` `70` `88`
- [ ] Hecho

### Paso 11 — Calibra el Cronoportal

En el móvil: Acción, 88. El diario dice amplitud 3 y la tomatera, 5 hojas por rama: frecuencia 5. Pulsa Calibrar. El mensaje te dice que cojas la 99.

- **En el móvil:** Acción → `88`
- **La mesa queda con:** `33` `36` `70` `88` `99`
- [ ] Hecho

### Paso 12 — Final

Lee la carta 99. Descarta 70, 88, 33 y 36. En la mesa solo queda la 99. ¡Fin!

- **La mesa queda con:** `99`
- [ ] Hecho

## Carta a carta

| Carta | Nombre | Tipo | Impreso en la carta | Para qué sirve | Paso |
|---|---|---|---|---|---|
| P | Llegada a la cúpula | Normal | Coge 10, 16 | Inicio: llegada al hangar. Te manda coger la 10 y la 16. | 1 |
| 10 | Hangar de la cúpula | Normal | Coge 21, 25, 17, 23, 33, 36; Descarta P | El hangar: reparte las cartas del hangar y te quita la P. | 1 |
| 16 | Cronoportal sin energía | Combina | Combinable: suma los números | El Cronoportal sin energía: se combina con el núcleo de fusión (54). | 1 |
| 17 | Traje sin casco | Combina | Combinable: suma los números | Traje sin casco: se combina con el casco (23). | 2 |
| 21 | Terminal de seguridad | App | — | Terminal de seguridad (app): código de 4 cifras tipo Mastermind. | 2 |
| 23 | Casco de astronauta | Combina | Combinable: suma los números | Casco: se combina con el traje (17). | 2 |
| 25 | Nota adhesiva | Normal | Texto: «No lleva el 2 ni el 5» | Nota adhesiva: el código no lleva 2 ni 5. | 2 |
| 28 | Plano de la cúpula | Normal | Texto: «Esclusa del reactor: código 173» | Plano: el código de la esclusa es 173. | 5 |
| 33 | Diario de la doctora Reyes | App | — | Diario de la doctora Reyes (app, solo lectura): amplitud 3 del calibrador. | 2 |
| 36 | Tomatera | Normal | Texto: «Cada rama: 5 hojas» | Tomatera: «Cada rama: 5 hojas» = frecuencia 5 del calibrador. | 2 |
| 40 | Traje completo | Normal | Descarta 17, 23 | Traje completo: resultado de 17 + 23; hace falta para la esclusa. | 7 |
| 44 | Pasillo de la cúpula | Normal | Coge 52, 28; Descarta 10, 21, 25 | Pasillo de la cúpula: aparece al abrir la terminal. | 4 |
| 52 | Panel de oxígeno | App | — | Panel de oxígeno (app): girar tuberías de la entrada a la salida. | 5 |
| 54 | Núcleo de fusión | Combina | Combinable: suma los números | Núcleo de fusión: se combina con el Cronoportal (16). | 9 |
| 66 | Esclusa del reactor | App | — | Esclusa del reactor (app): 173 en binario con 8 interruptores. | 6 |
| 70 | Cronoportal cargado | Normal | Coge 88; Descarta 16, 54, 79 | Cronoportal cargado: resultado de 16 + 54. | 10 |
| 79 | Sala del reactor | Normal | Coge 54; Descarta 44, 52, 66, 28, 40 | Sala del reactor: aparece al abrir la esclusa. | 8 |
| 88 | Calibrador del Cronoportal | App | — | Calibrador (app): amplitud 3 y frecuencia 5. | 10 |
| 99 | De vuelta a casa (FIN) | Normal | Descarta 70, 88, 33, 36 | Final de la aventura. | 11 |

## Si algo no cuadra

- **«No se pudo cargar el minijuego»:** la web aún no se ha actualizado. Espera un par de minutos y recarga con Ctrl+F5.
- **El Modo PC no deja coger una carta:** ya la tienes en la mesa o está en los descartes.
- **Una carta manda descartar algo que no tienes:** te has saltado un paso; vuelve al último paso hecho.
