#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""render_lote.py — Renderiza un lote de creativos Playa Blanca organizados por
ángulo en salidas/<sesion>/<angulo>/. Fuerza price=False (sin precio en imagen)."""
import os, sys, json, glob
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, "engine"))
import gen4
from PIL import Image, ImageOps

FOTOS = os.path.join(BASE, "..", "fotos_proyecto", "a")
SALIDAS = os.path.join(BASE, "salidas")
SESION = "sesion_01"

# --- index basename -> ruta real, override de gen4.src ---
idx = {}
for p in glob.glob(os.path.join(FOTOS, "*")):
    b = os.path.basename(p)
    if not b.startswith("._") and p.lower().endswith((".jpg", ".jpeg", ".png")):
        idx[b] = p
def _src(n):
    if n in idx:
        return idx[n]
    raise FileNotFoundError(n)
gen4.src = _src

# --- normaliza orientacion EXIF (idempotente) ---
for b, p in idx.items():
    try:
        ImageOps.exif_transpose(Image.open(p)).save(p)
    except Exception:
        pass

# --- los 25 creativos: Formulario instantaneo, SIN precio ---
CRE = [
 # ===== TESTIMONIOS (2) =====
 {"angulo":"Testimonios","slug":"testimonios","img":"DSC00908.JPG","fy":0.38,
  "kicker":"HISTORIAS REALES","h1":"Aquí mis nietos aprenden a nadar",
  "sub":["Familias que ya viven frente al Pacífico,","en la Riviera Pacífica de Panamá."],
  "trust":"3,500+ FAMILIAS · 23 AÑOS","cta":"Agenda tu visita →","cta_style":"white","out":"testimonios_01.png"},
 {"angulo":"Testimonios","slug":"testimonios","img":"DSC00275.JPG","fy":0.40,
  "kicker":"LO QUE DICEN QUIENES YA VIVEN AQUÍ","h1":"Brindamos por la mejor decisión",
  "sub":["Compraron en preventa. Hoy cenan","frente al mar cada noche."],
  "trust":"3,500+ FAMILIAS FELICES","cta":"Déjanos tus datos →","cta_style":"outline","out":"testimonios_02.png"},

 # ===== PRUEBA SOCIAL (3) =====
 {"angulo":"Prueba social","slug":"prueba_social","img":"DSC00571.JPG","fy":0.40,
  "kicker":"NO ESTÁS SOLO EN ESTO","h1":"3,500 familias ya brindan frente al mar",
  "sub":["Súmate a la comunidad que eligió","la Riviera Pacífica de Panamá."],
  "trust":"3,500+ FAMILIAS · 1,500+ HOGARES","cta":"Conoce más →","cta_style":"white","out":"prueba_social_01.png"},
 {"angulo":"Prueba social","slug":"prueba_social","img":"DSC00798.JPG","fy":0.40,
  "kicker":"CADA SEMANA LLEGAN MÁS","h1":"Más familias se mudan aquí cada mes",
  "sub":["Ven a conocer por qué eligen","Playa Blanca una y otra vez."],
  "trust":"23 AÑOS · 90 HECTÁREAS","cta":"Agenda tu visita →","cta_style":"outline","out":"prueba_social_02.png"},
 {"angulo":"Prueba social","slug":"prueba_social","img":"piscina.jpg","fy":0.42,
  "kicker":"UN VECINDARIO DISTINTO","h1":"Se siente como vacaciones, todo el año",
  "sub":["Vecinos que se vuelven amigos","frente a la laguna."],
  "trust":"3,500+ FAMILIAS · 15+ AMENIDADES","cta":"Déjanos tus datos →","cta_style":"white","out":"prueba_social_03.png"},

 # ===== FOMO / PREVENTA (3) =====
 {"angulo":"FOMO / preventa","slug":"fomo","img":"aquavista.jpg","fy":0.40,
  "kicker":"PREVENTA ABIERTA","h1":"El precio de hoy no vuelve mañana",
  "sub":["Las primeras fases salen primero.","Después, la lista de espera."],
  "trust":"FASES LIMITADAS · PREVENTA","cta":"Aparta tu cita →","cta_style":"white","out":"fomo_01.png"},
 {"angulo":"FOMO / preventa","slug":"fomo","img":"terrazas-villas.png","fy":0.38,
  "kicker":"DISPONIBILIDAD REAL","h1":"Las villas frente al agua se agotan primero",
  "sub":["Quedan pocas con vista directa","a la laguna."],
  "trust":"UNIDADES FRENTE AL AGUA LIMITADAS","cta":"Consulta disponibilidad →","cta_style":"outline","out":"fomo_02.png"},
 {"angulo":"FOMO / preventa","slug":"fomo","img":"DSC00879.JPG","fy":0.40,
  "kicker":"ANTES DE QUE SUBA","h1":"Asegura tu precio de preventa hoy",
  "sub":["Planes directos sin banco","y unidades que se agotan."],
  "trust":"PLANES SIN BANCO · PREVENTA","cta":"Quiero los planes →","cta_style":"white","out":"fomo_03.png"},

 # ===== ASPIRACIÓN (2) =====
 {"angulo":"Aspiración","slug":"aspiracion","img":"manana.jpg","fy":0.40,
  "kicker":"TU NUEVA RUTINA","h1":"Tu café de la mañana, frente al Pacífico",
  "sub":["Despertar con la laguna a tus pies.","Eso es vivir aquí."],
  "trust":"1.5 KM DE PLAYA PRIVADA","cta":"Conoce más →","cta_style":"outline","out":"aspiracion_01.png"},
 {"angulo":"Aspiración","slug":"aspiracion","img":"DSC00247.JPG","fy":0.35,
  "kicker":"IMAGINA ESTO","h1":"Despierta con esta vista cada día",
  "sub":["El mar de frente, la laguna al lado,","y nada que envidiarle a nadie."],
  "trust":"FRENTE AL PACÍFICO DE PANAMÁ","cta":"Agenda tu visita →","cta_style":"white","out":"aspiracion_02.png"},

 # ===== CONTRASTE LAGUNA (1) =====
 {"angulo":"Contraste laguna","slug":"laguna","img":"hero-lagoon.jpg","fy":0.30,
  "kicker":"EL DIFERENCIAL QUE NADIE TIENE","h1":"La laguna de agua salada más grande de la región",
  "sub":["Cristalina y navegable, dentro","de tu propio desarrollo."],
  "trust":"LAGUNA NAVEGABLE · 90 HECTÁREAS","cta":"Conoce la laguna →","cta_style":"white","out":"laguna_01.png"},

 # ===== AUTORIDAD (3) =====
 {"angulo":"Autoridad","slug":"autoridad","img":"about-hero.png","fy":0.35,
  "kicker":"23 AÑOS DE TRAYECTORIA","h1":"23 años entregando, cero promesas vacías",
  "sub":["Lo que ves construido ya es real.","No es un render, es tu futura casa."],
  "trust":"1,500+ HOGARES ENTREGADOS","cta":"Conoce más →","cta_style":"outline","out":"autoridad_01.png"},
 {"angulo":"Autoridad","slug":"autoridad","img":"ocean-3.png","fy":0.40,
  "kicker":"RESPALDO REAL","h1":"1,500 hogares entregados. El tuyo sigue",
  "sub":["Dos décadas construyendo frente","al Pacífico de Panamá."],
  "trust":"23 AÑOS · 3,500+ FAMILIAS","cta":"Solicita información →","cta_style":"white","out":"autoridad_02.png"},
 {"angulo":"Autoridad","slug":"autoridad","img":"napa-village.png","fy":0.40,
  "kicker":"HECHOS, NO PROMESAS","h1":"Un desarrollo consolidado, no un plano",
  "sub":["90 hectáreas ya viviéndose,","con familias dentro hoy."],
  "trust":"90 HECTÁREAS · 23 AÑOS","cta":"Déjanos tus datos →","cta_style":"outline","out":"autoridad_03.png"},

 # ===== RETIRO / VIDA (4) =====
 {"angulo":"Retiro / vida","slug":"retiro","img":"DSC00507.JPG","fy":0.38,
  "kicker":"ESTE CAPÍTULO ES TUYO","h1":"Los mejores años se disfrutan, no se esperan",
  "sub":["Cambia la rutina por amaneceres","frente al mar."],
  "trust":"VISA PENSIONADO · PLAYA PRIVADA","cta":"Agenda tu visita →","cta_style":"white","out":"retiro_01.png"},
 {"angulo":"Retiro / vida","slug":"retiro","img":"DSC00490.JPG","fy":0.40,
  "kicker":"TU RETIRO, A TU MANERA","h1":"Tu retiro merece playa, no sala de espera",
  "sub":["Vive con calma frente a la laguna,","con todo a pasos de casa."],
  "trust":"VISA PENSIONADO (+55)","cta":"Conoce más →","cta_style":"outline","out":"retiro_02.png"},
 {"angulo":"Retiro / vida","slug":"retiro","img":"DSC00611.JPG","fy":0.40,
  "kicker":"EL CLIMA QUE MERECES","h1":"Cambia el frío por el sonido del mar",
  "sub":["A 1.5 h de Ciudad de Panamá,","tu nueva vida te espera."],
  "trust":"RIVIERA PACÍFICA DE PANAMÁ","cta":"Déjanos tus datos →","cta_style":"white","out":"retiro_03.png"},
 {"angulo":"Retiro / vida","slug":"retiro","img":"DSC00515.JPG","fy":0.38,
  "kicker":"TE LO GANASTE","h1":"Aquí empieza el capítulo que te ganaste",
  "sub":["Frente al Pacífico, con título","a tu nombre y pagos en escrow."],
  "trust":"TÍTULO A TU NOMBRE · ESCROW","cta":"Quiero saber más →","cta_style":"outline","out":"retiro_04.png"},

 # ===== IDENTIDAD COMPRADOR (2) =====
 {"angulo":"Identidad comprador","slug":"identidad","img":"DSC06530.JPG","fy":0.40,
  "kicker":"PARA QUIEN YA LO LOGRÓ","h1":"Para quien ya no tiene nada que demostrar",
  "sub":["Tu segundo hogar frente al mar,","sin banco de por medio."],
  "trust":"PLANES DIRECTOS SIN BANCO","cta":"Conoce más →","cta_style":"white","out":"identidad_01.png"},
 {"angulo":"Identidad comprador","slug":"identidad","img":"DSC00771.JPG","fy":0.40,
  "kicker":"TU OFICINA, TU REGLA","h1":"Trabaja desde donde otros vacacionan",
  "sub":["Internet, amenidades y el mar","como vista de tu escritorio."],
  "trust":"90 HECTÁREAS · 15+ AMENIDADES","cta":"Déjanos tus datos →","cta_style":"outline","out":"identidad_02.png"},

 # ===== AMENIDADES (5) =====
 {"angulo":"Amenidades","slug":"amenidades","img":"spa.jpg","fy":0.35,
  "kicker":"TODO A MINUTOS","h1":"Spa, golf y club de playa a un paso",
  "sub":["Más de 15 amenidades dentro","de tu propio desarrollo."],
  "trust":"15+ AMENIDADES · SPA · GOLF","cta":"Conoce más →","cta_style":"white","out":"amenidades_01.png"},
 {"angulo":"Amenidades","slug":"amenidades","img":"tennis.jpg","fy":0.40,
  "kicker":"VIVE ACTIVO","h1":"15+ amenidades sin salir de casa",
  "sub":["Tenis, golf, gimnasio y club","de playa para los tuyos."],
  "trust":"CLUB DE PLAYA · GOLF · TENIS","cta":"Agenda tu visita →","cta_style":"outline","out":"amenidades_02.png"},
 {"angulo":"Amenidades","slug":"amenidades","img":"playa.jpg","fy":0.40,
  "kicker":"TUYA Y PRIVADA","h1":"1.5 km de playa privada para los tuyos",
  "sub":["Arena, palmeras y mar,","sin compartir con nadie más."],
  "trust":"1.5 KM DE PLAYA PRIVADA","cta":"Conoce más →","cta_style":"white","out":"amenidades_03.png"},
 {"angulo":"Amenidades","slug":"amenidades","img":"nuevos-proyectos-desktop.jpg","fy":0.40,
  "kicker":"TU CLUB DE PLAYA","h1":"Tu club de playa, a pasos de la puerta",
  "sub":["Relájate frente a la laguna","cada día, no solo en vacaciones."],
  "trust":"CLUB DE PLAYA · LAGUNA NAVEGABLE","cta":"Déjanos tus datos →","cta_style":"outline","out":"amenidades_04.png"},
 {"angulo":"Amenidades","slug":"amenidades","img":"fiesta.jpg","fy":0.42,
  "kicker":"VIDA EN COMUNIDAD","h1":"Aquí siempre hay algo que celebrar",
  "sub":["Eventos, club y vecinos","que se vuelven familia."],
  "trust":"3,500+ FAMILIAS · 15+ AMENIDADES","cta":"Conoce más →","cta_style":"white","out":"amenidades_05.png"},
]

def main():
    res = []
    for i, c in enumerate(CRE, 1):
        slug = c["slug"]
        outdir = os.path.join(SALIDAS, SESION, slug)
        os.makedirs(outdir, exist_ok=True)
        cfg = dict(c)
        cfg["price"] = False            # SIN precio en la imagen
        cfg["logo"] = True
        cfg["cta"] = c["cta"].replace("→", "").strip()   # el motor ya dibuja la flecha
        cfg["url"] = False                                # objetivo formulario: sin URL web
        cfg["out"] = os.path.join(SESION, slug, c["out"])
        try:
            base, bot = gen4.build(cfg)
            ok = bot <= 1505
            estado = "OK" if ok else f"REVISAR({int(bot)})"
            print(f"[{i:02}] {estado:12s} {c['angulo']:20s} {c['img']:28s} -> {c['out']}")
            res.append({"n":i,"angulo":c["angulo"],"img":c["img"],"h1":c["h1"],
                        "cta":c["cta"],"archivo":os.path.join(SESION,slug,c["out"]),
                        "ok":ok,"bot":int(bot)})
        except Exception as e:
            print(f"[{i:02}] ERROR {c['angulo']} ({c['img']}): {e}")
            res.append({"n":i,"angulo":c["angulo"],"img":c["img"],"error":str(e)})
    ok = sum(1 for r in res if r.get("ok"))
    over = [r["archivo"] for r in res if r.get("ok") is False and "error" not in r]
    err = [r for r in res if "error" in r]
    resumen_path = os.path.join(SALIDAS, SESION, "_resumen.json")
    json.dump(res, open(resumen_path, "w"), ensure_ascii=False, indent=2)
    print(f"\n=== {ok}/{len(CRE)} OK · overflow: {len(over)} · errores: {len(err)} ===")
    if over: print("OVERFLOW:", over)
    if err: print("ERRORES:", [(e['img'], e['error']) for e in err])
    print("Resumen:", resumen_path)

if __name__ == "__main__":
    main()
