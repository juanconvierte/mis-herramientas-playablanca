#!/usr/bin/env python3
"""
STUDIO — motor del brief. Recibe un spec (o lista) y renderiza.
Reglas DURAS que enforza solo: tamaño exacto, zona segura (cuadrado central),
compliance Meta Vivienda, marca. Todo lo demás lo manda el brief.

Uso:  python3 studio.py specs.json
spec = {
  "photo": "1(1).jpg",
  "style": "editorial|banda|cine|glass",
  "kicker": "PACÍFICO DE PANAMÁ",
  "hook": "La vida\nque se ganó.",
  "subs": ["Residencias frente a la playa"],
  "cta": "Quiero conocerla",
  "badge": "CUPOS LIMITADOS",          # opcional (sello arriba dcha)
  "pos": "abajo|centro|arriba",        # opcional (default abajo)
  "format": "story|feed|sq",           # opcional (default story)
  "out": "nombre.jpg"
}
"""
import sys, os, json
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

BASE = "/Users/juanescorcha/Downloads/PROYECTOS IA/META ADS"
FD   = BASE + "/motor-creativos/fonts/"
PH   = BASE + "/fotos/proyecto/a/"
OUT  = BASE + "/plataforma-creativos/salidas/"
os.makedirs(OUT, exist_ok=True)

FORMATS = {"story":(1080,1920), "feed":(1080,1350), "sq":(1080,1080)}

def fr(s):  return ImageFont.truetype(FD+"Fraunces.ttf", s)
def fri(s): return ImageFont.truetype(FD+"Fraunces-Italic.ttf", s)
def ar(s):  return ImageFont.truetype(FD+"Archivo.ttf", s)

# ---- REGLA DURA: compliance Meta Vivienda ----
import re
BANNED = [r"rentabilidad", r"plusval[íi]a", r"retorno", r"se paga sol[ao]", r"renta garantizad",
          r"alquiler garantizad", r"ingresos? por alquiler", r"sin banco", r"escrow", r"fideicomiso",
          r"t[íi]tulo a (tu|su) nombre", r"inversi[óo]n garantizad", r"ganancia asegurad",
          r"\b\+?\s?(5[0-9]|6[0-9])\s*a[ñn]os\b", r"pensionad"]
def lint(spec):
    blob = " ".join([str(spec.get(k,"")) for k in ("kicker","hook","cta","badge")] + spec.get("subs",[]))
    hits = [m.group(0) for r in BANNED for m in [re.search(r, blob, re.I)] if m]
    return hits

def tracked(d,text,font,fill,cx,y,sp):
    total=sum(d.textlength(c,font=font)+sp for c in text)-sp
    x=cx-total/2
    for c in text: d.text((x,y),c,font=font,fill=fill); x+=d.textlength(c,font=font)+sp

def wrap(d,text,font,maxw):
    out=[]
    for para in str(text).split("\n"):
        line=""
        for w in para.split(" "):
            t=(line+" "+w).strip()
            if d.textlength(t,font=font)>maxw and line: out.append(line); line=w
            else: line=t
        out.append(line)
    return out

def cover(name,W,H):
    img=Image.open(PH+name).convert("RGB")
    ir=img.width/img.height; cr=W/H
    if ir>cr: nh=H; nw=int(H*ir)
    else: nw=W; nh=int(W/ir)
    img=img.resize((nw,nh),Image.LANCZOS).crop(((nw-W)//2,(nh-H)//2,(nw-W)//2+W,(nh-H)//2+H))
    img=ImageEnhance.Color(img).enhance(1.06); img=ImageEnhance.Contrast(img).enhance(1.05)
    return img.convert("RGBA")

def vgrad(base,y0,y1,c,a0,a1,W,H):
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    for i in range(int(y0),int(y1)):
        t=(i-y0)/max(1,(y1-y0)); a=int(a0+(a1-a0)*t)
        d.line([(0,i),(W,i)],fill=(c[0],c[1],c[2],max(0,min(255,a))))
    base.alpha_composite(ov)

def safe_zone(W,H):
    # REGLA DURA: cuadrado central
    st=(H-W)//2; return st, H-st, H//2   # top, bot, cy

def anchor(pos, bh, ST, BT, CY):
    if pos=="arriba": y0=ST+40
    elif pos=="centro": y0=CY-bh/2+50
    else: y0=BT-bh-30
    return max(ST+20, min(y0, BT-bh-20))

def badge(d, txt, W, ST, color=(214,40,40)):
    if not txt: return
    f=ar(20); pad=16; tw=d.textlength(txt,font=f)
    bw=tw+pad*2; bh=44; x1=W-64; x0=x1-bw; y=ST+16
    d.rounded_rectangle([x0,y,x1,y+bh],radius=8,fill=color+(255,))
    d.text((x0+pad,y+bh/2),txt,font=f,fill=(255,255,255,255),anchor="lm")

# ---------------- ESTILOS ----------------
def sty_editorial(b,spec,W,H,ST,BT,CY):
    vgrad(b,H*0.42,H,(6,14,28),0,215,W,H); vgrad(b,0,H*0.22,(6,14,28),120,0,W,H)
    d=ImageDraw.Draw(b); hf=fr(int(W*0.078)); lines=wrap(d,spec["hook"],hf,W*0.84); subs=spec.get("subs",[])
    bh=(52 if spec.get("kicker") else 0)+len(lines)*int(hf.size*1.14)+30+len(subs)*40+70+(84 if spec.get("price") else 0)
    y=anchor(spec.get("pos","abajo"),bh,ST,BT,CY)
    if spec.get("kicker"): tracked(d,spec["kicker"],ar(23),(198,214,240,255),W/2,y,7); y+=58
    for ln in lines: d.text((W/2,y),ln,font=hf,fill=(255,255,255,255),anchor="ma"); y+=int(hf.size*1.14)
    y+=14; d.line([(W/2-46,y),(W/2+46,y)],fill=(255,255,255,150),width=2); y+=30
    for s in subs: d.text((W/2,y),s,font=ar(27),fill=(235,240,250,235),anchor="ma"); y+=40
    if spec.get("price"): y+=6; price_line(d,spec["price"],W,y); y+=84
    y+=18; _pill(d,spec.get("cta","Más información"),W,y,spec)

def sty_banda(b,spec,W,H,ST,BT,CY):
    vgrad(b,0,H*0.30,(6,14,28),90,0,W,H)
    d=ImageDraw.Draw(b); hf=fr(72); lines=wrap(d,spec["hook"],hf,W*0.72); subs=spec.get("subs",[])
    inner=(50 if spec.get("kicker") else 0)+len(lines)*int(hf.size*1.12)+18+len(subs)*38+30+92+(84 if spec.get("price") else 0)
    pad=54; bx0,bx1=70,W-70
    y0=anchor(spec.get("pos","abajo"),inner+pad*2,ST,BT,CY); by0,by1=y0,y0+inner+pad*2
    band=Image.new("RGBA",(W,H),(0,0,0,0)); bd=ImageDraw.Draw(band)
    for i in range(int(by0),int(by1)):
        t=(i-by0)/(by1-by0); bd.line([(bx0,i),(bx1,i)],fill=(int(20+20*t),int(52+30*t),int(120-20*t),238))
    m=Image.new("L",(W,H),0); ImageDraw.Draw(m).rounded_rectangle([bx0,by0,bx1,by1],radius=40,fill=255); b.paste(band,(0,0),m)
    d=ImageDraw.Draw(b); y=by0+pad
    if spec.get("kicker"): tracked(d,spec["kicker"],ar(21),(180,205,250,255),W/2,y,5); y+=50
    for ln in lines: d.text((W/2,y),ln,font=hf,fill=(255,255,255,255),anchor="ma"); y+=int(hf.size*1.12)
    y+=18
    for s in subs: d.text((W/2,y),s,font=ar(25),fill=(228,236,250,240),anchor="ma"); y+=38
    if spec.get("price"): y+=6; price_line(d,spec["price"],W,y); y+=84
    y+=22; _pill(d,spec.get("cta","Más información"),W,y,spec,invert=True)

def sty_cine(b,spec,W,H,ST,BT,CY):
    vgrad(b,H*0.45,H*0.86,(4,10,22),0,205,W,H)
    d=ImageDraw.Draw(b); d.rectangle([0,0,W,ST-120],fill=(6,10,18,255)); d.rectangle([0,BT+120,W,H],fill=(6,10,18,255))
    d.text((W/2,ST+30),"PLAYA BLANCA",font=fr(30),fill=(255,255,255,235),anchor="ma")
    hf=fr(78); lines=wrap(d,spec["hook"],hf,W*0.82); subs=spec.get("subs",[])
    bh=(52 if spec.get("kicker") else 0)+len(lines)*int(hf.size*1.13)+16+len(subs)*36+30+84+(84 if spec.get("price") else 0)
    y=anchor(spec.get("pos","abajo"),bh,ST,BT,CY)
    if spec.get("kicker"): tracked(d,spec["kicker"],ar(22),(150,185,240,255),W/2,y,6); y+=52
    for ln in lines: d.text((W/2,y),ln,font=hf,fill=(255,255,255,255),anchor="ma"); y+=int(hf.size*1.13)
    y+=14
    for s in subs: d.text((W/2,y),s,font=ar(26),fill=(232,238,250,235),anchor="ma"); y+=36
    if spec.get("price"): y+=6; price_line(d,spec["price"],W,y); y+=84
    y+=22; _pill(d,spec.get("cta","Más información"),W,y,spec,radius=14)

def sty_glass(b,spec,W,H,ST,BT,CY):
    vgrad(b,H*0.30,H,(6,14,28),0,120,W,H)
    d0=ImageDraw.Draw(b); hf=fr(64); lines=wrap(d0,spec["hook"],hf,760); subs=spec.get("subs",[])
    inner=(46 if spec.get("kicker") else 0)+len(lines)*int(hf.size*1.12)+16+len(subs)*36+28+82+(84 if spec.get("price") else 0)
    pad=52; cx0,cx1=90,W-90
    y0=anchor(spec.get("pos","abajo"),inner+pad*2,ST,BT,CY); box=(cx0,int(y0),cx1,int(y0+inner+pad*2))
    region=b.crop(box).filter(ImageFilter.GaussianBlur(22))
    region=Image.alpha_composite(region,Image.new("RGBA",region.size,(12,22,44,120)))
    m=Image.new("L",region.size,0); ImageDraw.Draw(m).rounded_rectangle([0,0,region.size[0]-1,region.size[1]-1],radius=38,fill=255)
    b.paste(region,(box[0],box[1]),m)
    d=ImageDraw.Draw(b); d.rounded_rectangle(box,radius=38,outline=(255,255,255,90),width=2)
    y=y0+pad
    if spec.get("kicker"): tracked(d,spec["kicker"],ar(20),(190,208,245,255),W/2,y,5); y+=46
    for ln in lines: d.text((W/2,y),ln,font=hf,fill=(255,255,255,255),anchor="ma"); y+=int(hf.size*1.12)
    y+=16
    for s in subs: d.text((W/2,y),s,font=ar(24),fill=(226,234,250,235),anchor="ma"); y+=36
    if spec.get("price"): y+=6; price_line(d,spec["price"],W,y); y+=84
    y+=18; _pill(d,spec.get("cta","Más información"),W,y,spec)

def price_line(d,text,W,y):
    """Precio destacado (tag con borde) — dato de producto, lo pide el cliente."""
    f=ar(36); tw=d.textlength(text,font=f); pad=24; bw=tw+pad*2; bh=66; x=(W-bw)/2
    d.rounded_rectangle([x,y,x+bw,y+bh],radius=14,outline=(255,255,255,165),width=2)
    d.text((W/2,y+bh/2),text,font=f,fill=(255,255,255,255),anchor="mm")
    return bh

def _pill(d,cta,W,y,spec,invert=False,radius=None):
    col=tuple(spec.get("cta_color",[63,123,216]))
    cw=520; ch=84; cx=(W-cw)//2; r=radius if radius is not None else ch//2
    if invert:
        d.rounded_rectangle([cx,y,cx+cw,y+ch],radius=r,fill=(255,255,255,255))
        d.text((W/2,y+ch/2),cta,font=ar(30),fill=(18,42,92,255),anchor="mm")
    else:
        d.rounded_rectangle([cx,y,cx+cw,y+ch],radius=r,fill=col+(255,))
        d.text((W/2,y+ch/2),cta,font=ar(30),fill=(255,255,255,255),anchor="mm")

STYLES={"editorial":sty_editorial,"banda":sty_banda,"cine":sty_cine,"glass":sty_glass}

def render(spec):
    hits=lint(spec)
    if hits: print(f"  ⚠️  COMPLIANCE: {spec.get('out')} usa términos prohibidos {hits} — corrige el brief")
    W,H=FORMATS.get(spec.get("format","story"),FORMATS["story"])
    ST,BT,CY=safe_zone(W,H)
    b=cover(spec["photo"],W,H)
    STYLES.get(spec.get("style","editorial"),sty_editorial)(b,spec,W,H,ST,BT,CY)
    badge(ImageDraw.Draw(b), spec.get("badge"), W, ST, tuple(spec.get("badge_color",[214,40,40])))
    out=OUT+spec.get("out","creativo.jpg")
    b.convert("RGB").save(out,quality=92)
    print(f"  ✓ {spec.get('out')}  [{spec.get('style')}·{spec.get('pos','abajo')}·{W}x{H}]{'  COMPLIANT' if not hits else ''}")
    return out

if __name__=="__main__":
    specs=json.load(open(sys.argv[1])) if len(sys.argv)>1 else []
    if isinstance(specs,dict): specs=[specs]
    print(f"STUDIO — {len(specs)} creativo(s)")
    for s in specs: render(s)
    print("LISTO")
