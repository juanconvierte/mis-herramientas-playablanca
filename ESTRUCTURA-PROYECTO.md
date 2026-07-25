# 🗺️ ESTRUCTURA DEL PROYECTO — Playa Blanca (mapa maestro)

> Generado por Claude el 2026-07-01. **Re-verificado contra disco el 2026-07-20.** Este archivo es tu MAPA. Si te sientes perdido, lee esto primero.
> **✅ REORGANIZADO jul 2026** — carpeta limpia y pro (ver `README.md`). Todo lo vivo está en la raíz. ⚠️ Queda un residual: `Playa Blanca/asistente/logs/` (4 logs muertos) — la carpeta vieja no se borró del todo.

## 0) Estructura ACTUAL (verificada 2026-07-20)
```
META ADS/
├── README.md · CLAUDE.md · ESTRUCTURA-PROYECTO.md · .env · .gitignore
├── MAPA-AGENTE-WHATSAPP.html   🗺️ diagrama del vigía WhatsApp
├── web-panama-LIVE/        🟢 Panamá vivo (landing + paneles CRM + 13 APIs + emails/)
├── landing-colombia-full/  🟢 Colombia vivo (espejo, con su api/)
├── motor-creativos/        🎨 motor Python de imágenes 1080x1920
├── plataforma-creativos/   🎨 versión web del motor (studio.py + render_*.py)
├── asistente/              🤖 bot Telegram + scripts + leads_db.json
├── CRM/                    🗄️ CRM propio futuro (1-DEMO · 2-PROPUESTA · 3-CONSTRUCCION)
├── fotos/                  📸 proyecto · muestras_ia · creativos
├── emails/                 ✉️ plantillas de correo (raíz)
├── exports/                📊 Excel/CSV compradores (retargeting/exclusión Meta)
├── docs/                   📄 ~24 archivos (.md, xlsx, csv, blueprints, propuesta/)
├── _ARCHIVO/               📦 respaldos (landings OLD, web-prueba, backups, Playa-Blanca-residual-jul)
└── Playa Blanca/           ⚠️ RESIDUAL — solo asistente/logs/ (borrar/mover con OK)
```
_web-panama-LIVE (paneles): `index.html`+`gracias.html` (landing) · `crmceo.html`·`crmdataplayablanca.html`·`paneljuan.html`·`war-room.html`·`dashboard-leads.html` (CRM) · `agente.html`·`oficina-habbo.html` (oficina IA) · `privacidad.html` · reportes. api/ (13): crm·hs-webhook·conversion·meta-events·vigia·wa-lead-poll·wa-grupo·reporte·parte·leads·panel·tg-bot·_excel._
_Lo de abajo (§1-§5) es el estado ANTES de reorganizar — histórico de por qué se decidió cada movida._

---

## 1) Qué hay hoy (3 carpetas grandes)

### 🟢 `web-panama-LIVE/` (424 MB) — **LO QUE ESTÁ VIVO EN VERCEL**
La web de Panamá + todo el sistema CRM/IA. **Esta es la carpeta canónica, la que importa.**
- `index.html` — landing de conversión (form + pixel + CAPI)
- `crm.html` — panel CRM (leads, **Reporte de Valor**, herramientas, webs)
- `api/` — 11 funciones serverless:
  - `crm.js` (leads por campaña) · `reporte.js` (Reporte de Valor + embudo) · `ai-brief.js` (brief IA Gemini gratis)
  - `conversion.js` (CAPI) · `leads.js` · `hs-webhook.js` (Telegram) · `dash-gate.js` (portón dashboard)
  - `status-am.js` / `status-pm.js` (crons Telegram) · `lib/status-lib.js`
  - `dash-<random>.html` — copia del Dashboard CEO con token (protegido por clave)
- `vercel.json` — deploy (CSP, crons, rewrites)
- `node_modules/`, `.git/`, `.vercel/` — necesarios, no tocar
- Secrets → **solo en Vercel env vars, NO en archivos** ✅

### 🟡 `Playa Blanca/` (1.1 GB) — **CARPETA VIEJA / TALLER LOCAL**
Todo lo que se construyó localmente antes de migrar a Vercel. Mucho está DUPLICADO con la de arriba.
- `dashboard.html` (420K) — panel CEO local (su copia vive ya en Vercel como dash-gate)
- `asistente/` — bot Telegram + scripts Python + **`leads_db.json`** (⚠️ base de leads local, respaldo)
- `motor_creativos/` (530M) — motor de imágenes 1080x1920 + bibliotecas de fotos
- `landing-panama-web/` (399M) — **copia local vieja** de la web Panamá (la viva es `web-panama-LIVE/`)
- `landing-colombia-full/` (8.4M) — **web Colombia VIVA** (esta sí sirve)
- `landing-colombia/` (1.6M) — versión vieja de Colombia (reemplazada por la de arriba)
- `web-prueba/` (3.3M) — prototipo de pruebas
- `fotos_proyecto/a/` (138M) — 111 fotos fuente del proyecto
- Docs: `ESTADO-PROYECTOS.md`, `README.md`, `AGENDA-REUNION-CLIENTE.md`, blueprints, etc.

### 🎨 `CREATIVOS/` (386 MB)
Assets creativos / fotos generadas.

---

## 2) Qué YA limpié (2026-07-01)

**Borrado de verdad (verificado inútil, no afecta nada vivo):**
- ✅ 8 × `.DS_Store`, 3 × `__pycache__/`, 3 × `__MACOSX/` (cruft, se regenera)
- ✅ `web-panama-LIVE/_zip_imgs/` (384M) — 0 referencias en el sitio + estaba en `.vercelignore` (no se despliega)
- ✅ `web-panama-LIVE/_thumbs/` (4.3M) — thumbnails regenerables + vercelignored

**Movido a `_ARCHIVO/` (respaldo intacto, borrable después):**
- 📦 `landing-panama-web-OLD/` (399M) — copia local vieja de Panamá (la viva es `web-panama-LIVE/`)
- 📦 `landing-colombia-OLD/` — Colombia vieja (la viva es `landing-colombia-full/`)
- 📦 `web-prueba/` — prototipo de pruebas
- 📦 `dashboard.backup-*.html` (2) — respaldos viejos del dashboard

**Resultado:** 1.9G → **1.5G**. `_ARCHIVO/` pesa 405M (si confirmas, se borra y quedas en ~1.1G).

---

## 3) EL PROBLEMA: duplicación (por esto se siente desordenado)

Hay ~800 MB de cosas repetidas en 2-3 lugares. Tu carpeta refleja tu cabeza: todo bueno, pero regado.

| Duplicado | Dónde | Veredicto |
|---|---|---|
| Web Panamá | `web-panama-LIVE/` (viva) **vs** `Playa Blanca/landing-panama-web/` (399M, vieja) | La vieja probablemente sobra |
| Web Colombia | `landing-colombia-full/` (viva) **vs** `landing-colombia/` (1.6M, vieja) | La vieja sobra |
| Biblioteca de imágenes (~109 fotos) | aparece en `motor_creativos/`, `web-panama-LIVE/_zip_imgs/a/` (384M), `fotos_proyecto/a/` | 2-3 copias de lo mismo |
| Backups dashboard | `dashboard.backup-*.html` (2 × ~480K) | Respaldos viejos |

---

## 4) ESTRUCTURA LIMPIA recomendada (el "por qué")

**Principio:** UNA sola carpeta por cada cosa viva. Todo lo viejo → a `_ARCHIVO/` (respaldo, NO se borra).

```
META ADS/
├── CLAUDE.md                  ← reglas del proyecto
├── ESTRUCTURA-PROYECTO.md     ← este mapa
├── web-panama-LIVE/           ← Panamá vivo (canónico)
├── landing-colombia-full/     ← Colombia vivo (mover aquí)
├── motor-creativos/           ← motor de imágenes (mover aquí)
├── asistente/                 ← bot/scripts + leads_db.json (mover aquí)
├── fotos/                     ← UNA biblioteca de imágenes (deduplicada)
├── docs/                      ← todos los .md juntos
└── _ARCHIVO/                  ← todo lo viejo (respaldo intacto)
    ├── landing-panama-web-OLD/
    ├── landing-colombia-OLD/
    ├── web-prueba/
    └── dashboard-backups/
```

**Por qué mejora todo:** abres la carpeta y en 5 segundos sabes qué está vivo (raíz) y qué es historia (`_ARCHIVO/`). Cero confusión sobre "cuál es la buena". Cuando llegue tu cliente #2, copias `web-panama-LIVE/` como plantilla.

---

## 5) Candidatos a limpiar (REQUIEREN TU OK — no toco sin permiso)

| Acción | Espacio liberado | Riesgo |
|---|---|---|
| Mover `Playa Blanca/landing-panama-web/` → `_ARCHIVO/` | ~399M | Bajo (la viva es `web-panama-LIVE/`) |
| Borrar `web-panama-LIVE/_zip_imgs/a/` (imgs sin procesar) | ~384M | Bajo (no se usan en el deploy) |
| Mover `landing-colombia/` (vieja) → `_ARCHIVO/` | ~1.6M | Bajo |
| Deduplicar biblioteca de imágenes a 1 sola copia | ~200M+ | Medio (verificar antes) |
| Mover `dashboard.backup-*.html` → `_ARCHIVO/` | ~1M | Cero |

---

## 6) ⚠️ Seguridad (verificar)
- `Playa Blanca/landing-colombia/.env.capi-colombia` — token CAPI Meta en texto plano. Confirmar que NO esté en un deploy público / repo. Si hay duda → rotar.
- `Playa Blanca/.env` — META_ACCESS_TOKEN, META_APP_SECRET, GEMINI_API_KEY. Mantener fuera de cualquier deploy.
- `web-panama-LIVE/` — ✅ limpio, todos los secrets en Vercel env.

---

## 7) Estado real del negocio (del reporte en vivo, 30 días)
- Inversión ~$3,190 · ~200 leads · CPL ~$15.5 (subió 20% por MOTR)
- **Embudo: 98% gestionados.** Solo 5 sin tocar. Pero **79 no localizables (40%)** ← el problema a atacar.
- Ventas/ROAS: pendiente (Paso 2 = poder marcar ventas → Supabase).
