/* Production smoke test: read-only requests. Amazon and GA4 requests are blocked. */
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const { chromium } = require(process.argv[2] ? path.join(process.argv[2], 'playwright') : 'playwright');
const root = path.resolve(__dirname,'..');
const base = 'https://pulsarfm.eu';
const marker = process.argv[3] || String(Date.now());
const evidence = path.join(root,'docs','qa-es','live');
const results = { startedAt:new Date().toISOString(),base,release:marker,pages:[],assets:[],checks:[],errors:[] };
fs.mkdirSync(evidence,{recursive:true});
const hash = text => crypto.createHash('sha256').update(text.replace(/\r\n/g,'\n')).digest('hex');
const liveUrl = route => {const url=new URL(route,base);url.searchParams.set('smoke',marker);return url.href;};
const fileFor = route => path.join(root,route.replace(/^\//,'')+(route.endsWith('/')?'index.html':''));
async function verifyFile(route,kind) {
  const response=await fetch(liveUrl(route),{signal:AbortSignal.timeout(20000),headers:{'Cache-Control':'no-cache'}});
  const text=await response.text();
  const expected=fs.readFileSync(fileFor(route),'utf8');
  const item={route,status:response.status,cacheControl:response.headers.get('cache-control'),matchesLocal:hash(text)===hash(expected)};
  results[kind].push(item);
  assert.equal(response.status,200,route+' must return 200');
  assert.equal(item.matchesLocal,true,route+' has not reached the published version');
}
async function batch(items,kind) {
  for(let i=0;i<items.length;i+=4) await Promise.all(items.slice(i,i+4).map(route=>verifyFile(route,kind)));
}
(async()=>{
 let browser;
 try {
  const routes=[...fs.readFileSync(path.join(root,'sitemap.xml'),'utf8').matchAll(/<loc>(.*?)<\/loc>/g)].map(m=>new URL(m[1]).pathname);
  await batch(routes,'pages');
  await batch(['/assets/radio-es.css','/assets/radio-region.js','/assets/radio-locales.js','/assets/radio-i18n.js','/assets/site-language.js','/assets/affiliate-analytics.js','/assets/recommendations.css','/sitemap.xml','/robots.txt'],'assets');
  results.checks.push('All '+routes.length+' sitemap pages and 9 critical assets match the local release');
  browser=await chromium.launch({headless:true,executablePath:process.env.PULSAR_CHROME||'C:/Program Files/Google/Chrome/Application/chrome.exe'});
  const context=await browser.newContext({viewport:{width:1440,height:1000}});
  await context.route('https://api.country.is/', route => route.fulfill({status:200,contentType:'application/json',body:JSON.stringify({country:'PT'})}));
  await context.route(/googletagmanager\.com|google-analytics\.com|amazon\.es/,route=>route.abort());
  const page=await context.newPage();
  page.on('pageerror',error=>results.errors.push(error.message));
  async function checkLayout(label) {
    const dimensions=await page.evaluate(()=>({viewport:innerWidth,width:document.documentElement.scrollWidth}));
    assert.ok(dimensions.width<=dimensions.viewport+1,label+' overflows viewport');
    results.checks.push(label+': layout fits viewport');
  }
  await page.goto(liveUrl('/es/'),{waitUntil:'domcontentloaded'});
  await page.waitForFunction(()=>typeof playerReady!=='undefined'&&playerReady,{timeout:30000});
  assert.equal(await page.locator('.radio-card').count(),64);
  assert.equal(await page.locator('html').getAttribute('lang'),'es-ES');
  await page.locator('#consent-reject').click();
  await page.evaluate(()=>{window.__playerAtStart=webampInstance;});
  await page.locator('[data-radio-language="pt"]').click();
  assert.equal(new URL(page.url()).pathname,'/');
  await page.locator('[data-radio-language="es"]').click();
  assert.equal(new URL(page.url()).pathname,'/es/');
  assert.equal(await page.evaluate(()=>webampInstance===window.__playerAtStart),true);
  await page.locator('#lang-switcher').click();
  assert.equal(await page.locator('html').getAttribute('lang'),'en');
  await page.locator('[data-radio-language="es"]').click();
  await page.locator('.filter-btn[data-genre="rock"]').click();
  assert.equal(new URL(page.url()).searchParams.get('genre'),'rock');
  await page.reload({waitUntil:'domcontentloaded'});
  await page.waitForFunction(()=>typeof playerReady!=='undefined'&&playerReady,{timeout:30000});
  assert.equal(await page.evaluate(()=>localStorage.getItem('pulsarfm-lang')),'es');
  assert.equal(await page.locator('.radio-group:not([hidden])').count(),1);
  assert.equal(await page.evaluate(()=>new URL('skins/base-2.91.wsz',document.baseURI).pathname),'/skins/base-2.91.wsz');
  await page.locator('.radio-group[data-genre="rock"] .play-button').first().click();
  await page.waitForFunction(()=>!!playingUrl&&document.querySelector('.radio-card.playing'),{timeout:10000});
  results.audio=await page.evaluate(async()=>{
    const audio=new Audio(playingUrl);audio.crossOrigin='anonymous';audio.muted=true;
    try {
      await audio.play();const deadline=Date.now()+12000;
      while(audio.currentTime<0.1&&Date.now()<deadline)await new Promise(r=>setTimeout(r,100));
      return {decoded:audio.currentTime>=0.1,currentTime:audio.currentTime,readyState:audio.readyState,station:document.querySelector('.radio-card.playing h3')?.textContent};
    } catch(error){return {decoded:false,error:error.message};}
    finally{audio.pause();audio.removeAttribute('src');audio.load();}
  });
  await page.evaluate(()=>webampInstance.pause());
  assert.equal(results.audio.decoded,true,'Existing live stream must decode');
  results.checks.push('Live radio: Webamp ready, station selection and CORS audio decoding work');
  results.checks.push('PT/ES/EN, persistence, filter URLs and skin paths work without recreating Webamp');
  for(const [width,label] of [[1440,'desktop'],[390,'mobile']]){
    await page.setViewportSize({width,height:width===390?844:1000});
    await page.goto(liveUrl('/es/recomendaciones/'),{waitUntil:'domcontentloaded'});
    assert.equal(await page.locator('.guide-nav li').count(),13);
    assert.equal(await page.locator('#guias .guide-link').count(),13);
    await checkLayout('Spanish hub '+label);
    await page.screenshot({path:path.join(evidence,'hub-'+label+'.png'),animations:'disabled'});
      const primary = JSON.parse(fs.readFileSync(path.join(root,'data/recommendations.es.json'),'utf8')).articles.filter(a=>!a.secondary);
      for (const article of primary) {
        const route = '/es/recomendaciones/'+article.slug+'/';
        await page.locator('.guide-nav a[href="'+route+'"]').click();
        assert.equal(new URL(page.url()).pathname,route);
        assert.equal(await page.locator('.product-recommendation').count(),article.productIds.length);
        assert.equal(await page.locator('.guide-comparison tbody tr').count(),article.productIds.length);
        assert.equal(await page.locator('.quick-picks li').count(),article.quickPicks.length);
        assert.equal(await page.locator('.guide-nav [aria-current="page"]').getAttribute('href'),route);
        await checkLayout(article.navLabel+' '+label);
        const ptRoute = '/recomendacoes/'+article.ptSlug+'/';
        assert.equal(await page.locator('.locale-nav a[lang="pt-PT"]').getAttribute('href'),ptRoute);
      }
      results.checks.push('All 13 guide buttons navigate to complete Spanish content on '+label);

    await page.goto(liveUrl('/es/recomendaciones/auriculares-cancelacion-ruido-trabajar/'),{waitUntil:'domcontentloaded'});
    await checkLayout('Spanish article '+label);
    const commercial=await page.locator('a[data-affiliate-link]').evaluateAll(links=>links.map(a=>({tag:new URL(a.href).searchParams.get('tag'),market:a.dataset.market,rel:a.rel})));
    assert.ok(commercial.length>0);assert.ok(commercial.every(a=>a.tag==='pulsarfmes-21'&&a.market==='ES'&&a.rel.split(' ').includes('sponsored')));
    await page.screenshot({path:path.join(evidence,'article-'+label+'.png'),animations:'disabled'});
  }
  await page.locator('[data-consent-settings]').click();
  await page.locator('[data-consent-choice="granted"]').click();
  const countEvents=()=>page.evaluate(()=>(window.dataLayer||[]).filter(e=>e[0]==='event'&&e[1]==='affiliate_click').length);
  const before=await countEvents();
  const simulateClick=()=>page.evaluate(()=>{document.addEventListener('click',event=>event.preventDefault(),{once:true});document.querySelector('a[data-affiliate-link]').dispatchEvent(new MouseEvent('click',{bubbles:true,button:0,cancelable:true}));});
  await simulateClick();assert.equal(await countEvents(),before+1);
  const event=await page.evaluate(()=>(window.dataLayer||[]).filter(e=>e[0]==='event'&&e[1]==='affiliate_click').at(-1)[2]);
  assert.equal(event.market,'ES');assert.equal(event.tracking_id,'pulsarfmes-21');
  await page.locator('[data-consent-settings]').click();await page.locator('[data-consent-choice="denied"]').click();
  await simulateClick();assert.equal(await countEvents(),before+1);
  results.checks.push('Commercial URLs keep confirmed IDs and sponsored attributes; one queued event on consent, none after revocation');
  await page.goto(liveUrl('/recomendacoes/melhores-auscultadores/'),{waitUntil:'domcontentloaded'});
  assert.equal(await page.locator('a[data-affiliate-link]').first().getAttribute('data-tracking-id'),'pulsarfm-21');
  const nojs=await browser.newContext({javaScriptEnabled:false});const crawler=await nojs.newPage();
  for(const route of ['/es/','/es/recomendaciones/','/es/recomendaciones/tocadiscos-para-empezar/','/es/radio-jazz/','/es/privacidad/']){
    const response=await crawler.goto(liveUrl(route),{waitUntil:'domcontentloaded'});assert.equal(response.status(),200);
    assert.equal(await crawler.locator('html').getAttribute('lang'),'es-ES');assert.ok((await crawler.locator('h1').textContent()).length>10);
    assert.equal(await crawler.locator('link[rel="canonical"]').getAttribute('href'),base+route);
  }
  results.checks.push('Key Spanish routes render localized content and self canonical without JavaScript');
  const noCacheRoutes=['/','/es/','/es/recomendaciones/'];
  results.normalUrls=[];
  for(const route of noCacheRoutes){const response=await fetch(base+route,{signal:AbortSignal.timeout(20000)});const text=await response.text();const matchesLocal=hash(text)===hash(fs.readFileSync(fileFor(route),'utf8'));results.normalUrls.push({route,status:response.status,matchesLocal});assert.equal(response.status,200);assert.equal(matchesLocal,true,'Unversioned URL is stale: '+route);}
  assert.deepEqual(results.errors,[]);results.success=true;
 }catch(error){results.success=false;results.failure=error.stack;process.exitCode=1;}
 finally{results.finishedAt=new Date().toISOString();fs.writeFileSync(path.join(evidence,'smoke-results.json'),JSON.stringify(results,null,2)+'\n');console.log(JSON.stringify({success:results.success,pages:results.pages.length,assets:results.assets.length,checks:results.checks,audio:results.audio,normalUrls:results.normalUrls,errors:results.errors,failure:results.failure},null,2));if(browser)await browser.close();}
})();
