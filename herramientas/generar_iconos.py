"""Genera los iconos de la app (PWA): un Cronoportal (anillo dorado con núcleo cian) sobre fondo azul verdoso.

Uso (desde la raíz del repo):  python herramientas/generar_iconos.py
Escribe assets/icons/{icon-192,icon-512,icon-maskable-512,apple-touch-icon}.png y favicon.png.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFilter

TAM = 1024


def degradado_radial(tam, centro_rgb, borde_rgb):
    img = Image.new("RGB", (tam, tam))
    px = img.load()
    c = tam / 2
    for y in range(tam):
        for x in range(tam):
            d = min(1.0, math.hypot(x - c, y - c) / (tam * 0.72))
            px[x, y] = tuple(int(centro_rgb[k] * (1 - d) + borde_rgb[k] * d) for k in range(3))
    return img


def portal(tam=TAM, margen=0.0):
    """Icono completo a tamaño `tam`; `margen` deja aire alrededor (para el icono «maskable»)."""
    fondo = degradado_radial(tam, (22, 64, 76), (5, 14, 18))
    capa = Image.new("RGBA", (tam, tam), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    c = tam / 2
    r = tam * (0.36 - margen)
    grosor = tam * 0.085
    # anillo: segmentos con degradado dorado -> cian
    pasos = 360
    for i in range(pasos):
        a0 = math.radians(i - 90)
        a1 = math.radians(i + 2 - 90)
        t = (math.sin(math.radians(i * 2)) + 1) / 2
        col = (int(217 + (61 - 217) * (1 - t) * 0.0 + (240 - 217) * t), int(164 + (214 - 164) * (1 - t) * 0.35 + (199 - 164) * t * 0.5), int(65 + (198 - 65) * (1 - t) * 0.55), 255)
        pts = [(c + math.cos(a0) * (r + grosor / 2), c + math.sin(a0) * (r + grosor / 2)), (c + math.cos(a1) * (r + grosor / 2), c + math.sin(a1) * (r + grosor / 2)),
               (c + math.cos(a1) * (r - grosor / 2), c + math.sin(a1) * (r - grosor / 2)), (c + math.cos(a0) * (r - grosor / 2), c + math.sin(a0) * (r - grosor / 2))]
        d.polygon(pts, fill=col)
    # runas: marcas en el anillo
    for i in range(12):
        a = math.radians(i * 30 - 90)
        x0, y0 = c + math.cos(a) * (r - grosor * 0.18), c + math.sin(a) * (r - grosor * 0.18)
        x1, y1 = c + math.cos(a) * (r + grosor * 0.18), c + math.sin(a) * (r + grosor * 0.18)
        d.line([(x0, y0), (x1, y1)], fill=(60, 36, 8, 255), width=int(tam * 0.008))
    # resplandor exterior del anillo
    brillo = capa.filter(ImageFilter.GaussianBlur(tam * 0.03))
    fondo = Image.alpha_composite(fondo.convert("RGBA"), brillo)
    fondo = Image.alpha_composite(fondo, capa)
    # núcleo cian
    nucleo = Image.new("RGBA", (tam, tam), (0, 0, 0, 0))
    nd = ImageDraw.Draw(nucleo)
    for k in range(40, 0, -1):
        rr = r * 0.72 * k / 40
        alfa = int(255 * (1 - k / 40) ** 1.4)
        nd.ellipse([c - rr, c - rr, c + rr, c + rr], fill=(120 + (40 - k), 255, 240, min(255, alfa + 20)))
    nucleo = nucleo.filter(ImageFilter.GaussianBlur(tam * 0.012))
    fondo = Image.alpha_composite(fondo, nucleo)
    # destello en cruz
    cruz = Image.new("RGBA", (tam, tam), (0, 0, 0, 0))
    cd = ImageDraw.Draw(cruz)
    cd.ellipse([c - tam * 0.05, c - tam * 0.05, c + tam * 0.05, c + tam * 0.05], fill=(255, 255, 255, 235))
    cd.polygon([(c, c - tam * 0.17), (c + tam * 0.012, c), (c, c + tam * 0.17), (c - tam * 0.012, c)], fill=(255, 255, 255, 190))
    cd.polygon([(c - tam * 0.17, c), (c, c - tam * 0.012), (c + tam * 0.17, c), (c, c + tam * 0.012)], fill=(255, 255, 255, 190))
    cruz = cruz.filter(ImageFilter.GaussianBlur(tam * 0.004))
    return Image.alpha_composite(fondo, cruz).convert("RGB")


def main():
    os.makedirs("assets/icons", exist_ok=True)
    normal = portal(TAM, 0.0)
    seguro = portal(TAM, 0.07)          # maskable: el motivo cabe en el 80 % central
    normal.resize((512, 512), Image.LANCZOS).save("assets/icons/icon-512.png", optimize=True)
    normal.resize((192, 192), Image.LANCZOS).save("assets/icons/icon-192.png", optimize=True)
    seguro.resize((512, 512), Image.LANCZOS).save("assets/icons/icon-maskable-512.png", optimize=True)
    normal.resize((180, 180), Image.LANCZOS).save("assets/icons/apple-touch-icon.png", optimize=True)
    normal.resize((64, 64), Image.LANCZOS).save("assets/icons/favicon.png", optimize=True)
    print("iconos escritos en assets/icons/")


if __name__ == "__main__":
    main()
