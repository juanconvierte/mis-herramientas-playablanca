#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""render_60.py — 6 creativos REALES para 60-65, con DATA VERIFICADA del sitio +
psicología de venta. Sin escrow/sin-banco/retornos. Sin precio/URL."""
import os, sys, json, glob
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "engine"))
import gen4
from PIL import Image, ImageOps

FOTOS = os.path.join(BASE, "..", "fotos_proyecto", "a")
SALIDAS = os.path.join(BASE, "salidas"); SESION = "sesion_60_65"

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

# cada uno: palanca psicológica + dato verificado
CRE = [
 {"img":"DSC00571.JPG","fy":0.40,"kicker":"NO SERÁS EL ÚNICO","h1":"Jubilados de EE.UU. y Canadá ya viven aquí",
  "sub":["Una comunidad de 3,500+ familias","frente al Pacífico de Panamá."],"trust":"3,500+ FAMILIAS · 23 AÑOS",
  "cta":"Quiero más información","out":"01_prueba_social.png"},   # prueba social + pertenencia
 {"img":"about-hero.png","fy":0.35,"kicker":"NADA DE PLANOS","h1":"Ya construido, no es un proyecto en papel",
  "sub":["23 años y 1,500+ hogares entregados.","Tu seguridad, primero."],"trust":"23 AÑOS · 1,500+ ENTREGAS",
  "cta":"Agenda tu visita","out":"02_seguridad.png"},            # reducción de miedo / confianza
 {"img":"hero-lagoon.jpg","fy":0.30,"kicker":"SIN RIESGO CAMBIARIO","h1":"Tu retiro en una economía en dólares",
  "sub":["Panamá usa el USD,","a 1 hora de la capital."],"trust":"ECONOMÍA DOLARIZADA · USD",
  "cta":"Quiero conocerlo","out":"03_usd.png"},                  # seguridad financiera (factual, sin retornos)
 {"img":"DSC00599.JPG","fy":0.40,"kicker":"PARA DISFRUTAR EL RETIRO","h1":"El retiro que te ganaste, frente al mar",
  "sub":["Con los beneficios del Programa","Pensionado de Panamá."],"trust":"PROGRAMA PENSIONADO · +55",
  "cta":"Solicita información","out":"04_pensionado.png"},        # identidad + beneficio real
 {"img":"4_1.jpg","fy":0.42,"kicker":"CERCA DE LOS TUYOS","h1":"Tus nietos, a un vuelo corto",
  "sub":["A 5 minutos del aeropuerto,","cada visita es fácil."],"trust":"5 MIN DEL AEROPUERTO · RÍO HATO",
  "cta":"Agenda tu visita","out":"05_familia.png"},              # familia / miedo a la distancia
 {"img":"playa.jpg","fy":0.42,"kicker":"TU NUEVA RUTINA","h1":"Del café al green en un desayuno",
  "sub":["4 campos de golf a minutos,","frente al Pacífico."],"trust":"4 CAMPOS DE GOLF · CLUB DEPORTIVO",
  "cta":"Quiero conocerlo","out":"06_golf.png"},                 # estilo de vida activo
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
