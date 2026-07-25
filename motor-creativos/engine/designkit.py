# ⚙️ CONFIGURA ESTAS RUTAS antes de usar:
# FONTS_DIR = carpeta con las fuentes (.ttf)
# BASE_DIR = carpeta con logo y assets
# Reemplaza /Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/Playa Blanca/motor_creativos/fonts/ y BASE_DIR/ por tus rutas reales.

#!/usr/bin/env python3
"""
Motor de diseño compartido para los 6 anuncios premium.
Playa Blanca Residences - Meta Ads 1080x1920.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
import math

W, H = 1080, 1920
FD = "/Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/Playa Blanca/motor_creativos/fonts/"
PD = "/usr/share/fonts/truetype/google-fonts/"

# ---------------- Paleta ----------------
COBALT    = (24, 78, 232)
COBALT_D  = (12, 50, 186)
COBALT_L  = (94, 140, 255)
NAVY      = (9, 23, 58)
NAVY_DEEP = (5, 14, 38)
WHITE     = (255, 255, 255)
OFFWHITE  = (238, 242, 250)
MIST      = (200, 213, 236)
ICE       = (198, 218, 252)

# -------------- Carga de fuentes con eje variable --------------
_cache = {}
def font(path, size, wght=None):
    key = (path, size, wght)
    if key in _cache:
        return _cache[key]
    f = ImageFont.truetype(path, size)
    if wght is not None:
        try:
            f.set_variation_by_axes([wght])
        except Exception:
            pass
    _cache[key] = f
    return f

# Atajos
def playfair(size, wght=700):  return font(FD+"PlayfairDisplay.ttf", size, wght)
def playfair_it(size, wght=500): return font(FD+"PlayfairDisplay-Italic.ttf", size, wght)
def cormorant(size, wght=500): return font(FD+"CormorantGaramond.ttf", size, wght)
def cormorant_it(size, wght=500): return font(FD+"CormorantGaramond-Italic.ttf", size, wght)
def mont(size, wght=500):      return font(FD+"Montserrat.ttf", size, wght)
def jost(size, wght=400):      return font(FD+"Jost.ttf", size, wght)
def poppins(size, style="Regular"): return font(PD+f"Poppins-{style}.ttf", size)

# ----------------- Helpers de dibujo -----------------
def measure(draw, text, font):
    bb = draw.textbbox((0,0), text, font=font)
    return bb[2]-bb[0], bb[3]-bb[1], bb

def tracked_width(draw, text, font, tracking):
    w = 0
    for ch in text:
        bb = draw.textbbox((0,0), ch, font=font)
        w += (bb[2]-bb[0])
    return w + tracking*(len(text)-1)

def draw_tracked(draw, text, font, fill, y, tracking, x=None, center=True, shadow=None):
    total = tracked_width(draw, text, font, tracking)
    if center:
        x = (W - total)/2
    elif x is None:
        x = 0
    cx = x
    for ch in text:
        bb = draw.textbbox((0,0), ch, font=font)
        cw = bb[2]-bb[0]
        if shadow:
            sc, (ox, oy) = shadow
            draw.text((cx+ox, y+oy), ch, font=font, fill=sc)
        draw.text((cx, y), ch, font=font, fill=fill)
        cx += cw + tracking
    return total, x

def draw_center(draw, text, font, fill, y, shadow=None):
    w, h, bb = measure(draw, text, font)
    x = (W - w)/2 - bb[0]
    if shadow:
        sc,(ox,oy)=shadow
        draw.text((x+ox, y+oy), text, font=font, fill=sc)
    draw.text((x, y), text, font=font, fill=fill)
    return w

def wrap_text(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for wd in words:
        t = (cur+" "+wd).strip()
        if draw.textbbox((0,0), t, font=font)[2] <= max_w:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = wd
    if cur: lines.append(cur)
    return lines

def cover_crop(img, target_w, target_h, focus_x=0.5, focus_y=0.5):
    """Recorta y escala como CSS background-size:cover con punto focal."""
    sw, sh = img.size
    scale = max(target_w/sw, target_h/sh)
    nw, nh = int(sw*scale+0.5), int(sh*scale+0.5)
    img2 = img.resize((nw, nh), Image.LANCZOS)
    max_x = nw - target_w
    max_y = nh - target_h
    left = int(max_x * focus_x)
    top  = int(max_y * focus_y)
    return img2.crop((left, top, left+target_w, top+target_h))

def enhance_premium(img, color=1.07, contrast=1.05, bright=1.0, sharp=1.06):
    img = ImageEnhance.Color(img).enhance(color)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    img = ImageEnhance.Brightness(img).enhance(bright)
    img = ImageEnhance.Sharpness(img).enhance(sharp)
    return img

def vgrad(draw_img, x0, y0, x1, y1, top_color, bot_color, top_a, bot_a, power=1.0):
    """Degradado vertical con alfa, sobre una capa RGBA."""
    h = y1 - y0
    ov = Image.new("RGBA", (x1-x0, h), (0,0,0,0))
    px = ov.load()
    for yy in range(h):
        t = (yy/h)**power
        r = int(top_color[0]+(bot_color[0]-top_color[0])*t)
        g = int(top_color[1]+(bot_color[1]-top_color[1])*t)
        b = int(top_color[2]+(bot_color[2]-top_color[2])*t)
        a = int(top_a+(bot_a-top_a)*t)
        for xx in range(x1-x0):
            px[xx,yy] = (r,g,b,a)
    draw_img.alpha_composite(ov, (x0,y0))

def soft_shadow_box(size_wh, box, radius, color, blur):
    layer = Image.new("RGBA", size_wh, (0,0,0,0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle(box, radius=radius, fill=color)
    return layer.filter(ImageFilter.GaussianBlur(blur))

def gradient_pill(w, h, c1, c2, radius=None):
    if radius is None: radius = h//2
    pill = Image.new("RGBA",(w,h),(0,0,0,0))
    pd = ImageDraw.Draw(pill)
    for i in range(w):
        t=i/w
        r=int(c1[0]+(c2[0]-c1[0])*t); g=int(c1[1]+(c2[1]-c1[1])*t); b=int(c1[2]+(c2[2]-c1[2])*t)
        pd.line([(i,0),(i,h)], fill=(r,g,b,255))
    mask=Image.new("L",(w,h),0)
    ImageDraw.Draw(mask).rounded_rectangle([0,0,w-1,h-1], radius=radius, fill=255)
    out=Image.new("RGBA",(w,h),(0,0,0,0))
    out.paste(pill,(0,0),mask)
    return out

def draw_arrow(draw, x, y, length, color, width=4, head=13):
    draw.line([(x,y),(x+length,y)], fill=color, width=width)
    draw.line([(x+length-head, y-head+1),(x+length,y)], fill=color, width=width)
    draw.line([(x+length-head, y+head-1),(x+length,y)], fill=color, width=width)

def grain(img, amount=6):
    import random
    n = Image.new("L", img.size)
    px = n.load()
    W2,H2 = img.size
    for y in range(0,H2,2):
        for x in range(0,W2,2):
            v = 128 + random.randint(-amount,amount)
            px[x,y]=v
            if x+1<W2: px[x+1,y]=v
    n = n.resize(img.size)
    return n

# Texto en mayúsculas SIN acentos problemáticos -> mantenemos acentos (las fonts los soportan)
def save(img, path):
    img.convert("RGB").save(path, quality=96, subsampling=0)
    print("saved", path)

def kicker_chip(base, text, font, y, fill=WHITE, tracking=4, pad_x=26, pad_y=12,
                chip_rgba=(8,20,52,120), border=None):
    """Etiqueta centrada con respaldo de chip translucido para legibilidad garantizada."""
    d = ImageDraw.Draw(base)
    tw = tracked_width(d, text, font, tracking)
    bb = d.textbbox((0,0), text, font=font)
    th = bb[3]-bb[1]
    chip_w = tw + 2*pad_x
    chip_h = th + 2*pad_y
    cx = (W - chip_w)/2
    chip = Image.new("RGBA",(W,H),(0,0,0,0))
    cd = ImageDraw.Draw(chip)
    cd.rounded_rectangle([cx, y-pad_y, cx+chip_w, y-pad_y+chip_h], radius=chip_h//2,
                         fill=chip_rgba, outline=border, width=2 if border else 0)
    base2 = Image.alpha_composite(base, chip)
    base.paste(base2, (0,0))
    draw_tracked(ImageDraw.Draw(base), text, font, fill, y, tracking, center=True)
    return chip_h

# ---- Logo de marca ----
def load_logo(white=False, size=None):
    p = "BASE_DIR/logo_white.png" if white else "BASE_DIR/logo_navy.png"
    lg = Image.open(p).convert("RGBA")
    if size:
        lg = lg.resize((size,size), Image.LANCZOS)
    return lg

def paste_center_logo(base, y, size, white=True):
    lg = load_logo(white=white, size=size)
    x = (W - size)//2
    base.alpha_composite(lg, (x, y))
    return y + size

def brand_lockup(base, y, logo_size=92, white=True, tagline=None, name="PLAYA BLANCA",
                 sub="BEACH & LAGOON RESIDENCES", name_color=None, sub_color=None):
    """Bloque de marca: logo + nombre + subtitulo, estilo identidad real."""
    d = ImageDraw.Draw(base)
    if name_color is None: name_color = WHITE if white else NAVY
    if sub_color is None: sub_color = MIST if white else (60,80,130)
    cy = y
    sh = ((4,12,34,110),(1,1))
    if tagline:
        tf = cormorant_it(40, 500)
        draw_center(d, tagline, tf, name_color, cy, shadow=sh); cy += 46
    cy = paste_center_logo(base, cy, logo_size, white=white) + 6
    d = ImageDraw.Draw(base)
    nf = mont(40, 700)
    draw_tracked(d, name, nf, name_color, cy, 8, center=True, shadow=sh); cy += 56
    sf = mont(19, 600)
    draw_tracked(d, sub, sf, sub_color, cy, 4, center=True, shadow=sh); cy += 36
    return cy

def open_fixed(path):
    """Abre imagen aplicando rotacion EXIF."""
    return ImageOps.exif_transpose(Image.open(path)).convert("RGB")
