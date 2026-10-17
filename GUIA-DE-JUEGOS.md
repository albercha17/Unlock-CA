# Guía de diseño: cómo crear un juego Unlock nuevo

El juego de referencia es **El Faro de Cabo Niebla** (`juegos/el-faro/`). Sigue su patrón: su flujo está comprobado y los manuales de las aventuras salen del mismo método.

## 0. Receta: crear un juego COMPLETO de una sola vez

Cuando se pida «crea un juego» (con o sin temática), se entrega **todo**, sin dejar fases para después:

1. **Diseño.** Tema, historia y grafo de cartas en 3 o 4 actos (más largo que el anterior), con al menos 7 puzles de app distintos y nuevos (ver la tabla de puzles ya usados en la [guía de puzles](GUIA-DE-PUZLES.md)). Las instancias (buscaminas, luces, dominó...) se generan con un script que **comprueba por fuerza bruta que la solución es única**. Cristina y Alberto salen siempre, con indumentaria de la época o del lugar (`PERSONAJES` y `HOJA` en `datos_<juego>.py`).
2. **Datos y construcción.** `herramientas/datos_<juego>.py` (`J`, `META`, `SPEC`, `PARA_QUE`, `PASOS`), una entrada en `JUEGOS` de `construir_aventuras.py` (tema, colores, minijuegos y `minutos` de partida) y el tema en `TEMAS` de `ui.js` (copiado a todos los juegos). Después `python herramientas/construir_aventuras.py <Juego>`.
3. **Pruebas del diseño.** `verificar.py` (3.000 partidas), `solvers_<juego>.py` + `ejecutar_manual.py`, `bot_azar.py` con 10 semillas, `probar_pistas.py`, `probar_impresion.py` y `crear_manual_md.py`.
4. **Imágenes de la interfaz.** `herramientas/pedidos/<juego>.py` con todos los objetos y texturas que usan los minijuegos y `python herramientas/chatgpt_fondos.py --solo <juego>`.
5. **Ilustraciones de las cartas.** `python herramientas/chatgpt_imagenes.py --conectar juegos/aventuras-ca/<juego>` (el Chrome se abre con `abrir_chrome_chatgpt.ps1`; avisa por si hay que iniciar sesión) y después `preparar_imagenes.py`. Revisa la hoja de contactos de las cartas.
6. **Minijuegos con interfaz.** Cada uno con sus imágenes reales (§6b), `capturar_minijuegos.py` revisado a ojo y `probar_apps.py` sin errores de consola. Repite el paso 3 con las imágenes ya puestas.
7. **Menú y documentación.** Tarjeta del juego en `juegos/aventuras-ca/index.html`, fila en `README.md`, el puzle nuevo en la tabla de la guía de puzles.
8. **Publicación.** Rama, commit con archivos concretos, push y Pull Request (nunca a `main`); al terminar, cerrar el servidor local y el Chrome de depuración.

## 1. Reglas de diseño (innegociables)

1. **Toda carta sirve para algo, y al final solo queda la carta final en la mesa** (todo lo demás se descarta). Si no la necesita ningún puzle, o se le da una función real (una pista impresa que otro paso consume) o se quita. Nada de cartas de relleno.
2. **Tres tipos de carta:** normal (gris), de app (verde) y de combinar (roja/azul). No hay cartas «herramienta».
3. **Combinar = sumar.** Los números de las dos cartas se suman y el resultado es la carta que se coge (`18 + 22 = 40`). Elige los números para que cuadren y comprueba que no haya sumas accidentales entre cartas combinables que coincidan en la mesa.
4. **Toda carta que haga coger o descartar lo dice, impreso en la propia carta** (franjas «Coge», «Descarta» y «Combinable: suma los números»), tanto en `imprimir.html` como en el Modo PC. Esto vale para **cualquier juego**, sin excepción. **Los descartes se imprimen en la carta que se obtiene** (cambio de escena, combinación o minijuego), junto al «Coge». Lo que aún hará falta se conserva; lo usado se descarta. Si un minijuego no da carta nueva, el mensaje de la app manda descartar.
5. **Nunca se imprime en una carta el número de otra que el jugador aún no puede tener.** Los números solo aparecen en la franja de la carta que se acaba de coger o en el mensaje del minijuego al resolverlo.
6. **Una carta que descarta otra debe poder descartarla siempre**, en cualquier orden legal de juego.
7. **Las ilustraciones no llevan texto.** El número, el título, las franjas y los textos los pone `imprimir.html` / el Modo PC.
8. **Un minijuego no debe delatar la respuesta:** sin medidores de cercanía ni cintas con la solución. La guía son las cartas (y, si procede, el sonido).
9. **Puzles y pistas visuales en las cartas.** Mucho de lo que el jugador resuelve debe estar en las propias cartas (cartas que se juntan y dan un número, ilustraciones que contienen la pista), no en texto largo ni en la app. Lo que enseña una ilustración no se repite en la app. Catálogo de ideas en GUIA-DE-PUZLES §7.21. Las franjas «Coge/Descarta» son una sola línea compacta para no tapar la ilustración.

## 2. Anatomía de un juego

```
index.html      estructura de la app + `window.APP_CONFIG` (segundos, carta final, mapa de minijuegos)
app.css / app.js  aspecto y lógica comunes de la app: inicio con reglas, reloj diegético, Acción, Pista, teclado con vista previa,
                cuaderno (registro + notas + reglas), guardado automático, pantalla final con informe, Wake Lock
precache.json   lista de ficheros del juego para el botón «Descargar para jugar sin conexión» (la genera `generar_pwa.py`)
musica.js       música de fondo generativa (WebAudio, sin archivos): un preset por tema en `PRESETS` (faro, egipto, marte, florencia,
                dinosaurios, cuento, trono, pompeya). Al crear un juego nuevo con tema propio, añade su preset (escala, tempo, instrumentos y ambiente)
                y prueba el sonido en `juegos/laboratorio/musica.html`. La app baja el volumen en minijuegos/pausas y tiene botón para quitarla.
pc.html         mesa virtual: mazo boca abajo, mesa, descartes
cartas.json     guion completo (ver §3)
cartas-data.js  copia generada de cartas.json para abrir pc/imprimir/prompts con doble clic (no editar)
pistas.js       visor de pistas (genérico, lee cartas.json)
style.css       estilos
minijuegos/     ui.js (base común) + un módulo por minijuego; lector.js para cartas de solo lectura
img/            ilustraciones JPG (520 px) usadas por el Modo PC e imprimir.html
video/          videoInicial.mp4 (opcional: si no está, la partida empieza sin vídeo)
MANUAL.md       manual de partida generado y verificado
```

Cada minijuego exporta `startMinigame(opts)` y se registra en `minijuegos` de `window.APP_CONFIG` en `index.html` (`'36': './minijuegos/36-puerta.js'`). La app (`index.html`, `app.css`, `app.js`) se edita **solo en `juegos/el-faro`** y se propaga con `python herramientas/regenerar_index.py`. Usa `openGame` de `ui.js`; los lectores no pausan el temporizador.

## 3. `cartas.json`

Por carta (la clave es el número, `P` para la inicial):

| Campo | Qué es |
|---|---|
| `titulo` | `Carta N — Nombre` |
| `tipo` | `gris`, `verde`, `roja` o `azul` |
| `coge` | números que se cogen al leer la carta (se imprimen en la franja) |
| `descarta` | números que se descartan al obtenerla (franja) |
| `combina` | `[pareja, resultado]` en las cartas de combinar. La pareja puede ser un **modificador** de la app (`["+9", 51]`): la carta se suma al número que da una máquina |
| `descripcion` | notas del diseñador (no se imprimen) |
| `pistas` | pistas progresivas; la última da la solución |
| `textoCarta` | texto impreso sobre la ilustración (3 líneas como máximo, sin números de otras cartas) |
| `textoEspejo` | `true` imprime el texto volteado como en un espejo (escritura de Leonardo): se lee con un espejo o con la cámara frontal del móvil |
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

0. `herramientas/probar_impresion.py`: comprueba que cada carta de `imprimir.html` muestra sus franjas Coge/Descarta/Combinable exactamente como dice `cartas.json`.
1. `herramientas/verificar.py`: simula 3.000 partidas en orden aleatorio legal. Falla si una partida se atasca, si al terminar no queda solo la carta final, si una carta descarta algo que no se tiene o que aún hace falta, si hay números impresos antes de tiempo, si una suma no cuadra o si una carta no sirve para nada. Necesita un `spec_*.json` con las dependencias (`needs`) de las cartas que no salen de un «coge».
2. `herramientas/ejecutar_manual.py`: juega el manual completo en un navegador (Selenium + Chrome) con el Modo PC y la app reales y comprueba la mesa tras cada paso.
3. `herramientas/bot_aventuras.py` (o `bot_faro.py`): partida autónoma que solo hace lo que dicen las cartas y los mensajes. `herramientas/bot_azar.py`: **muchas partidas en orden aleatorio** (mínimo 10 por juego): cada semilla elige otro orden de leer, coger, descartar, combinar y resolver apps.
4. Relee todos los textos buscando referencias a cartas eliminadas o instrucciones contradictorias, y abre cada minijuego con el visor de pistas.
5. `herramientas/crear_manual_md.py` genera `MANUAL.md` a partir de los mismos pasos.
6. `herramientas/sincronizar_cartas.py` regenera `cartas-data.js` (el verificador falla si está desfasado): sin él, `pc.html`/`imprimir.html` no cargan las cartas al abrirlos con doble clic.

## 6. Ilustraciones y vídeo

**Ropa distinta en cada juego, ambientada en la época.** La cara, el pelo y los rasgos de Cristina y Alberto salen de la hoja de personajes (`personajes/hoja.png`, ropa actual); la ropa la define `_meta.personajes` de cada juego (Egipto: ropa actual de viaje; Marte: monos de colonia marciana). Al crear un juego nuevo, escribe su vestuario en `personajes` y en la `hoja` de `datos_<juego>.py`.

**Generación automática con ChatGPT** (la hoja de personajes `personajes/hoja.png` solo da las caras; la ropa sale de `_meta.personajes` de cada juego): `herramientas/abrir_chrome_chatgpt.ps1` abre un Chrome normal (inicia sesión y pasa ahí la verificación «soy humano») y `python herramientas/chatgpt_imagenes.py --conectar juegos/aventuras-ca/<Juego>` genera y guarda todas las cartas. No cierres ese Chrome mientras trabaja.

**Expresiones distintas en cada imagen.** En el campo `arte` de cada carta, indica la emoción concreta de Cristina y de Alberto según la escena (sorpresa, concentración, miedo, alegría, duda, esfuerzo…). Evita el «sonríen» por defecto: con la misma cara en todas las cartas el juego se ve plano.

`prompts.html` (en las aventuras) da el prompt de la hoja de personajes, el de cada carta y el del vídeo. Las imágenes se guardan en `arte/` (local), se convierten con `herramientas/preparar_imagenes.py` y se suben como `img/*.jpg`.

## 6b. Aspecto de los minijuegos (ambientación)

Todos los minijuegos comparten `minijuegos/ui.js` (idéntico en cada juego) y cada juego tiene su **tema** (`<html data-tema="...">`):
fondo con la ilustración de la carta desenfocada, cabecera con la imagen, marco, tipografía, teclas, partículas ambientales
(lluvia y niebla en el Faro, polvo dorado en Egipto, polvo marciano y líneas de escaneo en Marte, chispas de vela en Florencia),
destello y sonido al acertar, sacudida al fallar y un botón de silencio (se recuerda en el móvil).

Para un juego nuevo:
1. Añade su tema al objeto `TEMAS` de `ui.js` (colores, tipografía, partículas, símbolo) y copia `ui.js` a las demás carpetas.
2. Pon `data-tema` en su `index.html` (el constructor lo hace con la clave `tema`).
3. Cada minijuego debe llamarse `Carta N — Nombre` (de ahí sale la imagen `img/N.jpg`) y usar solo `body`, `button`, `close`, `onClose`, `say` y `textura` de `openGame`.
4. Genera la textura de su panel y los gráficos de sus minijuegos con `herramientas/chatgpt_fondos.py`: cada juego tiene su catálogo en `herramientas/pedidos/<juego>.py`; el constructor deja un panel provisional en `img/ui/panel.jpg`.
5. **Nada de emojis ni dibujos planos en los minijuegos**: cada objeto (glifo, gema, tubería, engranaje...) es una imagen de ChatGPT.
   Los objetos se piden sobre fondo negro puro y se mezclan con `mix-blend-mode: screen` (el negro desaparece); las hojas con varios objetos se trocean solas.
   Ojo: un elemento con `transform` o `filter` aísla el mezclado; pon el `mix-blend-mode` en el propio elemento que gira, no en sus hijos.
6. Si un solucionador tenía que leer un emoji, que lea un atributo `data-*` del elemento (así se puede cambiar el dibujo sin romper las pruebas).
7. Revisa el resultado con `herramientas/capturar_minijuegos.py` y prueba cada minijuego con `herramientas/probar_apps.py <url> <carpeta> <solvers>`.

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
