"""Partida completa autonoma (orden propio del bot) en Egipto y Marte. uso: python bot_aventuras.py BASE"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bot_core import *
import solvers_egipto as SE
import solvers_marte as SM

BASE = sys.argv[1]
ok1 = jugar("EGIPTO", f"{BASE}/Aventuras-CA/Egipto/pc.html", f"{BASE}/Aventuras-CA/Egipto/index.html", SE.SOLVERS, SE.REQUIERE)
ok2 = jugar("MARTE", f"{BASE}/Aventuras-CA/Marte/pc.html", f"{BASE}/Aventuras-CA/Marte/index.html", SM.SOLVERS, SM.REQUIERE)
sys.exit(0 if (ok1 and ok2) else 1)
