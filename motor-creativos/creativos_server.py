#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""creativos_server.py — Servidor local para la sección Creativos del dashboard.
Corre el motor Python (sin API, sin Opus) y sirve las imágenes al navegador.

Endpoints (CORS abierto, 127.0.0.1:8770):
  GET  /salud                      -> ok
  GET  /biblioteca                 -> { "fotos": ["1.jpg", ...] }  (biblioteca_imagenes/)
  POST /generar  {angulos:[cfg...]} -> { "creativos":[{out,angulo,ok}] }  (rinde a salidas/)
  POST /generar_ia {angulos:[cfg+modo...]} -> { "creativos":[...] }       (IA o real)
  GET  /img/<archivo>              -> PNG generado (salidas/)
  GET  /foto/<archivo>             -> foto original (biblioteca_imagenes/)  [para thumbnails]

cfg de cada ángulo = {angulo, img, fy, kicker, h1, sub[], price_text, trust, cta, badge?, out}

/generar_ia: mismo cfg + {
    modo: "real" | "ia_generar" | "ia_editar",
    prompt_ia: "...",            # requerido para ia_generar / ia_editar
    ref_imgs: ["1.jpg", ...],    # opcional (ia_editar); basenames de fotos reales
    aspect: "9:16",              # opcional
    dry_run: true,               # opcional: construye el request SIN llamar a la API
  }
  - real        -> idéntico a /generar (gen4 sobre la foto real `img`)
  - ia_generar  -> Nano Banana 2 crea el FONDO desde prompt_ia, luego gen4 overlay
  - ia_editar   -> Nano Banana 2 edita el FONDO usando fotos reales de referencia,
                   luego gen4 overlay. Salida final = creativo 1080x1920 con marca.
"""
import os, sys, json, glob, mimetypes, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
sys.path.insert(0, os.path.join(BASE, "engine"))
BIB = os.path.join(BASE, "biblioteca_imagenes")
SAL = os.path.join(BASE, "salidas")
# Fondos IA (Nano Banana) se guardan aislados aquí; luego gen4 hace el overlay.
IA_FONDOS = os.path.join(SAL, "ia_fondos")
# Fotos reales de la propiedad (109) — fuente de refs para modo edición.
FOTOS_REALES = os.path.join(os.path.dirname(BASE), "fotos_proyecto", "a")
os.makedirs(SAL, exist_ok=True)
os.makedirs(IA_FONDOS, exist_ok=True)

import generar  # reutiliza render_uno con índice recursivo de fotos
import nano_banana  # generación/edición de fondos con Nano Banana 2 (Gemini)

PORT = 8770


def _resolver_refs(ref_imgs, angulo):
    """Convierte una lista de basenames (o rutas) en rutas absolutas de fotos
    reales para anclar el modelo (modo edición). Busca en biblioteca_imagenes/
    y en fotos_proyecto/a/. Si no se pasa ninguna, auto-elige por ángulo."""
    refs = []
    for r in (ref_imgs or []):
        if not r:
            continue
        if os.path.isabs(r) and os.path.isfile(r):
            refs.append(r); continue
        b = os.path.basename(r)
        for d in (BIB, FOTOS_REALES):
            cand = os.path.join(d, b)
            if os.path.isfile(cand):
                refs.append(cand); break
    if not refs:
        # autoselección determinista por ángulo desde fotos_proyecto/a
        refs = nano_banana.elegir_refs(angulo or "", n=2, fotos_dir=FOTOS_REALES)
    return refs[:3]


def _generar_un_creativo_ia(cfg):
    """Para un ángulo en modo ia_generar / ia_editar:
      1) crea/edita el FONDO con Nano Banana 2 -> PNG en IA_FONDOS/
      2) corre la plantilla gen4 (logo+texto en zona segura) sobre ese fondo
    Devuelve dict con out, fondo_ia, mode, ok/error.
    No envía nada a la API si dry_run=True (regla de oro)."""
    modo = cfg.get("modo", "ia_generar")
    angulo = cfg.get("angulo", "creativo")
    prompt = (cfg.get("prompt_ia") or "").strip()
    dry = bool(cfg.get("dry_run"))
    if not prompt:
        return {"angulo": angulo, "modo": modo, "error": "prompt_ia vacío"}

    ref_paths = _resolver_refs(cfg.get("ref_imgs"), angulo) if modo == "ia_editar" else []

    # nombre único para el fondo IA
    slug = (angulo.lower().replace(" ", "_") or "ia")
    stamp = "%s_%d" % (slug, int(time.time() * 1000) % 100000000)
    fondo_path = os.path.join(IA_FONDOS, "fondo_%s.png" % stamp)

    nb = nano_banana.generar_fondo(
        prompt, ref_paths=ref_paths, out_path=fondo_path,
        aspect=cfg.get("aspect", "9:16"), dry_run=dry,
    )
    if not nb.get("ok"):
        return {"angulo": angulo, "modo": modo, "fase": "nano_banana",
                "error": nb.get("error", "fallo nano_banana"), "detalle": nb}

    if dry:
        # dry-run: no hay fondo real en disco -> no se corre gen4
        return {"angulo": angulo, "modo": modo, "dry_run": True,
                "nano_banana": nb, "ok": True}

    fondo_real = nb.get("out_path", fondo_path)
    # overlay logo+texto: render_uno indexa recursivamente fotos_dir=IA_FONDOS
    # y busca cfg["img"] por basename -> el fondo IA recién creado.
    cfg2 = dict(cfg)
    cfg2["img"] = os.path.basename(fondo_real)
    cfg2.setdefault("out", "%s.png" % stamp)
    try:
        ruta, bot = generar.render_uno(cfg2, IA_FONDOS, SAL)
        return {"angulo": angulo, "modo": modo, "out": os.path.basename(ruta),
                "fondo_ia": os.path.basename(fondo_real),
                "ok": bot <= 1510}
    except Exception as e:
        return {"angulo": angulo, "modo": modo, "fase": "gen4",
                "fondo_ia": os.path.basename(fondo_real), "error": str(e)}


def listar_biblioteca():
    fs = []
    for p in sorted(glob.glob(os.path.join(BIB, "*"))):
        b = os.path.basename(p)
        if p.lower().endswith((".jpg", ".jpeg", ".png")) and not b.startswith("._"):
            fs.append(b)
    return fs


class H(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code); self._cors()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers(); self.wfile.write(body)

    def _file(self, path):
        if not os.path.exists(path):
            self._json({"error": "no existe"}, 404); return
        ctype = mimetypes.guess_type(path)[0] or "application/octet-stream"
        with open(path, "rb") as f:
            data = f.read()
        self.send_response(200); self._cors()
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers(); self.wfile.write(data)

    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()

    def do_GET(self):
        p = self.path.split("?")[0]
        if p == "/salud":
            self._json({"ok": True, "fotos": len(listar_biblioteca())})
        elif p == "/biblioteca":
            self._json({"fotos": listar_biblioteca()})
        elif p.startswith("/img/"):
            self._file(os.path.join(SAL, os.path.basename(p[5:])))
        elif p.startswith("/foto/"):
            self._file(os.path.join(BIB, os.path.basename(p[6:])))
        else:
            self._json({"error": "ruta desconocida"}, 404)

    def do_POST(self):
        ruta_post = self.path.split("?")[0]
        if ruta_post == "/generar":
            return self._post_generar()
        if ruta_post == "/generar_ia":
            return self._post_generar_ia()
        self._json({"error": "ruta desconocida"}, 404)

    def _post_generar(self):
        """Flujo REAL intacto: gen4 sobre foto real de la biblioteca."""
        try:
            n = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(n) or b"{}")
            angulos = payload.get("angulos") or []
            res = []
            for cfg in angulos:
                try:
                    ruta, bot = generar.render_uno(cfg, BIB, SAL)
                    res.append({"angulo": cfg.get("angulo"), "out": os.path.basename(ruta),
                                "ok": bot <= 1510})
                except Exception as e:
                    res.append({"angulo": cfg.get("angulo"), "error": str(e)})
            ok = sum(1 for r in res if r.get("ok"))
            print("[generar] %d/%d creativos" % (ok, len(angulos)), flush=True)
            self._json({"creativos": res})
        except Exception as e:
            self._json({"error": str(e)}, 500)

    def _post_generar_ia(self):
        """Flujo IA: cada ángulo trae modo = real | ia_generar | ia_editar.
          - real        -> idéntico a /generar (gen4 sobre foto real)
          - ia_generar  -> Nano Banana crea el fondo, luego gen4 hace el overlay
          - ia_editar   -> Nano Banana edita el fondo a partir de fotos reales
                           (ref_imgs / autoselección), luego gen4 hace el overlay
        Cada salida final es un creativo 1080x1920 con logo+texto, servible por /img.
        REGLA DE ORO: si cualquier ángulo trae dry_run:true, ese ángulo NO llama a
        la API (solo construye el request). El CEO dispara la llamada real."""
        try:
            n = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(n) or b"{}")
            angulos = payload.get("angulos") or []
            res = []
            for cfg in angulos:
                modo = cfg.get("modo", "real")
                try:
                    if modo == "real":
                        ruta, bot = generar.render_uno(cfg, BIB, SAL)
                        res.append({"angulo": cfg.get("angulo"), "modo": "real",
                                    "out": os.path.basename(ruta), "ok": bot <= 1510})
                    elif modo in ("ia_generar", "ia_editar"):
                        res.append(_generar_un_creativo_ia(cfg))
                    else:
                        res.append({"angulo": cfg.get("angulo"),
                                    "error": "modo desconocido: %s" % modo})
                except Exception as e:
                    res.append({"angulo": cfg.get("angulo"), "modo": modo,
                                "error": str(e)})
            ok = sum(1 for r in res if r.get("ok"))
            print("[generar_ia] %d/%d creativos" % (ok, len(angulos)), flush=True)
            self._json({"creativos": res})
        except Exception as e:
            self._json({"error": str(e)}, 500)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    print("🎨 Creativos server en http://127.0.0.1:%d  (biblioteca: %d fotos)"
          % (PORT, len(listar_biblioteca())), flush=True)
    ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
