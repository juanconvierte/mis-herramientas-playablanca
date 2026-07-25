# 📜 CONSTITUCIÓN — Proyecto Playa Blanca Residences

> Reglas NO negociables. Es lo PRIMERO que se lee antes de tocar cualquier cosa.
> (Formato SDD de la Biblia App Factory, adaptado a media buying + web + CRM, no a una app SaaS.)
> Complementa a `CLAUDE.md` (instrucciones vivas del proyecto).

## Stack real (no se cambia sin OK explícito de Juan)
- **Sitios web:** HTML + CSS + JS vanilla (SIN framework). `index.html` + `gracias.html` + paneles.
- **Backend:** Vercel Serverless Functions (Node, `api/*.js`) — usar `fetch` nativo, SIN dependencias npm pesadas.
- **CRM:** HubSpot (portal 6874300) vía API.
- **Ads / medición:** Meta Ads API + Pixel/CAPI + Microsoft Clarity.
- **Hosting/deploy:** Vercel (2 proyectos: landing-panama, landing-colombia-full).
- **Repos:** GitHub — `playablanca-panama`, `playablanca-colombia` (sitios cliente), `mis-herramientas-playablanca` (privado, de Juan).
- **Monitoreo:** Sentry (envío por HTTP directo, helper `api/_sentry.js`).
- **Correos:** Resend.
- **IA:** Claude Code (desarrollo/operación) + Gemini (motor de creativos).

## Lo PROHIBIDO
- Tocar campañas/ads/adsets VIVOS del cliente sin OK explícito (ads nuevos se crean en PAUSA).
- **Compliance VIVIENDA (Meta HOUSING):** NO "rentabilidad/plusvalía/retorno garantizado", "se paga sola", renta como promesa, "escrow/banco/título a tu nombre", ni **edad explícita** en el copy.
- Subir secretos a git (`.env`, `config.json`, tokens) — JAMÁS. Van en `.env` + Vercel env.
- Desplegar sin `git push` (Vercel↔GitHub CONECTADO → deploy = `git add/commit/push origin main`).
- Inventar datos — verificar contra `docs/DATOS-VERIFICADOS-PLAYA-BLANCA.md`.
- Borrar la **vigía WhatsApp** (`vigia`/`parte`/`wa-grupo`) — está VIVA, avisa leads.

## Convenciones
- Copy personalizado por buyer persona. Voz "usted" (Panamá) / "tú" colombiano (Colombia).
- **KPI real:** leads CUALIFICADOS (presupuesto declarado), NO el CPL. ROAS cuando se mida la venta.
- Editar `paneljuan.html` → regenerar el blob `B64_PANELJUAN` en `ceoapp1409.html` (el panel vive embebido ahí).
- Archivos `api/_*.js` = helpers (Vercel NO los expone como endpoints). Endpoints van sin `_`.
- Commits en español: `feat:`, `fix:`, `docs:`.

## Proceso obligatorio antes de tocar
1. Leer esta Constitución + `CLAUDE.md` + la memoria del proyecto.
2. `git fetch && git status` (proyecto abierto en varios chats — no pisar otra sesión).
3. Verificar en disco antes de dar algo por hecho.
4. Cambios grandes → plan primero (SDD), NO vibe coding.
5. Human in the loop: Juan decide, la IA ejecuta.

## Seguridad (no negociable)
- Secretos solo en `.env` + Vercel env.
- ⚠️ PENDIENTE: clave maestra CRM/DASH aún en HTML público (ceoapp1409) → rotar + gate server-side.
- Probar el embudo end-to-end (form → HubSpot etiquetado → aviso → panel) antes de dar por bueno.
