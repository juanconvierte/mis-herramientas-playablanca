# ⚖️ CONSTITUCIÓN — Reglas fijas del CRM Playa Blanca

> Reglas que NUNCA se rompen, en TODA sesión de construcción.
> (De la Biblia App Factory: "las reglas fijas van antes del primer prompt".)

## Seguridad (lo más importante)
1. **Secretos SOLO en `.env` o Vercel env.** NUNCA en el HTML/JS público, nunca en el chat, nunca en Git. Proteger con `.gitignore`.
2. **La llave `SUPABASE_SERVICE_ROLE` es la maestra** — solo se usa en el backend (APIs), jamás en el navegador.
3. **Row Level Security ON** — cada vendedora ve solo sus leads. Datos de compradores = datos personales, se cuidan.
4. **HTTPS siempre** (Vercel lo da). Nada de datos por URL.

## Datos
5. **No inventar datos.** Todo claim se verifica contra la data real del cliente. Si no está confirmado → preguntar a Juan.
6. **Nunca borrar data sin respaldo.** Migraciones y cambios de campos con datos adentro → siempre con backup primero.
7. **HubSpot es de solo-lectura** durante la migración. No se borra ni modifica nada allá.

## Negocio (heredado del CLAUDE.md del proyecto)
8. **NO tocar campañas/ads/adsets VIVOS del cliente sin OK explícito de Juan.**
9. **Compliance VIVIENDA (Meta HOUSING):** prohibido en copy/correos → "rentabilidad/plusvalía garantizada", "se paga sola", "sin banco", "escrow/fideicomiso", edad explícita. Solo diferenciales reales.
10. **KPI real = leads CUALIFICADOS** (presupuesto declarado), no CPL barato. La calidad manda.

## Cómo trabaja Claude
11. **Se prueba cada pieza antes de seguir** (verify). No se da nada por hecho.
12. **Ads/features nuevas se crean en PAUSA** salvo que Juan diga "actívalo".
13. **Antes de correr una skill** (`/cso`, `/review`, etc.) → preguntar a Juan (regla del usuario).
14. **Juan dirige, Claude ejecuta con plan por pasos.** En decisiones de negocio, Claude propone; Juan decide.
