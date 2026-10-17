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
| `instancias_cuento.py` | Instancias con solución única comprobada de los minijuegos de «Cuento» (vidriera, hadas, tarros, salto en el tiempo, caja de música, letras del libro); las importa `solvers_cuento.py`. |
| `listar_imagenes_ui.py <carpeta>` | Actualiza `img/ui/lista.json` (imágenes de minijuegos que existen de verdad) y crea `papel.jpg` provisional; los minijuegos de «Cuento» solo cargan lo listado. |
| `instancias_trono.py` | Instancias con solución única comprobada por fuerza bruta de los minijuegos de «Trono» (banquete, caminos, lengua, consejeros, antorchas, puerta, tapiz, profecía); escribe `instancias_trono.json`. |
| `listar_imagenes_trono.py [carpeta]` | Actualiza `img/ui/disponibles.json` de «Trono» (dibujos de minijuegos que existen de verdad, también en subcarpetas) y crea `papel.jpg` provisional; los minijuegos solo cargan lo listado. |
| `crear_manual_md.py <carpeta> <datos>` | Genera `MANUAL.md` a partir de los pasos verificados. |
| `chatgpt_imagenes.py [--foto F --hoja] [carpeta…]` | Maneja la web de ChatGPT con Selenium: hoja de personajes desde la foto (`personajes/hoja.png`) y luego las ilustraciones de cada carta (`<juego>/arte/ID.png`), y las convierte con `preparar_imagenes.py`. Perfil de Chrome fuera del repo (`~/.unlock-chatgpt-profile`). |
| `sincronizar_cartas.py [--comprobar]` | Genera `cartas-data.js` junto a cada `cartas.json`: es la copia que usan `pc.html`, `imprimir.html` y `prompts.html` cuando se abren con **doble clic** (el navegador bloquea `fetch` en `file://`). Con servidor siguen leyendo `cartas.json`. Hay que ejecutarlo tras cambiar un `cartas.json`; `verificar.py` avisa si está desfasado. |
| `preparar_imagenes.py <carpeta>` | Convierte `arte/*.png` en `img/*.jpg` ligeros y actualiza `img/pendientes.json`. |
| `generar_pwa.py [--comprobar]` | Escribe `sw.js` (con versión automática) y `precache.json` de cada juego. Ejecutar tras cambiar cualquier fichero del sitio. |
| `mosaicos.py` | Dibuja por código (teselas con juntas) los mosaicos de «Pompeya», los corta en placas (`arte/<carta>.png`) y escribe `codigos_pompeya.json` con el código de cada uno (los solucionadores lo leen de ahí). Los números de placa deben coincidir con `MOSAICOS` de `datos_pompeya.py`. |
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
