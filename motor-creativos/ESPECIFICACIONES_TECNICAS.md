# 📐 ESPECIFICACIONES TÉCNICAS EXACTAS

> Cada medida, color, fuente y parámetro para replicar el estilo al 100%.
> Si construyes en Canva/Photoshop o programas tu propio motor, usa estos valores.

---

## LIENZO
- **Tamaño**: 1080 × 1920 px (vertical 9:16)
- **Zona segura central**: cuadrado de 1080×1080 centrado
  - `SAFE_TOP = 420` (donde empieza el área segura)
  - `SAFE_BOT = 1500` (donde termina)
  - `SAFE_CY = 960` (centro vertical)
  - **TODO el texto debe estar entre y=420 y y=1500** para no cortarse en feed 1:1

---

## PALETA DE COLORES (RGB exacto)
```
COBALT     = (24, 78, 232)    # azul cobalto principal
COBALT_D   = (12, 50, 186)    # cobalto oscuro (gradientes)
COBALT_L   = (94, 140, 255)   # cobalto claro (acentos)
NAVY       = (9, 23, 58)       # navy (texto sobre blanco)
NAVY_DEEP  = (5, 14, 38)       # navy profundo
WHITE      = (255, 255, 255)
OFFWHITE   = (238, 242, 250)
MIST       = (200, 213, 236)   # texto secundario
ICE        = (198, 218, 252)   # kickers, acentos claros

PROHIBIDO: dorado, amarillo, cualquier color cálido
```

---

## TINTE AZUL DE MARCA (lo más importante)

El degradado azul que cubre TODA la imagen. Sin esto, no se ve Playa Blanca.

```python
# Colores del tinte (3 paradas verticales)
BLUE_TOP = (16, 42, 104)   # arriba
BLUE_MID = (13, 34, 88)    # centro
BLUE_BOT = (8, 22, 60)     # abajo

# Parámetros de intensidad
veil = 150          # opacidad base FUERTE y pareja en TODA la imagen (0-255)
text_extra = 70     # refuerzo adicional en la franja del texto (abajo)
```

**Cómo aplicarlo**: una capa RGBA del tamaño completo, con el degradado azul de 3 paradas, opacidad base 150 en toda la imagen, +70 en la zona donde va el texto. Componer sobre la foto.

Si el cliente pide "más azul" → sube `veil` a 165-180.
Si pide "menos azul" → baja `veil` a 120-135.

---

## TIPOGRAFÍA

### Fuentes (variable fonts de Google Fonts)
- **Fraunces** (serif de lujo) → titulares. Ejes: opsz, wght, soft, wonk
  - Titular: `Fraunces, opsz=144, wght=580, wonk=0`
  - Itálica acento: `Fraunces-Italic, wght=500`
- **Archivo** (sans geométrica) → todo lo demás. Ejes: wght, wdth
  - Kicker: `Archivo, wght=650`
  - Precio: `Archivo, wght=720`
  - CTA: `Archivo, wght=640-680`
  - Sublínea: `Archivo, wght=330` (light)

### Tamaños típicos
```
Titular (h1):      48-62 px (según largo, line-height ~+10)
Acento itálico:    44-46 px
Sublínea:          27-29 px
Kicker/eyebrow:    22 px (tracking ancho ~6)
Precio:            33 px (el número), 25 px ("Desde")
Precio gigante:    82 px
Trust:             21-22 px (tracking ~2)
CTA:               31 px
URL:               22-23 px
Badge:             20 px (tracking ~3)
```

---

## ESTRUCTURA DEL ANUNCIO (orden vertical)

Todo centrado horizontalmente, apilado en la zona segura:

```
1. LOGO oficial (blanco)           ~380-430 px ancho
2. EYEBROW con líneas finas         "TRIGGER EN MAYÚSCULAS"
3. TITULAR (Fraunces)               "Gancho emocional"
4. [Acento itálico opcional]
5. SUBLÍNEA (Archivo light)         1-2 líneas
6. [CHECKLIST opcional]             3-4 ítems
7. Divisor fino (línea 84px)
8. PRECIO en píldora con borde      "Desde $XXX,XXX USD"
9. TRUST (mayúsculas, tracking)     "23 AÑOS · 3,500+ FAMILIAS"
10. CTA (botón redondeado)          "Acción →"
11. URL discreta                     panama.playablancaresidences.com
```

**Algoritmo de centrado**: mide la altura total del bloque, luego:
```
center = SAFE_CY + 110   # ligeramente bajo el centro
y0 = center - altura_bloque/2
# clamp para que quepa: max(SAFE_TOP+30, min(y0, SAFE_BOT - altura - 20))
```

---

## ELEMENTOS DE UI

### Píldora de precio
- Fondo: blanco 24/255 de opacidad
- Borde: (165,198,250) con 235 de opacidad, 2px
- Radio: altura/2 (pill completa)
- Altura: 72px

### Botón CTA — 3 estilos
```
BLANCO (mayor CTR):   fondo blanco sólido, texto navy (16,40,96), flecha navy
OUTLINE (premium):    fondo blanco 28/255, borde blanco 235, texto blanco
SÓLIDO (urgencia):    gradiente cobalto→cobalto_oscuro, texto blanco
Altura: 92px, radio completo, con sombra suave debajo
```

### Badge de urgencia (rojo)
- Fondo: (200,40,40) con 230 opacidad
- Texto blanco, Archivo wght=700, tracking 3
- Posición: arriba, en y=SAFE_TOP+26
- Radio completo, altura ~44px

### Eyebrow con líneas
- Texto en ICE (198,218,252), Archivo wght=650, tracking 6
- Líneas finas a ambos lados: blanco 140/255, 2px, ~54px de largo

---

## ESTILOS DE CHECKLIST

### 1. Glass card (tarjeta de cristal)
- Recorta la región del fondo, aplica blur gaussiano 18px
- Capa oscura encima: (10,26,60) con 120 opacidad
- Borde redondeado 28px, blanco 60/255
- Checks: círculo azul (110,170,255), palomita blanca

### 2. Lateral con línea de acento
- Línea vertical azul (110,170,255) a la izquierda del bloque, 5px ancho
- Checks tipo palomita SIN círculo, en color de acento
- Texto alineado a la izquierda

### 3. Dos columnas
- 2 columnas de ~380px
- Checks circulares pequeños (azul), texto al lado
- Para listas de 6 ítems (amenidades)

### 4. Checks verdes (seguridad)
- Círculo VERDE (120,210,150), palomita blanca
- El verde comunica "seguro/aprobado"
- Para ángulos de seguridad jurídica

### 5. Estadísticas grandes
- Números grandes (Archivo wght=780, ~46px): "23", "1,500+", "90"
- Etiqueta pequeña debajo: "AÑOS", "ENTREGADAS", "HECTÁREAS"
- Divisores verticales entre cada stat

### 6. Sello circular de garantía
- Círculo con borde, número grande dentro ("23")
- Texto pequeño: "AÑOS DE RESPALDO"
- Da sensación de certificación/sello oficial

---

## PROCESAMIENTO DE FOTOS

### Corrección EXIF (CRÍTICO)
Las fotos DSC vienen rotadas 90°. SIEMPRE aplica:
```python
from PIL import ImageOps
img = ImageOps.exif_transpose(Image.open(path))
```

### Recorte tipo "cover" con punto focal
```python
# Escala como CSS background-size:cover
scale = max(target_w/src_w, target_h/src_h)
# Recorta centrado en focus_x, focus_y (0.0-1.0)
# Para torres: focus_y=0.25-0.30 (muestra la parte alta)
# Para parejas: focus_y=0.22-0.30 (muestra las caras)
# Para lagunas: focus_y=0.35-0.42 (muestra el agua)
```

### Realce premium
```python
Color:      1.05   (saturación +5%)
Contraste:  1.04
Brillo:     1.02
Nitidez:    1.05
```
