/* Local browser QA; no affiliate requests or real GA4 events are sent. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const cp = require('node:child_process');
// Use a project-installed Playwright or a NODE_PATH supplied by the local runtime.
const { chromium } = require(process.argv[2] ? path.join(process.argv[2], 'playwright') : 'playwright');
const root = path.resolve(__dirname, '..');
const base = 'http://127.0.0.1:4184';
const evidence = path.join(root, 'docs/qa-es');
fs.mkdirSync(evidence, { recursive: true });
(async () => {
  const server = cp.spawn('python', ['-X', 'utf8', '-m', 'http.server', '4184', '--bind', '127.0.0.1'], { cwd: root, windowsHide: true, stdio: 'ignore' });
  let browser;
  const results = { errors: [], screenshots: [], checks: [] };
  try {
    for (let i=0; i<30; i++) {
      try { const r = await fetch(base + '/'); if(r.ok) break; } catch(_) {}
      await new Promise(resolve => setTimeout(resolve,100));
    }
    browser = await chromium.launch({ headless: true, executablePath: process.env.PULSAR_CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
    const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
    await context.route(/googletagmanager\.com|google-analytics\.com|amazon\.es/, route => route.abort());
    const page = await context.newPage();
    page.on('pageerror', error => results.errors.push(error.message));
    const expectLayout = async (label) => {
      const geometry = await page.evaluate(() => ({ width: innerWidth, scroll: document.documentElement.scrollWidth }));
      assert.ok(geometry.scroll <= geometry.width + 1, label + ' overflows viewport: ' + JSON.stringify(geometry));
      results.checks.push(label + ': no horizontal page overflow');
    };
    const screenshot = async (name) => {
      await page.screenshot({path: path.join(evidence,name+'.png'), fullPage: false, animations:'disabled', timeout:10000});
      results.screenshots.push('docs/qa-es/'+name+'.png');
    };
    await page.goto(base+'/es/',{waitUntil:'domcontentloaded'});
    await page.waitForFunction(() => typeof playerReady !== 'undefined' && playerReady, {timeout:30000});
    assert.equal(await page.locator('.radio-card').count(),64);
    assert.equal(await page.locator('html').getAttribute('lang'),'es-ES');
    await page.evaluate(() => { window.__playerBeforeLanguage = webampInstance; });
    await page.locator('#consent-reject').click();
    await expectLayout('Spanish radio desktop');
    await screenshot('radio-desktop');
    await page.locator('[data-radio-language="pt"]').click();
    assert.equal(new URL(page.url()).pathname,'/');
    assert.equal(await page.locator('html').getAttribute('lang'),'pt-PT');
    await page.locator('[data-radio-language="es"]').click();
    assert.equal(new URL(page.url()).pathname,'/es/');
    assert.equal(await page.evaluate(() => webampInstance === window.__playerBeforeLanguage),true);
    await page.locator('.filter-btn[data-genre="rock"]').click();
    assert.equal(new URL(page.url()).searchParams.get('genre'),'rock');
    assert.equal(new URL(page.url()).pathname,'/es/');
    await page.reload({waitUntil:'domcontentloaded'});
    await page.waitForFunction(() => typeof playerReady !== 'undefined' && playerReady, {timeout:30000});
    assert.equal(await page.locator('html').getAttribute('lang'),'es-ES');
    assert.equal(await page.evaluate(() => localStorage.getItem('pulsarfm-lang')),'es');
    assert.equal(await page.locator('.radio-group:not([hidden])').count(),1);
    results.checks.push('PT/ES selection, persistence, filtered URLs and unchanged Webamp instance');
    await page.locator('#lang-switcher').click();
    assert.equal(new URL(page.url()).searchParams.get('lang'),'en');
    assert.equal(await page.locator('html').getAttribute('lang'),'en');
    await page.locator('[data-radio-language="es"]').click();
    assert.equal(new URL(page.url()).pathname,'/es/');
    results.checks.push('Existing EN button works from the Spanish locale');
    // Request a real existing station once, never change the stream catalog.
    await page.locator('.radio-group[data-genre="rock"] .play-button').first().click();
    await page.waitForFunction(() => !!playingUrl && document.querySelector('.radio-card.playing'), {timeout:10000});
    results.checks.push('Radio station selection reaches the existing player');
    results.radioState = await page.evaluate(() => ({station:document.querySelector('.radio-card.playing h3')?.textContent, url:playingUrl, playerReady}));
    results.audioCheck = await page.evaluate(async () => {
      const audio = new Audio(playingUrl);
      audio.crossOrigin = 'anonymous';
      audio.muted = true;
      try {
        await audio.play();
        const deadline = Date.now() + 12000;
        while (audio.currentTime < 0.1 && Date.now() < deadline) await new Promise(resolve => setTimeout(resolve,100));
        return { decoded: audio.currentTime >= 0.1, currentTime: audio.currentTime, readyState: audio.readyState };
      } catch (error) { return { decoded: false, error: error.message }; }
      finally { audio.pause(); audio.removeAttribute('src'); audio.load(); }
    });
    assert.equal(results.audioCheck.decoded,true,'The sample existing station must decode and advance');
    results.checks.push('Existing Radio Paradise stream decodes in Chrome with CORS and advancing playback time');
    await page.evaluate(() => webampInstance.pause());
    await page.setViewportSize({width:390,height:844});
    await expectLayout('Spanish radio mobile');
    await page.locator('.filter-btn[data-genre="all"]').click();
    await page.evaluate(() => scrollTo(0,0));
    await screenshot('radio-mobile');
    for (const [width,label] of [[1440,'desktop'],[390,'mobile']]) {
      await page.setViewportSize({width,height:width===390?844:1000});
      await page.goto(base+'/es/recomendaciones/',{waitUntil:'domcontentloaded'});
      assert.equal(await page.locator('.guide-nav li').count(),7);
      assert.equal(await page.locator('.guides-index .guide-link').count(),8);
      await expectLayout('Spanish hub '+label);
      await screenshot('hub-'+label);
      await page.goto(base+'/es/recomendaciones/tocadiscos-para-empezar/',{waitUntil:'domcontentloaded'});
      await expectLayout('Spanish article '+label);
      await screenshot('article-'+label);
      assert.equal(await page.locator('.product-recommendation').count(),2);
      assert.equal(await page.locator('a[data-affiliate-link]').first().getAttribute('data-tracking-id'),'pulsarfmes-21');
    }
    // Capture events locally; do not open affiliate links or send to GA4.
    await page.locator('[data-consent-settings]').click();
    await page.locator('[data-consent-choice="granted"]').click();
    const before = await page.evaluate(() => (window.dataLayer||[]).filter(e=>e[0]==='event'&&e[1]==='affiliate_click').length);
    await page.evaluate(() => document.querySelector('a[data-affiliate-link]').dispatchEvent(new MouseEvent('click',{bubbles:true,button:0,cancelable:true})));
    const after = await page.evaluate(() => (window.dataLayer||[]).filter(e=>e[0]==='event'&&e[1]==='affiliate_click').map(e=>e[2]));
    assert.equal(after.length,before+1);
    assert.equal(after.at(-1).market,'ES');
    await page.locator('[data-consent-settings]').click();
    await page.locator('[data-consent-choice="denied"]').click();
    await page.evaluate(() => document.querySelector('a[data-affiliate-link]').dispatchEvent(new MouseEvent('click',{bubbles:true,button:0,cancelable:true})));
    assert.equal(await page.evaluate(() => (window.dataLayer||[]).filter(e=>e[0]==='event'&&e[1]==='affiliate_click').length),after.length);
    results.checks.push('Browser consent: single ES affiliate event on accept; none on revoke');
    const nojs = await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});
    const crawler = await nojs.newPage();
    for(const route of ['/es/','/es/recomendaciones/','/es/recomendaciones/tocadiscos-para-empezar/','/es/radio-jazz/','/es/privacidad/']) {
      const response = await crawler.goto(base+route,{waitUntil:'domcontentloaded'});
      assert.equal(response.status(),200);
      assert.equal(await crawler.locator('html').getAttribute('lang'),'es-ES');
      assert.ok((await crawler.locator('h1').textContent()).length>10);
    }
    results.checks.push('5 key Spanish routes return localized content without JavaScript');
    for (const route of ['/','/privacidade.html','/radios-rock/','/en/rock-radio/','/recomendacoes/','/recomendacoes/melhores-auscultadores/']) {
      const response = await page.goto(base+route,{waitUntil:'domcontentloaded'});
      assert.equal(response.status(),200);
    }
    results.checks.push('6 representative legacy PT/EN URLs remain reachable');
    await page.goto(base+'/?lang=pt',{waitUntil:'domcontentloaded'});
    await page.locator('[data-radio-language="es"]').click();
    assert.equal(new URL(page.url()).pathname,'/es/');
    assert.equal(await page.evaluate(() => new URL('skins/base-2.91.wsz',document.baseURI).pathname),'/skins/base-2.91.wsz');
    const skinResponse = await page.request.get(base+'/skins/base-2.91.wsz');
    assert.equal(skinResponse.status(),200);
    results.checks.push('Root-to-ES navigation preserves original skin and player asset URLs');
    assert.deepEqual(results.errors,[]);
    results.success=true;
  } catch(error) {
    results.success=false;
    results.failure=error.stack;
    throw error;
  } finally {
    fs.writeFileSync(path.join(evidence,'browser-results.json'),JSON.stringify(results,null,2)+'\n');
    console.log(JSON.stringify(results,null,2));
    if(browser) await browser.close();
    server.kill();
  }
})().catch(()=>{process.exitCode=1;});
