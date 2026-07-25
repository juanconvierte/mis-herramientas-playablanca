# CLAUDE.md — CRM Playa Blanca (punto de entrada)

> Contexto del proyecto para Claude Code (estilo Biblia: claude.md apunta al líder).
> Cuando trabajes en esta carpeta, lee estos archivos EN ESTE ORDEN antes de construir:

1. **CONSTITUCION.md** — reglas fijas (seguridad, datos, compliance). NO se rompen.
2. **prompt-maestro.md** — objetivo, stack, features del MVP, criterios de aceptación.
3. **spec-crm.md** — especificación detallada (tablas, pantallas, flujo).
4. **agent-teams.md** — los agentes y quién hace qué.
5. **tasks.md** — la lista de tareas con estados (por dónde vas).
6. **history.md** — qué se hizo antes (memoria entre sesiones).

## Qué es este proyecto
CRM propio para Playa Blanca Residences que reemplaza HubSpot. Stack real:
Supabase + Vercel serverless + Resend + Telegram + login por PIN. Sin Clerk/Shopify/Stripe.

## Reglas rápidas (detalle en CONSTITUCION.md)
- Secretos SOLO en `.env` (nunca en el chat, HTML o Git).
- RLS en todas las tablas. `SERVICE_ROLE` solo en backend.
- No tocar campañas vivas ni apagar HubSpot sin OK de Juan.
- Construir con mock data → verificar → conectar APIs reales.
- Registrar cada avance en `history.md`.

## Estado
Fase 0 lista. Falta: Juan crea Supabase + Resend + llena `.env` → arranca Fase 1.
