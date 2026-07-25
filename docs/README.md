# Playa Blanca — App de Meta Ads (agencia IA)

Panel de control + copiloto de IA para gestionar las campañas de **Meta Ads** del
cliente **Playa Blanca Residences** (real estate de lujo, Panamá). Todo corre
**localmente** en el Mac: un dashboard en HTML que se abre en el navegador, un
asistente que responde preguntas, un bot de Telegram y un motor que genera
creativos (anuncios 1080×1920).

> Este README es el **mapa del proyecto**. Para el paso a paso pensado para el CEO
> (no técnico), ver **[MANUAL-USO.md](MANUAL-USO.md)**.

---

## 🚦 Lo más importante primero: SEGURIDAD

- **El token de Meta da control total de la cuenta publicitaria.** Vive en
  `asistente/config.json` y en `.env`. **Nunca** se comparte, se sube a internet,
  ni se pega en un chat público. El `.gitignore` ya bloquea estos archivos.
- **La app NO enciende ni modifica nada por su cuenta.** Subir presupuestos,
  pausar o activar campañas/anuncios solo ocurre cuando **tú apruebas** una acción
  en la Bandeja. Sin tu clic, no toca la cuenta.
- **Nunca inventar** testimonios, cifras, premios ni logos: es tráfico pagado a
  inversores y tiene implicaciones de compliance.

---

## 📂 Qué es cada cosa

| Pieza | Qué es | Tocar |
|---|---|---|
| **`dashboard.html`** | El panel principal. Se abre con doble clic en el navegador. KPIs, anuncios, Bandeja, Creativos, Reportes, Asistente. | Esencial — no borrar |
| **`asistente/`** | Copiloto local: bridge del chat (`server.py`), bot de Telegram (`telegram_bot.py`) y el experto que responde. Aquí vive `config.json` con las claves. | Esencial |
| **`motor_creativos/`** | Motor en Python que convierte fotos en anuncios con la identidad de marca (tinte azul, tipografía premium, logo, precio, CTA). Incluye la biblioteca de imágenes y los assets. | Esencial |
| **`.env`** | Claves de Meta (token, app id/secret, ad account). | Secreto — nunca subir |
| **`*.backup*.html`** | Copias de respaldo del dashboard por si una edición lo rompe. | Solo respaldo |
| **`HANDOFF-Playa-Blanca.md`** | Contexto del proyecto para arrancar un chat nuevo con todo el background (landing, HubSpot, CAPI, IDs). | Doc |
| **`NOVEDADES-NOCHE.md`** | Changelog de las mejoras que el motor aplica de noche. | Doc |

**Documentación más detallada (ya existente):**
- Asistente: [`asistente/LEEME.md`](asistente/LEEME.md)
- Motor de creativos: [`motor_creativos/README.md`](motor_creativos/README.md),
  `INSTALACION.md`, `APP_INSTRUCTIONS.md`, `ESPECIFICACIONES_TECNICAS.md`,
  `PROMPT_PARA_APPS.md` (todos dentro de `motor_creativos/`).

---

## ▶️ Cómo abrir la app

1. **Doble clic en `dashboard.html`** → se abre en el navegador. Eso es la app.
2. Para que funcionen el **chat del Asistente** y la sección **Creativos**, hay que
   tener encendidos los servidores locales (abajo). Si están apagados, el dashboard
   no se rompe: avisa y deja seguir con el resto.

---

## 🖥️ Servidores locales

Son procesos de Python que corren en tu Mac. Solo necesitan **Python 3** (sin
`pip install` nada).

### 1. Asistente + bot de Telegram (`asistente/`)
Arranca 3 procesos: el bridge del chat, el responder y el bot de Telegram.

- **Arrancar:** doble clic en `asistente/iniciar.command`
  (o en terminal: `bash asistente/start.sh`).
- **Detener:** doble clic en `asistente/detener.command`
  (o `bash asistente/detener.sh`).
- **Puerto del bridge:** `http://127.0.0.1:8765` (el dashboard le manda las preguntas).
- **Logs:** `asistente/logs/`.

### 2. Motor de creativos (`motor_creativos/`)
Sirve la sección **Creativos** del dashboard y genera los PNG.

- **Arrancar:** `python3 motor_creativos/creativos_server.py`.
- **Puerto:** `http://127.0.0.1:8770`.
- Las fotos de origen están en `motor_creativos/biblioteca_imagenes/`; los anuncios
  generados salen a `motor_creativos/salidas/`.

---

## 🔑 Dónde viven las claves

| Clave | Dónde |
|---|---|
| Token de Meta, app id/secret, ad account | `.env` |
| Token de Meta + bot de Telegram + IDs de cuenta/página/form | `asistente/config.json` |
| Claves de la landing (CAPI, HubSpot, panel) | En Vercel (ver `HANDOFF-Playa-Blanca.md`) |

Ninguna clave debe copiarse a otro archivo, captura o mensaje. Si un proceso
necesita una clave, ya la lee de estos archivos.

---

## 🛟 Si algo se rompe

- Si una edición del `dashboard.html` rompe la app, **restaura el backup más
  reciente** (`dashboard.backup-*.html`): renómbralo a `dashboard.html`.
- El dashboard es un único archivo HTML con JavaScript adentro. Antes de dar por
  buena una edición se verifica que la sintaxis del script siga siendo válida.
