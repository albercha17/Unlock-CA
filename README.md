# Unlock C&A

Escape rooms híbridos, al estilo Unlock: **cartas** (impresas o en pantalla con el *Modo PC*) y un **móvil** con los minijuegos, las pistas y el temporizador. Se publica en GitHub Pages: https://albercha17.github.io/Unlock-CA/

## Los juegos

| Juego | Dónde | Manual de partida |
|---|---|---|
| **Aventuras C&A** (hub con el Cronoportal) | [`Aventuras-CA/`](Aventuras-CA/index.html) | — |
| &nbsp;&nbsp;Egipto, 1274 a.C. — *El Ojo de Horus* | [`Aventuras-CA/Egipto/`](Aventuras-CA/Egipto/) | [MANUAL.md](Aventuras-CA/Egipto/MANUAL.md) |
| &nbsp;&nbsp;Marte, 2157 — *Cúpula Aurora* | [`Aventuras-CA/Marte/`](Aventuras-CA/Marte/) | [MANUAL.md](Aventuras-CA/Marte/MANUAL.md) |
| &nbsp;&nbsp;Apagón en el Barrio | [`Unlock-Apagon-en-el-Barrio/`](Unlock-Apagon-en-el-Barrio/) | — |
| &nbsp;&nbsp;Apagón en el Colegio | repositorio propio (enlace externo) | — |
| **El Faro de Cabo Niebla** (juego de referencia) | [`Unlock-El-Faro/`](Unlock-El-Faro/) | [MANUAL.md](Unlock-El-Faro/MANUAL.md) |

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
index.html                  menú principal
Aventuras-CA/               hub «Aventuras C&A» + Egipto/ + Marte/
Unlock-El-Faro/             juego de referencia
Unlock-Apagon-en-el-Barrio/ secuela del colegio
herramientas/               verificador, bots de prueba, manuales y conversor de imágenes
GUIA-DE-JUEGOS.md           cómo diseñar y crear un juego nuevo
```

Dentro de cada juego: `index.html` (app), `pc.html` (Modo PC), `cartas.json` (guion, pistas, textos impresos y prompts de ilustración), `pistas.js`, `juegos/` (un módulo por minijuego), `img/` (ilustraciones ligeras), `MANUAL.md`. Las aventuras añaden `prompts.html` (prompts para ChatGPT) e `imprimir.html`.

## Ilustraciones (Aventuras C&A)

1. Abre `prompts.html` del juego, adjunta a ChatGPT una foto de Cristina y Alberto y sigue los pasos (hoja de personajes → una imagen por carta → vídeo de inicio).
2. Guarda las imágenes como `arte/8.png`, `arte/P.png`... dentro de la carpeta del juego (`arte/` no se sube a git).
3. `python herramientas/preparar_imagenes.py Aventuras-CA/Egipto` las convierte a `img/*.jpg` ligeros; después se suben. Mientras no estén, las cartas salen con una ilustración de relleno.

## Publicar cambios

- GitHub Pages sirve la rama `main`. Se trabaja en ramas y se fusiona con un Pull Request.
- GitHub Pages ignora los archivos cuyo nombre empieza por `_`: no los uses en el código servido.
- **No uses `git add .`**: añade archivos de más (se subió una vez un perfil de Chrome). Añade siempre archivos o carpetas concretos. El `.gitignore` excluye las ilustraciones originales, perfiles y caches.
- Las páginas se prueban con un servidor local (`python -m http.server`), no con doble clic: los módulos de JavaScript no funcionan con `file://`.

## Comprobar un juego

```
python herramientas/verificar.py Unlock-El-Faro/cartas.json herramientas/spec_faro.json
python -m http.server 8810
python herramientas/ejecutar_manual.py http://127.0.0.1:8810 Unlock-El-Faro datos_faro solvers_faro
```

Más detalle en [`herramientas/LEEME.md`](herramientas/LEEME.md).
