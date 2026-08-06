# 6-ago-2026 · Fix: el panel no mostraba las notas de los leads

**Panel:** https://panama.playablancaresidences.com/crmdataplayablanca
**Estado:** ✅ RESUELTO y desplegado · **Pendiente:** 1 permiso en HubSpot (ver al final)

---

## 1. El síntoma

Al abrir la ficha de cualquier lead, el campo decía:

```
Notas registradas
0 con texto
```

Aunque el lead sí tuviera gestión hecha por el asesor.

## 2. Lo que NO era (descartado con evidencia)

| Sospecha | Cómo se descartó |
|---|---|
| Token de HubSpot vencido | El log mostró `fallos=0`: HubSpot respondió 200, nunca rechazó |
| Falta de permiso para leer notas | Igual: respuesta 200, no 403 |
| Endpoint de HubSpot cambiado | `/associations/notes` respondió bien (200) |
| Panel desactualizado en producción | El HTML servido era byte a byte igual al local |
| Caché del navegador | Se probó con recarga dura |

## 3. La causa real

**En HubSpot la gestión de un asesor NO vive solo en "notas".** Se guarda en **5 objetos distintos**:

`notes` (nota) · `calls` (llamada) · `tasks` (tarea) · `emails` (correo) · `meetings` (reunión)

El panel pedía únicamente `notes`. Los asesores de Playa Blanca registran sobre todo
**llamadas y tareas**, casi nunca notas escritas → el panel no tenía nada que mostrar.

**Evidencia** (log real de un lead, con el endpoint ya instrumentado):

```
[notas] id=240277504831 num_notes=2 notes=0 calls=1 tasks=1 emails=0 meetings=0 conTexto=2
```

Ese contacto **declara `num_notes=2` y tiene CERO notas**: son 1 llamada + 1 tarea.

> ⚠️ **`num_notes` de HubSpot MIENTE**: cuenta actividades, no notas. Nunca usarlo para
> contar notas. (`api/vigia-30.js:184` lo usa, pero ahí está bien porque solo pregunta
> "¿hubo gestión?", no "¿cuántas notas?").

## 4. La trampa de código que lo escondió

`api/crm.js` tenía este helper:

```js
async function hs(path, opts, token){
  const r = await fetch("https://api.hubapi.com"+path, {...});
  return r.json();          // ← nunca mira r.ok / r.status
}
```

Si HubSpot devolvía **403 o 401**, la respuesta era un objeto de error, y quien lo llamaba
hacía `(assoc.results||[])` → **lista vacía**. Es decir: *un fallo de permisos se veía
exactamente igual que un lead sin notas*, y no dejaba rastro en ningún log.

Por eso el bug pudo estar mucho tiempo sin que nadie lo notara.

## 5. Cómo se diagnosticó (método repetible)

Las variables de entorno de Vercel de este proyecto son `type=sensitive`:

- `vercel env pull` → las baja **vacías** (`CRM_KEY=""`)
- API de Vercel con `?decrypt=true` → tampoco las devuelve

**No hay forma de leer `CRM_KEY` ni `HUBSPOT_TOKEN` desde la máquina.** Sin la clave no se
puede llamar al API ni reproducir el bug localmente.

**La salida, y el método a repetir para cualquier bug futuro de estas APIs:**

1. Instrumentar el endpoint con `console.log` **sin datos personales** (solo IDs y conteos).
2. Desplegar con `git push`.
3. Pedirle a Juan que abra el panel una vez.
4. Leer desde acá:

```bash
vercel logs https://panama.playablancaresidences.com --json
```

## 6. Qué se cambió

**`api/crm.js`**

- `hsRaw()` + `hsFail()`: variante de `hs()` que **conserva el status HTTP y el cuerpo del
  error**. `hs()` se dejó intacto para no cambiarle el contrato al resto del endpoint.
- `?notes=<id>` ahora lee **las 5 clases de actividad** con una sola llamada de asociaciones
  (`/crm/v3/objects/contacts/{id}?associations=notes,calls,tasks,emails,meetings`) + un
  `batch/read` por clase que tenga algo. Se fusionan en un historial único ordenado por fecha.
- Red de seguridad: si la ficha no trae asociaciones de notas pero `num_notes>0`, se piden
  aparte por v4.
- Log por clase (`notes= calls= tasks= emails= meetings= conTexto= fallos=`) y `console.error`
  con el rechazo textual de HubSpot.
- Un fallo solo se reporta como error si además **no quedó nada que mostrar**.

**`crmdataplayablanca.html`**

- "Notas registradas" → **"Gestión registrada"**. Antes se pintaba desde `num_notas` (por eso
  salía 0 y el campo quedaba muerto, sin `id`); ahora el conteo lo pone la respuesta del API.
- "Historial de notas" → **"Historial de gestión"**. Cada entrada lleva su chip de tipo:
  `NOTA` · `LLAMADA` · `TAREA` · `CORREO` · `REUNIÓN`.
- Si HubSpot rechaza, el panel muestra **el motivo en claro** (permiso faltante, token vencido)
  con el detalle técnico y enlace a HubSpot — nunca más un `0` mentiroso.
- El vacío real es explícito: *"ni nota, ni llamada, ni tarea, ni correo, ni reunión"*.
- Los fallos ya no se guardan en `notesCache`: al reabrir la ficha se reintenta.

**Commits** (repo `playablanca-panama`, ambos desplegados):

- `9ab5a0f` — las notas ya no fallan en silencio: 3 caminos + motivo real
- `df926d7` — la ficha muestra TODA la gestión, no solo las notas

## 7. 🚨 PENDIENTE — falta un permiso en HubSpot

El mismo log destapó un segundo hallazgo:

```
batch-emails · 403 · MISSING_SCOPES
```

**El token de HubSpot no puede leer correos.** Nota, llamada, tarea y reunión sí se leen bien;
los **correos enviados al lead no aparecen** en el historial.

**Arreglo** (en HubSpot, no en código — requiere la mano de Juan): agregar el scope
`sales-email-read` al private app del portal **6874300**. No hay que tocar nada del panel:
en cuanto el scope esté, los correos entran solos al historial.

## 8. Lectura de negocio

Si al abrir un lead el historial sale vacío **y ahora dice explícitamente** "ni nota, ni
llamada, ni tarea, ni correo, ni reunión", eso ya no es un bug del panel: es que **el asesor
no registró nada**. Encaja con el 63% de leads "no localizables" medido el 27-jul, donde el
cuello de botella era contacto→cita, no la calidad del lead.

El panel ahora sirve como auditoría real de gestión, que antes era imposible porque todo
salía en 0.
