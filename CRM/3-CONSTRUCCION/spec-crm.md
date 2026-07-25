# 📐 SPEC-CRM — Plano Maestro del CRM Playa Blanca

> Este es el "plano" de tu Biblia App Factory (Spec Driven Development).
> Todo lo que el CRM hace, campo por campo, decidido ANTES de codear.
> Versión 1 · 11-jul-2026 · decisiones cerradas con Juan.

---

## 1. Qué es y para quién
CRM a medida para **Playa Blanca Residences** (inmobiliaria de lujo, Panamá).
Reemplaza a HubSpot ($900/mes que usan al 5%). Optimizado para **4 asesoras de venta**.
**Objetivo:** que un lead entre, se asigne solo, y ninguna venta se pierda por desorden.

**Escala:** ~500 leads/mes. Pequeño. No necesita infraestructura enterprise.

---

## 2. Stack (de la Biblia — lo que Juan ya domina)
| Capa | Herramienta | Costo |
|---|---|---|
| Base de datos | **Supabase** (Postgres administrado) | Gratis → $25/mes |
| Hosting | **Vercel** (Pro por ser comercial) | $20/mes |
| Correos | **Resend** | Gratis → $20/mes |
| Avisos | **Telegram** (bot ya existe) | Gratis |
| Monitoreo errores | **Sentry** | Gratis |
| Cerebro IA | **Claude / Gemini** | centavos/lead |
| **Costo total operando** | | **~$20–45/mes** (cobra $500 → margen ~90%) |

---

## 3. Decisiones CERRADAS
- **Vendedoras:** 4, nombres ficticios por ahora.
- **Reparto de leads:** equitativo **round-robin 1×1** (uno pa' cada una por turno).
- **Login:** **Clave/PIN por vendedora** (simple, sin Clerk). Cada una entra con su código.
- **Correo automático:** se dispara a las **2 horas** sin contactar el lead.
- **Etapas del pipeline:** Nuevo · Interesado · Cita · Negociación · Cerrado — **+ personalizables** (No contestó, Atendió llamada, etc.).
- **HubSpot:** corre **EN PARALELO**. NO se apaga hasta que Juan pruebe y confirme.
- **Migración:** script `migrar-hubspot.js` jala el histórico de HubSpot → Supabase (Claude lo corre solo). HubSpot queda intacto (solo lectura).
- **Landing:** la MISMA que ya existe. Solo se conecta por detrás a Supabase.
- **Correo de salida (dominio):** pendiente — Juan lo define después.

---

## 4. Base de datos (tablas)

### Tabla `leads`
| Campo | Tipo | Ejemplo |
|---|---|---|
| id | uuid | (auto) |
| creado | fecha | 2026-07-11 |
| nombre | texto | Zoraida |
| apellido | texto | Martínez |
| email | texto | zoraida@... |
| telefono | texto | +507... |
| presupuesto | texto | $195k–$300k |
| plazo | texto | 6–12 meses |
| proyecto_interes | texto | Aquavista |
| angulo | texto | Retiro / vida |
| campana | texto | PB LEADS PANAMA Calidad |
| red | texto | Instagram |
| ad_id | texto | (de la URL de conversión) |
| vendedor_id | ref | → tabla vendedoras |
| estado | texto | nuevo / interesado / cita / ... |
| notas | texto | (lo que escribe la asesora) |
| origen | texto | Form Panamá / Landing Colombia |

### Tabla `vendedoras`
| Campo | Tipo |
|---|---|
| id | uuid |
| nombre | texto |
| pin | texto (código de acceso) |
| email | texto |
| telegram_id | texto (para avisos) |
| activa | sí/no |

### Tablas extra (nivel intermedio — aprendidas de Atomic CRM, MIT)
- **`notas`** — historial de conversaciones por lead.
- **`tareas`** — pendientes con recordatorio ("llamar mañana").
- **`tags`** + **`lead_tags`** — etiquetas de color (Retiro, Inversión, Caliente...).
> Modelo completo en `supabase/schema.sql`. Esto sube el CRM de "básico" a "intermedio profesional" sin volverlo un HubSpot.

### Seguridad de datos (Row Level Security)
- Cada vendedora, con su PIN, ve **SOLO sus leads asignados**.
- Admin (Juan/Dyana) ve todo.
- RLS activo en las 6 tablas; solo el backend (SERVICE_ROLE) accede y filtra.

---

## 5. Pantallas
1. **Entrada por PIN** — la vendedora pone su código → entra.
2. **Pipeline (Kanban)** — tarjetas en columnas por etapa (el diseño ya aprobado, estilo Excermol). Arrastra para cambiar etapa.
3. **Lista** — los mismos leads en tabla (para filtrar/buscar).
4. **Ficha del lead** — toda su info + notas + botones (llamar / mensaje / correo).
5. **Panel del dueño** — KPIs + valor en pipeline + cerrado (para Ralph/Dyana).

---

## 5.5 Módulos — el 5% que SÍ usan (vs. las ~70 funciones de HubSpot)
**NÚCLEO v1:** Contactos/Leads · Pipeline (Kanban) · Formularios · Workflows (auto-asignación / follow-up / avisos) · Correos (Resend) · **Tareas** · Calificación 🔥 por presupuesto · Panel/Informes.
**FASE 2:** Secuencias de correo · Plantillas/Fragmentos · Programador de reuniones · Registro de llamadas/reuniones · Metas por asesora.
**NO (bloat / no aplica):** Empresas · Tickets · Productos/Pedidos · Cotizaciones/Facturas/Pagos/Suscripciones · todo Contenidos/CMS · Anuncios (ya en Meta) · SEO/AEO/Campañas/Redes/Marca/Eventos · Servicio al cliente · Gestión de datos enterprise.
**Pitch:** HubSpot ~70 módulos → tu CRM ~8. *"No pagas por 62 funciones que nunca tocas."*

## 6. Automatizaciones
1. **Auto-asignación** — lead entra → round-robin 1×1 → queda con dueña.
2. **Correo Resend** — 2h sin contactar → correo automático al lead (copy redactado por Claude, aprobado por Juan) + aviso.
3. **Aviso Telegram** — lead nuevo → mensaje instantáneo a la vendedora asignada con toda la info.
4. **(Futuro) Agente IA de soporte** — lee quejas del grupo → cruza Meta+CRM → redacta respuesta con plan.

---

## 7. Flujo completo (de punta a punta)
```
Meta Ads → Landing (form) → Supabase (guarda lead)
   → Auto-asignación (round-robin)
   → Aviso Telegram a la vendedora
   → aparece en el Kanban de su CRM
   → si 2h sin contactar → correo Resend automático
   → vendedora mueve el lead por etapas hasta Cerrado (Venta)
   → Panel del dueño mide todo (pipeline / cerrado / ROAS)
```
En paralelo: HubSpot sigue recibiendo lo mismo (red de seguridad) hasta que Juan confíe.

---

## 8. Fuera de alcance (por ahora)
- No se apaga HubSpot todavía.
- No hay app móvil (es web, funciona en el celular igual).
- Dominio de correo: se define después.
- Agente IA de soporte: fase posterior.
