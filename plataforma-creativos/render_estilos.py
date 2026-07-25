#!/usr/bin/env python3
"""Estilos de diseño para creativos — todo en zona segura (cuadrado central 420..1500)."""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import os

BASE = "/Users/juanescorcha/Downloads/PROYECTOS IA/META ADS"
FD   = BASE + "/motor-creativos/fonts/"
PH   = BASE + "/fotos/proyecto/a/"
OUT  = BASE + "/plataforma-creativos/muestras/"
os.makedirs(OUT, exist_ok=True)
W,H = 1080,1920
ST,BT,CY = 420,1500,960   # zona segura = cuadrado central

def fr(s):  return ImageFont.truetype(FD+"Fraunces.ttf", s)
def fri(s): return ImageFont.truetype(FD+"Fraunces-Italic.ttf", s)
def ar(s):  return ImageFont.truetype(FD+"Archivo.ttf", s)

ANG = {
 "retiro":     dict(kicker="PACÍFICO DE PANAMÁ", hook="Trabajó toda la vida.\nAhora despierte\nfrente al mar.",
                    subs=["Residencias frente a la playa","Un hogar, no unas vacaciones"], cta="Quiero conocerla"),
 "vista":      dict(kicker="PLAYA BLANCA RESIDENCES", hook="¿Y si esta fuera\nsu vista cada\nmañana?",
                    subs=["Residencias frente a la playa","Playa Blanca · Panamá"], cta="Ver la vista"),
 "tranquilidad":dict(kicker="BEACH & LAGOON RESIDENCES", hook="Cambie el ruido\npor el sonido\ndel mar.",
                    subs=["Comunidad cerrada · Seguridad 24/7","Pacífico de Panamá"], cta="Quiero conocerla"),
 "comunidad":  dict(kicker="PLAYA BLANCA · PANAMÁ", hook="Vecinos como usted.\nVida que\nse disfruta.",
                    subs=["Comunidad frente al mar","Amenidades · Seguridad · Calma"], cta="Quiero conocerla"),
}

def tracked(d,text,font,fill,cx,y,sp):
    total=sum(d.textlength(c,font=font)+sp for c in text)-sp
    x=cx-total/2
    for c in text: d.text((x,y),c,font=font,fill=fill); x+=d.textlength(c,font=font)+sp

def wrap(d,text,font,maxw):
    out=[]
    for para in text.split("\n"):
        line=""
        for w in para.split(" "):
            t=(line+" "+w).strip()
            if d.textlength(t,font=font)>maxw and line: out.append(line); line=w
            else: line=t
        out.append(line)
    return out

def cover(name):
    img=Image.open(PH+name).convert("RGB")
    ir=img.width/img.height; cr=W/H
    if ir>cr: nh=H; nw=int(H*ir)
    else: nw=W; nh=int(W/ir)
    img=img.resize((nw,nh),Image.LANCZOS).crop(((nw-W)//2,(nh-H)//2,(nw-W)//2+W,(nh-H)//2+H))
    img=ImageEnhance.Color(img).enhance(1.06); img=ImageEnhance.Contrast(img).enhance(1.05)
    return img.convert("RGBA")

def vgrad(base,y0,y1,c,a0,a1):
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    for i in range(int(y0),int(y1)):
        t=(i-y0)/max(1,(y1-y0)); a=int(a0+(a1-a0)*t)
        d.line([(0,i),(W,i)],fill=(c[0],c[1],c[2],max(0,min(255,a))))
    base.alpha_composite(ov)

# ---------------- ESTILO 1: EDITORIAL (lujo minimal) ----------------
def s_editorial(name,ang,out):
    A=ANG[ang]; b=cover(name)
    vgrad(b,H*0.42,H,(6,14,28),0,215); vgrad(b,0,H*0.22,(6,14,28),120,0)
    d=ImageDraw.Draw(b)
    hf=fr(84); lines=wrap(d,A["hook"],hf,W*0.84)
    bh=52+ len(lines)*int(hf.size*1.14) +30+ len(A["subs"])*40 +70
    y=BT-bh-20
    tracked(d,A["kicker"],ar(23),(198,214,240,255),W/2,y,7); y+=58
    for ln in lines: d.text((W/2,y),ln,font=hf,fill=(255,255,255,255),anchor="ma"); y+=int(hf.size*1.14)
    y+=14; d.line([(W/2-46,y),(W/2+46,y)],fill=(255,255,255,150),width=2); y+=30
    for s in A["subs"]: d.text((W/2,y),s,font=ar(27),fill=(235,240,250,235),anchor="ma"); y+=40
    y+=20; tracked(d,A["cta"].upper()+"   →",ar(26),(255,255,255,255),W/2,y,3)
    b.convert("RGB").save(out,quality=92); print("OK",out.split("/")[-1])

# ---------------- ESTILO 2: BANDA (bloque de color) ----------------
def s_banda(name,ang,out):
    A=ANG[ang]; b=cover(name)
    vgrad(b,0,H*0.30,(6,14,28),90,0)
    d=ImageDraw.Draw(b)
    hf=fr(72); lines=wrap(d,A["hook"],hf,W*0.72)
    inner=50+len(lines)*int(hf.size*1.12)+18+len(A["subs"])*38+30+92
    pad=60; bx0,bx1=70,W-70; by1=BT-30; by0=by1-inner-pad*2
    # banda gradiente azul translucida
    band=Image.new("RGBA",(W,H),(0,0,0,0)); bd=ImageDraw.Draw(band)
    for i in range(int(by0),int(by1)):
        t=(i-by0)/(by1-by0); col=(int(20+20*t),int(52+30*t),int(120-20*t),238)
        bd.line([(bx0,i),(bx1,i)],fill=col)
    m=Image.new("L",(W,H),0); ImageDraw.Draw(m).rounded_rectangle([bx0,by0,bx1,by1],radius=40,fill=255)
    b.paste(band,(0,0),m)
    d=ImageDraw.Draw(b)
    y=by0+pad
    tracked(d,A["kicker"],ar(21),(180,205,250,255),W/2,y,5); y+=50
    for ln in lines: d.text((W/2,y),ln,font=hf,fill=(255,255,255,255),anchor="ma"); y+=int(hf.size*1.12)
    y+=18
    for s in A["subs"]: d.text((W/2,y),s,font=ar(25),fill=(228,236,250,240),anchor="ma"); y+=38
    y+=22; cw=520; ch=84; cx=(W-cw)//2
    d.rounded_rectangle([cx,y,cx+cw,y+ch],radius=ch//2,fill=(255,255,255,255))
    d.text((W/2,y+ch/2),A["cta"],font=ar(30),fill=(18,42,92,255),anchor="mm")
    b.convert("RGB").save(out,quality=92); print("OK",out.split("/")[-1])

# ---------------- ESTILO 3: CINE (letterbox cinematográfico) ----------------
def s_cine(name,ang,out):
    A=ANG[ang]; b=cover(name)
    vgrad(b,H*0.45,H*0.86,(4,10,22),0,205)
    d=ImageDraw.Draw(b)
    # barras negras (cubren zona IG arriba/abajo, texto queda en el cuadrado)
    d.rectangle([0,0,W,300],fill=(6,10,18,255)); d.rectangle([0,H-300,W,H],fill=(6,10,18,255))
    # marca arriba del cuadrado
    d.text((W/2,470),"PLAYA BLANCA",font=fr(30),fill=(255,255,255,235),anchor="ma")
    tracked(d,"BEACH & LAGOON RESIDENCES",ar(15),(200,210,225,210),W/2,512,4)
    hf=fr(78); lines=wrap(d,A["hook"],hf,W*0.82)
    bh=48+len(lines)*int(hf.size*1.13)+16+len(A["subs"])*36+30+84
    y=BT-bh-10
    tracked(d,A["kicker"],ar(22),(150,185,240,255),W/2,y,6); y+=52
    for ln in lines: d.text((W/2,y),ln,font=hf,fill=(255,255,255,255),anchor="ma"); y+=int(hf.size*1.13)
    y+=14
    for s in A["subs"]: d.text((W/2,y),s,font=ar(26),fill=(232,238,250,235),anchor="ma"); y+=36
    y+=22; cw=500; ch=82; cx=(W-cw)//2
    d.rounded_rectangle([cx,y,cx+cw,y+ch],radius=14,fill=(63,123,216,255))
    d.text((W/2,y+ch/2),A["cta"],font=ar(29),fill=(255,255,255,255),anchor="mm")
    b.convert("RGB").save(out,quality=92); print("OK",out.split("/")[-1])

# ---------------- ESTILO 4: TARJETA GLASS (vidrio esmerilado) ----------------
def s_glass(name,ang,out):
    A=ANG[ang]; b=cover(name)
    vgrad(b,H*0.30,H,(6,14,28),0,120)
    d0=ImageDraw.Draw(b)
    hf=fr(64); lines=wrap(d0,A["hook"],hf,760)
    inner=44+len(lines)*int(hf.size*1.12)+16+len(A["subs"])*36+28+82
    pad=54; cx0,cx1=90,W-90; cy1=BT-40; cy0=cy1-inner-pad*2
    box=(cx0,int(cy0),cx1,int(cy1))
    region=b.crop(box).filter(ImageFilter.GaussianBlur(22))
    region=Image.alpha_composite(region,Image.new("RGBA",region.size,(12,22,44,120)))
    m=Image.new("L",region.size,0); ImageDraw.Draw(m).rounded_rectangle([0,0,region.size[0]-1,region.size[1]-1],radius=38,fill=255)
    b.paste(region,(box[0],box[1]),m)
    d=ImageDraw.Draw(b)
    d.rounded_rectangle(box,radius=38,outline=(255,255,255,90),width=2)
    y=cy0+pad
    tracked(d,A["kicker"],ar(20),(190,208,245,255),W/2,y,5); y+=46
    for ln in lines: d.text((W/2,y),ln,font=hf,fill=(255,255,255,255),anchor="ma"); y+=int(hf.size*1.12)
    y+=16
    for s in A["subs"]: d.text((W/2,y),s,font=ar(24),fill=(226,234,250,235),anchor="ma"); y+=36
    y+=20; cw=460; ch=78; bx=(W-cw)//2
    d.rounded_rectangle([bx,y,bx+cw,y+ch],radius=ch//2,fill=(63,123,216,255))
    d.text((W/2,y+ch/2),A["cta"],font=ar(28),fill=(255,255,255,255),anchor="mm")
    b.convert("RGB").save(out,quality=92); print("OK",out.split("/")[-1])

PHOTO="1(1).jpg"   # foto limpia conocida
s_editorial(PHOTO,"retiro",       OUT+"estilo_1_editorial.jpg")
s_banda(    PHOTO,"vista",        OUT+"estilo_2_banda.jpg")
s_cine(     PHOTO,"tranquilidad", OUT+"estilo_3_cine.jpg")
s_glass(    PHOTO,"comunidad",    OUT+"estilo_4_glass.jpg")
print("LISTO — 4 estilos")
