# Cuento — imágenes pendientes

El juego está completo y probado (cartas, puzles, minijuegos, manual, bots). Lo único que falta son las ilustraciones: hoy las cartas llevan
la imagen provisional «ilustración pendiente» y los minijuegos usan dibujos CSS de respaldo.

**Regla del usuario (13-14 oct 2026): en cada imagen, expresiones faciales DISTINTAS para Cristina y Alberto** (ya escritas en el campo `arte` de cada carta).
Ambos van dibujados como personajes de dibujos animados 2D clásicos (ver `_meta.personajes` en `cartas.json`).

## 1. Ilustraciones de las 39 cartas
`python herramientas/chatgpt_imagenes.py --conectar juegos/aventuras-ca/cuento`  (Chrome con `abrir_chrome_chatgpt.ps1`; si se bloquea, recargarlo).
Primero la hoja de personajes (el prompt `hoja` de `_meta`, con la foto de Cristina y Alberto adjunta) y luego las cartas:
P, 10, 12, 14, 16, 18, 20, 22, 26, 28, 35, 37, 57, 40, 42, 44, 46, 48, 51, 52, 54, 56, 58, 38, 94, 64, 66, 78, 69, 70, 80, 72, 76, 82, 62, 74, 84, 86, 99.
Después: `herramientas/preparar_imagenes.py` (lo hace el script solo), revisar la hoja de contacto, `probar_impresion.py`, `bot_azar.py cuento ...` y capturas.
El cupo de ChatGPT es de unas 50 imágenes por tramo: 39 cartas + hoja caben en un día; lo de la parte 2 va al día siguiente.

## 2. Gráficos de los minijuegos (10 pedidos, `herramientas/pedidos/cuento.py`)
`python herramientas/chatgpt_fondos.py --solo cuento` y luego `python herramientas/listar_imagenes_ui.py juegos/aventuras-ca/cuento` (actualiza `img/ui/lista.json`;
los minijuegos solo cargan lo que está en esa lista, así que no hay errores 404 mientras no existan).

| Archivo (`img/ui/`) | Minijuego | Qué es |
|---|---|---|
| `panel.jpg`, `papel.jpg` | todos / lectores | Textura del panel y pergamino |
| `cartel.jpg` | 14 Cartel | Madera del cartel de la panadería (multiply) |
| `puente.jpg` | 20 Puente | Puente de piedra de noche (columna estrecha, screen) |
| `vidriera.jpg` | 46 Vidriera | Fondo del tablero 5×5 (screen) |
| `hadas/` (brisa, lila, nube, dalia) | 51 Hadas | Cuatro hadas SIN alas rojas ni azules (para no delatar quién miente) |
| `sala-espejos.jpg` | 64 Rayos | Suelo de la sala de espejos (screen) |
| `tarros.jpg` | 69 Tarros | Mesa de cocina de fondo |
| `animales/` (conejo, ciervo, buho, rana, ardilla, zorro) | 72 Caja de música | Animalitos de madera dorada de la partitura |
| `pagina.jpg` | 84 Última página | Página de libro en blanco (multiply) |

## 3. Otros
- Vídeo de introducción (`video/videoInicial.mp4`, guion en `_meta.video`): opcional.
- Al terminar: `regenerar_index.py` no hace falta; basta con `listar_imagenes_ui.py` y commit de `img/` y `img/ui/lista.json`.
