# ⚙️ CONFIGURA ESTAS RUTAS antes de usar:
# FONTS_DIR = carpeta con las fuentes (.ttf)
# BASE_DIR = carpeta con logo y assets
# Reemplaza /Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/Playa Blanca/motor_creativos/fonts/ y BASE_DIR/ por tus rutas reales.

#!/usr/bin/env python3
"""Generador v4.1 - mide el bloque y lo CENTRA en zona segura. Degradado limpio + Fraunces."""
import sys; sys.path.insert(0,"/Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/Playa Blanca/motor_creativos/engine")
from kit3 import *
import os, json

U="/Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/Playa Blanca/motor_creativos/work/fotos/"; Z="/Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/Playa Blanca/motor_creativos/work/fotos/"
def src(n):
    for d in (U,Z):
        if os.path.exists(d+n): return d+n
    raise FileNotFoundError(n)

def layout(cfg, d, measure_only=True, base=None, y0=0):
    """Construye/mide el bloque. Si measure_only: devuelve altura total.
       Si no: dibuja empezando en y0 y devuelve y final."""
    CW=cfg.get("cw",880)
    yy=y0
    # LOGO
    logo_h=0
    if cfg.get("logo",True):
        lg=logo(white=True,target_w=cfg.get("logo_w",430)); logo_h=lg.height
        if not measure_only:
            base.alpha_composite(lg,((W-lg.width)//2,int(yy)))
        yy+=logo_h+cfg.get("logo_gap",26)
    else:
        if not measure_only:
            f=ar(23,700); draw_tracked(d,"PLAYA BLANCA",f,WHITE,yy,10,shadow=((3,9,26,140),(1,1)))
        yy+=40
        if not measure_only:
            f2=ar(15,600); draw_tracked(d,"BEACH & LAGOON RESIDENCES",f2,MIST,yy,5,shadow=((3,9,26,120),(1,1)))
        yy+=42
    # KICKER
    if cfg.get("kicker"):
        if not measure_only: kicker(d,cfg["kicker"],yy,color=ICE)
        yy+=52
    # TITULAR
    h1f=fr(cfg.get("h1_size",60),wght=cfg.get("h1_w",580),opsz=144,wonk=0)
    for ln in wrap_text(d,cfg["h1"],h1f,CW):
        if not measure_only: draw_center(d,ln,h1f,WHITE,yy,shadow=((2,8,24,150),(2,2)))
        yy+=cfg.get("h1_lh",70)
    if cfg.get("accent"):
        yy+=2
        if not measure_only: draw_center(d,cfg["accent"],fr_it(cfg.get("acc_size",44),500),ICE,yy)
        yy+=cfg.get("acc_lh",58)
    yy+=12
    # SUB
    if cfg.get("sub"):
        for ln in cfg["sub"]:
            if not measure_only: draw_center(d,ln,ar(cfg.get("sub_size",28),330),OFFWHITE,yy)
            yy+=39
        yy+=18
    # divisor
    if cfg.get("divider",True):
        if not measure_only: d.line([((W-84)/2,yy),((W+84)/2,yy)],fill=(255,255,255,95),width=2)
        yy+=36
    # PRECIO
    if cfg.get("big_price"):
        if not measure_only: draw_center(d,"Desde",ar(29,400),MIST,yy)
        yy+=42
        if not measure_only: draw_center(d,cfg.get("big_price_text","$202,910"),ar(82,750),WHITE,yy,shadow=((2,8,24,150),(2,2)))
        yy+=98
        if not measure_only: draw_center(d,"USD",ar(29,600),OFFWHITE,yy)
        yy+=54
    elif cfg.get("price",True):
        plf=ar(25,400); prf=ar(33,720); a="Desde "; b=cfg.get("price_text","$202,910 USD")
        aw,_,_=measure(d,a,plf); bw,_,_=measure(d,b,prf)
        pw=aw+bw+8+86; ph=72; px=(W-pw)/2; py=yy
        if not measure_only:
            pb=Image.new("RGBA",(W,H),(0,0,0,0))
            ImageDraw.Draw(pb).rounded_rectangle([px,py,px+pw,py+ph],radius=ph//2,fill=(255,255,255,24),outline=(165,198,250,235),width=2)
            base.alpha_composite(pb); dd=ImageDraw.Draw(base)
            c2=py+ph/2
            _,ah,abb=measure(dd,a,plf); dd.text((px+43,c2-ah/2-abb[1]),a,font=plf,fill=MIST)
            _,bh,bbb=measure(dd,b,prf); dd.text((px+43+aw+8,c2-bh/2-bbb[1]),b,font=prf,fill=WHITE)
        yy=py+ph+36
    # TRUST
    if cfg.get("trust"):
        if not measure_only: draw_tracked(d,cfg["trust"],ar(21,550),OFFWHITE,yy,2)
        yy+=52
    # CTA (con estilo variable)
    cta=cfg.get("cta","Más información")
    cw_,ch_=cfg.get("cta_w",560),92; cyb=yy
    style=cfg.get("cta_style","solid")
    if not measure_only:
        if style=="white":
            cta_white(base,cta,cyb,cw_,ch_)
        elif style=="outline":
            cta_outline(base,cta,cyb,cw_,ch_)
        else:
            cta_solid(base,cta,cyb,cw_,ch_)
    yy=cyb+ch_+30
    # URL (opcional: cfg["url"]=False la quita, ej. para objetivo formulario)
    if cfg.get("url", True):
        if not measure_only: draw_tracked(d,"panama.playablancaresidences.com",ar(22,420),MIST,yy,2)
        yy+=26
    return yy-y0  # altura total

def build(cfg):
    base=bg(src(cfg["img"]),fx=cfg.get("fx",0.5),fy=cfg.get("fy",0.4),
            color=cfg.get("color",1.05),contrast=cfg.get("contrast",1.04),bright=cfg.get("bright",1.02))
    d=ImageDraw.Draw(base)
    # 1) medir altura del bloque
    block_h = layout(cfg, d, measure_only=True)
    # 2) anclar: queremos el bloque centrado en zona segura, pero empujado un poco abajo
    #    para que el degradado lo sostenga. Centro de safe = 960; lo bajamos un toque.
    center = SAFE_CY + cfg.get("block_shift", 110)
    y0 = center - block_h/2
    # clamp dentro de safe con margen
    y0 = max(SAFE_TOP+30, min(y0, SAFE_BOT-block_h-20))
    # 3) degradado: que arranque un poco antes del bloque
    anchor = int(max(700, y0 - 130))
    cinematic_gradient(base, anchor=anchor, text_top=int(y0-10), floor_alpha=cfg.get("floor",252), plateau_alpha=cfg.get("plateau",205), top_dark=cfg.get("top_dark",72))
    d=ImageDraw.Draw(base)
    # 4) dibujar
    end = layout(cfg, d, measure_only=False, base=base, y0=y0)
    # badge de urgencia opcional (esquina superior, dentro de safe)
    if cfg.get("badge"):
        urgency_badge(base, cfg["badge"], y=SAFE_TOP+30, color=tuple(cfg.get("badge_color",[214,40,40])))
    save(base,"/Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/Playa Blanca/motor_creativos/salidas/"+cfg["out"])
    bot=y0+block_h
    st="OK" if bot<=1505 else f"OVER({int(bot)})"
    print(f'{cfg["out"]:10s} y0={int(y0):4d} h={int(block_h):4d} fin={int(bot):4d} {st}')
    return base,bot

if __name__=="__main__":
    for c in json.load(open("BASE_DIR/cfgs4.json")):
        build(c)
