#!/usr/bin/env python3
"""
Espejo de la landing del hijo -> web-panama-NUEVA.

  Diseño:          www.playablancaresidences.com/panama/  (idéntico, sin tocar)
  Funcionamiento:  el de web-panama-LIVE (formulario, HubSpot, Faro, CAPI, medición)

Uso (desde la carpeta web-panama-NUEVA):
  python3 -E tools/sincronizar.py             # baja la versión actual del hijo y regenera
  python3 -E tools/sincronizar.py --offline   # regenera desde la copia guardada en _fuente-hijo/

Cada parche exige encontrar su texto exacto. Si el hijo cambia su página y un parche
ya no calza, el script se detiene y dice cuál; no publica nada a medias.
"""
import hashlib
import json
import os
import re
import sys
import urllib.request

from PIL import Image, ImageOps

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FUENTE = os.path.join(RAIZ, '_fuente-hijo')
ORIGEN = 'https://www.playablancaresidences.com'
SITIO = 'https://panama.playablancaresidences.com'

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import parches  # noqa: E402  (tools/parches.py: todo lo que se cambia, en un solo lugar)


# ---------------------------------------------------------------- descarga
def bajar(ruta_remota, destino):
    req = urllib.request.Request(ORIGEN + ruta_remota, headers={'User-Agent': 'Mozilla/5.0 (espejo PB)'})
    with urllib.request.urlopen(req, timeout=30) as r:
        if r.status != 200:
            raise SystemExit('No bajó %s (HTTP %s)' % (ruta_remota, r.status))
        datos = r.read()
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, 'wb') as f:
        f.write(datos)
    return datos


def imagenes_referidas(texto):
    return sorted(set(m.group(1) for m in re.finditer(r'(?:\.\./)+(images/[^"\')\s]+)', texto)))


def descargar_todo():
    print('Bajando la versión actual del hijo...')
    html = bajar('/panama/', os.path.join(FUENTE, 'panama', 'index.html')).decode('utf-8')
    css = bajar('/panama/estilo.css', os.path.join(FUENTE, 'panama', 'estilo.css')).decode('utf-8')
    gracias = bajar('/panama/gracias/', os.path.join(FUENTE, 'panama', 'gracias', 'index.html')).decode('utf-8')
    rutas = imagenes_referidas(html + css + gracias)
    for r in rutas:
        bajar('/' + r, os.path.join(FUENTE, r))
    print('  %d imágenes' % len(rutas))


# ---------------------------------------------------------------- utilidades
def leer(ruta):
    with open(ruta, encoding='utf-8') as f:
        return f.read()


def escribir(ruta, texto):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(texto)


def aplicar(texto, lista, archivo):
    for nombre, viejo, nuevo, veces in lista:
        n = texto.count(viejo)
        if (veces is None and n == 0) or (veces is not None and n != veces):
            raise SystemExit('PARCHE NO CALZA [%s] "%s": esperaba %s, encontré %d' % (archivo, nombre, veces or '>=1', n))
        texto = texto.replace(viejo, nuevo)
    return texto


def huella(ruta):
    h = hashlib.sha256()
    with open(ruta, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()


# ---------------------------------------------------------------- imágenes
# Misma foto, mismo tamaño, menos peso: JPG recomprimido (respaldo) + WebP (navegadores actuales).
CALIDAD_JPG = 85
CALIDAD_WEBP = 82
CALIDAD_WEBP_HERO = 86


def optimizar_imagenes():
    origen = os.path.join(FUENTE, 'images')
    destino = os.path.join(RAIZ, 'images')
    manifiesto_ruta = os.path.join(destino, '.manifiesto.json')
    try:
        manifiesto = json.loads(leer(manifiesto_ruta))
    except (OSError, ValueError):
        manifiesto = {}
    resumen = []
    for carpeta, _, archivos in os.walk(origen):
        for nombre in sorted(archivos):
            if not re.search(r'\.(jpe?g|png)$', nombre, re.I):
                continue
            src = os.path.join(carpeta, nombre)
            rel = os.path.relpath(src, origen)
            dst = os.path.join(destino, rel)
            webp = re.sub(r'\.(jpe?g|png)$', '.webp', dst, flags=re.I)
            h = huella(src)
            if manifiesto.get(rel, {}).get('huella') == h and os.path.exists(dst) and os.path.exists(webp):
                resumen.append((rel, manifiesto[rel]['antes'], manifiesto[rel]['despues'], manifiesto[rel]['webp']))
                continue
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            im = Image.open(src)
            icc = im.info.get('icc_profile')
            im = ImageOps.exif_transpose(im)  # la orientación queda en los píxeles, no en metadatos
            antes = os.path.getsize(src)
            extra = {'icc_profile': icc} if icc else {}
            if nombre.lower().endswith('.png'):
                im.save(dst, 'PNG', optimize=True, **extra)
                im.save(webp, 'WEBP', quality=90, method=6, **extra)
            else:
                rgb = im.convert('RGB')
                rgb.save(dst, 'JPEG', quality=CALIDAD_JPG, optimize=True, progressive=True, **extra)
                q = CALIDAD_WEBP_HERO if 'hero' in nombre else CALIDAD_WEBP
                rgb.save(webp, 'WEBP', quality=q, method=6, **extra)
            if os.path.getsize(dst) >= antes:  # si no gana, queda el original tal cual
                with open(src, 'rb') as a, open(dst, 'wb') as b:
                    b.write(a.read())
            manifiesto[rel] = {'huella': h, 'antes': antes, 'despues': os.path.getsize(dst), 'webp': os.path.getsize(webp)}
            resumen.append((rel, antes, manifiesto[rel]['despues'], manifiesto[rel]['webp']))
    escribir(manifiesto_ruta, json.dumps(manifiesto, indent=1, sort_keys=True))
    a = sum(r[1] for r in resumen)
    w = sum(min(r[2], r[3]) for r in resumen)
    print('  imágenes: %d · %.1f MB -> %.1f MB' % (len(resumen), a / 1e6, w / 1e6))


def envolver_en_picture(html):
    """<img src="/images/x.jpg"> -> <picture><source webp><img ...></picture>. CSS: picture{display:contents}."""
    def cambio(m):
        tag = m.group(0)
        src = re.search(r'src="(/images/[^"]+\.(?:jpe?g|png))"', tag)
        if not src:
            return tag
        webp = re.sub(r'\.(jpe?g|png)$', '.webp', src.group(1), flags=re.I)
        if not os.path.exists(os.path.join(RAIZ, webp.lstrip('/'))):
            return tag
        if 'loading="lazy"' in tag and 'decoding=' not in tag:
            tag = tag[:-1].rstrip() + ' decoding="async">'
        return '<picture><source srcset="%s" type="image/webp">%s</picture>' % (webp, tag)
    return re.sub(r'<img\b[^>]*>', cambio, html)


def versionar_imagenes(html):
    """/images/x.webp -> /images/x.webp?v=huella: Vercel las guarda 1 año en caché; si cambian, cambia la URL."""
    def cambio(m):
        archivo = os.path.join(RAIZ, m.group(2).lstrip('/'))
        if not os.path.exists(archivo):
            raise SystemExit('Imagen referida que no existe: %s' % m.group(2))
        return '%s="%s?v=%s"' % (m.group(1), m.group(2), huella(archivo)[:8])
    return re.sub(r'(src|srcset|href)="(/images/[^"?]+)"', cambio, html)


# ---------------------------------------------------------------- armado
def armar():
    css_src = os.path.join(FUENTE, 'panama', 'estilo.css')
    css = leer(css_src)
    escribir(os.path.join(RAIZ, 'estilo.css'), css)
    version_css = huella(css_src)[:10]

    optimizar_imagenes()

    # --- landing
    html = leer(os.path.join(FUENTE, 'panama', 'index.html'))
    html = aplicar(html, parches.landing(SITIO, version_css), 'index.html')
    html = versionar_imagenes(envolver_en_picture(html))
    escribir(os.path.join(RAIZ, 'index.html'), html)

    # --- gracias
    g = leer(os.path.join(FUENTE, 'panama', 'gracias', 'index.html'))
    g = aplicar(g, parches.gracias(SITIO, version_css), 'gracias.html')
    escribir(os.path.join(RAIZ, 'gracias.html'), versionar_imagenes(g))

    print('Listo: index.html, gracias.html, estilo.css, images/')


if __name__ == '__main__':
    if '--offline' not in sys.argv:
        descargar_todo()
    armar()
