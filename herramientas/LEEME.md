# Herramientas

Todo se ejecuta **desde la raíz del repositorio**. Necesitan Python 3, Pillow y, para las pruebas en navegador, Selenium y Chrome.

| Herramienta | Para qué sirve |
|---|---|
| `verificar.py <cartas.json> <spec.json>` | Verificador estricto: 3.000 partidas aleatorias, fugas de números, descartes imposibles, sumas, **combinaciones accidentales** (dos cartas combinables que suman el número de otra carta aún no obtenida), utilidad de cada carta. |
| `ejecutar_manual.py <URL> <carpeta> <datos> <solvers>` | Juega el manual completo en el navegador y comprueba la mesa tras cada paso. |
| `bot_aventuras.py <URL>` / `bot_faro.py <URL>` | Partida autónoma completa (solo sigue lo impreso y los mensajes de la app). |
| `bot_azar.py <URL> <faro\|egipto\|marte> <N> [semilla] [-v]` | **N partidas en orden aleatorio** en el navegador (cada semilla elige otro orden de leer, coger, descartar, combinar y resolver apps). Falla si algo no cuadra o hay errores de consola. |
| `crear_manual_md.py <carpeta> <datos>` | Genera `MANUAL.md` a partir de los pasos verificados. |
| `chatgpt_imagenes.py [--foto F --hoja] [carpeta…]` | Maneja la web de ChatGPT con Selenium: hoja de personajes desde la foto (`personajes/hoja.png`) y luego las ilustraciones de cada carta (`<juego>/arte/ID.png`), y las convierte con `preparar_imagenes.py`. Perfil de Chrome fuera del repo (`~/.unlock-chatgpt-profile`). |
| `sincronizar_cartas.py [--comprobar]` | Genera `cartas-data.js` junto a cada `cartas.json`: es la copia que usan `pc.html`, `imprimir.html` y `prompts.html` cuando se abren con **doble clic** (el navegador bloquea `fetch` en `file://`). Con servidor siguen leyendo `cartas.json`. Hay que ejecutarlo tras cambiar un `cartas.json`; `verificar.py` avisa si está desfasado. |
| `preparar_imagenes.py <carpeta>` | Convierte `arte/*.png` en `img/*.jpg` ligeros y actualiza `img/pendientes.json`. |
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
