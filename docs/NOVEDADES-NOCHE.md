# Novedades del motor nocturno

Cambios aplicados mientras el CEO duerme. Cada ola: arreglar/probar/mejorar -> QA -> changelog.

## Wave 1 — 21:39
- Bandeja: ✅ aprobar ahora EJECUTA de verdad. set_targeting con selector de conjunto inline (no toca uno al azar). create_lookalike crea la audiencia fuente desde tu lead form y luego el lookalike, en el mismo clic.
- Audiencias: revisada (pendiente: corregir que "Enviaron tu formulario" use tu lead form real, no engagement de página).
- Bugs generales corregidos. Sintaxis OK.
- Backup actualizado.

## Wave 2 — 21:46
- Audiencias: la fuente "Enviaron tu formulario" ahora usa tu lead form REAL (1454090062522225) con subtype CUSTOM; labels honestos (separada de "Interacción con la página").
- NUEVO empleado: 🛡️ Bruno (Cumplimiento) — revisa tus creativos/copys vs políticas Meta (vivienda, claims financieros) para que no te baneen. Solo lectura.
- Sintaxis OK. Backup actualizado.

## Wave 3 — 21:55
- NUEVO empleado: 🧪 Tomás (A/B Lab) — declara anuncios GANADORES por las 3 tildes del mentor (ventas + CPC bajo el promedio + CTR sobre el promedio), marca cuáles están listos para Launch Pocket, recuerda el testeo diario. Solo lectura.
- Sintaxis OK. Backup actualizado.

## Wave 4 — 08:25
- NUEVO empleado: 📈 Rafa (Reportes) — arma un informe limpio para el cliente (KPIs con delta, mejores anuncios, por país, tendencia CPL, resumen ejecutivo) + botón Imprimir/PDF. Solo lectura.
- QA pendiente: se cortó por límite de tokens (resetea 11:30pm). Sintaxis verificada manual: OK.

## Revision 50 agentes — 09:22
- 50 auditores barrieron toda la app (18 vistas + Meta + seguridad + movil + datos + memoria + a11y + edge cases).
- App SOLIDA: 1 bug real arreglado -> PDF/impresion salia en blanco (texto blanco sobre blanco en tema oscuro), ahora legible para el cliente.
- Resto = falsos positivos / nits bajo riesgo. Seguridad verificada: nada se auto-activa, cuenta intacta. Sintaxis OK.

## Ola A saneo — 10:53
- Código muerto borrado: cluster ASIS (applyAll/recoPause/recoBudget/recoSelect/resolveCard…) + .impact-bar + huérfanos (setCur/toggleWhy/qs/gotoCrear/gotoAud/wrappers). Archivo más liviano.
- Docs nuevos: README.md + MANUAL-USO.md (paso a paso para el CEO) + .gitignore (protege token/.env/backups).
- Backups redundantes limpiados (queda 1).
- Sintaxis OK. Pendiente: seguridad/escapes (un agente pidió permiso de skill, se rehace en Ola B).

## Ola B saneo — 11:22
- Seguridad: app sólida contra XSS (esc/escJS bien usados). AÑADIDO: SRI (CDN Chart.js/JSZip firmados con integrity), CSP (Content-Security-Policy), defensa en profundidad.
- Accesibilidad: +19 aria-labels, foco de teclado.
- Rendimiento: guards de refresh / charts.
- Sintaxis OK. Backup actualizado.

## Ola C saneo — 11:38
- Responsive: ya muy sólido (drawer, tablas->tarjetas). Retoques: data-labels en barras, heatmap legible en móvil, touch targets del editor de presupuesto/chat.
- Resiliencia: ya muy buena. Retoques: rate-limit #17 con mensaje amable en load(), ping del puente Opus periódico.
- Sintaxis OK. Backup actualizado.

