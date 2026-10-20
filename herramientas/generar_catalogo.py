"""Genera juegos/catalogo.json: la lista de juegos con su dificultad (1-5), duración y nº de cartas.

Fuente de verdad: herramientas/juegos_config.py (dificultad y minutos de cada aventura). El Faro está aquí a mano.
Lo leen los menús (assets/js/menu.js), la página «Mis partidas» y la app para guardar resultados con el id del juego.

Uso (desde la raíz del repo):  python herramientas/generar_catalogo.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from juegos_config import JUEGOS  # noqa: E402


def n_cartas(carpeta):
    d = json.load(open(f"{carpeta}/cartas.json", encoding="utf-8"))
    return len([k for k in d if not k.startswith("_")])


catalogo = [dict(id="faro", nombre="El Faro de Cabo Niebla", ruta="juegos/el-faro/", dificultad=2, minutos=75, cartas=n_cartas("juegos/el-faro"))]
for nombre, cfg in JUEGOS.items():
    carpeta = f"juegos/aventuras-ca/{nombre.lower()}"
    catalogo.append(dict(id=nombre.lower(), nombre=cfg["titulo"], ruta=carpeta + "/", dificultad=cfg.get("dificultad", 3),
                         minutos=cfg.get("minutos", 60), cartas=n_cartas(carpeta)))
with open("juegos/catalogo.json", "w", encoding="utf-8", newline="\n") as f:
    json.dump(catalogo, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(len(catalogo), "juegos en juegos/catalogo.json")
