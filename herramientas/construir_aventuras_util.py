"""fuente() y placeholder() de construir_aventuras.py, importables sin construir nada (los usa ampliacion.py)."""
import os
from PIL import Image, ImageDraw, ImageFont


def fuente(tam):
    for f in (r"C:\Windows\Fonts\segoeui.ttf", r"C:\Windows\Fonts\arial.ttf"):
        if os.path.exists(f):
            return ImageFont.truetype(f, tam)
    return ImageFont.load_default()


def placeholder(ruta, titulo, c1, c2):
    w, h = 520, 726
    im = Image.new("RGB", (w, h), c1)
    px = im.load()
    a = tuple(int(c1[i:i + 2], 16) for i in (1, 3, 5))
    b = tuple(int(c2[i:i + 2], 16) for i in (1, 3, 5))
    for y in range(h):
        t = y / (h - 1)
        col = tuple(int(a[k] * (1 - t) + b[k] * t) for k in range(3))
        for x in range(w):
            px[x, y] = col
    d = ImageDraw.Draw(im)
    f = fuente(34)
    palabras, lineas, actual = titulo.split(), [], ""
    for p in palabras:
        prueba = (actual + " " + p).strip()
        if d.textlength(prueba, font=f) > w - 90:
            lineas.append(actual)
            actual = p
        else:
            actual = prueba
    lineas.append(actual)
    y = h // 2 - 20 * len(lineas)
    for l in lineas:
        d.text(((w - d.textlength(l, font=f)) / 2, y), l, font=f, fill=(255, 255, 255))
        y += 44
    f2 = fuente(18)
    t2 = "ilustración pendiente"
    d.text(((w - d.textlength(t2, font=f2)) / 2, h - 150), t2, font=f2, fill=(255, 255, 255, 180))
    im.save(ruta, quality=82)
