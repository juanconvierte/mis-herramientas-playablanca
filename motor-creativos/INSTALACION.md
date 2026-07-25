# 🔧 INSTALACIÓN — Cómo montar tu app automática

Tienes 3 caminos según tu nivel técnico. Elige el tuyo.

---

## 🟢 CAMINO 1 — El más fácil (sin programar nada)
**Usar un agente IA que ya ejecuta código (como Claude con análisis de datos)**

1. Abre una conversación con un agente IA que pueda ejecutar Python
2. Pega el contenido de `APP_INSTRUCTIONS.md` como primer mensaje
3. Sube los archivos: `engine/`, `fonts/`, `assets/`
4. Sube tu ZIP de fotos
5. Escribe: *"genérame 10 anuncios variando ángulos"*
6. El agente hace TODO y te devuelve los PNG

Esto es literalmente lo que pasó en esta conversación. 👈

---

## 🟡 CAMINO 2 — App propia con backend (para devs)
**Montar una app web donde subes ZIP y descargas anuncios**

Stack sugerido:
```
Frontend: Next.js (subida de ZIP, galería de resultados)
Backend:  Python (FastAPI) con el motor engine/
Cola:     procesa los anuncios en background
```

Endpoints mínimos:
```python
POST /upload-zip      → recibe ZIP, descomprime, corrige EXIF, mapea fotos
POST /generate        → recibe config (ángulos elegidos), corre gen4.py
GET  /results/{id}    → devuelve los PNG generados
```

El corazón ya lo tienes en `engine/`. Solo envuélvelo en la API.

### Configuración del motor
En `engine/kit3.py` y `engine/gen4.py`, reemplaza:
```python
FONTS_DIR/  →  "/ruta/real/a/fonts/"
BASE_DIR/   →  "/ruta/real/a/assets/"
```

### Dependencias
```bash
pip install pillow numpy fastapi uvicorn python-multipart
```

---

## 🔵 CAMINO 3 — Solo imágenes con IA (sin texto perfecto)
**Para Midjourney/DALL-E/Firefly**

1. Usa `PROMPT_PARA_APPS.md`
2. Rellena los campos del prompt
3. Genera la foto base con tinte azul
4. Pon el texto encima en Canva siguiendo `ESPECIFICACIONES_TECNICAS.md`

⚠️ Limitación: las IAs de imagen no ponen texto legible. Por eso el motor Python es superior para este caso.

---

## 📋 CHECKLIST DE ARCHIVOS NECESARIOS

Para que funcione necesitas:
- [ ] `engine/designkit.py` (motor base)
- [ ] `engine/kit3.py` (elementos: tinte, checklists, CTAs)
- [ ] `engine/gen4.py` (generador con medición/centrado)
- [ ] `fonts/Fraunces.ttf` + `fonts/Fraunces-Italic.ttf`
- [ ] `fonts/Archivo.ttf`
- [ ] `assets/logo_white_trim.png` + `assets/logo_navy_trim.png`
- [ ] Python 3.10+ con Pillow y numpy

---

## 🎯 PRUEBA RÁPIDA

```bash
cd PB_SISTEMA
python QUICKSTART.py tu_zip_de_fotos.zip
```

Esto descomprime, corrige y mapea tus fotos. Después configuras los ángulos y generas.

---

## ❓ PREGUNTAS FRECUENTES

**¿Puedo cambiar los colores?**
Sí, en `ESPECIFICACIONES_TECNICAS.md` están los RGB. Cambia la paleta en designkit.py.

**¿Puedo usar otras fotos / otro proyecto?**
Sí. Cambia los datos fijos en APP_INSTRUCTIONS.md (precios, trust, URL) y mete tus fotos.

**¿El tinte azul es muy fuerte/débil?**
Ajusta `veil` en la función cinematic_gradient (kit3.py). 150 = el valor actual.

**¿Cómo agrego más estilos de checklist?**
Copia una función check_* en kit3.py y modifícala. El patrón es siempre el mismo.
