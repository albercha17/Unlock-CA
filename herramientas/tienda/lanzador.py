"""Lanzador de la producción de pedidos: lo ejecuta la tarea programada «Cronoportal pedidos» cada 10 minutos.

Mantiene una copia del repo en %USERPROFILE%/.cronoportal/app, al día con la rama main de GitHub (solo descarga
cuando hay un commit nuevo) y ejecuta su herramientas/tienda/produccion.py. Lo copia ahí `produccion.py --instalar`.
"""
import io
import json
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from datetime import datetime
from pathlib import Path

REPO = "albercha17/Unlock-CA"
BASE = Path.home() / ".cronoportal"
APP = BASE / "app"
LOG = BASE / "produccion.log"
if sys.stdout is None:
    sys.stdout = sys.stderr = open(LOG, "a", encoding="utf-8", buffering=1)


def log(*a):
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "[lanzador]", *a, flush=True)


def leer(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "cronoportal", "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def actualizar():
    marca = BASE / "app.sha"
    try:
        sha = json.loads(leer(f"https://api.github.com/repos/{REPO}/commits/main"))["sha"]
    except Exception as e:  # noqa: BLE001  sin internet: se usa la copia que haya
        log(f"No pude mirar GitHub ({e}); uso la copia actual.")
        return
    if APP.exists() and marca.exists() and marca.read_text().strip() == sha:
        return
    log(f"Descargando la versión {sha[:7]} de main...")
    datos = leer(f"https://codeload.github.com/{REPO}/zip/{sha}", timeout=600)
    nueva = BASE / "app-nueva"
    shutil.rmtree(nueva, ignore_errors=True)
    with zipfile.ZipFile(io.BytesIO(datos)) as z:
        z.extractall(nueva)
    raiz = next(nueva.iterdir())  # Unlock-CA-<sha>/
    shutil.rmtree(APP, ignore_errors=True)
    raiz.rename(APP)
    shutil.rmtree(nueva, ignore_errors=True)
    marca.write_text(sha)
    log("Copia actualizada.")


def main():
    actualizar()
    script = APP / "herramientas" / "tienda" / "produccion.py"
    if not script.exists():
        log("No hay copia del programa todavía.")
        return
    python = Path(sys.executable)
    python = python.with_name("python.exe") if python.name.lower() == "pythonw.exe" else python
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    subprocess.run([str(python), str(script), *sys.argv[1:]], cwd=APP, stdout=sys.stdout, stderr=sys.stderr,
                   creationflags=flags, check=False)


if __name__ == "__main__":
    main()
