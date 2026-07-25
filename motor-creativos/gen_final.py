#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_final.py — Copy de Opus + Gemini compone el anuncio.
Flujo barato: BORRADOR con modelo barato (draft) -> si gusta, FINAL con Nano Banana 2.
Uso:  python3 gen_final.py draft aspiracion
      python3 gen_final.py final aspiracion retiro
Sujeto+texto en ZONA SEGURA central; bordes = relleno; logo OFICIAL en post; 1 badge."""
import sys, os, time
import numpy as np
BASE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, BASE)
sys.path.insert(0, os.path.join(BASE, "engine"))
import nano_banana as nb
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance
from kit3 import ar
from designkit import gradient_pill, draw_arrow

W, H, SAFE_TOP, SAFE_BOT = 1080, 1920, 420, 1500
LOGO = os.path.join(BASE, "assets", "logo_white_trim.png")
OUT = os.path.join(BASE, "salidas", "nano_final"); os.makedirs(OUT, exist_ok=True)

# Modelos: draft = barato (Nano Banana 1 / 2.5 Flash Image), final = Nano Banana 2 (3 Pro Image)
MODELS = {
    "draft": ["gemini-2.5-flash-image", "gemini-2.5-flash-image-preview", "gemini-2.0-flash-preview-image-generation"],
    "final": ["gemini-3-pro-image-preview"],
}
EP = "https://generativelanguage.googleapis.com/v1beta/models/{}:generateContent"

FRAME = """
FRAME & SAFE ZONE (very important):
- Compose so the PEOPLE and ALL the text (badge, headline, bullets, CTA button) sit INSIDE the central
  vertical band. Put the badge, headline and the bullets between 28% and 66% of the image height, COMPACT.
  Leave the area from about 67% to 77% of the height as CLEAN dark cobalt gradient EMPTY space (no text) —
  a CTA button will be composited there separately.
- It must be ONE single CONTINUOUS full-bleed photograph filling the whole 9:16 frame edge-to-edge. The
  very TOP simply shows the natural sky of that same photo and the very BOTTOM the natural ground/water/
  terrace of that same photo. Do NOT create separate flat filler bands, stripes, solid color blocks, a
  card, frame, border or inset at the top or bottom — no pasted-looking margins, just one organic photo.
- Keep the people and ALL text comfortably inside the central safe band so a center-crop loses only empty
  sky/ground, never a person or a word. Show the couple only ONCE.
- The text sits over a SOFT dark cobalt gradient that blends smoothly upward into the photo (not a hard
  rectangular panel with a visible edge).
- Use EXACTLY ONE badge in the whole image, placed directly ABOVE the headline (required, must be visible).
  Do NOT place any badge, seal, emblem or pill near the top edge or anywhere else.
- Do NOT draw any logo, brand name or wordmark anywhere.
- RESERVE the TOP-LEFT corner of the safe band (roughly the left third, from 22% to 38% of the height) as
  clean open sky or distant out-of-focus background — NO face, NO head, NO hand, NO object there — because a
  small official logo is composited in that corner afterwards. Position the people centered or toward the
  right so the top-left corner stays clear; keep all heads BELOW 40% of the height.
- Do NOT draw any CTA button, arrow or call-to-action — leave that lower area empty (it is added later).
- Headline and bullets over a clean dark cobalt gradient, razor-sharp and legible. Perfect Spanish spelling
  with accents, no gibberish, no duplicate text."""

ITEMS = {
 "aspiracion": """Photorealistic cinematic top-performing direct-response real-estate ad, vertical 9:16,
premium magazine quality. SCENE: a stylish aspirational Latino couple in their early 40s relaxing on a
rooftop infinity-pool terrace at golden-hour sunset, toasting with sparkling drinks, overlooking a huge
turquoise saltwater lagoon, modern white residential towers and palms of a luxury beachfront resort on the
Pacific coast of Panama. The couple is centered and slightly toward the RIGHT, with their heads in the
upper-middle area kept BELOW 40% of the height; the UPPER-LEFT corner stays clear open golden sky (no head,
no object) for a logo. Realistic faces and hands. BRAND COLORS: deep cobalt blue & navy with bright CYAN.
SPANISH COPY (exact, with accents):
- badge: "PREVENTA"
- headline UPPERCASE, words "FRENTE AL MAR" in cyan rest white: "VIVIR FRENTE AL MAR YA NO ES UN SUEÑO LEJANO"
- bullets with cyan check icons: "Planes de pago directos, sin banco" / "Título de propiedad a tu nombre" / "Cupos de preventa limitados"
- CTA button cyan-to-blue, white bold uppercase + arrow: "QUIERO MI PLAN" """ + FRAME,

 "retiro": """Photorealistic cinematic top-performing direct-response real-estate ad, vertical 9:16, warm
joyful feel. SCENE: a happy vital retired Latino couple in their mid-60s laughing while walking barefoot on
a private white-sand beach at warm sunset, a luxury beachfront resort with turquoise lagoon and modern white
towers softly behind. Realistic faces. BRAND COLORS: deep cobalt blue & navy with bright CYAN, warm sunset.
SPANISH COPY (exact, with accents):
- badge: "VISA PENSIONADO +55"
- headline UPPERCASE, word "PLAYA" in cyan rest white: "TUS MEJORES AÑOS MERECEN PLAYA"
- bullets with cyan check icons: "Clima de playa los 365 días" / "Spa, golf y club a pasos de casa" / "1.5 km de playa privada"
- CTA button cyan-to-blue, white bold uppercase + arrow: "AGENDA TU VISITA" """ + FRAME,

 "amenidades": """Photorealistic cinematic top-performing direct-response real-estate ad, vertical 9:16,
bright sunny joyful feel. SCENE: a happy young Latino family with two kids enjoying a luxury beach club and
pool, palm trees, turquoise saltwater lagoon and modern white residential towers of a beachfront resort on
the Pacific coast of Panama. Realistic faces. BRAND COLORS: deep cobalt blue & navy with bright CYAN.
SPANISH COPY (exact, with accents):
- badge: "15+ AMENIDADES"
- headline UPPERCASE, words "A UN PASO DE CASA" in cyan rest white: "TU CLUB DE PLAYA A UN PASO DE CASA"
- bullets with cyan check icons: "Club de playa y 1.5 km de arena" / "Spa, golf, tenis y gimnasio" / "Laguna de agua salada navegable"
- CTA button cyan-to-blue, white bold uppercase + arrow: "CONOCE LAS AMENIDADES" """ + FRAME,
}

def _safe_frame(im):
    """Reemplaza el TOP (0..SAFE_TOP) y BOTTOM (SAFE_BOT..H) por relleno ambiente
    (la misma foto borrosa+oscura) con feather suave. Lo unico recortable en un
    center-crop es ese relleno generico; el contenido vive en la zona segura."""
    rgb = im.convert("RGB")
    blur = ImageEnhance.Brightness(rgb.filter(ImageFilter.GaussianBlur(60))).enhance(0.55)
    yy = np.arange(H); f = 110
    a = np.zeros(H)                                  # 0 = foto nitida (zona segura intacta)
    a[yy <= SAFE_TOP - f] = 255
    m = (yy > SAFE_TOP - f) & (yy < SAFE_TOP); a[m] = np.clip(255*(SAFE_TOP - yy[m])/f, 0, 255)
    m = (yy > SAFE_BOT) & (yy < SAFE_BOT + f); a[m] = np.clip(255*(yy[m] - SAFE_BOT)/f, 0, 255)
    a[yy >= SAFE_BOT + f] = 255
    mask = Image.fromarray(np.repeat(a[:, None], W, 1).astype("uint8"), "L")
    return Image.composite(blur, rgb, mask).convert("RGBA")

def _draw_cta(im, text, y=1330):
    """Compone el botón CTA (cian->cobalto, texto blanco + flecha) centrado,
    dentro de la zona segura. Lo dibujo yo para que NUNCA falte ni tenga typos."""
    text = text.upper()
    d = ImageDraw.Draw(im); f = ar(34, 730)
    tw = d.textlength(text, font=f); pad = 54; h = 98; w = int(tw + pad*2 + 50)
    x = (W - w) // 2
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([x, y+7, x+w, y+h+7], radius=h//2, fill=(4, 12, 34, 150))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(13)))
    im.alpha_composite(gradient_pill(w, h, (56, 208, 255), (20, 60, 162)), (x, y))
    d = ImageDraw.Draw(im)
    bb = d.textbbox((0, 0), text, font=f)
    d.text((x+pad, y+(h-(bb[3]-bb[1]))//2-bb[1]), text, font=f, fill=(255, 255, 255))
    draw_arrow(d, x+pad+tw+24, y+h//2, 28, (255, 255, 255), 5, 12)

def finalize(path, cta=None):
    im = Image.open(path).convert("RGBA").resize((W, H), Image.LANCZOS)
    im = _safe_frame(im)
    # logo oficial: esquina superior izquierda, dentro de zona segura
    lg = Image.open(LOGO).convert("RGBA"); tw = 232; r = tw/lg.width
    lg = lg.resize((tw, int(lg.height*r)), Image.LANCZOS)
    x = 60; y = SAFE_TOP + 38
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([x-50, y-34, x+lg.width+50, y+lg.height+34], fill=(6, 16, 40, 115))
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(46)))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sh.alpha_composite(lg, (x, y+3))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7))); im.alpha_composite(lg, (x, y))
    if cta:
        _draw_cta(im, cta)
    im.convert("RGB").save(path, quality=95)

def add_logo(path):      # compat
    finalize(path, None)

def gen(name, tier):
    out = os.path.join(OUT, f"{name}_{tier}.png")
    last = None
    for model in MODELS[tier]:
        nb.ENDPOINT = EP.format(model)
        t0 = time.time()
        g = nb.generar_fondo(ITEMS[name], ref_paths=[], out_path=out, aspect="9:16", timeout=240)
        if g.get("ok"):
            add_logo(out)
            print(f"OK {name} [{tier}:{model}] {time.time()-t0:.0f}s + logo -> {os.path.basename(out)}")
            return
        last = (model, g.get("error"), str(g.get("body"))[:150])
        print(f"  fallo {model}: {g.get('error')}")
    print(f"ERROR {name} [{tier}]: {last}")

if __name__ == "__main__":
    args = sys.argv[1:]
    tier = args[0] if args and args[0] in MODELS else "draft"
    names = [a for a in args if a in ITEMS] or list(ITEMS)
    for n in names: gen(n, tier)
