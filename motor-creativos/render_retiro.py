#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""render_retiro.py — 7 creativos REALES (foto del proyecto + texto, sin IA) para
público 55-68 (retiro/jubilados). Estilo gen4 (el que convierte). Sin precio, sin URL."""
import os, sys, json, glob
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "engine"))
import gen4
from PIL import Image, ImageOps

FOTOS = os.path.join(BASE, "..", "fotos_proyecto", "a")
SALIDAS = os.path.join(BASE, "salidas")
SESION = "sesion_retiro"

idx = {}
for p in glob.glob(os.path.join(FOTOS, "*")):
    b = os.path.basename(p)
    if not b.startswith("._") and p.lower().endswith((".jpg", ".jpeg", ".png")):
        idx[b] = p
def _src(n):
    if n in idx: return idx[n]
    raise FileNotFoundError(n)
gen4.src = _src
for b, p in idx.items():
    try: ImageOps.exif_transpose(Image.open(p)).save(p)
    except Exception: pass

CRE = [
 {"img":"DSC00507.JPG","fy":0.40,"kicker":"TU RETIRO, A TU MANERA","h1":"Un retiro con vista al Pacífico",
  "sub":["Despierta frente al mar,","no frente a una sala de espera."],"trust":"VISA PENSIONADO (+55)",
  "cta":"Quiero más información","out":"retiro_01.png"},
 {"img":"DSC00490.JPG","fy":0.42,"kicker":"LOS AÑOS QUE TE GANASTE","h1":"Los mejores años se viven, no se esperan",
  "sub":["Frente a la laguna, con calma","y todo a pasos de casa."],"trust":"CLIMA DE PLAYA · 365 DÍAS",
  "cta":"Agenda tu visita","out":"retiro_02.png"},
 {"img":"DSC00611.JPG","fy":0.40,"kicker":"CAMBIA EL RITMO","h1":"Cambia el frío por el sonido del mar",
  "sub":["A 1.5 h de Ciudad de Panamá,","tu nueva vida te espera."],"trust":"RIVIERA PACÍFICA DE PANAMÁ",
  "cta":"Conoce más","out":"retiro_03.png"},
 {"img":"DSC00275.JPG","fy":0.40,"kicker":"SIN PRISA, CON VISTA","h1":"Cada atardecer, frente al Pacífico",
  "sub":["Cenas frente al mar,","en tu propio hogar."],"trust":"3,500+ FAMILIAS · 23 AÑOS",
  "cta":"Quiero más información","out":"retiro_04.png"},
 {"img":"DSC00515.JPG","fy":0.38,"kicker":"TU TRANQUILIDAD PRIMERO","h1":"Título a tu nombre, pagos en escrow",
  "sub":["Compra con seguridad jurídica","y planes directos sin banco."],"trust":"TÍTULO A TU NOMBRE · ESCROW",
  "cta":"Solicita información","out":"retiro_05.png"},
 {"img":"DSC00247.JPG","fy":0.36,"kicker":"TU NUEVA RUTINA","h1":"Tu café de la mañana, frente al mar",
  "sub":["Despertar con la laguna a tus pies.","Eso es vivir aquí."],"trust":"1.5 KM DE PLAYA PRIVADA",
  "cta":"Agenda tu visita","out":"retiro_06.png"},
 {"img":"DSC00879.JPG","fy":0.40,"kicker":"COMPRA SIN BANCO","h1":"Tu casa de retiro, sin pisar un banco",
  "sub":["Planes de pago directos","con el desarrollador."],"trust":"PLANES SIN BANCO · 23 AÑOS",
  "cta":"Quiero los planes","out":"retiro_07.png"},
]

def main():
    outdir = os.path.join(SALIDAS, SESION); os.makedirs(outdir, exist_ok=True)
    res = []
    for i, c in enumerate(CRE, 1):
        cfg = dict(c); cfg["price"] = False; cfg["url"] = False; cfg["logo"] = True
        cfg["cta"] = c["cta"].replace("→", "").strip()
        cfg["out"] = os.path.join(SESION, c["out"])
        try:
            base, bot = gen4.build(cfg)
            ok = bot <= 1505
            print(f"[{i}] {'OK' if ok else 'REVISAR('+str(int(bot))+')'}  {c['img']:16s} -> {c['out']}")
            res.append({"n":i,"img":c["img"],"h1":c["h1"],"archivo":os.path.join(SESION,c["out"]),"ok":ok})
        except Exception as e:
            print(f"[{i}] ERROR {c['img']}: {e}"); res.append({"n":i,"img":c["img"],"error":str(e)})
    json.dump(res, open(os.path.join(outdir,"_resumen.json"),"w"), ensure_ascii=False, indent=2)
    print(f"=== {sum(1 for r in res if r.get('ok'))}/{len(CRE)} OK ===")

if __name__ == "__main__":
    main()
