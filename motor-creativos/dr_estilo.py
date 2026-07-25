#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dr_estilo.py — Creativos estilo 'ganador DR' sobre FOTOS REALES.
Titular CAPS con keyword en cian + bullets con check + badge + botón CTA brillante.
ÚNICA REGLA: 1080x1920 (9:16) con TEXTO en zona segura central 420-1500 (no se recorta)."""
import os, sys, json, glob
import numpy as np
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "engine"))
from kit3 import ar, logo, WHITE, COBALT_D
from designkit import open_fixed, cover_crop, enhance_premium, gradient_pill, save, draw_arrow
from PIL import Image, ImageDraw

W, H = 1080, 1920
SAFE_TOP, SAFE_BOT = 420, 1500
CYAN = (56, 208, 255)
FOTOS = os.path.join(BASE, "..", "fotos_proyecto", "a")
SALIDAS = os.path.join(BASE, "salidas")
SESION = "dr_estilo"

_idx = {}
for p in glob.glob(os.path.join(FOTOS, "*")):
    b = os.path.basename(p)
    if not b.startswith("._") and p.lower().endswith((".jpg", ".jpeg", ".png")):
        _idx[b] = p
def src(n):
    if n in _idx: return _idx[n]
    raise FileNotFoundError(n)

def photo_bg(name, fy=0.38):
    im = cover_crop(open_fixed(src(name)), W, H, 0.5, fy)
    im = enhance_premium(im, color=1.06, contrast=1.10, bright=0.96, sharp=1.06)
    return im.convert("RGBA")

def scrim(base, text_top):
    yy = np.linspace(0, 1, H)
    ramp_start = (text_top - 170) / H
    body = np.clip((yy - ramp_start) / 0.16, 0, 1) * 212
    top = np.clip((0.10 - yy) / 0.10, 0, 1) * 140
    alpha = np.clip(50 + body + top, 0, 255).astype("uint8")
    col = np.zeros((H, W, 4), dtype="uint8")
    col[:, :, 0] = 4; col[:, :, 1] = 11; col[:, :, 2] = 30
    col[:, :, 3] = alpha[:, None]
    base.alpha_composite(Image.fromarray(col, "RGBA"))

_PUNCT = set(".,;:!?¿¡()")
def _toks(text):
    text = text.upper()
    out, cur, hl = [], "", False
    for ch in text:
        if ch == "*":
            if cur: out.append((cur, hl)); cur = ""
            hl = not hl
        elif ch == " ":
            if cur: out.append((cur, hl)); cur = ""
        else:
            cur += ch
    if cur: out.append((cur, hl))
    merged = []
    for w, h in out:
        if merged and all(c in _PUNCT for c in w):
            merged[-1] = (merged[-1][0] + w, merged[-1][1])   # junta puntuación a la palabra previa
        else:
            merged.append((w, h))
    return merged

def _wrap(d, toks, f, maxw, space):
    lines, cur, cw = [], [], 0
    for word, hl in toks:
        ww = d.textlength(word, font=f)
        add = ww if not cur else cw + space + ww
        if cur and add > maxw:
            lines.append(cur); cur = [(word, hl)]; cw = ww
        else:
            cur.append((word, hl)); cw = add
    if cur: lines.append(cur)
    return lines

def draw_headline(base, text, x, y, maxw, size=78, lh=84):
    d = ImageDraw.Draw(base)
    f = ar(size, 830, 84)
    space = d.textlength(" ", font=f)
    for line in _wrap(d, _toks(text), f, maxw, space):
        cx = x
        for word, hl in line:
            d.text((cx + 2, y + 3), word, font=f, fill=(3, 9, 26))
            d.text((cx, y), word, font=f, fill=CYAN if hl else WHITE)
            cx += d.textlength(word, font=f) + space
        y += lh
    return y

def n_lines(base, text, maxw, size=78):
    d = ImageDraw.Draw(base); f = ar(size, 830, 84)
    return len(_wrap(d, _toks(text), f, maxw, d.textlength(" ", font=f)))

def draw_bullets(base, items, x, y, lh=62):
    f = ar(30, 520)
    for it in items:
        cy = y + lh // 2; r = 18
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(ov).ellipse([x, cy - r, x + 2 * r, cy + r], fill=CYAN + (255,))
        base.alpha_composite(ov)
        d = ImageDraw.Draw(base)
        d.line([(x + 11, cy + 1), (x + 16, cy + 9)], fill=(6, 18, 46), width=4)
        d.line([(x + 16, cy + 9), (x + 26, cy - 7)], fill=(6, 18, 46), width=4)
        bb = d.textbbox((0, 0), it, font=f)
        d.text((x + 2 * r + 20, cy - (bb[3] - bb[1]) // 2 - bb[1]), it, font=f, fill=WHITE)
        y += lh
    return y

def cta_pill(base, text, x, y):
    text = text.upper()
    d = ImageDraw.Draw(base); f = ar(31, 740)
    tw = d.textlength(text, font=f); pad = 48; h = 90; w = int(tw + pad * 2 + 48)
    base.alpha_composite(gradient_pill(w, h, CYAN, COBALT_D), (x, y))
    d = ImageDraw.Draw(base)
    bb = d.textbbox((0, 0), text, font=f)
    d.text((x + pad, y + (h - (bb[3] - bb[1])) // 2 - bb[1]), text, font=f, fill=WHITE)
    draw_arrow(d, x + pad + tw + 24, y + h // 2, 28, WHITE, 5, 12)
    return y + h

def badge(base, text, x, y, color=(214, 40, 40)):
    d = ImageDraw.Draw(base); f = ar(21, 760)
    t = text.upper(); tw = d.textlength(t, font=f); w = int(tw + 44); h = 50
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(ov).rounded_rectangle([x, y, x + w, y + h], radius=10, fill=color + (245,))
    base.alpha_composite(ov)
    d = ImageDraw.Draw(base)
    bb = d.textbbox((0, 0), t, font=f)
    d.text((x + 22, y + (h - (bb[3] - bb[1])) // 2 - bb[1]), t, font=f, fill=WHITE)
    return w

def build(cfg, outpath):
    base = photo_bg(cfg["img"], cfg.get("fy", 0.38))
    x = 70; maxw = W - 140
    size = cfg.get("h1_size", 78); lh = cfg.get("h1_lh", 84)
    badge_h = 66 if cfg.get("badge") else 0
    head_h = n_lines(base, cfg["headline"], maxw, size) * lh
    bull_h = len(cfg.get("bullets", [])) * 62
    cta_h = 90; g1, g2 = 30, 38
    total = badge_h + head_h + (g1 + bull_h if bull_h else 0) + g2 + cta_h
    y0 = SAFE_BOT - 24 - total                      # bloque termina dentro de zona segura
    y0 = max(SAFE_TOP + 150, y0)                     # no chocar el logo
    scrim(base, y0)
    base.alpha_composite(logo(white=True, target_w=190), (66, SAFE_TOP + 22))
    yy = y0
    if cfg.get("badge"):                             # badge ENCIMA del titular, alineado izq (nunca se corta)
        badge(base, cfg["badge"], x, int(yy), color=tuple(cfg.get("badge_color", [214, 40, 40])))
        yy += badge_h
    y = draw_headline(base, cfg["headline"], x, yy, maxw, size, lh)
    if cfg.get("bullets"):
        y = draw_bullets(base, cfg["bullets"], x, y + g1)
    cta_pill(base, cfg["cta"], x, y + g2)
    save(base, outpath)

CRE = [
 {"angulo":"Prueba social","img":"DSC00908.JPG","fy":0.34,"badge":"3,500+ FAMILIAS","badge_color":[26,86,200],
  "headline":"Ellos ya despiertan *frente al mar*. ¿Y tú?",
  "bullets":["Comunidad de 3,500+ familias","1.5 km de playa privada","Laguna navegable de agua salada"],
  "cta":"Agenda tu visita","out":"dr_01_prueba_social.png"},
 {"angulo":"FOMO / preventa","img":"DSC00879.JPG","fy":0.36,"badge":"PREVENTA","badge_color":[214,40,40],
  "headline":"En preventa cuesta menos. *Mañana no*.",
  "bullets":["Precio de preventa por tiempo limitado","Planes directos sin banco","Unidades frente al agua que vuelan"],
  "cta":"Aparta tu unidad","out":"dr_02_fomo.png"},
 {"angulo":"Retiro / vida","img":"DSC00490.JPG","fy":0.38,"badge":"VISA PENSIONADO","badge_color":[26,86,200],
  "headline":"Jubílate *frente al Pacífico*, no en una sala de espera",
  "bullets":["Visa Pensionado para mayores de 55","Clima de playa los 365 días","Spa, golf y club a pasos de casa"],
  "cta":"Quiero conocerlo","out":"dr_03_retiro.png"},
 {"angulo":"Sin banco","img":"DSC00859.JPG","fy":0.42,"badge":"SIN BANCO","badge_color":[20,120,90],
  "headline":"Tu casa frente al mar *sin pisar un banco*",
  "bullets":["Financiamiento directo con el desarrollador","Pagos en escrow ante notaría","Título a tu nombre desde el día uno"],
  "cta":"Pide tu plan de pago","out":"dr_04_sin_banco.png"},
 {"angulo":"Identidad comprador","img":"DSC06530.JPG","fy":0.40,"badge":"PARA TI","badge_color":[26,86,200],
  "headline":"Ya lo lograste. Ahora *vive frente al mar*.",
  "bullets":["Tu segundo hogar en la Riviera Pacífica","Sin banco, directo con el desarrollador","Respaldo de 23 años y 1,500+ entregas"],
  "cta":"Descúbrelo","out":"dr_05_identidad.png"},
 {"angulo":"Amenidades","img":"piscina.jpg","fy":0.48,"badge":"15+ AMENIDADES","badge_color":[26,86,200],
  "headline":"Spa, golf y club de playa *a tu puerta*",
  "bullets":["Club de playa y 1.5 km de arena privada","Laguna de agua salada navegable","Spa, golf, tenis y +15 amenidades"],
  "cta":"Agenda tu visita","out":"dr_06_amenidades.png"},
]

def main():
    outdir = os.path.join(SALIDAS, SESION); os.makedirs(outdir, exist_ok=True)
    res = []
    for i, c in enumerate(CRE, 1):
        try:
            build(c, os.path.join(outdir, c["out"]))
            print(f"[{i}] OK {c['angulo']:20s} {c['img']:16s} -> {c['out']}")
            res.append({"n":i,"angulo":c["angulo"],"img":c["img"],"headline":c["headline"],"archivo":os.path.join(SESION,c["out"])})
        except Exception as e:
            print(f"[{i}] ERROR {c['angulo']} ({c['img']}): {e}")
            res.append({"n":i,"angulo":c["angulo"],"error":str(e)})
    json.dump(res, open(os.path.join(outdir, "_resumen.json"), "w"), ensure_ascii=False, indent=2)
    print(f"\n=== {sum(1 for r in res if 'error' not in r)}/{len(CRE)} DR OK ===")

if __name__ == "__main__":
    main()
