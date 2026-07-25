# 🎯 Estilo Ganador DR — Biblioteca de prompts para Nano Banana 2

Anuncios de respuesta directa (DR) para **Playa Blanca Residences**, listos para generar con **Nano Banana 2 (Gemini 3 Pro Image)**.

> **Entregable:** `prompts_estilo_ganador.json` → array de **12 ángulos**, cada uno con titular, bullets, CTA, sujeto y el **prompt completo en inglés** que renderiza el anuncio terminado (con el texto del anuncio EN ESPAÑOL dentro de la imagen).
>
> ⚠️ Estos prompts **NO** generan imágenes por sí solos. Tú decides cuándo enviarlos al modelo (cada generación cuesta dinero). Aquí solo está el texto de los prompts.

---

## 🧪 La fórmula del estilo (anatomía del anuncio)

Cada creativo replica el patrón ganador de infoproducto/ecommerce, adaptado a inmobiliaria de lujo:

| Zona | Elemento | Regla |
|------|----------|-------|
| **Formato** | Vertical **9:16** (también sirve 1:1 si recortas centrado) | Fondo cinematográfico, alto contraste |
| **Arriba** | **TITULAR** grande en mayúsculas, sans condensada bold | UNA palabra clave resaltada en **cian/azul** (acento de marca) |
| **Centro** | **SUJETO**: el avatar real (pareja madura, familia, inversionista, jubilado, latino) | Expresión emocional que matchea el mensaje |
| **Medio-bajo** | **2-3 BULLETS** con íconos ✅ ⚡ 🚀 | Beneficios concretos, líneas cortas |
| **Abajo** | **BOTÓN CTA** de color con verbo de acción | Cian→azul, texto blanco bold |
| **Esquina** | **LOGO** Playa Blanca pequeño | Espacio reservado limpio |
| **Look** | Iluminación tipo estudio/DR, fotorrealista | Tinte azul cobalto/navy unificador, elementos UI sutiles de fondo |

### Gancho del titular (qué dispara la atención)
Dolor, deseo, pregunta, prueba social, FOMO, anclaje de precio o identidad. Siempre **fuerte y emocional** — pero honesto.

### Color de acento: cian / azul / turquesa (NO dorado)
Para mantener coherencia con la identidad de marca del motor (`README.md`: azul cobalto + navy + blanco, **nada de dorado**), el color de acento del titular y el CTA es **cian/azul/turquesa** (resuena con la laguna). Esto unifica esta biblioteca con el resto del sistema de creativos.

---

## 📐 Los 12 ángulos

| # | Ángulo | Objetivo | Titular (keyword en negrita) | Avatar |
|---|--------|----------|------------------------------|--------|
| 1 | Prueba social / autoridad de masas | formulario | 3,500 FAMILIAS YA VIVEN FRENTE AL **MAR** | Pareja madura |
| 2 | FOMO / preventa | formulario | PRECIOS DE PREVENTA QUE NO **VOLVERÁN** | Inversionista |
| 3 | Aspiración / estilo de vida | web | IMAGINA DESPERTAR ASÍ CADA **MAÑANA** | Mujer 40s al amanecer |
| 4 | Autoridad / 23 años | formulario | 23 AÑOS CONSTRUYENDO HOGARES FRENTE AL **PACÍFICO** | Familia multigeneracional |
| 5 | Anclaje de precio | formulario | VIVIR FRENTE AL MAR CUESTA MENOS DE LO QUE **CREES** | Pareja joven |
| 6 | Sin banco / directo | formulario | COMPRA SIN BANCO. PLANES DIRECTOS CON EL **DESARROLLADOR** | Hombre con llaves |
| 7 | Identidad / comprador colombiano | web | COLOMBIANO: TU PRÓXIMA CASA TIENE PLAYA EN **PANAMÁ** | Pareja en mirador |
| 8 | Urgencia de vida / retiro | formulario | TU RETIRO MERECE PLAYA, NO SALA DE **ESPERA** | Jubilados vitales |
| 9 | Contraste laguna / diferencial | web | LA LAGUNA DE AGUA SALADA MÁS GRANDE DE LA **REGIÓN** | Familia en kayak |
| 10 | Seguridad jurídica / escrow | formulario | TÍTULO A TU NOMBRE, PAGOS EN **ESCROW** | Pareja firmando |
| 11 | Amenidades premium | web | SPA, GOLF Y CLUB DE PLAYA A UN PASO DE TU **PUERTA** | Grupo en club de playa |
| 12 | Pregunta-gancho / postergación | formulario | ¿CUÁNTOS VERANOS MÁS VAS A DEJAR **PASAR**? | Persona reflexiva |

Sujetos, escenas y emociones **variados**: amanecer, atardecer, interiores, terraza, laguna, club, oficina; alegría, plenitud, decisión, alivio, reflexión.

---

## ✅ Cumplimiento (Meta — categoría VIVIENDA + claims)

Todo el copy es **compliant**:

- ❌ Sin "rentabilidad/plusvalía garantizada", "inversión protegida/segura", "se paga sola", "ganancia asegurada" ni "garantizado" estilo infoproducto.
- ❌ Sin segmentación ni lenguaje discriminatorio por edad, género u otra categoría protegida en el copy del anuncio. (Los avatares son recursos creativos, **no** criterios de exclusión de audiencia.)
- ✅ Diferenciales **reales y verificables**: 1.5 km de playa privada, laguna de agua salada, 90 hectáreas, 23 años, 1,500+ unidades, 3,500+ familias, planes sin banco, título a tu nombre, escrow, Visa Pensionado, desde $193,912.
- ✅ Ganchos fuertes pero **honestos**: deseo, urgencia de vida, prueba social y FOMO de preventa — sin prometer retornos financieros.

> Nota: el precio "$193,912" y las cifras (1,500+ / 3,500+ / 23 años) deben coincidir con los datos oficiales vigentes antes de publicar. Ajusta si cambian.

---

## 🔌 Conexión con la app — sección futura "Estudio de Anuncios estilo DR"

Esta biblioteca es la semilla de un módulo dentro del sistema de creativos / dashboard:

1. **Selector de ángulo** — el usuario elige uno de los 12 ángulos (o varios) desde la UI del dashboard.
2. **Emparejado con foto real** — opcionalmente, se ancla a una de las 109 fotos reales en `fotos_proyecto/a/` (ej. `hero-lagoon.jpg` para el ángulo de laguna, `spa.jpg` para amenidades, `terrazas-villas.png` para aspiración) pasándola como imagen de referencia a Nano Banana 2 para máxima fidelidad del lugar.
3. **Render bajo demanda** — al pulsar "Generar", la app envía `prompt_nanobanana` al modelo (Gemini 3 Pro Image). El gasto ocurre **solo** en ese momento, controlado por el usuario.
4. **Variantes A/B** — se generan 2-3 variantes por ángulo (cambiando sujeto/escena/keyword) para testear en Meta.
5. **Consistencia de marca** — el estilo (tinte azul cobalto/navy, acento cian, logo, zona segura central) está embebido en cada prompt, alineado con las 5 reglas de oro del `README.md` del motor.
6. **Salida** — PNG 9:16 listo para subir como creativo a las campañas de lead-gen (`act_852024635148139`).

### Cómo usar manualmente (sin app)
1. Abre `prompts_estilo_ganador.json`.
2. Copia el campo `prompt_nanobanana` del ángulo que quieras.
3. (Opcional) Adjunta la foto real correspondiente como referencia.
4. Pégalo en Nano Banana 2 / Gemini 3 Pro Image y genera.
5. Revisa que el texto en español salió nítido y sin errores; reintenta si hace falta.

---

*Esta biblioteca no consume crédito de generación de imágenes: es únicamente texto de prompts. El gasto ocurre cuando tú decides renderizar.*
