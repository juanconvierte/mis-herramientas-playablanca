# PROMPT-MAESTRO — CRM Playa Blanca

> Archivo maestro de la Biblia App Factory. Es el "brief" que activa a Claude Code
> para construir. Adaptado al proyecto real (NO es la app SaaS genérica de la Biblia).

## OBJETIVO
Construir un CRM propio para Playa Blanca Residences que reemplace HubSpot ($900/mes).
Optimizado para 4 asesoras de venta. ~500 leads/mes. Simple, confiable, a medida.

## STACK (leer CONSTITUCION.md para las reglas completas)
- **Frontend:** HTML + JS + CSS (mismo enfoque que `web-panama-LIVE`, NO Next.js).
- **Base de datos:** Supabase (Postgres) + Row Level Security.
- **Backend:** funciones serverless en Vercel (`/api/*.js`).
- **Login:** PIN por vendedora (NO Clerk).
- **Correos:** Resend. **Avisos:** Telegram (bot ya existe).
- **IA:** Claude / Gemini (agente de soporte, fase 2).
- **Monitoreo:** Sentry. **Hosting:** Vercel.
- **Pagos:** NINGUNO (un CRM no cobra; se descarta Shopify/Stripe de la Biblia).

## FUNCIONALIDADES DEL MVP (máximo 4, con prioridad)
1. **[ALTA]** Captura de lead: el form de la landing actual escribe a Supabase.
2. **[ALTA]** Pipeline Kanban con login por PIN (cada asesora ve solo sus leads).
3. **[ALTA]** Auto-asignación round-robin 1×1 al entrar cada lead.
4. **[MEDIA]** Automatización: correo Resend a las 2h sin contacto + aviso Telegram.

## LAS 4 ACCIONES QUE MUEVEN LA AGUJA
- **Genera revenue:** el CRM propio es lo que le cobras $500/mes al cliente.
- **Retiene usuario:** auto-asignación + Kanban simple → las asesoras lo adoptan.
- **Reduce soporte:** una sola pantalla, sin curva (vs. HubSpot enredado).
- **Escala sola:** lead entra → asigna → correo → aviso, sin intervención manual.

## DISEÑO
- Referencia visual: `../1-DEMO/index.html` (estilo Kanban tipo Excermol, YA aprobado).
- Colores: indigo `#6d5ef0` · teal `#12b3a6` · navy `#0e1630`. Fondo `#f6f7fb`.
- Tipografía: Inter. Estilo: limpio, tarjetas redondeadas, columnas con borde de color.
- Ver `/ui-reference` para el detalle.

## IA DE LA APP
- Proveedor: Claude / Google AI Studio (Gemini).
- Para qué: agente de soporte que lee quejas del grupo + cruza Meta+CRM (FASE 2).

## RESTRICCIONES (qué NO hacer)
- No agregar features fuera de las 4 del MVP.
- No usar Clerk, Shopify ni Stripe (no aplican).
- **No tocar campañas/ads vivos del cliente** ni apagar HubSpot sin OK de Juan.
- Cumplir compliance VIVIENDA en todo copy (ver CONSTITUCION.md).
- Seguir TODAS las reglas de CONSTITUCION.md.

## REPOS / REFERENCIAS
- `../../web-panama-LIVE/` — el CRM actual (crm.html + api/crm.js). Mismo patrón de código.
- `../1-DEMO/` — el diseño Kanban objetivo.
- `spec-crm.md` — la especificación detallada (tablas, pantallas, flujo).

## INSTRUCCIONES DE EJECUCIÓN
1. Leer CONSTITUCION.md primero.
2. Leer `spec-crm.md` (la especificación completa).
3. Leer el `.env` (todas las keys están ahí).
4. Construir con **mock data primero**, verificar diseño, LUEGO conectar Supabase real.
5. Probar cada pieza antes de seguir (verify). No dar nada por hecho.
6. Correr HubSpot en paralelo (no apagar).
7. Al terminar cada fase: registrar en `history.md` + avisar a Juan para aprobar.

## CRITERIOS DE ACEPTACIÓN
- [ ] Form de la landing → guarda lead en Supabase.
- [ ] Login por PIN funciona; cada asesora ve solo lo suyo (RLS).
- [ ] Las 4 features del MVP funcionan.
- [ ] Auto-asignación round-robin reparte 1×1.
- [ ] Correo Resend (2h) + aviso Telegram funcionan.
- [ ] Deploy en Vercel con URL pública + Sentry conectado.
- [ ] RLS activo en TODAS las tablas.
- [ ] Migración HubSpot verificada (conteo coincide).
