"""Pasa probar_apps.py (cada minijuego por la interfaz real) a los 14 juegos, uno tras otro, con un servidor propio por juego.
Uso:  python herramientas/probar_todos.py [juego ...]      (sin argumentos, todos)"""
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JUEGOS = ["faro", "egipto", "marte", "florencia", "dinosaurios", "cuento", "trono", "pompeya", "arcade", "oeste", "espia", "futbol", "piratas", "juguetes"]
sys.stdout.reconfigure(encoding="utf-8")


def main():
    elegidos = sys.argv[1:] or JUEGOS
    malos = []
    for j in elegidos:
        carpeta = "juegos/el-faro" if j == "faro" else f"juegos/aventuras-ca/{j}"
        r = subprocess.run([sys.executable, "herramientas/con_servidor.py", sys.executable, "herramientas/probar_apps.py", "{URL}", carpeta, f"solvers_{j}"],
                           cwd=RAIZ, capture_output=True, text=True, encoding="utf-8", errors="replace")
        lineas = [l for l in r.stdout.splitlines() if l.startswith("[") or "errores de consola" in l]
        fallos = [l for l in lineas if "FALLO" in l]
        consola = [l for l in lineas if "errores de consola" in l and "[]" not in l]
        estado = "OK" if not fallos and not consola and r.returncode == 0 else "FALLA"
        print(f"{j:12} {estado}  ({sum(1 for l in lineas if l.startswith('[') and 'OK' in l)} apps OK)")
        for l in fallos + consola:
            print("     ", l[:230])
        if estado != "OK":
            malos.append(j)
        sys.stdout.flush()
    print("RESUMEN:", "todo bien" if not malos else "fallan " + ", ".join(malos))


if __name__ == "__main__":
    main()
