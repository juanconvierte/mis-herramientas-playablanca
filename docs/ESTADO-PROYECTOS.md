# 📊 ESTADO DE TUS 2 PROYECTOS — Playa Blanca (jun 2026)

## 🇵🇦 PANAMÁ — checklist
- ✅ **Cuenta publicitaria:** `act_852024635148139` (Playablanca Residences, USD)
- ✅ **Campaña VIVA:** "PB | LEADS PANAMA | Vivienda - Compradores Calidad" (`120251665917840616`), HOUSING, $50/día
- ✅ **Conjunto:** `120251665958320616` · edad 50-63 · 2 pins 17km (Ciudad Panamá + Coronado)
- ✅ **Captación:** Formulario instantáneo Meta (`1454090062522225` · "MOTR Dic - Form Vivienda")
- ✅ **Anuncios activos:** 14 (6 originales 🟢 + 8 nuevos "dolores" 🟢 con copy del copywriter+Bruno) · 19 en pausa
- ✅ **Pixel/Dataset:** `2195180334399669`
- ⚪ **CAPI:** NO necesita (form instantáneo = tracking nativo)
- ✅ **HubSpot:** portal `6874300` (leads etiquetados)
- ⚪ **UTMs:** no aplica (form instantáneo no lleva)
- ✅ **Leads reales:** 2 (Zoraida 🔥 6-12m · Dumas, ambos $195-300k) → en `leads_db.json`
- ✅ **Bot Telegram:** status 8am/6pm (solo esta campaña)
- ✅ **Gasto/CPL:** ~$61 · 2 leads · CPL ~$30 (día 1-2, bajando)
- 🟡 **PENDIENTE:** decidir pausar 2 ads viejos con "sin banco/escrow" (compliance)
- 🟡 **PENDIENTE:** token `leads_retrieval` (auto-leads) → bloqueado: la app necesita agregar el caso de uso

## 🇨🇴 COLOMBIA — checklist
- ✅ **Web construida:** `landing-colombia/index.html` (retiro/dólares/cercanía, 8 ángulos, form 3 pasos)
- ✅ **Pixel/Dataset:** `1923056805076909` ("Playa Blanca Colombia") — SEPARADO de Panamá
- ✅ **CAPI Colombia:** token guardado (`.env.capi-colombia`) — listo para Fase 2 server-side
- ✅ **UTMs `co_*`:** definidos (`UTMS-COLOMBIA.md`)
- ✅ **HubSpot:** mismo portal, etiqueta `origen_formulario = "Landing Colombia"` (filtrable)
- ✅ **Dominio:** `colombia.playablancaresidences.com` (ya whitelisted en el dataset)
- ✅ **Público objetivo:** colombianos 55-65 (retiro, dólares)
- ✅ **Dataset settings:** coincidencias avanzadas ON · cookies origen ON · dominio autorizado
- ✅ **Web DESPLEGADA y viva:** https://landing-colombia-full.vercel.app (200, pixel Colombia, 0 claims prohibidos, disclaimer OK)
- ✅ **Form PROBADO** → llega a HubSpot etiquetado "Landing Colombia" (lead de prueba "PRUEBA Borrar Landing CO" — borrar del CRM)
- ✅ **CAPI configurado:** env `META_ACCESS_TOKEN` (token CAPI Colombia) + `DASH_KEY` (22FAE9E4CB834B34AB07EE32) en el proyecto Vercel
- ⏳ **HUBSPOT_TOKEN:** falta (es "sensitive", no se jala por CLI) → Juan lo pega para que funcione el PANEL de leads
- ⏳ **Dominio colombia.playablancaresidences.com:** pendiente DNS — el subdominio no tiene registro apuntando a Vercel (registrador externo). Juan debe: (1) en Vercel dashboard quitar el dominio de `landing-panama` y asignarlo a `landing-colombia-full`, (2) agregar registro DNS `colombia` CNAME → `cname.vercel-dns.com` en el registrador. Mientras tanto la web vive en el .vercel.app
- ❌ **Campaña Colombia NO creada** (falta, cuando decidas mandar tráfico)
- ❌ **Creativos Colombia** (faltan anuncios retiro/dólares)
- 🟡 **Cuenta publicitaria CO:** decidir — dataset ligado a `23843359180650615` (handoff) y compartido con `852024635148139`

## 🎯 PENDIENTES — orden sugerido
### Colombia (para lanzar)
1. Probar el form (1 lead → revisar HubSpot)
2. Subir la web (netlify.com/drop o Vercel)
3. Conectar `colombia.playablancaresidences.com`
4. Decidir cuenta publicitaria para la pauta CO
5. Crear creativos Colombia (retiro/dólares)
6. Crear campaña Colombia (objetivo Tráfico/Leads → web, con UTMs `co_*`)
7. (Opcional) CAPI server-side

### Panamá (mantenimiento)
1. Decidir 2 ads "sin banco/escrow" (pausar o confirmar dato)
2. Activar `leads_retrieval` (agregar caso de uso a la app) → auto-leads al Telegram
3. NO tocar la campaña 7 días (aprendizaje)

## 🔑 Diferencias clave (cero mezcla de data)
| | 🇵🇦 Panamá | 🇨🇴 Colombia |
|---|---|---|
| Captación | Form instantáneo | Web |
| Pixel | 2195180334399669 | 1923056805076909 |
| CAPI | no necesita | token listo |
| UTMs | sin UTM | co_* |
| Estado | VIVA | web lista, falta lanzar |
