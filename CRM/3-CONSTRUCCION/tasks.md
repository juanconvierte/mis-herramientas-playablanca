# ✅ TASKS — Construcción del CRM Playa Blanca

Estados: ⬜ pendiente · 🟨 haciendo · ✅ hecho

---

## FASE 0 — Setup (antes de codear)
- ✅ Escribir `spec-crm.md` (plano maestro)
- ✅ Escribir `CONSTITUCION.md` (reglas)
- ⬜ Juan crea cuenta **Supabase** + proyecto nuevo
- ⬜ Juan crea cuenta **Resend**
- ⬜ Juan llena el `.env` (ver `.env.example`) — SIN pegarlo en el chat
- ⬜ Confirmar los 4 nombres ficticios de vendedoras + sus correos/telegram

## FASE 1 — CRM que guarda leads de verdad
- ✅ Crear tabla `leads` en Supabase
- ✅ Crear tabla `vendedoras` (con PIN de acceso) + notas/tareas/tags
- ✅ Activar Row Level Security (todas las tablas)
- ✅ API de guardado (POST → Supabase) + listar + actualizar
- ⬜ Conectar el formulario de la landing actual a Supabase  ← SIGUE
- ✅ Convertir el demo Kanban en real (lee/escribe Supabase)
- ✅ Entrada por PIN (login simple por vendedora)
- ✅ Auto-asignación round-robin 1×1
- ✅ PRUEBA: lead → cae en Supabase → aparece en el Kanban (verificado en vivo)

## FASE 2 — Automatización (la magia)
- ⬜ Auto-asignación round-robin 1×1
- ⬜ Conectar Resend + escribir copy del correo (Claude redacta, Juan aprueba)
- ⬜ Regla: 2h sin contactar → correo automático
- ⬜ Conectar avisos de Telegram al CRM
- ⬜ PRUEBA: lead → asigna → correo → Telegram ✋ (Juan aprueba)

## FASE 3 — Migración + paralelo
- ⬜ Script `migrar-hubspot.js` (Claude lo corre)
- ⬜ Migrar histórico HubSpot → Supabase (verificar que el conteo coincida)
- ⬜ Correr CRM + HubSpot en paralelo (1–2 semanas de prueba)
- ⬜ (Futuro, con OK de Juan) apagar HubSpot → ahorro $900/mes

## FASE 4 — Confiable + vendible (SaaS)
- ⬜ Agregar Sentry (monitoreo de errores)
- ⬜ Auditoría de seguridad `/cso` (preguntar antes)
- ⬜ Revisión de código `/review` (preguntar antes)
- ⬜ Checklist "CRM confiable" reutilizable
- ⬜ Convertir en plantilla para vender a otras microempresas

---

## Deuda / preguntas abiertas
- Dominio de correo de salida (Juan lo define)
- Etapas extra exactas (No contestó, Atendió llamada, ...) — Juan las precisa
- ¿Panamá y Colombia en el mismo CRM o separados?
