# Sesión 21-jul-2026 — "Panel de Juan": rename + fix del bug de fondo

Registro completo del trabajo. Todo desplegado a producción (`landing-panama`) y verificado en vivo.

---

## 1. El síntoma que reportó Juan

- "La sala de guerra tiene clave en mi panel."
- "¿Por qué murió lo que estaba y ahora dice Sala de Guerra?"
- Después del rename seguía saliendo un cuadro de clave con error.

## 2. Diagnóstico (qué pasaba de verdad)

### a) Confusión de nombres (3 nombres para lo mismo)
| Dónde se veía | Nombre |
|---|---|
| Botón en la app `/ceoapp1409` | "Mi Panel (Juan)" |
| Título dentro del panel | "Sala de Guerra" |
| Panel viejo, ya muerto (404) | "Panel del Creador" (`/creadorcrm`) |

El panel de media buyer (`paneljuan.html`) siempre se tituló internamente **"Sala de Guerra"** (los backups del 15-jul ya lo decían). En la limpieza del 20-jul se **embebió** dentro de `/ceoapp1409` (blob base64) y se **borraron las rutas sueltas** `/paneljuan` y `/creadorcrm` → ambas dan **404**. Por eso Juan sintió que "murió lo que estaba".

### b) Bug de fondo: el fetch fallaba desde el iframe blob
El panel embebido corre en un **iframe `blob:`**. Adentro hacía `fetch('/api/panel')` con **ruta relativa**. Desde un contexto `blob:` la ruta relativa **no resuelve al dominio real** → el `fetch` tira error → cae en el `catch` de `load()` → muestra el gate con **"No se pudo conectar. Reintenta."**

Eso es lo que Juan interpretaba como "me pide clave". No era clave incorrecta: era el fetch roto. La página principal `/ceoapp1409` sí cargaba (fetch relativo normal en una página https común); solo el **embed blob** fallaba. Bug introducido el 20-jul al pasar de ruta propia a embed blob.

## 3. Cambios aplicados

### Rename → "Panel de Juan" (en todo)
- `web-panama-LIVE/paneljuan.html`: `<title>`, `<h3>` del gate, brand `.ctrl`, pie `.foot` → "Panel de Juan".
- `web-panama-LIVE/ceoapp1409.html`: botón de navegación, `title` del iframe `ifCeo`, y el mapa `_titles.ceo` → "Panel de Juan".

### Fix del blob fetch (URL absoluta)
En `paneljuan.html`, tras la línea de `KEY`, se añadió:
```js
const _API=(/^https?:/.test(location.origin))?location.origin:'https://panama.playablancaresidences.com';
```
y los 2 fetch pasaron a absoluto:
```js
fetch(`${_API}/api/panel?...`)
fetch(`${_API}/api/meta-events?...`)
```
`location.origin` es dinámico → sirve igual en `panama.playablancaresidences.com` y en `landing-panama.vercel.app` (mismo origen, pasa CSP `'self'`).

### Regeneración del embed
El panel embebido es un **snapshot base64 congelado** (`B64_PANELJUAN`) dentro de `ceoapp1409.html`; editar `paneljuan.html` en disco NO lo cambia. Se regeneró el base64 desde el `paneljuan.html` ya arreglado, **preservando** la línea del auto-pass de clave:
```js
const _P=new URLSearchParams('embed=1&k=890D65CDA777439C932F');
```
(Si se regenera sin preservar esa línea, vuelve a `location.search` → el embed pierde la clave → reaparece el gate.)

## 4. Verificación (en vivo, ambos dominios)
- Botón y título internos = "Panel de Juan"; cero "Sala de Guerra".
- Embed con clave horneada + fetch absolutos + sin fetch relativos.
- Integridad HTML OK (`</html>`, secciones balanceadas), `B64_AGENTE` y `KEY` del padre intactos.

## 5. Backups
En `_ARCHIVO/`:
- `paneljuan.bak-rename-20260721-2125.html`, `ceoapp1409.bak-rename-20260721-2125.html`
- `paneljuan.bak-apifix-20260721-2141.html`, `ceoapp1409.bak-apifix-20260721-2141.html`

## 6. ⚠️ Pendiente de seguridad (NO arreglado — necesita OK de Juan)
La **llave maestra** `890D65CDA777439C932F` (= `CRM_KEY`/`DASH_KEY`) está **hardcodeada en HTML público** en `ceoapp1409.html` (`const KEY="890D65CDA777439C932F";`). Probado con curl: con solo el link `/ceoapp1409` cualquiera saca todos los leads + gasto + pipeline vía `/api/panel`, `/api/crm`, `/api/reporte`, `/api/leads`. Viola la regla dura del proyecto (secretos nunca en HTML público).

**Arreglo propuesto (pendiente):** rotar esa clave y ponerle gate real a `/ceoapp1409` (login server-side, sin `KEY` en el HTML).

## 7. Cómo probar
Abrir con anti-cache: `https://panama.playablancaresidences.com/ceoapp1409?v=fix2` → click "Panel de Juan" → debe cargar la data directa, sin gate ni "No se pudo conectar".

## 8. Regla para el futuro
Cualquier HTML embebido como **blob base64** dentro de `ceoapp1409.html` que llame a APIs propias **debe usar `location.origin + ruta` (absoluta)**, nunca ruta relativa. Si un embed muestra "No se pudo conectar", sospechar primero de esto; segundo, de CSP `connect-src` en `vercel.json`.
