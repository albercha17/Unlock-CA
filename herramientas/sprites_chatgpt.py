"""Fábrica de sprites con ChatGPT (Chrome abierto con abrir_chrome_chatgpt.ps1 y la sesión iniciada): objetos de colores con TRANSPARENCIA.

A diferencia de chatgpt_fondos.py (objetos luminosos sobre negro, para mezclar con «screen»), aquí ChatGPT dibuja las hojas de objetos sobre un fondo de
color puro (magenta por defecto), y esta herramienta quita ese color, trocea la hoja en objetos sueltos y guarda cada uno como PNG con transparencia
(o recortado tal cual, para dibujos sobre papel). Los pedidos viven en herramientas/pedidos_sprites/<juego>.py (variable PEDIDOS):
    destino : carpeta donde se guardan las piezas (p. ej. juegos/aventuras-ca/juguetes/img/ui)
    prefijo : texto que se antepone al nombre de cada pieza (p. ej. «spr-» -> spr-patito.png)
    prompt  : lo que se le pide a ChatGPT (la herramienta añade las reglas del fondo)
    hoja    : (columnas, filas)
    nombres : nombres de los objetos en orden de lectura (izquierda→derecha, arriba→abajo)
    clave   : color del fondo, «magenta» (por defecto), «verde» o «azul»
    modo    : «alfa» (quita el fondo; por defecto) o «recorte» (conserva el fondo dentro del recuadro; para dibujos sobre papel)
    ancho   : ancho máximo de cada pieza (por defecto 360)
Uso (desde la raíz del repo):
    python herramientas/sprites_chatgpt.py --lista
    python herramientas/sprites_chatgpt.py --solo juguetes          # genera lo que falte (los pedidos con marca .origen se saltan)
    python herramientas/sprites_chatgpt.py --solo juguetes --forzar
"""
import argparse
import runpy
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chatgpt_imagenes import RAIZ, Chat  # noqa: E402

COLORES = {"magenta": (255, 0, 255), "verde": (0, 255, 0), "azul": (0, 120, 255)}
NOMBRE_COLOR = {"magenta": "magenta puro (#FF00FF)", "verde": "verde puro (#00FF00)", "azul": "azul puro (#0078FF)"}
REGLAS = (" Cada objeto va SEPARADO de los demás, con mucho espacio entre ellos, de frente y entero (sin recortar), sobre un fondo {c} liso y uniforme, sin suelo, sin sombras "
          "proyectadas sobre el fondo ni reflejos. Los objetos NO deben contener ese color. Sin texto, letras ni números. Sin personas. Iluminación suave y uniforme.")


def cargar_pedidos():
    pedidos = []
    for f in sorted((RAIZ / "herramientas" / "pedidos_sprites").glob("*.py")):
        ns = runpy.run_path(str(f))
        for p in ns.get("PEDIDOS", []):
            p["_origen"] = f.stem
            pedidos.append(p)
    return pedidos


def marca_de(p):
    return RAIZ / p["destino"] / f"{p.get('prefijo', '')}{p['nombres'][0]}.origen"


def alfa_clave(im, clave="magenta"):
    """Devuelve la imagen RGBA sin el color de fondo (borde suave y sin halo del color)."""
    c = np.array(COLORES[clave], dtype=np.float32)
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    dist = np.sqrt(((a - c) ** 2).sum(axis=2))
    alfa = np.clip((dist - 70) / 90.0, 0, 1)
    # quita el halo: en los bordes semitransparentes, aleja el color del fondo
    rgb = a.copy()
    borde = (alfa > 0) & (alfa < 1)
    if borde.any():
        k = alfa[borde][:, None]
        rgb[borde] = np.clip((a[borde] - c * (1 - k)) / np.maximum(k, 0.05), 0, 255)
    out = np.dstack([rgb, alfa * 255]).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def cajas_objetos(im, clave, n, columnas, filas):
    """Encuentra las cajas de los n objetos más grandes de la hoja (fondo de color) y las ordena por filas."""
    c = np.array(COLORES[clave], dtype=np.float32)
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    h, w, _ = a.shape
    paso = max(2, w // 240)
    mini = np.sqrt(((a[::paso, ::paso] - c) ** 2).sum(axis=2)) > 110
    m = Image.fromarray((mini * 255).astype("uint8")).filter(ImageFilter.MaxFilter(7))
    m = np.asarray(m) > 0
    etiquetas = np.zeros(m.shape, dtype=int)
    n_et = 0
    for y in range(m.shape[0]):
        for x in range(m.shape[1]):
            if m[y, x] and etiquetas[y, x] == 0:
                n_et += 1
                pila = [(y, x)]
                etiquetas[y, x] = n_et
                while pila:
                    cy, cx = pila.pop()
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < m.shape[0] and 0 <= nx < m.shape[1] and m[ny, nx] and etiquetas[ny, nx] == 0:
                            etiquetas[ny, nx] = n_et
                            pila.append((ny, nx))
    cajas = []
    for e in range(1, n_et + 1):
        ys, xs = np.where(etiquetas == e)
        if len(ys) < 30:
            continue
        cajas.append((int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), len(ys)))
    cajas.sort(key=lambda b: -b[4])
    cajas = cajas[:n]
    ok = len(cajas) == n
    if ok:
        cajas.sort(key=lambda b: (b[1] + b[3]) / 2)
        por_fila = [sorted(cajas[i * columnas:(i + 1) * columnas], key=lambda b: b[0]) for i in range(filas)]
        cajas = [b for fila in por_fila for b in fila]
        return [(x0 * paso, y0 * paso, (x1 + 1) * paso, (y1 + 1) * paso) for x0, y0, x1, y1, _ in cajas], True
    # plan B: cuadrícula regular
    return [(cc * w // columnas, r * h // filas, (cc + 1) * w // columnas, (r + 1) * h // filas) for r in range(filas) for cc in range(columnas)][:n], False


def limpiar_motas(rgba, minimo=0.04):
    """Quita las motas sueltas (restos de objetos vecinos): conserva solo las manchas de al menos `minimo` veces la mayor."""
    a = np.asarray(rgba)[:, :, 3] > 24
    paso = 3
    mini = a[::paso, ::paso]
    m = Image.fromarray((mini * 255).astype("uint8")).filter(ImageFilter.MaxFilter(7))
    m = np.asarray(m) > 0
    et = np.zeros(m.shape, dtype=int)
    n = 0
    areas = {}
    for y in range(m.shape[0]):
        for x in range(m.shape[1]):
            if m[y, x] and et[y, x] == 0:
                n += 1
                pila = [(y, x)]
                et[y, x] = n
                cuenta = 0
                while pila:
                    cy, cx = pila.pop()
                    cuenta += 1
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < m.shape[0] and 0 <= nx < m.shape[1] and m[ny, nx] and et[ny, nx] == 0:
                            et[ny, nx] = n
                            pila.append((ny, nx))
                areas[n] = cuenta
    if not areas:
        return rgba
    mayor = max(areas.values())
    buenos = [k for k, v in areas.items() if v >= mayor * minimo]
    mascara = np.isin(et, buenos)
    grande = np.kron(mascara, np.ones((paso, paso), dtype=bool))[:a.shape[0], :a.shape[1]]
    if grande.shape != a.shape:
        grande = np.pad(grande, ((0, a.shape[0] - grande.shape[0]), (0, a.shape[1] - grande.shape[1])))
    arr = np.asarray(rgba).copy()
    arr[:, :, 3] = np.where(grande, arr[:, :, 3], 0)
    return Image.fromarray(arr, "RGBA")


def recortar_alfa(rgba, margen=4):
    a = np.asarray(rgba)[:, :, 3] > 24
    ys, xs = np.where(a)
    if len(ys) == 0:
        return rgba
    return rgba.crop((max(0, xs.min() - margen), max(0, ys.min() - margen), min(rgba.width, xs.max() + margen + 1), min(rgba.height, ys.max() + margen + 1)))


def procesar_hoja(im, p):
    clave = p.get("clave", "magenta")
    cols, filas = p["hoja"]
    cajas, ok = cajas_objetos(im, clave, len(p["nombres"]), cols, filas)
    ancho = p.get("ancho", 360)
    piezas = []
    for (x0, y0, x1, y1) in cajas:
        mx, my = int((x1 - x0) * 0.04) + 3, int((y1 - y0) * 0.04) + 3
        caja = (max(0, x0 - mx), max(0, y0 - my), min(im.width, x1 + mx), min(im.height, y1 + my))
        pz = im.crop(caja)
        if p.get("modo", "alfa") == "alfa":
            pz = recortar_alfa(limpiar_motas(alfa_clave(pz, clave)))
        else:
            pz = pz.convert("RGB")
            c = np.array(COLORES[clave], dtype=np.float32)
            solido = np.sqrt(((np.asarray(pz).astype(np.float32) - c) ** 2).sum(axis=2)) > 150
            ys, xs = np.where(solido)
            if len(ys):                                   # quita el borde de color de fondo que rodea al recorte
                ix, iy = int((xs.max() - xs.min()) * 0.01) + 1, int((ys.max() - ys.min()) * 0.01) + 1
                pz = pz.crop((int(xs.min()) + ix, int(ys.min()) + iy, int(xs.max()) - ix, int(ys.max()) - iy))
        if pz.width > ancho:
            pz = pz.resize((ancho, max(1, round(pz.height * ancho / pz.width))), Image.LANCZOS)
        piezas.append(pz)
    return piezas, ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--solo", help="texto que debe contener el nombre del fichero de pedidos o la carpeta de destino")
    ap.add_argument("--forzar", action="store_true")
    ap.add_argument("--lista", action="store_true")
    ap.add_argument("--reprocesar", action="store_true", help="vuelve a trocear las hojas ya guardadas (_hoja-*.png/jpg) sin pedir nada a ChatGPT")
    args = ap.parse_args()
    pend = [p for p in cargar_pedidos() if not args.solo or args.solo in p["destino"] or args.solo == p["_origen"]]
    if args.lista:
        for p in pend:
            print("hecho    " if marca_de(p).exists() else "pendiente", p["destino"], p.get("prefijo", ""), p["nombres"])
        return
    if args.reprocesar:
        for p in pend:
            destino = RAIZ / p["destino"]
            hoja = next((destino / f"_hoja-{p['nombres'][0]}{e}" for e in (".png", ".jpg") if (destino / f"_hoja-{p['nombres'][0]}{e}").exists()), None)
            if hoja is None:
                print("sin hoja guardada:", p["nombres"][0])
                continue
            piezas, ok = procesar_hoja(Image.open(hoja).convert("RGB"), p)
            for nombre, pz in zip(p["nombres"], piezas):
                pz.save(destino / f"{p.get('prefijo', '')}{nombre}.png", "PNG", optimize=True)
            print("reprocesado", p["nombres"][0], len(piezas), "" if ok else "(cuadrícula)")
        return
    chat = Chat(9222)
    hechas = 0
    for n, p in enumerate(pend, 1):
        marca = marca_de(p)
        if marca.exists() and not args.forzar:
            print(f"[{n}/{len(pend)}] {p['destino']} {p['nombres'][:3]}…: ya existe")
            continue
        print(f"[{n}/{len(pend)}] {p['destino']} {p['nombres'][:3]}…")
        chat.nuevo_chat()
        chat.enviar(p["prompt"] + REGLAS.format(c=NOMBRE_COLOR[p.get("clave", "magenta")]))
        src = chat.esperar_imagen()
        if not src:
            print("  x no salió imagen" + (" (límite)" if chat.hay_limite() else ""))
            if chat.hay_limite():
                break
            continue
        destino = RAIZ / p["destino"]
        destino.mkdir(parents=True, exist_ok=True)
        tmp = destino / "_hoja.png"
        chat.descargar(src, tmp)
        im = Image.open(tmp).convert("RGB")
        piezas, ok = procesar_hoja(im, p)
        im.save(destino / f"_hoja-{p['nombres'][0]}.png", "PNG")   # la hoja original (para --reprocesar y para revisar)
        tmp.unlink()
        for nombre, pz in zip(p["nombres"], piezas):
            pz.save(destino / f"{p.get('prefijo', '')}{nombre}.png", "PNG", optimize=True)
        print(f"  ok -> {len(piezas)} piezas" + ("" if ok else "  (¡troceado en cuadrícula, revisar!)"))
        marca.write_text("chatgpt\n", encoding="utf-8")
        hechas += 1
        time.sleep(6)
    print(f"{hechas} pedidos generados")


if __name__ == "__main__":
    main()
