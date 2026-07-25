#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""nano_banana.py — Generación/edición de imágenes con Nano Banana 2
(Google Gemini · modelo `gemini-3-pro-image-preview`) para Playa Blanca.

Dos modos:
  • GENERAR  → solo prompt de texto (fondo nuevo desde cero).
  • EDICIÓN  → prompt + 1..3 fotos reales de referencia (inlineData base64)
               para limpiar logos, reencuadrar a 9:16, mejorar luz, etc.,
               manteniendo grounding en la propiedad real.

La GEMINI_API_KEY se lee de  ../.env  (raíz del proyecto Playa Blanca),
sin dependencias externas (parser propio). Solo requiere `requests`.

────────────────────────────────────────────────────────────────────────
REGLA DE ORO (no la rompas): este módulo NO debe enviarse a la API durante
build/verificación. Cada imagen cuesta dinero. Para probar:
    python3 nano_banana.py --dry      # construye el request y lo IMPRIME
    python3 -c "import nano_banana"    # valida import
La única llamada real ocurre cuando el CEO pulse "Generar" en su app.
────────────────────────────────────────────────────────────────────────

API pública del módulo
----------------------
  generar_fondo(prompt, ref_paths=[], out_path=None, aspect="9:16",
                api_key=None, timeout=120, dry_run=False) -> dict
      → {ok, mode, out_path, bytes, ...}  o  {ok:False, error, ...}

  elegir_refs(angulo, n=2, fotos_dir=None) -> list[str]
      → rutas absolutas de 1..3 fotos de fotos_proyecto/a para grounding.

  build_request(prompt, ref_paths=[], aspect="9:16") -> dict
      → payload JSON exacto que se enviaría (usado por el dry-run).

  cargar_api_key(env_path=None) -> str | None
"""
from __future__ import annotations
import os
import sys
import json
import base64
import glob
import argparse

# ── Rutas base ────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))                 # .../motor_creativos
PROYECTO = os.path.dirname(BASE)                                   # .../Playa Blanca
ENV_PATH = os.path.join(PROYECTO, ".env")
FOTOS_DIR = os.path.join(PROYECTO, "fotos_proyecto", "a")          # 109 fotos reales

# ── Modelo / endpoint Nano Banana 2 ──────────────────────────────────────
MODEL = "gemini-3-pro-image-preview"
ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"{MODEL}:generateContent"
)

_IMG_EXTS = (".jpg", ".jpeg", ".png", ".webp")
_MIME = {
    ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".png": "image/png", ".webp": "image/webp",
}


# ── .env loader (sin python-dotenv) ──────────────────────────────────────
def cargar_api_key(env_path: str | None = None) -> str | None:
    """Lee GEMINI_API_KEY de .env (o del entorno como fallback).
    Soporta comillas y comentarios. Devuelve None si no la encuentra."""
    val = os.environ.get("GEMINI_API_KEY")
    if val:
        return val.strip()
    path = env_path or ENV_PATH
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                if k.strip() == "GEMINI_API_KEY":
                    v = v.strip().strip('"').strip("'")
                    return v or None
    except FileNotFoundError:
        return None
    return None


# ── Selección de fotos de referencia (grounding) ──────────────────────────
# Mapa ángulo → palabras clave que aparecen en nombres / orden de preferencia.
# Como las 109 fotos están numeradas (1.jpg, 2.jpg, ...) sin semántica en el
# nombre, el selector es determinista por ángulo: reparte el set en bloques
# para que cada ángulo tome fotos distintas y reproducibles. Si en el futuro
# se renombran las fotos con palabras (playa, lobby, piscina...), el filtro
# por keyword se activa solo.
_ANGULO_KEYWORDS = {
    "playa":        ["playa", "beach", "mar", "arena", "ocean"],
    "laguna":       ["laguna", "lagoon", "agua", "lake"],
    "piscina":      ["piscina", "pool", "alberca"],
    "amenidades":   ["amenidad", "amenity", "gym", "spa", "club"],
    "interior":     ["interior", "sala", "cocina", "living", "room", "depto", "apto"],
    "vista":        ["vista", "view", "balcon", "terraza", "balcony", "rooftop"],
    "atardecer":    ["atardecer", "sunset", "golden", "dusk"],
    "aereo":        ["aereo", "aerial", "drone", "dron", "fachada", "facade"],
    "lifestyle":    ["lifestyle", "familia", "family", "gente", "people"],
    "inversion":    ["fachada", "facade", "exterior", "torre", "edificio", "building"],
}


def _listar_fotos(fotos_dir: str) -> list[str]:
    out = []
    if not os.path.isdir(fotos_dir):
        return out
    for p in sorted(glob.glob(os.path.join(fotos_dir, "*"))):
        b = os.path.basename(p)
        if b.startswith("._") or b.startswith("."):
            continue
        if p.lower().endswith(_IMG_EXTS):
            out.append(p)
    return out


def elegir_refs(angulo: str, n: int = 2, fotos_dir: str | None = None) -> list[str]:
    """Devuelve 1..3 rutas absolutas de fotos reales para anclar el modelo
    a la propiedad. Determinista: el mismo ángulo siempre da las mismas fotos.

    1) Si los nombres contienen keywords del ángulo, filtra por ellas.
    2) Si no (caso actual: fotos numeradas), reparte el set en un bloque
       distinto por ángulo, vía hash estable del nombre del ángulo.
    """
    n = max(1, min(3, int(n)))
    fotos = _listar_fotos(fotos_dir or FOTOS_DIR)
    if not fotos:
        return []

    key = (angulo or "").strip().lower()

    # 1) Filtro por keyword si los nombres lo permiten
    kws = []
    for ang, words in _ANGULO_KEYWORDS.items():
        if ang in key:
            kws = words
            break
    if not kws:  # también acepta que el ángulo libre traiga su propia palabra
        kws = [w for w in key.replace("-", " ").split() if len(w) > 3]
    if kws:
        match = [p for p in fotos if any(w in os.path.basename(p).lower() for w in kws)]
        if match:
            return match[:n]

    # 2) Reparto determinista por ángulo (fotos numeradas sin semántica)
    seed = sum(ord(c) for c in key) if key else 0
    start = seed % len(fotos)
    # paso amplio para que ángulos contiguos no colisionen en las mismas fotos
    step = max(1, len(fotos) // max(n, 1))
    picked, seen = [], set()
    for i in range(n):
        idx = (start + i * step) % len(fotos)
        # evita duplicados si el set es pequeño
        while idx in seen and len(seen) < len(fotos):
            idx = (idx + 1) % len(fotos)
        seen.add(idx)
        picked.append(fotos[idx])
    return picked


# ── Construcción del request ──────────────────────────────────────────────
def _foto_a_inline(path: str) -> dict:
    """Lee una foto y la devuelve como part inlineData (base64)."""
    ext = os.path.splitext(path)[1].lower()
    mime = _MIME.get(ext, "image/jpeg")
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return {"inlineData": {"mimeType": mime, "data": b64}}


def _aspect_hint(aspect: str) -> str:
    """Refuerza el aspect ratio en el prompt (el endpoint no expone un campo
    de aspect dedicado en esta preview; se ancla por texto)."""
    aspect = (aspect or "9:16").strip()
    nombres = {
        "9:16": "vertical 9:16 (1080x1920, formato Meta Stories/Reels)",
        "1:1": "square 1:1",
        "4:5": "portrait 4:5",
        "16:9": "landscape 16:9",
    }
    return nombres.get(aspect, f"aspect ratio {aspect}")


def build_request(prompt: str, ref_paths: list[str] | None = None,
                  aspect: str = "9:16") -> dict:
    """Arma el payload JSON exacto del POST a generateContent.

    parts = [ {text: PROMPT (+ hint de aspecto)} , {inlineData: foto1}, ... ]
    No lee la API key (eso lo hace el caller); puro armado de body.
    """
    ref_paths = ref_paths or []
    full_prompt = (
        f"{prompt.strip()}\n\n"
        f"Output an image in {_aspect_hint(aspect)}."
    )
    parts: list[dict] = [{"text": full_prompt}]
    for p in ref_paths:
        parts.append(_foto_a_inline(p))
    return {
        "contents": [{"parts": parts}],
        "generationConfig": {"responseModalities": ["IMAGE"]},
    }


def _extraer_imagen(data: dict) -> tuple[bytes | None, str]:
    """Saca el primer inlineData (PNG base64) de la respuesta.
    Devuelve (bytes, mime) o (None, '') si no hay imagen."""
    try:
        cands = data.get("candidates") or []
        for c in cands:
            for part in (c.get("content", {}).get("parts") or []):
                inline = part.get("inlineData") or part.get("inline_data")
                if inline and inline.get("data"):
                    mime = inline.get("mimeType") or inline.get("mime_type") or "image/png"
                    return base64.b64decode(inline["data"]), mime
    except Exception:
        pass
    return None, ""


# ── Función principal ─────────────────────────────────────────────────────
def generar_fondo(prompt: str,
                  ref_paths: list[str] | None = None,
                  out_path: str | None = None,
                  aspect: str = "9:16",
                  api_key: str | None = None,
                  timeout: int = 120,
                  dry_run: bool = False) -> dict:
    """Genera (o edita) una imagen con Nano Banana 2 y la guarda como PNG.

    MODO GENERAR : ref_paths vacío → fondo nuevo solo desde el prompt.
    MODO EDICIÓN : ref_paths con 1..3 fotos reales → limpiar logo / reencuadrar
                   a 9:16 / mejorar luz, anclado a la propiedad real.

    Args:
        prompt: instrucción de texto (es/en).
        ref_paths: lista de rutas a fotos de referencia (opcional, máx 3 útiles).
        out_path: dónde guardar el PNG. Si None → motor_creativos/salidas/nano_<n>.png
        aspect: "9:16" (default), "1:1", "4:5", "16:9".
        api_key: si None se lee de .env.
        timeout: segundos para la llamada HTTP.
        dry_run: si True NO envía nada; devuelve el request construido.

    Returns:
        dict. Éxito: {ok:True, mode, out_path, bytes, mime, parts, refs}.
        Dry-run: {ok:True, dry_run:True, request, endpoint, ...} (sin enviar).
        Error:   {ok:False, error, ...}.
    """
    ref_paths = list(ref_paths or [])
    mode = "edicion" if ref_paths else "generar"

    if not (prompt and prompt.strip()):
        return {"ok": False, "error": "prompt vacío", "mode": mode}

    # Validar que las fotos de referencia existen antes de leerlas
    faltan = [p for p in ref_paths if not os.path.isfile(p)]
    if faltan:
        return {"ok": False, "mode": mode,
                "error": f"fotos de referencia no encontradas: {faltan}"}
    if len(ref_paths) > 3:
        # el modelo se ancla mejor con <=3; recortamos avisando
        ref_paths = ref_paths[:3]

    # Armar request (esto sí puede leer las fotos a base64)
    try:
        payload = build_request(prompt, ref_paths, aspect)
    except Exception as e:
        return {"ok": False, "mode": mode, "error": f"no se pudo armar el request: {e}"}

    out_path = out_path or os.path.join(BASE, "salidas", f"nano_{abs(hash(prompt)) % 10000}.png")

    # ── DRY-RUN: construir pero NO enviar (regla de oro) ──────────────
    if dry_run:
        # versión imprimible: oculta el base64 de las fotos (pesado)
        printable = {
            "contents": [{
                "parts": [
                    (p if "text" in p
                     else {"inlineData": {
                         "mimeType": p["inlineData"]["mimeType"],
                         "data": f"<base64 {len(p['inlineData']['data'])} chars omitido>"}})
                    for p in payload["contents"][0]["parts"]
                ]
            }],
            "generationConfig": payload["generationConfig"],
        }
        return {
            "ok": True, "dry_run": True, "mode": mode,
            "endpoint": ENDPOINT, "model": MODEL,
            "out_path": out_path, "aspect": aspect,
            "refs": ref_paths,
            "parts": len(payload["contents"][0]["parts"]),
            "request": printable,
        }

    # ── Llamada REAL (solo cuando el CEO pulse Generar) ───────────────
    key = api_key or cargar_api_key()
    if not key:
        return {"ok": False, "mode": mode,
                "error": "GEMINI_API_KEY no encontrada (.env ni entorno)"}

    try:
        import requests
    except ImportError:
        return {"ok": False, "mode": mode,
                "error": "falta la librería 'requests' (pip install requests)"}

    headers = {"X-goog-api-key": key, "Content-Type": "application/json"}
    try:
        resp = requests.post(ENDPOINT, headers=headers, json=payload, timeout=timeout)
    except requests.exceptions.Timeout:
        return {"ok": False, "mode": mode, "error": f"timeout tras {timeout}s"}
    except requests.exceptions.RequestException as e:
        return {"ok": False, "mode": mode, "error": f"error de red: {e}"}

    # Errores de cuota / billing / auth
    if resp.status_code == 429:
        return {"ok": False, "mode": mode, "status": 429,
                "error": "límite de cuota / rate-limit (429)", "body": resp.text[:500]}
    if resp.status_code in (401, 403):
        return {"ok": False, "mode": mode, "status": resp.status_code,
                "error": "auth/billing rechazado (revisa API key o facturación)",
                "body": resp.text[:500]}
    if resp.status_code != 200:
        return {"ok": False, "mode": mode, "status": resp.status_code,
                "error": f"HTTP {resp.status_code}", "body": resp.text[:500]}

    try:
        data = resp.json()
    except ValueError:
        return {"ok": False, "mode": mode, "error": "respuesta no es JSON",
                "body": resp.text[:500]}

    # Bloqueo por safety / prompt feedback sin candidatos
    if not data.get("candidates"):
        fb = data.get("promptFeedback") or {}
        return {"ok": False, "mode": mode,
                "error": "sin candidatos (posible bloqueo de safety)",
                "promptFeedback": fb, "body": str(data)[:500]}

    img_bytes, mime = _extraer_imagen(data)
    if not img_bytes:
        return {"ok": False, "mode": mode,
                "error": "la respuesta no contiene imagen (solo texto?)",
                "body": str(data)[:500]}

    # Guardar PNG
    try:
        os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(img_bytes)
    except OSError as e:
        return {"ok": False, "mode": mode, "error": f"no se pudo guardar: {e}"}

    return {
        "ok": True, "mode": mode, "out_path": out_path,
        "bytes": len(img_bytes), "mime": mime,
        "parts": len(payload["contents"][0]["parts"]),
        "refs": ref_paths,
    }


# ── CLI dry-run (NUNCA envía) ─────────────────────────────────────────────
def _main(argv=None):
    ap = argparse.ArgumentParser(
        description="Nano Banana 2 — generar/editar fondos Playa Blanca.")
    ap.add_argument("--dry", action="store_true",
                    help="Construye el request y lo imprime SIN enviarlo (regla de oro).")
    ap.add_argument("--prompt", default=(
        "Cinematic luxury beachfront real estate in Panama at golden hour, "
        "turquoise lagoon, modern residences, premium architectural photography."))
    ap.add_argument("--angulo", default="playa",
                    help="Ángulo para auto-elegir fotos de referencia.")
    ap.add_argument("--refs", nargs="*", default=None,
                    help="Rutas de fotos de referencia (override del auto-selector).")
    ap.add_argument("--n", type=int, default=2, help="Nº de fotos de referencia auto.")
    ap.add_argument("--aspect", default="9:16")
    ap.add_argument("--out", default=None)
    args = ap.parse_args(argv)

    refs = args.refs if args.refs is not None else elegir_refs(args.angulo, args.n)

    if not args.dry:
        print("Sin --dry no se hace nada (la llamada real cuesta dinero del CEO).",
              file=sys.stderr)
        print("Usa:  python3 nano_banana.py --dry   para inspeccionar el request.",
              file=sys.stderr)
        return 2

    res = generar_fondo(args.prompt, ref_paths=refs, out_path=args.out,
                        aspect=args.aspect, dry_run=True)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    print(f"\n[refs elegidas para '{args.angulo}']:", file=sys.stderr)
    for r in refs:
        print("  -", r, file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
