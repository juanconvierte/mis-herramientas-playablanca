# 🤖 CRM Playa Blanca — Proyecto completo

> Proyecto para construir un **CRM propio** que reemplace HubSpot ($900/mes) y venderle
> a Playa Blanca un ecosistema completo por **$1.400/mes**.
> Todo lo del CRM (demo, venta y construcción) vive AQUÍ, organizado en 3 carpetas.

---

## 📁 Las 3 carpetas (en orden)

### `1-DEMO/` — para VENDER 🎯
Demo interactivo del CRM (estilo Kanban premium). Se ve mejor que HubSpot.
- **Abrir:** doble-click en `1-DEMO/index.html`
- **Golpe de venta:** botón **"Simular lead nuevo"** → entra un lead → se asigna solo → correo + Telegram.
- Datos de muestra (no guarda nada — es demo).

### `2-PROPUESTA/` — para CERRAR los $1.400 💰
- `index.html` → **propuesta visual premium** (la que le muestras/mandas al cliente).
- `GUION-REUNION.md` → **qué decir** paso a paso + las **3 objeciones con respuesta**.
- **Abrir:** doble-click en `2-PROPUESTA/index.html`.

### `3-CONSTRUCCION/` — el PLANO para construirlo 🔧
El "war room" con la **estructura exacta de la Biblia App Factory**. Aquí se construye el CRM real.

**Archivos canónicos de la Biblia:**
- `CLAUDE.md` → **punto de entrada** (qué leer y en qué orden).
- `CONSTITUCION.md` → reglas fijas (seguridad, compliance).
- `prompt-maestro.md` → **brief maestro** (objetivo, stack, MVP, criterios de aceptación).
- `agent-teams.md` → los agentes de construcción (líder + frontend + BD + acceso/emails + devops + reviewer).
- `tasks.md` → tareas con estados.
- `history.md` → **registro de cambios / memoria** entre sesiones.
- `README.md` → instrucciones de setup.
- `.env.example` → **plantilla de accesos** (copiar como `.env`). · `.gitignore` → protege el `.env`.
- `ui-reference/` → referencia de diseño (apunta al demo).

**Extras del proyecto:**
- `spec-crm.md` → especificación detallada (tablas, pantallas, flujo).
- `CHECKLIST-CRM-CONFIABLE.md` → auditoría de confiabilidad (reutilizable para vender a otras empresas).
- `correos-resend.md` → copy de los correos automáticos.

---

## 🚦 Estado actual
- ✅ **Fase 0 completa:** demo, propuesta, guion y plano — todo listo.
- ⏳ **Falta arrancar la construcción** (Fase 1): esperando cuentas + `.env`.

## ▶️ Para ARRANCAR la construcción (3 pasos de Juan)
1. Crear cuenta **Supabase** → proyecto `crm-playa-blanca` → copiar URL + 2 keys.
2. Crear cuenta **Resend** → copiar API key.
3. Copiar `3-CONSTRUCCION/.env.example` → `.env` y llenar las llaves.
   ⚠️ **Las llaves van SOLO en el `.env`, nunca en el chat.**
4. Decir "listo" → Claude construye Fase 1 (tablas → form → Kanban real → login PIN).

## 💵 Números clave del negocio
- Hoy el cliente paga: **$1.300** ($400 gestión + $900 HubSpot).
- Propuesta: **$1.400** ($900 gestión + $500 CRM propio) → captura los $900 de HubSpot.
- HubSpot tiene ~70 módulos; usan ~8. Costo real de operar el CRM propio: **~$20–45/mes**.
