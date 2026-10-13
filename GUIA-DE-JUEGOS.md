# Guía de diseño: cómo crear un juego Unlock nuevo

El juego de referencia es **El Faro de Cabo Niebla** (`Unlock-El-Faro/`). Sigue su patrón: su flujo está comprobado y los manuales de las aventuras salen del mismo método.

## 1. Reglas de diseño (innegociables)

1. **Toda carta sirve para algo.** Si no la necesita ningún puzle, o se le da una función real (una pista impresa que otro paso consume) o se quita. Nada de cartas de relleno.
2. **Tres tipos de carta:** normal (gris), de app (verde) y de combinar (roja/azul). No hay cartas «herramienta».
3. **Combinar = sumar.** Los números de las dos cartas se suman y el resultado es la carta que se coge (`18 + 22 = 40`). Elige los números para que cuadren y comprueba que no haya sumas accidentales entre cartas combinables que coincidan en la mesa.
4. **Los descartes se imprimen en la carta que se obtiene** (cambio de escena, combinación o minijuego), junto al «Coge». Lo que aún hará falta se conserva; lo usado se descarta. Si un minijuego no da carta nueva, el mensaje de la app manda descartar.
5. **Nunca se imprime en una carta el número de otra que el jugador aún no puede tener.** Los números solo aparecen en la franja de la carta que se acaba de coger o en el mensaje del minijuego al resolverlo.
6. **Una carta que descarta otra debe poder descartarla siempre**, en cualquier orden legal de juego.
7. **Las ilustraciones no llevan texto.** El número, el título, las franjas y los textos los pone `imprimir.html` / el Modo PC.
8. **Un minijuego no debe delatar la respuesta:** sin medidores de cercanía ni cintas con la solución. La guía son las cartas (y, si procede, el sonido).

## 2. Anatomía de un juego

```
index.html      shell de la app: temporizador, Acción, Pista, vídeo de inicio, Modo PC
pc.html         mesa virtual: mazo boca abajo, mesa, descartes
cartas.json     guion completo (ver §3)
pistas.js       visor de pistas (genérico, lee cartas.json)
style.css       estilos
juegos/         ui.js (base común) + un módulo por minijuego; lector.js para cartas de solo lectura
img/            ilustraciones JPG (520 px) usadas por el Modo PC e imprimir.html
video/          videoInicial.mp4 (opcional: si no está, la partida empieza sin vídeo)
MANUAL.md       manual de partida generado y verificado
```

Cada minijuego exporta `startMinigame(opts)` y se registra en el mapa `MINIGAMES` de `index.html` (`'36': './juegos/36-puerta.js'`). Usa `openGame` de `ui.js`; los lectores no pausan el temporizador.

## 3. `cartas.json`

Por carta (la clave es el número, `P` para la inicial):

| Campo | Qué es |
|---|---|
| `titulo` | `Carta N — Nombre` |
| `tipo` | `gris`, `verde`, `roja` o `azul` |
| `coge` | números que se cogen al leer la carta (se imprimen en la franja) |
| `descarta` | números que se descartan al obtenerla (franja) |
| `combina` | `[pareja, resultado]` en las cartas de combinar |
| `descripcion` | notas del diseñador (no se imprimen) |
| `pistas` | pistas progresivas; la última da la solución |
| `textoCarta` | texto impreso sobre la ilustración (3 líneas como máximo, sin números de otras cartas) |
| `arte` | descripción de la ilustración para ChatGPT |

`_meta` lleva el nombre del juego, el estilo, los personajes, la hoja de personajes, la foto de referencia y el prompt del vídeo.

## 4. Flujo de diseño

1. Dibuja el **grafo**: escenas (cartas que reparten otras), cartas de app (cada una exige datos de otras y da una carta nueva), combinaciones y el final.
2. Reparte las **pistas** en cartas físicas (texto impreso) y en lectores de la app, de modo que cada puzle necesite al menos una pista de otra carta.
3. Asigna **números** que cumplan las sumas, que ninguna pareja de cartas combinables sume el número de otra carta (el verificador lo detecta) y que ningún dato impreso (`17 deben`, `código 173`) coincida con el número de una carta del juego.
4. Escribe los **descartes** en la carta obtenida.
5. Escribe cada minijuego con su mensaje final «Coged la carta N» (y «Descartad…» si procede).
6. **Verifica** (§5) y genera el manual.

## 5. Verificación (antes de dar un juego por terminado)

1. `herramientas/verificar.py`: simula 3.000 partidas en orden aleatorio legal. Falla si una partida se atasca, si una carta descarta algo que no se tiene o que aún hace falta, si hay números impresos antes de tiempo, si una suma no cuadra o si una carta no sirve para nada. Necesita un `spec_*.json` con las dependencias (`needs`) de las cartas que no salen de un «coge».
2. `herramientas/ejecutar_manual.py`: juega el manual completo en un navegador (Selenium + Chrome) con el Modo PC y la app reales y comprueba la mesa tras cada paso.
3. `herramientas/bot_aventuras.py` (o `bot_faro.py`): partida autónoma que solo hace lo que dicen las cartas y los mensajes. `herramientas/bot_azar.py`: **muchas partidas en orden aleatorio** (mínimo 10 por juego): cada semilla elige otro orden de leer, coger, descartar, combinar y resolver apps.
4. Relee todos los textos buscando referencias a cartas eliminadas o instrucciones contradictorias, y abre cada minijuego con el visor de pistas.
5. `herramientas/crear_manual_md.py` genera `MANUAL.md` a partir de los mismos pasos.

## 6. Ilustraciones y vídeo

`prompts.html` (en las aventuras) da el prompt de la hoja de personajes, el de cada carta y el del vídeo. Las imágenes se guardan en `arte/` (local), se convierten con `herramientas/preparar_imagenes.py` y se suben como `img/*.jpg`.

## 7. Publicación

- Ramas + Pull Request; `main` lo fusiona el dueño del repositorio.
- No uses archivos que empiecen por `_` (GitHub Pages los ignora).
- Añade archivos concretos, nunca `git add .`.
- Prueba con servidor local, no con `file://`.

## 8. Errores reales que ya nos pasaron (para no repetirlos)

- Una foto imprimía «Carta 33» antes de poder tenerla, y la 33 mandaba descartar cartas que aún no se tenían → regla 5 y 6.
- Una carta «herramienta» que no se usaba en ningún puzle → reglas 1 y 2.
- Una cinta de puntos y rayas bajo el morse y un medidor de señal en la radio hacían los puzles triviales → regla 8.
- `_ui.js` daba 404 en GitHub Pages por empezar con guion bajo.
- Un `git add .` subió el perfil de Chrome del script de ChatGPT a un repositorio público.
