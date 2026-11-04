"""Sustituye los dibujos por código de «El Cuarto de Leo, 1995» (juguetes, estantería, cubos y marioneta) por los sprites que dibuja ChatGPT
(herramientas/sprites_chatgpt.py + pedidos_sprites/juguetes.py). juguetes.py llama a activar(modulo, carpeta) al empezar: si faltan sprites, no cambia nada.

  spr-<juguete>.png   16 juguetes con transparencia       dib-<dibujo>.png  6 dibujos de ceras sobre papel (cubos)
  estanteria-vacia.png  estantería de tres baldas           pipo-cuerpo / pipo-brazo / pipo-pierna.png  piezas de la marioneta
Los juguetes se componen por código (colores cambiados, boca abajo, de balda), así la foto Polaroid y la estantería de la app son idénticas salvo
las diferencias previstas."""
import colorsys
import os

import numpy as np
from PIL import Image, ImageOps

S = 2                                   # supersampling de oeste.Hoja
ALTO = {"patito": 80, "tambor": 74, "cohete": 100, "libro": 92, "pelota": 82, "coche": 64, "osito": 100, "barco": 92, "cubos": 94, "cometa": 100,
        "trompo": 92, "xilofono": 66, "dado": 62, "robot": 100, "caballito": 90, "trenecito": 68}
BALDAS = (0.328, 0.617, 0.908)          # alto (en fracción de la imagen) de la cara superior de cada balda, medido en estanteria-vacia.png
RECORTE_ESTANTERIA = 12                 # píxeles de borde magenta que se quitan de estanteria-vacia.png
HB = 120.0                              # alto del cuerpo de Pipo (unidades de lámina con k = 1)
REL_BRAZO, REL_PIERNA = 0.795, 0.866    # alto del brazo y de la pierna respecto al del cuerpo (medidos en la hoja de ChatGPT)
HOMBRO_I, HOMBRO_D, CADERA_Y = (0.19, 0.655), (0.81, 0.64), 0.93
PIVOTE_BRAZO, PIVOTE_PIERNA = (0.547, 0.07), (0.478, 0.072)
ANG_BRAZO = (10, 155)                   # grados respecto a «colgando»: abajo, arriba
ANG_PIERNA = (4, 55)


class Sprites:
    def __init__(self, carpeta):
        self.ui = os.path.join(carpeta, "img", "ui")
        self._c = {}

    def carga(self, nombre):
        if nombre not in self._c:
            ruta = os.path.join(self.ui, nombre + ".png")
            self._c[nombre] = Image.open(ruta).convert("RGBA") if os.path.exists(ruta) else None
        return self._c[nombre]


def recolor(img, rgb):
    """Cambia el matiz de las partes con color de un sprite al del color pedido (el blanco, el negro y los grises no cambian)."""
    a = np.asarray(img).astype(np.float32) / 255.0
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    mx, mn = a[:, :, :3].max(axis=2), a[:, :, :3].min(axis=2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    h_dest = colorsys.rgb_to_hsv(*[c / 255.0 for c in rgb])[0]
    out = a.copy()
    sel = (sat > 0.35) & (a[:, :, 3] > 0.05)
    ys, xs = np.where(sel)
    for y, x in zip(ys.tolist(), xs.tolist()):
        _, s, v = colorsys.rgb_to_hsv(r[y, x], g[y, x], b[y, x])
        out[y, x, :3] = colorsys.hsv_to_rgb(h_dest, s, v)
    return Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8), "RGBA")


def activar(m, carpeta):
    """Cambia las funciones de dibujo de juguetes.py (módulo `m`) por las de sprites, si los sprites existen."""
    sp = Sprites(carpeta)
    if sp.carga("spr-patito") is None:
        print("  (sin sprites de juguetes: se usan los dibujos por código)")
        return
    viejo = {"juguete": m.juguete, "dibujar_estanteria": m.dibujar_estanteria, "dibujar_marioneta": m.dibujar_marioneta, "punto_miembro": m.punto_miembro,
             "dibujo_cubo": m.dibujo_cubo, "zonas_diferencias": m.zonas_diferencias, "ui_estanteria": m.ui_estanteria, "_cubos_ui": m._cubos_ui}
    cache_col = {}

    # ------------------------------------------------------------ juguetes
    def juguete(h, nombre, cx, base, k=1.0, color=None, boca_abajo=False):
        spr = sp.carga("spr-" + nombre)
        if spr is None:
            return viejo["juguete"](h, nombre, cx, base, k, color, boca_abajo)
        if color is not None:
            clave = (nombre, tuple(color))
            if clave not in cache_col:
                cache_col[clave] = recolor(spr, color)
            spr = cache_col[clave]
        if boca_abajo:
            spr = ImageOps.flip(spr)
        alto = ALTO.get(nombre, 60) * k / 1.1
        hp = max(2, round(alto * S))
        wp = max(2, round(spr.width * hp / spr.height))
        r = spr.resize((wp, hp), Image.LANCZOS)
        h.im.paste(r.convert("RGB"), (int(cx * S - wp / 2), int(base * S - hp)), r.getchannel("A"))

    def ancho_juguete(nombre, k=1.1):
        spr = sp.carga("spr-" + nombre)
        alto = ALTO.get(nombre, 60) * k / 1.1
        return spr.width * alto / spr.height if spr is not None else 90

    # ------------------------------------------------------------ estantería
    est = sp.carga("estanteria-vacia")

    def fondo_estanteria():
        r = RECORTE_ESTANTERIA
        return est.convert("RGB").crop((r, r, est.width - r, est.height - r))

    def dibujar_estanteria(h, x0, y0, ancho, inst, despues):
        e = inst["estanteria"]
        fondo = fondo_estanteria()
        alto_img = ancho * fondo.height / fondo.width
        h.im.paste(fondo.resize((round(ancho * S), round(alto_img * S)), Image.LANCZOS), (round(x0 * S), round(y0 * S)))
        k = ancho / 600
        baldas = {b: [list(t) for t in lista] for b, lista in e["antes"].items()}
        colores = {}
        girado = False
        if despues:
            for c in e["cambios"]:
                if c["tipo"] == "color":
                    colores[c["juguete"]] = m.COLORES_NOMBRE[c["hasta"]]
                elif c["tipo"] == "falta":
                    for b in baldas.values():
                        b[:] = [t for t in b if t[0] != c["juguete"]]
                elif c["tipo"] == "girado":
                    girado = True
                elif c["tipo"] == "sobra":
                    baldas[c["balda"]].append([c["juguete"], c["x"]])
                elif c["tipo"] == "movido":
                    for b in baldas.values():
                        b[:] = [t for t in b if t[0] != c["juguete"]]
                    baldas[c["a_balda"]].append([c["juguete"], c["x"]])
        for b in ("0", "1", "2"):
            base = y0 + BALDAS[int(b)] * alto_img + 3 * k
            for nombre, x in baldas[b]:
                juguete(h, nombre, x0 + x * k, base, 1.1 * k, color=colores.get(nombre), boca_abajo=girado and nombre == "cohete")

    def ui_estanteria(inst):
        h = m.Hoja(620, 424, (230, 216, 190))
        dibujar_estanteria(h, 10, 12, 600, inst, despues=True)
        return h.final()

    def zonas_diferencias(inst):
        """Rectángulos (en % de la imagen de la estantería de ahora, 620 x 424) de las diferencias, para el minijuego."""
        e = inst["estanteria"]
        W2, H2, x0, y0 = 620, 424, 10, 12
        fondo = fondo_estanteria()
        alto_img = 600 * fondo.height / fondo.width
        zonas = []

        def caja(nombre, x, balda):
            base = y0 + BALDAS[int(balda)] * alto_img + 3
            w, al = ancho_juguete(nombre) + 8, ALTO[nombre] + 6
            return [round((x0 + x - w / 2) / W2 * 100, 2), round((base - al) / H2 * 100, 2), round(w / W2 * 100, 2), round(al / H2 * 100, 2)]
        pos = {n: (b, x) for b, lista in e["antes"].items() for n, x in lista}
        for c in e["cambios"]:
            if c["tipo"] in ("color", "falta", "girado"):
                b, x = pos[c["juguete"]]
                zonas.append([caja(c["juguete"], x, b)])
            elif c["tipo"] == "sobra":
                zonas.append([caja(c["juguete"], c["x"], c["balda"])])
            elif c["tipo"] == "movido":
                b, x = pos[c["juguete"]]
                zonas.append([caja(c["juguete"], c["x"], c["a_balda"]), caja(c["juguete"], x, b)])
        return zonas

    # ------------------------------------------------------------ cubos
    def dibujo_cubo(nombre, lado):
        d = sp.carga("dib-" + nombre)
        if d is None:
            return viejo["dibujo_cubo"](nombre, lado)
        im = d.convert("RGB")
        arr = np.asarray(im).astype(np.float32)
        fuera = np.sqrt(((arr - np.array((255, 0, 255), dtype=np.float32)) ** 2).sum(axis=2)) < 150       # restos del fondo magenta
        ys, xs = np.where(~fuera)
        if len(ys):
            x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
            ix, iy = int((x1 - x0) * 0.08), int((y1 - y0) * 0.08)       # el papel sale algo girado: se recorta por dentro
            im = im.crop((int(x0) + ix, int(y0) + iy, int(x1) - ix, int(y1) - iy))
        t = min(im.size)
        im = im.crop(((im.width - t) // 2, (im.height - t) // 2, (im.width - t) // 2 + t, (im.height - t) // 2 + t))
        return im.resize((lado, lado), Image.LANCZOS)

    def cubos_ui(cu):
        os.makedirs(sp.ui, exist_ok=True)
        for nombre in cu["dibujos"]:
            im = dibujo_cubo(nombre, 240)
            for q, (x, y) in enumerate(((0, 0), (120, 0), (0, 120), (120, 120))):
                im.crop((x, y, x + 120, y + 120)).save(os.path.join(sp.ui, f"cubo-{nombre}-{q}.png"))

    # ------------------------------------------------------------ marioneta
    cuerpo, brazo, pierna = sp.carga("pipo-cuerpo"), sp.carga("pipo-brazo"), sp.carga("pipo-pierna")
    if cuerpo is not None and brazo is not None and pierna is not None:
        def geometria(cx, top, k):
            """Posiciones (en unidades de lámina) del cuerpo y de los puntos de giro de los miembros."""
            hb = HB * k
            wb = cuerpo.width * hb / cuerpo.height
            x0, y0 = cx - wb / 2, top - 20 * k
            return {"hb": hb, "wb": wb, "x0": x0, "y0": y0,
                    "brazo_izq": (x0 + HOMBRO_I[0] * wb, y0 + HOMBRO_I[1] * hb), "brazo_der": (x0 + HOMBRO_D[0] * wb, y0 + HOMBRO_D[1] * hb),
                    "pierna_izq": (cx - 0.2 * wb, y0 + CADERA_Y * hb), "pierna_der": (cx + 0.2 * wb, y0 + CADERA_Y * hb)}

        def angulo(nombre, arriba):
            lado = -1 if nombre.endswith("izq") else 1
            a = ANG_BRAZO if nombre.startswith("brazo") else ANG_PIERNA
            return lado * (a[1] if nombre in arriba else a[0])

        def pegar_miembro(h, spr, pivote, pos, alto_px, ang):
            wp = spr.width * alto_px / spr.height
            r = spr.resize((max(2, round(wp)), max(2, round(alto_px))), Image.LANCZOS)
            lado = int(2 * max(r.size) + 4)
            lienzo = Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
            px, py = pivote[0] * r.width, pivote[1] * r.height
            lienzo.paste(r, (round(lado / 2 - px), round(lado / 2 - py)), r)
            lienzo = lienzo.rotate(ang, resample=Image.BICUBIC, center=(lado / 2, lado / 2))
            h.im.paste(lienzo.convert("RGB"), (round(pos[0] * S - lado / 2), round(pos[1] * S - lado / 2)), lienzo.getchannel("A"))

        def dibujar_marioneta(h, cx, top, arriba=(), k=1.0, hilos=True):
            g = geometria(cx, top, k)
            for n in ("pierna_izq", "pierna_der"):
                pegar_miembro(h, pierna, PIVOTE_PIERNA, g[n], REL_PIERNA * g["hb"] * S, angulo(n, arriba))
            r = cuerpo.resize((round(g["wb"] * S), round(g["hb"] * S)), Image.LANCZOS)
            h.im.paste(r.convert("RGB"), (round(g["x0"] * S), round(g["y0"] * S)), r.getchannel("A"))
            for n in ("brazo_izq", "brazo_der"):
                pegar_miembro(h, brazo, PIVOTE_BRAZO, g[n], REL_BRAZO * g["hb"] * S, angulo(n, arriba))

        def punto_miembro(cx, top, nombre, arriba, k=1.0):
            import math
            g = geometria(cx, top, k)
            if nombre.startswith("brazo"):
                largo, p = REL_BRAZO * g["hb"] * (1 - PIVOTE_BRAZO[1]) * 0.9, g[nombre]
            else:
                largo, p = REL_PIERNA * g["hb"] * (1 - PIVOTE_PIERNA[1]) * 0.9, g[nombre]
            t = math.radians(angulo(nombre, arriba))
            return (p[0] + largo * math.sin(t), p[1] + largo * math.cos(t))
        m.dibujar_marioneta, m.punto_miembro = dibujar_marioneta, punto_miembro


    # ------------------------------------------------------------ imágenes de la interfaz (img/ui)
    def alfa_magenta(im):
        c = np.array((255, 0, 255), dtype=np.float32)
        a = np.asarray(im.convert("RGB")).astype(np.float32)
        alfa = np.clip((np.sqrt(((a - c) ** 2).sum(axis=2)) - 70) / 90.0, 0, 1)
        rgb = a.copy()
        b = (alfa > 0) & (alfa < 1)
        if b.any():
            kk = alfa[b][:, None]
            rgb[b] = np.clip((a[b] - c * (1 - kk)) / np.maximum(kk, 0.05), 0, 255)
        return Image.fromarray(np.dstack([rgb, alfa * 255]).astype(np.uint8), "RGBA")

    def ui_imagenes(carpeta_juego, inst):
        ui = os.path.join(carpeta_juego, "img", "ui")
        os.makedirs(ui, exist_ok=True)
        ui_estanteria(inst).save(os.path.join(ui, "estanteria.jpg"), quality=90)
        miembros = inst["marioneta"]["miembros"]
        for bits in range(16):
            arriba = tuple(mi for i, mi in enumerate(miembros) if bits >> i & 1)
            h = m.Hoja(240, 320, (255, 0, 255))
            m.dibujar_marioneta(h, 120, 60, arriba, k=1.0)
            alfa_magenta(h.final()).save(os.path.join(ui, f"pipo-{bits}.png"))
        for nombre in sorted(set(inst["folioscopio"]["juguetes"]) | set(inst["memoria"]["imagenes"])):
            spr = sp.carga("spr-" + nombre)
            if spr is None:
                continue
            t = 110
            r = spr.resize((max(2, round(spr.width * t / max(spr.size))), max(2, round(spr.height * t / max(spr.size)))), Image.LANCZOS)
            lienzo = Image.new("RGBA", (t, t), (0, 0, 0, 0))
            lienzo.paste(r, ((t - r.width) // 2, t - r.height - 2), r)
            lienzo.save(os.path.join(ui, f"jug-{nombre}.png"))
        cubos_ui(inst["cubos"])

    m.juguete, m.dibujar_estanteria, m.ui_estanteria, m.zonas_diferencias = juguete, dibujar_estanteria, ui_estanteria, zonas_diferencias
    m.dibujo_cubo, m._cubos_ui, m.ui_imagenes = dibujo_cubo, cubos_ui, ui_imagenes
    print("  (sprites de ChatGPT activados: juguetes, estantería, cubos y marioneta)")
