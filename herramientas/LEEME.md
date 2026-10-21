# Herramientas

Todo se ejecuta **desde la raíz del repositorio**. Necesitan Python 3, Pillow y, para las pruebas en navegador, Selenium y Chrome.

| Herramienta | Para qué sirve |
|---|---|
| `verificar.py <cartas.json> <spec.json>` | Verificador estricto: 3.000 partidas aleatorias, fugas de números, descartes imposibles, sumas, **combinaciones accidentales** (dos cartas combinables que suman el número de otra carta aún no obtenida), utilidad de cada carta (toda carta debe ser requisito de algún paso), que al terminar quede solo la carta final y que `cartas-data.js` esté al día. |
| `ejecutar_manual.py <URL> <carpeta> <datos> <solvers>` | Juega el manual completo en el navegador y comprueba la mesa tras cada paso. |
| `bot_aventuras.py <URL>` / `bot_faro.py <URL>` | Partida autónoma completa (solo sigue lo impreso y los mensajes de la app). |
| `bot_azar.py <URL> <faro\|egipto\|marte\|florencia\|dinosaurios…> <N> [semilla] [-v]` | **N partidas en orden aleatorio** en el navegador (cada semilla elige otro orden de leer, coger, descartar, combinar y resolver apps). Falla si algo no cuadra o hay errores de consola. |
| `probar_impresion.py [carpetas…]` | Abre `imprimir.html` por `file://` y comprueba carta a carta que las franjas **Coge / Descarta / Combinable** impresas coinciden con `cartas.json` y que carga cada ilustración. |
| `probar_pistas.py <URL> <carpeta>` | Abre el visor de **Pistas** de la app con cada carta del juego y recorre todas sus pistas. |
| `capturar_minijuegos.py <URL> <carpeta> <salida>` | Fotografía (tamaño móvil) cada minijuego de un juego y las junta en una hoja de contactos `_hoja.png`: para revisar el aspecto y comparar antes y después. |
| `chatgpt_fondos.py [--solo texto] [--forzar] [--lista] [--afinar]` | Genera con ChatGPT los gráficos de la interfaz de los minijuegos (objetos sobre negro puro que se mezclan con `screen`, texturas y hojas de varios objetos que se trocean solas). Los catálogos están en `herramientas/pedidos/<juego>.py`. |
| `probar_apps.py <URL> <carpeta> <solvers> [cartas…]` | Resuelve por la interfaz real los minijuegos de un juego (sin jugar la partida entera) y falla ante errores de consola: sirve para probar rápido tras tocar su aspecto. |
| `generadores_puzles.py [--prueba]` | Banco de generadores con **solución única comprobada**: nonograma, luces (Akari), rascacielos, tabla lógica, caballeros y bribones, caja negra, Rush Hour, Hashi, lengua inventada, luces en cruz, puente y linterna, tubos de colores. |
| `crear_laboratorio.py [semilla]` / `probar_laboratorio.py <URL>` | Genera las instancias de `juegos/laboratorio/` (prototipos jugables de ideas de puzles) y las resuelve por la interfaz real comprobando el mensaje de éxito. |
| `auditar_minijuegos.py [carpetas…]` | Auditoría estática de los minijuegos y de las pistas contra las reglas de diseño (mensajes de acierto/fallo, sin emojis, pistas, anchos, alt). |
| `instancias_cuento.py` | Instancias con solución única comprobada de los minijuegos de «Cuento» (vidriera, hadas, tarros, salto en el tiempo, botas, habichuela, caja de música, letras del libro); las importan `cuento.py` y `solvers_cuento.py`. |
| `instancias_egipto.py` / `egipto.py` | Instancias con solución única comprobada de los 11 puzles de «Egipto» (granero, pirámide, nilómetro, friso, heqat, criptograma, cámaras, canales, azulejos, tierras y sellos) y dibujante por código de sus cartas-pista (`arte/<carta>.png`, mosaicos de la pirámide, el friso, el plano, los azulejos y el campo). |
| `instancias_dinosaurios.py` / `dinosaurios.py` | Instancias con solución única comprobada de los 11 puzles de «Dinosaurios» (huellas, manada, nidos, cráter, lava, senderos, árbol, corral, planear, barro, anillos) y dibujante por código de sus cartas-pista (`arte/<carta>.png`, mosaicos del valle, la ladera y los senderos). |
| `cuento.py` | Dibuja por código las cartas-pista del «Cuento» de 60 cartas (`arte/<carta>.png`, mosaicos de la vela, el bosque y los espejos) y mete los datos en las apps 48 y 52. |
| `listar_imagenes_ui.py <carpeta>` | Actualiza `img/ui/lista.json` (imágenes de minijuegos que existen de verdad) y crea `papel.jpg` provisional; los minijuegos de «Cuento» solo cargan lo listado. |
| `instancias_trono.py` | Instancias con solución única comprobada por fuerza bruta de los minijuegos de «Trono» (banquete, caminos, lengua, consejeros, antorchas, puerta, tapiz, profecía); escribe `instancias_trono.json`. |
| `listar_imagenes_trono.py [carpeta]` | Actualiza `img/ui/disponibles.json` de «Trono» (dibujos de minijuegos que existen de verdad, también en subcarpetas) y crea `papel.jpg` provisional; los minijuegos solo cargan lo listado. |
| `crear_manual_md.py <carpeta> <datos>` | Genera `MANUAL.md` a partir de los pasos verificados. |
| `chatgpt_imagenes.py [--foto F --hoja] [carpeta…]` | Maneja la web de ChatGPT con Selenium: hoja de personajes desde la foto (`personajes/hoja.png`) y luego las ilustraciones de cada carta (`<juego>/arte/ID.png`), y las convierte con `preparar_imagenes.py`. Perfil de Chrome fuera del repo (`~/.unlock-chatgpt-profile`). |
| `sincronizar_cartas.py [--comprobar]` | Genera `cartas-data.js` junto a cada `cartas.json`: es la copia que usan `pc.html`, `imprimir.html` y `prompts.html` cuando se abren con **doble clic** (el navegador bloquea `fetch` en `file://`). Con servidor siguen leyendo `cartas.json`. Hay que ejecutarlo tras cambiar un `cartas.json`; `verificar.py` avisa si está desfasado. |
| `preparar_imagenes.py <carpeta>` | Convierte `arte/*.png` en `img/*.jpg` ligeros y actualiza `img/pendientes.json`. |
| `generar_pwa.py [--comprobar]` | Escribe `sw.js` (con versión automática) y `precache.json` de cada juego. Ejecutar tras cambiar cualquier fichero del sitio. |
| `mosaicos.py` | Dibuja por código (teselas con juntas) los mosaicos de «Pompeya», los corta en placas (`arte/<carta>.png`) y escribe `codigos_pompeya.json` con el código de cada uno (los solucionadores lo leen de ahí). Los números de placa deben coincidir con `MOSAICOS` de `datos_pompeya.py`. |
| `pixeles.py` | Igual que `mosaicos.py` pero con pantallas de píxeles de neón para «Game Over, 1985»: placa base 3×2 con placas boca abajo, radar 2×2, marquesina 1×3 y las cartas sueltas 52 (tráfico) y 70 (piezas). Escribe `codigos_arcade.json`. |
| `oeste.py` | Dibuja con PIL (suavizado, fuentes de cartel) las láminas de «Dry Gulch»: tren de 5 cartas en fila, cartel de «Se busca» de 3 en columna, mapa 2×2 y las cartas sueltas 36 (libro del sheriff), 52 (reloj) y 70 (informe). Escribe `codigos_oeste.json`. |
| `espia.py` | Dibuja las cartas de «Montecarlo, 1965»: dos hojas de criptografía visual (cartas 14 y 15) y la rejilla de Cardano con su carta de letras (30 y 31) a 520 px (se superponen), el plano del yate (40), las dos cartas de pistas del skyline (52 y 53) y el manual del desactivador (70). Escribe `codigos_espia.json` y deja en `arte/` la imagen de las hojas superpuestas para comprobarlo. |
| `parche_dorsos.py` | Reversos ambientados para imprimir a doble cara en todos los `imprimir.html`: tras cada hoja de cartas va su hoja de reversos (columnas invertidas para que cuadre), con el número de la carta y el diseño del juego. **Al crear un juego nuevo, añade su entrada a `TABLA` (y su patrón a `PATRONES`) y ejecútalo:** es idempotente y refresca la tabla en todos los juegos. `probar_impresion.py` comprueba que cada reverso queda detrás de su carta. |
| `futbol.py` | Dibuja con PIL las láminas de «La Final del Siglo, 1970»: seis cromos con anverso (`14.png`) y reverso (`14r.png`), las dos cartas de pistas de la pizarra (30 y 31), las jugadas del VAR (40 y 41) con su reglamento (42), la clasificación y los resultados de la liguilla (52 y 53) y el informe del portero (70), a partir de `instancias_futbol.json`. |
| `instancias_futbol.py` | Busca con semilla fija, y comprueba por fuerza bruta, la alineación 1-2-2-1 con sus pistas (solución única), las cuatro jugadas del VAR con su decisión, la liguilla de cuatro equipos con tres marcadores por descubrir (solución única) y la tanda de penaltis; escribe `instancias_futbol.json`. |
| `piratas.py` | Dibuja las láminas de «Mar de las Brumas, 1715»: las tres **cartas que se pliegan** (30 carta náutica, 76 testamento y 70 mapa: primero la carta plegada y luego se abre metiendo franjas con señuelos; comprueba que plegarla da la composición) y las cartas 31, 40, 52 y 64, más las imágenes de los minijuegos (`img/ui`). Deja las cartas plegadas en `arte/comprobar/`. |
| `instancias_piratas.py` | Busca con semilla fija, y comprueba por fuerza bruta, la bodega (Sokoban resuelto por BFS), la persecución de la fragata (BFS sobre barco y fragata), la constelación girada (aparece una sola vez), el suelo de losas (camino único), el rumbo con sus señuelos y la ruta del mapa; escribe `instancias_piratas.json`. `piratas.py` copia cada instancia en su minijuego. |
| `juguetes.py` | Dibuja las láminas de «El Cuarto de Leo, 1995» (Polaroid, vistas de la torre, hilos y cartel de la marioneta, las cinco páginas del folioscopio e instrucciones de la pista de canicas) y las imágenes de sus minijuegos, y copia en cada minijuego los datos de su instancia. |
| `instancias_juguetes.py` | Diferencias, torre de bloques con vistas de solución única (fuerza bruta sobre 4^9 torres), marioneta, orden del folioscopio y pista de canicas con balancines (una sola posición válida). |
| `parche_folioscopio.py` | Añade a todos los `pc.html` el botón **Hojear** de los folioscopios (`_meta.folioscopios`): ordenar las páginas y reproducirlas. Idempotente. |
| `ampliacion.py` | Ayudas para ampliar un juego publicado hasta 36 cartas: rehace las mesas del manual simulando los pasos, escribe `cartas.json`/`spec` desde `datos_<juego>.py` sin regenerar la carpeta y cambia el «Coged la carta N» de un minijuego. |
| `instancias_ampliacion.py` / `dibujos_ampliacion.py` | Instancias (solución única comprobada) y láminas de los puzles añadidos al ampliar Marte, Egipto, Florencia, Montecarlo, Piratas, Juguetes y El Faro; copian los datos en los minijuegos nuevos. |
| `ampliar_faro.py` | Amplía El Faro a 36 cartas y cambia sus protagonistas por Cristina y Alberto (idempotente). |
| `parche_plegado.py` | Añade a todos los `pc.html` el botón **Plegar** de las cartas con campo `plegado` (fracciones de la franja escondida). Idempotente. |
| `probar_reversos.py <URL> <carpeta> [capturas]` | Comprueba las cartas con dos caras: que existe cada reverso, que «Dar la vuelta» funciona en la mesa y en la carta ampliada del Modo PC, y que las hojas de reversos de `imprimir.html` quedan detrás de su carta. |
| `instancias_espia.py` | Busca con semilla fija, y comprueba por fuerza bruta, el laberinto 7×7 perfecto, el rascacielos 4×4 de solución única (con las pistas repartidas en dos cartas) y las cuatro cargas de la bomba con la regla que las resuelve; escribe `instancias_espia.json`. |
| `instancias_arcade.py` | Busca con semilla fija, y comprueba por fuerza bruta, la autopista (Frogger por turnos, solución mínima por BFS) y el pozo de bloques (teselado único) de «Game Over»; escribe `instancias_arcade.json`, que leen `pixeles.py` y los solucionadores. |
| `probar_mosaicos.py <URL> <carpeta> [capturas]` | Comprueba que las placas reconstruyen el mosaico, que la «Mesa de montaje» del Modo PC se puede resolver y que las cartas-mosaico se ven bien en `pc.html` e `imprimir.html`. |
| `parche_mosaicos.py` | Añade a todos los `pc.html` e `imprimir.html` el soporte de cartas-mosaico (campo `mosaico` de `cartas.json`) y la Mesa de montaje. Idempotente. |
| `probar_qr.py` | Comprueba (sin cámara) que el QR impreso en cada carta de los 7 juegos se lee con el mismo lector que usa la app. Arranca su propio servidor. |
| `generar_catalogo.py` | Escribe `juegos/catalogo.json` (dificultad, minutos y cartas de cada juego) para los menús, «Mis partidas» y las partidas guardadas. |
| `generar_iconos.py` | Dibuja los iconos de la app instalable en `assets/icons/`. |
| `probar_pwa.py [juego]` | Prueba menús, service worker, modo sin conexión y cuentas (con Supabase simulado). Arranca su propio servidor. |
| `regenerar_index.py [--probar] [Juego]` | Regenera el `index.html` de cada juego de Aventuras C&A desde la plantilla del Faro y copia `app.css`/`app.js` (la app se edita solo en `juegos/el-faro`). La configuración de cada juego está en `juegos_config.py`. |
| `construir_aventuras.py` | Plantilla que generó las carpetas de Egipto y Marte (no sobrescribe juegos existentes). |

Módulos de apoyo: `bot_core.py` (jugador y mesa), `solvers_*.py` (cómo se resuelve cada minijuego), `datos_*.py` (pasos del manual, «para qué sirve» de cada carta y, en Egipto y Marte, el guion de origen), `spec_*.json` (dependencias entre cartas para el verificador), `prompts_plantilla.html`.

## Ejemplo completo con El Faro

```
python herramientas/verificar.py juegos/el-faro/cartas.json herramientas/spec_faro.json
python -m http.server 8810        # en otra terminal
python herramientas/ejecutar_manual.py http://127.0.0.1:8810 juegos/el-faro datos_faro solvers_faro
python herramientas/crear_manual_md.py juegos/el-faro datos_faro
```

## Un juego nuevo

1. Copia `datos_egipto.py` como `datos_<juego>.py` y cámbialo (cartas, `SPEC`, `PASOS`, `PARA_QUE`).
2. Escribe los minijuegos en `minijuegos/` y un `solvers_<juego>.py` con cómo se resuelve cada uno.
3. Pasa el verificador, el manual y el bot. Genera `MANUAL.md`.

Los `spec_*.json` indican, para cada carta que no sale en el «coge» de otra, qué cartas hay que tener en la mano para obtenerla (`needs`) y los descartes que manda la app (`eventos`).
