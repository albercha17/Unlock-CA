"""Ejecuta el manual completo (de la P a la 99, por la interfaz real) de los 14 juegos, uno tras otro. Uso: python herramientas/manual_todos.py [juego ...]"""
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JUEGOS = ["faro", "egipto", "marte", "florencia", "dinosaurios", "cuento", "trono", "pompeya", "arcade", "oeste", "espia", "futbol", "piratas", "juguetes", "colosos"]
sys.stdout.reconfigure(encoding="utf-8")
malos = []
for j in sys.argv[1:] or JUEGOS:
    c = "juegos/el-faro" if j == "faro" else f"juegos/aventuras-ca/{j}"
    r = subprocess.run([sys.executable, "herramientas/con_servidor.py", sys.executable, "herramientas/ejecutar_manual.py", "{URL}", c, f"datos_{j}", f"solvers_{j}"],
                       cwd=RAIZ, capture_output=True, text=True, encoding="utf-8", errors="replace")
    ok = "MANUAL VERIFICADO" in r.stdout
    print(f"{j:12} {'OK' if ok else 'FALLA'}", flush=True)
    if not ok:
        malos.append(j)
        print("   ", (r.stdout.strip().splitlines() or [""])[-1][:200])
print("RESUMEN:", "todo bien" if not malos else "fallan " + ", ".join(malos))
