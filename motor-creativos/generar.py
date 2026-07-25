#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generar.py — Orquestador: toma fotos (carpeta o zip) + lista de ángulos (JSON)
y renderiza creativos 1080x1920 con el motor Playa Blanca.

Uso:
  python3 generar.py --fotos work/fotos --angulos angulos.json --salida salidas
  python3 generar.py --zip misfotos.zip --angulos angulos.json

angulos.json = lista de objetos. Cada uno (mapea a tu brief):
  { "angulo":"Prueba social", "img":"DSC001.jpg", "fy":0.4,
    "kicker":"EYEBROW", "h1":"TITULAR", "sub":["línea 1","línea 2"],
    "price_text":"$193,912 USD",  (sin la palabra 'Desde', el motor la pone)
    "trust":"3,500+ FAMILIAS · 23 AÑOS", "cta":"Únete a ellas →",
    "badge":null, "out":"01_prueba_social.png" }
"""
import os, sys, json, zipfile, argparse, glob
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "engine"))

def fix_exif(folder):
    from PIL import Image, ImageOps
    n = 0
    for p in glob.glob(os.path.join(folder, "**", "*"), recursive=True):
        if p.lower().endswith((".jpg", ".jpeg", ".png")) and "/._" not in p and not os.path.basename(p).startswith("._"):
            try:
                ImageOps.exif_transpose(Image.open(p)).save(p); n += 1
            except Exception:
                pass
    return n

def listar_fotos(folder):
    out = []
    for p in sorted(glob.glob(os.path.join(folder, "**", "*"), recursive=True)):
        b = os.path.basename(p)
        if p.lower().endswith((".jpg", ".jpeg", ".png")) and not b.startswith("._"):
            out.append(b)
    return out

def render_uno(cfg, fotos_dir, salida_dir):
    import gen4
    # índice basename -> ruta real (recursivo) y override de src() del motor
    idx = {}
    for p in glob.glob(os.path.join(fotos_dir, "**", "*"), recursive=True):
        b = os.path.basename(p)
        if b not in idx and not b.startswith("._") and "__MACOSX" not in p:
            idx[b] = p
    def _src(n):
        if n in idx:
            return idx[n]
        raise FileNotFoundError(n)
    gen4.src = _src
    # precio: el motor antepone "Desde" → quitar si el usuario ya lo puso
    pt = (cfg.get("price_text") or "").strip()
    if pt.lower().startswith("desde"):
        pt = pt[5:].strip()
    c = {
        "img": cfg["img"], "fx": cfg.get("fx", 0.5), "fy": cfg.get("fy", 0.4),
        "logo": cfg.get("logo", True), "kicker": cfg.get("kicker", ""),
        "h1": cfg.get("h1", ""), "sub": cfg.get("sub", []),
        "price_text": pt, "trust": cfg.get("trust", ""),
        "cta": cfg.get("cta", ""), "cta_style": cfg.get("cta_style", "white"),
        "block_shift": cfg.get("block_shift", 110),
        "out": cfg.get("out") or (cfg.get("angulo", "creativo").lower().replace(" ", "_") + ".png"),
    }
    if cfg.get("badge"):
        c["badge"] = cfg["badge"]
    base, bot = gen4.build(c)
    return os.path.join(salida_dir, c["out"]), int(bot)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fotos"); ap.add_argument("--zip")
    ap.add_argument("--angulos", required=True)
    ap.add_argument("--salida", default=os.path.join(BASE, "salidas"))
    a = ap.parse_args()

    fotos_dir = a.fotos or os.path.join(BASE, "work", "fotos")
    if a.zip:
        os.makedirs(fotos_dir, exist_ok=True)
        with zipfile.ZipFile(a.zip) as z:
            z.extractall(fotos_dir)
    n = fix_exif(fotos_dir)
    print(f"[fotos] {n} corregidas EXIF · disponibles: {listar_fotos(fotos_dir)[:12]}")
    os.makedirs(a.salida, exist_ok=True)

    angulos = json.load(open(a.angulos, encoding="utf-8"))
    if isinstance(angulos, dict):
        angulos = angulos.get("angulos") or list(angulos.values())
    res = []
    for i, cfg in enumerate(angulos, 1):
        try:
            ruta, bot = render_uno(cfg, fotos_dir, a.salida)
            estado = "OK" if bot <= 1505 else f"REVISAR(texto baja a {bot})"
            print(f"[{i:02}] {estado}  {os.path.basename(ruta)}")
            res.append({"angulo": cfg.get("angulo"), "archivo": os.path.basename(ruta), "ok": bot <= 1505})
        except Exception as e:
            print(f"[{i:02}] ERROR {cfg.get('angulo','?')}: {e}")
            res.append({"angulo": cfg.get("angulo"), "error": str(e)})
    ok = sum(1 for r in res if r.get("ok"))
    print(f"\n=== {ok}/{len(angulos)} creativos generados en {a.salida} ===")
    json.dump(res, open(os.path.join(a.salida, "_resultado.json"), "w"), ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
