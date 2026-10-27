#!/usr/bin/env python3
"""
Espejo de la landing del hijo -> web-panama-NUEVA.

  Diseño:          www.playablancaresidences.com/panama/  (idéntico, sin tocar)
  Funcionamiento:  el de web-panama-LIVE (formulario, HubSpot, Faro, CAPI, medición)

Uso (desde la carpeta web-panama-NUEVA):
  python3 -E tools/sincronizar.py             # baja la versión actual del hijo y regenera
  python3 -E tools/sincronizar.py --offline   # regenera desde la copia guardada en _fuente-hijo/

Cada parche exige encontrar su texto exacto. Si el hijo cambia su página y un parche
ya no calza, el script se detiene ANTES de escribir nada y dice cuál parche falló.
"""
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import urllib.request

from PIL import Image, ImageOps

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FUENTE = os.path.join(RAIZ, '_fuente-hijo')
ORIGEN = 'https://www.playablancaresidences.com'

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
    """Baja a una carpeta temporal; _fuente-hijo solo se reemplaza si el armado sale bien."""
    print('Bajando la versión actual del hijo...')
    tmp = tempfile.mkdtemp(prefix='fuente-hijo-', dir=RAIZ)
    html = bajar('/panama/', os.path.join(tmp, 'panama', 'index.html')).decode('utf-8')
    css = bajar('/panama/estilo.css', os.path.join(tmp, 'panama', 'estilo.css')).decode('utf-8')
    gracias = bajar('/panama/gracias/', os.path.join(tmp, 'panama', 'gracias', 'index.html')).decode('utf-8')
    rutas = imagenes_referidas(html + css + gracias)
    for r in rutas:
        bajar('/' + r, os.path.join(tmp, r))
    print('  %d imágenes' % len(rutas))
    return tmp


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
            raise SystemExit('PARCHE NO CALZA [%s] "%s": esperaba %s, encontré %d. No se escribió nada.'
                             % (archivo, nombre, veces or '>=1', n))
        texto = texto.replace(viejo, nuevo)
    return texto


def huella(ruta):
    h = hashlib.sha256()
    with open(ruta, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()


def movil(rel):
    return re.sub(r'\.(jpe?g|png)$', '-movil.webp', rel, flags=re.I)


# ---------------------------------------------------------------- imágenes
# Misma foto, mismo tamaño, menos peso: JPG recomprimido (respaldo) + WebP (navegadores actuales).
CALIDAD_JPG = 85
CALIDAD_WEBP = 82
CALIDAD_WEBP_HERO = 86


def optimizar_imagenes(fuente):
    origen = os.path.join(fuente, 'images')
    destino = os.path.join(RAIZ, 'images')
    manifiesto_ruta = os.path.join(destino, '.manifiesto.json')
    try:
        manifiesto = json.loads(leer(manifiesto_ruta))
    except (OSError, ValueError):
        manifiesto = {}
    vigentes, resumen = set(), []
    for carpeta, _, archivos in os.walk(origen):
        for nombre in sorted(archivos):
            if not re.search(r'\.(jpe?g|png)$', nombre, re.I):
                continue
            src = os.path.join(carpeta, nombre)
            rel = os.path.relpath(src, origen)
            dst = os.path.join(destino, rel)
            webp = re.sub(r'\.(jpe?g|png)$', '.webp', dst, flags=re.I)
            recorte = parches.RECORTES_MOVIL.get(rel)
            salidas = [dst, webp] + ([os.path.join(destino, movil(rel))] if recorte else [])
            vigentes.update(os.path.relpath(s, destino) for s in salidas)
            h = huella(src)
            clave = h + json.dumps(recorte, sort_keys=True)
            if manifiesto.get(rel, {}).get('huella') == clave and all(os.path.exists(s) for s in salidas):
                resumen.append(manifiesto[rel])
                continue
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            im = Image.open(src)
            icc = im.info.get('icc_profile')
            im = ImageOps.exif_transpose(im)  # la orientación queda en los píxeles, no en metadatos
            extra = {'icc_profile': icc} if icc else {}
            if nombre.lower().endswith('.png'):
                im.save(dst, 'PNG', optimize=True, **extra)
                im.save(webp, 'WEBP', quality=90, method=6, **extra)
            else:
                rgb = im.convert('RGB')
                rgb.save(dst, 'JPEG', quality=CALIDAD_JPG, optimize=True, progressive=True, **extra)
                q = CALIDAD_WEBP_HERO if 'hero' in nombre else CALIDAD_WEBP
                rgb.save(webp, 'WEBP', quality=q, method=6, **extra)
                if recorte:
                    w, alto = rgb.size
                    x = (w - recorte['ancho']) // 2
                    rgb.crop((x, 0, x + recorte['ancho'], alto)).save(salidas[2], 'WEBP', quality=q, method=6, **extra)
            if os.path.getsize(dst) >= os.path.getsize(src):  # si no gana, queda el original tal cual
                shutil.copyfile(src, dst)
            manifiesto[rel] = {'huella': clave, 'antes': os.path.getsize(src), 'jpg': os.path.getsize(dst),
                               'webp': os.path.getsize(webp)}
            if recorte:
                manifiesto[rel]['movil'] = os.path.getsize(salidas[2])
            resumen.append(manifiesto[rel])
    # fotos que el hijo ya no usa
    for carpeta, _, archivos in os.walk(destino):
        for nombre in archivos:
            rel = os.path.relpath(os.path.join(carpeta, nombre), destino)
            if nombre != '.manifiesto.json' and rel not in vigentes:
                os.remove(os.path.join(carpeta, nombre))
    manifiesto = {k: v for k, v in manifiesto.items() if k in vigentes}
    escribir(manifiesto_ruta, json.dumps(manifiesto, indent=1, sort_keys=True))
    a = sum(r['antes'] for r in resumen)
    w = sum(min(r['jpg'], r['webp']) for r in resumen)
    print('  imágenes: %d · %.1f MB -> %.1f MB' % (len(resumen), a / 1e6, w / 1e6))


def envolver_en_picture(html):
    """<img src="/images/x.jpg"> -> <picture>[recorte celular]<source webp><img ...></picture>."""
    def cambio(m):
        tag = m.group(0)
        src = re.search(r'src="(/images/([^"]+\.(?:jpe?g|png)))"', tag)
        if not src:
            return tag
        webp = re.sub(r'\.(jpe?g|png)$', '.webp', src.group(1), flags=re.I)
        if not os.path.exists(os.path.join(RAIZ, webp.lstrip('/'))):
            return tag
        if 'loading="lazy"' in tag and 'decoding=' not in tag:
            tag = tag[:-1].rstrip() + ' decoding="async">'
        fuentes = ''
        recorte = parches.RECORTES_MOVIL.get(src.group(2))
        if recorte:
            fuentes += '<source media="%s" srcset="/images/%s" type="image/webp">' % (recorte['media'], movil(src.group(2)))
        fuentes += '<source srcset="%s" type="image/webp">' % webp
        return '<picture>%s%s</picture>' % (fuentes, tag)
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
def armar(fuente):
    # 1) parches en memoria: si alguno no calza, se para aquí sin tocar nada
    css_src = os.path.join(fuente, 'panama', 'estilo.css')
    css = leer(css_src)
    version_css = huella(css_src)[:10]
    html = aplicar(leer(os.path.join(fuente, 'panama', 'index.html')), parches.landing(version_css), 'index.html')
    g = aplicar(leer(os.path.join(fuente, 'panama', 'gracias', 'index.html')), parches.gracias(version_css), 'gracias.html')

    # 2) fotos, 3) armado final
    optimizar_imagenes(fuente)
    html = versionar_imagenes(envolver_en_picture(html))
    g = versionar_imagenes(g)
    escribir(os.path.join(RAIZ, 'estilo.css'), css)
    escribir(os.path.join(RAIZ, 'index.html'), html)
    escribir(os.path.join(RAIZ, 'gracias.html'), g)
    print('Listo: index.html, gracias.html, estilo.css, images/')


if __name__ == '__main__':
    if '--offline' in sys.argv:
        armar(FUENTE)
    else:
        tmp = descargar_todo()
        try:
            armar(tmp)
        except BaseException:
            shutil.rmtree(tmp, ignore_errors=True)
            raise
        shutil.rmtree(FUENTE, ignore_errors=True)
        os.rename(tmp, FUENTE)
