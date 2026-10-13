"""Genera con ChatGPT (Chrome abierto con abrir_chrome_chatgpt.ps1) imágenes sueltas que no son cartas:
texturas de panel, fondos, iconos... Cada elemento de PEDIDOS es (destino .jpg del repo, prompt).

Uso (desde la raíz del repo, con el Chrome de ChatGPT abierto y la sesión iniciada):
    python herramientas/chatgpt_fondos.py                 # genera las que falten
    python herramientas/chatgpt_fondos.py --forzar        # regenera todas
    python herramientas/chatgpt_fondos.py --solo egipto   # solo las que contengan 'egipto' en su ruta

Cada imagen se guarda reducida y comprimida (JPG, 720 px de ancho) en el destino indicado.
"""
import argparse
import io
import sys
import time
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chatgpt_imagenes import RAIZ, Chat  # noqa: E402

SIN = " Sin texto, letras ni números. Sin personas. Vista frontal plana, sin perspectiva, formato vertical 2:3."

PEDIDOS = [
    ("juegos/el-faro/img/ui/panel.jpg",
     "Crea una textura de panel de madera oscura de cabina de barco, con listones verticales, remaches y esquinas de latón envejecido, "
     "humedad y salitre, iluminación tenue de farol desde un lado y el centro liso y limpio para poder poner interfaz encima." + SIN),
    ("juegos/aventuras-ca/egipto/img/ui/panel.jpg",
     "Crea una textura de losa de arenisca antigua del antiguo Egipto con un marco decorativo de bandas de jeroglíficos y lapislázuli "
     "en los bordes (sin significado legible), luz cálida de antorcha y el centro liso y limpio para poder poner interfaz encima." + SIN),
    ("juegos/aventuras-ca/marte/img/ui/panel.jpg",
     "Crea una textura de panel metálico industrial de una colonia en Marte, cubierto de polvo rojizo fino, con tornillos, juntas, cables "
     "y pequeñas luces de estado naranjas en los bordes y el centro liso y limpio para poder poner interfaz encima." + SIN),
    ("juegos/aventuras-ca/florencia/img/ui/panel.jpg",
     "Crea una textura de pergamino antiguo con bordes quemados y filigrana renacentista dorada decorativa en las esquinas, luz de vela "
     "y el centro liso y limpio para poder poner interfaz encima." + SIN),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--forzar", action="store_true")
    ap.add_argument("--solo", help="texto que debe contener la ruta de destino")
    args = ap.parse_args()
    pend = [(d, p) for d, p in PEDIDOS if (not args.solo or args.solo in d)]
    chat = Chat(9222)
    hechas = 0
    try:
        for n, (destino, prompt) in enumerate(pend, 1):
            ruta = RAIZ / destino
            marca = ruta.with_suffix(".origen")  # señal de que ya es la versión de ChatGPT (y no un provisional)
            if marca.exists() and not args.forzar:
                print(f"[{n}/{len(pend)}] {destino}: ya existe")
                continue
            print(f"[{n}/{len(pend)}] {destino}")
            chat.nuevo_chat()
            chat.enviar(prompt)
            src = chat.esperar_imagen()
            if not src:
                print("  x no salió imagen" + (" (límite)" if chat.hay_limite() else ""))
                if chat.hay_limite():
                    break
                continue
            tmp = ruta.with_suffix(".png")
            chat.descargar(src, tmp)
            im = Image.open(tmp).convert("RGB")
            w = 720
            im = im.resize((w, round(im.height * w / im.width)))
            ruta.parent.mkdir(parents=True, exist_ok=True)
            im.save(ruta, "JPEG", quality=78, optimize=True)
            tmp.unlink()
            marca.write_text("chatgpt\n", encoding="utf-8")
            hechas += 1
            print(f"  ok -> {destino}")
            time.sleep(8)
    finally:
        pass
    print(f"{hechas} imágenes generadas")


if __name__ == "__main__":
    main()
