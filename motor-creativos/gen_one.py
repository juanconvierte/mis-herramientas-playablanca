#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_one.py — Genera UN creativo desde un spec JSON (lo escribe el agente Director
de Diseño). Uso: python3 gen_one.py <draft|final> <spec.json>
spec = {name, scene, badge, headline, keyword, bullets[3], cta, layout_notes?}"""
import sys, os, json
BASE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, BASE)
import nano_banana as nb
from gen_final import FRAME, finalize, MODELS, EP, OUT

def build(spec):
    bl = " / ".join(f'"{b}"' for b in spec["bullets"])
    return (f'{spec["scene"]}\n'
            f'BRAND COLORS: deep cobalt blue & navy with bright CYAN.\n'
            f'SPANISH COPY (exact, with accents):\n'
            f'- badge: "{spec["badge"]}"\n'
            f'- headline UPPERCASE, words "{spec.get("keyword","")}" in cyan, rest white: "{spec["headline"]}"\n'
            f'- bullets with cyan check icons: {bl}\n'
            f'(Do NOT draw a CTA button — leave clean dark space below the bullets; the button is added later.)\n'
            f'{spec.get("layout_notes","")}\n' + FRAME)

def main():
    tier = sys.argv[1]; spec = json.load(open(sys.argv[2], encoding="utf-8"))
    name = spec["name"]; out = os.path.join(OUT, f"{name}_{tier}.png")
    for model in MODELS[tier]:
        nb.ENDPOINT = EP.format(model)
        g = nb.generar_fondo(build(spec), ref_paths=[], out_path=out, aspect="9:16", timeout=240)
        if g.get("ok"):
            finalize(out, spec.get("cta")); print(f"OK {name} [{tier}:{model}] -> {out}"); return out
        print(f"  fallo {model}: {g.get('error')}")
    print(f"ERROR {name}"); return None

if __name__ == "__main__":
    main()
