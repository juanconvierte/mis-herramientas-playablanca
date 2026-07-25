#!/usr/bin/env python3
"""Render de muestra (espejo del canvas de la plataforma) para previsualizar."""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os

BASE = "/Users/juanescorcha/Downloads/PROYECTOS IA/META ADS"
FD   = BASE + "/motor-creativos/fonts/"
PH   = BASE + "/fotos/proyecto/a/"
OUT  = BASE + "/plataforma-creativos/muestras/"
os.makedirs(OUT, exist_ok=True)

def fr(sz): return ImageFont.truetype(FD+"Fraunces.ttf", sz)
def ar(sz): return ImageFont.truetype(FD+"Archivo.ttf", sz)

ANGLES = {
 "retiro":      dict(kicker="PACÍFICO DE PANAMÁ", hook="Trabajó toda la vida.\nAhora despierte frente al mar.",
                     subs=["Residencias frente a la playa · Playa Blanca","Un hogar, no unas vacaciones"], cta="Quiero conocerla"),
 "vista":       dict(kicker="PLAYA BLANCA RESIDENCES", hook="¿Y si esta fuera\nsu vista cada mañana?",
                     subs=["Residencias frente a la playa","Playa Blanca · Panamá"], cta="Ver la vista"),
 "tranquilidad":dict(kicker="BEACH & LAGOON RESIDENCES", hook="Aquí el tiempo\nse siente distinto.",
                     subs=["Comunidad cerrada · Seguridad 24/7","Playa Blanca, Pacífico de Panamá"], cta="Quiero conocerla"),
}

def tracked(d, text, font, fill, cx, y, sp, anchor_center=True):
    widths=[d.textlength(c,font=font)+sp for c in text]; total=sum(widths)-sp
    x=cx-total/2 if anchor_center else cx
    for c in text:
        d.text((x,y),c,font=font,fill=fill); x+=d.textlength(c,font=font)+sp

def wrap(d, text, font, maxw):
    out=[]
    for para in text.split("\n"):
        line=""
        for w in para.split(" "):
            t=(line+" "+w).strip()
            if d.textlength(t,font=font)>maxw and line: out.append(line); line=w
            else: line=t
        out.append(line)
    return out

def cover(img, W, H):
    ir=img.width/img.height; cr=W/H
    if ir>cr: nh=H; nw=int(H*ir)
    else: nw=W; nh=int(W/ir)
    img=img.resize((nw,nh), Image.LANCZOS)
    return img.crop(((nw-W)//2,(nh-H)//2,(nw-W)//2+W,(nh-H)//2+H))

# zona segura (convención del motor): cuadrado central 420..1500
SAFE_TOP, SAFE_BOT, SAFE_CY = 420, 1500, 960

def build_block(d, A, W):
    """Devuelve lista de ops [(tipo, altura, ...)] y altura total. Cada op lleva su avance."""
    ops=[]
    ops.append(("text", 48, fr(34), "PLAYA BLANCA", (255,255,255,255), "ma"))
    ops.append(("track",30, ar(17), "BEACH & LAGOON RESIDENCES", 4, (255,255,255,200)))
    ops.append(("gap",  30))
    ops.append(("track",52, ar(22), A["kicker"], 5, (143,180,240,255)))
    hf=fr(int(W*0.072))
    for ln in wrap(d,A["hook"],hf,W*0.86):
        ops.append(("text", int(hf.size*1.16), hf, ln, (255,255,255,255), "ma"))
    ops.append(("gap", 12))
    for s in A["subs"]:
        ops.append(("text", 38, ar(27), s, (255,255,255,235), "ma"))
    ops.append(("gap", 26))
    ops.append(("cta", 88+34, A["cta"]))
    ops.append(("track",26, ar(22), "panama.playablancaresidences.com", 2, (255,255,255,185)))
    h=sum(o[1] for o in ops)
    return ops,h

def render(photo, angle, out, W=1080, H=1920):
    A=ANGLES[angle]
    base=cover(Image.open(PH+photo).convert("RGB"), W, H)
    base=ImageEnhance.Color(base).enhance(1.05)
    base=ImageEnhance.Contrast(base).enhance(1.04)
    base=base.convert("RGBA")
    d0=ImageDraw.Draw(base)
    ops,bh=build_block(d0, A, W)
    # anclar bloque centrado en zona segura, empujado un toque abajo
    y0=SAFE_CY - bh/2 + 70
    y0=max(SAFE_TOP+20, min(y0, SAFE_BOT-bh-20))
    # veil azul + scrim que arranca antes del bloque
    base.alpha_composite(Image.new("RGBA",(W,H),(10,26,45,45)))
    scrim=Image.new("RGBA",(W,H),(0,0,0,0)); sd=ImageDraw.Draw(scrim)
    top=int(max(500, y0-150))
    for i in range(top,H):
        t=(i-top)/(H-top); a=int(30 + 215*min(1,t*1.15))
        sd.line([(0,i),(W,i)], fill=(6,16,30,min(a,248)))
    base.alpha_composite(scrim)
    d=ImageDraw.Draw(base)
    y=y0
    for op in ops:
        kind,adv=op[0],op[1]
        if kind=="text":
            _,_,font,txt,fill,anc=op; d.text((W/2,y),txt,font=font,fill=fill,anchor=anc)
        elif kind=="track":
            _,_,font,txt,sp,fill=op; tracked(d,txt,font,fill,W/2,y,sp)
        elif kind=="cta":
            cta=op[2]; cw=min(int(W*0.62),560); ch=88; cx=(W-cw)//2
            d.rounded_rectangle([cx,y,cx+cw,y+ch],radius=ch//2,fill=(63,123,216,255))
            d.text((W/2,y+ch/2),cta,font=ar(30),fill=(255,255,255,255),anchor="mm")
        y+=adv
    # marca de zona segura (debug, se quita en prod)
    end=y0+bh
    st="OK" if (y0>=SAFE_TOP and end<=SAFE_BOT) else f"FUERA(y0={int(y0)},fin={int(end)})"
    base.convert("RGB").save(out+".jpg",quality=92)
    print("OK", out.split("/")[-1], f"y0={int(y0)} fin={int(end)} {st}")

pics=sorted([p for p in os.listdir(PH) if p.lower().endswith((".jpg",".png"))])
combos=[("retiro",pics[0]),("vista",pics[10] if len(pics)>10 else pics[1]),("tranquilidad",pics[20] if len(pics)>20 else pics[2])]
for ang,ph in combos:
    render(ph, ang, OUT+f"muestra_{ang}")
print("FOTOS USADAS:", [c[1] for c in combos])
