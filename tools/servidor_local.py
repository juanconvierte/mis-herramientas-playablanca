#!/usr/bin/env python3
"""
Servidor local que imita a Vercel con el vercel.json de esta carpeta
(cleanUrls, rewrites y headers, incluida la CSP), para probar antes de publicar.

  python3 -E tools/servidor_local.py [puerto]     -> http://localhost:4173
  RAIZ_SITIO=../web-panama-LIVE python3 tools/servidor_local.py 4174   (sirve otra carpeta)
"""
import http.server
import json
import os
import re
import sys

RAIZ = os.environ.get('RAIZ_SITIO') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = json.load(open(os.path.join(RAIZ, 'vercel.json'), encoding='utf-8'))
NO_PUBLICO = re.compile(r'^/(tools|_?fuente-hijo[^/]*|\.git|images/\.manifiesto\.json)(/|$)')


def regla(fuente):
    return re.compile('^' + fuente + '$')


HEADERS = [(regla(h['source']), h['headers']) for h in CFG.get('headers', [])]
REWRITES = [(regla(r['source']), r['destination']) for r in CFG.get('rewrites', [])]


class Vercelito(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=RAIZ, **k)

    def resolver(self):
        ruta = self.path.split('?', 1)[0].split('#', 1)[0]
        if NO_PUBLICO.match(ruta):
            return None, ruta
        for rx, destino in REWRITES:
            if rx.match(ruta):
                return destino, ruta
        if CFG.get('cleanUrls'):
            if ruta.endswith('.html'):
                return 'REDIRECT:' + ruta[:-5], ruta
            if ruta != '/' and not os.path.splitext(ruta)[1] and os.path.exists(os.path.join(RAIZ, ruta.lstrip('/') + '.html')):
                return ruta + '.html', ruta
        return ruta, ruta

    def do_GET(self):
        destino, original = self.resolver()
        if destino is None:
            self.send_error(404)
            return
        if destino.startswith('REDIRECT:'):
            self.send_response(308)
            self.send_header('Location', destino[9:] or '/')
            self.end_headers()
            return
        self._original = original
        q = self.path[len(self.path.split('?', 1)[0]):]
        self.path = destino + q
        return super().do_GET()

    def end_headers(self):
        original = getattr(self, '_original', self.path)
        for rx, lista in HEADERS:
            if rx.match(original):
                for h in lista:
                    self.send_header(h['key'], h['value'])
        super().end_headers()

    def log_message(self, *a):
        pass


if __name__ == '__main__':
    puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 4173
    print('http://localhost:%d' % puerto)
    http.server.ThreadingHTTPServer(('127.0.0.1', puerto), Vercelito).serve_forever()
