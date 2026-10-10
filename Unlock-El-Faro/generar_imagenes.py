"""Genera las ilustraciones de las cartas con la API de imágenes de OpenAI.

Uso (desde esta carpeta):
    python generar_imagenes.py                 # genera todas las que falten
    python generar_imagenes.py --solo 6 7 P    # solo esas cartas
    python generar_imagenes.py --calidad high  # low | medium | high (por defecto medium)
    python generar_imagenes.py --forzar        # regenera aunque ya existan

Necesita la variable de entorno OPENAI_API_KEY. Guarda en arte/ID.png.
Las cartas donde salen personajes usan arte/_personajes.png como referencia
para que Inés, Marcos y Anselmo se parezcan en todas.
"""
import argparse
import base64
import json
import sys
import time
from pathlib import Path

from openai import OpenAI

sys.stdout.reconfigure(encoding="utf-8")

AQUI = Path(__file__).parent
ARTE = AQUI / "arte"
MODELO = "gpt-image-1"
TAMANO = "1024x1536"
HOJA = ARTE / "_personajes.png"


def cargar():
    datos = json.loads((AQUI / "cartas.json").read_text(encoding="utf-8"))
    meta = datos.pop("_meta")
    return meta, datos


def orden(clave):
    return (0, 0) if clave == "P" else (1, int(clave))


def quienes_salen(arte, personajes):
    salen = [n for n in personajes if n in arte]
    if "Anselmo" in personajes and "anciano de barba blanca" in arte and "Anselmo" not in salen:
        salen.append("Anselmo")
    return salen


def prompt_carta(carta, meta):
    salen = quienes_salen(carta["arte"], meta["personajes"])
    p = ("Crea una ilustración vertical con proporción 2:3 para una carta de juego de escape room. "
         + carta["arte"])
    if salen:
        p += ("\nPersonajes (mantén exactamente el mismo aspecto que en la imagen de referencia): "
              + " ".join(meta["personajes"][n] for n in salen))
    return p + "\n" + meta["estilo"], bool(salen)


def guardar(resp, destino):
    destino.write_bytes(base64.b64decode(resp.data[0].b64_json))


def con_reintentos(fn, etiqueta):
    for intento in range(1, 4):
        try:
            return fn()
        except Exception as e:  # noqa: BLE001
            print(f"  ! {etiqueta}: {e}")
            if intento == 3:
                return None
            time.sleep(5 * intento)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--solo", nargs="*", help="ids de carta a generar")
    ap.add_argument("--calidad", default="medium", choices=["low", "medium", "high"])
    ap.add_argument("--forzar", action="store_true")
    args = ap.parse_args()

    meta, cartas = cargar()
    ids = sorted(cartas, key=orden)
    if args.solo:
        desconocidas = [i for i in args.solo if i not in cartas]
        if desconocidas:
            sys.exit(f"Cartas que no existen: {desconocidas}")
        ids = [i for i in ids if i in args.solo]

    ARTE.mkdir(exist_ok=True)
    cliente = OpenAI()

    pendientes = [i for i in ids if args.forzar or not (ARTE / f"{i}.png").exists()]
    necesita_hoja = any(quienes_salen(cartas[i]["arte"], meta["personajes"]) for i in pendientes)

    if necesita_hoja and (args.forzar or not HOJA.exists()):
        print("Generando hoja de personajes de referencia...")
        p = ("Crea una hoja de personajes (character sheet) con tres personas de cuerpo entero, "
             "de frente, sobre fondo claro y neutro:\n"
             + "\n".join(f"- {d}" for d in meta["personajes"].values()) + "\n\n" + meta["estilo"])
        r = con_reintentos(lambda: cliente.images.generate(
            model=MODELO, prompt=p, size=TAMANO, quality=args.calidad, n=1), "hoja de personajes")
        if r is None:
            sys.exit("No se pudo generar la hoja de personajes.")
        guardar(r, HOJA)
        print(f"  ok -> {HOJA.name}")

    hechas = 0
    for i in pendientes:
        p, con_personajes = prompt_carta(cartas[i], meta)
        print(f"Carta {i}: {cartas[i]['titulo']}")
        if con_personajes:
            def llamada():
                with open(HOJA, "rb") as ref:
                    return cliente.images.edit(model=MODELO, image=ref, prompt=p,
                                               size=TAMANO, quality=args.calidad, n=1)
        else:
            def llamada():
                return cliente.images.generate(model=MODELO, prompt=p, size=TAMANO,
                                               quality=args.calidad, n=1)
        r = con_reintentos(llamada, f"carta {i}")
        if r is None:
            print("  x fallida, sigo con la siguiente")
            continue
        guardar(r, ARTE / f"{i}.png")
        hechas += 1
        print(f"  ok -> arte/{i}.png")

    print(f"\nListo: {hechas} de {len(pendientes)} imágenes generadas.")


if __name__ == "__main__":
    main()
