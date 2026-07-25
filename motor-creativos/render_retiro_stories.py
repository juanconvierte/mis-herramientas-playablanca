#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""render_retiro_stories.py — 6 creativos Stories 9:16 (1080x1920) para publico
retiro/jubilados que YA lo son y quieren vivir frente al Pacifico. Estilo gen4
(el que convierte) con ZONA SEGURA (SAFE_TOP=420 / SAFE_BOT=1500). Foto real del
proyecto + texto. COMPLIANT HOUSING: sin edad, sin escrow/sin-banco/titulo, sin
rentabilidad/plusvalia/alquiler/"se paga sola". Tono usted (Panama). Sin precio/URL
(objetivo formulario). Solo data verificada (23 anos, 3,500+ familias, 1,500+ entregas)."""
import os, sys, json, glob
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "engine"))
import kit3, gen4
from PIL import Image, ImageOps

# ---- FIX rutas nuevas (reorg jul 2026: carpeta "Playa Blanca/" ya no existe) ----
FONTS = os.path.join(BASE, "fonts") + "/"
ASSETS = os.path.join(BASE, "assets")
SALIDAS = os.path.join(BASE, "salidas")
SESION = "sesion_retiro_stories"
FOTOS = os.path.join(BASE, "..", "fotos", "proyecto", "a")

kit3.FD = FONTS  # fr()/ar()/fr_it() leen FD del modulo en cada llamada

def _logo(white=False, target_w=None):
    p = os.path.join(ASSETS, "logo_white_trim.png" if white else "logo_navy_trim.png")
    lg = Image.open(p).convert("RGBA")
    if target_w:
        r = target_w / lg.width
        lg = lg.resize((target_w, int(lg.height * r)), Image.LANCZOS)
    return lg
gen4.logo = _logo  # gen4 importo logo via 'from kit3 import *'

_realsave = gen4.save
def _save(img, path):
    # reescribe prefijo viejo -> salidas nuevas y crea carpeta
    if "salidas/" in path:
        path = os.path.join(SALIDAS, path.split("salidas/", 1)[1])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return _realsave(img, path)
gen4.save = _save

# indexar fotos y resolver src
idx = {}
for p in glob.glob(os.path.join(FOTOS, "*")):
    b = os.path.basename(p)
    if not b.startswith("._") and p.lower().endswith((".jpg", ".jpeg", ".png")):
        idx[b] = p
def _src(n):
    if n in idx: return idx[n]
    raise FileNotFoundError(n)
gen4.src = _src

CRE = [
 # 1 — NUEVA ETAPA / despertar frente al mar
 {"img":"DSC00507.JPG","fy":0.34,"kicker":"LA ETAPA QUE SE GANÓ",
  "h1":"Su nueva vida, frente al Pacífico",
  "sub":["Despierte con el mar,","no con el reloj."],
  "trust":"RIVIERA PACÍFICA DE PANAMÁ","cta":"Quiero información","out":"retiro_01.png"},
 # 2 — CAMBIAR EL RITMO / escapar de la ciudad
 {"img":"DSC00247.JPG","fy":0.40,"kicker":"CAMBIE EL RITMO",
  "h1":"Cambie el ruido de la ciudad por el mar",
  "sub":["A 1.5 h de Ciudad de Panamá,","otra forma de vivir."],
  "trust":"A 1.5 H DE LA CIUDAD","cta":"Conocer más","out":"retiro_02.png"},
 # 3 — COMUNIDAD / vecinos en su misma etapa + seguridad
 {"img":"DSC00908.JPG","fy":0.42,"kicker":"BUENA COMPAÑÍA",
  "h1":"Una comunidad que ya echó raíces",
  "sub":["Vecinos en su misma etapa,","con seguridad las 24 horas."],
  "trust":"3,500+ FAMILIAS · 23 AÑOS","cta":"Quiero conocerla","out":"retiro_03.png"},
 # 4 — BIENESTAR / caminar por la playa cada mañana
 {"img":"DSC00571.JPG","fy":0.45,"kicker":"SIN PRISA",
  "h1":"Caminar por la playa, cada mañana",
  "sub":["Buen clima todo el año","y calma para disfrutarlo."],
  "trust":"CLIMA DE PLAYA · 365 DÍAS","cta":"Quiero información","out":"retiro_04.png"},
 # 5 — FAMILIA / punto de encuentro hijos y nietos
 {"img":"piscina.jpg","fy":0.42,"kicker":"PUNTO DE ENCUENTRO",
  "h1":"El lugar donde se reúne la familia",
  "sub":["Fines de semana con hijos","y nietos, frente al mar."],
  "trust":"FRENTE A LA LAGUNA CRISTALINA","cta":"Quiero conocer más","out":"retiro_05.png"},
 # 6 — AMENIDADES / todo resuelto, usted a disfrutar
 {"img":"DSC00879.JPG","fy":0.42,"kicker":"TODO RESUELTO",
  "h1":"Usted, solo a disfrutar",
  "sub":["Piscinas, playa y áreas verdes.","Mantenimiento resuelto."],
  "trust":"1,500+ UNIDADES ENTREGADAS","cta":"Ver amenidades","out":"retiro_06.png"},
]

def main():
    outdir = os.path.join(SALIDAS, SESION); os.makedirs(outdir, exist_ok=True)
    res = []
    for i, c in enumerate(CRE, 1):
        cfg = dict(c)
        cfg["price"] = False; cfg["url"] = False; cfg["logo"] = True
        cfg["cta_w"] = 620
        cfg["out"] = os.path.join(SESION, c["out"])
        try:
            base, bot = gen4.build(cfg)
            ok = bot <= 1500  # dentro de zona segura (SAFE_BOT)
            print(f"[{i}] {'OK' if ok else 'REVISAR('+str(int(bot))+')'}  {c['img']:16s} -> {c['out']}")
            res.append({"n":i,"img":c["img"],"h1":c["h1"],
                        "archivo":os.path.join(SESION,c["out"]),"fin":int(bot),"ok":ok})
        except Exception as e:
            print(f"[{i}] ERROR {c['img']}: {e}")
            res.append({"n":i,"img":c["img"],"error":str(e)})
    json.dump(res, open(os.path.join(outdir,"_resumen.json"),"w"), ensure_ascii=False, indent=2)
    print(f"=== {sum(1 for r in res if r.get('ok'))}/{len(CRE)} OK dentro de zona segura ===")

if __name__ == "__main__":
    main()
