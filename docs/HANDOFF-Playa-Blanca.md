# HANDOFF — Proyecto Playa Blanca Residences
**Sube este archivo a un chat nuevo y tendrá todo el contexto del proyecto.**
(No contiene valores de claves — seguro de compartir. Generado jun 2026.)

---

## 0. Cómo trabajar con Juan (importante)
- Juan Escorcha — **media buyer / Meta Ads**, NO técnico. No domina HubSpot.
- **Hablar SIEMPRE simple, un paso a la vez, sin jerga, no enredar.** Si algo es técnico o un menú confunde → pedir screenshot y marcar el clic exacto.
- **Ahorrar tiempo:** ir directo a lo funcional, no ofrecer pasos opcionales/cosméticos.
- **Perfeccionista:** auditar antes de deploy, calidad > velocidad.
- **NUNCA inventar** testimonios, cifras, premios ni logos (tráfico pagado a inversores = compliance).

---

## 1. Qué es el proyecto
Landing de conversión para correr **Meta Ads** del cliente **Playa Blanca Residences** (real estate de lujo, costa Pacífica de Panamá; diferenciador = **la laguna de agua salada más grande de Centroamérica/Caribe**).
Flujo: **Meta Ads → Landing → Form 3 pasos → HubSpot CRM + Pixel + CAPI → /gracias.**
Público: inversores **55-68**, patrimonio alto (PA + CO). Claridad > completitud. Objetivo ROAS 10-15x.

---

## 2. Estado actual (TODO LISTO menos encender ads)
| Pieza | Estado |
|---|---|
| Landing + dominio propio + SSL | ✅ LISTO (panama.playablancaresidences.com) |
| Pixel Meta (eventos + value/currency) | ✅ LISTO |
| CAPI server-side | ✅ LISTO (events_received:1) |
| HubSpot (script, cookie hubspotutk, anti-spam) | ✅ LISTO — leads entran limpios |
| Teléfono internacional (+E.164, selector país) | ✅ LISTO |
| Panel de leads EN VIVO (dark premium) | ✅ LISTO |
| CRM limpio (contactos de prueba borrados) | ✅ LISTO |
| Campaña Meta Ads | ⏳ PENDIENTE — encender |

---

## 3. URLs
- Landing: **https://panama.playablancaresidences.com** (respaldo: landing-panama.vercel.app)
- /gracias · /privacidad
- Panel de leads: **/panel?key=DASH_KEY** (clave en Vercel env DASH_KEY)

## 4. IDs
- HubSpot Portal: **6874300** · Form GUID: **6a6d9dfe-74e4-4078-8b1c-18a3a814a0f8**
- Pixel Meta (sitio): **2195180334399669** · Pixel Meta (HubSpot, aparte): **2206424516102243**
- Cuenta publicitaria: **23843359180650615**
- Vercel: proyecto **landing-panama** (team juanconviertes-projects)

## 5. Claves — dónde viven (NUNCA en archivos ni memoria)
- `META_ACCESS_TOKEN` → Vercel env (CAPI)
- `HUBSPOT_TOKEN` → Vercel env (panel lee HubSpot)
- `DASH_KEY` → Vercel env (clave del panel)
- HubSpot Private App `pat-...` (scopes: contacts read/write, schemas.contacts.read, owners.read) → en HubSpot de Juan. Si se necesita, Juan lo pega en el chat (no se guarda).

---

## 6. Arquitectura / archivos
- `index.html` — landing (form 3 pasos, Pixel, script HubSpot, selector país de teléfono)
- `gracias.html` / `privacidad.html`
- `api/conversion.js` — CAPI server-side → Meta (usa META_ACCESS_TOKEN)
- `api/leads.js` — API protegida del panel (lee HubSpot con HUBSPOT_TOKEN, protegida por DASH_KEY, resuelve nombres de asesores)
- `panel.html` — panel de leads en vivo (dark, refresco 60s, filtra origen="Landing Panamá")
- `vercel.json` — rutas, headers, seguridad (OJO: headers source en path-to-regexp, sin `(?:)` ni `$`)
- Internos (NO publicar, gitignored+vercelignored): GUIA-SOP, Presentación PPT, MASTER-Playa-Blanca.html, dashboard-leads.html, _gen_*.js

**Deploy:** Vercel CLI. `vercel --prod --yes` (login de Juan ya hecho). NO hay GitHub conectado; el deploy es manual con ese comando.

---

## 7. Variables del formulario → HubSpot
- Estándar: `firstname, lastname, phone, email`
- Custom: `objetivo_de_inversion, plazo_de_decision, rango_de_inversion, tipo_de_propiedad`
- Origen: `utm_source/medium/campaign/content/term`, `origen_formulario` (= "Landing Panamá", marca de la landing)
- Teléfono: se arma `+E.164` con `buildFullPhone()` (quita ceros, no duplica código). Se reescribe en el campo al enviar para que la captura automática de HubSpot lo guarde limpio.

---

## 8. Decisiones / reglas clave
- Desarrollador = **"Playa Blanca Residences"** (cerrado por Juan; NO meter "Grupo Los Pueblos" — evidencia dice que NO lo desarrolla).
- **Testimonios:** hay 3 DEMO ficticios (data-demo=3). Juan los DEJA y pidió NO mencionarlos más. Tema cerrado.
- Anti-spam HubSpot: dominio registrado en Configuración → Seguimiento y analíticas → Código de seguimiento → Seguimiento avanzado → Dominios de sitio adicionales.

---

## 9. Qué falta
1. **Encender la campaña Meta** (objetivo Leads, creativos 5/10 hechos, público 55-68, presupuesto test $30-50/día, UTMs).
2. Verificar Pixel verde con Pixel Helper en vivo (1 envío real).
3. Datos opcionales del cliente (no inventar): años entrega, banco escrow, foto/nombre asesor real.

## 10. Cómo continuar (prompts)
- "Actualiza el panel de leads."
- "Cambia [X] de la landing y deploya."
- "Arma la campaña de Meta paso a paso."
- "Verifica los leads en HubSpot por API." (pegar el token pat- si lo pide)

---
*Fin del handoff. Detalle completo también en MASTER-Playa-Blanca.html (local, privado).*
