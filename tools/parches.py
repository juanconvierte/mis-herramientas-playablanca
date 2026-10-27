"""
Todo lo que se le cambia a la página del hijo, en un solo lugar.
Regla: el DISEÑO no se toca. Solo rutas, velocidad y el funcionamiento probado de
web-panama-LIVE (medición, formulario, CAPI). Única excepción visible: el enlace
"Política de privacidad" en la letra pequeña del pie (la landing actual lo tiene; ley 81 / Meta / Clarity).

SEO: el canonical, og:url y JSON-LD se dejan como los puso el hijo (apuntan a su página),
para no competir en Google con la web del cliente. Esta es una página de anuncios.

Formato de cada parche: (nombre, texto_exacto_del_hijo, reemplazo, veces)
  veces = número exacto de apariciones esperadas, o None = al menos una.
"""

PIXEL = '2195180334399669'

# Copias de prueba (este proyecto en Vercel, vistas previas de landing-panama y localhost): se ven igual,
# pero NO mandan datos ni miden nada. En panama.playablancaresidences.com todo funciona normal.
# landing-panama-git-main-… sirve producción: queda fuera a propósito.
MODO_PRUEBA = """<script>
  window.PB_PRUEBA = /^landing-panama-(nueva|git-(?!main-)|[a-z0-9]{9}-)/.test(location.hostname) || location.hostname === 'localhost';
  if (window.PB_PRUEBA) { window.fbq = function(){}; window.fbq.loaded = true; }
</script>"""


def landing(version_css):
    return [
        # ---- rutas: el hijo vive en /panama/ y saca las fotos de ../images/; aquí todo vive en la raíz
        ('fotos a la raíz', '../images/', '/images/', None),
        ('hoja de estilos con versión + modo prueba',
         '<link rel="stylesheet" href="estilo.css">',
         '<link rel="stylesheet" href="/estilo.css?v=%s">\n'
         '<style>picture{display:contents}picture>source{display:none}</style>\n%s' % (version_css, MODO_PRUEBA), 1),

        # ---- formulario: al enviar va a la página de gracias de este sitio
        ('redirect a gracias', "window.location.href = 'gracias/';", "window.location.href = '/gracias';", 1),

        # ---- única diferencia visible: privacidad en la letra pequeña del pie (estilo .pie-legal a del propio hijo)
        ('política de privacidad en el pie',
         'se garantizan rendimientos ni retornos de inversión.\n    </p>',
         'se garantizan rendimientos ni retornos de inversión.\n      <a href="/privacidad" style="white-space:nowrap">Política de privacidad</a>.\n    </p>', 1),
    ] + funcionamiento()


AJUSTES_FIN = """<script>
  /* ============ FUNCIONAMIENTO DE LA LANDING ORIGINAL (web-panama-LIVE) ============ */
  (function(){
    // Mensajes de error visibles: el diseño trae los espacios vacíos; se llenan al marcar el campo en rojo.
    var MSG = { contact_name: 'Ingrese su nombre completo', phone: 'Ingrese un número válido', email: 'Ingrese un email válido' };
    Object.keys(MSG).forEach(function(id){
      var campo = document.getElementById(id);
      var err = document.getElementById('error_' + (id === 'contact_name' ? 'name' : id));
      if (!campo || !err || typeof MutationObserver === 'undefined') return;
      new MutationObserver(function(){ err.textContent = campo.classList.contains('error') ? MSG[id] : ''; })
        .observe(campo, { attributes: true, attributeFilter: ['class'] });
    });

    // Tarjetas de proyectos: en la landing original llevan al formulario (también con teclado).
    var contacto = document.getElementById('contacto');
    function irAlForm(){
      if (!contacto) return;
      try { contacto.scrollIntoView({ behavior: 'smooth', block: 'start' }); } catch(_) { location.hash = '#contacto'; }
    }
    document.querySelectorAll('.proy').forEach(function(card){
      card.style.cursor = 'pointer';
      card.setAttribute('tabindex', '0');
      card.setAttribute('role', 'link');
      card.addEventListener('click', irAlForm);
      card.addEventListener('keydown', function(e){
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); card.click(); }
      });
    });

    // Llamadas: quien toca "Llamar" sale del formulario; queda medido como evento propio
    // (no "Contact": ese nombre ya significa "el asesor contactó al lead" en la escalera de Meta).
    document.querySelectorAll('a[href^="tel:"]').forEach(function(a){
      a.addEventListener('click', function(){
        try { if (typeof fbq === 'function') fbq('trackCustom', 'ClickToCall', { source: 'landing_panama' }); } catch(_) {}
      });
    });
  })();
</script>
</body>"""


def funcionamiento():
    """Piezas de web-panama-LIVE que la página del hijo no trae o trae rotas. Ninguna cambia el diseño."""
    return [
        # el logo lleva arriba de la misma página (en el hijo saca al visitante a otra web)
        ('logo se queda en la landing',
         '<a href="https://playablancaresidences.com/" aria-label="Playa Blanca Residences">',
         '<a href="#top" aria-label="Playa Blanca Residences">', 1),
        # pixel sin JavaScript, como en la landing original
        ('pixel noscript', '<body>',
         '<body>\n<noscript><img height="1" width="1" style="display:none" alt="" '
         'src="https://www.facebook.com/tr?id=%s&ev=PageView&noscript=1"></noscript>' % PIXEL, 1),
        # Clarity y HubSpot no corren en las copias de prueba (HubSpot captura formularios por su cuenta)
        ('Clarity fuera de las copias de prueba', '(function(c,l,a,r,i,t,y){',
         'if (!window.PB_PRUEBA) (function(c,l,a,r,i,t,y){', 1),
        ('HubSpot fuera de las copias de prueba',
         '<script type="text/javascript" id="hs-script-loader" async defer src="//js.hs-scripts.com/6874300.js"></script>',
         '<script>if (!window.PB_PRUEBA) { (function(){ var s = document.createElement(\'script\'); s.id = \'hs-script-loader\';'
         ' s.async = true; s.defer = true; s.src = \'https://js.hs-scripts.com/6874300.js\'; document.body.appendChild(s); })(); }</script>', 1),
        # envío: en copias de prueba se recorre todo el flujo hasta /gracias pero no sale ningún dato
        ('Lead del pixel', "        if (typeof fbq === 'function') {\n          try {\n            fbq('track', 'Lead', {",
         "        if (typeof fbq === 'function' && !window.PB_PRUEBA) {\n          try {\n            fbq('track', 'Lead', {", 1),
        ('envío HubSpot + Faro + CAPI',
         '        var hsPromise = sendToHubSpot(payload);\n        sendToFaro(payload);\n        sendCAPI(payload, eventId);',
         '        var hsPromise = window.PB_PRUEBA ? Promise.resolve() : sendToHubSpot(payload);\n'
         '        if (!window.PB_PRUEBA) { sendToFaro(payload); sendCAPI(payload, eventId); }', 1),
        ('reenvío de respaldo', 'if (!sent && payload) {', 'if (!sent && payload && !window.PB_PRUEBA) {', 1),
        ('PageView CAPI', 'if (window.__pbPvSent) return;', 'if (window.PB_PRUEBA || window.__pbPvSent) return;', 1),
        # arreglos de la página del hijo
        ('el form se acomoda en pantalla al cambiar de paso', "form.closest('.form-card')", "form.closest('.form-caja')", 1),
        ('texto del botón si falla el envío', "'Recibir disponibilidad y precios →'", "'Solicitar información'", 1),
        ('clic en tarjetas de proyecto cuenta como CTA',
         'a[href="#contacto"], .btn-primary, .btn-navy, .nav-cta', 'a[href="#contacto"], .btn-primary, .btn-navy, .nav-cta, .proy', 1),
        ('ajustes al final', '</body>', AJUSTES_FIN, 1),
    ]


# ------------------------------------------------------------------ gracias
GRACIAS_HEAD = """<script>
  !function(f,b,e,v,n,t,s)
  {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
  n.callMethod.apply(n,arguments):n.queue.push(arguments)};
  if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
  n.queue=[];t=b.createElement(e);t.async=!0;
  t.src=v;s=b.getElementsByTagName(e)[0];
  s.parentNode.insertBefore(t,s)}(window, document,'script',
  'https://connect.facebook.net/en_US/fbevents.js');
  (function(){ var x = null; try { x = localStorage.getItem('pb_xid'); } catch(e){}
    fbq('init', '%(pixel)s', x ? { external_id: x } : {}); })();
  fbq('track', 'PageView');
  /* CompleteRegistration: una sola vez por lead real (candado pb_cr_fired, mismo scope que pb_lead_name). */
  (function() {
    try {
      var hasLead = localStorage.getItem('pb_lead_name');
      var alreadyFired = localStorage.getItem('pb_cr_fired');
      if (hasLead && !alreadyFired) {
        localStorage.setItem('pb_cr_fired', '1');
        fbq('track', 'CompleteRegistration', {
          content_name: 'Lead Panama Landing',
          status: true,
          content_category: localStorage.getItem('pb_lead_objetivo') || 'Sin especificar'
        });
      }
    } catch(e) {}
  })();
</script>
</head>""" % {'pixel': PIXEL}

GRACIAS_BODY_FIN = """<noscript><img height="1" width="1" style="display:none" alt="" src="https://www.facebook.com/tr?id=%(pixel)s&ev=PageView&noscript=1"></noscript>
<script>
  /* WhatsApp con los datos del lead + limpieza (CR ya disparó arriba). Igual que gracias.html de web-panama-LIVE. */
  (function() {
    function lg(k){ try { return localStorage.getItem(k) || ''; } catch(_) { return ''; } }
    var leadName = lg('pb_lead_name'), leadObjetivo = lg('pb_lead_objetivo'), leadRango = lg('pb_lead_rango');
    var waBtn = document.getElementById('waBtn');
    if (waBtn && (leadName || leadObjetivo)) {
      var waText = 'Hola, soy ' + (leadName || 'un interesado') + '. Acabo de solicitar información sobre Playa Blanca';
      if (leadObjetivo) waText += ' para ' + leadObjetivo.toLowerCase();
      if (leadRango) waText += ' en el rango de ' + leadRango;
      waText += '. Quedo atento.';
      waBtn.href = 'https://wa.me/50767558003?text=' + encodeURIComponent(waText);
    }
    try {
      ['pb_lead_name','pb_lead_objetivo','pb_lead_rango','pb_lead_tipo','pb_lead_phone','pb_cr_fired']
        .forEach(function(k){ localStorage.removeItem(k); });
    } catch(_) {}
    if (waBtn) waBtn.addEventListener('click', function() {
      if (typeof fbq === 'function') fbq('track', 'Contact', { content_name: 'WhatsApp Post-Lead', source: 'thank_you_page' });
    });
  })();
  (function() {
    var start = Date.now(), f30 = false, f60 = false;
    setInterval(function() {
      var s = (Date.now() - start) / 1000;
      if (s >= 30 && !f30) { f30 = true; if (typeof fbq === 'function') fbq('trackCustom', 'TYPageEngaged30s'); }
      if (s >= 60 && !f60) { f60 = true; if (typeof fbq === 'function') fbq('trackCustom', 'TYPageEngaged60s'); }
    }, 5000);
  })();
</script>
</body>""" % {'pixel': PIXEL}


def gracias(version_css):
    return [
        ('icono', '<link rel="icon" href="../../images/palmera.png">', '<link rel="icon" href="/images/palmera.png">', 1),
        ('hoja de estilos', '<link rel="stylesheet" href="../estilo.css">',
         '<link rel="stylesheet" href="/estilo.css?v=%s">' % version_css, 1),
        ('volver al inicio', 'href="../"', 'href="/"', 1),
        ('id del botón WhatsApp', '<a class="btn btn-gold" href="https://wa.me/',
         '<a id="waBtn" class="btn btn-gold" href="https://wa.me/', 1),
        ('modo prueba + pixel + CompleteRegistration', '</head>', MODO_PRUEBA + '\n' + GRACIAS_HEAD, 1),
        ('WhatsApp personalizado + Contact + tiempo en página', '</body>', GRACIAS_BODY_FIN, 1),
    ]


# ------------------------------------------------------------------ fotos
# Recortes para celular: misma foto, mismos píxeles visibles, la mitad de peso.
# El hero cubre la pantalla (object-fit: cover, centrado); en un celular vertical
# (proporción <= 9:16) solo se ve el centro. Un recorte centrado de 1000 px de ancho
# a la misma altura se escala igual (manda la altura) -> se ve idéntico.
RECORTES_MOVIL = {
    'hero-lagoon.jpg': {'ancho': 1000, 'media': '(max-aspect-ratio: 9/16)'},
}
