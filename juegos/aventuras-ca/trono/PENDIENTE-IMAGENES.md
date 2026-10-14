# Trono: imágenes pendientes

El juego está completo y probado (cartas, minijuegos, solucionadores, manual y bots), pero **no tiene ilustraciones reales todavía**: las 39 cartas
llevan la imagen provisional «ilustración pendiente» (`img/*.jpg`) y los minijuegos usan dibujos CSS/SVG de respaldo. Las imágenes se generan con
ChatGPT cuando haya cupo (unas 50 por tramo; se libera al día siguiente, ver el mensaje «Vuelve a intentarlo mañana a las HH:MM»).

## Orden recomendado (para repartir en dos o tres días)

1. **Hoja de personajes** (`prompts.html` → hoja) y las **cartas** (39): en una sola tanda salen ~40 imágenes.
   ```
   powershell herramientas/abrir_chrome_chatgpt.ps1        # Chrome con depuración remota (puerto 9222); si se queda bloqueado, recargarlo
   python herramientas/chatgpt_imagenes.py --conectar juegos/aventuras-ca/trono
   ```
   Regla del usuario: **expresiones distintas en cada imagen** (cada `arte` ya las indica: sorpresa, concentración, miedo, alegría, duda...).
   Después, `preparar_imagenes` (se ejecuta solo), revisar la hoja de contactos y repetir `probar_impresion.py`.
2. **Gráficos de los minijuegos** (13 imágenes, catálogo en `herramientas/pedidos/trono.py`):
   ```
   python herramientas/chatgpt_fondos.py --solo trono
   python herramientas/listar_imagenes_trono.py            # escribe img/ui/disponibles.json: los minijuegos solo usan lo que está en la lista
   ```
   Texturas: `piedra`, `mesa`, `mapa`, `cripta`, `puerta`, `pergamino`. Sprites sobre negro: `cuervo`, `castillo`, `antorcha`. Piezas del atasco: `tronco`,
   `carro`. Tapiz: `tapiz/hilo`. Retratos (hoja 4x1): `consejeros/{aldric,brenna,corvin,dalia}`.
3. **Vídeo de introducción** (opcional): el prompt está en `prompts.html`; se guarda como `video/videoInicial.mp4`.

## Después de generar
`python herramientas/probar_apps.py <URL> juegos/aventuras-ca/trono solvers_trono`, `bot_azar.py <URL> trono 5`, `probar_impresion.py juegos/aventuras-ca/trono`,
`capturar_minijuegos.py` (revisar el aspecto con imágenes) y `auditar_minijuegos.py juegos/aventuras-ca/trono`.
