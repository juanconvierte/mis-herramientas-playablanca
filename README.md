# web-panama-NUEVA

Landing Panamá con el **diseño del hijo** (www.playablancaresidences.com/panama/) y el **funcionamiento de web-panama-LIVE** (HubSpot, Faro, CAPI, pixel, medición).

- Copia de prueba: https://landing-panama-nueva.vercel.app — se ve igual, pero **no manda datos** (modo prueba).
- Actualizar desde la página del hijo: `python3 -E tools/sincronizar.py` (todo lo que se cambia está en `tools/parches.py`).
- Probar local: `python3 -E tools/servidor_local.py` y `node tools/qa/comparar.js` / `node tools/qa/formulario.js`.
- **Dar play** (solo con OK de Juan): `bash tools/dar-play.sh` → copia index, gracias, estilo.css e images/ a web-panama-LIVE y hace push. El dominio y las APIs no se mueven.
