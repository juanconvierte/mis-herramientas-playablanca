# CLAUDE.md — Proyecto Playa Blanca Residences (media buying)

Media buying para **Playa Blanca Residences** (inmobiliaria de lujo, Pacífico de Panamá). Cliente: Ralph (dueño) · Dyana (marketing). Agencia: Juan (cobra $400/mes fijo).

**KPI real (dicho por el cliente):** leads **CUALIFICADOS** = compradores potenciales con presupuesto real (rango de inversión + intención cercana). Ralph textual: *"no me importa si un lead sale caro con tal de que se pague solo cuando vendo una propiedad; me da igual si me llegan baratos pero no son compradores"*. → CPL es secundario; el número que importa es **calidad de lead** (presupuesto declarado) y, cuando se pueda medir, **ROAS**.

## Reglas duras (anti-bug — aprendidas a la mala)
- **Compliance VIVIENDA (Meta HOUSING):** PROHIBIDO en copy/landings → "rentabilidad/plusvalía/retorno garantizado", "se paga sola", ingresos por alquiler como promesa, "sin banco", "escrow", "fideicomiso", "título a tu nombre", y **edad explícita** en el texto del anuncio (riesgo discriminación). Solo diferenciales reales verificables.
- **Nunca tocar campañas/ads/adsets VIVOS del cliente sin OK explícito.** Ads nuevos se crean en PAUSA salvo que Juan diga "actívalos".
- **Secretos** (tokens Meta/CAPI/HubSpot, DASH_KEY) → SOLO en `.env`/config.json/Vercel env. NUNCA dentro del HTML público. Proteger con `.vercelignore`/`.gitignore`.
- **No inventar datos.** Verificar todo claim contra la data oficial del cliente (ver `ESTADO-PROYECTOS.md`). Si no está confirmado → marcar para preguntar al cliente.
- **🚨 DESPLIEGUE = `git push` (Vercel↔GitHub CONECTADO, 24-jul).** Los 2 sitios están enlazados a Vercel por Git. Para publicar CUALQUIER cambio de un sitio: desde su carpeta correr `git add -A && git commit -m "..." && git push origin main` → Vercel despliega solo + GitHub respalda (1 movimiento = deploy + backup). **PROHIBIDO** desplegar con `vercel --prod`/deploy suelto SIN push: deja GitHub viejo y se pierde el respaldo. Repos privados: `web-panama-LIVE`→`playablanca-panama`, `landing-colombia-full`→`playablanca-colombia`, herramientas propias→`mis-herramientas-playablanca` (push manual, NO Vercel). Auth por SSH (`id_ed25519`, ya conecta a `juanconvierte`).
- **🚨 VARIOS CHATS A LA VEZ (Juan tiene el proyecto abierto en ~3 chats).** ANTES de tocar o desplegar cualquier sitio: correr `git fetch && git status` en su carpeta para NO pisar cambios de otra sesión. Si hay cambios sin commitear de otra sesión (working tree modificado), commitéalos/coordina ANTES de desplegar. (Ya pasó: una sesión desplegó un secfix sin commit → GitHub quedó viejo y hubo que resincronizar.)
- **Nota estructura (24-jul):** `asistente/`, `Playa Blanca/`, oficina-habbo/war-room/agente.html se movieron a `_ARCHIVO/jubilados-24jul/` (Telegram muerto, NO se entrega). El token Meta vive en `.env` raíz + Vercel env (ya NO en `asistente/config.json`). Lo PESADO (fotos/renders/_ARCHIVO ~1.4GB) va a Google Drive, NO a git.

## Datos clave (verificar siguen vigentes antes de usar)
- Cuenta Meta: `act_852024635148139` (USD) · token en `asistente/config.json` (y en Vercel env).
- Campaña viva: "PB | LEADS PANAMA | Vivienda - Compradores Calidad" `120251665917840616` · ad set `120251665958320616` · form instantáneo `1454090062522225`.
- Página FB `360302430750185` · IG `17841400495105711`.
- Pixel/dataset: Panamá `2195180334399669` · Colombia `1923056805076909`.
- HubSpot portal `6874300` · form GUID `6a6d9dfe-74e4-4078-8b1c-18a3a814a0f8`.
- Vercel (logueado como juanconvierte): proyectos `landing-panama`, `landing-colombia-full`, `web-prueba`.

## Mapa de archivos (verificado 20-jul-2026 contra disco — ver `ESTRUCTURA-PROYECTO.md` y `README.md`)
Estructura en la raíz de `META ADS/`:
- `web-panama-LIVE/` → 🟢 Panamá VIVO en Vercel. Landing (`index.html` + `gracias.html`), paneles CRM (`crmceo.html`, `crmdataplayablanca.html`, `paneljuan.html`, `war-room.html`, `dashboard-leads.html`), oficina IA (`agente.html`, `oficina-habbo.html`), legal (`privacidad.html`), reportes (`reporte-final.html`, `reporte-qa-87.html`), config (`vercel.json`, `package.json`). Backend `api/` (13 funciones): `crm.js`, `hs-webhook.js` (leads HubSpot + control por API), `conversion.js` + `meta-events.js` (CAPI), `vigia.js` + `wa-lead-poll.js` + `wa-grupo.js` (vigía WhatsApp→grupo), `reporte.js`, `parte.js`, `leads.js`, `panel.js`, `tg-bot.js`, `_excel.js`. Correos en `emails/` (5 plantillas + preview).
- `landing-colombia-full/` → 🟢 web Colombia viva (espejo Panamá, retiro/dólares) con su propio `api/`. Campaña pendiente de lanzar.
- `motor-creativos/` → motor Python de imágenes 1080x1920 (`engine/`, `biblioteca_imagenes/`, `salidas/`, `fonts/`, `specs/`). `plataforma-creativos/` → versión web del motor (studio.py + render_*.py).
- `asistente/` → bot Telegram + scripts Python + `leads_db.json` (histórico local; el sistema vivo ya está en Vercel).
- `CRM/` → proyecto CRM propio futuro (reemplaza HubSpot), 3 fases: `1-DEMO/`, `2-PROPUESTA/`, `3-CONSTRUCCION/`.
- `fotos/` → biblioteca de imágenes (`proyecto/`, `muestras_ia/`, `creativos/`). `docs/` → ~24 archivos: documentación (.md), Excels de leads, blueprints, `propuesta/`. `emails/` (raíz) → plantillas correo. `exports/` → Excel/CSV de compradores (retargeting/exclusión Meta).
- Raíz: `MAPA-AGENTE-WHATSAPP.html` (diagrama del vigía).
- `_ARCHIVO/` → versiones viejas / respaldos (web-prueba, landings OLD, backups dashboard, `Playa-Blanca-residual-jul/`). NO borrar sin OK.
- ⚠️ Residual: la carpeta `Playa Blanca/` (vieja) NO se eliminó del todo — quedan `Playa Blanca/asistente/logs/` (4 logs muertos). Candidata a mover a `_ARCHIVO/` o borrar con OK.
- Secretos: `.env` (raíz, gitignored) + `asistente/config.json` + Vercel env.

## Cómo verificar el trabajo (correr SIEMPRE antes de dar por hecho)
- HTML íntegro: `python3 -c "h=open('archivo.html').read();print(h.count('<section')==h.count('</section>'), '</html>' in h)"`
- Landing pública: `curl -s -o /dev/null -w '%{http_code}' URL` (debe dar 200) + grep del pixel/título.
- Estado campaña/leads: leer vía Graph API con el token de config.json (lead real = action_type `onsite_conversion.lead_grouped`, NO sumar todas las que contienen "lead").

## Convenciones
- Copy: personalizado por imagen/ángulo, nunca genérico. Público núcleo = 55-65 (Panamá: "usted"; Colombia: "tú").
- Antes de desplegar una web: probar el form (1 lead → llega a HubSpot etiquetado) y verificar token NO expuesto.
- Memoria persistente del proyecto en `~/.claude/projects/.../memory/` (índice MEMORY.md).

## gstack (skills de Garry Tan/YC — instalación curada, jul 2026)
Instalados 10 skills gstack en `~/.claude/skills/` (markdown puro, sin Bun; NO se corrió el `./setup` pesado). Encajan con el proyecto:
- `/plan-ceo-review` → revisa una idea/feature en modo CEO/fundador (¿mueve la aguja?).
- `/office-hours` → estilo YC Office Hours: describe qué construyes, te guía.
- `/design-consultation` + `/design-review` → sistema de diseño y QA visual para landings/creativos.
- `/review` → revisión pre-deploy de cambios (CRM, landings, APIs).
- `/cso` → auditoría de seguridad (relevante: tokens Meta/HubSpot/CAPI).
- `/investigate` → debugging con causa raíz.
- `/careful` + `/guard` → modo seguridad contra comandos destructivos (encaja con "no tocar campañas vivas").
- `/retro` → retrospectiva del trabajo.
- NO instalados (no aplican al stack: iOS, browser binary, Supabase/gbrain, canary, benchmark, /qa, /ship, /browse). Si se quieren: instalar Bun + correr `gstack/setup`.
- Regla del usuario sigue vigente: PREGUNTAR antes de invocar cualquier skill.
