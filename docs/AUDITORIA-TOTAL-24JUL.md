# Auditoría TOTAL del ecosistema — Playa Blanca — 24-jul-2026

Auditor multi-agente (80 agentes, 12 lentes + verificación adversarial). **68 hallazgos → 47 confirmados reales, 21 descartados.**

Dimensiones: seguridad · bugs · fiabilidad · integridad · UX · compliance.

---

## [1] `CRITICA` · seguridad — Stored XSS: campos de lead se inyectan en innerHTML sin escapar (render y renderWebTable)

- **Archivo:** /Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/web-panama-LIVE/ceoapp1409.html (render() líneas ~1074-1083; renderWebTable() líneas ~955-962)
- **Evidencia:** `<div>${l.nombre}</div>`, `${l.email||''}`, `${l.tel||'—'}`, `${l.anuncio}` interpolados directo en template->innerHTML sin esc(). La función esc() existe (línea 643) pero SOLO se usa para LINKS, nunca para leads. crm.js (l.158/217) y leads.js (l.81-83) devuelven firstname/lastname/email/phone crudos, sin sanitizar.
- **Síntoma/Riesgo:** Un atacante llena el formulario público (landing PA/CO o form instantáneo de Meta) con nombre/email = `<img src=x onerror=...>`; se guarda en HubSpot y al abrir el panel el admin ejecuta ese JS. La CSP trae script-src 'unsafe-inline' => el handler corre. En contexto del admin puede leer la master key global KEY (890D65, misma página) y disparar endpoints same-origin permitidos por connect-src 'self': POST /api/wa-grupo (spam/phishing al grupo WhatsApp real de asesores), GET /api/wa-lead-poll?archive= (borra contactos HubSpot). Robo de credencial + acciones destructivas + PII con solo abrir el panel.
- **Fix:** Escapar TODOS los campos de lead con la esc() ya existente antes de meterlos al innerHTML (nombre, firstname/lastname, email, tel/phone, anuncio, angulo, objetivo_de_inversion, rango/rango_de_inversion, estado, vendedor, interes), o construir las celdas con textContent en vez de template string. Idealmente sanitizar también en crm.js/leads.js del lado server.
- **Verificado:** CONFIRMADO como Stored XSS real y explotable de punta a punta. Cadena verificada leyendo los archivos:

1) SINK (sin escapar): en /Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/web-panama-LIVE/ceoapp1409.html, render() interpola datos de lead crudos en innerHTML: `${l.nombre}` y `${l.estado}` (línea 1075), `${l.tel}` y `${l.email}` (1076), `${l.angulo}`/`${l.interes}`/`${l.anuncio}` (1077-1078), `${l.rango}` (1079), `${l.vendedor}` (1081). Igual en renderWebTable(): `${_nm}` (firstname+last

## [2] `CRITICA` · seguridad — Segunda clave viva (PANEL_KEY 'ralph-ceo-pb-7q29') horneada en el embed Agente base64 público

- **Archivo:** /Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/web-panama-LIVE/ceoapp1409.html (línea 912, const B64_AGENTE=... -> decodificado línea 98)
- **Evidencia:** atob(B64_AGENTE) contiene: `let KEY = new URLSearchParams(location.search).get('k') || 'ralph-ceo-pb-7q29'`. Ese valor ES PANEL_KEY: vercel.json:18 corre el cron /api/wa-grupo?key=ralph-ceo-pb-7q29 y los gates wa-grupo.js:24, hs-webhook.js:178, wa-lead-poll.js:20, vigia.js son process.env.PANEL_KEY||CRM_KEY||DASH_KEY. Es DISTINTA del master 890D65.
- **Síntoma/Riesgo:** Cualquiera descarga /ceoapp1409 (público, no está en .vercelignore), hace atob de la constante y obtiene la clave sin credenciales. Con ella: POST /api/wa-grupo con {text:'...'} => mensaje ARBITRARIO al grupo WhatsApp real de Ralph+asesores (impersonación/phishing); wa-grupo.js:35 chatId=q.to||group => ?to=<numero> reenvía el reporte Excel de leads (PII) a un WhatsApp del atacante (exfiltración); GET /api/wa-lead-poll?archive=<email> => DELETE de contacto en HubSpot.
- **Fix:** Dejar de embeber blobs con claves horneadas en HTML público. Rotar PANEL_KEY. Usar clave dedicada solo-cron (CRON_SECRET/Bearer verificado server-side) para wa-grupo en vez de query key reutilizada; añadir allowlist para el parámetro 'to'; separar la capacidad de envío detrás de clave de escritura distinta de la de lectura.
- **Verificado:** CONFIRMADO real. La clave 'ralph-ceo-pb-7q29' está horneada en un blob base64 público. ceoapp1409.html:912 define const B64_AGENTE="..."; al decodificarlo (base64 -d) su línea 98 es: `let KEY = new URLSearchParams(location.search).get('k') || 'ralph-ceo-pb-7q29'`. El archivo ES público: NO está en .vercelignore (que sí tapa agente.html/paneljuan.html/dashboard-leads.html), no hay rewrite ni gate de servidor, se sirve como .html estático → cualquiera hace curl + atob sin credenciales. La clave es

## [3] `CRITICA` · seguridad — Borrado de contactos HubSpot vía GET ?archive= (destructivo, sin CSRF, key en URL)

- **Archivo:** /Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/web-panama-LIVE/api/wa-lead-poll.js
- **Evidencia:** if(q.archive && c.id){ await hs('/crm/v3/objects/contacts/'+c.id,{method:'DELETE'},token); ... } (línea 65-66)
- **Síntoma/Riesgo:** Una petición GET con la clave (?archive=<email>) ejecuta un DELETE en HubSpot y archiva/borra el primer contacto con ese email. Es una operación destructiva sobre los ~2900 leads del cliente, disparable por GET (idempotente en apariencia → prefetch/crawler/historial pueden dispararla) y la clave viaja en la URL (se filtra por referrer/logs). Con la PANEL_KEY filtrada en vercel.json (o la master key 890D65... que es fallback), un atacante borra contactos uno a uno tras enumerarlos por /api/crm o ?hoy.
- **Fix:** Exigir POST + una clave dedicada distinta de la de paneles (como el ?ctl=HS_CONTROL_KEY de hs-webhook), nunca GET. Idealmente restringir a un allowlist de emails de prueba o quitar el endpoint de producción. Nunca aceptar borrado con la key semi-pública.
- **Verificado:** CONFIRMADO (con correcciones al finder). Archivo: /Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/web-panama-LIVE/api/wa-lead-poll.js. Línea 20 = único gate (?key). Líneas 59-66: un GET con ?archive=<email> busca el contacto por email y ejecuta DELETE /crm/v3/objects/contacts/{id} en HubSpot (archiva). Endpoint desplegado (está en vercel.json functions, NO en .vercelignore) → público.

DOS afirmaciones del finder son FALSAS (verificadas EN VIVO contra panama.playablancaresidences.com):
1) "P

## [4] `CRITICA` · seguridad — wa-grupo permite exfiltrar el Excel de leads (PII) a un WhatsApp arbitrario con ?to=

- **Archivo:** /Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/web-panama-LIVE/api/wa-grupo.js
- **Evidencia:** let chatId = q.to || group; ... sendWA(built, id, token, chatId, apiUrl) → fd.append('file', new Blob([buf])...) (líneas 35, 72, 157-160)
- **Síntoma/Riesgo:** chatId = q.to || group: cualquier valor de ?to (salvo self/yo) se usa como destinatario sin validar. GET /api/wa-grupo?key=KEY&auto=1&to=<numero-atacante>@c.us construye el reporte y adjunta el Excel con leadsDetalle (nombre, teléfono, email, presupuesto de todos los leads del periodo) y lo envía al número del atacante. Exfiltración masiva de PII con una sola request (la key está filtrada en vercel.json y en HTML público).
- **Fix:** No aceptar destinatario arbitrario en producción: ignorar ?to salvo el modo self/yo (que ya se resuelve solo). El destino real debe ser SIEMPRE GREENAPI_GROUP. Si se necesita override, exigir clave dedicada y un allowlist de números.
- **Verificado:** CONFIRMADO end-to-end. (1) /api/wa-grupo.js es publico (api/ NO esta en .vercelignore; ademas es cron en vercel.json). (2) Linea 35 `let chatId = q.to || group` acepta ?to= arbitrario sin validar (salvo self/yo). (3) Linea 72 sendWA adjunta el Excel de buildExcel(leadsDetalle); _excel.js:52 escribe filas con ld.nombre, ld.tel, ld.rango(presupuesto), ld.plazo, ld.estado, ld.asesor = PII de leads. tipo=mes exporta un mes entero. (4) El gate (linea 24) = PANEL_KEY||CRM_KEY||DASH_KEY; PANEL_KEY SI e

## [5] `ALTA` · compliance — Testimonios inventados (nombres, fotos y citas de muestra) servidos en la landing publica

- **Archivo:** /Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/web-panama-LIVE/index.html
- **Evidencia:** Comentario en el HTML (linea ~1578): 'estos 3 testimonios son de MUESTRA (nombres y citas de demostracion, no verificados). Reemplazar por testimonios reales autorizados por el cliente'.
- **Síntoma/Riesgo:** La seccion #testimonios (lineas ~1581-1621) muestra a 'Roberto Achong', 'Maritza de Leon' y 'Carolina Him' con foto (testi-roberto/maritza/carolina.jpg) y citas de compra, pero el propio codigo los marca como falsos. Es prueba social fabricada en una pagina viva de una empresa real: publicidad enganosa al comprador y motivo tipico de rechazo/penalizacion en la revision de anuncios de Meta (categoria Vivienda) y de reclamos de consumidor en PA/CO.
- **Fix:** Quitar la seccion #testimonios (y sus 3 img testi-*.jpg) del index.html hasta tener testimonios reales con consentimiento firmado del cliente; nunca publicar personas/fotos ficticias como propietarios.
- **Verificado:** CONFIRMADO. En web-panama-LIVE/index.html (líneas 1577-1623) la sección pública #testimonios muestra 3 "propietarios" con nombre, foto y cita de compra: Roberto Achong (testi-roberto.jpg), Maritza de León (testi-maritza.jpg), Carolina Him (testi-carolina.jpg). El comentario interno (1578-1580) los marca textualmente como "de MUESTRA (nombres y citas de demostración, no verificados)". Verificado que es realmente público: index.html es la landing principal servida (panama.playablancaresidences.com

## [6] `ALTA` · seguridad — El panel de leads se sirve público SIN login y falta en .vercelignore (extiende el hallazgo #1 de la clave)

- **Archivo:** web-panama-LIVE/crmdataplayablanca.html:450
- **Evidencia:** const KEY="890D65CDA777439C932F"; ... (init l.1034) fetchData(false) dispara /api/crm?key=890...&all=1 al cargar. .vercelignore SÍ excluye dashboard-leads.html (comentario: 'DATOS PRIVADOS de leads (PII). JAMÁS publicar') pero NO excluye crmdataplayablanca.html ni crmceo.html. vercel.json (cleanUrls) las sirve en /crmdataplayablanca sin ninguna cabecera de auth.
- **Síntoma/Riesgo:** A diferencia de crmceo.html (que sí tiene gate de clave), esta página NO tiene ninguna verificación: al abrirla se auto-consulta /api/crm con la clave horneada y se pintan los ~2900 leads con PII al instante. crm.js solo valida key===CRM_KEY (l.94) y devuelve todo con ?all=1 (l.151-180). La protección por .vercelignore se aplicó al dashboard viejo y dejó vivo el nuevo con la misma PII. La 'seguridad' es solo que la URL sea secreta (obscuridad).
- **Fix:** Añadir crmdataplayablanca.html y crmceo.html a .vercelignore mientras no tengan auth real; mover la validación a sesión/cookie de servidor y quitar la clave del HTML; rotar CRM_KEY/DASH_KEY. Si el panel debe ser accesible, ponerlo tras el mismo gate de servidor que valida contra env, sin clave embebida.
- **Verificado:** VERIFICADO REAL. Confirmado contra disco (web-panama-LIVE/): (1) .vercelignore SÍ excluye el panel viejo dashboard-leads.html (linea 24-25, comentario 'DATOS PRIVADOS de leads (PII). JAMAS publicar') pero NO excluye crmdataplayablanca.html ni crmceo.html -> con vercel.json cleanUrls:true la pagina se sirve publica en /crmdataplayablanca sin cabecera de auth. (2) crmdataplayablanca.html:450 hornea const KEY=\"890D65CDA777439C932F\"; init l.1034 fetchData(false) -> l.923 fetch('/api/crm?key=KEY&al

## [7] `ALTA` · seguridad — Endpoint /api/leads del deploy Colombia expone TODO el PII de leads con solo la clave maestra (ya filtrada)

- **Archivo:** /Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/landing-colombia-full/api/leads.js:26
- **Evidencia:** const key = (req.query && req.query.key) || ""; if (key !== dashKey) {...401}  → luego devuelve res.json({ leads, owners })
- **Síntoma/Riesgo:** leads.js está desplegado público (no está en .vercelignore) y solo se protege con ?key=DASH_KEY, comparado en texto plano. DASH_KEY es la misma clase de clave maestra ya hardcodeada en el HTML público del ecosistema (hallazgo #1). Confirma el ALCANCE: GET a https://landing-colombia-full.vercel.app/api/leads?key=<clave-filtrada> devuelve nombre, email, teléfono, presupuesto (rango_de_inversion), objetivo, UTMs y asesor asignado de TODOS los leads Colombia (filtro origen_formulario='Landing Colombia'), paginado hasta 3000. Rotar la clave del HTML NO cierra esto: hay que rotar también la env DASH_KEY.
- **Fix:** Rotar DASH_KEY/CRM_KEY en Vercel (Colombia y Panamá) a un valor nuevo NO presente en ningún HTML/blob; migrar a auth server-side real (cookie de sesión firmada o header Bearer validado, no query param que queda en logs/Referer); si el panel Colombia ya está retirado, borrar api/leads.js del deploy Colombia.
- **Verificado:** CONFIRMADO como fuga real y explotable, con un matiz de alcance. Verificado en disco: (1) landing-colombia-full/api/leads.js SÍ se despliega público — el .vercelignore de Colombia solo tapa *.md, .env*, .gitignore y panel.html; nada bajo api/, así que https://landing-colombia-full.vercel.app/api/leads es una función viva. (2) Única protección = ?key= en texto plano contra process.env.DASH_KEY (líneas 26-27), sin sesión, sin chequeo de origen/referer, sin rate-limit. (3) En éxito devuelve PII com

## [8] `ALTA` · seguridad — leads.js es el endpoint de exfiltración masiva de PII (CSV email+teléfono listo para Meta)

- **Archivo:** web-panama-LIVE/api/leads.js:131-135,166-180,203-206
- **Evidencia:** metaCsv(rows) -> "email,phone,fn,ln,country,ct" ; dias=Math.min(730,...) ; res.status(200).send(metaCsv(data))
- **Síntoma/Riesgo:** Con la clave maestra ya filtrada en el HTML público, GET /api/leads?audiencia=1&format=csv&dias=730 descarga hasta ~2900 contactos con email+teléfono+nombre en un CSV con cabeceras (email,phone,fn,ln,country,ct) exactamente en el formato de subida de audiencias de Meta; ?audiencia=1&full=1 devuelve TODAS las filas con PII cruda en JSON. Es el vector de robo masivo más grave: un solo GET saca toda la base para spam/venta de datos.
- **Fix:** Separar la exportación en bloque detrás de una segunda clave fuerte NO embebida en HTML, o exigir POST + header Authorization; limitar 'dias' y 'format=csv' a sesiones autenticadas de servidor; rotar CRM_KEY/DASH_KEY; añadir rate-limit. No incluir email+teléfono juntos en respuestas destinadas al front.
- **Verificado:** CONFIRMADO real=true, severidad alta (correcta). leads.js NO está en .vercelignore -> se despliega público en /api/leads. Tiene gate de auth (líneas 199-200: 401 si key != DASH_KEY/CRM_KEY), pero el gate cae porque la clave maestra 890D65CDA777439C932F está hardcodeada en HTML público (ceoapp1409.html:488, crmdataplayablanca.html:450) y usada como fetch('/api/leads?key='+KEY) en ceoapp1409.html:969 -> prueba que ese valor == CRM_KEY en runtime. Vectores de exfil verificados: (1) ?audiencia=1&ful

## [9] `ALTA` · seguridad — hs-webhook: ?to= + ?real=1/objectId permite exfiltrar PII de cualquier contacto y spamear WhatsApp arbitrario

- **Archivo:** web-panama-LIVE/api/hs-webhook.js (118-129, 206-215, 236-259)
- **Evidencia:** L121 let chatId = to || group; L212 waSend(m, q.to?...) en la rama ?real; L255 waSend(msg, qto) en POST con qto = req.query.to; hsGet(id) con id = ev.objectId|ev.vid|... (L243) sin validar pertenencia.
- **Síntoma/Riesgo:** Una vez pasada la clave (que es la master filtrada, ver hallazgo aparte), el parámetro ?to=<num>@c.us redirige el envío a CUALQUIER número de WhatsApp usando la instancia Green API del cliente. Vectores concretos: GET ?real=1&wa=1&to=X manda la ficha completa (nombre, teléfono, presupuesto, link HubSpot) del lead más reciente al número del atacante; POST body [{objectId:<id>}]&to=X hace hsGet de un ID arbitrario y envía su PII → enumerando IDs se exfiltra toda la base (~2900) al WhatsApp del atacante; ?test=1&wa=1&to=X convierte la instancia del cliente en emisor de spam/suplantación. La marca de dedup (wa_alerta) solo se pone si !qto, así que con ?to= no deja rastro en el contacto.
- **Fix:** Ignorar ?to= en producción (o permitirlo solo con una segunda clave dedicada de pruebas distinta de la de paneles). No exponer ?real=1 en un endpoint con la clave semi-pública. Rotar la master key (bloquea todo el vector).
- **Verificado:** CONFIRMADO real y explotable en producción, PERO el finder nombró la clave equivocada. hs-webhook.js:177 usa `_key = PANEL_KEY || CRM_KEY || DASH_KEY`, y PANEL_KEY SÍ está seteada en prod a `ralph-ceo-pb-7q29` (verificado: vercel.json:18 corre un cron que autentica wa-grupo con ese valor, y wa-grupo usa la misma cadena; como CRM_KEY=890D65, el cron solo funciona si PANEL_KEY=ralph-ceo-pb-7q29). Por eso PANEL_KEY corta la cadena y la master key NO abre este endpoint.

Prueba en vivo (solo ?health

## [10] `ALTA` · seguridad — wa-grupo POST {text} inyecta cualquier mensaje al grupo de asesores (impersonación)

- **Archivo:** /Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/web-panama-LIVE/api/wa-grupo.js
- **Evidencia:** if(req.method === 'POST' && req.body && req.body.text){ ... sendMessage/${token} ... message:String(req.body.text) } (líneas 42-45)
- **Síntoma/Riesgo:** POST /api/wa-grupo?key=KEY con body {text:'...'} envía texto libre al grupo de WhatsApp de los asesores del cliente sin más control. Con la key filtrada, un atacante difunde mensajes falsos (phishing, órdenes falsas de 'llamar a este número', desprestigio) a todo el equipo de ventas, haciéndose pasar por el sistema de la agencia.
- **Fix:** Proteger el envío de texto libre al grupo con una clave dedicada distinta de la de paneles/crons, o eliminar el modo texto-libre. Registrar y limitar (rate-limit) los envíos al grupo.
- **Verificado:** REAL y explotable sin credenciales, pero con una CORRECCION importante a la clave. Verificado leyendo el codigo y decodificando blobs.

FLUJO CONFIRMADO:
1) /api/wa-grupo.js esta en web-panama-LIVE/api/ (NO en .vercelignore) -> funcion servida publicamente; ademas figura como cron en vercel.json:18.
2) Lineas 42-46: POST con body JSON {text:"..."} ejecuta fetch(.../sendMessage/${token}, {chatId, message:String(req.body.text)}). chatId por defecto = GREENAPI_GROUP (grupo real de asesores). Vercel

## [11] `ALTA` · seguridad — PANEL_KEY viva ('ralph-ceo-pb-7q29') hardcodeada en vercel.json

- **Archivo:** /Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/web-panama-LIVE/vercel.json
- **Evidencia:** crons: { path: '/api/wa-grupo?key=ralph-ceo-pb-7q29&auto=1', schedule: '0 13 * * *' }
- **Síntoma/Riesgo:** El cron '/api/wa-grupo?key=ralph-ceo-pb-7q29&auto=1' incrusta en texto plano la PANEL_KEY (fallback de CRM_KEY/DASH_KEY). Es un SEGUNDO secreto filtrado, distinto de la master key ya conocida. Esa clave abre wa-grupo (exfil/inyección al grupo), wa-lead-poll (?archive borra contactos, ?hoy/?check leaks PII) y hs-webhook. Queda en el repo, en los logs de build/deploy y en el dashboard de crons de Vercel.
- **Fix:** Sacar la clave del path del cron: proteger los crons con CRON_SECRET (header Authorization Bearer que Vercel inyecta) en vez de ?key= en la URL, y rotar 'ralph-ceo-pb-7q29'. Ningún secreto en vercel.json ni en query strings.
- **Verificado:** VERIFICADO REAL (severidad alta correcta). 'ralph-ceo-pb-7q29' es un SEGUNDO secreto vivo y DISTINTO del master 890D65: es el valor de PANEL_KEY. Prueba: el gate de api/wa-grupo.js:23-24, api/wa-lead-poll.js:19-20 y hs-webhook es `PANEL_KEY||CRM_KEY||DASH_KEY`; el `||` toma el primero truthy, y para que el cron diario vercel.json:18 (/api/wa-grupo?key=ralph-ceo-pb-7q29&auto=1) autentique, PANEL_KEY debe ser exactamente esa cadena. El master 890D65 NO abre estos 3 endpoints. La clave habilita acc

## [12] `ALTA` · seguridad — Clave viva PANEL_KEY hardcodeada en la URL del cron (vercel.json)

- **Archivo:** web-panama-LIVE/vercel.json:18
- **Evidencia:** { "path": "/api/wa-grupo?key=ralph-ceo-pb-7q29&auto=1", "schedule": "0 13 * * *" }
- **Síntoma/Riesgo:** El cron `{ "path": "/api/wa-grupo?key=ralph-ceo-pb-7q29&auto=1" }` incrusta en texto plano el valor real de PANEL_KEY. Esa misma clave (=`ralph-ceo-pb-7q29`) es aceptada como auth por /api/wa-grupo (wa-grupo.js:23), /api/vigia (vigia.js:69), /api/wa-lead-poll (wa-lead-poll.js:19) y /api/meta-events (meta-events.js:68). Cualquiera que vea el archivo (repo/commit/leak) obtiene: POST a /api/wa-grupo?key=... con {text:...} => manda mensajes ARBITRARIOS al grupo de WhatsApp de asesores (phishing/spam al equipo de ventas), disparar reportes, y operar el vigía. Viola la regla dura del proyecto: secretos SOLO en .env/Vercel env, nunca hardcodeados. NOTA: panel.js:104-105 ya excluyó PANEL_KEY (no abre el panel de leads), así que NO expone los 2900 PII — pero sí el canal de WhatsApp del equipo y el sistema de alertas.
- **Fix:** Quitar la clave de la URL del cron. Usar el mecanismo oficial de Vercel Cron: no pasar `key`, y en wa-grupo.js validar el header `Authorization: Bearer $CRON_SECRET` (var de entorno CRON_SECRET) o el header `x-vercel-cron`. Rotar PANEL_KEY inmediatamente ya que su valor está en el archivo de config.
- **Verificado:** VERIFICADO REAL (con 2 correcciones al finder). Confirmado leyendo los archivos: vercel.json:18 lleva en texto plano `/api/wa-grupo?key=ralph-ceo-pb-7q29&auto=1`; el gate wa-grupo.js:23-24 = `PANEL_KEY||CRM_KEY||DASH_KEY` vs req.query.key; la rama POST {text} (lineas 42-46) envia mensaje ARBITRARIO al grupo real de WhatsApp de asesores. La MISMA clave gatea vigia.js (~69), wa-lead-poll.js:19 y meta-events.js (~72). Es una clave DISTINTA del master 890D65 (hallazgo #1). panel.js:104 si excluyo PA

## [13] `ALTA` · seguridad — Auth de cron por User-Agent spoofable: /api/vigia?seed=1 suprime TODAS las alertas de leads sin clave

- **Archivo:** web-panama-LIVE/api/vigia.js:65
- **Evidencia:** const isCron = ua.includes("vercel-cron"); ... if(!isCron && !okKey){ res.status(401)... }  // luego: if(seed){ ...marca leads como avisados... }
- **Síntoma/Riesgo:** El cron se autentica con `const isCron = ua.includes('vercel-cron')` y en la línea 70 `if(!isCron && !okKey) 401`. El User-Agent es trivialmente falsificable: cualquiera desde internet enviando el header `User-Agent: vercel-cron` pasa el gate SIN clave. Como la puerta es única, un atacante llega a las ramas de operación: `GET /api/vigia?seed=1&window=10080` (línea 130) marca TODOS los leads recientes como ya-avisados (vigia_alerta) => el vigía deja de notificar leads reales al equipo de ventas => los leads se enfrían sin que nadie se entere. También `?setup=1` (línea 101). Mismo patrón en parte.js:17 (dispara spam de Telegram al Jefe + quema cuota de Gemini/Meta). Ninguno requiere secreto.
- **Fix:** No confiar en User-Agent. Validar el cron con `Authorization: Bearer $CRON_SECRET` (Vercel inyecta este header en crons si se define CRON_SECRET) o el header `x-vercel-cron`. Además, aislar las operaciones peligrosas (seed/setup) para que exijan okKey humano SIEMPRE, incluso en cron. Aplicar igual a parte.js:17.
- **Verificado:** CONFIRMADO real y explotable. vigia.js:64-70 autentica el cron solo con `isCron = ua.includes("vercel-cron")` y la puerta única `if(!isCron && !okKey) 401`. El User-Agent es un header controlado por el cliente (curl -H "User-Agent: vercel-cron"), así que cualquiera en internet pasa el gate SIN clave. El endpoint es público (los /api/* de web-panama-LIVE se despliegan todos; el .vercelignore solo tapa HTML/artefactos, nunca api/; hallazgo #1 ya prueba que /api/crm es alcanzable). Verificado que l

## [14] `MEDIA` · fiabilidad — Perdida silenciosa del lead completo si falla el fetch del navegador a HubSpot (usuario ve 'recibido' igual)

- **Archivo:** /Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/web-panama-LIVE/index.html
- **Evidencia:** hsPromise.then(doRedirect).catch(doRedirect); setTimeout(doRedirect, 2000); ... sendToHubSpot(...).catch(function(err){ console.warn('[HubSpot] Submission failed:', err); })
- **Síntoma/Riesgo:** El payload completo del lead (nombre, telefono, presupuesto, objetivo) se entrega UNICAMENTE por el fetch del navegador a api.hsforms.com. En el submit, hsPromise.then(doRedirect).catch(doRedirect) + setTimeout(doRedirect,2000) redirigen a /gracias pase lo que pase. Si un ad-blocker, un fallo de red, un cambio de CSP o una caida de HubSpot rechaza ese POST, el lead se pierde sin traza y el usuario ve la pagina de exito. El unico respaldo server-side (sendCAPI -> /api/conversion -> upsert por email) solo guarda email+fbc/fbp, SIN nombre ni telefono, por lo que el asesor no puede contactar al lead.
- **Fix:** Enviar tambien el payload completo a un endpoint propio same-origin (p.ej. /api/crm o /api/hs-webhook con keepalive) como fuente de verdad/fallback antes del redirect, o esperar el 200 de hsforms y mostrar un error visible si falla en vez de redirigir a /gracias.
- **Verificado:** CONFIRMADO (fiabilidad, no seguridad; publico:false correcto). En web-panama-LIVE/index.html el submit envia el lead completo (nombre, telefono, email, presupuesto, objetivo) UNICAMENTE por fetch del navegador a api.hsforms.com (lineas 2296-2301) y redirige a /gracias pase lo que pase: hsPromise.then(doRedirect).catch(doRedirect) + setTimeout(doRedirect,2000) (2232-2233). El unico sink same-origin del submit es /api/conversion; NO hay sendBeacon ni llamada a /api/crm o /api/hs-webhook. Verificad

## [15] `MEDIA` · bug — Embed Agente usa fetch relativo /api/... que no resuelve desde origen blob: -> estado en vivo siempre falla y muestra falso 'Todo funcionando'

- **Archivo:** /Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/web-panama-LIVE/ceoapp1409.html (B64_AGENTE, líneas 182-184 y 248) — el fix ya existe en B64_PANELJUAN línea 796
- **Evidencia:** Agente hace `fetch('/api/hs-webhook?...')`, `/api/wa-lead-poll`, `/api/vigia` RELATIVOS. Probado: new URL('/api/hs-webhook','blob:https://panama.../uuid') lanza 'Invalid URL'. Panel de Juan sí trae el fix `_API=(/^https?:/.test(location.origin))?location.origin:'https://panama...'`; Agente no lo tiene. blobFrame carga el iframe con blob: URL, así que location es blob.
- **Síntoma/Riesgo:** Como /agente ahora es 404 y solo se llega vía el embed blob, las 3 llamadas de salud SIEMPRE lanzan y se tragan en .catch(()=>null) => todos los nodos quedan 'sin dato' (ámbar), pero el banner global cuenta solo nodos rojos (0) y pinta 🟢 'Todo funcionando. Ningún nodo roto.'. Es un monitor ciego que reporta salud: no detecta caídas reales (grupo sin avisos, Green API desconectado, gatillo caído).
- **Fix:** Replicar el fix de paneljuan en el blob del agente: definir `const _API=(/^https?:/.test(location.origin))?location.origin:'https://panama.playablancaresidences.com';` y anteponerlo a los fetch de refresh() y a tryKey(). Alternativamente que blobFrame inyecte un <base href> absoluto o pase la URL del origen. Además, degradar el estado global a 'sin dato' (no verde) cuando las 3 respuestas son null.
- **Verificado:** CONFIRMADO real. Verificado leyendo /Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/web-panama-LIVE/ceoapp1409.html y decodificando ambos embeds base64.

Cadena probada:
1) B64_AGENTE (definido en ceoapp1409.html:912) hace 3 fetch RELATIVOS raíz: /api/hs-webhook, /api/wa-lead-poll, /api/vigia (líneas decodificadas 182-184), cada uno con .catch(()=>null). tryKey() también usa fetch relativo.
2) El embed del Agente NO tiene el fix: sin _API, sin location.origin, sin <base>. En cambio B64_PANEL

## [16] `MEDIA` · seguridad — PII real de 4 leads incrustada en el HTML público (SAMPLE_DATA) y usada como fallback

- **Archivo:** web-panama-LIVE/crmdataplayablanca.html:454-457
- **Evidencia:** const SAMPLE_DATA=[{"nombre":"MARTA BONILLA","tel":"+50769429691","email":"mbg192839@gmail.com","hsid":"235514732295",...},{"nombre":"Marcelino Ríos","tel":"+50762197654","email":"marcelinoriosabrego95@gmail.com"...}, ... (4 registros con hsid, nombre, teléfono y correo reales)]
- **Síntoma/Riesgo:** Cualquiera que abra 'ver código fuente' de la página pública lee nombre+teléfono+email de 4 contactos reales de HubSpot, SIN necesidad de la clave ni de que la API responda. Además, fetchData() los pinta en pantalla como fallback cada vez que /api/crm falla o la clave se rota (línea 929: applyData(SAMPLE_DATA,...)). Es una fuga de PII independiente de la clave: rotar CRM_KEY NO la elimina.
- **Fix:** Reemplazar SAMPLE_DATA por datos 100% ficticios/anónimos o por [] ; en el catch de fetchData mostrar un estado de error ('no se pudo cargar, reintentando') en vez de renderizar registros reales de muestra.
- **Verificado:** CONFIRMADO. web-panama-LIVE/crmdataplayablanca.html:453-458 contiene const SAMPLE_DATA con 4 registros; 3 son PII REAL (MARTA BONILLA +50769429691 mbg192839@gmail.com hsid 235514732295; Marcelino Rios +50762197654 marcelinoriosabrego95@gmail.com hsid 235491827022; Benja +50767089124 ruth12r09@gmail.com hsid 235460095019), con presupuesto declarado y asesor asignado. VERIFICADO que son reales: los mismos email/hsid aparecen en exports/meta-compradores-panama-365d.csv (export real de HubSpot). El 

## [17] `MEDIA` · fiabilidad — Un 500 transitorio del backend expulsa al CEO autenticado a la pantalla de clave y oculta el panel

- **Archivo:** web-panama-LIVE/crmceo.html:623-625
- **Evidencia:** auto-refresh: setInterval(()=>{ ... Object.keys(CACHE).forEach(k=>delete CACHE[k]); load(); }, 300000). En load() sin caché -> tryKey -> fetch('/api/panel...'); catch(e){ showGate('No se pudo conectar. Intenta de nuevo.') } (l.601). panel.js hace res.status(500) ante cualquier excepción de HubSpot/Meta (l.364).
- **Síntoma/Riesgo:** Cada 5 min se limpia la caché y se re-consulta. Si HubSpot/Meta devuelven 500 o hay un blip de red, el usuario ya logueado ve de golpe el overlay opaco 'Panel privado / Clave de acceso / No se pudo conectar' tapando el dashboard que estaba mirando: parece que lo deslogueó, y como la clave sigue en sessionStorage tendría que re-teclearla. Un error transitorio esconde toda la vista.
- **Fix:** En el catch de load(): si ya hay datos previamente renderizados (o KEY válida), conservar la última vista y mostrar un banner discreto 'reintentando…' en lugar de showGate(); reservar showGate() solo para r.status===401. Opcional: en auto-refresh no borrar la caché hasta tener respuesta OK.
- **Verificado:** CONFIRMADO leyendo ambos archivos. Cadena reproducible: (1) crmceo.html:623-625 auto-refresh cada 5 min limpia CACHE y llama load(); (2) load() (593-603) entra al try→tryKey(KEY); (3) tryKey (587) hace `if(!r.ok) throw new Error('http '+r.status)`; (4) catch (601) llama showGate('No se pudo conectar...'); (5) showGate (583) pone $('#gate').style.display='flex', overlay OPACO (CSS l.202: position:fixed;inset:0;background:var(--bg);z-index:100) que tapa todo el dashboard. Backend confirmado: panel

## [18] `MEDIA` · seguridad — /api/conversion sin autenticación: permite inyectar eventos falsos a Meta y CREAR/escribir contactos en HubSpot

- **Archivo:** /Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/landing-colombia-full/api/conversion.js:23
- **Evidencia:** ALLOWED_EVENTS = ['PageView','Lead','CompleteRegistration','ViewContent','Contact','Purchase'] ... savePassport(): fetch('.../contacts/batch/upsert', { inputs:[{ idProperty:'email', id:user_data.email, properties:props }] })
- **Síntoma/Riesgo:** El endpoint no tiene ninguna auth y el Access-Control-Allow-Origin solo lo aplica el navegador (curl/servidor lo ignoran). Cualquiera puede POSTear en bucle: (a) event_name 'Purchase' o 'Lead' con custom_data.value y currency arbitrarios (ALLOWED_EVENTS incluye Purchase) -> contamina el pixel Colombia 1923056805076909, corrompe optimización por valor/ROAS y puede marcar la cuenta; (b) al incluir user_data.email + fbc, savePassport() hace batch/upsert por email en HubSpot -> crea/edita contactos arbitrarios en el CRM del cliente (spam/pollución de la base de ~2900 leads) sin login.
- **Fix:** Validar el header Origin/Referer server-side y rechazar (403) si no está en ALLOWED_ORIGINS; añadir rate-limiting por IP; quitar 'Purchase' de ALLOWED_EVENTS mientras no se use; no ejecutar savePassport (upsert que crea contactos) desde un endpoint anónimo — mover el guardado de fbc/fbp a un flujo autenticado o condicionarlo a un token compartido.
- **Verificado:** CONFIRMADO real y explotable. Archivo verificado: /Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/landing-colombia-full/api/conversion.js. El endpoint es PÚBLICO (el .vercelignore de landing-colombia-full solo tapa *.md .env* .gitignore panel.html; api/ NO está tapado) → vivo en https://landing-colombia-full.vercel.app/api/conversion. Sin auth: el handler solo valida que exista req.body.user_data (l.32), que event_name esté en el whitelist (l.37) y que META_ACCESS_TOKEN esté seteado (l.42). 

## [19] `MEDIA` · integridad — Clasificación de presupuesto inconsistente entre panel.js y reporte.js (mismo lead, tier distinto)

- **Archivo:** web-panama-LIVE/api/reporte.js:57-66 vs web-panama-LIVE/api/panel.js:20-30
- **Evidencia:** reporte: nums=s.replace(/[^0-9]/g,' ').split... low=nums[0]; if(low>=500)premium
- **Síntoma/Riesgo:** panel.js usa midpoint() (punto medio, trata <2000 como miles) y reporte.js usa bucketRango() (toma el primer número). Un rango en dólares completos como '$1,200,000' -> bucketRango lo parte en [1,200] -> low=1 -> 'medio', subcontando compradores premium. El mismo lead puede salir como 'alto' en un panel y 'medio' en otro, y pctComprador/costoPorComprador (el KPI que a Ralph le importa) queda mal.
- **Fix:** Extraer una única función de tiering compartida entre crm/panel/reporte; normalizar montos en dólares completos vs 'mil' de forma consistente.
- **Verificado:** CONFIRMADO real, reproducible con data VIVA (aunque el ejemplo del finder, "$1,200,000", es contrived y NO ocurre: el form solo emite 4 valores fijos). El disparador real es la opción #2 del formulario, "$250K - $350K", presente idéntica en Panamá (index.html:1131-1134) y Colombia. Verificado ejecutando ambas funciones reales sobre las 4 opciones vivas: 3 coinciden, pero "$250K - $350K" diverge -> reporte.js bucketRango() = "medio" (toma el número bajo 250 vs umbral 300); panel.js midpoint()+tie

## [20] `MEDIA` · seguridad — CAPI relay escribe en HubSpot SIN autenticación (inyección/sobrescritura de contactos)

- **Archivo:** web-panama-LIVE/api/conversion.js (65-80) y espejo landing-colombia-full/api/conversion.js (71-85)
- **Evidencia:** PA L74: fetch('.../contacts/batch/upsert', {inputs:[{idProperty:'email', id:user_data.email, properties:props}]}) — sin verificar que el request venga de un lead legítimo. No hay auth previa en todo el handler.
- **Síntoma/Riesgo:** El endpoint /api/conversion NO tiene clave ni firma (cualquiera en internet puede hacer POST). savePassport() hace un upsert a HubSpot por email. Un atacante puede POSTear {event_name:'Lead', user_data:{email:'lo-que-sea@x.com'}, event_id:'x'} y HubSpot CREA el contacto (o si el email ya existe, SOBRESCRIBE fb_fbc/fb_fbp/fb_event_id). Impacto: (1) inyección masiva de contactos basura contaminando la base de ~2900 leads reales y consumiendo cupo de HubSpot; (2) corrupción de atribución/dedup CAPI de leads reales sobrescribiendo su fb_event_id con un valor del atacante. Con ?debug=1 (Panamá, línea 97) además devuelve el id y props del contacto creado, confirmando el impacto.
- **Fix:** No permitir CREATE desde este endpoint: usar update-only (o exigir que el email ya exista como lead). Añadir un secreto compartido/HMAC o token efímero por sesión, rate-limit por IP, y validar tipos. Quitar el volcado de la respuesta de HubSpot en ?debug=1.
- **Verificado:** CONFIRMADO y explotable sin credenciales. Leí ambos archivos: web-panama-LIVE/api/conversion.js (handler L17-102, savePassport L65-80, debug L97) y landing-colombia-full/api/conversion.js (L23-107, savePassport L71-85). El handler NO tiene clave/HMAC/firma; solo valida método POST, presencia de user_data, event_name contra allowlist y que exista META_ACCESS_TOKEN en env. El CORS (Access-Control-Allow-Origin) es defensa solo de navegador: un POST server-side con curl lo ignora. conversion.js NO e

## [21] `MEDIA` · integridad — CAPI relay sin auth ni rate-limit permite envenenar el pixel de Meta (incluye Purchase)

- **Archivo:** web-panama-LIVE/api/conversion.js (29-32,82-90) y landing-colombia-full/api/conversion.js (36-39,87-95)
- **Evidencia:** L29 ALLOWED_EVENTS con 'Purchase'; L82-90 POST directo a graph.facebook.com/PIXEL_ID/events con event_name y custom_data del atacante. No hay clave, firma ni límite.
- **Síntoma/Riesgo:** Sin autenticación, cualquiera puede inyectar eventos arbitrarios al pixel (ALLOWED_EVENTS incluye 'Lead','Purchase','CompleteRegistration'). Un atacante puede inflar conversiones/Purchase falsos o dispararlos en masa, corrompiendo la data de optimización y las métricas de campaña (el KPI del negocio) y quemando la calidad del dataset. No hay throttling: se puede automatizar a miles de requests.
- **Fix:** Rate-limit por IP; restringir ALLOWED_EVENTS a lo que realmente emite el sitio (quitar Purchase si no se usa); validar event_source_url contra el dominio propio; considerar token efímero emitido por la landing.
- **Verificado:** CONFIRMADO leyendo web-panama-LIVE/api/conversion.js y landing-colombia-full/api/conversion.js. El relay CAPI es una función serverless de Vercel pública (vive; la memoria confirma CAPI emitiendo eventos) SIN autenticación, firma ni rate-limit. La única defensa es el header CORS Access-Control-Allow-Origin, que es protección del navegador y un atacante con curl la ignora; en Colombia ALLOWED_ORIGINS solo se usa para setear el header de respuesta, nunca para rechazar la request. ALLOWED_EVENTS in

## [22] `MEDIA` · seguridad — Bypass de auth por User-Agent en vigia.js: escrituras a HubSpot y supresión de alertas sin clave

- **Archivo:** /Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/web-panama-LIVE/api/vigia.js
- **Evidencia:** const isCron = ua.includes('vercel-cron'); ... if(!isCron && !okKey){ res.status(401)... }  (líneas 65, 70)
- **Síntoma/Riesgo:** isCron = ua.includes('vercel-cron') y el cron 'entra sin key'. El header User-Agent es trivialmente falsificable (curl -H 'User-Agent: vercel-cron'), así que SIN clave un atacante ejecuta todo vigia: (a) ?setup crea propiedades en HubSpot; (b) ?seed=1&window=10080 estampa vigia_alerta en los ~100 leads más recientes marcándolos como ya-avisados → SUPRIME en silencio las alertas de compradores calificados (mata el KPI del negocio); (c) inunda el Telegram del Jefe con mensajes HOT/normales.
- **Fix:** No confiar en User-Agent. Autenticar los crons con CRON_SECRET (Authorization: Bearer del entorno de Vercel) y exigirlo siempre. El UA no es prueba de identidad.
- **Verificado:** CONFIRMADO leyendo el archivo y la config de deploy. vigia.js:64-70: `isCron = ua.includes("vercel-cron")` y `if(!isCron && !okKey) 401`. La UA es falsificable (curl -H 'User-Agent: vercel-cron') => bypass de auth SIN clave. El endpoint ES publico y esta desplegado: api/vigia.js NO esta en .vercelignore y vercel.json define 5 crons a /api/vigia?window=... sin key, confirmando que vive en panama.playablancaresidences.com/api/vigia apoyandose SOLO en el chequeo de UA. Un atacante sin credenciales 

## [23] `MEDIA` · bug — Nombre de lead con metacaracteres Markdown rompe el envío a Telegram y la alerta se pierde para siempre

- **Archivo:** /Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/web-panama-LIVE/api/vigia.js
- **Evidencia:** body: JSON.stringify({chat_id:chat, text, parse_mode:'Markdown'}) (línea 92) ; if(!dry) await stampAlerta(c.id); (línea 188, incondicional)
- **Síntoma/Riesgo:** El nombre/email del lead (entrada libre del formulario) se interpola en el mensaje enviado con parse_mode:'Markdown'. Un nombre con '*', '_' o '[x](url)' desbalanceado hace que Telegram responda 400 'can't parse entities' y no entregue el aviso. Peor: tras el envío se ejecuta siempre stampAlerta(c.id) (línea 188, fuera del if/else), así que el lead queda marcado como ya-avisado y NUNCA se reintenta → un comprador calificado (el KPI del negocio) se pierde en silencio.
- **Fix:** Escapar el texto del usuario para MarkdownV2 (o usar parse_mode HTML con escape), y solo estampar vigia_alerta si el envío devolvió ok:true; si el envío falla, NO marcar para que el próximo cron reintente.
- **Verificado:** CONFIRMADO leyendo /web-panama-LIVE/api/vigia.js. Cadena verificada end-to-end: (1) linea 92 envia a Telegram con parse_mode:"Markdown" interpolando datos libres del lead; el nombre va envuelto en *${nombre}* (l.151/166/180) y el EMAIL va crudo sin envolver (l.167/182 `✉️ ${l.email}`). (2) telegram() (l.88-95) NO lanza en respuesta 400: un 400 "can't parse entities" es una respuesta HTTP resuelta, r.json() la parsea, j.ok=false, no hay throw. (3) linea 188 `if(!dry) await stampAlerta(c.id)` esta

## [24] `MEDIA` · compliance — Simulador de renta para inversionistas (proyección de ingresos/ROI) en AMBAS landings — riesgo de baneo Meta Vivienda

- **Archivo:** web-panama-LIVE/index.html:1293 (y landing-colombia-full/index.html:1294)
- **Evidencia:** 'Simulador para inversionistas' · '¿Cuánto podría generar su propiedad?' · 'Ingreso neto estimado al mes $2,140 USD' · 'Ingreso acumulado estimado $25,675 en 12 meses'
- **Síntoma/Riesgo:** La sección #simulador presenta la propiedad como instrumento de inversión y proyecta ingresos por alquiler ('Simulador para inversionistas', '¿Cuánto podría generar su/tu propiedad?', 'Ingreso neto estimado al mes $2,140 USD', 'Ingreso acumulado estimado $25,675 en 12 meses'). Meta clasifica bienes raíces en Categoría Especial VIVIENDA; anuncios que apuntan a una landing que promete/estima rentabilidad por alquiler suelen ser rechazados y, repetidos, restringen la cuenta de ads (act_852024635148139). Viola la regla dura de CLAUDE.md ('PROHIBIDO rentabilidad/retorno... ingresos por alquiler como promesa'). El disclaimer legal no neutraliza el rechazo del revisor de Meta.
- **Fix:** Quitar el simulador de ROI de la landing que recibe tráfico de Meta Vivienda (o servir una variante sin #simulador para el tráfico pagado). Si se conserva, mover la calculadora detrás del formulario (post-lead) y eliminar cifras de 'ingreso neto/acumulado' del contenido público indexable. Confirmar con Ralph/Juan la aceptación explícita del riesgo antes de dejarlo vivo.
- **Verificado:** CONFIRMADO como real y público. La sección #simulador existe verbatim en AMBAS landings vivas: web-panama-LIVE/index.html (comentario línea 1293, contenido 1294-1362) y landing-colombia-full/index.html (1294, 1295-1363). index.html NO está en ningún .vercelignore (solo excluyen paneles/docs internos), así que es 100% pública. Las cifras de ingreso ($2,140 neto/mes, $25,675 en 12 meses) están HARDCODEADAS como defaults en el HTML estático — se renderizan aun sin JS y las ve cualquier crawler/revi

## [25] `MEDIA` · compliance — Sección #rentas presenta ingresos por alquiler como beneficio ('póngalo a trabajar', 'retorno por alquiler') — prohibido en Housing

- **Archivo:** web-panama-LIVE/index.html:1274 (y landing-colombia-full/index.html:1275)
- **Evidencia:** 'póngalo a trabajar' · 'con potencial de retorno por alquiler'
- **Síntoma/Riesgo:** El copy vende el retorno económico del inmueble: 'Su propiedad, también una oportunidad', 'póngalo a trabajar', 'Una unidad en Panamá, en dólares, con potencial de retorno por alquiler'. Es exactamente 'ingresos por alquiler como promesa', prohibido por CLAUDE.md y sensible para Meta VIVIENDA. Aunque el bullet lleva 'potencial' y hay usd-note, el encabezado y CTA enmarcan la compra como inversión de renta, lo que puede disparar rechazo del anuncio y penalización de cuenta.
- **Fix:** Reescribir la sección a uso/disfrute y flexibilidad ('úsela cuando quiera; el programa de alquiler vacacional gestionado evita que quede vacía') SIN prometer ni cuantificar retorno. Eliminar 'potencial de retorno por alquiler' del texto público. Mantener el matiz de que el rendimiento no está garantizado.
- **Verificado:** CONFIRMADO parcialmente, pero severidad rebajada de alta a media. La copy existe verbatim y es publica en ambas landings vivas: web-panama-LIVE/index.html:1274-1279 y landing-colombia-full/index.html:1275-1280 ("Su propiedad, tambien una oportunidad", "pongalo a trabajar", "con potencial de retorno por alquiler"). Enmarca la compra como oportunidad de renta en una landing de VIVIENDA/Housing, lo que roza la regla dura de CLAUDE.md. NO es bug/crash ni fuga de seguridad; es compliance.

El finder 

## [26] `MEDIA` · fiabilidad — El lead CUALIFICADO llega al CRM solo por fetch cliente a api.hsforms.com; sin fallback server-side que lleve teléfono/presupuesto

- **Archivo:** web-panama-LIVE/index.html:2296 (sendToHubSpot) + web-panama-LIVE/api/conversion.js:65 (savePassport); idéntico en Colombia
- **Evidencia:** fetch('https://api.hsforms.com/submissions/v3/integration/submit/...').catch(...) — savePassport() solo setea fb_fbc/fb_fbp/fb_event_id
- **Síntoma/Riesgo:** La única vía que persiste nombre/teléfono/objetivo/rango (el dato que define 'lead cualificado') es un fetch del navegador a https://api.hsforms.com. Ese host lo bloquean con frecuencia adblockers/navegadores de privacidad (uBlock, Brave, AdGuard listan HubSpot como tracker) y también cae ante fallo de red o corte de HubSpot. El .catch se traga el error y doRedirect() manda igual a /gracias, así que el usuario cree que envió y el equipo no se entera. El respaldo server-side (/api/conversion → savePassport) SOLO hace upsert de fb_fbc/fb_fbp/fb_event_id por email; NO guarda teléfono, nombre ni presupuesto. Resultado: lead perdido o contacto 'pelón' sin datos para vender ni contactar.
- **Fix:** Crear un proxy server-side /api/lead que reciba el payload completo y haga contacts upsert a HubSpot (nombre, teléfono, rango_de_inversion, objetivo, UTMs) usando HUBSPOT_TOKEN del entorno, invocado con keepalive en paralelo al submit de hsforms; o extender conversion.js para que persista custom_data (rango/objetivo/phone) en el contacto. Así, si hsforms cae/está bloqueado, el lead cualificado igual entra por servidor.
- **Verificado:** CONFIRMADO (fiabilidad, no seguridad). La data cualificadora (phone + rango_de_inversion + objetivo + nombre) llega a HubSpot SOLO por fetch cliente a api.hsforms.com (index.html:2296 Panamá / :2272 Colombia). El .catch se traga el fallo y hsPromise.then(doRedirect).catch(doRedirect)+setTimeout(doRedirect,2000) manda a /gracias pase lo que pase → fallo invisible para usuario y equipo. El respaldo server-side conversion.js savePassport (:65 PA / :75 CO) SOLO hace upsert de fb_fbc/fb_fbp/fb_event_

## [27] `MEDIA` · integridad — /api/conversion sin autenticación: permite inyectar eventos Lead falsos al Pixel y upsert arbitrario de contactos en HubSpot

- **Archivo:** web-panama-LIVE/api/conversion.js:17 (y landing-colombia-full/api/conversion.js:23)
- **Evidencia:** module.exports async handler → sin chequeo de key; ALLOWED_EVENTS valida solo el nombre, no la procedencia; savePassport hace contacts/batch/upsert por email del payload
- **Síntoma/Riesgo:** El endpoint no exige clave ni verifica origen del lado servidor (el header CORS solo restringe navegadores, no un curl). Un atacante puede POSTear repetidamente {event_name:'Lead', user_data:{email:...}} y (a) contaminar el Pixel (2195180334399669 / 1923056805076909) con conversiones Lead falsas que sesgan la optimización y el ROAS reportado, y (b) crear/upsertar contactos basura en HubSpot vía savePassport (batch/upsert por email). Sin rate-limit ni verificación, es abusable para envenenar la data de campaña y ensuciar el CRM.
- **Fix:** Añadir verificación de origen/referer server-side y un token compartido o firma HMAC de un solo uso emitida por la propia landing; limitar tasa por IP; y en savePassport, no crear contactos nuevos por email arbitrario (usar update-only o validar que el email ya existe / provino de un submit legítimo).
- **Verificado:** CONFIRMADO real=true, severidad media (correcta). Verificado leyendo web-panama-LIVE/api/conversion.js y landing-colombia-full/api/conversion.js + .vercelignore de ambos + los index.html.

Endpoint PÚBLICO y VIVO: conversion.js NO está en ningún .vercelignore → se despliega. Ambas landings lo llaman con fetch('/api/conversion') (Panamá index.html:2318/2353; Colombia index.html:2294/2329). No es código muerto.

Sin auth server-side (verificado): no hay chequeo de key/token/secret/HMAC ni de refer

## [28] `BAJA` · seguridad — Form de lead sin anti-bot y endpoint HubSpot posteable directamente -> CRM spammeable + alertas WhatsApp por lead basura

- **Archivo:** /Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/web-panama-LIVE/index.html
- **Evidencia:** const PORTAL_ID = '6874300'; const FORM_GUID = '6a6d9dfe-74e4-4078-8b1c-18a3a814a0f8'; fetch('https://api.hsforms.com/submissions/v3/integration/submit/'+PORTAL_ID+'/'+FORM_GUID, ...)
- **Síntoma/Riesgo:** El form #leadForm no tiene honeypot, captcha ni control de tiempo minimo, y sendToHubSpot (lineas ~2262-2296) postea a api.hsforms.com/submissions/v3/integration/submit/6874300/6a6d9dfe-74e4-4078-8b1c-18a3a814a0f8 con PORTAL_ID y FORM_GUID visibles en el HTML. Cualquiera puede automatizar envios de leads falsos; cada uno dispara el vigia -> grupo WhatsApp de asesores y ensucia los ~2900 leads y el KPI de 'lead cualificado' que le importa a Ralph.
- **Fix:** Anadir un campo honeypot oculto + rechazo si se llena, y una comprobacion de tiempo minimo de llenado (>2-3s). Idealmente enrutar el envio por un endpoint propio same-origin (reutilizar /api/crm o /api/hs-webhook) con rate-limit por IP antes de reenviar a HubSpot, o hCaptcha invisible en el paso 3.
- **Verificado:** CONFIRMADO leyendo el archivo. #leadForm (index.html:1090-1207) NO tiene honeypot, captcha ni chequeo de tiempo minimo; las vars formStarted/formSubmitted son solo analytics (StartForm/FormAbandoned), no gate anti-bot. sendToHubSpot postea DIRECTO desde el cliente a api.hsforms.com/submissions/v3/.../6874300/6a6d9dfe-... (linea 2296), sin pasar por ningun endpoint propio con rate-limit. Un atacante sin credenciales puede curl-ear el endpoint e inyectar leads basura -> cada uno dispara el vigia a

## [29] `BAJA` · ux — El embed 'Panel de Juan' pide teclear la clave maestra que la propia página ya conoce (gate redundante, sin protección) y no entra en modo embed

- **Archivo:** /Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/web-panama-LIVE/ceoapp1409.html (blobFrame líneas 914-919; B64_PANELJUAN líneas 794, 810, 836)
- **Evidencia:** blobFrame crea el blob con URL.createObjectURL SIN query (?k, embed, theme). En paneljuan `KEY=_P.get('k')||_P.get('key')||sessionStorage.getItem('pb_juan_master')||''` => vacío en primera visita (el padre nunca setea pb_juan_master) => showGate('') muestra el <input type=password>. Tampoco llega embed=1 (línea 791) => no aplica modo seamless.
- **Síntoma/Riesgo:** Al pulsar 'Panel de Juan' aparece una pantalla de login pidiendo 'Clave de acceso' en lugar del panel, aunque el resto del panel ya cargó leads sin pedir nada (inconsistencia). El gate no aporta seguridad: el master 890D65 está en el mismo HTML público (línea 488) y /api/panel lo acepta, así que solo agrega fricción. Además se ve con su propia barra/marca en vez de integrado.
- **Fix:** Inyectar clave y tema al iframe: o setear sessionStorage.setItem('pb_juan_master', KEY) antes de abrir el embed, o pasar la clave/embed vía postMessage al cargar (paneljuan ya escucha 'pbtheme'; añadir un mensaje 'pbkey' que dispare load()), y marcar embed. (No resuelve la exposición del secreto —eso es el hallazgo del 890D65— pero elimina la fricción/inconsistencia.)
- **Verificado:** CONFIRMADO (UX, no seguridad). Verificado leyendo ceoapp1409.html y decodificando el blob B64_PANELJUAN. Mecanismo real: blobFrame (lineas 914-919) crea el iframe con URL.createObjectURL SIN query (no ?embed=1, no ?k=, no ?theme=), no setea sessionStorage.pb_juan_master y no envia la clave por postMessage; solo manda pbtheme tras load (917). Dentro de paneljuan: _P=URLSearchParams(location.search) queda vacio; embed=1 nunca aplica (791) -> panel muestra su propia barra/marca; KEY=_P.get('k')||_P

## [30] `BAJA` · seguridad — crmceo acepta la clave por query param (?k=) y la envía en la URL a /api/panel

- **Archivo:** web-panama-LIVE/crmceo.html:572
- **Evidencia:** KEY = new URLSearchParams(location.search).get('k') || sessionStorage.getItem('pb_panel_key') || ''; ... (l.585) fetch(`/api/panel?key=${encodeURIComponent(k)}&pais=...`)
- **Síntoma/Riesgo:** La clave de acceso viaja en la query string: queda en el historial del navegador, en los logs de acceso de Vercel y en cualquier link que Ralph copie/comparta con ?k=... (ese link = acceso directo al panel). El Referrer-Policy strict-origin-when-cross-origin evita el leak a terceros vía Referer, pero no el historial ni los logs.
- **Fix:** Aceptar la clave solo por el formulario del gate y transmitirla en un header (o cookie httpOnly de sesión) en vez de ?key=; eliminar el soporte de ?k= en la URL. En el backend leer la clave de header/cookie, no de req.query.
- **Verificado:** CONFIRMADO, severidad baja correcta (no exagerada). Verificado contra código real: crmceo.html:572 lee la clave de ?k= (URLSearchParams.get('k')) y crmceo.html:585 la manda como /api/panel?key=<clave> en la query string; api/panel.js:106-107 efectivamente valida req.query.key (401 si inválida). crmceo.html NO está en .vercelignore -> es público. Síntoma concreto y garantizado: en CADA carga y en el auto-refresh de 5 min se dispara /api/panel?key=<clave> -> la clave queda en los access logs de Ve

## [31] `BAJA` · integridad — CompleteRegistration se vuelve a disparar en sesiones nuevas -> conversiones infladas en Meta

- **Archivo:** web-panama-LIVE/gracias.html:30-43
- **Evidencia:** gracias.html:32-35 var hasLead=localStorage.getItem('pb_lead_name'); var alreadyFired=sessionStorage.getItem('pb_cr_fired'); ... sessionStorage.setItem('pb_cr_fired','1')
- **Síntoma/Riesgo:** El disparo de fbq('track','CompleteRegistration') se protege con un flag en sessionStorage ('pb_cr_fired'), pero el gatillo 'pb_lead_name' vive en localStorage y NO se borra nunca (confirmado: solo se escribe en index.html:2221, ningun removeItem en todo el proyecto). Como sessionStorage se reinicia en cada sesion de navegador, un lead que vuelva a /gracias en una sesion nueva (recarga tras cerrar el navegador, marcador, enlace compartido, o navegacion atras) re-dispara CompleteRegistration SIN haber enviado un nuevo lead. Resultado: conversiones fantasma que ensucian CPA/optimizacion de Meta -> contamina justo la senal de calidad/ROAS que es el KPI del cliente.
- **Fix:** Persistir el flag de 'ya disparado' o consumir el gatillo: tras disparar, hacer localStorage.removeItem('pb_lead_name') (y pb_lead_phone/objetivo/rango/tipo), o mover el flag 'pb_cr_fired' a localStorage ligado al eventId del lead. Asi CompleteRegistration se dispara exactamente una vez por submission real.
- **Verificado:** CONFIRMADO como defecto de codigo real, pero severidad rebajada de media a baja. Verificado en disco: gracias.html:32-35 lee el trigger pb_lead_name de localStorage (escrito via lsSet -> localStorage.setItem en index.html:1724 y 2221, persiste para siempre) mientras el flag anti-duplicado pb_cr_fired vive en sessionStorage (gracias.html:33-35). Grep confirma que NO existe ningun removeItem de pb_lead_* en todo el proyecto (los unicos removeItem son de claves de auth pb_juan_master/pb_panel_key).

## [32] `BAJA` · compliance — gracias.html usa 'financiamiento directo' -> riesgo de politica Vivienda de Meta (implica 'sin banco')

- **Archivo:** web-panama-LIVE/gracias.html:343 y 377
- **Evidencia:** gracias.html:343 'opciones de financiamiento' | gracias.html:377 'opciones de financiamiento directo'
- **Síntoma/Riesgo:** La pagina de gracias (destino post-lead ligado a la campana, publicamente accesible y revisable por Meta) promete 'opciones de financiamiento' y 'financiamiento directo'. 'Financiamiento directo' implica financiacion sin intermediario bancario, que cae bajo las reglas duras de CLAUDE.md (prohibido 'sin banco' en HOUSING). Riesgo de rechazo/flag de la cuenta publicitaria por categoria especial Vivienda.
- **Fix:** Quitar 'directo' y evitar prometer financiacion sin banco. Usar copy neutro ya verificado con el cliente, p.ej. 'planes de pago' u 'opciones de pago flexibles', sin afirmar financiamiento propietario/sin banco.
- **Verificado:** Verificado leyendo gracias.html. Existe el texto: L343 "opciones de financiamiento" y L377 "opciones de financiamiento directo". La página es pública/viva (no está en .vercelignore; es el destino post-lead). PERO el finder exageró la severidad "media" y sobre-extendió el caso: (1) L343 "opciones de financiamiento" es lenguaje estándar inmobiliario, NO prohibido = falsa alarma dentro del hallazgo. (2) La equivalencia "financiamiento directo = sin banco" es una interpretación estirada: CLAUDE.md p

## [33] `BAJA` · fiabilidad — Logos de los 5 correos-preview se bloquean por CSP si la galeria se abre por el dominio *.vercel.app

- **Archivo:** web-panama-LIVE/emails/index.html (srcdoc, ej. linea 95) + vercel.json CSP img-src
- **Evidencia:** srcdoc: <img src="https://panama.playablancaresidences.com/logo-white.png"> ; CSP: img-src 'self' data: https://www.facebook.com ... (sin el custom domain)
- **Síntoma/Riesgo:** Cada srcdoc referencia el logo con URL absoluta https://panama.playablancaresidences.com/logo-white.png. La CSP del sitio es img-src 'self' (sin ese host explicito). En el dominio canonico coincide con 'self' y carga; pero si la pagina se sirve por el alias landing-panama.vercel.app, 'self' ya no es panama.playablancaresidences.com -> los 5 logos quedan bloqueados y las previews salen con imagen rota.
- **Fix:** En los srcdoc de la galeria usar ruta raiz relativa '/logo-white.png' (carga same-origin en cualquier host). Los correos reales que se envian por el ESP deben mantener la URL absoluta; separar la variante de preview de la de envio, o anadir el dominio a img-src.
- **Verificado:** CONFIRMADO y correctamente calificado como baja. Verificado leyendo los archivos: (1) vercel.json:33 define img-src 'self' data: https://www.facebook.com ... SIN incluir panama.playablancaresidences.com; (2) web-panama-LIVE/emails/index.html tiene exactamente 5 srcdoc con <img src="https://panama.playablancaresidences.com/logo-white.png"> (lineas 95,134,173,215,254) y CERO refs relativas /logo; (3) emails/index.html NO esta en .vercelignore (solo se ignoran los 5 correos sueltos + preview.html) 

## [34] `BAJA` · ux — Saludo y WhatsApp personalizados quedan 'pegados' en visitas repetidas a /gracias

- **Archivo:** web-panama-LIVE/gracias.html:417-443
- **Evidencia:** gracias.html:419 leadName=localStorage.getItem('pb_lead_name')||''; :429 greetingEl.textContent='Gracias, '+firstName
- **Síntoma/Riesgo:** Misma raiz que el hallazgo de CompleteRegistration: como pb_lead_name/objetivo/rango nunca se limpian, cualquier visita futura a /gracias (aunque no haya enviado nada esta vez) muestra 'Gracias, <nombre>' y pre-rellena el mensaje de WhatsApp con datos de un lead anterior. Confuso si el dispositivo es compartido o si el usuario vuelve semanas despues.
- **Fix:** Consumir/limpiar los datos del lead tras usarlos en la personalizacion (localStorage.removeItem de pb_lead_*), de modo que la personalizacion solo aplique al flujo inmediato post-envio.
- **Verificado:** CONFIRMADO leyendo los archivos. Ciclo de vida: index.html:2221-2225 escribe pb_lead_name/phone/objetivo/rango/tipo en localStorage (via lsSet) al enviar el form, antes del redirect a /gracias. gracias.html:419-443 los lee en CADA carga y personaliza el saludo "Gracias, <nombre>" (#greetingName, existe en :342) y pre-rellena el href del boton WhatsApp (#waBtn, existe en :345) con nombre+objetivo+rango. Grep exhaustivo de removeItem en todo el proyecto: NUNCA se borra ninguna clave pb_lead_* (los

## [35] `BAJA` · fiabilidad — El form trata cualquier respuesta HTTP (incl. 400/403/500) como éxito: pérdida silenciosa de leads

- **Archivo:** /Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/landing-colombia-full/index.html:2272
- **Evidencia:** return fetch('https://api.hsforms.com/.../submit/'+PORTAL_ID+'/'+FORM_GUID, {...}).catch(function(err){ console.warn(...) });  // sin chequear response.ok
- **Síntoma/Riesgo:** sendToHubSpot() solo hace fetch(...).catch(); fetch NO rechaza en respuestas 4xx/5xx, solo en error de red. Nunca se revisa response.ok. Por eso hsPromise.then(doRedirect) se ejecuta igual y el usuario SIEMPRE cae en /gracias como si hubiera enviado. Si el form de HubSpot se rompe (GUID deshabilitado, propiedad renombrada/eliminada, portal en pausa), TODOS los leads desaparecen sin ninguna señal ni al usuario ni al media buyer: el visitante ve 'Solicitud recibida' pero el lead nunca entra al CRM. Idéntico patrón en sendCAPI().
- **Fix:** En sendToHubSpot añadir .then(r => { if(!r.ok) throw new Error('HS '+r.status); }); registrar el fallo en Clarity (window.clarity('set','hs_submit_fail',status)) o a un endpoint de alerta para tener visibilidad; mantener el redirect a /gracias pero disparar una señal de fallo para poder detectar caídas del form.
- **Verificado:** CONFIRMADO a nivel de código (landing-colombia-full/index.html). sendToHubSpot() (líneas 2237-2278) hace `return fetch(...).catch(...)` SIN verificar `response.ok`; fetch no rechaza en 4xx/5xx, solo en error de red. En la línea 2208 `hsPromise.then(doRedirect).catch(doRedirect)` redirige a /gracias en ambas ramas, por lo que el visitante SIEMPRE ve éxito aunque HubSpot devuelva 400/403/404/500. sendCAPI() (2280-2318) repite el patrón fire-and-forget, pero su resultado ni siquiera condiciona el r

## [36] `BAJA` · compliance — La Política de Privacidad de Colombia declara el ID de pixel EQUIVOCADO (el de Panamá)

- **Archivo:** landing-colombia-full/privacidad.html:182
- **Evidencia:** "El Meta Pixel (ID: 2195180334399669) instala las cookies _fbp y _fbc..." — pero index.html:59 y gracias.html:24 cargan fbq('init','1923056805076909')
- **Síntoma/Riesgo:** El documento legal informa a los titulares un identificador de rastreo que NO es el que realmente se ejecuta. 2195180334399669 es el pixel de Panamá; el de Colombia es 1923056805076909. Divulgación de datos inexacta (Ley 81/2019, RGPD/CCPA) que confunde a quien audite el rastreo o ejerza derechos.
- **Fix:** Reemplazar en privacidad.html:182 el ID 2195180334399669 por 1923056805076909 (pixel Colombia), que es el que instalan index.html y gracias.html.
- **Verificado:** CONFIRMADO factualmente. landing-colombia-full/privacidad.html:182 declara literalmente "El Meta Pixel (ID: 2195180334399669)" — ese es el pixel de PANAMÁ. Las páginas que realmente se ejecutan en el sitio Colombia cargan otro pixel: index.html:59 y gracias.html:24 hacen fbq('init','1923056805076909') y los noscript img (index.html:65 / gracias.html:43) usan id=1923056805076909. El grep en todo el proyecto Colombia confirma que 2195180334399669 aparece SOLO en esa línea de la política; el pixel 

## [37] `BAJA` · fiabilidad — CompleteRegistration se re-dispara en visitas nuevas e infla conversiones en Meta

- **Archivo:** landing-colombia-full/gracias.html:27-40
- **Evidencia:** guard = sessionStorage 'pb_cr_fired' (se borra al cerrar pestaña) pero el marcador 'pb_lead_name' vive en localStorage y NUNCA se limpia (grep removeItem = 0 en index.html/gracias.html)
- **Síntoma/Riesgo:** El comentario dice 'una sola vez por lead', pero el anti-duplicado es por sesión de pestaña, no por lead. Si el usuario cierra la pestaña y vuelve a abrir /gracias (historial, autocompletar, back), sessionStorage está vacío y pb_lead_name sigue en localStorage → CompleteRegistration se dispara de nuevo SIN lead nuevo. Meta cuenta conversiones fantasma y ensucia la optimización/ROAS.
- **Fix:** Ligar el anti-duplicado a un id persistente por lead: en el submit (index.html) guardar el eventId en localStorage (pb_lead_eid) y en gracias.html disparar CR solo si no existe un flag persistente pb_cr_fired_<eid> en localStorage; o limpiar pb_lead_name/pb_lead_* tras disparar CR.
- **Verificado:** CONFIRMADO como bug real, pero severidad rebajada de "media" a "baja". Verificado leyendo los archivos: en /Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/landing-colombia-full/gracias.html (lineas 27-40) el anti-duplicado usa sessionStorage 'pb_cr_fired' (linea 30, scope por pestaña, se borra al cerrar la pestaña) mientras el marcador de lead es localStorage 'pb_lead_name' (linea 29, persistente). En index.html linea 2197 se escribe pb_lead_name y NUNCA se borra (grep -c removeItem index.ht

## [38] `BAJA` · fiabilidad — personalizeThankYou lee localStorage sin try/catch: puede lanzar excepción en webview IG/FB

- **Archivo:** landing-colombia-full/gracias.html:288-297
- **Evidencia:** línea 289: var leadName = localStorage.getItem('pb_lead_name') || '';  (sin guardia). El script de cabecera SÍ envuelve el mismo acceso en try/catch (28-39), este bloque final no.
- **Síntoma/Riesgo:** Donde el almacenamiento está bloqueado (webview in-app de IG/FB, modo privado, cookies de terceros bloqueadas) localStorage.getItem lanza SecurityError. Al no estar capturado, aborta todo el <script> final: no se muestra el saludo personalizado y NO se registra trackEngagement (TYPageEngaged30s/60s). El grueso del tráfico es webview de Meta.
- **Fix:** Envolver el acceso en try/catch (o reutilizar un helper lsGet como en index.html) y degradar en silencio, igual que ya hace el bloque de CompleteRegistration de la cabecera.
- **Verificado:** CONFIRMADO como defecto de código real pero de impacto mínimo (severidad baja, en el límite). Verificado en /Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/landing-colombia-full/gracias.html.

Hechos de código (correctos): línea 289 `var leadName = localStorage.getItem('pb_lead_name') || '';` no tiene try/catch, mientras que el bloque de cabecera (líneas 28-39, CompleteRegistration) SÍ lo envuelve. Además `personalizeThankYou()` (288-297) y `trackEngagement()` (300-314) son dos IIFE ejecutad

## [39] `BAJA` · compliance — La política declara WhatsApp como único canal de seguimiento, pero se quitó de la landing

- **Archivo:** landing-colombia-full/privacidad.html:174,203,221,351
- **Evidencia:** "El único canal de seguimiento es WhatsApp..." y "Número de teléfono / WhatsApp" — pero se removió WhatsApp de las landings y el campo es teléfono/celular.
- **Síntoma/Riesgo:** Inconsistencia entre la práctica declarada y la landing en producción. No rompe la página, pero una política que describe un canal/base de consentimiento que no coincide con lo implementado es riesgo de exactitud legal.
- **Fix:** Alinear la redacción: describir el canal como llamada/teléfono (y WhatsApp solo si de verdad se usa) y ajustar la base legal 'Consentimiento explícito' asociada.
- **Verificado:** VERIFICADO. Las 4 citas en landing-colombia-full/privacidad.html existen textualmente: L174 "Número de teléfono / WhatsApp"; L203-204 "Contactarle vía WhatsApp..." con base legal "Consentimiento explícito"; L221 "El único canal de seguimiento es WhatsApp..."; L351 "Teléfono / WhatsApp". Y confirmé la otra mitad: en index.html WhatsApp fue realmente retirado (única mención = comentario CSS L798 "botón WhatsApp flotante retirado"; el campo es type=tel name=phone "teléfono / celular"). La inconsist

## [40] `BAJA` · integridad — reporte.js reporta inversión=0 y leads=0 en silencio si Meta falla o el token expira

- **Archivo:** web-panama-LIVE/api/reporte.js:19-28,137-156
- **Evidencia:** catch (e) { return { spend: 0, leads: 0 }; }  (sin surfacing del error)
- **Síntoma/Riesgo:** metaInsights() atrapa cualquier error de Meta y devuelve {spend:0,leads:0} sin bandera de salud. El 'Reporte de Valor' que Juan le manda a Ralph puede mostrar inversion:$0, cpl:$0 y costoPorComprador:0 como si no se hubiera pautado nada, cuando en realidad el token venció o la API cambió. Falsea el KPI justo hacia el cliente. panel.js sí expone tecnico.tokenOk/pixelOk, pero reporte.js no tiene ese flag.
- **Fix:** Propagar un flag metaOk/tokenOk en el JSON de reporte.js y que el front avise 'no se pudo leer Meta' en vez de mostrar $0 como dato válido; distinguir 'cero real' de 'error'.
- **Verificado:** CONFIRMADO leyendo web-panama-LIVE/api/reporte.js. metaInsights() (líneas 19-28) devuelve {spend:0,leads:0} en cualquier fallo y el JSON del reporte (líneas 137-160) NO expone ningún flag metaOk/tokenOk. Si Meta falla para las 3 campañas ACTIVE, totSpend=0 propaga a inversion:$0 (l.142), cpl:$0 (l.143, rama totCRM) y costoPorComprador:0 (l.155), mientras los leads del CRM (fetch a /api/crm con crmKey, NO metaToken, l.88) sí se muestran → el reporte enseña leads reales junto a $0 de gasto/CPL sin

## [41] `BAJA` · fiabilidad — Versión Graph API v19.0 hardcodeada (cerca de deprecación) en crm/panel/reporte

- **Archivo:** web-panama-LIVE/api/crm.js:200, panel.js:78, reporte.js:22
- **Evidencia:** crm/panel/reporte: /v19.0/  vs  meta-events/conversion: /v22.0/
- **Síntoma/Riesgo:** crm.js, panel.js y reporte.js llaman graph.facebook.com/v19.0 mientras meta-events.js y conversion.js ya usan v22.0. Cuando Meta sunset-ee v19.0, esas llamadas empezarán a fallar; combinado con el swallow de errores, los paneles mostrarán ceros de spend/leads/ángulo sin avisar. Inconsistencia de versión = fallo diferido difícil de diagnosticar.
- **Fix:** Unificar todas las llamadas a una versión soportada (p.ej. v22.0) en una constante compartida; revisar el calendario de deprecación de Meta.
- **Verificado:** CONFIRMADO leyendo disco, pero severidad rebajada de media a baja (latente, no rompe nada hoy). Hechos verificados: (1) v19.0 hardcodeada en web-panama-LIVE/api/crm.js:200, panel.js:78, reporte.js:22 — y el finder SUBCONTÓ: parte.js:38, hs-webhook.js:109 y vigia.js:55 tambien usan v19.0; solo conversion.js:84 y meta-events.js:39 usan v22.0. (2) Mecanismo de ceros silenciosos CONFIRMADO: panel.js y reporte.js (metaInsights) envuelven la llamada en try/catch que devuelve {spend:0,leads:0,...} y ad

## [42] `BAJA` · fiabilidad — panel.js y reporte.js dependen 100% de crm.js vía URL absoluta de producción: cualquier hipo tumba todo el endpoint con 500

- **Archivo:** web-panama-LIVE/api/panel.js:115,122-123 y web-panama-LIVE/api/reporte.js:88-90
- **Evidencia:** const base="https://panama.playablancaresidences.com"; if(crm.error){ res.status(500)... }
- **Síntoma/Riesgo:** Ambos hacen fetch a la URL absoluta de prod y si crm.js devuelve error o tarda, retornan 500 sin degradación parcial (el panel queda sin nada, no muestra al menos la parte de Meta). Además, en un deploy preview o dominio alterno estos endpoints llaman igual al dominio de PRODUCCIÓN, mezclando entornos y mandando la clave a prod.
- **Fix:** Usar ruta relativa/variable de entorno para el host propio; ante fallo de crm devolver payload parcial (solo métricas Meta) en vez de 500; timeout con fallback.
- **Verificado:** CONFIRMADO el núcleo de fiabilidad; DESCARTADA la parte de seguridad (el finder exageró). Verificado en disco: panel.js:115 fija base="https://panama.playablancaresidences.com", :122 hace getJSON(`${base}/api/crm?key=${crmKey}`), :123 devuelve 500 si crm.error; getJSON (:73) no tiene try/catch, así que un throw de fetch cae al catch externo (:364)→500. reporte.js:88 hace fetch a la misma URL absoluta de prod, :90 crm.error→500, :161 catch→500. Ambos dependen 100% de crm.js: si crm falla/tarda, d

## [43] `BAJA` · bug — leads.js modo default: error de HubSpot sin .results se traga como '0 leads' con 200 OK

- **Archivo:** web-panama-LIVE/api/leads.js:223-227
- **Evidencia:** const j = await hs(...); if (!j.results) break;
- **Síntoma/Riesgo:** En el modo normal la paginación no tiene reintento: si HubSpot responde un objeto de error/rate-limit (sin .results), 'if(!j.results) break' corta y devuelve count:0/leads parciales con status 200. El panel interpreta 'no hay leads' en vez de 'hubo un error', ocultando un fallo real (a diferencia del modo audiencia que sí reintenta con searchPage).
- **Fix:** Distinguir respuesta válida vacía de error (revisar j.status/j.category); reintentar con backoff como searchPage(); si tras reintentos falla, devolver 502/flag parcial en vez de 200 con lista truncada.
- **Verificado:** CONFIRMADO leyendo web-panama-LIVE/api/leads.js. En el modo default (líneas 219-227) la paginación llama a hs() directo, sin reintento y sin flag de parcialidad, a diferencia del modo audiencia que usa searchPage() con 5 reintentos+backoff (líneas 40-47) y setea parcial=true (línea 148). hs() (líneas 27-33) hace r.json() y NO lanza en errores HTTP: una respuesta de error de HubSpot (429 rate-limit, 4xx/5xx) devuelve un body JSON tipo {status:"error",category:"RATE_LIMITS"} que se parsea bien, po

## [44] `BAJA` · seguridad — Bypass de auth por User-Agent en parte.js: spam a Telegram y coste de Gemini sin clave

- **Archivo:** /Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/web-panama-LIVE/api/parte.js
- **Evidencia:** const isCron = ua.includes('vercel-cron'); if (!isCron && key !== process.env.CRM_KEY) {...}  (líneas 17, 19)
- **Síntoma/Riesgo:** Mismo patrón: isCron por User-Agent permite disparar /api/parte sin clave. Cada llamada genera un prompt a Gemini y envía 5+ mensajes al Telegram del Jefe. Un atacante puede spamear el chat y consumir la cuota de Gemini falsificando el UA.
- **Fix:** Reemplazar la detección por UA por CRON_SECRET (Bearer) obligatorio para el cron; exigir clave siempre en el resto.
- **Verificado:** CONFIRMADO (real, pero severidad ajustada media -> baja). Verificado leyendo /web-panama-LIVE/api/parte.js lineas 16-19 y el deploy config.

BYPASS REAL: `const isCron = ua.includes("vercel-cron"); ... if (!isCron && key !== process.env.CRM_KEY) 401`. El User-Agent lo controla el atacante, asi que `curl -A "vercel-cron/1.0" https://panama.playablancaresidences.com/api/parte` pasa la puerta SIN clave. `turno` default = "am", un GET pelado funciona.

ENDPOINT PUBLICO: confirmado. .vercelignore NO 

## [45] `BAJA` · bug — parte.js casca (TypeError 500) si Gemini bloquea/trunca la respuesta; el fallback nunca corre

- **Archivo:** /Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/web-panama-LIVE/api/parte.js
- **Evidencia:** out = gj.candidates && gj.candidates[0] && gj.candidates[0].content.parts[0].text;  (línea 75)
- **Síntoma/Riesgo:** gj.candidates[0].content.parts[0].text asume que el candidato trae content.parts. Si Gemini devuelve un candidato con finishReason SAFETY/RECITATION/MAX_TOKENS sin 'content' o sin 'parts', se lanza TypeError ('cannot read properties of undefined') dentro del for, que NO está en try interno → salta al catch externo → 500. El parte del día no se envía y el fallback de texto crudo (líneas 100-103) queda como código muerto en ese escenario.
- **Fix:** Acceso defensivo: out = gj?.candidates?.[0]?.content?.parts?.[0]?.text. Así 'out' queda undefined y el retry + fallback funcionan en vez de tirar 500.
- **Verificado:** CONFIRMADO como bug real. web-panama-LIVE/api/parte.js línea 75: `out = gj.candidates && gj.candidates[0] && gj.candidates[0].content.parts[0].text`. Los guardas `&&` sólo cubren `gj.candidates` y `gj.candidates[0]`, NO `.content` ni `.parts`. Si Gemini devuelve 200 con un candidato sin `content` (finishReason SAFETY/RECITATION) o sin `parts` (MAX_TOKENS con thinking) —comportamiento documentado y no determinista de la API— acceder a `.parts[0]` lanza TypeError. El for (69-78) no tiene try inter

## [46] `BAJA` · fiabilidad — La alerta por-lead al grupo depende de un cron EXTERNO no versionado (SPOF); si cae, se dejan de avisar leads en silencio

- **Archivo:** /Users/juanescorcha/Downloads/PROYECTOS IA/META ADS/web-panama-LIVE/api/wa-lead-poll.js
- **Evidencia:** vercel.json crons NO incluye wa-lead-poll ; comentario: 'con ping cada ~3 min desde Render/cron el contenedor NO se enfría' (líneas 12-13)
- **Síntoma/Riesgo:** wa-lead-poll (el vigía que avisa cada lead al grupo de asesores) NO está en los crons de vercel.json; se dispara desde un pinger externo (cron-job.org/Render, según los comentarios) que no está en el repo. Si ese servicio se detiene o cambia de clave, las alertas en tiempo real al grupo cesan sin ningún error visible ni fallback interno, y el equipo de ventas deja de recibir leads.
- **Fix:** Mover el poll a un cron de Vercel (o confiar el aviso al webhook de HubSpot como fuente primaria y documentar el pinger como respaldo). Añadir un heartbeat/alerta si no hay corridas en X minutos.
- **Verificado:** VERIFICADO REAL, pero severidad ajustada de media a BAJA. Confirmado leyendo archivos: (1) wa-lead-poll.js NO está en los `crons` de vercel.json (solo aparece en `functions` con maxDuration:60); los crons son parte(am/pm), vigia(x5) y wa-grupo. (2) El gatillo es un pinger EXTERNO no versionado: docs/HANDOFF-SESION-12JUL.md:10 dice literal 'Trigger: cron-job.org ... pinguea /api/wa-lead-poll?key=...&mins=5 cada 2 min (Vercel Hobby NO permite cron cada 3 min)'. agente.html:126 lo marca 'EXTERNO = 

## [47] `BAJA` · fiabilidad — Dos nombres distintos para el token de Meta: si falta META_ACCESS_TOKEN el CAPI público da 500 en cada envío

- **Archivo:** web-panama-LIVE/api/conversion.js:34
- **Evidencia:** conversion.js:34 `const ACCESS_TOKEN = process.env.META_ACCESS_TOKEN;`  vs  panel.js:103 `const metaToken = process.env.META_ADS_TOKEN;`
- **Síntoma/Riesgo:** conversion.js (el endpoint CAPI que dispara el form público en AMBAS landings) exige `process.env.META_ACCESS_TOKEN` y hace `if(!ACCESS_TOKEN) return res.status(500)` (línea 35). Pero TODO el resto del backend (panel.js:103, crm.js:92, reporte.js:75, parte.js:24, vigia.js:73) usa un nombre DISTINTO: `META_ADS_TOKEN`. Ambos deben existir en Vercel. Si alguien configura solo el nombre 'obvio' (META_ADS_TOKEN), cada PageView/Lead del formulario de las landings devuelve 500 y se pierde el matcheo de conversiones en Meta, en silencio para el usuario. Es un footgun de config sin ninguna alerta.
- **Fix:** Unificar a un solo nombre (p.ej. META_ADS_TOKEN) en todos los archivos, o en conversion.js hacer fallback como ya hace meta-events.js:71: `process.env.META_ACCESS_TOKEN || process.env.META_ADS_TOKEN`. Documentar la var requerida en el README/ESTADO-PROYECTOS.
- **Verificado:** CONFIRMADO a nivel de codigo, pero es un footgun LATENTE de config, no un crash activo. Verificado leyendo los archivos: conversion.js Panama (34-35) y Colombia (41-42) exigen process.env.META_ACCESS_TOKEN y hacen `if(!ACCESS_TOKEN) return res.status(500)` SIN fallback. Otros 6 archivos usan el nombre DISTINTO META_ADS_TOKEN: crm.js:92, reporte.js:75, panel.js:103, parte.js:24, vigia.js:73, hs-webhook.js:179. Solo meta-events.js:71 tiene el fallback (`META_ADS_TOKEN || META_ACCESS_TOKEN`) y adem
