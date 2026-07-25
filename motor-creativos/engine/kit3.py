# ⚙️ CONFIGURA ESTAS RUTAS antes de usar:
# FONTS_DIR = carpeta con las fuentes (.ttf)
# BASE_DIR = carpeta con logo y assets
# Reemplaza /Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/Playa Blanca/motor_creativos/fonts/ y BASE_DIR/ por tus rutas reales.

#!/usr/bin/env python3
"""Motor v4 - degradado direccional limpio + tipografia premium (Fraunces+Archivo).
Texto anclado abajo, foto respira arriba. Zona segura central para 9:16 + 1:1."""
import sys; sys.path.insert(0,"/Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/Playa Blanca/motor_creativos/engine")
from designkit import (W,H,COBALT,COBALT_D,COBALT_L,NAVY,NAVY_DEEP,WHITE,OFFWHITE,MIST,ICE,
                       measure,tracked_width,draw_tracked,draw_center,wrap_text,cover_crop,
                       enhance_premium,gradient_pill,draw_arrow,save,open_fixed,font)
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
import numpy as np

FD="/Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/Playa Blanca/motor_creativos/fonts/"
_c={}
def F(path,size,axes=None):
    k=(path,size,tuple(axes) if axes else None)
    if k in _c: return _c[k]
    f=ImageFont.truetype(path,size)
    if axes:
        try: f.set_variation_by_axes(axes)
        except: pass
    _c[k]=f; return f

# Fraunces: [opsz, wght, soft, wonk]  -> opsz alto = display elegante, wonk 0 = sobrio
def fr(size,wght=600,opsz=144,soft=0,wonk=0): return F(FD+"Fraunces.ttf",size,[opsz,wght,soft,wonk])
def fr_it(size,wght=500,opsz=144,soft=0,wonk=0): return F(FD+"Fraunces-Italic.ttf",size,[opsz,wght,soft,wonk])
# Archivo: [wght, wdth]
def ar(size,wght=500,wdth=100): return F(FD+"Archivo.ttf",size,[wght,wdth])

# ---- ZONA SEGURA ----
SAFE_TOP=(H-W)//2; SAFE_BOT=SAFE_TOP+W; SAFE_CY=H//2  # 420,1500,960

# ---- LOGO oficial ----
def logo(white=False,target_w=None):
    p="/Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/Playa Blanca/motor_creativos/assets/logo_white_trim.png" if white else "/Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/Playa Blanca/motor_creativos/assets/logo_navy_trim.png"
    lg=Image.open(p).convert("RGBA")
    if target_w:
        r=target_w/lg.width; lg=lg.resize((target_w,int(lg.height*r)),Image.LANCZOS)
    return lg
def paste_logo(base,y,target_w,white=True):
    lg=logo(white=white,target_w=target_w); x=(W-lg.width)//2
    base.alpha_composite(lg,(x,y)); return y+lg.height

# ---- BACKGROUND ----
def bg(path,fx=0.5,fy=0.4,color=1.05,contrast=1.04,bright=1.02):
    src=open_fixed(path); im=cover_crop(src,W,H,focus_x=fx,focus_y=fy)
    im=enhance_premium(im,color=color,contrast=contrast,bright=bright,sharp=1.05)
    return im.convert("RGBA")

# ---- DEGRADADO DIRECCIONAL LIMPIO (la clave) ----
def cinematic_gradient(base, anchor=980, floor_alpha=252, top_alpha=0,
                       text_top=None, plateau_alpha=205,
                       color_top=(7,17,44), color_bot=(3,9,26), top_dark=72):
    """
    TINTE AZUL DE MARCA FUERTE full-image:
    - capa azul de marca bien presente y PAREJA en TODA la imagen
    - el texto blanco resalta con fuerza en cualquier zona (clara u oscura)
    - refuerzo extra en la franja de texto para legibilidad total
    La imagen se ve teñida de azul marca (duotono), texto siempre legible.
    """
    if text_top is None: text_top = anchor + 120
    # Azul de marca (cobalto/navy)
    BLUE_TOP = (16, 42, 104)
    BLUE_MID = (13, 34, 88)
    BLUE_BOT = (8, 22, 60)
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); px=ov.load()
    veil = 150              # capa azul base FUERTE y pareja en toda la imagen
    text_extra = 70         # refuerzo adicional en zona de texto
    for y in range(H):
        prog = y/H
        if prog < 0.5:
            t=prog/0.5
            r=int(BLUE_TOP[0]+(BLUE_MID[0]-BLUE_TOP[0])*t)
            g=int(BLUE_TOP[1]+(BLUE_MID[1]-BLUE_TOP[1])*t)
            b=int(BLUE_TOP[2]+(BLUE_MID[2]-BLUE_TOP[2])*t)
        else:
            t=(prog-0.5)/0.5
            r=int(BLUE_MID[0]+(BLUE_BOT[0]-BLUE_MID[0])*t)
            g=int(BLUE_MID[1]+(BLUE_BOT[1]-BLUE_MID[1])*t)
            b=int(BLUE_MID[2]+(BLUE_BOT[2]-BLUE_MID[2])*t)
        a = veil
        # refuerzo gradual hacia la zona de texto (abajo)
        if y > text_top - 160:
            tt=(y-(text_top-160))/max(1,(H-(text_top-160)))
            tt=max(0,min(1,tt))
            a += int(text_extra*(tt**1.1))
        if a>255: a=255
        for x in range(W): px[x,y]=(r,g,b,a)
    base.alpha_composite(ov)

def soft_shadow(box,radius,color,blur):
    l=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(l).rounded_rectangle(box,radius=radius,fill=color)
    return l.filter(ImageFilter.GaussianBlur(blur))

# kicker con lineas finas
def kicker(d,text,y,color=ICE,line=(255,255,255,140),size=22,track=6,ll=54,gp=24):
    f=ar(size,650); tw=tracked_width(d,text,f,track); tot=tw+2*(ll+gp); lx=(W-tot)/2
    yy_line=y+size*0.62
    d.line([(lx,yy_line),(lx+ll,yy_line)],fill=line,width=2)
    draw_tracked(d,text,f,color,y,track,x=lx+ll+gp,center=False)
    d.line([(lx+ll+gp+tw+gp,yy_line),(lx+tot,yy_line)],fill=line,width=2)

def draw_safe(base):
    d=ImageDraw.Draw(base)
    d.line([(0,SAFE_TOP),(W,SAFE_TOP)],fill=(255,40,40,200),width=3)
    d.line([(0,SAFE_BOT),(W,SAFE_BOT)],fill=(255,40,40,200),width=3)

# ===== VARIANTES DE BOTON / CTA para A/B testing =====
def cta_solid(base, y, text, w=560, h=92, c1=COBALT, c2=COBALT_D, arrow=True):
    """CTA pill solido con gradiente (default)."""
    cx=(W-w)//2
    base.alpha_composite(soft_shadow([cx,y+8,cx+w,y+h+8],h//2,(5,16,42,175),14))
    base.alpha_composite(gradient_pill(w,h,c1,c2),(int(cx),int(y)))
    d=ImageDraw.Draw(base)
    cf=ar(31,640); tw_,thh,tbb=measure(d,text,cf)
    grp=tw_+(22+30 if arrow else 0); gx=(W-grp)//2
    d.text((gx,y+(h-thh)//2-tbb[1]),text,font=cf,fill=WHITE)
    if arrow: draw_arrow(d,gx+tw_+22,y+h//2,30,WHITE,4,12)
    return y+h

def cta_outline(base, y, text, w=560, h=90, arrow=True):
    """CTA outline blanco (mas elegante, menos agresivo)."""
    cx=(W-w)//2
    pill=Image.new("RGBA",(W,H),(0,0,0,0))
    ImageDraw.Draw(pill).rounded_rectangle([cx,y,cx+w,y+h],radius=h//2,
        fill=(255,255,255,18),outline=(255,255,255,235),width=3)
    base.alpha_composite(pill)
    d=ImageDraw.Draw(base)
    cf=ar(31,640); tw_,thh,tbb=measure(d,text,cf)
    grp=tw_+(22+30 if arrow else 0); gx=(W-grp)//2
    d.text((gx,y+(h-thh)//2-tbb[1]),text,font=cf,fill=WHITE)
    if arrow: draw_arrow(d,gx+tw_+22,y+h//2,30,WHITE,4,12)
    return y+h

def cta_white(base, y, text, w=560, h=92, arrow=True, txt_color=None):
    """CTA blanco solido con texto navy (maximo contraste, alto CTR)."""
    if txt_color is None: txt_color=NAVY
    cx=(W-w)//2
    base.alpha_composite(soft_shadow([cx,y+8,cx+w,y+h+8],h//2,(5,16,42,150),14))
    pill=Image.new("RGBA",(W,H),(0,0,0,0))
    ImageDraw.Draw(pill).rounded_rectangle([cx,y,cx+w,y+h],radius=h//2,fill=(255,255,255,255))
    base.alpha_composite(pill)
    d=ImageDraw.Draw(base)
    cf=ar(31,680); tw_,thh,tbb=measure(d,text,cf)
    grp=tw_+(22+30 if arrow else 0); gx=(W-grp)//2
    d.text((gx,y+(h-thh)//2-tbb[1]),text,font=cf,fill=txt_color)
    if arrow:
        dd=ImageDraw.Draw(base)
        ax=gx+tw_+22; ay=y+h//2
        dd.line([(ax,ay),(ax+30,ay)],fill=txt_color,width=4)
        dd.line([(ax+30-12,ay-12),(ax+30,ay)],fill=txt_color,width=4)
        dd.line([(ax+30-12,ay+12),(ax+30,ay)],fill=txt_color,width=4)
    return y+h

# Badge de urgencia (esquina) - sube CTR con escasez visual
def urgency_badge(base, text, y=None, color=(214,40,40)):
    d=ImageDraw.Draw(base)
    f=ar(20,700)
    tw=tracked_width(d,text,f,2)
    pad=22; w=tw+2*pad; h=52
    if y is None: y=SAFE_TOP+20
    x=(W-w)//2
    pill=Image.new("RGBA",(W,H),(0,0,0,0))
    ImageDraw.Draw(pill).rounded_rectangle([x,y,x+w,y+h],radius=h//2,fill=color+(240,))
    base.alpha_composite(pill)
    draw_tracked(ImageDraw.Draw(base),text,f,WHITE,y+(h-26)//2,2,center=True)
    return y+h

# Sello/medallon de confianza
def trust_seal(base, big_text, small_text, cx, cy, r=78):
    seal=Image.new("RGBA",(W,H),(0,0,0,0))
    sd=ImageDraw.Draw(seal)
    sd.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(255,255,255,22),outline=(255,255,255,220),width=3)
    base.alpha_composite(seal)
    d=ImageDraw.Draw(base)
    bf=ar(38,750); bb=d.textbbox((0,0),big_text,font=bf)
    d.text((cx-(bb[2]-bb[0])//2,cy-32),big_text,font=bf,fill=WHITE)
    sf=ar(15,600)
    for i,ln in enumerate(small_text.split("\n")):
        sb=d.textbbox((0,0),ln,font=sf)
        d.text((cx-(sb[2]-sb[0])//2,cy+6+i*18),ln,font=sf,fill=OFFWHITE)

# ===== VARIANTES DE BOTON CTA (para A/B de conversion) =====
def cta_solid(base, cta, yy, cw=560, ch=92):
    """Botón sólido cobalto con sombra (default, alta conversión)."""
    cx=(W-cw)//2
    base.alpha_composite(soft_shadow([cx,yy+8,cx+cw,yy+ch+8],ch//2,(5,16,42,175),14))
    base.alpha_composite(gradient_pill(cw,ch,COBALT,COBALT_D),(int(cx),int(yy)))
    d=ImageDraw.Draw(base)
    cf=ar(31,640); tw,th,tb=measure(d,cta,cf); grp=tw+22+30; gx=(W-grp)//2
    d.text((gx,yy+(ch-th)/2-tb[1]),cta,font=cf,fill=WHITE)
    draw_arrow(d,gx+tw+22,yy+ch/2,30,WHITE,4,12)
    return yy+ch

def cta_outline(base, cta, yy, cw=560, ch=92):
    """Botón outline (borde) translúcido — look editorial premium."""
    cx=(W-cw)//2
    ov=Image.new("RGBA",(W,H),(0,0,0,0))
    ImageDraw.Draw(ov).rounded_rectangle([cx,yy,cx+cw,yy+ch],radius=ch//2,
        fill=(255,255,255,28),outline=(255,255,255,235),width=2)
    base.alpha_composite(ov)
    d=ImageDraw.Draw(base)
    cf=ar(31,640); tw,th,tb=measure(d,cta,cf); grp=tw+22+30; gx=(W-grp)//2
    d.text((gx,yy+(ch-th)/2-tb[1]),cta,font=cf,fill=WHITE)
    draw_arrow(d,gx+tw+22,yy+ch/2,30,WHITE,4,12)
    return yy+ch

def cta_white(base, cta, yy, cw=560, ch=92):
    """Botón blanco sólido, texto navy — máximo contraste, muy clickeable."""
    cx=(W-cw)//2
    base.alpha_composite(soft_shadow([cx,yy+8,cx+cw,yy+ch+8],ch//2,(5,16,42,150),14))
    ov=Image.new("RGBA",(W,H),(0,0,0,0))
    ImageDraw.Draw(ov).rounded_rectangle([cx,yy,cx+cw,yy+ch],radius=ch//2,fill=(255,255,255,250))
    base.alpha_composite(ov)
    d=ImageDraw.Draw(base)
    cf=ar(31,680); tw,th,tb=measure(d,cta,cf); grp=tw+22+30; gx=(W-grp)//2
    d.text((gx,yy+(ch-th)/2-tb[1]),cta,font=cf,fill=(16,40,96))
    draw_arrow(d,gx+tw+22,yy+ch/2,30,(16,40,96),4,12)
    return yy+ch

def badge_urgency(base, text, yy):
    """Píldora de urgencia (roja sutil) para escasez."""
    d=ImageDraw.Draw(base)
    f=ar(20,700); tw=tracked_width(d,text,f,3)
    pw=tw+56; ph=44; px=(W-pw)//2
    ov=Image.new("RGBA",(W,H),(0,0,0,0))
    ImageDraw.Draw(ov).rounded_rectangle([px,yy,px+pw,yy+ph],radius=ph//2,
        fill=(200,40,40,230))
    base.alpha_composite(ov)
    d=ImageDraw.Draw(base)
    draw_tracked(d,text,f,WHITE,yy+(ph-f.size)//2-2,3,x=px+28,center=False)
    return yy+ph

# ===== ELEMENTOS PRO PARA CTR =====
def stat_highlight(base, yy, big, label, cw=560):
    """Dato grande destacado (ej: '30%' + 'plusvalía estimada'). Sube CTR con razón concreta."""
    d=ImageDraw.Draw(base)
    bf=ar(72,780)
    bb=d.textbbox((0,0),big,font=bf); bw=bb[2]-bb[0]
    lf=ar(24,500)
    lab_lines=label.split("\n")
    # dato grande centrado
    d.text(((W-bw)//2,yy),big,font=bf,fill=WHITE,
           stroke_width=0)
    # sombra suave manual
    yy2=yy+88
    for ln in lab_lines:
        lb=d.textbbox((0,0),ln,font=lf); lw=lb[2]-lb[0]
        d.text(((W-lw)//2,yy2),ln,font=lf,fill=ICE); yy2+=30
    return yy2

def badge_pill(base, text, yy, fill=(255,255,255,235), txt=(16,40,96)):
    """Píldora de dato/garantía (blanca) — destaca sobre el azul, sube confianza."""
    d=ImageDraw.Draw(base)
    f=ar(20,700); tw=tracked_width(d,text,f,2)
    pw=tw+52; ph=46; px=(W-pw)//2
    ov=Image.new("RGBA",(W,H),(0,0,0,0))
    ImageDraw.Draw(ov).rounded_rectangle([px,yy,px+pw,yy+ph],radius=ph//2,fill=fill)
    base.alpha_composite(ov)
    draw_tracked(ImageDraw.Draw(base),text,f,txt,yy+(ph-22)//2-2,2,x=px+26,center=False)
    return yy+ph

def double_cta_hint(base, yy, main_text, sub_text, cw=560, ch=92):
    """CTA con micro-texto debajo (ej: 'Agenda visita' + 'Respuesta en 24h')."""
    end=cta_white(base,main_text,yy,cw,ch)
    d=ImageDraw.Draw(base)
    sf=ar(19,500); sb=d.textbbox((0,0),sub_text,font=sf); sw=sb[2]-sb[0]
    d.text(((W-sw)//2,end+10),sub_text,font=sf,fill=ICE)
    return end+10+26

# ===== BULLETS CON CHECK ELEGANTES (estilo premium, no emoji barato) =====
def check_bullets(base, yy, items, cw=720):
    """Lista de beneficios con check circular azul/blanco elegante."""
    d=ImageDraw.Draw(base)
    f=ar(27,450)
    # medir el item mas ancho para centrar el bloque
    line_h=52
    cx_block = W//2
    # alinear a la izquierda dentro de un bloque centrado
    maxw=0
    for it in items:
        bb=d.textbbox((0,0),it,font=f); maxw=max(maxw,bb[2]-bb[0])
    check_d=30; gap=18
    block_w=check_d+gap+maxw
    x0=(W-block_w)//2
    for it in items:
        cy=yy+line_h//2
        # check circle
        r=check_d//2
        ov=Image.new("RGBA",(W,H),(0,0,0,0))
        od=ImageDraw.Draw(ov)
        od.ellipse([x0,cy-r,x0+check_d,cy+r],fill=(255,255,255,235))
        base.alpha_composite(ov)
        d=ImageDraw.Draw(base)
        # checkmark navy
        d.line([(x0+8,cy+1),(x0+13,cy+7)],fill=(16,40,96),width=3)
        d.line([(x0+13,cy+7),(x0+23,cy-7)],fill=(16,40,96),width=3)
        # texto
        tb=d.textbbox((0,0),it,font=f)
        d.text((x0+check_d+gap,cy-(tb[3]-tb[1])//2-tb[1]),it,font=f,fill=WHITE)
        yy+=line_h
    return yy

# ===== ELEMENTOS NUEVOS PARA CREATIVOS VARIADOS =====

def check_card(base, yy, items, cw=760, pad=28):
    """Bullets dentro de una tarjeta de cristal (glass card)."""
    d=ImageDraw.Draw(base)
    f=ar(26,450)
    line_h=54
    card_h=pad*2+line_h*len(items)
    x0=int((W-cw)//2); yy=int(yy)
    # glass card con blur
    region=base.crop((x0,yy,x0+cw,yy+card_h)).filter(ImageFilter.GaussianBlur(18))
    dk=Image.new("RGBA",region.size,(10,26,60,120))
    region=Image.alpha_composite(region.convert("RGBA"),dk)
    mask=Image.new("L",region.size,0)
    ImageDraw.Draw(mask).rounded_rectangle([0,0,cw-1,card_h-1],radius=28,fill=255)
    base.paste(region,(x0,yy),mask)
    bd=Image.new("RGBA",(W,H),(0,0,0,0))
    ImageDraw.Draw(bd).rounded_rectangle([x0,yy,x0+cw,yy+card_h],radius=28,outline=(255,255,255,60),width=2)
    base.alpha_composite(bd)
    # items
    iy=yy+pad
    tx=x0+pad+8
    for it in items:
        cy=iy+line_h//2
        r=14
        ov=Image.new("RGBA",(W,H),(0,0,0,0))
        ImageDraw.Draw(ov).ellipse([tx,cy-r,tx+28,cy+r],fill=(110,170,255,255))
        base.alpha_composite(ov)
        d=ImageDraw.Draw(base)
        d.line([(tx+8,cy+1),(tx+13,cy+7)],fill=WHITE,width=3)
        d.line([(tx+13,cy+7),(tx+22,cy-6)],fill=WHITE,width=3)
        tb=d.textbbox((0,0),it,font=f)
        d.text((tx+28+16,cy-(tb[3]-tb[1])//2-tb[1]),it,font=f,fill=WHITE)
        iy+=line_h
    return yy+card_h

def number_stats(base, yy, stats):
    """Fila de estadísticas grandes (ej: 23 AÑOS | 3,500+ FAMILIAS | 90 HA)."""
    d=ImageDraw.Draw(base)
    nf=ar(46,780); lf=ar(17,550)
    n=len(stats)
    seg=W//n
    for i,(big,lab) in enumerate(stats):
        cx=seg*i+seg//2
        bb=d.textbbox((0,0),big,font=nf)
        d.text((cx-(bb[2]-bb[0])//2,yy),big,font=nf,fill=WHITE)
        lb=d.textbbox((0,0),lab,font=lf)
        d.text((cx-(lb[2]-lb[0])//2,yy+56),lab,font=lf,fill=ICE)
        # divisor vertical
        if i<n-1:
            d.line([(seg*(i+1),yy+8),(seg*(i+1),yy+62)],fill=(255,255,255,80),width=1)
    return yy+86

def check_row_inline(base, yy, items):
    """Check en fila horizontal (chips), para 2-3 beneficios cortos."""
    d=ImageDraw.Draw(base)
    f=ar(22,550)
    # medir
    chips=[]
    for it in items:
        tb=d.textbbox((0,0),it,font=f); w=tb[2]-tb[0]
        chips.append((it,w))
    gap=16; chip_pad=44; ch=48
    total=sum(28+10+w+chip_pad for _,w in chips)+gap*(len(chips)-1)
    x=(W-total)//2
    for it,w in chips:
        cw_=28+10+w+chip_pad
        ov=Image.new("RGBA",(W,H),(0,0,0,0))
        ImageDraw.Draw(ov).rounded_rectangle([x,yy,x+cw_,yy+ch],radius=ch//2,fill=(255,255,255,30),outline=(255,255,255,150),width=1)
        base.alpha_composite(ov)
        d=ImageDraw.Draw(base)
        cy=yy+ch//2; cx=x+chip_pad//2
        r=12
        ov2=Image.new("RGBA",(W,H),(0,0,0,0))
        ImageDraw.Draw(ov2).ellipse([cx,cy-r,cx+24,cy+r],fill=(110,200,255,255))
        base.alpha_composite(ov2)
        d=ImageDraw.Draw(base)
        d.line([(cx+7,cy+1),(cx+11,cy+6)],fill=(10,30,70),width=2)
        d.line([(cx+11,cy+6),(cx+19,cy-5)],fill=(10,30,70),width=2)
        d.text((cx+24+10,cy-(f.size)//2-2),it,font=f,fill=WHITE)
        x+=cw_+gap
    return yy+ch

def side_accent_line(base, yy, h, color=(110,170,255,255)):
    """Línea de acento vertical al lado del texto (estilo editorial moderno)."""
    d=ImageDraw.Draw(base)
    x=(W-880)//2 - 24
    ov=Image.new("RGBA",(W,H),(0,0,0,0))
    ImageDraw.Draw(ov).rounded_rectangle([x,yy,x+5,yy+h],radius=2,fill=color)
    base.alpha_composite(ov)

# ===== 5 ESTILOS NUEVOS DE CHECKLIST (tanda creativa 2) =====

def check_timeline(base, yy, items, accent=(110,170,255,255)):
    """Checklist tipo timeline vertical: circulos conectados por linea."""
    d=ImageDraw.Draw(base)
    f=ar(26,460); line_h=66
    maxw=0
    for it in items:
        bb=d.textbbox((0,0),it,font=f); maxw=max(maxw,bb[2]-bb[0])
    block_w=40+22+maxw
    x0=int((W-block_w)//2)
    cx=x0+18
    n=len(items)
    # linea conectora
    ov=Image.new("RGBA",(W,H),(0,0,0,0))
    ImageDraw.Draw(ov).line([(cx,int(yy)+line_h//2),(cx,int(yy)+line_h*(n-1)+line_h//2)],fill=(255,255,255,90),width=2)
    base.alpha_composite(ov)
    iy=yy
    for it in items:
        cy=int(iy)+line_h//2
        r=18
        ov2=Image.new("RGBA",(W,H),(0,0,0,0))
        od=ImageDraw.Draw(ov2)
        od.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(12,30,72,255),outline=accent,width=3)
        base.alpha_composite(ov2)
        d=ImageDraw.Draw(base)
        d.line([(cx-7,cy+1),(cx-2,cy+7)],fill=accent,width=3)
        d.line([(cx-2,cy+7),(cx+8,cy-6)],fill=accent,width=3)
        tb=d.textbbox((0,0),it,font=f)
        d.text((cx+r+22,cy-(tb[3]-tb[1])//2-tb[1]),it,font=f,fill=WHITE)
        iy+=line_h
    return yy+line_h*n

def check_numbered(base, yy, items, accent=(110,170,255,255)):
    """Checklist con numeros grandes (01, 02, 03) en vez de checks."""
    d=ImageDraw.Draw(base)
    f=ar(27,460); nf=ar(34,800); line_h=64
    maxw=0
    for it in items:
        bb=d.textbbox((0,0),it,font=f); maxw=max(maxw,bb[2]-bb[0])
    block_w=56+20+maxw
    x0=int((W-block_w)//2)
    iy=yy
    for i,it in enumerate(items):
        cy=int(iy)+line_h//2
        num=f"0{i+1}"
        d=ImageDraw.Draw(base)
        # numero en color de acento
        nb=d.textbbox((0,0),num,font=nf)
        d.text((x0,cy-(nb[3]-nb[1])//2-nb[1]),num,font=nf,fill=(120,180,255,255))
        tb=d.textbbox((0,0),it,font=f)
        d.text((x0+56+20,cy-(tb[3]-tb[1])//2-tb[1]),it,font=f,fill=WHITE)
        iy+=line_h
    return yy+line_h*len(items)

def check_pills_stack(base, yy, items, accent=(110,200,255,255)):
    """Cada beneficio en su propia pildora apilada (full width)."""
    d=ImageDraw.Draw(base)
    f=ar(25,500); pill_h=56; gap=14; pw=720
    x0=int((W-pw)//2)
    iy=yy
    for it in items:
        ov=Image.new("RGBA",(W,H),(0,0,0,0))
        ImageDraw.Draw(ov).rounded_rectangle([x0,int(iy),x0+pw,int(iy)+pill_h],radius=pill_h//2,
            fill=(255,255,255,26),outline=(255,255,255,90),width=1)
        base.alpha_composite(ov)
        d=ImageDraw.Draw(base)
        cy=int(iy)+pill_h//2; cxc=x0+30
        r=12
        ov2=Image.new("RGBA",(W,H),(0,0,0,0))
        ImageDraw.Draw(ov2).ellipse([cxc,cy-r,cxc+24,cy+r],fill=accent)
        base.alpha_composite(ov2)
        d=ImageDraw.Draw(base)
        d.line([(cxc+7,cy+1),(cxc+11,cy+6)],fill=(10,30,70),width=2)
        d.line([(cxc+11,cy+6),(cxc+19,cy-5)],fill=(10,30,70),width=2)
        tb=d.textbbox((0,0),it,font=f)
        d.text((cxc+24+16,cy-(tb[3]-tb[1])//2-tb[1]),it,font=f,fill=WHITE)
        iy+=pill_h+gap
    return yy+(pill_h+gap)*len(items)-gap

def feature_icons_row(base, yy, items):
    """Fila de iconos con etiqueta debajo (estilo amenidades visual)."""
    d=ImageDraw.Draw(base)
    f=ar(18,550)
    n=len(items)
    seg=min(180, (W-120)//n)
    total=seg*n
    x0=(W-total)//2
    for i,(icon,lab) in enumerate(items):
        cx=x0+seg*i+seg//2
        cy=int(yy)+34
        # circulo con icono (usamos inicial estilizada)
        r=32
        ov=Image.new("RGBA",(W,H),(0,0,0,0))
        ImageDraw.Draw(ov).ellipse([cx-r,cy-r,cx+r,cy+r],fill=(255,255,255,30),outline=(160,200,255,220),width=2)
        base.alpha_composite(ov)
        d=ImageDraw.Draw(base)
        icf=ar(28,700); ib=d.textbbox((0,0),icon,font=icf)
        d.text((cx-(ib[2]-ib[0])//2,cy-(ib[3]-ib[1])//2-ib[1]),icon,font=icf,fill=WHITE)
        lb=d.textbbox((0,0),lab,font=f)
        d.text((cx-(lb[2]-lb[0])//2,cy+r+12),lab,font=f,fill=ICE)
    return yy+34+32+12+24

def check_split_card(base, yy, items, accent=(120,210,150,255)):
    """Card dividida: cada fila con check verde + fondo alternado sutil."""
    d=ImageDraw.Draw(base)
    f=ar(26,460); row_h=58; cw=740
    x0=int((W-cw)//2)
    total_h=row_h*len(items)
    # card base
    region=base.crop((x0,int(yy),x0+cw,int(yy)+total_h)).filter(ImageFilter.GaussianBlur(16))
    dk=Image.new("RGBA",region.size,(8,22,54,130))
    region=Image.alpha_composite(region.convert("RGBA"),dk)
    mask=Image.new("L",region.size,0)
    ImageDraw.Draw(mask).rounded_rectangle([0,0,cw-1,total_h-1],radius=24,fill=255)
    base.paste(region,(x0,int(yy)),mask)
    bd=Image.new("RGBA",(W,H),(0,0,0,0))
    ImageDraw.Draw(bd).rounded_rectangle([x0,int(yy),x0+cw,int(yy)+total_h],radius=24,outline=(255,255,255,55),width=2)
    base.alpha_composite(bd)
    iy=yy
    for i,it in enumerate(items):
        cy=int(iy)+row_h//2; tx=x0+34
        # separador entre filas
        if i>0:
            d=ImageDraw.Draw(base)
            d.line([(x0+24,int(iy)),(x0+cw-24,int(iy))],fill=(255,255,255,30),width=1)
        r=14
        ov=Image.new("RGBA",(W,H),(0,0,0,0))
        ImageDraw.Draw(ov).ellipse([tx,cy-r,tx+28,cy+r],fill=accent)
        base.alpha_composite(ov)
        d=ImageDraw.Draw(base)
        d.line([(tx+8,cy+1),(tx+12,cy+7)],fill=WHITE,width=3)
        d.line([(tx+12,cy+7),(tx+21,cy-6)],fill=WHITE,width=3)
        tb=d.textbbox((0,0),it,font=f)
        d.text((tx+28+16,cy-(tb[3]-tb[1])//2-tb[1]),it,font=f,fill=WHITE)
        iy+=row_h
    return yy+total_h
