#!/usr/bin/env python3
"""Diferencia píxel a píxel entre dos capturas: % de píxeles distintos y mapa de calor.
  python3 -E tools/qa/diferencia.py A.png B.png [mapa.png]
"""
import sys

from PIL import Image, ImageChops


def comparar(a_ruta, b_ruta, mapa=None):
    a = Image.open(a_ruta).convert('RGB')
    b = Image.open(b_ruta).convert('RGB')
    if a.size != b.size:
        w, h = max(a.size[0], b.size[0]), max(a.size[1], b.size[1])
        print('TAMAÑO DISTINTO: A=%s B=%s' % (a.size, b.size))
        lienzo_a, lienzo_b = Image.new('RGB', (w, h), 'magenta'), Image.new('RGB', (w, h), 'magenta')
        lienzo_a.paste(a, (0, 0)); lienzo_b.paste(b, (0, 0))
        a, b = lienzo_a, lienzo_b
    d = ImageChops.difference(a, b).convert('L')
    hist = d.histogram()
    total = sum(hist)
    distintos = total - hist[0]
    fuertes = sum(hist[41:])
    media = sum(i * n for i, n in enumerate(hist)) / total
    caja = d.point(lambda v: 255 if v > 40 else 0).getbbox()
    print('píxeles distintos: %.3f%% · fuertes(>40): %.4f%% · diferencia media: %.3f · zona fuerte: %s'
          % (100.0 * distintos / total, 100.0 * fuertes / total, media, caja))
    if mapa:
        rojo = Image.new('RGB', a.size, (255, 0, 0))
        base = a.convert('L').convert('RGB').point(lambda v: v // 3)
        base.paste(rojo, mask=d.point(lambda v: 255 if v > 40 else 0))
        base.save(mapa)
    return fuertes / total


if __name__ == '__main__':
    comparar(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
