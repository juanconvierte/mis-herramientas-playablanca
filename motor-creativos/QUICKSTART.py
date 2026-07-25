#!/usr/bin/env python3
"""
🚀 QUICKSTART — Flujo automático completo de Playa Blanca
=========================================================
Este script muestra cómo, desde un ZIP de fotos, generar anuncios automáticamente.

USO:
    python QUICKSTART.py mi_zip_de_fotos.zip

REQUISITOS:
    pip install pillow
    Tener las carpetas: engine/, fonts/, assets/
"""
import sys, os, zipfile, json

# ============ CONFIGURA TUS RUTAS ============
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR = os.path.join(BASE_DIR, "fonts")
ASSETS    = os.path.join(BASE_DIR, "assets")
WORK      = os.path.join(BASE_DIR, "work")
OUT       = os.path.join(BASE_DIR, "salidas")
# =============================================

def paso1_descomprimir(zip_path):
    """Descomprime el ZIP y corrige rotación EXIF."""
    from PIL import Image, ImageOps
    os.makedirs(f"{WORK}/fotos", exist_ok=True)
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(f"{WORK}/fotos")
    # Corregir rotación EXIF (fotos DSC vienen rotadas 90°)
    fixed = 0
    for root,_,files in os.walk(f"{WORK}/fotos"):
        for f in files:
            if f.lower().endswith(('.jpg','.jpeg','.png')) and not f.startswith('._'):
                p = os.path.join(root,f)
                try:
                    im = ImageOps.exif_transpose(Image.open(p))
                    im.save(p); fixed += 1
                except: pass
    print(f"✅ Descomprimido y {fixed} fotos corregidas (EXIF)")
    return f"{WORK}/fotos"

def paso2_mapear_fotos(carpeta):
    """Lista las fotos disponibles para que elijas o el agente clasifique."""
    from PIL import Image
    fotos = []
    for root,_,files in os.walk(carpeta):
        for f in sorted(files):
            if f.lower().endswith(('.jpg','.jpeg','.png')) and not f.startswith('._'):
                p = os.path.join(root,f)
                try:
                    w,h = Image.open(p).size
                    orient = "vertical" if h>w else ("horizontal" if w>h else "cuadrada")
                    fotos.append({"archivo": f, "ruta": p, "orientacion": orient, "tamaño": f"{w}x{h}"})
                except: pass
    print(f"✅ {len(fotos)} fotos encontradas:")
    for ft in fotos[:20]:
        print(f"   - {ft['archivo']:30s} {ft['orientacion']:10s} {ft['tamaño']}")
    return fotos

def paso3_generar(config_json):
    """Genera los anuncios usando el motor gen4."""
    sys.path.insert(0, f"{BASE_DIR}/engine")
    os.makedirs(OUT, exist_ok=True)
    # NOTA: el motor (gen4.py) necesita que configures FONTS_DIR y BASE_DIR adentro.
    # Aquí cargas tu config y llamas build() por cada anuncio.
    print(f"✅ Para generar: configura las rutas en engine/gen4.py y engine/kit3.py")
    print(f"   Luego: from gen4 import build; build(cfg) por cada anuncio del JSON")

if __name__ == "__main__":
    print("="*55)
    print("🏖️  PLAYA BLANCA — Generador Automático de Anuncios")
    print("="*55)
    if len(sys.argv) < 2:
        print("\nUso: python QUICKSTART.py tu_zip.zip\n")
        print("Pasos que ejecuta:")
        print("  1. Descomprime tu ZIP + corrige rotación de fotos")
        print("  2. Mapea las fotos disponibles")
        print("  3. Genera los anuncios (configura rutas primero)")
        sys.exit(0)
    zip_path = sys.argv[1]
    carpeta = paso1_descomprimir(zip_path)
    fotos = paso2_mapear_fotos(carpeta)
    print("\n👉 Siguiente: edita angulos_completos.json con tus fotos y ángulos,")
    print("   luego corre el motor. Lee APP_INSTRUCTIONS.md para el detalle.")
