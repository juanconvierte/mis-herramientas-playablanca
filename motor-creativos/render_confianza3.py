#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""render_confianza3.py — 3 creativos REALES de CONFIANZA (trust), nuevos/distintos
de la sesion_confianza previa. Solo data VERIFICADA (23 años, 1,500+ entregas,
3,500+ familias, 90 hectáreas, ya construido). Sin precio/URL. Sin escrow/sin-banco/
título/edad (no verificados o riesgo HOUSING)."""
import os, sys, json, glob
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "engine"))
import gen4
from PIL import Image, ImageOps

FOTOS = os.path.join(BASE, "..", "fotos_proyecto", "a")
SALIDAS = os.path.join(BASE, "salidas"); SESION = "sesion_confianza3"

idx = {}
for p in glob.glob(os.path.join(FOTOS, "*")):
    b = os.path.basename(p)
    if not b.startswith("._") and p.lower().endswith((".jpg", ".jpeg", ".png")): idx[b] = p
def _src(n):
    if n in idx: return idx[n]
    raise FileNotFoundError(n)
gen4.src = _src
for b, p in idx.items():
    try: ImageOps.exif_transpose(Image.open(p)).save(p)
    except Exception: pass

CRE = [
 {"img":"masterplan.png","fy":0.38,"kicker":"TRAYECTORIA REAL","h1":"El tiempo ya nos dio la razón",
  "sub":["23 años de desarrollo consolidado,","no una promesa en papel."],"trust":"23 AÑOS · 1,500+ ENTREGAS",
  "cta":"Conoce la historia","out":"01_autoridad.png"},        # autoridad / trayectoria
 {"img":"DSC00908.JPG","fy":0.42,"kicker":"COMUNIDAD CONSOLIDADA","h1":"Donde 3,500 familias echaron raíces",
  "sub":["Favorito de jubilados de EE.UU.","y Canadá, frente al Pacífico."],"trust":"3,500+ FAMILIAS · 23 AÑOS",
  "cta":"Conoce más","out":"02_comunidad.png"},                # prueba social / comunidad
 {"img":"terrazas-villas.png","fy":0.40,"kicker":"YA CONSTRUIDO","h1":"No compras planos. Compras realidad",
  "sub":["Camina hoy por lo que ya","está construido y entregado."],"trust":"1,500+ UNIDADES ENTREGADAS",
  "cta":"Agenda tu visita","out":"03_ya_construido.png"},      # tangible / sin riesgo
]

def main():
    outdir = os.path.join(SALIDAS, SESION); os.makedirs(outdir, exist_ok=True)
    res = []
    for i, c in enumerate(CRE, 1):
        cfg = dict(c); cfg["price"] = False; cfg["url"] = False; cfg["logo"] = True
        cfg["cta"] = c["cta"].replace("→", "").strip(); cfg["out"] = os.path.join(SESION, c["out"])
        try:
            base, bot = gen4.build(cfg); ok = bot <= 1505
            print(f"[{i}] {'OK' if ok else 'REVISAR('+str(int(bot))+')'}  {c['img']:18s} -> {c['out']}")
            res.append({"n":i,"img":c["img"],"h1":c["h1"],"archivo":os.path.join(SESION,c["out"]),"ok":ok})
        except Exception as e:
            print(f"[{i}] ERROR {c['img']}: {e}"); res.append({"n":i,"img":c["img"],"error":str(e)})
    json.dump(res, open(os.path.join(outdir,"_resumen.json"),"w"), ensure_ascii=False, indent=2)
    print(f"=== {sum(1 for r in res if r.get('ok'))}/{len(CRE)} OK ===")

if __name__ == "__main__":
    main()
