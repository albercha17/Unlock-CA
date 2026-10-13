# Unlock C&A

Escape rooms híbridos, al estilo Unlock: **cartas** (impresas o en pantalla con el *Modo PC*) y un **móvil** con los minijuegos, las pistas y el temporizador. Se publica en GitHub Pages: https://albercha17.github.io/Unlock-CA/

## Los juegos

| Juego | Dónde | Manual de partida |
|---|---|---|
| **Aventuras C&A** (hub con el Cronoportal) | [`juegos/aventuras-ca/`](juegos/aventuras-ca/index.html) | — |
| &nbsp;&nbsp;Egipto, 1274 a.C. — *El Ojo de Horus* | [`juegos/aventuras-ca/egipto/`](juegos/aventuras-ca/egipto/) | [MANUAL.md](juegos/aventuras-ca/egipto/MANUAL.md) |
| &nbsp;&nbsp;Marte, 2157 — *Cúpula Aurora* | [`juegos/aventuras-ca/marte/`](juegos/aventuras-ca/marte/) | [MANUAL.md](juegos/aventuras-ca/marte/MANUAL.md) |
| &nbsp;&nbsp;Florencia, 1503 — *El Taller de Leonardo* | [`juegos/aventuras-ca/florencia/`](juegos/aventuras-ca/florencia/) | [MANUAL.md](juegos/aventuras-ca/florencia/MANUAL.md) |
| &nbsp;&nbsp;Apagón en el Colegio | repositorio propio, clonado en `juegos/apagon-colegio/` (enlace externo) | — |
| **El Faro de Cabo Niebla** (juego de referencia) | [`juegos/el-faro/`](juegos/el-faro/) | [MANUAL.md](juegos/el-faro/MANUAL.md) |

**El Faro es el juego de referencia:** su flujo está comprobado de principio a fin y los juegos nuevos se hacen igual (ver la [guía de diseño](GUIA-DE-JUEGOS.md)).

## Cómo se juega

1. Se parte de la carta **P**. Cada carta dice qué hay que **coger** y qué **descartar** (franja impresa en la carta).
2. Los números de las cartas de **app** (verdes) se escriben en el móvil, en *Acción*, para abrir su minijuego. *Pista* da ayuda de cualquier carta.
3. Las cartas **de combinar** (rojas y azules) se suman: el resultado es el número de la carta que se coge.
4. Solo hay tres tipos de carta: **normal**, **de app** y **de combinar**. Todas sirven para algo.
5. **Modo PC** (`pc.html` en cada juego): mesa virtual con el mazo boca abajo (número en el dorso), las cartas en mesa y los descartes (recuperables). Sustituye a las cartas impresas; los minijuegos se hacen en el móvil.
6. Para imprimir: `imprimir.html` de cada aventura (hojas A4 de 9 cartas + dorsos).

## Estructura

```
index.html                       menú principal
assets/                          estilos e imágenes del menú
juegos/
  aventuras-ca/                  hub «Aventuras C&A»
    egipto/  marte/  florencia/  una carpeta por juego
  el-faro/                       juego de referencia
  apagon-colegio/                OTRO repositorio (solo local; ver .gitignore)
herramientas/                    verificador, bots de prueba, manuales, ChatGPT y conversor de imágenes
GUIA-DE-JUEGOS.md                cómo diseñar y crear un juego nuevo
```

Dentro de cada juego: `index.html` (app), `pc.html` (Modo PC), `cartas.json` (guion, pistas, textos impresos y prompts de ilustración), `pistas.js`, `minijuegos/` (un módulo por minijuego), `img/` (ilustraciones ligeras que se publican), `MANUAL.md`. Los juegos con ilustraciones añaden `prompts.html` (prompts para ChatGPT) e `imprimir.html`. Los originales pesados van en `arte/` y no se suben.

## Ilustraciones (Aventuras C&A)

Están hechas con ChatGPT de forma automática (Selenium), con la cara de Cristina y Alberto de una hoja de personajes y **ropa distinta en cada juego**:

1. `herramientas/abrir_chrome_chatgpt.ps1` abre un Chrome normal: inicia sesión en ChatGPT (y pasa la verificación «soy humano») ahí.
2. `python herramientas/chatgpt_imagenes.py --conectar --hoja --foto F1.jpg F2.jpg` crea la hoja de personajes (`personajes/hoja.png`, solo en local).
3. `python herramientas/chatgpt_imagenes.py --conectar juegos/aventuras-ca/egipto` genera cada carta en `arte/ID.png` y la convierte a `img/ID.jpg`.

`arte/`, `personajes/` y las fotos no se suben a git. Manualmente se puede hacer igual con `prompts.html` de cada juego.

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
