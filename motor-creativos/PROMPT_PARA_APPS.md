# 🎨 PROMPT PARA APPS DE IMÁGENES (Midjourney, DALL-E, Firefly, etc.)

> Copia el prompt, rellena los campos [ENTRE CORCHETES] y pégalo en tu app de imágenes.
> NOTA: las apps de IA generan la composición pero NO ponen texto perfecto. Para texto perfecto, usa el motor Python (ver ESPECIFICACIONES_TECNICAS.md).

---

## PROMPT MAESTRO (rellénalo)

```
Luxury real estate Meta/Facebook ad, vertical 9:16 format (1080x1920px), 
text composition centered in the middle safe-zone square so nothing crops 
in feed 1:1.

BASE IMAGE: [ELIGE: white residential tower at golden hour / aerial turquoise 
saltwater lagoon with palm island / mature couple 55-65 toasting cocktails by 
infinity pool / beachfront villas aerial view / family with kids playing on 
white sand beach / premium apartment interior with blue velvet armchairs]. 
Professional DSLR photography, cinematic warm lighting, shallow depth of field, 
realistic skin tones, subject looking [confident / serene / enjoying life].

BRAND BLUE TINT: Strong, even cobalt/navy blue duotone overlay across the 
ENTIRE image (not a timid veil) — unifies the piece and makes white text pop. 
Extra reinforcement in the lower text band.

TEXT OVERLAY (centered, inside safe square, premium editorial style):
- Official "Playa Blanca" logo (palm tree icon) at top, white, discreet
- Small EYEBROW with thin lines on sides: "[TRIGGER IN CAPS, e.g. TU LEGADO FRENTE AL MAR]"
- Large SERIF HEADLINE (Fraunces font, white): "[SHORT EMOTIONAL HOOK]"
- Light sans SUBLINE (Archivo): "[benefit or location, 1.5h from capital]"
- PRICE pill with border: "Desde $[XXX,XXX] USD"
- Optional red urgency BADGE: "[ÚLTIMAS UNIDADES / RENTA EN USD / YA CONSTRUIDO]"
- Optional CHECKLIST (3-4 items) with elegant circular checks — premium, not cheap emoji
- TRUST line in wide tracking caps: "23 AÑOS · 3,500+ FAMILIAS"
- Rounded CTA button [white with navy text = best CTR / cobalt solid / outline]: "[Asegura el tuyo] →"
- Discreet URL: panama.playablancaresidences.com

MANDATORY PALETTE: cobalt blue + navy + white. NO gold whatsoever.
AESTHETIC: premium editorial like Buenaventura resort, silent luxury, lots of 
air, text always legible, direct-response but elegant. --ar 9:16 --style raw
```

---

## EJEMPLOS RELLENADOS (para que veas cómo)

### Ejemplo A — Legado
```
BASE IMAGE: family with kids playing on white sand beach, father watching, 
golden hour
EYEBROW: TU LEGADO FRENTE AL MAR
HEADLINE: Lo que les dejes, los unirá siempre
SUBLINE: Residencias frente al Pacífico, a 1.5h de la capital
PRICE: Desde $193,912 USD
TRUST: 23 AÑOS · 3,500+ FAMILIAS
CTA: Asegura el tuyo →
(sin checklist — ángulo emocional)
```

### Ejemplo B — Renta pasiva (con checklist)
```
BASE IMAGE: white residential tower at golden hour
EYEBROW: INGRESO PASIVO EN DÓLARES
HEADLINE: Tu segunda casa que se paga sola
SUBLINE: El desarrollo gestiona el alquiler vacacional
BADGE: RENTA EN USD
CHECKLIST: Renta estimada en dólares / El resort la administra / Título a tu nombre
PRICE: Desde $202,910 USD
CTA: Conoce los planes →
```

### Ejemplo C — vs Competencia (el más agresivo)
```
BASE IMAGE: aerial turquoise saltwater lagoon with palm island
EYEBROW: ÚNICA EN LA REGIÓN
HEADLINE: La laguna que Buenaventura nunca tendrá
SUBLINE: La laguna de agua salada más grande de Centroamérica y el Caribe
BADGE: ÚNICA EN LA REGIÓN
PRICE: Desde $256,100 USD
CTA: Compara y elige →
```

---

## ⚠️ LIMITACIÓN IMPORTANTE

Las apps de imágenes IA (Midjourney, DALL-E) **NO ponen texto legible y perfecto**. 
Generan la foto con el tinte y la composición, pero el texto sale deforme.

**Para texto perfecto tienes 2 opciones:**
1. Genera la foto base con IA + tinte azul, luego pon el texto en Canva/Photoshop siguiendo las medidas de ESPECIFICACIONES_TECNICAS.md
2. Usa el motor Python (engine/) que hace TODO perfecto y automático — esta es la forma real como se hicieron los 58 anuncios.
