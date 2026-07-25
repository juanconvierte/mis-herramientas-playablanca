# 🛡️ CHECKLIST "CRM CONFIABLE" — reutilizable para vender a microempresas

> Se corre ANTES de entregar/vender cualquier CRM. Traduce lo que cuida HubSpot
> (empresa enterprise) a la versión micro, verificable, para negocios de ~500 leads/mes.
> Basado en el estudio real de la infraestructura de HubSpot (jul-2026).
> Estados: ⬜ pendiente · ✅ hecho · ⚠️ revisar

---

## Idea central (la verdad honesta)
La distancia entre HubSpot y un CRM pequeño **NO es la seguridad de base — es la ESCALA**.
Supabase y Vercel corren sobre la misma nube (AWS) con SOC 2, cifrado y respaldos.
Un CRM micro **bien construido hereda esa base**. Lo que HubSpot tiene extra (equipo de
seguridad 24/7, certificaciones propias, SLAs enterprise) es **innecesario** para una
inmobiliaria de 500 leads/mes. La confiabilidad depende de **disciplina**, no de tamaño.

---

## PILAR 1 — Los datos NUNCA se pierden
- ⬜ Base en **Supabase** (Postgres administrado con respaldos automáticos)
- ⬜ Respaldo verificado: existe copia recuperable (point-in-time en plan Pro)
- ⬜ Antes de cualquier migración o cambio de campo con datos → **backup manual primero**
- ⬜ HubSpot en paralelo hasta confirmar que nada se pierde (red de seguridad)
- **Cómo cuida HubSpot:** todo cifrado, en DBs + sistemas de respaldo.

## PILAR 2 — Cada quien ve SOLO lo suyo (aislamiento)
- ⬜ **Row Level Security (RLS) activado** en Supabase
- ⬜ Vendedora con su PIN ve solo sus leads asignados
- ⬜ Admin (dueño) ve todo; vendedora NO ve leads de otra
- ⬜ Probado: entrar con PIN de vendedora A y confirmar que no aparecen leads de B
- **Cómo cuida HubSpot:** arquitectura multi-tenant (aísla 200.000+ empresas entre sí).

## PILAR 3 — Conexión y datos cifrados
- ⬜ **HTTPS** en todo (Vercel lo da automático)
- ⬜ Cifrado en reposo (Supabase lo trae por defecto)
- ⬜ Cifrado en tránsito (TLS)
- ⬜ Cero datos personales en la URL / parámetros
- **Cómo cuida HubSpot:** cifrado en reposo Y en tránsito, siempre.

## PILAR 4 — Secretos protegidos
- ⬜ Tokens/keys SOLO en `.env` o Vercel env (nunca en el navegador, Git o chat)
- ⬜ `.env` en `.gitignore` (verificar que no se subió)
- ⬜ `SERVICE_ROLE` de Supabase solo en backend, jamás en frontend
- ⬜ Grep del código público buscando fugas: `grep -rniE "eyJ|re_|sk_|token|secret" *.html`
- **Cómo cuida HubSpot:** gestión de secretos + separación backend/frontend estricta.

## PILAR 5 — No se cae + si algo falla, avisa
- ⬜ Hosting en Vercel (99.9%+ uptime) + Supabase (administrado)
- ⬜ **Sentry** conectado (monitoreo de errores en producción)
- ⬜ Cada pieza **probada** antes de subir (verify)
- ⬜ Aviso Telegram si el sistema detecta caída/errores
- **Cómo cuida HubSpot:** 3.000+ microservicios, observabilidad y tooling propio.

## PILAR 6 — Privacidad / datos personales (leads = personas)
- ⬜ Aviso de privacidad en la landing (ya existe `privacidad.html`)
- ⬜ Poder **borrar** un lead a solicitud (derecho del titular)
- ⬜ Consentimiento en el formulario (casilla / texto)
- ⬜ Panamá: considerar **Ley 81 de protección de datos**
- **Cómo cuida HubSpot:** GDPR (EU Cloud Code of Conduct), "GDPR delete", consentimiento.

## PILAR 7 — Autenticación
- ⬜ Login por **PIN por vendedora** (decisión Playa Blanca)
- ⬜ PIN no se comparte; uno por persona
- ⬜ Sesión sobre HTTPS
- ⬜ (Escala) migrar a magic link si crece el equipo

---

## ⚠️ LO QUE NO PODEMOS IGUALAR DE HUBSPOT (decir la verdad al cliente)
No se promete lo que no se puede cumplir. Un CRM micro **NO** ofrece:
- Certificación SOC 2 propia (Supabase/Vercel sí la tienen abajo; nosotros no auditamos).
- Equipo de seguridad 24/7 ni respuesta a incidentes enterprise.
- SLA contractual de uptime con penalizaciones.
- Escala de millones de eventos/segundo.
**Para una microempresa de ~500 leads/mes, nada de eso hace falta.** Se vende confiabilidad
real y honesta: "seguro, respaldado y a tu medida" — no "somos HubSpot".

---

## Auditoría final antes de vender
- ⬜ Correr skill **`/cso`** (auditoría de ciberseguridad) — preguntar a Juan antes
- ⬜ Correr skill **`/review`** (revisión de código)
- ⬜ Repasar los 7 pilares → todo en ✅
- ⬜ Prueba de fuego: 1 lead real de punta a punta sin fallos

---
_Este checklist es un ACTIVO reutilizable: cópialo para cada nueva microempresa cliente._
