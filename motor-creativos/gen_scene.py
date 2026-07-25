#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_scene.py — Pipeline 0% error: Nano Banana 2 genera SOLO la escena (sin texto)
y el motor (dr_estilo) compone TODO el texto perfecto en zona segura. Relleno ambiente
en bordes. Uso: python3 gen_scene.py [draft|final] [nombre...]"""
import sys, os, time
BASE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, BASE)
import nano_banana as nb
import dr_estilo as dr
from gen_final import _safe_frame, MODELS, EP
from PIL import Image

OUT = os.path.join(BASE, "salidas", "nano_final"); os.makedirs(OUT, exist_ok=True)

SCENE_RULES = (" Single continuous full-bleed photorealistic photograph, 9:16 vertical, premium cinematic "
   "magazine quality, realistic faces and hands no distortion. The people are centered in the UPPER-MIDDLE "
   "of the frame; the LOWER THIRD is calmer, simpler and a bit darker (uncluttered) for text; the TOP-LEFT "
   "corner is clear open sky / distant out-of-focus scenery for a logo. Brand mood: cobalt blue, navy, cyan, "
   "warm golden light. IMPORTANT: absolutely NO text, words, letters, numbers, logos, watermarks or UI.")

ITEMS = {
 "aspiracion": {
   "scene": "A stylish aspirational Latino couple in their early 40s toasting with sparkling wine on a rooftop "
            "infinity-pool terrace at golden-hour sunset, overlooking a huge turquoise saltwater lagoon, modern "
            "white residential towers and palms of a luxury beachfront resort on the Pacific coast of Panama.",
   "fy": 0.34, "badge": "PREVENTA", "badge_color": [26, 86, 200],
   "headline": "Vivir *frente al mar* ya es posible",
   "bullets": ["Planes de pago directos, sin banco", "Título de propiedad a tu nombre", "Cupos de preventa limitados"],
   "cta": "Quiero mi plan"},
 "retiro": {
   "scene": "A happy vital retired Latino couple in their mid-60s walking barefoot and holding hands on a private "
            "white-sand beach at warm sunset, a luxury beachfront resort with a turquoise lagoon and modern white "
            "towers softly behind them, Pacific coast of Panama.",
   "fy": 0.36, "badge": "VISA PENSIONADO +55", "badge_color": [20, 120, 90],
   "headline": "Tu retiro *frente al mar* en Panamá",
   "bullets": ["Título a tu nombre y pagos en escrow", "Planes de pago directos, sin banco", "1.5 km de playa privada y 15+ amenidades"],
   "cta": "Agenda tu visita"},
 "amenidades": {
   "scene": "A happy young Latino family with two kids enjoying a luxury beach club and pool, palm trees, turquoise "
            "saltwater lagoon and modern white residential towers of a beachfront resort on the Pacific coast of Panama.",
   "fy": 0.34, "badge": "15+ AMENIDADES", "badge_color": [26, 86, 200],
   "headline": "Tu club de playa *a un paso de casa*",
   "bullets": ["Club de playa y 1.5 km de arena", "Spa, golf, tenis y gimnasio", "Laguna de agua salada navegable"],
   "cta": "Conoce las amenidades"},
}

def run(name, tier):
    it = ITEMS[name]
    raw = os.path.join(OUT, f"{name}_scene.png")
    if tier == "reuse":                              # 0 API: reusa la escena ya generada
        if not os.path.exists(raw):
            print(f"ERROR no hay escena guardada para {name} (usa draft/final primero)"); return
        print(f"  REUSE escena {name} (0 llamadas API)")
    else:
        for model in MODELS[tier]:
            nb.ENDPOINT = EP.format(model)
            t0 = time.time()
            g = nb.generar_fondo(it["scene"] + SCENE_RULES, ref_paths=[], out_path=raw, aspect="9:16", timeout=240)
            if g.get("ok"):
                print(f"  escena OK [{tier}:{model}] {time.time()-t0:.0f}s"); break
            print(f"  fallo {model}: {g.get('error')}")
        else:
            print(f"ERROR escena {name}"); return
    dr._idx[name] = raw
    cfg = {"img": name, "fy": it["fy"], "badge": it["badge"], "badge_color": it["badge_color"],
           "headline": it["headline"], "bullets": it["bullets"], "cta": it["cta"], "out": f"{name}.png"}
    out = os.path.join(OUT, f"{name}.png")
    dr.build(cfg, out)                              # motor compone TODO el texto + logo
    im = _safe_frame(Image.open(out).convert("RGBA"))   # relleno ambiente bordes
    im.convert("RGB").save(out, quality=95)
    print(f"OK {name} -> {out}")

if __name__ == "__main__":
    args = sys.argv[1:]
    tier = args[0] if args and args[0] in (list(MODELS) + ["reuse"]) else "final"
    names = [a for a in args if a in ITEMS] or list(ITEMS)
    for n in names: run(n, tier)
