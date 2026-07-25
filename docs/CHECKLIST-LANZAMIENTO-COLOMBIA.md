# ✅ CHECKLIST DE LANZAMIENTO — Landing Colombia (verificado 11-jul-2026)

Página viva: **landing-colombia-full.vercel.app** (raíz = V2). Dataset/Pixel Colombia: **1923056805076909**.

---

## 📡 TRACKING (todo verificado en código + probado en vivo)

| Item | Estado | Detalle |
|---|---|---|
| Pixel Meta | ✅ | `1923056805076909` en landing + gracias |
| API de Conversiones (CAPI) | ✅ **PROBADO** | `/api/conversion`, token en Vercel env, respondió `events_received:1` |
| Dedup Pixel ↔ CAPI | ✅ | mismo `event_id` → no cuenta doble |
| Advanced Matching | ✅ | email, teléfono y nombre hasheados (SHA-256) en el CAPI |
| Value + Currency (ROAS) | ✅ | cada Lead manda `value` (según presupuesto) + `USD` → permite optimizar por valor |

## 🎯 EVENTOS DEL EMBUDO

| Evento | Dónde se dispara | Canal |
|---|---|---|
| PageView | landing + gracias | pixel |
| ViewContent | al llegar al paso 3 del form | pixel |
| **Lead** | al ENVIAR el formulario (landing) | **pixel + CAPI** (el más confiable) |
| **CompleteRegistration** | en la página de **gracias** | pixel |
| ScrollDepth50/75, TYPageEngaged30/60 | señales de engagement | pixel custom |

**👉 El evento de conversión en la página de GRACIAS = `CompleteRegistration`.**

**👉 Para OPTIMIZAR tu campaña usa el evento `Lead`** (no CompleteRegistration): se dispara al enviar el form, lo respaldan Pixel + CAPI (server-side = no se pierde), y lleva value+currency. Es tu conversión principal.

## 🗂️ CRM / LEADS

| Item | Estado |
|---|---|
| Form → HubSpot | ✅ portal `6874300`, form `6a6d9dfe...`, etiquetado `Landing Colombia` |
| Campos capturados | ✅ nombre, teléfono (internacional armado bien), email, objetivo, plazo, presupuesto, tipo, UTMs |
| Redirect a /gracias | ✅ tras enviar (o 2s máx) |

## 📄 PÁGINA

| Item | Estado |
|---|---|
| Landing V2 (hero reforzado, calculadora, testimonios) | ✅ |
| Form multi-paso que CALIFICA (objetivo+plazo+presupuesto obligatorios) | ✅ con validación clara |
| Gracias rediseñada (Navy, sin WhatsApp) | ✅ |
| Sin botones WhatsApp (leads solo por form = traqueo) | ✅ |
| Móvil (sin overflow, sin imágenes rotas, CTA fijo no estorba) | ✅ |
| Privacidad `/privacidad` | ✅ |

---

## ⚠️ ANTES DE MANDAR TRÁFICO (acción tuya, no de la página)

1. **Lista blanca del dominio (CRÍTICO para el pixel):** hoy Meta solo acepta eventos de navegador desde `colombia.playablancaresidences.com`. O conectas ese dominio (DNS) y mandas tráfico ahí, O agregas `landing-colombia-full.vercel.app` a la lista de autorizados del pixel en Meta. Sin esto: el CAPI trackea pero el pixel del navegador se bloquea.
2. **1 lead de prueba** → confirmar que llega a HubSpot etiquetado Colombia.
3. **Texto:** unificar "24 horas" (landing) vs "minutos" (gracias).

---

## 🚀 CÓMO ARMAR LA CAMPAÑA (lead-gen a la landing)

1. **Objetivo:** Clientes potenciales (Leads) o Ventas → **Ubicación de conversión = Sitio web** (NUNCA "Formulario instantáneo" de Meta — ese fue el problema de calidad en Panamá).
2. **Dataset/Pixel:** `1923056805076909`. **Evento a optimizar: `Lead`.**
3. **Categoría especial de anuncios:** Meta probablemente pida declarar **Vivienda** (bienes raíces). Eso LIMITA la segmentación (sin edad/género, geo amplio). Deja el público amplio Colombia y que el FORMULARIO califique. NO pongas edad explícita en el copy (riesgo discriminación).
4. **Presupuesto de PRUEBA:** bajo ($10-20/día) para medir CPL + calidad. Escalar solo lo que traiga leads buenos.
5. **Creativos:** los ángulos que ya tienes (dólares / retiro / renta). Empieza con 2-3 para comparar.
6. **URL:** la landing + UTMs (`utm_source=meta`, `utm_campaign=...`) — la página ya los captura y los manda a HubSpot.
7. **Ventana de atribución:** 7 días clic / 1 día vista (estándar lead-gen).
8. **Primeras 48-72h:** no toques nada (fase de aprendizaje). Mide calidad por presupuesto/plazo en el CRM, no solo cantidad.
