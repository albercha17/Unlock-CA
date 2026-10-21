# Unlock C&A

Escape rooms híbridos, al estilo Unlock: **cartas** (impresas o en pantalla con el *Modo PC*) y un **móvil** con los minijuegos, las pistas y el temporizador. Se publica en GitHub Pages: https://albercha17.github.io/Unlock-CA/

## Los juegos

| Juego | Dónde | Manual de partida |
|---|---|---|
| **Aventuras C&A** (hub con el Cronoportal) | [`juegos/aventuras-ca/`](juegos/aventuras-ca/index.html) | — |
| &nbsp;&nbsp;Egipto, 1274 a.C. — *El Ojo de Horus* (60 cartas, 11 puzles distintos: granero, pirámide, nilómetro, friso, heqat, criptograma, cámaras, canales, azulejos, tierras y consola) | [`juegos/aventuras-ca/egipto/`](juegos/aventuras-ca/egipto/) | [MANUAL.md](juegos/aventuras-ca/egipto/MANUAL.md) |
| &nbsp;&nbsp;Marte, 2157 — *Cúpula Aurora* (60 cartas, 11 puzles distintos: satélites, invernadero, cableado, rocas, brazo, cifras, reactor, rover, paneles, sopa y consola) | [`juegos/aventuras-ca/marte/`](juegos/aventuras-ca/marte/) | [MANUAL.md](juegos/aventuras-ca/marte/MANUAL.md) |
| &nbsp;&nbsp;Florencia, 1503 — *El Taller de Leonardo* | [`juegos/aventuras-ca/florencia/`](juegos/aventuras-ca/florencia/) | [MANUAL.md](juegos/aventuras-ca/florencia/MANUAL.md) |
| &nbsp;&nbsp;Cretácico, hace 66 millones de años — *El Valle de los Gigantes* (61 cartas, 11 puzles distintos: huellas, manada, nidos, cráter, lava, senderos, árbol, corral, planear, balsa y anillos) | [`juegos/aventuras-ca/dinosaurios/`](juegos/aventuras-ca/dinosaurios/) | [MANUAL.md](juegos/aventuras-ca/dinosaurios/MANUAL.md) |
| &nbsp;&nbsp;Dentro de un cuento animado — *Érase una vez: El Libro de los Finales Felices* (60 cartas, 11 puzles distintos: cartel, puente del troll, saltos al pasado, botas de siete leguas, habichuela, vidriera, hadas, rayos de luna, tarros, caja de música y última página) | [`juegos/aventuras-ca/cuento/`](juegos/aventuras-ca/cuento/) | [MANUAL.md](juegos/aventuras-ca/cuento/MANUAL.md) |
| &nbsp;&nbsp;Reino de hielo y fuego — *La Corona del Dragón* (fantasía medieval, dificultad difícil) | [`juegos/aventuras-ca/trono/`](juegos/aventuras-ca/trono/) | [MANUAL.md](juegos/aventuras-ca/trono/MANUAL.md) |
| &nbsp;&nbsp;Pompeya, 79 d.C. — *El Mosaico del Mundo* (60 cartas, 10 puzles distintos: mosaico laberinto, cuentas romanas, sello, fuente, cuadrado SATOR, balanza romana, grafitos, calendario, huida y barca) | [`juegos/aventuras-ca/pompeya/`](juegos/aventuras-ca/pompeya/) | [MANUAL.md](juegos/aventuras-ca/pompeya/MANUAL.md) |
| &nbsp;&nbsp;Dentro de una recreativa, 1985 — *Game Over: La Última Moneda* (placa con piezas **boca abajo**, radar, mando, autopista y pozo de bloques) | [`juegos/aventuras-ca/arcade/`](juegos/aventuras-ca/arcade/) | [MANUAL.md](juegos/aventuras-ca/arcade/MANUAL.md) |
| &nbsp;&nbsp;Lejano Oeste, 1878 — *Dry Gulch: El Tren del Oro* (vagones que se **enganchan** en fila, cartel de «Se busca» en columna, mapa, dos mechas y barra de oro falsa) | [`juegos/aventuras-ca/oeste/`](juegos/aventuras-ca/oeste/) | [MANUAL.md](juegos/aventuras-ca/oeste/MANUAL.md) |
| &nbsp;&nbsp;Montecarlo, 1965 — *Operación Cristal* (espías: cartas que se **superponen** a contraluz, rejilla de cifrado, laberinto a ciegas, skyline y cables) | [`juegos/aventuras-ca/espia/`](juegos/aventuras-ca/espia/) | [MANUAL.md](juegos/aventuras-ca/espia/MANUAL.md) |
| &nbsp;&nbsp;Fútbol, 1970 — *La Final del Siglo: La Copa de Cristal* (cromos con **dos caras**, alineación, VAR, liguilla y penaltis) | [`juegos/aventuras-ca/futbol/`](juegos/aventuras-ca/futbol/) | [MANUAL.md](juegos/aventuras-ca/futbol/MANUAL.md) |
| &nbsp;&nbsp;Piratas, 1715 — *Mar de las Brumas: El Tesoro de la Isla Calavera* (cartas que se **pliegan**, timón con desvío de la aguja, bodega de barriles, persecución de una fragata, constelación girada, suelo de losas trampa y cavar en la gruta) | [`juegos/aventuras-ca/piratas/`](juegos/aventuras-ca/piratas/) | [MANUAL.md](juegos/aventuras-ca/piratas/MANUAL.md) |
| &nbsp;&nbsp;Juguetes, 1995 — *El Cuarto de Leo: La Noche de los Juguetes* (**fácil**; cartas que se **hojean**: folioscopio; diferencias con una Polaroid, torre de bloques por sus vistas, hilos de marioneta, tren y pista de canicas con balancines) | [`juegos/aventuras-ca/juguetes/`](juegos/aventuras-ca/juguetes/) | [MANUAL.md](juegos/aventuras-ca/juguetes/MANUAL.md) |
| &nbsp;&nbsp;Apagón en el Colegio | repositorio propio, clonado en `juegos/apagon-colegio/` (enlace externo) | — |
| **El Faro de Cabo Niebla** (juego de referencia) | [`juegos/el-faro/`](juegos/el-faro/) | [MANUAL.md](juegos/el-faro/MANUAL.md) |

**El Faro es el juego de referencia** (desde el 20 oct 2026 lo protagonizan también Cristina y Alberto y tiene 36 cartas): su flujo está comprobado de principio a fin y los juegos nuevos se hacen igual (ver la [guía de diseño](GUIA-DE-JUEGOS.md)).

## Cómo se juega

1. Se parte de la carta **P**. Cada carta dice qué hay que **coger** y qué **descartar** (franja impresa en la carta).
2. Los números de las cartas de **app** (verdes) se escriben en el móvil, en *Acción*, para abrir su minijuego. *Pista* da ayuda de cualquier carta.
3. Las cartas **de combinar** (rojas y azules) se suman: el resultado es el número de la carta que se coge.
4. Solo hay tres tipos de carta: **normal**, **de app** y **de combinar**. Todas sirven para algo.
5. **Modo PC** (`pc.html` en cada juego): mesa virtual con el mazo boca abajo (número en el dorso), las cartas en mesa y los descartes (recuperables). Sustituye a las cartas impresas; los minijuegos se hacen en el móvil.
6. Para imprimir: `imprimir.html` de cada aventura. **A doble cara:** cada hoja A4 de 9 cartas va seguida de su hoja de **reversos** (volteando por el lado largo). Cada carta tiene su reverso con su **número** en grande y el diseño propio del juego (colores, dibujo repetido, emoji y título), y las columnas de la hoja de reversos están invertidas para que cada reverso quede justo detrás de su carta. Las cartas con dos caras de verdad llevan su reverso ilustrado. El diseño de cada juego está en `herramientas/parche_dorsos.py` (`TABLA`).

## Estructura

```
index.html                       menú principal
assets/                          estilos e imágenes del menú
juegos/
  aventuras-ca/                  hub «Aventuras C&A»
    egipto/  marte/  florencia/  dinosaurios/  cuento/  trono/  pompeya/  arcade/  oeste/  espia/  futbol/  piratas/  juguetes/  una carpeta por juego
  el-faro/                       juego de referencia
  apagon-colegio/                OTRO repositorio (solo local; ver .gitignore)
herramientas/                    verificador, bots de prueba, manuales, ChatGPT y conversor de imágenes
GUIA-DE-JUEGOS.md                cómo diseñar y crear un juego nuevo
```

Dentro de cada juego: `index.html` (app), `pc.html` (Modo PC), `cartas.json` (guion, pistas, textos impresos y prompts de ilustración), `pistas.js`, `minijuegos/` (un módulo por minijuego), `img/` (ilustraciones ligeras que se publican), `MANUAL.md`. Los juegos con ilustraciones añaden `prompts.html` (prompts para ChatGPT) e `imprimir.html`. Los originales pesados van en `arte/` y no se suben.

## Cartas que se juntan (mosaicos)

Algunos puzles no se leen en una carta sino **entre varias**: Pompeya junta las cuatro placas de un mosaico laberinto (2×2), las dos mitades del lacre de un sello y las dos mitades de un calendario de piedra (las dibuja `python herramientas/pompeya.py`); Marte junta el invernadero, la placa de bornes, el radar, el esquema del reactor, los paneles y la sopa de letras (`python herramientas/marte.py`); Egipto junta la pirámide, el friso de animales, el plano del templo, el friso de azulejos y el campo (`python herramientas/egipto.py`); Dinosaurios junta el mapa del valle, la ladera, los senderos y la manada (`python herramientas/dinosaurios.py`); el Cuento junta las dos mitades de la vela del troll, del mapa del bosque y del plano de la sala de los espejos (`python herramientas/cuento.py`).

- **Impresas:** `imprimir.html` las saca sin borde; se juntan sobre la mesa.
- **Modo PC:** cuando las piezas están en la mesa sale el botón **Mesa de montaje**: se tocan dos piezas para cambiarlas de sitio hasta que el dibujo encaje.
- **Piezas boca abajo y 3 columnas:** «Game Over, 1985» tiene una placa de 3×2 piezas en la que algunas se entregan giradas 180° (con las letras al revés): la Mesa de montaje tiene un botón «Dar la vuelta». Sus dibujos de píxeles los hace `python herramientas/pixeles.py`; las instancias de la autopista y del pozo de bloques, `python herramientas/instancias_arcade.py` (búsqueda con solución comprobada).
- **Cartas con dos caras:** «La Final del Siglo, 1970» tiene seis cromos de jugadores cuyo anverso solo enseña el dorsal y cuyo **reverso** (`img/<id>r.jpg`, campo `reverso` en `cartas.json`) trae la ficha técnica. En el Modo PC cada carta con reverso tiene el botón **Dar la vuelta** (también en la carta ampliada); en papel, `imprimir.html` añade tras cada hoja de cartas su hoja de reversos con las columnas invertidas, para imprimirlas a doble cara (volteando por el lado largo). Las láminas las dibuja `python herramientas/futbol.py` (reversos como `14r.png`); `python herramientas/probar_reversos.py URL carpeta` lo comprueba.
- **Cartas que se hojean (folioscopio):** «El Cuarto de Leo, 1995» tiene cinco páginas de un cuaderno (cartas 41, 43, 45, 49 y 51) que se ordenan por el sol de la ventana y se hojean como una animación. En el Modo PC, cuando las cinco están en la mesa sale el botón **Hojear** (campo `folioscopios` de `_meta`, añadido a todos los `pc.html` con `python herramientas/parche_folioscopio.py`): se ordenan tocando dos páginas para cambiarlas de sitio y se reproducen.
- **Cartas que se pliegan:** «Mar de las Brumas, 1715» tiene tres cartas (carta náutica, testamento y mapa) que se pliegan en acordeón hasta que la línea A toque la B (y la C, la D), como los «fold-in» de la revista MAD: la franja de en medio queda escondida y lo de los lados se junta en un dibujo nuevo (desplegadas, enseñan señuelos). En el Modo PC, botón **Plegar** (campo `plegado` de `cartas.json`, añadido a todos los `pc.html` con `python herramientas/parche_plegado.py`). Las láminas las dibuja `python herramientas/piratas.py`, que comprueba que plegar la lámina da exactamente la composición.
- **Cartas que se superponen:** «Montecarlo, 1965» tiene dos pares de cartas que se ponen **una encima de otra** (en papel, a contraluz: dos hojas de ruido que revelan un número —criptografía visual— y una carta negra con ventanas sobre una de letras —rejilla de Cardano—). En el Modo PC sale el botón **Superponer las cartas**: la de encima se multiplica sobre la de abajo y se mueve con flechas hasta que los marcos coinciden. Las láminas las dibuja `python herramientas/espia.py` (a 520 px de ancho, para que el ruido de 8 px llegue intacto al sitio web).
- **Filas y columnas:** «Dry Gulch» une cartas en **fila** (5 vagones que se enganchan por los símbolos de sus extremos) y en **columna** (un cartel de «Se busca» partido en 3 cartas, cada rasgo de la cara en una carta distinta). Se dibujan con `python herramientas/oeste.py`.
- **Cómo se hacen:** `python herramientas/mosaicos.py` dibuja los mosaicos por código (teselas con juntas), los corta en placas y guarda en `herramientas/codigos_pompeya.json` el código de cada uno (los solucionadores de prueba lo leen de ahí). `python herramientas/probar_mosaicos.py URL carpeta` comprueba que las placas reconstruyen el dibujo y que la mesa de montaje se resuelve.

## Ilustraciones (Aventuras C&A)

Están hechas con ChatGPT de forma automática (Selenium), con la cara de Cristina y Alberto de una hoja de personajes y **ropa distinta en cada juego**:

1. `herramientas/abrir_chrome_chatgpt.ps1` abre un Chrome normal: inicia sesión en ChatGPT (y pasa la verificación «soy humano») ahí.
2. `python herramientas/chatgpt_imagenes.py --conectar --hoja --foto F1.jpg F2.jpg` crea la hoja de personajes (`personajes/hoja.png`, solo en local).
3. `python herramientas/chatgpt_imagenes.py --conectar juegos/aventuras-ca/egipto` genera cada carta en `arte/ID.png` y la convierte a `img/ID.jpg`.

`arte/`, `personajes/` y las fotos no se suben a git. Manualmente se puede hacer igual con `prompts.html` de cada juego.

## App en el móvil y cuentas

- **Instalable (PWA):** desde Safari en iPhone (o Chrome en Android) se añade a la pantalla de inicio y funciona a pantalla completa y **sin conexión** (cada juego tiene un botón «Descargar para jugar sin conexión»). Guía para jugadores: `instalar.html`.
- **Cuentas y partidas:** inicio de sesión con correo y contraseña (el Supabase de «Noches de Cine»: el de «La Arena» está pausado). Al terminar un juego se guardan el tiempo y las pistas; `perfil.html` («Mis partidas») muestra el historial y el mejor tiempo, y los menús marcan las aventuras completadas. Sin cuenta, o sin red, las partidas se guardan en el dispositivo y se suben después. **Hay que crear la tabla una vez** ejecutando `supabase/unlock_partidas.sql` en el editor SQL de Supabase.
- **Se siente como una app:** barra inferior (Inicio, Aventuras, Partidas, Ajustes) en los menús (`assets/js/barra.js`), pantalla de arranque con el Cronoportal al abrir la app instalada (`splash.js` + imágenes de arranque de iPhone en `assets/splash/`), transiciones entre páginas (View Transitions, con fundido de respaldo), hojas que se cierran **deslizando hacia abajo** (cuaderno, teclado y minijuegos) y un toque de vibración en Android.
- **Ajustes** (`ajustes.html`, aplicados por `assets/js/ajustes.js` en todas las páginas): música y su volumen, sonidos de minijuegos, tamaño de texto, contraste alto, reducir movimiento, y gestión de descargas sin conexión y partidas guardadas.
- **Sin QR:** las cartas impresas no llevan código QR (decisión del 17 oct 2026); en la app el número de la carta se escribe con el teclado.
- **Logros y récords:** `perfil.html` calcula insignias (primera aventura, sin pistas, a todo gas, impecable, valiente, viajera del tiempo, coleccionista, repetidora) con las partidas guardadas.
- **Aviso de versión nueva:** la app instalada avisa con «Actualizar» cuando hay una versión nueva (`assets/js/pwa.js`).
- **iPhone:** márgenes para la muesca y la barra inferior en la app y los minijuegos (`env(safe-area-inset-*)`).
- **Dificultad antes de elegir:** cada tarjeta de los menús muestra dificultad, minutos y número de cartas (`juegos/catalogo.json`, generado con `python herramientas/generar_catalogo.py`).
- Tras cambiar **cualquier** fichero del sitio, ejecuta `python herramientas/generar_pwa.py` (actualiza `sw.js` y las listas `precache.json` para que los móviles reciban los cambios). `python herramientas/probar_pwa.py` comprueba menús, modo sin conexión y cuentas con un Supabase simulado.

## Publicar cambios

- GitHub Pages sirve la rama `main`. Se trabaja en ramas y se fusiona con un Pull Request.
- GitHub Pages ignora los archivos cuyo nombre empieza por `_`: no los uses en el código servido.
- **No uses `git add .`**: añade archivos de más (se subió una vez un perfil de Chrome). Añade siempre archivos o carpetas concretos. El `.gitignore` excluye las ilustraciones originales, perfiles y caches.
- La app del móvil (`index.html`) se prueba con un servidor local (`python -m http.server`): sus módulos de JavaScript no funcionan con `file://`.
- `pc.html`, `imprimir.html` y `prompts.html` también se pueden abrir con **doble clic**: usan `cartas-data.js`, que se genera con `python herramientas/sincronizar_cartas.py` (ejecútalo siempre que cambies un `cartas.json`).

## Comprobar un juego

```
python herramientas/verificar.py juegos/el-faro/cartas.json herramientas/spec_faro.json
python -m http.server 8810
python herramientas/ejecutar_manual.py http://127.0.0.1:8810 juegos/el-faro datos_faro solvers_faro
```

Más detalle en [`herramientas/LEEME.md`](herramientas/LEEME.md).
