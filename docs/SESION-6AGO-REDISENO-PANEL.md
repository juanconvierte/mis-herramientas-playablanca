# Bitácora · 6-ago-2026 — Rediseño del panel + 2º negocio (Hoteles)

**Todo desplegado y verificado en producción.** Repo `playablanca-panama` (carpeta `web-panama-LIVE/`).
Panel: `panama.playablancaresidences.com/ceoapp1409`

---

## Cómo quedó el menú

```
INICIO
  🏠 Mi Centro Residences    ← antes "Mi Centro"
  🏨 Mi Centro Hoteles       ← NUEVO (2º negocio)
CRM
  📥 Leads · Formulario      ← ahora incluye el Reporte de Valor y las webs
PANELES
  🎯 Panel de Juan
  🕹️ Agente WhatsApp
```

Desaparecieron del menú: **Reporte de Valor**, **Web Panamá**, **Web Colombia** — no se borraron, se absorbieron dentro de Leads · Formulario.

---

## 1. Leads · Formulario — de listas a dash

**Antes:** cada campaña se desplegaba en una tabla con nombre, teléfono y correo de cada lead.
**Ahora:** una tarjeta por campaña con nº de leads, cuántos entraron hoy, último día con actividad, **compradores +$300K y su %**, y cuántos siguen sin gestionar. Cero listas de nombres. Botón *"Ver leads uno por uno ↗"* → `/crmdataplayablanca`.

**Detalle que importa:** la bandera de cada campaña **se deduce del prefijo telefónico real de sus leads** (+507 Panamá / +57 Colombia), no del nombre de la campaña. El nombre miente: "MOTR" es Colombia y no lo dice por ningún lado.

**Formulario de la web** — bloque nuevo con una tarjeta por página (Panamá / Colombia), alimentado por `/api/leads?origen=Landing Panamá|Landing Colombia`. Sustituye a las dos secciones del sidebar.

---

## 2. Reporte de Valor: adentro y atado al filtro

Ya no es una sección aparte. Vive dentro de Leads · Formulario en dos alturas:
- **Debajo del filtro:** las cifras de plata — inversión, leads, compradores +$300mil, costo por comprador, CPL, % gestionados. Con botón **⬇ Exportar / Imprimir**.
- **Más abajo:** el detalle — embudo por estado, calidad por presupuesto, alertas de sin-gestionar y no-localizables, desglose por campaña.

**El filtro de fechas ahora manda sobre el reporte.** Tocar *7 días* recalcula **inversión y leads juntos**. Verificado: 30 días → $5,130 / 271 leads · 7 días → $1,197 / 63 leads.

Dos límites conocidos, por cómo funciona `/api/reporte`:
- **"Todos" pide 365 días** — es el tope de la API. Gasto más viejo que un año no entra.
- **Rango personalizado:** la API solo cuenta días hacia atrás desde hoy. Si pones *Hasta* en una fecha pasada, el reporte llega igual hasta hoy. El subtítulo siempre muestra el periodo real que se está usando.

Al imprimir sale **solo** el reporte, con el nombre del cliente arriba y sin sidebar ni tarjetas — funcione desde la vista que funcione.

---

## 3. Dos embudos en `/crmdataplayablanca`

El embudo único se partió en dos, lado a lado:
- **Embudo · Formulario interno** — formulario instantáneo de Meta (el lead nunca sale de Facebook/Instagram).
- **Embudo · Formulario de la web** — con selector **Ambas páginas / Página Panamá / Página Colombia**.

Al tocar una etapa, la tabla filtra **también por la fuente** de ese embudo, y el chip lo indica ("Etapa: Contactados · Formulario de la web").

### 🔑 El separador es `origen_formulario`
Campo de HubSpot que ponen las dos landings al enviar el formulario: `"Landing Panamá"` / `"Landing Colombia"`. **Si no lo trae → es formulario instantáneo de Meta.**

`api/crm.js` ahora expone en ambos payloads:
| Campo | Valores |
|---|---|
| `fuente` | `"web"` \| `"interno"` |
| `origen` | el `origen_formulario` crudo |
| `web_pagina` | `"PA"` \| `"CO"` \| `""` |

⚠️ **También se relajó `esFormLead()`**: ahora acepta un lead con `origen_formulario` de landing aunque no traiga etiqueta de campaña (entró directo/orgánico a la página). Antes esos se caían del panel. **El total puede haber subido — no son leads nuevos, son reales que no se estaban viendo.**

---

## 4. Mi Centro Hoteles (2º negocio)

Ver el manual completo en **`docs/PANEL-HOTELES.md`**. Resumen:

- Cuenta `act_562075948235993` "Playa Blanca Hotel" · BM `385598385556249` · app "Playa Blanca Hoteles" · token System User "Dashboard" en `META_TOKEN_HOTELES`.
- Panel de Meta Ads: 8 cifras con su variación contra el periodo anterior, selector 7/30/90 días, y tabla de campañas **solo activas** (nada de pausadas ni finalizadas), con las fugas en rojo.
- **Aquí el norte son RESERVAS y ROAS**, no leads cualificados. No hay HubSpot detrás.

**Los accesos de cada centro se guardan por separado** en el navegador: `pb_links_v2` (Residences) vs `pb_links_hot_v1` (Hoteles). Editar uno no toca al otro y no se puede arrastrar un acceso de un centro a otro. Los KPIs de leads y el recorrido del día siguen siendo **solo de Residences**.

---

## 🚨 Las dos trampas que casi muerden

### 1. Vercel Hobby = 12 Serverless Functions, y ya están las 12
Agregar **un** archivo en `api/` congela **todos** los despliegues del sitio (`exceeded_serverless_functions_per_deployment`). Pasó el 5-ago con `api/vigia-30.js`: la producción quedó clavada en el build del 3-ago con el parte diario de WhatsApp caído.

**Regla:** lógica nueva va en un helper **`api/_nombre.js`** (Vercel excluye los `api/_*`, no cuentan) colgado de un endpoint que ya exista. Así se hizo con `api/_hoteles.js` → `/api/panel?negocio=hoteles`.

```bash
ls api/*.js | grep -v '/_' | wc -l    # cuenta las que cuentan. Tope: 12
```

### 2. Meta reporta la misma compra bajo varios nombres
`omni_purchase`, `web_in_store_purchase` y `offsite_conversion.fb_pixel_purchase` devolvían **47, 47 y 47 — la misma reserva**. Sumarlos infla las reservas ×3 y el ROAS es mentira. Cada métrica usa **un tipo canónico** y no se suman entre sí.

---

## Commits de la sesión

| Commit | Qué hizo |
|---|---|
| `4e16c26` | Leads · Formulario resumido tipo dash + 2 embudos separados |
| `c51e138` | Reporte de Valor dentro de Leads · Formulario, atado al filtro de fechas |
| `4126978` | Mi Centro Residences + Mi Centro Hoteles con accesos propios |
| `20259de` | Panel de Meta Ads del hotel |
| `660e128` | Republica para tomar `META_TOKEN_HOTELES` |
| `a2384b7` | La tabla del hotel lista solo campañas activas |

*(De otra sesión en paralelo, sin conflicto: `cc1988c` vigía-30, `cb133fd` fix wa-grupo, `7a2f89f` + `c2252b4` liberar slot de función.)*

Doc del hotel: `00a3307` en el repo privado `mis-herramientas-playablanca` — **commiteado local, sin push** (ese repo es push manual).

---

## ⏭️ Pendientes al cerrar

1. **Rotar el token de Hoteles.** Se pegó en un chat el 6-ago → comprometido. Es permanente y trae `ads_management` (escritura sobre campañas) que el panel no necesita. El nuevo: solo `ads_read` + `business_management`. Cambiarlo en Vercel y **republicar** (los builds ya hechos no recogen una env nueva).
2. **Push del repo de docs** si se quiere respaldar `docs/PANEL-HOTELES.md` y este archivo.
3. **Viene de antes:** que las columnas Alta/Media/Baja del tablero de prioridad en `/crmdataplayablanca` filtren la tabla al click, como ya hace el embudo.

## 💡 Lo que dicen los datos, para cuando haya tiempo

**Hotel (30 días):** $11,928 → **47 reservas** por $18,624 → **ROAS 1.56**. Contra el mes previo: reservas **+96%**, ROAS **+280%**, gastando 9% menos.
**La fuga:** 31 de 78 campañas con gasto no trajeron ni una reserva. Patrón claro — **WhatsApp y llamadas convierten** (`WS_COLOMBIA12%` 4.20x, `CALLS_DAYPASS` 4.12x), **las de tráfico a web gastan y no cierran**. Ahí hay presupuesto que mover.

---

## Cómo verificar que todo sigue vivo

```bash
curl -s -o /dev/null -w '%{http_code}\n' https://panama.playablancaresidences.com/ceoapp1409
curl -s -o /dev/null -w '%{http_code}\n' https://panama.playablancaresidences.com/crmdataplayablanca
```

```bash
cd "/Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/web-panama-LIVE" && ls api/*.js | grep -v '/_' | wc -l
```

**Recordatorio de despliegue:** siempre `git add -A && git commit && git push origin main` (Vercel publica solo + GitHub respalda). Nunca `vercel --prod` suelto. Y antes de tocar: `git fetch && git status`, que el proyecto está abierto en varios chats a la vez.
