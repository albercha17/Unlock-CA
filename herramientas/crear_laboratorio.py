"""Genera juegos/laboratorio/datos.js con instancias (solución única comprobada) para los prototipos del laboratorio.

Uso (desde la raíz): python herramientas/crear_laboratorio.py [semilla]
Las páginas del laboratorio (juegos/laboratorio/*.html) leen estas constantes. Cada prototipo es una idea de la guía de puzles (§7.9)
para probar el tacto en el móvil antes de meterla en un juego.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generadores_puzles as G  # noqa: E402

semilla = int(sys.argv[1]) if len(sys.argv) > 1 else 7
datos = {}
datos["nonograma"] = G.nonograma(6, 6, semilla)
datos["akari"] = G.akari(6, semilla)
cb = G.caja_negra(semilla=semilla)
cb["ejemplos"] = [[list(map(list, e)), bool(r)] for e, r in cb["ejemplos"]]
datos["cajaNegra"] = cb
datos["rosetta"] = None
for s in range(semilla, semilla + 60):
    r = G.rosetta(s)
    if r["unica"]:
        datos["rosetta"] = r
        break
datos["zebra"] = G.zebra(semilla=semilla)
datos["caballeros"] = G.caballeros(4, semilla)
rh = G.rush_hour(semilla)
rh["ruta"] = G.rush_hour_ruta(rh)
datos["bloques"] = rh
tb = G.tubos(3, 4, 2, semilla)
tb["ruta"] = G.tubos_ruta(tb)
datos["tubos"] = tb
datos["puentes"] = G.hashi(7, 7, semilla)
os.makedirs("juegos/laboratorio", exist_ok=True)
with open("juegos/laboratorio/datos.js", "w", encoding="utf-8", newline="\n") as f:
    f.write("// Generado por herramientas/crear_laboratorio.py (no editar a mano)\nwindow.LAB = " + json.dumps(datos, ensure_ascii=False, indent=1) + ";\n")
print("datos.js escrito con semilla", semilla, list(datos))
