#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""formatos_nuevos.py — Renderiza FORMATOS VISUALES distintos (no solo foto+texto):
solo-texto, quote/testimonio, collage, comparativa y animación (MP4 9:16).
Reusa la marca del motor (fuentes, logo, colores, CTA). Sin URL (objetivo formulario)."""
import os, sys, json, glob, math, subprocess, shutil
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "engine"))
from kit3 import *                      # W,H,fr,fr_it,ar,colores,logo,paste_logo,kicker,cta_*,bg,cinematic_gradient,...
from designkit import vgrad, kicker_chip
import gen4

FFMPEG = "/Users/juanescorcha/bin/ffmpeg"
FOTOS  = os.path.join(BASE, "..", "fotos_proyecto", "a")
SALIDAS= os.path.join(BASE, "salidas")
SESION = "sesion_02"

# --- índice de fotos + src ---
_idx = {}
for p in glob.glob(os.path.join(FOTOS, "*")):
    b = os.path.basename(p)
    if not b.startswith("._") and p.lower().endswith((".jpg", ".jpeg", ".png")):
        _idx[b] = p
def src(n):
    if n in _idx: return _idx[n]
    raise FileNotFoundError(n)
gen4.src = src

# ===================== helpers compartidos =====================
def brand_bg():
    base = Image.new("RGBA", (W, H), NAVY_DEEP + (255,))
    vgrad(base, 0, 0, W, H, (20, 52, 122), (5, 14, 38), 255, 255, power=1.15)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([W//2-560, 240, W//2+560, 1180], fill=(40, 86, 190, 70))
    base.alpha_composite(glow.filter(ImageFilter.GaussianBlur(160)))
    return base

def compose_centered(base, draw_fn, shift=30, start=240):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_fn(layer, start)
    bb = layer.getbbox()
    if not bb: return
    block_h = bb[3] - bb[1]
    target_t = int(SAFE_CY - block_h/2 + shift)
    target_t = max(SAFE_TOP+24, min(target_t, SAFE_BOT-block_h-16))
    base.alpha_composite(layer, (0, target_t - bb[1]))

def _draw_block(layer, y0, cfg):
    """Bloque de marca estándar (logo, kicker, h1, sub, divisor, trust, cta). Sin URL."""
    yy = paste_logo(layer, int(y0), cfg.get("logo_w", 420), white=True) + 26
    d = ImageDraw.Draw(layer)
    if cfg.get("kicker"):
        kicker(d, cfg["kicker"], yy); yy += 58
    h1f = fr(cfg.get("h1_size", 72), wght=cfg.get("h1_w", 590))
    for ln in wrap_text(d, cfg["h1"], h1f, cfg.get("cw", 900)):
        draw_center(d, ln, h1f, WHITE, yy, shadow=((2,8,24,150),(2,2))); yy += cfg.get("h1_lh", 82)
    yy += 8
    if cfg.get("sub"):
        for ln in cfg["sub"]:
            draw_center(d, ln, ar(cfg.get("sub_size", 30), 360), OFFWHITE, yy); yy += 42
        yy += 8
    if cfg.get("divider", True):
        d.line([((W-90)/2, yy), ((W+90)/2, yy)], fill=(255,255,255,95), width=2); yy += 34
    if cfg.get("trust"):
        draw_tracked(d, cfg["trust"], ar(21, 560), OFFWHITE, yy, 2); yy += 54
    st = cfg.get("cta_style", "white")
    fn = {"white": cta_white, "outline": cta_outline, "solid": cta_solid}.get(st, cta_white)
    fn(layer, cfg.get("cta", "Más información"), yy)
    return yy

def _star_pts(cx, cy, r):
    pts = []
    for i in range(10):
        ang = -math.pi/2 + i*math.pi/5
        rad = r if i % 2 == 0 else r*0.42
        pts.append((cx + rad*math.cos(ang), cy + rad*math.sin(ang)))
    return pts
def draw_stars(layer, cy, n=5, r=15, gap=14, color=ICE):
    d = ImageDraw.Draw(layer)
    total = n*(2*r) + (n-1)*gap
    x = (W - total)/2 + r
    for _ in range(n):
        d.polygon(_star_pts(x, cy, r), fill=color); x += 2*r + gap

# ===================== FORMATOS =====================
def f_foto_persona(cfg, out):  # usa el motor (foto + texto)
    c = dict(cfg); c["price"] = False; c["url"] = False; c["logo"] = True; c["out"] = out
    c["cta"] = cfg["cta"].replace("→", "").strip()
    gen4.build(c)

def f_foto_lugar(cfg, out):
    f_foto_persona(cfg, out)

def f_solo_texto(cfg, outpath):
    base = brand_bg()
    compose_centered(base, lambda L, y: _draw_block(L, y, cfg), shift=cfg.get("block_shift", 20))
    save(base, outpath)

def f_quote(cfg, outpath):
    base = bg(src(cfg["img"]), fx=cfg.get("fx", 0.5), fy=cfg.get("fy", 0.4))
    cinematic_gradient(base, anchor=620, text_top=720)
    def block(layer, y0):
        yy = paste_logo(layer, int(y0), 360, white=True) + 30
        d = ImageDraw.Draw(layer)
        # comilla grande
        qf = fr(150, wght=600)
        draw_center(d, "“", qf, ICE, yy); yy += 120
        # cita en cursiva
        qif = fr_it(cfg.get("q_size", 52), wght=500)
        for ln in wrap_text(d, cfg["quote"], qif, 860):
            draw_center(d, ln, qif, WHITE, yy, shadow=((2,8,24,150),(2,2))); yy += cfg.get("q_lh", 64)
        yy += 18
        draw_stars(layer, yy + 8); yy += 44
        draw_center(d, cfg["author"], ar(26, 500), ICE, yy); yy += 50
        cta_white(layer, cfg["cta"].replace("→", "").strip(), yy)
    compose_centered(base, block, shift=cfg.get("block_shift", 40))
    save(base, outpath)

def _paste_inset(base, name, x, y, s, fy=0.45):
    im = cover_crop(open_fixed(src(name)), s, s, 0.5, fy)
    border = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(border).rounded_rectangle([x-5, y-5, x+s+5, y+s+5], radius=34, fill=(255,255,255,240))
    base.alpha_composite(border)
    mask = Image.new("L", (s, s), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, s-1, s-1], radius=28, fill=255)
    base.paste(im.convert("RGB"), (x, y), mask)

def f_collage(cfg, outpath):
    base = bg(src(cfg["img"]), fx=cfg.get("fx", 0.5), fy=cfg.get("fy", 0.42))
    cinematic_gradient(base, anchor=900, text_top=980)
    ins = cfg.get("insets", [])
    s = 300; y = 452
    if len(ins) >= 1: _paste_inset(base, ins[0], 78, y, s)
    if len(ins) >= 2: _paste_inset(base, ins[1], W-78-s, y, s)
    compose_centered(base, lambda L, yy: _draw_block(L, yy, cfg), shift=cfg.get("block_shift", 150))
    save(base, outpath)

def f_comparativa(cfg, outpath):
    base = Image.new("RGBA", (W, H), NAVY_DEEP + (255,))
    top = cover_crop(open_fixed(src(cfg["img_top"])), W, 960, 0.5, cfg.get("fy_top", 0.45))
    top = ImageEnhance.Color(top).enhance(0.38)
    top = ImageEnhance.Brightness(top).enhance(0.88)
    bot = cover_crop(open_fixed(src(cfg["img_bot"])), W, 960, 0.5, cfg.get("fy_bot", 0.5))
    base.paste(top.convert("RGB"), (0, 0)); base.paste(bot.convert("RGB"), (0, 960))
    # scrims para legibilidad
    vgrad(base, 0, 420, W, 780, (5,14,38), (5,14,38), 210, 0)
    vgrad(base, 0, 980, W, 1500, (6,16,44), (5,14,38), 40, 238)
    # divisor + chip central con chevron hacia ABAJO
    d = ImageDraw.Draw(base)
    d.line([(60, 960), (W-60, 960)], fill=(255,255,255,130), width=2)
    chip = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(chip).ellipse([W//2-42, 918, W//2+42, 1002], fill=COBALT+(255,), outline=(255,255,255,240), width=3)
    base.alpha_composite(chip)
    dd = ImageDraw.Draw(base)
    dd.line([(W//2-16, 952), (W//2, 972)], fill=WHITE, width=6)
    dd.line([(W//2+16, 952), (W//2, 972)], fill=WHITE, width=6)
    # logo + labels (con chip oscuro para contraste) + h1 + cta
    paste_logo(base, 446, 320, white=True)
    kicker_chip(base, cfg.get("label_top", "HOY"), ar(22, 680), 596, fill=WHITE, tracking=4, chip_rgba=(8,20,52,210))
    kicker_chip(base, cfg.get("label_bot", "AQUÍ"), ar(22, 680), 1050, fill=WHITE, tracking=4, chip_rgba=(8,20,52,210))
    dd = ImageDraw.Draw(base)
    h1f = fr(cfg.get("h1_size", 58), wght=620)
    yy = 1140
    for ln in wrap_text(dd, cfg["h1"], h1f, 900):
        draw_center(dd, ln, h1f, WHITE, yy, shadow=((2,8,24,170),(2,2))); yy += 66
    cta_white(base, cfg["cta"].replace("→", "").strip(), yy + 10)
    save(base, outpath)

def f_animacion(cfg, outpath_mp4):
    poster = outpath_mp4.replace(".mp4", "_poster.png")
    # overlay transparente (veil + texto), una sola vez
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cinematic_gradient(ov, anchor=820, text_top=900)
    compose_centered(ov, lambda L, y: _draw_block(L, y, cfg), shift=cfg.get("block_shift", 60))
    # foto base pre-escalada (zoom margin)
    BW, BH = int(W*1.12), int(H*1.12)
    big = cover_crop(open_fixed(src(cfg["img"])), BW, BH, 0.5, cfg.get("fy", 0.42)).convert("RGBA")
    frames_dir = os.path.join(BASE, "work", "frames_anim"); shutil.rmtree(frames_dir, ignore_errors=True); os.makedirs(frames_dir)
    fps = cfg.get("fps", 24); dur = cfg.get("dur", 4.0); N = int(fps*dur)
    for i in range(N):
        t = i/(N-1)
        cw = int(W*(1.12 - 0.12*t)); ch = int(H*(1.12 - 0.12*t))
        left = (BW - cw)//2; top = int((BH - ch)*0.40)
        frame = big.crop((left, top, left+cw, top+ch)).resize((W, H), Image.LANCZOS)
        frame.alpha_composite(ov)
        if i == 0: frame.convert("RGB").save(poster, quality=95)
        frame.convert("RGB").save(os.path.join(frames_dir, f"{i:04d}.jpg"), quality=90)
    cmd = [FFMPEG, "-y", "-framerate", str(fps), "-i", os.path.join(frames_dir, "%04d.jpg"),
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-movflags", "+faststart", outpath_mp4]
    r = subprocess.run(cmd, capture_output=True, text=True)
    shutil.rmtree(frames_dir, ignore_errors=True)
    if r.returncode != 0:
        raise RuntimeError("ffmpeg: " + r.stderr[-400:])
    print("saved", outpath_mp4, "(", N, "frames )")

# ===================== los 7 samples =====================
CRE = [
 {"fmt":"foto_persona","fn":f_foto_persona,"ext":"png","angulo":"Testimonios",
  "img":"DSC00908.JPG","fy":0.38,"kicker":"FAMILIAS REALES","h1":"Aquí los domingos saben distinto",
  "sub":["Familias que ya viven frente al","Pacífico de Panamá."],"trust":"3,500+ FAMILIAS · 23 AÑOS",
  "cta":"Agenda tu visita","cta_style":"white"},

 {"fmt":"foto_lugar","fn":f_foto_lugar,"ext":"png","angulo":"Aspiración",
  "img":"hero-lagoon.jpg","fy":0.30,"kicker":"TU NUEVA VISTA","h1":"Despierta frente a esta laguna",
  "sub":["La de agua salada más grande","de la región. Navegable."],"trust":"LAGUNA NAVEGABLE · 90 HECTÁREAS",
  "cta":"Conoce más","cta_style":"white"},

 {"fmt":"solo_texto","fn":f_solo_texto,"ext":"png","angulo":"Autoridad",
  "kicker":"POR QUÉ PLAYA BLANCA","h1":"Lo que prometemos, ya está construido",
  "sub":["23 años · 3,500+ familias","1,500+ hogares entregados."],"trust":"CERO PROMESAS VACÍAS",
  "cta":"Conoce el proyecto","cta_style":"white","h1_size":70,"h1_lh":80},

 {"fmt":"quote","fn":f_quote,"ext":"png","angulo":"Testimonios","img":"DSC00275.JPG","fy":0.40,
  "quote":"Compramos sin banco y hoy desayunamos frente al Pacífico.",
  "author":"— Carlos y Marta · Bogotá","cta":"Quiero lo mismo"},

 {"fmt":"collage","fn":f_collage,"ext":"png","angulo":"Amenidades","img":"playa.jpg","fy":0.45,
  "insets":["spa.jpg","piscina.jpg"],"kicker":"AMENIDADES","h1":"Todo a un paso de tu puerta",
  "sub":["Spa, golf, club de playa","y 1.5 km de playa privada."],"trust":"15+ AMENIDADES",
  "cta":"Conoce más","cta_style":"white","block_shift":160},

 {"fmt":"comparativa","fn":f_comparativa,"ext":"png","angulo":"Aspiración",
  "img_top":"DSC00771.JPG","img_bot":"playa.jpg","fy_top":0.4,"fy_bot":0.5,
  "label_top":"TU LUNES HOY","label_bot":"TU LUNES AQUÍ","h1":"Mismo lunes. Otro lugar.",
  "cta":"Agenda tu visita"},

 {"fmt":"animacion","fn":f_animacion,"ext":"mp4","angulo":"Aspiración","img":"manana.jpg","fy":0.42,
  "kicker":"VIVE AQUÍ","h1":"Tu mañana, frente al Pacífico","sub":["A 1.5 h de Ciudad de Panamá."],
  "trust":"1.5 KM DE PLAYA PRIVADA","cta":"Agenda tu visita","cta_style":"white","fps":24,"dur":4.0},
]

def main():
    sel = set(sys.argv[1:])
    res = []
    for i, c in enumerate(CRE, 1):
        if sel and c["fmt"] not in sel: continue
        outdir = os.path.join(SALIDAS, SESION, c["fmt"]); os.makedirs(outdir, exist_ok=True)
        fname = f"{c['fmt']}.{c['ext']}"
        if c["fmt"] in ("foto_persona", "foto_lugar"):
            out_rel = os.path.join(SESION, c["fmt"], fname)   # gen4 guarda en salidas/+out
            outpath = os.path.join(SALIDAS, out_rel)
        else:
            outpath = os.path.join(outdir, fname); out_rel = os.path.relpath(outpath, SALIDAS)
        try:
            if c["fmt"] in ("foto_persona", "foto_lugar"):
                c["fn"](c, out_rel)
            else:
                c["fn"](c, outpath)
            print(f"[{i}] OK  {c['fmt']:12s} -> {fname}")
            res.append({"n":i,"formato":c["fmt"],"angulo":c["angulo"],
                        "archivo":out_rel if c['fmt'].startswith('foto') else os.path.join(SESION,c['fmt'],fname),
                        "img":c.get("img") or c.get("img_top")})
        except Exception as e:
            print(f"[{i}] ERROR {c['fmt']}: {e}")
            res.append({"n":i,"formato":c["fmt"],"error":str(e)})
    json.dump(res, open(os.path.join(SALIDAS, SESION, "_resumen.json"), "w"), ensure_ascii=False, indent=2)
    ok = sum(1 for r in res if "error" not in r)
    print(f"\n=== {ok}/{len(CRE)} formatos OK ===")
    errs = [r for r in res if "error" in r]
    if errs: print("ERRORES:", [(e['formato'], e['error']) for e in errs])

if __name__ == "__main__":
    main()
