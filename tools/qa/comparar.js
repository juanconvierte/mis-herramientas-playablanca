// Compara la página del hijo (A) contra la copia (B): capturas de página completa,
// texto visible, enlaces y campos del formulario, en escritorio y celular.
//   npm i playwright-core   (una vez, en cualquier carpeta; usar NODE_PATH si hace falta)
//   node tools/qa/comparar.js            -> tools/qa/salida/
// Variables: A, B (urls), ORIGINALES=1 (B usa los JPG originales del hijo -> comparación exacta)
const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const RAIZ = path.resolve(__dirname, '..', '..');
const EXE = process.env.CHROME ||
  '/Users/juanescorcha/Library/Caches/ms-playwright/chromium-1247/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing';
const A = process.env.A || 'https://www.playablancaresidences.com/panama/';
const B = process.env.B || 'http://localhost:4173/';
const OUT = process.env.OUT || path.join(__dirname, 'salida');
const ORIGINALES = process.env.ORIGINALES === '1';
// Nada de medición real durante las pruebas (no ensuciar el pixel, HubSpot, Clarity ni Faro)
const BLOQUEAR = /facebook\.(com|net)|clarity\.ms|hs-scripts|hs-analytics|hsforms|hubspot|hs-banner|hscollectedforms|faro-five-chi|\/api\/conversion/;

const VISTAS = [
  { nombre: 'escritorio', viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 },
  { nombre: 'movil', viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true },
];

function original(rel) {
  const base = path.join(RAIZ, '_fuente-hijo', 'images', rel);
  for (const ext of ['.jpg', '.jpeg', '.png']) {
    if (fs.existsSync(base + ext)) return { file: base + ext, type: ext === '.png' ? 'image/png' : 'image/jpeg' };
  }
  return null;
}

async function capturar(browser, url, vista, prefijo, esB) {
  const ctx = await browser.newContext({
    viewport: vista.viewport, deviceScaleFactor: vista.deviceScaleFactor,
    isMobile: !!vista.isMobile, hasTouch: !!vista.hasTouch,
    reducedMotion: 'reduce', locale: 'es-PA', timezoneId: 'America/Panama',
  });
  const page = await ctx.newPage();
  const errores = [];
  page.on('pageerror', e => errores.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errores.push('console: ' + m.text()); });
  const fallidas = [];
  page.on('requestfailed', r => { if (!BLOQUEAR.test(r.url())) fallidas.push(r.url() + ' ' + (r.failure() || {}).errorText); });
  page.on('response', r => { if (r.status() >= 400 && !BLOQUEAR.test(r.url())) fallidas.push(r.status() + ' ' + r.url()); });

  await page.route('**/*', route => {
    const u = route.request().url();
    if (BLOQUEAR.test(u)) return route.abort();
    if (esB && ORIGINALES) {
      const m = u.match(/\/images\/(.+?)\.(webp|jpe?g|png)(\?|$)/);
      if (m) {
        const o = original(m[1]);
        if (o) return route.fulfill({ status: 200, contentType: o.type, body: fs.readFileSync(o.file) });
      }
    }
    return route.continue();
  });

  await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  await page.evaluate(async () => {
    document.querySelectorAll('img[loading="lazy"]').forEach(i => { i.loading = 'eager'; });
    document.querySelectorAll('.reveal').forEach(e => e.classList.add('visible'));
    await document.fonts.ready;
    for (let y = 0; y < document.documentElement.scrollHeight; y += 500) {
      window.scrollTo(0, y);
      await new Promise(r => setTimeout(r, 40));
    }
    window.scrollTo(0, 0);
    await Promise.all([...document.images].map(i => (i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; }))));
    await Promise.all([...document.images].map(i => i.decode().catch(() => null)));  // que estén dibujadas, no solo bajadas
  });
  await page.waitForTimeout(1200);

  const datos = await page.evaluate(() => {
    const visibles = el => !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
    return {
      titulo: document.title,
      texto: document.body.innerText.replace(/\s+/g, ' ').trim(),
      enlaces: [...document.querySelectorAll('a')].map(a => a.getAttribute('href')),
      campos: [...document.querySelectorAll('input, select, textarea, button')].map(e => ({
        tag: e.tagName, type: e.type, name: e.name, id: e.id, value: e.tagName === 'SELECT' ? [...e.options].map(o => o.value).join('|') : (e.dataset.value || ''),
      })),
      opciones: [...document.querySelectorAll('[data-value]')].map(e => (e.closest('[data-field]') || {}).dataset?.field + '=' + e.dataset.value),
      imagenes: [...document.images].filter(visibles).map(i => ({ src: i.currentSrc.split('/').pop().split('?')[0], w: i.naturalWidth, h: i.naturalHeight, rw: Math.round(i.getBoundingClientRect().width), rh: Math.round(i.getBoundingClientRect().height) })),
      alto: document.documentElement.scrollHeight,
    };
  });
  await page.screenshot({ path: prefijo + '.png', fullPage: true });
  fs.writeFileSync(prefijo + '.json', JSON.stringify({ ...datos, errores, fallidas }, null, 1));
  await ctx.close();
  return datos;
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ executablePath: EXE, headless: true });
  for (const v of VISTAS) {
    const a = await capturar(browser, A, v, path.join(OUT, v.nombre + '-A'), false);
    const b = await capturar(browser, B, v, path.join(OUT, v.nombre + '-B'), true);
    console.log(`${v.nombre}: alto A=${a.alto} B=${b.alto} · texto igual=${a.texto === b.texto} · enlaces iguales=${JSON.stringify(a.enlaces) === JSON.stringify(b.enlaces)} · campos iguales=${JSON.stringify(a.campos) === JSON.stringify(b.campos)}`);
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
