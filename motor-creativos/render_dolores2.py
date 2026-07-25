#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""render_dolores2.py — 3 creativos REALES más (~60 años): bienestar, legado/nietos,
estatus. Se suman a sesion_dolores_60. Sin precio/URL."""
import os, sys, json, glob
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "engine"))
import gen4
from PIL import Image, ImageOps

FOTOS = os.path.join(BASE, "..", "fotos_proyecto", "a")
SALIDAS = os.path.join(BASE, "salidas"); SESION = "sesion_dolores_60"

idx = {}
for p in glob.glob(os.path.join(FOTOS, "*")):
    b = os.path.basename(p)
    if not b.startswith("._") and p.lower().endswith((".jpg", ".jpeg", ".png")): idx[b] = p
def _src(n):
    if n in idx: return idx[n]
    raise FileNotFoundError(n)
gen4.src = _src

CRE = [
 {"img":"spa.jpg","fy":0.36,"kicker":"TU BIENESTAR, PRIMERO","h1":"Camina, nada y respira frente al mar",
  "sub":["Spa, golf y 1.5 km de playa","para mantenerte activo."],"trust":"SPA · GOLF · CLUB DE PLAYA",
  "cta":"Quiero conocerlo","out":"d06_bienestar.png"},   # dolor: salud/sedentarismo -> deseo: vida activa
 {"img":"DSC00908.JPG","fy":0.38,"kicker":"UN LUGAR PARA LOS TUYOS","h1":"Donde tus nietos querrán volver",
  "sub":["Reúne a la familia frente","al mar, cada verano."],"trust":"1.5 KM DE PLAYA PRIVADA · LAGUNA",
  "cta":"Agenda tu visita","out":"d07_legado.png"},      # dolor: distancia familia -> deseo: legado/nietos
 {"img":"DSC00591.JPG","fy":0.40,"kicker":"TE LO GANASTE","h1":"Para quien ya no tiene nada que demostrar",
  "sub":["El hogar frente al mar que","siempre mereciste."],"trust":"RESIDENCIAS DE LUJO · 23 AÑOS",
  "cta":"Solicita información","out":"d08_estatus.png"},  # dolor: sentirse invisible -> deseo: estatus/dignidad
]

def main():
    outdir = os.path.join(SALIDAS, SESION); os.makedirs(outdir, exist_ok=True)
    res = []
    for i, c in enumerate(CRE, 1):
        cfg = dict(c); cfg["price"] = False; cfg["url"] = False; cfg["logo"] = True
        cfg["cta"] = c["cta"].replace("→", "").strip(); cfg["out"] = os.path.join(SESION, c["out"])
        try:
            base, bot = gen4.build(cfg); ok = bot <= 1505
            print(f"[{i}] {'OK' if ok else 'REVISAR('+str(int(bot))+')'}  {c['img']:16s} -> {c['out']}")
            res.append({"img":c["img"],"h1":c["h1"],"archivo":os.path.join(SESION,c["out"]),"ok":ok})
        except Exception as e:
            print(f"[{i}] ERROR {c['img']}: {e}"); res.append({"img":c["img"],"error":str(e)})
    print(f"=== {sum(1 for r in res if r.get('ok'))}/{len(CRE)} OK ===")

if __name__ == "__main__":
    main()
