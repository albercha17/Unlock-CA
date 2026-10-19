"""Convierte las ilustraciones originales de un juego a JPG ligeros para la web.

Uso (desde la raiz del repo):
    python herramientas/preparar_imagenes.py juegos/aventuras-ca/egipto
    python herramientas/preparar_imagenes.py juegos/el-faro

Lee juegos/aventuras-ca/egipto/arte/ID.png (o .jpg/.jpeg/.webp; ID = numero de la carta o P; IDr.png es el reverso de una carta con `reverso`),
escribe juegos/aventuras-ca/egipto/img/ID.jpg (520 px de ancho) y quita esa carta de img/pendientes.json
para que la hoja de impresion deje de avisar de que es una ilustracion de relleno.
Las originales (arte/) no se suben a git: pesan demasiado.
"""
import json
import os
import sys

from PIL import Image

EXT = (".png", ".jpg", ".jpeg", ".webp")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    juego = sys.argv[1]
    arte, img = os.path.join(juego, "arte"), os.path.join(juego, "img")
    cartas = json.load(open(os.path.join(juego, "cartas.json"), encoding="utf-8"))
    cartas.pop("_meta", None)
    if not os.path.isdir(arte):
        sys.exit(f"No existe la carpeta {arte}. Guarda ahi las ilustraciones (por ejemplo 8.png, P.png).")
    os.makedirs(img, exist_ok=True)
    pend_ruta = os.path.join(img, "pendientes.json")
    pendientes = json.load(open(pend_ruta, encoding="utf-8")) if os.path.exists(pend_ruta) else []

    hechas, raras = [], []
    for f in sorted(os.listdir(arte)):
        base, ext = os.path.splitext(f)
        if ext.lower() not in EXT:
            continue
        es_reverso = base.endswith("r") and cartas.get(base[:-1], {}).get("reverso")     # 14r.png = el reverso de la carta 14 (cartas con dos caras)
        if base not in cartas and not es_reverso:
            raras.append(f)
            continue
        im = Image.open(os.path.join(arte, f)).convert("RGB")
        w = 520
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        im.save(os.path.join(img, base + ".jpg"), quality=80, optimize=True)
        hechas.append(base)
        if base in pendientes:
            pendientes.remove(base)
    json.dump(pendientes, open(pend_ruta, "w", encoding="utf-8"))
    print(f"Convertidas {len(hechas)} ilustraciones: {', '.join(hechas) or 'ninguna'}")
    if raras:
        print("Ignoradas (el nombre no es una carta del juego):", ", ".join(raras))
    print(f"Todavia de relleno ({len(pendientes)}): {', '.join(pendientes) or 'ninguna'}")


if __name__ == "__main__":
    main()
