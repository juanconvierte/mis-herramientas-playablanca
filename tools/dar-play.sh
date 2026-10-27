#!/bin/bash
# DAR PLAY — pone la landing nueva en panama.playablancaresidences.com.
# Correr SOLO con el OK de Juan:   bash tools/dar-play.sh
#
# Arma el cambio en una copia temporal sacada de GitHub (git worktree), nunca en la carpeta
# web-panama-LIVE (ahí hay trabajo sin terminar de otra sesión). Copia 4 cosas (index.html,
# gracias.html, estilo.css, images/), commitea SOLO eso y hace push a main -> Vercel despliega.
# El dominio, las APIs, los robots de WhatsApp, privacidad, correos y vercel.json NO se tocan.
# Si algo falla antes del push, no se publica nada. Volver atrás: tools/volver-atras.sh <commit>.
set -euo pipefail

NUEVA="$(cd "$(dirname "$0")/.." && pwd)"
LIVE="$(cd "${PLAY_LIVE_DIR:-$NUEVA/../web-panama-LIVE}" && pwd)"   # PLAY_LIVE_DIR solo para ensayos
DOMINIO="${PLAY_DOMINIO:-https://panama.playablancaresidences.com}"
# Versiones de la landing actual contra las que se armó y probó la copia (26-oct-2026).
# Si alguien cambió después el formulario de LIVE, se para: hay que volver a comparar.
BLOB_INDEX=23db7a5c9d45e4b923f9016a267b5d713e05a510
BLOB_GRACIAS=72fa2cb9a235c01c6ae923fa25ad0407cffce3d3

echo "1/6 Revisando la copia..."
python3 -E - "$NUEVA" <<'EOF'
import hashlib, os, re, sys
n = sys.argv[1]
for f in ['index.html', 'gracias.html']:
    h = open(os.path.join(n, f), encoding='utf-8').read()
    assert h.count('<section') == h.count('</section>'), f + ': secciones descuadradas'
    assert '</html>' in h, f + ': HTML cortado'
    assert '2195180334399669' in h, f + ': falta el pixel'
    for ruta, v in re.findall(r'"(/(?:images/[^"?]+|estilo\.css))\?v=([0-9a-f]+)"', h):
        dig = hashlib.sha256(open(os.path.join(n, ruta.lstrip('/')), 'rb').read()).hexdigest()
        assert dig.startswith(v), f + ': versión vieja de ' + ruta + ' (correr tools/sincronizar.py)'
h = open(os.path.join(n, 'index.html'), encoding='utf-8').read()
for x in ['api.hsforms.com', 'faro-five-chi.vercel.app/api/publico/entrada', "fetch('/api/conversion'", "'/gracias'"]:
    assert x in h, 'index.html: falta ' + x
m = re.search(r'window\.PB_PRUEBA = /(.+?)/\.test\(location\.hostname\)', h)
assert m, 'no encuentro el modo prueba'
rx = re.compile(m.group(1))
for host in ['panama.playablancaresidences.com', 'landing-panama.vercel.app', 'colombia.playablancaresidences.com',
             'landing-panama-git-main-juanconviertes-projects.vercel.app', 'landing-panama-juanconviertes-projects.vercel.app',
             'www.playablancaresidences.com']:
    assert not rx.search(host), 'el modo prueba apagaría los envíos en ' + host
assert rx.search('landing-panama-nueva.vercel.app'), 'el modo prueba no cubre la copia de prueba'
print('   OK')
EOF

echo "2/6 Revisando GitHub (proyecto landing-panama)..."
git -C "$LIVE" fetch -q origin
nuestra() { case "$(git -C "$LIVE" show "origin/main:$1" 2>/dev/null || true)" in *PB_PRUEBA*) return 0;; *) return 1;; esac; }  # sin tubería: pipefail
if [ "$(git -C "$LIVE" rev-parse origin/main:index.html)" != "$BLOB_INDEX" ] && ! nuestra index.html; then
  echo "La landing actual (index.html) cambió desde que se armó la copia. Parar: volver a comparar el formulario."; exit 1
fi
if [ "$(git -C "$LIVE" rev-parse origin/main:gracias.html)" != "$BLOB_GRACIAS" ] && ! nuestra gracias.html; then
  echo "gracias.html cambió desde que se armó la copia. Parar: volver a comparar."; exit 1
fi

echo "3/6 Armando el cambio en una copia temporal de GitHub..."
TMP="$(mktemp -d)/landing"
limpiar() { cd "$NUEVA"; git -C "$LIVE" worktree remove --force "$TMP" >/dev/null 2>&1 || rm -rf "$TMP"; git -C "$LIVE" worktree prune >/dev/null 2>&1 || true; }
trap limpiar EXIT
git -C "$LIVE" worktree add -q --detach "$TMP" origin/main
cd "$TMP"
cp "$NUEVA/index.html" index.html
cp "$NUEVA/gracias.html" gracias.html
cp "$NUEVA/estilo.css" estilo.css
mkdir -p images
rsync -a --delete --exclude '.manifiesto.json' "$NUEVA/images/" images/

echo "4/6 Revisando que no viaje ningún secreto..."
if grep -nE "EAA[A-Za-z0-9]{20,}|pat-na1-|sk_live|ralph-ceo|DASH_KEY|CRM_KEY|META_ACCESS_TOKEN|HUBSPOT_TOKEN" index.html gracias.html estilo.css; then
  echo "Posible secreto en los archivos. Parar (no se publicó nada)."; exit 1
fi

echo "5/6 Guardando y publicando (solo esas 4 rutas)..."
git add -- index.html gracias.html estilo.css images
if git diff --cached --quiet; then echo "   No hay cambios: la landing nueva ya está publicada."; exit 0; fi
git commit -q -m "Landing Panamá: diseño nuevo (espejo de playablancaresidences.com/panama) con el funcionamiento de siempre" -- index.html gracias.html estilo.css images
COMMIT="$(git rev-parse --short HEAD)"
if ! git push -q origin HEAD:main; then
  echo "GitHub rechazó el push (otra sesión publicó justo ahora). No se publicó nada: volver a correr el script."; exit 1
fi
echo "   commit $COMMIT subido. Vercel despliega en ~1 min."
cd "$NUEVA"
if [ "$(git -C "$LIVE" symbolic-ref --short HEAD 2>/dev/null || true)" = "main" ]; then
  git -C "$LIVE" merge -q --ff-only origin/main 2>/dev/null || echo "   (la carpeta web-panama-LIVE quedó atrás de GitHub: hacer git pull cuando toque)"
fi

echo "6/6 Esperando el despliegue..."
VCSS="$(grep -o -m1 'estilo\.css?v=[0-9a-f]*' "$NUEVA/index.html")"
for i in $(seq 1 30); do
  sleep 10
  H="$(curl -s --max-time 15 "$DOMINIO/?nocache=$RANDOM$i" || true)"
  case "$H" in
    *"$VCSS"*)
      echo "   EN VIVO."
      for p in / /gracias /privacidad /emails /logo-white.png /robots.txt; do
        printf '   %s %s\n' "$(curl -s --max-time 15 -o /dev/null -w '%{http_code}' "$DOMINIO$p" || echo ERR)" "$p"
      done
      printf '   %s /api/conversion (GET debe dar 405)\n' "$(curl -s --max-time 15 -o /dev/null -w '%{http_code}' "$DOMINIO/api/conversion" || echo ERR)"
      echo "Listo. Volver atrás: bash \"$NUEVA/tools/volver-atras.sh\" $COMMIT"
      exit 0;;
  esac
done
echo "El push salió (commit $COMMIT) pero tras 5 min aún no se ve en vivo: revisar el deploy en Vercel (proyecto landing-panama)."
exit 1
