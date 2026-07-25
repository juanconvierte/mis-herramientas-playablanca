# ESTUDIO DE ERRORES — Sistema de alertas y reportes WhatsApp (13-jul-2026)

Post-mortem completo exigido por Juan tras múltiples fallas. **Cada error real, su causa raíz y el candado que lo hace irrepetible.** Auditado por agentes independientes (workflow `revision-requisitos-juan`) + fixes aplicados y verificados en producción.

## El sistema (lo simple que SIEMPRE debió ser)
```
Cae lead en HubSpot → espera a tener su data → alerta a WhatsApp con su número de orden
+ Reporte diario 8am · semanal lunes · mensual día 1
```

## Los 14 errores — causa raíz y candado

| # | Error (lo que Juan vio) | Causa raíz | Candado aplicado |
|---|---|---|---|
| 1 | Reporte diario llegó 1am con 0 leads | Crons a las 23:57-59, jitter de Vercel cruzó medianoche → contó el día equivocado | Un solo cron 8am Panamá, reporta el día YA CERRADO (`off=1`) |
| 2 | Semanal del domingo nunca llegó | 3 crons separados se desincronizaron + cruce de medianoche | Una sola corrida decide: diario + semanal (si ayer=domingo) + mensual (si ayer=fin de mes) |
| 3 | "Total semana: 15" vs semanal 71 | Panel contaba semana desde domingo; reporte usaba Lun-Dom | Semana empieza LUNES en todo + tope `untilS` |
| 4 | Alertas de leads NUNCA llegaban al grupo | Whitelist oculta (`CRM_NOTIFY_CAMPAIGNS`) se comía KMS-COL y MOTR en silencio | Env borrada → alerta TODA campaña, siempre con nombre de campaña |
| 5 | Lead 4 llegaba como #3 / todos #03 | (a) contaba TOTAL del día, no posición; (b) día anclado a HOY, no al día del lead; (c) HubSpot tarda en indexar → el lead no se contaba a sí mismo | Rank determinista: `(leads ANTERIORES del día DEL LEAD) + 1`, operador LT estricto |
| 6 | Número #01 falso cuando la API fallaba | `n\|\|1` inventaba un 1 | Si no sabe el número → muestra `#—`, jamás inventa |
| 7 | Panamá llegaba SIN presupuesto/plazo | Alerta salía a los 2 min; Meta→HubSpot llena esos campos DESPUÉS | Vigía espera hasta que el lead tenga presupuesto (máx 10 min), luego envía completo |
| 8 | Leads perdidos en silencio | Marcaba "enviado" ANTES de confirmar; si Green API fallaba → perdido para siempre | Marca solo si Green API confirma (`idMessage`); si falla → reintenta el próximo ciclo |
| 9 | Alertas duplicadas | Dedup en RAM se borraba con cada deploy | Marca PERSISTENTE `wa_alerta` en el propio contacto de HubSpot — sobrevive todo |
| 10 | "Pruebas" que llegaban al GRUPO | El POST ignoraba `?to=self` (iba al grupo aunque se pidiera self) + si fallaba resolver el número propio, caía al grupo | `?to` respetado en todas las rutas + fail-safe: si no resuelve self, NO envía (jamás cae al grupo) |
| 11 | Modos de prueba apuntaban al grupo por defecto | `?test=1&wa=1` y `?real=1&wa=1` → grupo si no se decía lo contrario | Default = SELF. Grupo solo con destino explícito |
| 12 | Endpoint abierto a internet | `hs-webhook` no pedía clave → cualquiera podía disparar fichas de leads reales (PII) al grupo del cliente | Clave obligatoria (401 sin ella) — verificado |
| 13 | Lotes llegaban a medias | Función moría a los 10s; un lote de 6 tarda 30-40s | `maxDuration: 60` en las 3 funciones de envío |
| 14 | Fechas/horas "malas" (6 "de hoy" vs 12/07) | **TRES relojes a la vez:** alertas GMT-5, HubSpot de Juan GMT-4, CRM propio UTC → contradicciones por todos lados | **UN SOLO RELOJ: GMT-5** (Panamá = Colombia, la zona del negocio) en alertas, reportes Y CRM. Hora etiquetada "(PA)" |

## La regla del reloj (para no confundirse nunca más)
- **Todo el sistema vive en GMT-5** (hora de Panamá y Colombia — donde están el cliente, los vendedores y los leads).
- Juan está en Venezuela (GMT-4): su teléfono/HubSpot muestra **+1 hora**. No es error — es el mismo instante.
- Un lead de las 11:30pm hora Panamá del sábado ES del sábado, aunque en Venezuela ya sea domingo 12:30am.
- Opcional pendiente: cambiar la zona de la cuenta HubSpot a GMT-5 para que Juan vea lo mismo en todos lados.

## Errores de proceso (míos, no del código)
1. **Dije "todo verde / cero errores" sin probar con leads reales de CADA campaña.** Regla nueva: jamás declarar "sin errores" sin prueba de punta a punta con data real.
2. **Reenvíos masivos de prueba repetidos** → spam al número de Juan y al grupo. Regla nueva: un envío de prueba por cambio, a self, y solo lo que se acordó.
3. **Nunca definí el reloj único** hasta que las contradicciones explotaron. Regla nueva: una sola fuente de verdad por dato, definida ANTES de construir.

## Estado actual (13-jul noche)
- 🔒 **TODO va al número de test (Digitel de Juan).** Vigía Y reportes 8am. Al grupo: NADA.
- Para activar el grupo (cuando Juan autorice): quitar `&to=self` en (1) `api/wa-lead-poll.js` (POST interno) y (2) cron de `wa-grupo` en `vercel.json` → redeploy. Dos líneas.
- Verificado en producción: clave 401 ✓ · rank #NN correcto ✓ · hora "(PA)" ✓ · `wa_alerta` creada ✓ · deploy 200 ✓.

## Números correctos de referencia (validados por agente verificador)
| Lead | # | Día (GMT-5) |
|---|---|---|
| Andres Gomez | #12 | 12/07 |
| tayra julio | #13 | 12/07 |
| Luis Alfredo M. | #14 | 12/07 |
| Albeiro Gómez | #15 | 12/07 |
| German Hernandez | #01 | 13/07 |
| Leonardo Viloria | #02 | 13/07 |

(El CRM de Juan los mostraba todos como "13-jul" porque agrupaba en UTC — ya corregido al reloj único GMT-5.)
