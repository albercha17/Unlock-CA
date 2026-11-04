"""Captura las 11 apps de cada juego y las junta en UN montaje por juego (para revisar de un vistazo qué se ve cutre).
Uso:  python herramientas/capturar_todos.py <carpeta_salida> [juego ...]      (sin juegos: los 14)
Escribe <carpeta_salida>/montaje-<juego>.png (4 columnas, cada app a media escala)."""
import os
import subprocess
import sys

from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JUEGOS = ["faro", "egipto", "marte", "florencia", "dinosaurios", "cuento", "trono", "pompeya", "arcade", "oeste", "espia", "futbol", "piratas", "juguetes"]
sys.path.insert(0, os.path.join(RAIZ, "herramientas"))


def main():
    salida = sys.argv[1]
    juegos = sys.argv[2:] or JUEGOS
    os.makedirs(salida, exist_ok=True)
    for j in juegos:
        carpeta = "juegos/el-faro" if j == "faro" else f"juegos/aventuras-ca/{j}"
        solv = __import__(f"solvers_{j}")
        cartas = list(solv.SOLVERS)
        tmp = os.path.join(salida, "_tmp-" + j)
        subprocess.run([sys.executable, "herramientas/con_servidor.py", sys.executable, "herramientas/capturar_apps.py", "{URL}", carpeta, tmp] + cartas,
                       cwd=RAIZ, capture_output=True, text=True)
        fotos = [os.path.join(tmp, f"{os.path.basename(carpeta)}-{c}.png") for c in cartas]
        fotos = [f for f in fotos if os.path.exists(f)]
        if not fotos:
            print(j, "sin capturas")
            continue
        ims = [Image.open(f).convert("RGB") for f in fotos]
        w, h = 252, 374
        cols = 4
        filas = (len(ims) + cols - 1) // cols
        lienzo = Image.new("RGB", (cols * w, filas * h), (20, 20, 24))
        for i, im in enumerate(ims):
            lienzo.paste(im.resize((w, h), Image.LANCZOS), ((i % cols) * w, (i // cols) * h))
        lienzo.save(os.path.join(salida, f"montaje-{j}.png"))
        print("ok", j, len(ims), "apps")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
