#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_nano_full.py — Copy de Opus 4.8 + Nano Banana 2 compone TODA la imagen
(texto integrado por la IA, estilo anuncio DR de alta conversión). 9:16."""
import os, sys, json, time
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import nano_banana as nb

OUTDIR = os.path.join(BASE, "salidas", "nano_full")
os.makedirs(OUTDIR, exist_ok=True)

def build_prompt(scene, badge, headline, keyword, bullets, cta):
    bl = " / ".join(f"'{b}'" for b in bullets)
    return f"""Create a complete, professional, ready-to-publish vertical 9:16 (1080x1920) direct-response
real estate advertisement, in the style of high-converting Meta/Facebook ads. Compose the ENTIRE
design and lay out all the text yourself, cleanly and professionally.

PHOTOREALISTIC BACKGROUND SCENE: {scene} Luxury beachfront resort on the Pacific coast of Panama,
large crystal-clear turquoise saltwater lagoon, modern white residential towers, palm trees,
warm golden-hour cinematic light. Natural realistic faces and skin, no distortion.

BRAND: "Playa Blanca Residences". Color scheme: deep cobalt blue / navy with bright CYAN accents,
modern, premium, clean. Place a small white "PLAYA BLANCA" wordmark in the TOP-LEFT corner.

Lay out the following SPANISH texts integrated over a dark gradient in the lower part of the image so
they are perfectly legible. Use EXACT spelling WITH ACCENTS (Á, É, Í, Ó, Ú, ñ). Do NOT change, translate
or misspell any word. No gibberish, no duplicated text, no lorem ipsum, no watermark.

- Small rounded BADGE in the top-right: "{badge}"
- Big BOLD UPPERCASE condensed headline. Render the words "{keyword}" in bright CYAN and the rest in WHITE:
  "{headline}"
- Three bullet lines, each preceded by a small cyan circular check icon:
  {bl}
- One bright CYAN-to-BLUE rounded CTA button with white bold uppercase text and a right arrow, reading:
  "{cta}"

Typography must be crisp, correctly spelled Spanish, professional ad design. Output the finished ad image."""

ITEMS = [
 {"scene":"A happy Latino family, parents in their late 30s with two young children, laughing together "
          "near the turquoise lagoon, casual elegant resort wear, joyful candid moment.",
  "badge":"3,500+ FAMILIAS","headline":"AQUÍ TUS HIJOS CRECEN FRENTE AL MAR","keyword":"FRENTE AL MAR",
  "bullets":["1.5 km de playa privada","Laguna navegable de agua salada","Comunidad de 3,500+ familias"],
  "cta":"AGENDA TU VISITA","out":"full_familia.png"},

 {"scene":"An elegant mature Latino couple in their late 50s on a luxury terrace at sunset, smiling, "
          "holding drinks, relaxed and aspirational.",
  "badge":"PREVENTA ABIERTA","headline":"EN PREVENTA CUESTA MENOS. MAÑANA NO.","keyword":"MAÑANA NO",
  "bullets":["Planes directos sin banco","Título a tu nombre","Unidades frente al agua limitadas"],
  "cta":"APARTA TU UNIDAD","out":"full_preventa.png"},
]

def main():
    res = []
    for i, it in enumerate(ITEMS, 1):
        prompt = build_prompt(it["scene"], it["badge"], it["headline"], it["keyword"], it["bullets"], it["cta"])
        out_path = os.path.join(OUTDIR, it["out"])
        t0 = time.time()
        g = nb.generar_fondo(prompt, ref_paths=[], out_path=out_path, aspect="9:16", timeout=240)
        dt = time.time() - t0
        if g.get("ok"):
            print(f"[{i}] OK ({dt:.0f}s, {g['bytes']} bytes) -> {it['out']}")
            res.append({"n":i, "archivo":it["out"], "headline":it["headline"]})
        else:
            print(f"[{i}] ERROR: {g.get('error')} | {str(g.get('body'))[:200]}")
            res.append({"n":i, "error":g.get("error")})
    json.dump(res, open(os.path.join(OUTDIR, "_resumen.json"), "w"), ensure_ascii=False, indent=2)
    print("=== listo ===")

if __name__ == "__main__":
    main()
