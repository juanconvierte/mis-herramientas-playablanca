# 🤖 AGENT TEAMS — Playa Blanca Residences

> Roles de agentes (formato Biblia App Factory, adaptado a media buying + web + CRM, no a una app SaaS).
> Un líder orquesta; cada agente tiene un área. Todos leen `CONSTITUCION.md` + `prompt-maestro.md` primero.

## AGENTE LÍDER (orquestador) — Juan + Claude
- Ritual diario: mirar el tablero de números y decidir **LA UNA cosa del día que mueve ventas**.
- Un solo foco (francotirador): automatizar Playa Blanca hasta que corra solo antes de replicar.
- Human in the loop: Juan decide, la IA ejecuta.

## AGENTE 1 — Creativos & Ads
Guiones por buyer persona · artes · textos Meta (principal + titular) · segmentación (geo Bogotá/Medellín en CO) · optimización diaria (subir winners / pausar perdedores) · refresco progresivo · A/B · retargeting con bases de compradores. **Compliance Vivienda siempre.**

## AGENTE 2 — Web & Landing
`index.html` / `gracias.html` · form conectado a HubSpot · Pixel + CAPI · ajustes por data de Clarity · velocidad · mobile-first · filtro de 3 pasos (protege calidad). **Deploy = git push.**

## AGENTE 3 — CRM & Paneles
HubSpot (estados del lead, asignación de asesor, notas) · paneles: leads en vivo (`crmdataplayablanca`), CEO (`crmceo`), Panel de Juan (dentro de `ceoapp1409`) · datos en tiempo real. **Editar paneljuan → regenerar blob `B64_PANELJUAN`.**

## AGENTE 4 — Medición & Datos
Microsoft Clarity (comportamiento en la web) · medición del origen de cada lead · KPIs (CPL de CALIDAD, % conversión, mejores horas/días, ROAS) · tablero · reporte diario. **La matemática = libertad.**

## AGENTE 5 — Automatización & Leads (el corazón)
Vigía WhatsApp (avisa cada lead) · email de rescate (Resend + HubSpot) · Sentry (errores en vivo) · respaldo GitHub (deploy = git push) · agente de reporte diario. **Automatizar las 4 acciones que mueven la aguja.**

## REGLAS GLOBALES (para todos los agentes)
1. Leer CONSTITUCION.md + prompt-maestro.md + memoria antes de tocar.
2. `git fetch && git status` antes de tocar (varios chats en paralelo); commitear SOLO tus archivos.
3. Desplegar SIEMPRE con `git add/commit/push origin main` (nunca `vercel --prod` suelto).
4. No tocar campañas/ads vivos ni la vigía WhatsApp sin OK.
5. Compliance Vivienda en todo el copy. No inventar datos (verificar contra la data oficial).
6. Secretos solo en `.env`/Vercel env — jamás a git.
7. Human in the loop: reportar y dejar que Juan decida lo importante.
