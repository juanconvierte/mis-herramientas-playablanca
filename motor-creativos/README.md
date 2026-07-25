# 🏖️ PLAYA BLANCA — Sistema Automático de Anuncios Meta Ads

> Sistema completo para generar anuncios inmobiliarios de lujo (1080×1920) con identidad de marca azul, tipografía premium, zona segura central y checklists elegantes — **automáticamente desde un ZIP de fotos**.

Este paquete contiene TODO lo necesario para que una app/agente replique exactamente el estilo de Playa Blanca.

---

## 📦 Contenido del paquete

| Archivo | Para qué sirve |
|---------|----------------|
| `README.md` | Este documento (visión general) |
| `APP_INSTRUCTIONS.md` | **El cerebro**: instrucciones para que un agente IA sea "tú" |
| `PROMPT_PARA_APPS.md` | Prompt listo para pegar en apps de imágenes (Midjourney, DALL-E, etc.) |
| `ESPECIFICACIONES_TECNICAS.md` | Cada medida, color, fuente y regla exacta |
| `engine/` | El motor Python real (kit3.py, gen4.py, designkit.py) |
| `fonts/` | Las fuentes premium (Fraunces, Archivo) |
| `assets/` | Logo oficial blanco y navy |
| `ejemplos_config/` | JSONs de ejemplo de los 58 anuncios ya hechos |

---

## 🚀 Flujo de trabajo (lo que hace la app)

```
1. Usuario sube ZIP con fotos del proyecto
2. App descomprime y corrige rotación EXIF (fotos DSC vienen rotadas)
3. App mapea cada foto a su mejor ángulo (torre→inversión, pareja→retiro, etc.)
4. Usuario elige ángulos (o la app sugiere los mejores)
5. App genera cada anuncio:
   - Aplica tinte azul de marca FUERTE sobre toda la imagen
   - Coloca texto en ZONA SEGURA CENTRAL (funciona en 9:16 y 1:1)
   - Tipografía Fraunces (titular) + Archivo (resto)
   - Logo oficial + badge + precio + checklist + CTA
6. App exporta PNG 1080×1920 listo para Meta Ads
```

---

## 🎨 Las 5 reglas de oro (lo que hace que se vea PRO)

1. **TINTE AZUL DE MARCA** — capa azul cobalto/navy FUERTE y pareja sobre TODA la imagen (no un velo tímido). Esto unifica todo y hace que el texto blanco resalte.

2. **ZONA SEGURA CENTRAL** — todo el texto vive en el cuadrado central (y=420 a y=1500). Así funciona en historia 9:16 Y en feed 1:1 sin cortarse.

3. **TIPOGRAFÍA PREMIUM** — Fraunces (serif de lujo) para titulares, Archivo (sans geométrica) para kickers/precio/CTA. Nada de fuentes genéricas.

4. **LOGO OFICIAL + JERARQUÍA** — logo real de la marca, eyebrow con líneas finas, titular grande, sublínea, precio en píldora, trust, CTA. Siempre en ese orden.

5. **PALETA OBLIGATORIA** — azul cobalto + navy + blanco. NADA de dorado. URL siempre `panama.playablancaresidences.com`.

---

## 💡 Cómo empezar

Si tienes un agente IA (como Claude, GPT, etc.) con capacidad de ejecutar código:
1. Dale el archivo `APP_INSTRUCTIONS.md` como system prompt
2. Sube el `engine/` y las `fonts/`
3. Sube tu ZIP de fotos
4. Di "genérame 10 anuncios" y listo

Si solo quieres generar imágenes con una app de IA (sin código):
1. Usa `PROMPT_PARA_APPS.md` y rellena los campos
