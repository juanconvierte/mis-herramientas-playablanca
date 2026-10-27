// Prueba el formulario de punta a punta SIN mandar nada real: HubSpot, Faro, CAPI y Meta quedan
// interceptados. Compara lo que manda la landing actual (LIVE) contra la copia (NUEVA).
//   node tools/qa/formulario.js      (con los dos servidores locales: 4173 nueva, 4174 LIVE)
const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const EXE = process.env.CHROME ||
  '/Users/juanescorcha/Library/Caches/ms-playwright/chromium-1247/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing';
const OUT = process.env.OUT || path.join(__dirname, 'salida');
const CASOS = [
  { nombre: 'LIVE', url: process.env.LIVE || 'http://127.0.0.1:4174/' },
  { nombre: 'NUEVA', url: process.env.NUEVA || 'http://127.0.0.1:4173/' },
  { nombre: 'NUEVA-modo-prueba', url: process.env.PRUEBA || 'http://landing-panama-nueva.localhost:4173/', prueba: true },
];
const SALIDAS = /api\.hsforms\.com|faro-five-chi\.vercel\.app|\/api\/conversion|facebook\.(com|net)|clarity\.ms|hs-scripts\.com|hs-analytics|hs-banner|hscollectedforms|hubspot\.com/;

// Registra cada llamada a fbq en sessionStorage (sobrevive al salto a /gracias)
const ESPIA_FBQ = `(() => {
  let real;
  const log = (a) => { try { const l = JSON.parse(sessionStorage.getItem('__qa_fbq') || '[]'); l.push({ en: location.pathname, args: a }); sessionStorage.setItem('__qa_fbq', JSON.stringify(l)); } catch (e) {} };
  Object.defineProperty(window, 'fbq', {
    configurable: true,
    get() { return real; },
    set(v) { const orig = v; real = function () { log([].slice.call(arguments)); return orig.apply(this, arguments); }; Object.assign(real, orig); real.queue = orig.queue; },
  });
})();`;

async function correr(browser, caso, movil) {
  const ctx = await browser.newContext(movil
    ? { viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true }
    : { viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();
  await page.addInitScript(ESPIA_FBQ);
  const salidas = [];
  const errores = [];
  page.on('pageerror', e => errores.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error' && !/ERR_FAILED|net::ERR/.test(m.text())) errores.push(m.text().slice(0, 200)); });
  await page.route('**/*', route => {
    const req = route.request();
    const u = req.url();
    if (!SALIDAS.test(u)) return route.continue();
    let cuerpo = req.postData();
    try { cuerpo = JSON.parse(cuerpo); } catch (_) {}
    salidas.push({ url: u.split('?')[0], metodo: req.method(), cuerpo });
    if (/api\.hsforms\.com|faro-five-chi|\/api\/conversion/.test(u)) {
      return route.fulfill({ status: 200, contentType: 'application/json', body: '{"ok":true}' });
    }
    return route.abort();
  });

  const r = { caso: caso.nombre + (movil ? ' (celular)' : ''), checks: {} };
  await page.goto(caso.url + '?utm_source=facebook&utm_medium=paid&utm_campaign=QA&utm_content=anuncio-qa&utm_term=t1&fbclid=QAfbclid123', { waitUntil: 'networkidle' });
  await page.waitForTimeout(600);

  // Chip del hero -> preselecciona el objetivo y baja al formulario
  const chip = page.locator('.hero-chip[data-hero-objetivo="Retiro"]');
  if (await chip.count()) {
    await chip.click();
    await page.waitForTimeout(900);
    r.checks.chip_preselecciona = await page.locator('#objetivo_inversion').inputValue() === 'Retiro';
  } else {
    await page.click('[data-field="objetivo_inversion"] [data-value="Retiro"]');
  }
  await page.click('[data-field="plazo_decision"] [data-value="Inmediato"]');
  await page.waitForTimeout(700);
  r.checks.paso2_auto = await page.locator('.form-step[data-step="2"]').evaluate(e => e.classList.contains('active'));
  await page.click('[data-field="rango_inversion"] [data-value="$250K - $350K"]');
  await page.selectOption('#tipo_propiedad', 'Apartamento 1-2 recámaras');
  await page.waitForTimeout(700);
  r.checks.paso3_auto = await page.locator('.form-step[data-step="3"]').evaluate(e => e.classList.contains('active'));

  // Enviar vacío -> errores
  await page.click('.form-submit');
  await page.waitForTimeout(300);
  r.checks.error_nombre_marcado = await page.locator('#contact_name').evaluate(e => e.classList.contains('error'));
  r.checks.error_nombre_texto = await page.locator('#error_name').evaluate(e => (getComputedStyle(e).display !== 'none' ? e.textContent.trim() : ''));
  r.checks.error_consentimiento = await page.locator('#error_consent').evaluate(e => getComputedStyle(e).display !== 'none');
  r.checks.sin_envio_con_errores = salidas.filter(s => /hsforms|faro/.test(s.url)).length === 0;

  await page.fill('#contact_name', 'Prueba Automatica QA');
  r.checks.error_se_limpia = await page.locator('#error_name').evaluate(e => e.textContent.trim() === '' || getComputedStyle(e).display === 'none');
  await page.fill('#phone', '6123 4567');
  await page.fill('#email', 'qa-automatica@example.com');
  await page.check('#consent_check');
  await Promise.all([
    page.waitForURL(/\/gracias/, { timeout: 8000 }).catch(() => null),
    page.click('.form-submit'),
  ]);
  await page.waitForTimeout(1500);
  r.checks.llego_a_gracias = /\/gracias/.test(page.url());
  r.checks.gracias_limpia_datos = await page.evaluate(() => !localStorage.getItem('pb_lead_name') && !localStorage.getItem('pb_lead_phone'));
  r.fbq = await page.evaluate(() => JSON.parse(sessionStorage.getItem('__qa_fbq') || '[]'));
  r.salidas = salidas;
  r.errores = errores;
  r.titulo_gracias = await page.title();
  await ctx.close();
  return r;
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ executablePath: EXE, headless: true });
  const todos = [];
  for (const caso of CASOS) {
    for (const movil of [false, true]) {
      const r = await correr(browser, caso, movil);
      todos.push(r);
      const tipos = r.salidas.map(s => s.url.replace(/^https?:\/\/[^/]+/, m => m.replace(/^https?:\/\//, '')).split('/').slice(0, 3).join('/'));
      console.log(`\n== ${r.caso}\n  checks: ${JSON.stringify(r.checks)}\n  salidas: ${JSON.stringify([...new Set(tipos)])}\n  fbq: ${r.fbq.map(f => f.en + ':' + f.args[0] + (f.args[1] && typeof f.args[1] === 'string' ? ' ' + f.args[1] : '')).join(' | ')}\n  errores: ${JSON.stringify(r.errores)}`);
    }
  }
  fs.writeFileSync(path.join(OUT, 'formulario.json'), JSON.stringify(todos, null, 1));
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
