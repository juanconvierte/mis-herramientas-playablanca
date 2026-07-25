# HANDOFF — Fix landings por Clarity + CAPI PageView (21-jul-2026)

> Para retomar en chat limpio. Estado: **TODO desplegado y vivo.** Solo quedan tareas de Juan + medición.

---

## 1. Qué se hizo (resumen 1 línea)
Se diagnosticó con Microsoft Clarity por qué las landings no convertían, se aplicaron **15 arreglos** (12 UX + 3 de tracking CAPI) a **AMBAS** landings (Colombia y Panamá), se verificaron y se **desplegaron a producción**. El filtro de calidad del formulario (3 pasos) quedó **intacto**.

## 2. Diagnóstico (data Clarity, proyecto `xlby6ydjfh`, 3 días)
- Global engañoso: scroll 13.7%, activo 25s, dead-clicks 12.2%, script-errors 2.86%, 84% móvil, 11% bots.
- **Split real (lo que cambió el diagnóstico):**
  - **COLOMBIA** (~90% del tráfico): scroll **11.9%**, dead-clicks 201, script-errors 9 → aquí estaban TODOS los problemas.
  - **PANAMÁ**: scroll 60.7% = **ARTEFACTO de n=7-10 sesiones** (equipo/desktop, sin pauta). El primer viewport es **CÓDIGO IDÉNTICO** en ambas (verificado por diff). **Panamá NO es benchmark** — se corrigió ese mito.
- Causa raíz: **fricción absoluta del primer viewport de Colombia** sobre tráfico pago móvil frío. El form estaba a 3 secciones (~20% de profundidad) → la sesión mediana nunca lo veía. Además botones falsos (dead-clicks) y el form se rompía en el webview de Instagram/Facebook (~15%).

## 3. Los 15 arreglos (aplicados a AMBAS landings)
**Comportamiento / UX:**
- **A** — Storage a prueba de fallos: helpers `lsSet/lsGet` (try/catch) + todos los `localStorage.*` ruteados por ellos. *(El fallo de storage en webview IG/FB abortaba el JS y MATABA el form → 0 leads.)*
- **B** — Handler de submit en try/catch: siempre reactiva el botón + garantiza HubSpot+CAPI+redirect (no más "lead fantasma / botón congelado").
- **C** — Fallback de `fbclid` desde la URL para CAPI (protege match en webview).
- **D** — "Descubre": `<div>` inerte → `<a href="#contacto">` con área de toque ≥44px.
- **E** — 6 tarjetas de propiedad → `<a href="#contacto">` (el tap abre el form).
- **F** — Hero más corto: `min-height 92svh→80svh`, padding `6.5rem→5rem` (asoma la siguiente sección).
- **G** — 2ª imagen del split `eager`→`lazy` (acelera el LCP del hero).
- **H** — Failsafe de `.reveal`: `setTimeout 1.2s` + guard `IntersectionObserver` (evita página en blanco bajo el hero si el observer falla).
- **I** — Quitar hover-lift de tarjetas que NO son enlaces (`.why-card`).
- **J** — `window.onerror` → `clarity('set','js_error',...)` (diagnostica los script-errors residuales).
- **K** — **4 chips del Paso 1 EN EL HERO** (Retiro / Segunda residencia / Vivir todo el año / Vacaciones familiares): tap preselecciona el option-card del Paso 1 + `scrollIntoView('#contacto')`. **Filtro de 3 pasos INTACTO** (todavía hay que responder plazo + presupuesto para ser lead).
- **L** — Tap en la pista de los sliders del simulador (móvil salta al valor).

**Tracking / Facebook (fix "cobertura CAPI 0%"):**
- **CAPI-1** — `api/conversion.js`: `ALLOWED_EVENTS += 'PageView'`.
- **CAPI-2** — head: `window.__pbPvId` generado + el píxel PageView lleva `{eventID: __pbPvId}`.
- **CAPI-3** — `sendPageViewCAPI()` manda PageView a `/api/conversion` con el MISMO `event_id` → Meta deduplica → sube cobertura.
- Contexto: el píxel disparaba PageView (1,542/7d) pero CAPI solo mandaba Lead → cobertura 0%. Lead ya estaba maxeado (EMQ 9.3); esto es el **volumen PageView**. Sube gradual (server-side, promedio 7 días).

## 4. Compliance VIVIENDA (Meta HOUSING)
Verificado: **cero** términos prohibidos introducidos (rentabilidad/plusvalía/se paga sola/escrow/etc., ni edad explícita). `rentabilidad` aparece solo en 2 disclaimers pre-existentes (no tocados). Colombia = "tú", Panamá = "usted" (hero de Panamá NO reescrito).

## 5. Estado de despliegue — ✅ VIVO
| Landing | Proyecto Vercel | Dominio | Pixel | Estado |
|---|---|---|---|---|
| 🇨🇴 Colombia | `landing-colombia-full` | landing-colombia-full.vercel.app | 1923056805076909 | ✅ 200 |
| 🇵🇦 Panamá | `landing-panama` | panama.playablancaresidences.com | 2195180334399669 | ✅ 200 |

Verificado en vivo: `hero-chip`, `__pbPvId`, `80svh`, `sendPageViewCAPI` presentes; `/api/conversion` 200; voz correcta; pixels correctos. Deploy Panamá: `dpl_2Z3Sw4mdb4a6cmiMkqm9fLoiFCTK`.

## 6. Archivos tocados
- `landing-colombia-full/index.html` (2278→2394 líneas) + `landing-colombia-full/api/conversion.js`
- `web-panama-LIVE/index.html` + `web-panama-LIVE/api/conversion.js`
- **Backups (para revertir):** `_ARCHIVO/index-colombia-PRE-FIX-clarity-20jul.html`, `_ARCHIVO/index-panama-PRE-FIX-clarity-20jul.html`, `_ARCHIVO/conversion-panama-PRE-FIX-clarity-20jul.js`. Reversión = re-deploy del backup.

## 7. PENDIENTE (no-deploy — tareas de Juan + tiempo)
1. 🔴 **Rotar token Clarity** — se pegó en el chat (`CLARITY_DATA_EXPORT_TOKEN` en `.env`, jti `d3410fbd`). Generar uno nuevo en Clarity → Settings → Data Export y cambiarlo en `.env`.
2. 🧪 **QA del form DENTRO del webview de Instagram/Facebook** (ambas): completar los 3 pasos → confirmar lead a HubSpot + redirect `/gracias`. Es el ambiente (~15%) donde antes rompía.
3. ⏳ **Medir en 3-5 días:** re-jalar Clarity (sobre `real_sessions=343`, segmentar in-app IG/FB vs ChromeMobile) + cobertura CAPI en Meta Events Manager. **Metas:** scroll 11.9→25-35%+, dead-clicks 12.2→<3%, script-errors→≈0 propios, cobertura CAPI 0→75%+.

## 8. Decisión de negocio registrada (importante)
Juan validó: **el filtro de calidad NO es el scroll, son las 3 preguntas del form** (objetivo + plazo + presupuesto ≥$190K). Los chips NO diluyen calidad — solo adelantan el Paso 1; incompleto ≠ lead (Lead solo se dispara al completar los 3 pasos). Los chips + form arriba **suben conversión SIN degradar calidad**. Se decidió NO reforzar el filtro por ahora → "probar y medir es la clave". Si la data muestra baja calidad, la palanca es endurecer las preguntas del form (no esconderlo).

## 9. Cómo verificar (comandos)
```bash
# páginas vivas
curl -s -o /dev/null -w "%{http_code}" https://panama.playablancaresidences.com
curl -s -o /dev/null -w "%{http_code}" https://landing-colombia-full.vercel.app
# fix presente
curl -s https://landing-colombia-full.vercel.app | grep -c "sendPageViewCAPI"
# Clarity (token en .env)
curl -s -H "Authorization: Bearer $CLARITY_DATA_EXPORT_TOKEN" \
  "https://www.clarity.ms/export-data/api/v1/project-live-insights?numOfDays=3"
```
