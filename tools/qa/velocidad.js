// Velocidad en celular con 4G lento (como Lighthouse): hijo (A) vs copia (B). Mediana de 3 cargas.
//   A=... B=... node tools/qa/velocidad.js
const { chromium } = require('playwright-core');

const EXE = process.env.CHROME ||
  '/Users/juanescorcha/Library/Caches/ms-playwright/chromium-1247/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing';
const URLS = { hijo: process.env.A || 'https://www.playablancaresidences.com/panama/', copia: process.env.B || 'https://landing-panama-nueva.vercel.app/' };
const BLOQUEAR = /facebook\.(com|net)|clarity\.ms|hs-scripts|hs-analytics|hsforms|hubspot|hs-banner|hscollectedforms/;

async function medir(browser, url) {
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true });
  const page = await ctx.newPage();
  await page.route('**/*', r => (BLOQUEAR.test(r.request().url()) ? r.abort() : r.continue()));
  const cdp = await ctx.newCDPSession(page);
  await cdp.send('Network.enable');
  await cdp.send('Network.setCacheDisabled', { cacheDisabled: true });
  await cdp.send('Network.emulateNetworkConditions', { offline: false, latency: 150, downloadThroughput: 1.6 * 1024 * 1024 / 8, uploadThroughput: 750 * 1024 / 8 });
  await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });
  let bytes = 0;
  cdp.on('Network.loadingFinished', e => { bytes += e.encodedDataLength; });
  await page.addInitScript(() => {
    window.__lcp = 0;
    new PerformanceObserver(l => { for (const e of l.getEntries()) window.__lcp = e.startTime; }).observe({ type: 'largest-contentful-paint', buffered: true });
  });
  const t0 = Date.now();
  await page.goto(url + '?v=' + Math.random(), { waitUntil: 'load', timeout: 120000 });
  const carga = Date.now() - t0;
  await page.waitForTimeout(1500);
  const m = await page.evaluate(() => ({
    lcp: Math.round(window.__lcp),
    fcp: Math.round((performance.getEntriesByName('first-contentful-paint')[0] || {}).startTime || 0),
  }));
  await ctx.close();
  return { ...m, carga, kb: Math.round(bytes / 1024) };
}

const mediana = a => a.slice().sort((x, y) => x - y)[Math.floor(a.length / 2)];

(async () => {
  const browser = await chromium.launch({ executablePath: EXE, headless: true });
  for (const [nombre, url] of Object.entries(URLS)) {
    const r = [];
    for (let i = 0; i < (+process.env.N || 3); i++) r.push(await medir(browser, url));
    console.log(`${nombre.padEnd(6)} LCP ${mediana(r.map(x => x.lcp))} ms · FCP ${mediana(r.map(x => x.fcp))} ms · carga ${mediana(r.map(x => x.carga))} ms · descarga ${mediana(r.map(x => x.kb))} KB`);
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
