#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""modern.py — Overlay EDITORIAL 2025 (look de lujo moderno) sobre una escena IA.
Serif elegante, tag tracked, bullets con líneas finas (sin check-bubbles), CTA plano
outline, mucho aire. Todo en ZONA SEGURA. Texto local = 0 errores."""
import os, sys, math
import numpy as np
BASE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, BASE)
sys.path.insert(0, os.path.join(BASE, "engine"))
from kit3 import (fr, fr_it, ar, logo, WHITE, OFFWHITE, MIST, ICE, NAVY_DEEP,
                  draw_tracked, tracked_width)
from designkit import open_fixed, cover_crop, enhance_premium, save
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

W, H, SAFE_TOP, SAFE_BOT = 1080, 1920, 420, 1500
CYAN = (96, 206, 248)
X = 84                       # margen izquierdo (mucho aire)
MAXW = W - X - 70

def photo_bg(path, fy=0.36):
    im = cover_crop(open_fixed(path), W, H, 0.5, fy)
    im = enhance_premium(im, color=1.04, contrast=1.06, bright=0.97, sharp=1.04)
    return im.convert("RGBA")

def soft_gradient(base, top_y):
    """Degradado navy de top_y hacia abajo, fuerte para legibilidad total (sin panel duro)."""
    yy = np.arange(H)
    a = np.clip((yy - top_y) / max(1, (SAFE_BOT - top_y)), 0, 1) ** 1.05 * 250
    col = np.zeros((H, W, 4), dtype="uint8")
    col[:, :, 0] = 5; col[:, :, 1] = 13; col[:, :, 2] = 34
    col[:, :, 3] = np.clip(a, 0, 250)[:, None].astype("uint8")
    base.alpha_composite(Image.fromarray(col, "RGBA"))

def logo_backing(base, x, y, w, h):
    """Halo oscuro suave tras el logo para que se lea sobre cielos claros."""
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([x-46, y-30, x+w+46, y+h+30], fill=(5, 14, 36, 150))
    base.alpha_composite(glow.filter(ImageFilter.GaussianBlur(48)))

def glass_card(base, box, radius=30):
    """Tarjeta de cristal esmerilado (frosted glass) tras el bloque de texto:
    foto borrosa + tinte navy + borde fino 1px. Look editorial premium, legible."""
    x0, y0, x1, y1 = [int(v) for v in box]
    x0 = max(0, x0); y0 = max(0, y0); x1 = min(W, x1); y1 = min(H, y1)
    region = base.convert("RGB").crop((x0, y0, x1, y1)).filter(ImageFilter.GaussianBlur(24))
    region = ImageEnhance.Brightness(region).enhance(0.60)
    dk = Image.new("RGBA", region.size, (8, 18, 44, 150))
    region = Image.alpha_composite(region.convert("RGBA"), dk)
    mask = Image.new("L", region.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, x1-x0-1, y1-y0-1], radius=radius, fill=255)
    base.paste(region, (x0, y0), mask)
    bd = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(bd).rounded_rectangle([x0, y0, x1, y1], radius=radius, outline=(255, 255, 255, 64), width=2)
    base.alpha_composite(bd)

def safe_frame(base):
    yy = np.arange(H); f = 110; a = np.zeros(H)
    a[yy <= SAFE_TOP - f] = 255
    m = (yy > SAFE_TOP - f) & (yy < SAFE_TOP); a[m] = np.clip(255*(SAFE_TOP - yy[m])/f, 0, 255)
    m = (yy > SAFE_BOT) & (yy < SAFE_BOT + f); a[m] = np.clip(255*(yy[m] - SAFE_BOT)/f, 0, 255)
    a[yy >= SAFE_BOT + f] = 255
    rgb = base.convert("RGB")
    blur = rgb.filter(ImageFilter.GaussianBlur(60))
    from PIL import ImageEnhance
    blur = ImageEnhance.Brightness(blur).enhance(0.55)
    mask = Image.fromarray(np.repeat(a[:, None], W, 1).astype("uint8"), "L")
    return Image.composite(blur, rgb, mask).convert("RGBA")

# --- titular con keyword en cian (toggle con *...*), serif, alineado izq ---
def _toks(text):
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
    return out

def _wrap(d, toks, f, maxw, sp):
    lines, cur, cw = [], [], 0
    for w, hl in toks:
        ww = d.textlength(w, font=f)
        add = ww if not cur else cw + sp + ww
        if cur and add > maxw:
            lines.append(cur); cur = [(w, hl)]; cw = ww
        else:
            cur.append((w, hl)); cw = add
    if cur: lines.append(cur)
    return lines

def headline_lines(base, text, f):
    d = ImageDraw.Draw(base)
    return _wrap(d, _toks(text), f, MAXW, d.textlength(" ", font=f))

def draw_headline(base, text, y, f, lh):
    d = ImageDraw.Draw(base)
    sp = d.textlength(" ", font=f)
    for line in _wrap(d, _toks(text), f, MAXW, sp):
        cx = X
        for w, hl in line:
            d.text((cx+1, y+2), w, font=f, fill=(3, 9, 26))
            d.text((cx, y), w, font=f, fill=CYAN if hl else WHITE)
            cx += d.textlength(w, font=f) + sp
        y += lh
    return y

def build(scene_path, cfg, out):
    base = photo_bg(scene_path, cfg.get("fy", 0.34))
    # ---- medir bloque para anclar en zona segura ----
    hf = fr(cfg.get("h1_size", 70), wght=cfg.get("h1_w", 460), opsz=144)
    lh = cfg.get("h1_lh", 80)
    nlines = len(headline_lines(base, cfg["headline"], hf))
    tag_h = 50 if cfg.get("tag") else 0
    head_h = nlines * lh
    bull = cfg.get("bullets", []); bull_h = len(bull) * 64
    cta_h = 88
    g_tag, g_bull, g_cta = 26, 34, 40
    total = tag_h + g_tag + head_h + (g_bull + bull_h if bull else 0) + g_cta + cta_h
    y0 = SAFE_BOT - 64 - total
    y0 = max(SAFE_TOP + 210, y0)
    # tarjeta de cristal tras el bloque de texto (look que ama Juan) — dentro de zona segura
    glass_card(base, (44, y0 - 44, W - 44, y0 + total + 30))
    # ---- logo oficial, arriba-izq, con halo para contraste ----
    lg = logo(white=True, target_w=210)
    logo_backing(base, X - 4, SAFE_TOP + 26, lg.width, lg.height)
    base.alpha_composite(lg, (X - 4, SAFE_TOP + 26))
    d = ImageDraw.Draw(base)
    y = y0
    # tag: raya fina + texto tracked en mayúsculas
    if cfg.get("tag"):
        tf = ar(21, 600)
        d.line([(X, y + 16), (X + 40, y + 16)], fill=CYAN + (255,), width=2)
        draw_tracked(d, cfg["tag"].upper(), tf, ICE, y + 4, 5, x=X + 56, center=False)
        y += tag_h + g_tag
    # headline serif
    y = draw_headline(base, cfg["headline"], y, hf, lh)
    # bullets: línea fina + texto, mucho aire (sin check-bubbles)
    if bull:
        y += g_bull
        bf = ar(30, 360)
        for it in bull:
            cy = y + 30
            d.line([(X, cy), (X + 26, cy)], fill=CYAN + (255,), width=3)
            bb = d.textbbox((0, 0), it, font=bf)
            d.text((X + 26 + 22, cy - (bb[3]-bb[1])//2 - bb[1]), it, font=bf, fill=OFFWHITE)
            y += 64
    # CTA plano outline (sin brillo)
    y += g_cta
    cta = cfg["cta"].replace("→", "").strip().upper()
    cf = ar(29, 640)
    tw = d.textlength(cta, font=cf); pad = 42; h = 84; w = int(tw + pad*2 + 46)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(ov).rounded_rectangle([X, int(y), X + w, int(y)+h], radius=h//2,
                                         outline=(255, 255, 255, 235), width=2, fill=(255, 255, 255, 26))
    base.alpha_composite(ov)
    d = ImageDraw.Draw(base)
    bb = d.textbbox((0, 0), cta, font=cf)
    d.text((X + pad, int(y) + (h-(bb[3]-bb[1]))//2 - bb[1]), cta, font=cf, fill=WHITE)
    ax = X + pad + tw + 20; ay = int(y) + h//2
    d.line([(ax, ay), (ax+26, ay)], fill=WHITE, width=3)
    d.line([(ax+26-11, ay-11), (ax+26, ay)], fill=WHITE, width=3)
    d.line([(ax+26-11, ay+11), (ax+26, ay)], fill=WHITE, width=3)
    # relleno ambiente bordes
    base = safe_frame(base)
    save(base, out)
