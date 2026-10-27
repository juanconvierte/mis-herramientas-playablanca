// Navegación y medición fina de la copia (sin mandar nada real):
// tarjetas de proyecto, logo, "Llamar", preguntas frecuentes, barra fija del celular, gracias directa/tras lead.
//   node tools/qa/extras.js      (servidor local en 4173)
const { chromium } = require('playwright-core');

const EXE = process.env.CHROME ||
  '/Users/juanescorcha/Library/Caches/ms-playwright/chromium-1247/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing';
const URL = process.env.NUEVA || 'http://localhost:4173/';
const SALIDAS = /api\.hsforms\.com|faro-five-chi\.vercel\.app|\/api\/conversion|facebook\.(com|net)|clarity\.ms|hs-scripts\.com|hubspot/;
const ESPIA = `(() => { let real; Object.defineProperty(window, 'fbq', { configurable: true, get() { return real; },
  set(v) { const o = v; real = function () { (window.__fb = window.__fb || []).push([].slice.call(arguments)); return o.apply(this, arguments); }; Object.assign(real, o); real.queue = o.queue; } }); })();`;

async function nuevo(browser, movil) {
  const ctx = await browser.newContext(movil ? { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true } : { viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();
  await page.addInitScript(ESPIA);
  await page.route('**/*', r => {
    const u = r.request().url();
    if (!SALIDAS.test(u)) return r.continue();
    if (/hsforms|faro|conversion/.test(u)) return r.fulfill({ status: 200, body: '{}' });
    return r.abort();
  });
  const errores = [];
  page.on('pageerror', e => errores.push(e.message));
  return { ctx, page, errores };
}
const eventos = page => page.evaluate(() => (window.__fb || []).map(a => a[0] + ':' + a[1] + (a[2] && a[2].content_name ? '(' + a[2].content_name + ')' : '')));

(async () => {
  const browser = await chromium.launch({ executablePath: EXE, headless: true });
  const res = {};

  // Escritorio: tarjeta de proyecto, logo, Llamar, FAQ
  let { ctx, page, errores } = await nuevo(browser, false);
  await page.goto(URL, { waitUntil: 'networkidle' });
  await page.locator('#proyectos').scrollIntoViewIfNeeded();
  await page.locator('.proy').first().click();
  await page.waitForTimeout(1200);
  res.tarjeta_lleva_al_form = await page.evaluate(() => { const r = document.getElementById('contacto').getBoundingClientRect(); return r.top < 200 && r.bottom > 0; });
  await page.locator('a.nav-tel').evaluate(a => a.addEventListener('click', e => e.preventDefault()));
  await page.click('a.nav-tel');
  await page.locator('#preguntas').scrollIntoViewIfNeeded();
  await page.locator('.faq-item summary').first().click();
  await page.waitForTimeout(300);
  await page.locator('#nav a[aria-label]').click();
  await page.waitForTimeout(1200);
  res.logo_se_queda = page.url().startsWith(URL) && await page.evaluate(() => window.scrollY < 50);
  res.eventos_escritorio = await eventos(page);
  res.errores_escritorio = errores;
  await ctx.close();

  // Celular: barra fija (se esconde con el formulario a la vista)
  ({ ctx, page, errores } = await nuevo(browser, true));
  await page.goto(URL, { waitUntil: 'networkidle' });
  await page.evaluate(() => window.scrollTo(0, 1200));
  await page.waitForTimeout(600);
  const barra = () => page.evaluate(() => { const b = document.querySelector('.mobile-sticky-cta'); return b ? getComputedStyle(b).transform : 'no-existe'; });
  res.barra_fuera_del_form = await barra();
  await page.locator('#contacto').scrollIntoViewIfNeeded();
  await page.waitForTimeout(600);
  res.barra_con_form_visible = await barra();
  res.errores_celular = errores;
  await ctx.close();

  // /gracias directo (sin lead): no debe contar CompleteRegistration
  ({ ctx, page, errores } = await nuevo(browser, false));
  await page.goto(URL + 'gracias', { waitUntil: 'networkidle' });
  res.gracias_directo_eventos = await eventos(page);
  res.gracias_volver = await page.locator('a.btn-outline').getAttribute('href');
  // tras un lead: WhatsApp personalizado + CR una sola vez
  await page.evaluate(() => { localStorage.setItem('pb_lead_name', 'Ana Pérez'); localStorage.setItem('pb_lead_objetivo', 'Retiro'); localStorage.setItem('pb_lead_rango', '$250K - $350K'); });
  await page.reload({ waitUntil: 'networkidle' });
  res.gracias_tras_lead_eventos = await eventos(page);
  res.whatsapp_personalizado = decodeURIComponent(await page.locator('#waBtn').getAttribute('href'));
  await page.locator('#waBtn').evaluate(a => a.addEventListener('click', e => e.preventDefault()));
  await page.click('#waBtn');
  res.gracias_tras_click = await eventos(page);
  await page.reload({ waitUntil: 'networkidle' });
  res.gracias_recarga_no_repite_CR = !(await eventos(page)).some(e => e.includes('CompleteRegistration'));
  res.errores_gracias = errores;
  await ctx.close();

  console.log(JSON.stringify(res, null, 1));
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
