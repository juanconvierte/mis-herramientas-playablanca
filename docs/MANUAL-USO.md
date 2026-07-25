# Manual de uso — Playa Blanca (paso a paso)

Guía simple para usar la app día a día. Sin tecnicismos. Un paso a la vez.

> **Regla de oro de seguridad:** la app **nunca enciende ni cambia nada de tus
> campañas por su cuenta**. Solo actúa cuando **tú apruebas** en la Bandeja.
> Tu cuenta de Meta está intacta hasta que tú das un clic.

---

## 1. Abrir la app

1. Doble clic en **`dashboard.html`**.
2. Se abre en el navegador. Eso es tu panel de control.
3. Arriba ves tus números de hoy: **gasto, leads y CPL** (costo por lead).

Si vas a usar el **chat del Asistente** o la sección **Creativos**, primero
enciende los servidores (paso 2). Si no, puedes mirar todo lo demás igual.

---

## 2. Encender el copiloto (Asistente + Telegram)

1. Entra a la carpeta **`asistente/`**.
2. **Doble clic en `iniciar.command`**.
3. Se abre una ventana negra (Terminal) y arranca todo. Cuando diga
   *"Todo en marcha"*, ya está. Puedes cerrar esa ventana: los procesos siguen
   corriendo solos.
4. Abre **Telegram** y escribe **`/ayuda`** a tu bot para confirmar que responde.

**Para apagarlo:** doble clic en **`detener.command`** (misma carpeta).

---

## 3. Conectar / revisar que Meta está al día

- La app ya está conectada a tu cuenta de Meta (los datos de gasto/leads/CPL que
  ves arriba salen de ahí en vivo).
- Si los números **no cargan** o salen en cero: revisa que el copiloto esté
  encendido (paso 2) y recarga la página del dashboard (F5).
- No tienes que pegar ningún token: ya está guardado de forma segura.

---

## 4. Bandeja (aprobar acciones) — lo más importante

La **Bandeja** es donde el copiloto te propone cambios (subir presupuesto a un
anuncio que va bien, pausar uno que gasta sin resultados, crear una audiencia
similar, etc.).

1. Abre la sección **Bandeja**.
2. Lee cada tarjeta: dice **qué propone** y **por qué**.
3. Decide:
   - **Aprobar** → la app ejecuta ese cambio en Meta **en ese momento**.
   - **Descartar** → no pasa nada, la cuenta queda igual.

**Nada se ejecuta sin tu aprobación.** Si dudas de una tarjeta, descártala y
pregúntale al Asistente antes.

> Tip: pregúntale al Asistente "¿pauso este anuncio?" o "¿subo el presupuesto?"
> y te da la recomendación antes de que apruebes.

---

## 5. Generar creativos (anuncios)

1. Enciende el motor: en terminal corre
   `python3 motor_creativos/creativos_server.py`
   (déjalo abierto mientras generas).
2. En el dashboard ve a la sección **Creativos**.
3. Elige fotos de tu **biblioteca** y los ángulos que quieras (inversión, retiro,
   laguna, etc.).
4. Dale a **generar**: la app crea los anuncios 1080×1920 con tu marca (azul,
   tipografía premium, logo, precio, CTA).
5. Los anuncios terminados quedan guardados en `motor_creativos/salidas/`.

---

## 6. Instalar / subir un anuncio a Meta

1. Elige el creativo que más te gusta de los generados.
2. Descárgalo desde la sección Creativos (o tómalo de `motor_creativos/salidas/`).
3. Súbelo tú mismo en el Administrador de Anuncios de Meta, dentro de tu campaña
   de Leads.
4. **La app no publica anuncios sola en tu cuenta**: tú controlas qué entra y
   cuándo. Así no hay sorpresas con el presupuesto.

---

## 7. Reportes para el cliente

1. Abre la sección **Reportes**.
2. Verás un informe limpio: KPIs con su variación, mejores anuncios, desglose por
   país, tendencia del CPL y un resumen ejecutivo.
3. Usa el botón **Imprimir / PDF** para guardarlo o enviarlo al cliente.

---

## 8. Preguntas frecuentes

- **¿La app puede gastar mi dinero sola?** No. Solo ejecuta lo que apruebas en la
  Bandeja.
- **¿Y si cierro la ventana negra (Terminal)?** No pasa nada: el copiloto sigue
  corriendo. Para apagarlo de verdad usa `detener.command`.
- **¿Los números no cargan?** Enciende el copiloto (paso 2) y recarga el dashboard.
- **¿Rompí algo editando?** Hay copias de respaldo `dashboard.backup-*.html`.
  Renombra la más reciente a `dashboard.html` y listo.
- **¿Dónde está mi token?** Guardado y protegido. No lo copies ni lo pegues en
  ningún lado.
