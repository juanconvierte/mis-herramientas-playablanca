# 🏨 Panel Hoteles — Playa Blanca Hotel & Resort

**Creado:** 6-ago-2026 · **Estado:** 🟢 VIVO en `/ceoapp1409` → menú **Mi Centro Hoteles**

Segundo negocio dentro del mismo panel. **No es Playa Blanca Residences**: aquí se venden noches de hotel, no propiedades, así que el norte es **RESERVAS y ROAS**, no leads cualificados. No hay HubSpot detrás — todo sale de Meta Ads.

---

## Datos de la cuenta

| Qué | Valor |
|---|---|
| Cuenta publicitaria | `act_562075948235993` · "Playa Blanca Hotel" · USD |
| Business Manager | `385598385556249` · "Playa Blanca Hotel & Resort" |
| App de Meta | "Playa Blanca Hoteles" · app_id `1080275238288900` |
| Token | System User **"Dashboard"** · permanente (no vence) |
| Dónde vive el token | Vercel env **`META_TOKEN_HOTELES`** (proyecto `landing-panama`) |
| Píxel / conjunto de datos | `2608573855963095` |

⚠️ **Rotar el token.** El token original se pegó en un chat el 6-ago → considerarlo comprometido. Al reemplazarlo, generar uno solo con **`ads_read` + `business_management`**. El actual trae también `ads_management` (escritura sobre campañas), que este panel **no necesita**.

---

## 🚨 REGLA DURA: Vercel Hobby = 12 Serverless Functions

**Ya están las 12 ocupadas.** Agregar **un** archivo nuevo en `api/` **congela TODOS los despliegues del sitio** con `exceeded_serverless_functions_per_deployment`.

Ya pasó: el 5-ago entró `api/vigia-30.js`, el conteo saltó a 13 y la producción quedó clavada en el build del 3-ago — con el parte diario de WhatsApp caído. Se arregló renombrando `api/sentry-test.js` → `api/_sentry-test.js` (commit `7a2f89f`).

**Cómo agregar lógica nueva sin romper nada:**
1. Ponerla en un helper **`api/_nombre.js`** — Vercel excluye los `api/_*` y **no cuentan** como función.
2. Colgarla de un endpoint que **ya exista**, con un parámetro.

Así se hizo aquí: `api/_hoteles.js` se sirve desde `/api/panel?negocio=hoteles`. Si algún día hace falta una función de verdad → **Vercel Pro**.

Contar las que cuentan:
```bash
ls api/*.js | grep -v '/_' | wc -l
```

---

## Cómo funciona

**`api/_hoteles.js`** — pide a Meta los insights de la cuenta en tres tiros paralelos: periodo actual, periodo anterior (para el "vs.") y desglose por campaña. Cache en memoria de 5 min por periodo.

**`/api/panel?negocio=hoteles&dias=30`** — el endpoint. Reusa el mismo control de clave del panel (`RALPH_KEY`, `ARIE_KEY`, `CRM_KEY`, `DASH_KEY`); no se inventaron claves nuevas.

**`ceoapp1409.html`** → `viewHoteles`, función `loadHoteles(dias)`. Selector de 7 / 30 / 90 días.

### Lo que muestra
Ocho cifras, cada una con su variación contra el periodo anterior: **inversión · reservas · ROAS (con el valor facturado) · costo por reserva · alcance · conversaciones de WhatsApp · CPM · CTR**.

Debajo, la tabla de campañas por inversión. **Se resalta en rojo la campaña que gastó $100 o más sin traer una sola reserva** — ahí está la fuga.

### Solo campañas activas
La tabla lista **únicamente las que están corriendo** (`effective_status === "ACTIVE"`). Pausadas, finalizadas y archivadas no aparecen.

⚠️ **Por eso la suma de la tabla NO cuadra con la inversión total de arriba**: el gasto de las pausadas ya ocurrió y sigue contando en las cifras. El subtítulo lo dice explícitamente ("no se listan N pausadas/finalizadas, aunque su gasto de $X sí cuenta arriba"). Nunca se esconde plata en silencio.

---

## ⚠️ Doble conteo de compras en Meta

Meta reporta **la misma compra bajo varios `action_type` a la vez**. En esta cuenta, `omni_purchase`, `web_in_store_purchase` y `offsite_conversion.fb_pixel_purchase` devolvían **47, 47 y 47 — son la misma reserva**.

Por eso cada métrica toma **un tipo canónico** y **no se suman entre sí**. Si se sumaran, las reservas saldrían infladas ×3 y el ROAS sería mentira.

| Métrica | Tipo canónico (en orden de preferencia) |
|---|---|
| Reservas | `omni_purchase` → `offsite_conversion.fb_pixel_purchase` → `web_in_store_purchase` → `purchase` |
| Leads | `onsite_conversion.lead_grouped` → `onsite_conversion.lead` → `lead` |
| Conversaciones WhatsApp | `onsite_conversion.messaging_conversation_started_7d` → `..._replied_7d` |
| Llamadas | `click_to_call_callback_request_submitted` → `click_to_call_call_confirm` |

---

## Foto de arranque (30 días al 6-ago-2026)

| Métrica | Valor | vs. mes anterior |
|---|---|---|
| Inversión | $11,928 | ▼ 9.2% |
| **Reservas** | **47** | **▲ 96%** |
| Valor facturado | $18,624 | — |
| **ROAS** | **1.56x** | **▲ 280%** |
| Costo por reserva | $253.64 | ▼ 54% |
| Alcance | 1,485,152 | ▼ 12% |
| Conversaciones WhatsApp | 9,242 | — |
| CPM | $2.25 | ▲ 4.7% |
| CTR | 2.71% | — |

**La cuenta va bien**: casi el doble de reservas gastando 9% menos.

### 🩸 La fuga
De 78 campañas con gasto, **31 no trajeron ni una reserva**. La que más gastó ($1,666) trajo **0** — ya está pausada, pero se llevó la plata. Las pausadas/finalizadas se llevaron **$3,607** del periodo.

### 🏆 Las que sí funcionan
| Campaña | ROAS |
|---|---|
| `PBH_ADS_2026_07_WS_COLOMBIA12%_V1` | **4.20x** |
| `PBH_ADS_2026_07_CALLS_DAYPASS_V1` | **4.12x** |

**Lectura:** WhatsApp y llamadas convierten; las de tráfico a web (`WEB_*`) gastan y no cierran. Ahí hay presupuesto que mover.

---

## Accesos rápidos (en Mi Centro Hoteles)
- [Cuenta publicitaria · Campañas](https://adsmanager.facebook.com/adsmanager/manage/campaigns?act=562075948235993&business_id=385598385556249)
- [Píxeles / Conjunto de datos](https://business.facebook.com/latest/settings/events_dataset_and_pixel/?business_id=385598385556249&selected_asset_id=2608573855963095&selected_asset_type=events-dataset-new)

Los accesos de cada centro se guardan **por separado** en el navegador: `pb_links_v2` (Residences) y `pb_links_hot_v1` (Hoteles). Editar uno no toca al otro, y no se puede arrastrar un acceso de un centro a otro.

---

## Si algo falla

| Síntoma | Causa | Arreglo |
|---|---|---|
| "falta META_TOKEN_HOTELES en las variables de Vercel" | La env no está, o se agregó después del último build | Cargarla en Vercel y **republicar** (los builds viejos no la toman) |
| "clave inválida" | Falta `?key=` o está mal | Es el portero funcionando. Entrar por el panel, no por URL suelta |
| "error Meta: ..." | Token vencido/revocado o sin permiso sobre la cuenta | Regenerar el System User token en la app *Playa Blanca Hoteles* |
| Las cifras no cambian al tocar 7/30/90 | Cache de 5 min | Esperar, o agregar `&fresh=1` a la llamada |
