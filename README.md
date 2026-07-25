# 🏖️ Playa Blanca Residences — Sistema de Media Buying + CRM

Sistema completo de adquisición de leads para **Playa Blanca Residences** (inmobiliaria de lujo, Pacífico de Panamá). Meta Ads → landings de conversión → CRM en vivo → notificaciones IA. Todo en Vercel, 24/7, sin depender de una máquina local.

> **Objetivo del negocio:** leads **cualificados** (compradores potenciales con presupuesto real), no volumen barato.
> **Cómo ganamos:** demostrar valor con datos → embudo, CPL, calidad de lead y (pronto) ROAS real.

---

## 📁 Estructura

```
META ADS/
│
├── 🟢 VIVO EN VERCEL (no mover — enlazado a deploys)
│   ├── web-panama-LIVE/     Web Panamá VIVA + CRM actual + APIs — el corazón
│   │   ├── index.html       landing de conversión (form + pixel + CAPI)
│   │   ├── crm.html         panel CRM actual (leads, Reporte de Valor)
│   │   └── api/             serverless: crm · reporte · ai-brief · conversion · webhooks
│   └── landing-colombia-full/  Web Colombia VIVA (espejo, ángulo retiro/dólares)
│
├── 🆕 CRM/                  PROYECTO CRM PROPIO (reemplazo de HubSpot) — ver CRM/LEEME.md
│   ├── 1-DEMO/             demo Kanban interactivo (herramienta de venta)
│   ├── 2-PROPUESTA/        propuesta visual + guion de reunión (cerrar $1.400/mes)
│   └── 3-CONSTRUCCION/     el plano: spec · constitución · tareas · checklist · correos · .env.example
│
├── 🎨 CREATIVOS Y CONTENIDO
│   ├── motor-creativos/    Motor Python de imágenes 1080x1920 (foto + copy IA)
│   ├── plataforma-creativos/  plataforma de creativos (en desarrollo)
│   └── fotos/              Biblioteca de imágenes (proyecto, muestras IA, creativos)
│
├── 🤖 asistente/           Bot Telegram + scripts + leads_db.json (histórico local)
├── 📄 docs/                Toda la documentación (.md, exports, blueprints)
├── 📦 _ARCHIVO/            Versiones viejas / respaldos (no borrar sin OK)
├── ⚠️ Playa Blanca/        Carpeta residual del reorg — revisar y archivar/borrar con OK
│
├── 🧠 CLAUDE.md            Reglas del proyecto (compliance, campañas, convenciones)
├── 🗺️ ESTRUCTURA-PROYECTO.md  Mapa maestro detallado
└── 🔑 .env                 Secretos (gitignored)
```

## 🔴 Qué está VIVO (en Vercel)
- **Panamá:** `panama.playablancaresidences.com` (landing + CRM `/crm` + Reporte de Valor + brief IA diario)
- **Colombia:** landing desplegada (campaña pendiente de lanzar)
- **Crons:** reportes Telegram (mañana/tarde) + brief IA (Gemini gratis)

## 🧰 Stack
Vercel (serverless + cron) · HubSpot CRM API · Meta Graph API (Ads + CAPI) · Telegram Bot API · Gemini (brief IA gratis) · Python (motor creativos)

## ✅ Cómo verificar
- Landing viva: `curl -s -o /dev/null -w '%{http_code}' https://panama.playablancaresidences.com/` → 200
- Lead real (Meta) = action_type `onsite_conversion.lead_grouped` (NO sumar todo lo que diga "lead")
- Secretos: solo en `.env` / `config.json` / Vercel env — nunca en HTML público

## 🔒 Seguridad
Todos los tokens viven en Vercel env vars o `.env` (gitignored). El dashboard CEO con token embebido está protegido por clave (`api/dash-gate`). Ver `CLAUDE.md`.
