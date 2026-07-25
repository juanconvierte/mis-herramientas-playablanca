#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""render_confianza.py — 6 creativos REALES de CONFIANZA (trust). Solo data verificada
(años, entregas, comunidad, USD, extranjero compra igual, ya construido). Sin precio/URL."""
import os, sys, json, glob
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "engine"))
import gen4
from PIL import Image, ImageOps

FOTOS = os.path.join(BASE, "..", "fotos_proyecto", "a")
SALIDAS = os.path.join(BASE, "salidas"); SESION = "sesion_confianza"

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
 {"img":"ocean-3.png","fy":0.40,"kicker":"23 AÑOS CUMPLIENDO","h1":"23 años entregando, no prometiendo",
  "sub":["Un desarrollo consolidado","frente al Pacífico de Panamá."],"trust":"23 AÑOS · 1,500+ ENTREGAS",
  "cta":"Conoce la historia","out":"01_trayectoria.png"},      # trayectoria
 {"img":"napa-village.png","fy":0.40,"kicker":"NADA EN PAPEL","h1":"Camina hoy por lo que será tuyo",
  "sub":["No vendemos renders.","Vendemos lo que ya puedes tocar."],"trust":"1,500+ UNIDADES ENTREGADAS",
  "cta":"Agenda tu visita","out":"02_ya_construido.png"},      # tangible, no planos
 {"img":"DSC00798.JPG","fy":0.40,"kicker":"COMUNIDAD REAL","h1":"3,500 familias ya confían en nosotros",
  "sub":["Favorito de jubilados de","EE.UU. y Canadá."],"trust":"3,500+ FAMILIAS · 23 AÑOS",
  "cta":"Conoce más","out":"03_comunidad.png"},                # prueba social/comunidad
 {"img":"DSC00788.JPG","fy":0.42,"kicker":"PARA EXTRANJEROS TAMBIÉN","h1":"En Panamá compras en igualdad",
  "sub":["El extranjero tiene los mismos","derechos de propiedad."],"trust":"RIVIERA PACÍFICA · PANAMÁ",
  "cta":"Quiero más información","out":"04_extranjero.png"},    # seguridad para extranjeros (ley Panamá)
 {"img":"aquavista.jpg","fy":0.40,"kicker":"SIN SORPRESAS DE CAMBIO","h1":"Tu compra, en una economía en dólares",
  "sub":["Panamá usa el USD,","sin riesgo cambiario."],"trust":"ECONOMÍA DOLARIZADA · USD",
  "cta":"Conoce los planes","out":"05_usd.png"},               # estabilidad USD
 {"img":"about-hero.png","fy":0.35,"kicker":"VELO CON TUS OJOS","h1":"Visítalo antes de decidir",
  "sub":["Recorre el proyecto, la laguna","y las amenidades."],"trust":"23 AÑOS · 90 HECTÁREAS",
  "cta":"Agenda tu visita","out":"06_visita.png"},             # invitación a ver = transparencia
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
            res.append({"n":i,"img":c["img"],"h1":c["h1"],"archivo":os.path.join(SESION,c["out"]),"ok":ok})
        except Exception as e:
            print(f"[{i}] ERROR {c['img']}: {e}"); res.append({"n":i,"img":c["img"],"error":str(e)})
    json.dump(res, open(os.path.join(outdir,"_resumen.json"),"w"), ensure_ascii=False, indent=2)
    print(f"=== {sum(1 for r in res if r.get('ok'))}/{len(CRE)} OK ===")

if __name__ == "__main__":
    main()
