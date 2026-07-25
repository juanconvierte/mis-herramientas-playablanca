# HISTORIAL DE CAMBIOS — CRM Playa Blanca

> Claude Code registra aquí cada cambio: fecha, tarea, archivos tocados y decisión.
> Sirve para no perder contexto entre sesiones (memoria del proyecto, estilo Biblia).

---

## 2026-07-11 — FASE 0 (setup / Biblia)
- **Demo de venta** creado: `../1-DEMO/index.html` (Kanban estilo Excermol, interactivo, botón "Simular lead").
- **Propuesta + guion** creados: `../2-PROPUESTA/` (index.html visual + GUION-REUNION.md con 3 objeciones).
- **Plano SDD** creado: `spec-crm.md`, `CONSTITUCION.md`, `tasks.md`, `CHECKLIST-CRM-CONFIABLE.md`, `correos-resend.md`, `.env.example`.
- **Estructura Biblia completada:** añadidos `prompt-maestro.md`, `agent-teams.md`, `history.md`, `CLAUDE.md`, `README.md`, `.gitignore`, `/ui-reference`.
- **Decisiones cerradas:** 4 vendedoras ficticias · round-robin 1×1 · login PIN · correo 2h · HubSpot en paralelo (no apagar) · misma landing.
- **Reorg:** todo el CRM movido a la carpeta `CRM/` (1-DEMO, 2-PROPUESTA, 3-CONSTRUCCION).
- **Estado:** esperando que Juan cree cuentas Supabase + Resend y llene `.env` para arrancar Fase 1.

## 2026-07-11 — Investigación open-source (apalancarse)
- Investigados CRMs open-source. Descartado **Twenty** (potente pero AGPL = riesgo para vender; pesado, VPS+Docker).
- Estudiado **Atomic CRM** (Marmelab, MIT, Supabase) — clonado para aprender. Modelo pro: contactos, deals, tareas, notas, tags, sales.
- **Decisión:** NO adoptar el fork entero (React+react-admin = complejo, no matchea el demo). **Aprender + adaptar** su modelo de datos a nuestro stack simple.
- **Schema subido a versión INTERMEDIA:** agregadas tablas `notas`, `tareas`, `tags`, `lead_tags` (robadas de Atomic). CRM pasa de básico → intermedio profesional.

## 2026-07-11 — Supabase conectado (Fase 1 arrancando)
- Proyecto Supabase creado: `crm-playa-blanca`, ref **lnbkugbllmfyjtuvaltv**, org "Playa Blanca" (Free), región Americas.
- Seguridad al crear: Data API ON, expose-new-tables OFF, RLS auto ON.
- En `.env`: `SUPABASE_URL` + `SUPABASE_ANON_KEY` (publishable) + `SUPABASE_SERVICE_ROLE` (secret). ⚠️ La secret key se expuso en el chat → rotar antes de meter leads reales (proyecto vacío ahora = riesgo bajo).
- ⏳ PENDIENTE: correr `supabase/schema.sql` en el SQL Editor (crear las 6 tablas). El sandbox no tiene psql y la conexión directa es IPv6 → Juan lo pega manual.

## 2026-07-12 — FASE 1 FUNCIONANDO (probado en vivo) ✅
- Tablas creadas en Supabase por Claude (vía pooler us-east-2 + psycopg2), grants + reload PostgREST → REST 200.
- **Capa de datos:** `lib/db.js` (REST con fetch, service_role) + `lib/leads.js` (crear+auto-asignación round-robin, listar, actualizar).
- **API serverless:** `api/leads.js` (GET/POST/PATCH) + `api/login.js` (PIN).
- **UI real:** `index.html` — login por PIN + Kanban por estado + tarjetas + auto-asignación + "Simular lead" + money rollup.
- **Servidor de prueba:** `_dev-server.js` (local, no producción).
- **PROBADO en vivo contra Supabase real:** login admin (0000), 6 leads sembrados repartidos round-robin (Dyana/Carolina/Roberto/Sofía), "Simular lead" creó Fernando Quintero→Roberto EN LA BASE, pipeline $2.4M. Screenshot verificado.
- Datos de prueba (origen `seed`/`sim`) → borrar antes de leads reales.
- **NADA de HubSpot tocado.** Todo aislado en el Supabase nuevo.
- FALTA: conectar el form de la landing real → Supabase · Fase 2 (Resend 2h + Telegram) · deploy Vercel.

<!-- Próximas entradas las agrega Claude Code al construir cada tarea -->
