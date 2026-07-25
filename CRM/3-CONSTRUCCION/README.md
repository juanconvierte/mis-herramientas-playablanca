# CRM Playa Blanca — Construcción

Carpeta "war room" (metodología Biblia App Factory). Aquí se construye el CRM real.

## Archivos (estructura Biblia)
| Archivo | Qué es |
|---|---|
| `CLAUDE.md` | Punto de entrada — qué leer y en qué orden |
| `CONSTITUCION.md` | Reglas fijas (seguridad, compliance) |
| `prompt-maestro.md` | Brief maestro (objetivo, stack, MVP, criterios) |
| `spec-crm.md` | Especificación detallada (tablas, pantallas, flujo) |
| `agent-teams.md` | Los agentes de construcción |
| `tasks.md` | Tareas con estados |
| `history.md` | Registro de cambios (memoria) |
| `CHECKLIST-CRM-CONFIABLE.md` | Auditoría de confiabilidad (reutilizable) |
| `correos-resend.md` | Copy de correos automáticos |
| `.env.example` | Plantilla de accesos (copiar como `.env`) |
| `ui-reference/` | Referencia de diseño |

## Setup (para arrancar la construcción)
1. Crear cuenta **Supabase** → proyecto `crm-playa-blanca` → copiar URL + anon + service_role.
2. Crear cuenta **Resend** → copiar API key.
3. Copiar `.env.example` → `.env` y llenar las llaves. **Nunca pegar llaves en el chat.**
4. Decir "listo" → Claude construye Fase 1.

## Stack
HTML/JS + Vercel serverless + Supabase (Postgres + RLS) + Resend + Telegram + Sentry.
Login por PIN. Sin Clerk/Shopify/Stripe.
