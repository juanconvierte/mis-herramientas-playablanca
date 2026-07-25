#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_nano_dr.py — Pipeline ganador: Nano Banana 2 genera la ESCENA fotorrealista
(sin texto) → dr_estilo superpone el texto DR nítido. Salida lista para Meta."""
import os, sys, json, time
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import nano_banana as nb
import dr_estilo as dr

OUTDIR = os.path.join(BASE, "salidas", "nano_dr")
os.makedirs(OUTDIR, exist_ok=True)

STYLE = ("Ultra-photorealistic lifestyle real-estate photograph, vertical 9:16 format, "
         "cinematic premium magazine quality, warm golden-hour light with subtle cobalt-blue accents, "
         "shallow depth of field, natural realistic faces and skin, no distortion, no extra limbs. "
         "Setting: a luxury beachfront residential resort on the Pacific coast of Panama with a large "
         "crystal-clear turquoise saltwater lagoon, modern white residential towers and palm trees. "
         "IMPORTANT: do NOT add any text, words, letters, numbers, logos, watermarks or graphic UI. "
         "Keep the lower third of the frame calmer, simpler and slightly darker so text can be overlaid later.")

ITEMS = [
 {"scene":"A happy Latino family — parents in their late 30s with two young children — laughing and "
          "playing together at the edge of the turquoise lagoon, casual elegant resort wear, joyful "
          "candid moment, the family positioned in the upper-middle of the frame.",
  "fy":0.30,"badge":"3,500+ FAMILIAS","badge_color":[26,86,200],
  "headline":"Aquí tus hijos crecen *frente al mar*",
  "bullets":["1.5 km de playa privada","Laguna navegable de agua salada","Comunidad de 3,500+ familias"],
  "cta":"Agenda tu visita","raw":"escena_familia.png","out":"familia_DR.png"},

 {"scene":"An elegant mature Latino couple in their late 50s walking hand in hand along the private "
          "white-sand beach at sunset, relaxed and smiling, resort wear, the couple in the upper-middle "
          "of the frame, calm sand and water in the lower third.",
  "fy":0.32,"badge":"VISA PENSIONADO","badge_color":[20,120,90],
  "headline":"Tu retiro merece *playa*, no sala de espera",
  "bullets":["Visa Pensionado para mayores de 55","Clima de playa los 365 días","Spa, golf y club a pasos de casa"],
  "cta":"Quiero conocerlo","raw":"escena_retiro.png","out":"retiro_DR.png"},
]

def main():
    res = []
    for i, it in enumerate(ITEMS, 1):
        raw_path = os.path.join(OUTDIR, it["raw"])
        prompt = it["scene"] + "\n\n" + STYLE
        t0 = time.time()
        g = nb.generar_fondo(prompt, ref_paths=[], out_path=raw_path, aspect="9:16", timeout=200)
        dt = time.time() - t0
        if not g.get("ok"):
            print(f"[{i}] ERROR escena: {g.get('error')} | {str(g.get('body'))[:200]}")
            res.append({"n":i, "error": g.get("error")}); continue
        print(f"[{i}] escena OK ({dt:.0f}s, {g['bytes']} bytes) -> {it['raw']}")
        key = f"nano_dr_{i}"
        dr._idx[key] = raw_path
        cfg = {"img":key, "fy":it["fy"], "badge":it["badge"], "badge_color":it["badge_color"],
               "headline":it["headline"], "bullets":it["bullets"], "cta":it["cta"], "out":it["out"]}
        out_path = os.path.join(OUTDIR, it["out"])
        dr.build(cfg, out_path)
        print(f"[{i}] DR OK -> {it['out']}")
        res.append({"n":i, "escena":it["raw"], "final":it["out"], "headline":it["headline"]})
    json.dump(res, open(os.path.join(OUTDIR, "_resumen.json"), "w"), ensure_ascii=False, indent=2)
    print("=== listo ===")

if __name__ == "__main__":
    main()
