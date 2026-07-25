# 📧 Sistema de Correos — Playa Blanca (Resend)

Hub de documentación del sistema de correos. **Las plantillas VIVAS viven en `web-panama-LIVE/emails/`** (de ahí se sirven/despliegan en Vercel). Este README es el mapa.

---

## Las 5 plantillas

| # | Archivo | Etapa | Asunto |
|---|---------|-------|--------|
| 1 | `01-bienvenida.html` | Apenas entra el lead | Bienvenido a Playa Blanca Residences |
| 2 | `02-seguimiento.html` | No contestó / no lo ubicamos | Seguimos a su disposición — Playa Blanca |
| 3 | `03-proyecto.html` | Nutrir / mostrar valor | Un rincón del Pacífico, pensado para usted |
| 4 | `04-cita.html` | Agendar visita | Le invitamos a conocer Playa Blanca en persona |
| 5 | `05-reactivacion.html` | Lead frío / última oportunidad | Su lugar frente al mar lo sigue esperando |

- **Ubicación real:** `web-panama-LIVE/emails/*.html` (email-safe: tablas, estilos inline, Georgia+Arial).
- **Preview en vivo:** https://panama.playablancaresidences.com/emails/preview
- **Diseño:** navy #1B2F4B + dorado #B8933F + logo blanco (desde `panama.playablancaresidences.com/logo-white.png`). Cumple compliance vivienda (sin plusvalía/rentabilidad garantizada).

---

## Resend — estado (12-jul-2026)

- **Cuenta:** juanconvierte@gmail.com · plan **Free** (3,000 correos/mes, 100/día, 1,000 contactos, **1 dominio**).
- **API key:** creada (`re_...`) y guardada en Vercel → env **`RESEND_API_KEY`** (proyecto `landing-panama`, Production, cifrada). NO está en ningún HTML.
- **Dominio:** ⏳ PENDIENTE de verificar. Hay que agregar `playablancaresidences.com` en Resend → Domains → te da registros DNS (SPF/DKIM/return-path `send.` + tracking `links.`) → los pega el admin del **GoDaddy** del cliente. Un solo dominio raíz cubre Panamá y Colombia.
  - ⚠️ El tracking subdomain NO debe ser `panama` (colisiona con la landing/panel viva). Usar `links`.
- **SMTP (alternativo, no lo usamos):** host `smtp.resend.com` · port `465` · user `resend` · pass = la API key.

---

## Cómo se enviarán (2 caminos)

- **A) Automático por etapa** (piloto automático): construir `web-panama-LIVE/api/mail.js` (REST API de Resend, key del env) + disparo por cron/webhook de HubSpot. Marcar propiedad en HubSpot (ej `bienvenida_enviada`) para no duplicar. **PENDIENTE de construir** (esperando OK de Juan).
- **B) Masivo manual** (sin código): Resend → Audiences (subir CSV) → Broadcasts → pegar HTML → enviar.

**Probar sin dominio:** se puede enviar desde el dominio de prueba de Resend (`onboarding@resend.dev`) al propio correo de Juan para validar antes de tener el dominio.

---

## Variables de entorno del proyecto `landing-panama` (Vercel) — solo NOMBRES

| Env | Para qué |
|-----|----------|
| `RESEND_API_KEY` | enviar correos (Resend) — **nuevo** |
| `PANEL_KEY` | clave del panel del CEO `/crmceo` (= `ralph-ceo-pb-7q29`) |
| `HUBSPOT_TOKEN` | leer contactos/leads HubSpot |
| `META_ADS_TOKEN` | insights de campañas Meta |
| `CRM_KEY` / `DASH_KEY` | proteger APIs internas (/api/crm, /api/reporte, /api/panel) |
| `TELEGRAM_BOT_TOKEN` / `TG_BOT_DS` / `TG_CHAT_JUAN` / `TG_GROUP` / `TG_WEBHOOK_SECRET` | bot Telegram (oficina IA) |
| `GEMINI_KEY_FREE` | IA gratis |
| `META_ACCESS_TOKEN` | CAPI conversiones |
| `MONTHLY_BUDGET` / `CRM_NOTIFY_CAMPAIGNS` | config vigía/reportes |

> Los VALORES son secretos → viven solo en Vercel env (`vercel env ls`), nunca en archivos.

---

## Próximos pasos
1. Verificar dominio en Resend (DNS GoDaddy).
2. Construir `/api/mail.js` + probar a correo propio.
3. Conectar disparo por etapa (HubSpot) + dedup.
