"""Fábrica de gráficos de interfaz con ChatGPT (Chrome abierto con abrir_chrome_chatgpt.ps1 y la sesión iniciada).

Los pedidos viven en herramientas/pedidos/*.py (uno por juego): cada módulo define PEDIDOS = [dict(...), ...] con
    destino : ruta .jpg del repo (imagen suelta) o carpeta (hoja con varios objetos)
    prompt  : lo que se le pide a ChatGPT
    ancho   : ancho final en píxeles (por defecto 720; 320 para sprites)
    hoja    : (columnas, filas) si el pedido es una hoja de varios objetos sobre fondo negro
    nombres : nombres de los objetos de la hoja, en orden de lectura (izquierda→derecha, arriba→abajo)

Los objetos van sobre NEGRO PURO: en la app se mezclan con `mix-blend-mode: screen`, así el negro desaparece y quedan
como piezas luminosas sobre el fondo. Las hojas se trocean solas (detección de objetos) y cada pieza se guarda recortada.

Uso (desde la raíz del repo):
    python herramientas/chatgpt_fondos.py                  # genera lo que falte (ignora lo que ya tiene marca .origen)
    python herramientas/chatgpt_fondos.py --solo egipto    # solo los pedidos cuyo destino contenga 'egipto'
    python herramientas/chatgpt_fondos.py --solo glifos --forzar
    python herramientas/chatgpt_fondos.py --lista          # muestra los pedidos y su estado
"""
import argparse
import runpy
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chatgpt_imagenes import RAIZ, Chat  # noqa: E402

NEGRO = (" Fondo negro puro (#000000) liso y uniforme, sin suelo, sin sombras sobre el fondo. "
         "Sin texto, letras ni números. Sin personas.")


def cargar_pedidos():
    pedidos = []
    for f in sorted((RAIZ / "herramientas" / "pedidos").glob("*.py")):
        ns = runpy.run_path(str(f), init_globals={"NEGRO": NEGRO})
        pedidos += ns.get("PEDIDOS", [])
    return pedidos


def marca_de(p):
    d = RAIZ / p["destino"]
    return (d / ".origen") if p.get("hoja") else d.with_suffix(".origen")


def ajustar(im, margen=0.05, umbral=34):
    """Recorta el negro sobrante alrededor del objeto (ignora motas sueltas de unos pocos píxeles)."""
    a = np.asarray(im.convert("L")) > umbral
    filas = np.where(a.sum(axis=1) >= 3)[0]
    cols = np.where(a.sum(axis=0) >= 3)[0]
    if len(filas) == 0 or len(cols) == 0:
        return im
    y0, y1, x0, x1 = filas[0], filas[-1], cols[0], cols[-1]
    mx, my = int((x1 - x0) * margen) + 2, int((y1 - y0) * margen) + 2
    return im.crop((max(0, x0 - mx), max(0, y0 - my), min(im.width, x1 + mx + 1), min(im.height, y1 + my + 1)))


def trocear(im, columnas, filas, n):
    """Recorta los objetos de una hoja sobre fondo negro. Devuelve n imágenes ordenadas por filas."""
    a = np.asarray(im.convert("L"))
    h, w = a.shape
    paso = max(2, w // 220)
    mini = (a[::paso, ::paso] > 38)
    # cierra huecos pequeños para unir las partes de un mismo objeto
    from PIL import ImageFilter
    m = Image.fromarray((mini * 255).astype("uint8")).filter(ImageFilter.MaxFilter(9))
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
        if len(ys) < 25:
            continue
        cajas.append((int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), len(ys)))
    cajas.sort(key=lambda c: -c[4])
    cajas = cajas[:n]
    if len(cajas) == n:
        # orden de lectura: filas por su centro vertical, dentro de cada fila por x
        cajas.sort(key=lambda c: ((c[1] + c[3]) / 2))
        por_fila = [sorted(cajas[i * columnas:(i + 1) * columnas], key=lambda c: c[0]) for i in range(filas)] if columnas * filas == n else [sorted(cajas, key=lambda c: c[0])]
        cajas = [c for fila in por_fila for c in fila]
        piezas = []
        for (x0, y0, x1, y1, _n) in cajas:
            mx = int((x1 - x0) * 0.08 * paso) + paso * 3
            my = int((y1 - y0) * 0.08 * paso) + paso * 3
            box = (max(0, x0 * paso - mx), max(0, y0 * paso - my), min(w, (x1 + 1) * paso + mx), min(h, (y1 + 1) * paso + my))
            piezas.append(im.crop(box))
        return piezas, True
    # plan B: cuadrícula regular
    piezas = []
    for r in range(filas):
        for c in range(columnas):
            if len(piezas) < n:
                piezas.append(im.crop((c * w // columnas, r * h // filas, (c + 1) * w // columnas, (r + 1) * h // filas)))
    return piezas, False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--forzar", action="store_true")
    ap.add_argument("--solo", help="texto que debe contener la ruta de destino")
    ap.add_argument("--lista", action="store_true")
    ap.add_argument("--afinar", action="store_true", help="vuelve a recortar el negro sobrante de las piezas de hoja ya generadas")
    args = ap.parse_args()
    pend = [p for p in cargar_pedidos() if (not args.solo or args.solo in p["destino"])]
    if args.lista:
        for p in pend:
            print(("hecho   " if marca_de(p).exists() else "pendiente"), p["destino"], p.get("nombres", ""))
        return
    if args.afinar:
        for p in pend:
            if p.get("hoja") and marca_de(p).exists():
                for nombre in p["nombres"]:
                    f = RAIZ / p["destino"] / f"{nombre}.jpg"
                    if f.exists():
                        pz = ajustar(Image.open(f).convert("RGB"))
                        w = p.get("ancho", 720)
                        pz.resize((w, max(1, round(pz.height * w / pz.width)))).save(f, "JPEG", quality=84, optimize=True)
                print("afinado", p["destino"])
        return
    chat = Chat(9222)
    hechas = 0
    for n, p in enumerate(pend, 1):
        destino = RAIZ / p["destino"]
        marca = marca_de(p)
        if marca.exists() and not args.forzar:
            print(f"[{n}/{len(pend)}] {p['destino']}: ya existe")
            continue
        print(f"[{n}/{len(pend)}] {p['destino']}")
        chat.nuevo_chat()
        chat.enviar(p["prompt"])
        src = chat.esperar_imagen()
        if not src:
            print("  x no salió imagen" + (" (límite)" if chat.hay_limite() else ""))
            if chat.hay_limite():
                break
            continue
        tmp = (destino / "_hoja.png") if p.get("hoja") else destino.with_suffix(".png")
        tmp.parent.mkdir(parents=True, exist_ok=True)
        chat.descargar(src, tmp)
        im = Image.open(tmp).convert("RGB")
        w = p.get("ancho", 720)
        if p.get("hoja"):
            cols, filas = p["hoja"]
            piezas, ok = trocear(im, cols, filas, len(p["nombres"]))
            for nombre, pz in zip(p["nombres"], piezas):
                pz = ajustar(pz)
                pz = pz.resize((w, max(1, round(pz.height * w / pz.width))))
                pz.save(destino / f"{nombre}.jpg", "JPEG", quality=84, optimize=True)
            print(f"  ok -> {len(piezas)} piezas" + ("" if ok else "  (¡troceado en cuadrícula, revisar!)"))
            tmp.unlink()
        else:
            im = im.resize((w, round(im.height * w / im.width)))
            im.save(destino, "JPEG", quality=80, optimize=True)
            tmp.unlink()
            print(f"  ok -> {p['destino']}")
        marca.write_text("chatgpt\n", encoding="utf-8")
        hechas += 1
        time.sleep(6)
    print(f"{hechas} pedidos generados")


if __name__ == "__main__":
    main()
