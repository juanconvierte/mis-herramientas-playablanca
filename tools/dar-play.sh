#!/bin/bash
# DAR PLAY — pone la landing nueva en panama.playablancaresidences.com.
# Correr SOLO con el OK de Juan:   bash tools/dar-play.sh
#
# Qué hace: copia 4 cosas a web-panama-LIVE (index.html, gracias.html, estilo.css, images/),
# las commitea SOLAS (nunca git add -A: ese repo tiene trabajo sin terminar de otra sesión)
# y hace git push -> Vercel despliega. El dominio, las APIs, los robots de WhatsApp,
# la privacidad, los correos y vercel.json NO se tocan.
# Volver atrás: git -C ../web-panama-LIVE revert --no-edit <commit que imprime al final> && git push origin main
set -euo pipefail

NUEVA="$(cd "$(dirname "$0")/.." && pwd)"
LIVE="$(cd "$NUEVA/../web-panama-LIVE" && pwd)"
ARCHIVOS=(index.html gracias.html estilo.css images)

echo "1/6 Revisando que la copia esté completa..."
for f in index.html gracias.html estilo.css images/hero-lagoon.webp; do
  [ -e "$NUEVA/$f" ] || { echo "FALTA $f en web-panama-NUEVA. Parar."; exit 1; }
done
python3 -c "
import sys
for f in ['index.html', 'gracias.html']:
    h = open('$NUEVA/' + f, encoding='utf-8').read()
    assert h.count('<section') == h.count('</section>'), f + ': secciones descuadradas'
    assert '</html>' in h, f + ': HTML cortado'
    assert '2195180334399669' in h, f + ': falta el pixel'
h = open('$NUEVA/index.html', encoding='utf-8').read()
for x in ['api.hsforms.com', 'faro-five-chi.vercel.app/api/publico/entrada', '/api/conversion', \"'/gracias'\", 'PB_PRUEBA']:
    assert x in h, 'index.html: falta ' + x
print('   OK')
"

echo "2/6 Revisando que web-panama-LIVE esté al día con GitHub..."
cd "$LIVE"
git fetch -q origin
[ "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)" ] || { echo "LIVE no coincide con GitHub (otra sesión desplegó o hay commits sin subir). Parar y coordinar."; exit 1; }
if ! git diff --quiet -- index.html gracias.html || ! git diff --cached --quiet; then
  echo "index.html/gracias.html tienen cambios sin guardar o hay algo en stage de otra sesión. Parar y coordinar."; exit 1
fi
[ ! -e estilo.css ] || git ls-files --error-unmatch estilo.css >/dev/null 2>&1 || { echo "Hay un estilo.css suelto en LIVE que no es nuestro. Parar."; exit 1; }

echo "3/6 Copiando la landing nueva..."
cp "$NUEVA/index.html" index.html
cp "$NUEVA/gracias.html" gracias.html
cp "$NUEVA/estilo.css" estilo.css
mkdir -p images
rsync -a --delete --exclude '.manifiesto.json' "$NUEVA/images/" images/

echo "4/6 Revisando que no viaje ningún secreto..."
if grep -nE "EAA[A-Za-z0-9]{20,}|pat-na1-|sk_live|ralph-ceo|DASH_KEY|CRM_KEY|META_ACCESS_TOKEN|HUBSPOT_TOKEN" index.html gracias.html estilo.css; then
  echo "Posible secreto en los archivos. Parar."; git checkout -- index.html gracias.html; exit 1
fi

echo "5/6 Guardando y publicando (solo esas 4 rutas)..."
git add -- "${ARCHIVOS[@]}"
git commit -q -m "Landing Panamá: diseño nuevo (espejo de playablancaresidences.com/panama) con el funcionamiento de siempre" -- "${ARCHIVOS[@]}"
COMMIT="$(git rev-parse --short HEAD)"
git push -q origin main
echo "   commit $COMMIT subido. Vercel despliega en ~1 min."

echo "6/6 Esperando el despliegue..."
for i in $(seq 1 30); do
  sleep 10
  if curl -s "https://panama.playablancaresidences.com/?nocache=$RANDOM" | grep -q 'estilo.css?v='; then
    echo "   EN VIVO."
    for p in / /gracias /privacidad /emails /logo-white.png /robots.txt; do
      printf '   %s %s\n' "$(curl -s -o /dev/null -w '%{http_code}' "https://panama.playablancaresidences.com$p")" "$p"
    done
    printf '   %s /api/conversion (GET debe dar 405)\n' "$(curl -s -o /dev/null -w '%{http_code}' https://panama.playablancaresidences.com/api/conversion)"
    echo "Volver atrás: git -C \"$LIVE\" revert --no-edit $COMMIT && git -C \"$LIVE\" push origin main"
    exit 0
  fi
done
echo "Todavía no se ve en vivo tras 5 min: revisar el deploy en Vercel (proyecto landing-panama)."
