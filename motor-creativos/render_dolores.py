#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""render_dolores.py — 5 creativos REALES (foto + texto, sin IA) que atacan los
DOLORES y DESEOS de una persona ~60 años. Diferenciales confirmados. Sin precio/URL."""
import os, sys, json, glob
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "engine"))
import gen4
from PIL import Image, ImageOps

FOTOS = os.path.join(BASE, "..", "fotos_proyecto", "a")
SALIDAS = os.path.join(BASE, "salidas")
SESION = "sesion_dolores_60"

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

# dolor -> deseo
CRE = [
 {"img":"DSC00586.JPG","fy":0.40,"kicker":"DEJA ATRÁS EL FRÍO","h1":"Cambia el invierno por un verano sin fin",
  "sub":["Clima de playa los 365 días,","a 1.5 h de la ciudad."],"trust":"RIVIERA PACÍFICA DE PANAMÁ",
  "cta":"Quiero conocerlo","out":"d01_clima.png"},   # dolor: frío/achaques -> deseo: calor todo el año
 {"img":"manana.jpg","fy":0.42,"kicker":"BAJA EL RITMO","h1":"El silencio que tu vida pedía",
  "sub":["Olas y brisa, en lugar","de tráfico y ruido."],"trust":"90 HECTÁREAS · PLAYA PRIVADA",
  "cta":"Agenda tu visita","out":"d02_calma.png"},   # dolor: estrés/ruido -> deseo: paz
 {"img":"piscina.jpg","fy":0.46,"kicker":"NO ESTÁS SOLO","h1":"Vecinos que se vuelven amigos",
  "sub":["Una comunidad de 3,500+ familias","que eligió vivir frente al mar."],"trust":"3,500+ FAMILIAS · CLUB DE PLAYA",
  "cta":"Conoce más","out":"d03_comunidad.png"},     # dolor: soledad -> deseo: comunidad
 {"img":"DSC00453.JPG","fy":0.40,"kicker":"NO LO SIGAS POSPONIENDO","h1":"Los mejores años son ahora, no después",
  "sub":["El mar que siempre soñaste,","por fin a tu nombre."],"trust":"VISA PENSIONADO (+55)",
  "cta":"Quiero más información","out":"d04_ahora.png"},  # dolor: tiempo se va -> deseo: vivirlo ya
 {"img":"DSC00859.JPG","fy":0.45,"kicker":"COMPRA CON CONFIANZA","h1":"Tu hogar frente al mar, con respaldo real",
  "sub":["Título a tu nombre y 23 años","entregando: 1,500+ hogares."],"trust":"23 AÑOS · 1,500+ HOGARES ENTREGADOS",
  "cta":"Solicita información","out":"d05_confianza.png"},  # dolor: miedo a perder dinero -> deseo: seguridad
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
