# HANDOFF — Sesión 12-jul-2026 (contexto completo para continuar en chat limpio)

Este doc captura TODO lo hecho hoy + lo pendiente, para poder hacer `/clear` y seguir sin perder nada.

## 🎯 Lo que se logró HOY (todo verificado y vivo salvo lo marcado)

### 1. Vigía de leads (alerta instantánea por lead) — VIVO
- Endpoint: `web-panama-LIVE/api/wa-lead-poll.js`. Revisa HubSpot cada X min, si entra lead nuevo → dispara alerta pro al grupo WhatsApp vía `/api/hs-webhook`.
- Dedup en memoria (`_SENT` Map). Ventana = `mins` (debe ≈ intervalo del cron).
- **Trigger: cron-job.org** (cuenta de Juan) → pinguea `https://panama.playablancaresidences.com/api/wa-lead-poll?key=ralph-ceo-pb-7q29&mins=5` cada 2 min. (Vercel Hobby NO permite cron cada 3 min → por eso cron-job.org externo.)
- Ruta debug: `?check=email` (lee pasaporte fbc/fbp/event_id) · `?archive=email` (borra contacto de prueba) · `?setup=1` (crea las 4 props HubSpot).

### 2. Reportes WhatsApp (diario/semanal/mensual) — VIVOS
- Endpoint: `web-panama-LIVE/api/wa-grupo.js` + Excel en `api/_excel.js`.
- Crons Vercel (`vercel.json`): slots 57/58/59 a las 04:57/58/59 UTC = 23:57/58/59 Panamá. Lógica por slot decide dia/semana/mes.
  - Domingo: 11:58 = diario, 11:59 = semanal. Fin de mes: 11:57 = diario, 11:59 = mes. (PROBADO con `?noenvio=1`.)
- Manda al grupo real "Reportes Diarios Real Estate Playa Blanca" vía Green API (número Digitel de Juan). Excel adjunto + reporte como caption (1 mensaje).
- Prueba a número propio: `hs-webhook?test=1&wa=1&to=self` (resuelve el wid del propio WhatsApp).

### 3. PASAPORTE CAPI — VIVO y PROBADO (Panamá) ✅
- **Objetivo:** guardar fbc/fbp/event_id de cada lead → base para evento diferido Purchase → ROAS real + mejorar calidad Meta.
- Permiso HubSpot `crm.schemas.contacts.write` PRENDIDO en la app privada **"Verificacion"** (el token vive SOLO en Vercel env `HUBSPOT_TOKEN`, no en docs; fue expuesto en el chat del 12-jul → ROTAR pendiente cuando Juan quiera).
- 4 props creadas en HubSpot vía `wa-lead-poll?setup=1`: `fb_fbc`, `fb_fbp`, `fb_event_id`, `tipo_de_propiedad`.
- Guardado server-side en `api/conversion.js` (Panamá + Colombia): tras enviar el evento a Meta, hace `POST /crm/v3/objects/contacts/batch/upsert` (idProperty=email) con los 3 fb_. **Probado:** email real → fbc/fbp/event_id llegan a HubSpot. (Emails `.test` los rechaza HubSpot con INVALID_EMAIL — usar dominio válido para probar.)
- **Colombia:** mismo código listo, PERO su proyecto Vercel necesita env `HUBSPOT_TOKEN` cuando se lance.

### 4. Panel del Creador (JUAN2026) — VIVO (diseño), data pendiente
- Página: `web-panama-LIVE/creadorcrm.html` → `https://panama.playablancaresidences.com/creadorcrm` · clave **JUAN2026** (env `JUAN_KEY` en Vercel). Favicon 🚀.
- Estilo clonado del panel CEO (navy/gold). Muestra los 15 eventos en 4 grupos (Embudo/Calidad/Engagement/Audiencia) + embudo del form + KPIs. Cada evento marca ● vivo / ○ pendiente.
- API: `api/meta-events.js` → intenta leer conteos del pixel vía Graph `/{pixel}/stats?aggregation=event_total_counts`.
- ⚠️ **PROBLEMA:** ese endpoint de Meta devuelve 0 hasta para Lead (aunque hay data real en Events Manager). → El panel muestra todo en 0. **La data SÍ existe** (visible en Events Manager UI), pero la Graph API no la expone limpio.
- **Plan B pendiente:** contador propio — cada evento pixel también pinguea `/api/ev?e=Nombre` → cuenta en Vercel KV (gratis, NO Supabase) → panel lee eso. (Juan dijo: después.)

### 5. Panamá `_fbc` = Colombia — desplegado
- Panamá ahora setea la cookie `_fbc` apenas carga la página (espejo de Colombia) → mejor cobertura de fbc. Cada landing con SU pixel/CAPI (PA `2195180334399669`, CO `1923056805076909`).

## ✅ CIERRE DE SESIÓN (12-jul noche) — lo que se completó al final
- **15 eventos portados a Panamá** (espejo de Colombia, adaptado a sliders ROI `roi-precio/ocupacion/tarifa`). Ambos países con los 15. Desplegado.
- **Colombia pasaporte VIVO:** se agregó env `HUBSPOT_TOKEN` al proyecto Vercel `landing-colombia-full` (prj_PEx2OvBoRE) + redeploy. PROBADO: fbc/fbp/event_id se guardan desde Colombia. Colombia = Panamá completo.
- **Clarity Colombia ARREGLADO:** el CSP de `landing-colombia-full/vercel.json` NO tenía `clarity.ms` → bloqueaba el script → 0 grabaciones. Se agregó `https://www.clarity.ms https://*.clarity.ms` a script-src/img-src/connect-src. Ya graba. (Ambas landings usan el MISMO proyecto Clarity `xlby6ydjfh` — para separar Colombia, crear 2º proyecto Clarity.)
- **tipo_de_propiedad ARREGLADO:** era enumeration con opciones `Apartamento 2-3 recámaras / Villa / Casa / Penthouse` que NO calzaban con lo que manda la landing (`Apartamento 3-4 recámaras / Casa / Villa`) → HubSpot botaba el valor (por eso panel widget vacío 0/231). Se alinearon por API a: `Apartamento 1-2 recámaras · Apartamento 3-4 recámaras · Casa / Villa · Aún no lo sé`. Chequear con próximo lead real que capture (si el FORM valida aparte por sus opciones, ajustar el form en HubSpot UI también).
- **Rutas debug en `wa-lead-poll.js`** (todas key-protected): `?setup=1` (crea 4 props), `?check=email`, `?archive=email`, `?prop=nombre` (lee def de propiedad), `?fixtipo=1` (alinea opciones tipo_de_propiedad). `conversion.js?debug=1` devuelve `_hs` (status del upsert).
- **Verificación final:** landings 200, panel CEO 200, panel Creador 200, APIs (panel/meta-events/vigía) OK, Clarity en CSP CO, tipo alineado. TODO VIVO.

## 🔴 PENDIENTES (orden sugerido) — actualizado

0. **INVESTIGAR: leads del instant form llegan VACÍOS a HubSpot.** El lead "tayra julio" (12-jul 19:49) entró con solo nombre/email/teléfono/asesor — sin rango_de_inversion, plazo, objetivo, tipo, utm, origen_formulario (todo "--"). Vino del FORMULARIO INSTANTÁNEO de Meta (form `1454090062522225`), NO de la landing. Juan dice que el instant form SÍ pide filtros (presupuesto/plazo) → entonces el problema es que **las respuestas del instant form NO se están mapeando a los campos de HubSpot**. Revisar: (a) las preguntas reales del instant form en Meta, (b) cómo la integración Meta↔HubSpot mapea esas respuestas a las propiedades (rango_de_inversion, plazo_de_decision, objetivo_de_inversion, tipo_de_propiedad). Afecta a TODOS los leads del instant form → sin esto el panel/reportes salen sin presupuesto para esos leads. IMPORTANTE.
1. **Plan B contador (Vercel KV)** → llenar el panel del Creador con data real (Meta Graph stats devuelve 0; la data existe solo en Events Manager UI).
2. **Webhook HubSpot → evento diferido `CitaAgendada`/`Purchase`** (action_source: system_generated, usa el pasaporte guardado) → ROAS real. ESTE es el gran paso desbloqueado hoy.
3. **ROTAR token HubSpot** (expuesto en chat; Juan decidió DIFERIR — chat no es público, no urgente). Al rotar: usar "vence más tarde" (7 días), meter nuevo token en Vercel env `HUBSPOT_TOKEN` de AMBOS proyectos (landing-panama Y landing-colombia-full), redeploy los 2.
4. Organizar carpeta META ADS + docs MD por proyecto (SIN romper nada).
5. Backup a GitHub (respaldo + deploy).
6. Fix ad set `optimization_goal` LEAD_GENERATION → QUALITY_LEAD (con OK de Juan, no tocar vivo).
7. Arreglar 2 ads viejos no-compliant HOUSING.
8. Dominio Colombia (DNS/CNAME) + Resend + `/api/mail.js`.
9. Lanzar campaña Colombia WEB (en pausa).
10. Verificar que bajen los errores 4XX de la app "Verificacion" (ocasionales, no rompen; probable rate-limits + pruebas de hoy).
11. Opcional: 2º proyecto Clarity separado para Colombia.
12. Confirmar con próximo lead real que `tipo_de_propiedad` se captura (si no, ajustar opciones del form en HubSpot UI).

## Datos técnicos clave
- Vercel proyecto Panamá: `landing-panama` (prj_GzLCnAUJ...), logueado `juanconviertes-projects`. Deploy: `cd web-panama-LIVE && vercel --prod --yes`.
- Límite Vercel Hobby: ~13 funciones serverless en `/api`. Estamos al tope — NO agregar endpoints nuevos sin quitar otro (por eso `hs-setup` se fusionó en `wa-lead-poll?setup=1`).
- Env sensibles NO se leen con `vercel env pull` (marcados sensibles): HUBSPOT_TOKEN, GREENAPI_*, META_*, JUAN_KEY, PANEL_KEY (ralph-ceo-pb-7q29).
- HubSpot portal 6874300 · app privada "Verificacion" tiene: contacts.read/write, owners.read, schemas.contacts.read+**write** (nuevo).
- Green API: grupo en env `GREENAPI_GROUP`. `waSend(msg, to)` acepta `to='self'` para mensaje a sí mismo.

## Reglas de Juan (recordar siempre)
- Todo tiene que quedar configurado para **Panamá Y Colombia** (espejo).
- Preguntar antes de invocar cualquier skill.
- No tocar campañas/ads VIVOS sin OK. Ads nuevos en PAUSA.
- Compliance HOUSING en copy/landings.
- Secretos solo en env, nunca en HTML público.
- Juan no es técnico: dirigir con pasos cortos, opción múltiple, sin enredar.
