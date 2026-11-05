# Manual de partida — El primer salto

> Este recorrido se ha ejecutado paso a paso en la web (Modo PC + app) con `herramientas/ejecutar_manual.py`: tras cada paso la mesa queda exactamente como se indica y la partida termina con solo la carta final en la mesa.

## Preparación

- **PC:** abre el juego, pulsa *Modo PC* (o *Reiniciar* si ya habías jugado). Debe haber la carta **P** en la mesa y 16 cartas boca abajo en el mazo.
- **Móvil:** abre el juego y pulsa *Empezar* (arranca la hora). *Acción* abre un minijuego con el número de su carta y *Pista* da ayuda de esa carta.
- **Reglas:** «Coge» → a la mesa; «Descarta» → a los descartes (se pueden recuperar). Dos cartas con la etiqueta *Combina* se suman: el resultado es la carta que coges.

## Los 10 pasos

### Paso 1 — El primer salto

Pon el Modo PC (solo la P en la mesa) y en el móvil pulsa Empezar. Lee la carta P: coge la 10 y la 12.

- **La mesa queda con:** `P` `10` `12`
- [ ] Hecho

### Paso 2 — El taller del salón

Lee la carta 10. Descarta la P y coge 14, 16, 21 y 22.

- **La mesa queda con:** `10` `12` `14` `16` `21` `22`
- [ ] Hecho

### Paso 3 — La vitrina del cristal

En el móvil: Acción, 14. Cuenta los engranajes de la pizarra (16): rojos, azules y amarillos; el código es 352. El mensaje te dice que cojas la 24. Apunta la cifra de la vitrina: 4.

- **En el móvil:** Acción → `14`
- **La mesa queda con:** `10` `12` `14` `16` `21` `22` `24`
- [ ] Hecho

### Paso 4 — La vitrina se abre

Lee la carta 24. Descarta 10, 14 y 16 y coge 18, 19 y 20. Junta el plano: 19 arriba y 21 abajo.

- **La mesa queda con:** `12` `18` `19` `20` `21` `22` `24`
- [ ] Hecho

### Paso 5 — Calibrar el portal

En el móvil: Acción, 20. Sigue el camino del plano (19 y 21): toca, en orden, reloj, luna, estrella, sol. El mensaje te dice que cojas la 28. Apunta la cifra del plano: 7.

- **En el móvil:** Acción → `20`
- **La mesa queda con:** `12` `18` `19` `20` `21` `22` `24` `28`
- [ ] Hecho

### Paso 6 — El portal se calibra

Lee la carta 28. Descarta 18, 19, 20, 21 y 24 y coge 86 y 35.

- **La mesa queda con:** `12` `22` `28` `35` `86`
- [ ] Hecho

### Paso 7 — El cristal

La mitad del cristal (22) y la otra mitad (35) son combinables: 22 + 35 = 57. Coge la 57.

- **Suma:** `22 + 35 = 57`
- **La mesa queda con:** `12` `22` `28` `35` `57` `86`
- [ ] Hecho

### Paso 8 — ¡El primer salto!

Lee la carta 57. Descarta 22, 35, 12 y 28 y coge la 85.

- **La mesa queda con:** `57` `85` `86`
- [ ] Hecho

### Paso 9 — El panel de vuelta

En el móvil: Acción, 85. Con el orden de la carta 86 (primero el plano, luego la vitrina), marca 74. El mensaje te dice que cojas la 99.

- **En el móvil:** Acción → `85`
- **La mesa queda con:** `57` `85` `86` `99`
- [ ] Hecho

### Paso 10 — Final

Lee la carta 99. Descarta 57, 85 y 86. En la mesa solo queda la 99. ¡Fin!

- **La mesa queda con:** `99`
- [ ] Hecho

## Carta a carta

| Carta | Nombre | Tipo | Impreso en la carta | Para qué sirve | Paso |
|---|---|---|---|---|---|
| P | El primer salto | Normal | Coge 10, 12 | El primer salto | 1 |
| 10 | El taller del salón | Normal | Coge 14, 16, 21, 22; Descarta P | El taller del salón | 1 |
| 12 | Cronoportal sin cristal | Normal | — | Cronoportal sin cristal | 1 |
| 14 | La vitrina del cristal | App | — | La vitrina del cristal | 2 |
| 16 | La pizarra de Alberto | Normal | — | La pizarra de Alberto | 2 |
| 18 | La nota de Cristina | Normal | — | La nota de Cristina | 4 |
| 19 | El plano del Umbral (mitad de arriba) | Normal | — | El plano del Umbral (mitad de arriba) | 4 |
| 20 | Calibrar el portal | App | — | Calibrar el portal | 4 |
| 21 | El plano del Umbral (mitad de abajo) | Normal | — | El plano del Umbral (mitad de abajo) | 2 |
| 22 | Mitad del cristal | Combina | Combinable: suma los números | Mitad del cristal | 2 |
| 24 | La vitrina se abre | Normal | Coge 18, 19, 20; Descarta 10, 14, 16 | La vitrina se abre | 3 |
| 28 | El portal se calibra | Normal | Coge 86, 35; Descarta 18, 19, 20, 21, 24 | El portal se calibra | 5 |
| 35 | La otra mitad del cristal | Combina | Combinable: suma los números | La otra mitad del cristal | 6 |
| 57 | ¡El primer salto! | Normal | Coge 85; Descarta 22, 35, 12, 28 | ¡El primer salto! | 7 |
| 85 | El panel de vuelta | App | — | El panel de vuelta | 8 |
| 86 | El orden del panel | Normal | — | El orden del panel | 6 |
| 99 | De vuelta a casa (FIN) | Normal | Descarta 57, 85, 86 | De vuelta a casa (FIN) | 9 |

## Si algo no cuadra

- **«No se pudo cargar el minijuego»:** la web aún no se ha actualizado. Espera un par de minutos y recarga con Ctrl+F5.
- **El Modo PC no deja coger una carta:** ya la tienes en la mesa o está en los descartes.
- **Una carta manda descartar algo que no tienes:** te has saltado un paso; vuelve al último paso hecho.
