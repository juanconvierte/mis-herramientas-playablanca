# AGENT TEAMS — CRM Playa Blanca

> Modo Agent Teams de la Biblia. Un agente líder orquesta; los demás construyen.
> Adaptado al CRM real: SIN agente de Pagos (no hay cobros). Auth = PIN, no Clerk.

## AGENTE LÍDER (Orquestador)
Lee `tasks.md`, lanza el agente correcto según el estado de cada tarea, verifica que
cada uno funcione, y registra en `history.md`. Punto de entrada: `CLAUDE.md` apunta aquí.
- Tarea `pending` → lanza el agente que corresponde.
- Tarea `spec_ready` → pausa, espera aprobación de Juan.
- Tarea `in_progress` → lanza Implementer + Reviewer.
- Tarea `done` → registra en `history.md`.

## AGENTE 1 — FRONTEND
**Rol:** todo lo que las asesoras ven y usan.
- Pipeline Kanban (reusar el diseño de `../1-DEMO/`), vista Lista, ficha del lead.
- Pantalla de entrada por PIN.
- Conectar datos reales con Supabase. Responsivo (funciona en celular).
- SOLO las features del MVP. Diseño según `/ui-reference`.
**Stack:** HTML, JS, CSS (Inter). Sin frameworks pesados.

## AGENTE 2 — BASE DE DATOS Y BACKEND
**Rol:** toda la lógica de datos.
- Crear tablas `leads` y `vendedoras` (ver `spec-crm.md`) con tipos correctos.
- **RLS (Row Level Security) en TODAS las tablas — sin excepción.**
- Funciones serverless (`/api/*.js`) para: guardar lead, listar, cambiar estado, asignar.
- Auto-asignación round-robin 1×1.
- Conectar Sentry para errores.
**Restricciones:** nunca exponer `SERVICE_ROLE` en el frontend. Cada función con manejo de errores.
**Stack:** Supabase, PostgreSQL, Vercel serverless, Sentry.

## AGENTE 3 — ACCESO Y EMAILS
**Rol:** que las asesoras entren y que salgan las comunicaciones.
- **Acceso por PIN** (una clave por vendedora; sin Clerk). Sesión sobre HTTPS.
- **Resend:** correo confirmación (0 min) + correo seguimiento (2h sin contacto). Copy en `correos-resend.md`.
- **Telegram:** aviso al entrar cada lead a la vendedora asignada (bot ya existe).
**Restricciones:** los correos deben funcionar y probarse antes del primer deploy. Compliance vivienda.
**Stack:** Supabase Auth (PIN), Resend, Telegram Bot API.

## AGENTE 4 — DEVOPS Y DEPLOY
**Rol:** que todo funcione en producción.
- Repo Git + rama de trabajo. Deploy en Vercel (preview + producción).
- Cargar TODAS las variables del `.env` en Vercel env.
- Sentry activo antes del primer deploy. Dominio si se provee.
- Mantener este `README.md` con instrucciones de setup.
**Restricciones:** variables de Vercel deben coincidir con `.env`. Preview OK antes de producción.
**Stack:** Git, Vercel, Sentry.

## AGENTE REVIEWER (antes del Pull Request)
No construye. Lee `prompt-maestro.md` + `CONSTITUCION.md`, revisa el código, verifica
convenciones y seguridad (correr `/cso` y `/review` — preguntar a Juan antes). Aprueba o rechaza.

---

## FASE 2 (después del MVP)
- **AGENTE SOPORTE IA:** lee quejas del grupo WhatsApp → cruza Meta + tráfico + CRM →
  redacta respuesta neutral con plan. NO promete features ni precios distintos.
- **AGENTE META ADS:** lee métricas, sugiere optimizaciones. Nunca pausa campañas completas,
  nunca sube presupuesto >30%/día, nada >$100/día sin OK de Juan.

## REGLAS GLOBALES
Las reglas fijas están en `CONSTITUCION.md` (seguridad, datos, negocio, compliance).
Resumen: secretos solo en `.env` · RLS obligatorio · no borrar sin respaldo ·
no tocar campañas vivas · construir con mock data primero · probar antes de seguir ·
preguntar a Juan antes de correr skills · Juan decide, Claude ejecuta.
