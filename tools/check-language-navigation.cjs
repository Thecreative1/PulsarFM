/* Navigation regression matrix. Country replies are intercepted; no visitor IP is sent by these cases. */
const fs=require('node:fs'), path=require('node:path'), cp=require('node:child_process'), assert=require('node:assert/strict');
const {chromium}=require(path.join(process.argv[2],'playwright'));
const root=path.resolve(__dirname,'..');
const base=process.argv[3]||'http://127.0.0.1:4185';
const live=base.startsWith('https:');
const out=path.join(root,'docs/qa-es',live?'live/language-navigation.json':'language-navigation.json');
const report={base,startedAt:new Date().toISOString(),cases:[],errors:[],countryRequestsMocked:true};
const cases=[
 {name:'fresh-Spain',route:'/',country:'ES',lang:'es',market:'es',requests:1},
 {name:'fresh-Portugal',route:'/',country:'PT',lang:'pt',market:'pt',requests:1},
 {name:'fresh-other-country',route:'/',country:'FR',lang:'pt',market:'pt',requests:1},
 {name:'country-service-error',route:'/',status:503,lang:'pt',market:'pt',requests:1},
 {name:'country-network-failure',route:'/',abort:true,lang:'pt',market:'pt',requests:1},
 {name:'country-invalid-response',route:'/',raw:'broken-json',lang:'pt',market:'pt',requests:1},
 {name:'country-unknown',route:'/',country:'ZZ',lang:'pt',market:'pt',requests:1},
 {name:'country-timeout',route:'/',delay:2500,country:'ES',lang:'pt',market:'pt',requests:1},
 {name:'explicit-PT-wins-Spain',route:'/?lang=pt',country:'ES',lang:'pt',market:'pt',requests:0},
 {name:'explicit-ES-wins-Portugal',route:'/?lang=es',country:'PT',lang:'es',market:'es',requests:0},
 {name:'explicit-EN',route:'/?lang=en',country:'ES',lang:'en',market:'pt',requests:0},
 {name:'Spanish-URL-wins-stored-PT',route:'/es/',saved:'pt',country:'PT',lang:'es',market:'es',requests:0},
 {name:'Spanish-URL-explicit-EN',route:'/es/?lang=en',country:'ES',lang:'en',market:'es',requests:0},
 {name:'Spanish-URL-explicit-PT',route:'/es/?lang=pt',country:'ES',lang:'pt',market:'pt',requests:0},
 {name:'stored-ES-wins-root',route:'/',saved:'es',country:'PT',lang:'es',market:'es',requests:0},
 {name:'stored-PT-wins-Spain',route:'/',saved:'pt',country:'ES',lang:'pt',market:'pt',requests:0},
 {name:'stored-EN-Spanish-market',route:'/',saved:'en',savedMarket:'es',country:'ES',lang:'en',market:'es',requests:0},
 {name:'invalid-preference-detects-country',route:'/',saved:'invalid',country:'ES',lang:'es',market:'es',requests:1},
 {name:'blocked-storage-keeps-navigation',route:'/',blockedStorage:true,country:'ES',lang:'es',market:'es',requests:1},
 {name:'manual-choice-wins-late-Spain',route:'/',hold:true,country:'ES',lang:'pt',market:'pt',requests:1}
];
(async()=>{
 let browser,server;
 try{
  if(!live){server=cp.spawn('python',['-X','utf8','-m','http.server','4185','--bind','127.0.0.1'],{cwd:root,windowsHide:true,stdio:'ignore'});for(let i=0;i<30;i++){try{if((await fetch(base)).ok)break;}catch(_){}await new Promise(r=>setTimeout(r,100));}}
  browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
  for(const width of [1440,390]){
   for(const c of cases){
    const ctx=await browser.newContext({viewport:{width,height:width===390?844:1000},locale:'es-ES',timezoneId:'Europe/Madrid'});
    await ctx.route(/googletagmanager\.com|google-analytics\.com|amazon\.es/,r=>r.abort());
    let requests=0,release;
    const gate=new Promise(resolve=>{release=resolve;});
    await ctx.route('https://api.country.is/',async r=>{
      requests++;
      if(c.hold)await gate;
      if(c.delay)await new Promise(resolve=>setTimeout(resolve,c.delay));
      if(c.abort)return r.abort();
      try{await r.fulfill({status:c.status||200,contentType:'application/json',body:c.raw||JSON.stringify({country:c.country})});}catch(_){}
    });
    await ctx.addInitScript(({saved,savedMarket,blockedStorage})=>{
      if(blockedStorage){Storage.prototype.getItem=()=>{throw new DOMException('blocked','SecurityError')};Storage.prototype.setItem=()=>{throw new DOMException('blocked','SecurityError')};}
      else {localStorage.setItem('pulsarfm-consent','denied');if(saved)localStorage.setItem('pulsarfm-lang',saved);if(savedMarket)localStorage.setItem('pulsarfm-market',savedMarket);}
    },c);
    const page=await ctx.newPage();page.on('pageerror',e=>report.errors.push(c.name+': '+e.message));
    await page.goto(base+c.route,{waitUntil:'domcontentloaded'});
    await page.waitForFunction(()=>typeof currentLang!=='undefined');
    if(c.hold){await page.locator('[data-radio-language="pt"]').click();release();}
    await page.evaluate(()=>window.PulsarRadioRegion.country);
    await page.waitForFunction(expected=>currentLang===expected,c.lang);
    const state=await page.evaluate(()=>({lang:document.documentElement.lang,market:marketLanguage,path:location.pathname,query:location.search,button:document.getElementById('lang-switcher').textContent,gear:new URL(document.getElementById('gear-btn').href).pathname,canonical:document.querySelector('link[rel="canonical"]').href,cards:document.querySelectorAll('.radio-card').length,width:innerWidth,scroll:document.documentElement.scrollWidth}));
    assert.equal(state.lang,c.lang==='pt'?'pt-PT':c.lang==='es'?'es-ES':'en',c.name);
    assert.equal(state.market,c.market,c.name);
    assert.equal(state.path,c.lang==='es'?'/es/':'/',c.name);
    assert.equal(state.button,c.lang==='en'?c.market.toUpperCase():'EN',c.name);
    assert.equal(state.gear,c.market==='es'?'/es/recomendaciones/':'/recomendacoes/',c.name);
    assert.equal(state.canonical,'https://pulsarfm.eu'+(c.lang==='es'?'/es/':'/'),c.name);
    assert.equal(state.cards,64);assert.ok(state.scroll<=state.width+1);assert.equal(requests,c.requests,c.name);
    if(c.lang==='en')assert.equal(new URL(page.url()).searchParams.get('lang'),'en');
    if(c.name==='fresh-Spain'){
      await page.waitForFunction(()=>playerReady,{timeout:30000});
      await page.evaluate(()=>{window.__originalPlayer=webampInstance;});
      await page.locator('.filter-btn[data-genre="rock"]').click();
      await page.locator('#lang-switcher').click();
      assert.equal(await page.locator('#lang-switcher').textContent(),'ES');
      assert.equal(await page.locator('#gear-btn').getAttribute('href'),'/es/recomendaciones/');
      await page.reload({waitUntil:'domcontentloaded'});
      await page.waitForFunction(()=>typeof currentLang!=='undefined');
      assert.equal(await page.locator('html').getAttribute('lang'),'en');assert.equal(await page.locator('#lang-switcher').textContent(),'ES');
      await page.waitForFunction(()=>playerReady,{timeout:30000});
      await page.evaluate(()=>{window.__originalPlayer=webampInstance;});
      await page.locator('#lang-switcher').click();
      assert.equal(new URL(page.url()).pathname,'/es/');assert.equal(new URL(page.url()).searchParams.get('genre'),'rock');
      await page.goBack({waitUntil:'domcontentloaded'});assert.equal(await page.locator('html').getAttribute('lang'),'en');assert.equal(await page.locator('#lang-switcher').textContent(),'ES');
      await page.goForward({waitUntil:'domcontentloaded'});assert.equal(await page.locator('html').getAttribute('lang'),'es-ES');
      assert.equal(await page.evaluate(()=>webampInstance===window.__originalPlayer),true);
      await page.locator('[data-radio-language="pt"]').click();assert.equal(await page.locator('html').getAttribute('lang'),'pt-PT');
      await page.locator('#lang-switcher').click();assert.equal(await page.locator('#lang-switcher').textContent(),'PT');
      await page.locator('#lang-switcher').click();assert.equal(await page.locator('html').getAttribute('lang'),'pt-PT');
      await page.locator('[data-radio-language="es"]').click();
      await page.locator('#lang-switcher').click();
      const genreHref=await page.locator('.genre-filter-link[data-genre="rock"]').first().getAttribute('href');
      assert.ok(genreHref.includes('return_lang=es'));
      await page.goto(new URL(genreHref,base).href,{waitUntil:'domcontentloaded'});
      await page.locator('.home-cta').click();
      await page.waitForFunction(()=>typeof currentLang!=='undefined');
      assert.equal(await page.locator('html').getAttribute('lang'),'en');assert.equal(await page.locator('#lang-switcher').textContent(),'ES');
      await page.locator('#lang-switcher').click();
      assert.equal(await page.locator('html').getAttribute('lang'),'es-ES');
      const gearHref=await page.locator('#gear-btn').getAttribute('href');
      await page.goto(base+gearHref,{waitUntil:'domcontentloaded'});assert.equal(await page.locator('html').getAttribute('lang'),'es-ES');
      await page.locator('.brand').click();await page.waitForFunction(()=>typeof currentLang!=='undefined');assert.equal(await page.locator('html').getAttribute('lang'),'es-ES');
      report.cases.push({name:'ES-EN-ES-reload-history-genre-guides',width,passed:true});
    }
    if(c.blockedStorage){await page.locator('#consent-reject').click();await page.locator('#lang-switcher').click();assert.equal(await page.locator('#lang-switcher').textContent(),'ES');await page.locator('#lang-switcher').click();assert.equal(await page.locator('html').getAttribute('lang'),'es-ES');}
    report.cases.push({name:c.name,width,passed:true,requests});console.log('PASS '+width+' '+c.name);
    await ctx.close();
   }
  }
  // One real CORS request verifies provider availability; never log the returned IP.
  const probe=await browser.newContext();const page=await probe.newPage();
  await probe.route(/googletagmanager\.com|google-analytics\.com/,r=>r.abort());
  await page.goto(base+'/?lang=pt',{waitUntil:'domcontentloaded'});
  report.provider=await page.evaluate(async()=>{try{const r=await fetch('https://api.country.is/',{credentials:'omit',referrerPolicy:'no-referrer',signal:AbortSignal.timeout(2000)});const d=await r.json();return {status:r.status,corsReadable:r.ok,countryCodeValid:/^[A-Z]{2}$/.test(d.country)};}catch(e){return {corsReadable:false,error:e.message};}});
  assert.equal(report.provider.corsReadable,true,'Provider CORS availability');
  assert.equal(report.provider.countryCodeValid,true);
  assert.deepEqual(report.errors,[]);report.success=true;
 }catch(e){report.success=false;report.failure=e.stack;process.exitCode=1;}
 finally{report.finishedAt=new Date().toISOString();fs.mkdirSync(path.dirname(out),{recursive:true});fs.writeFileSync(out,JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({success:report.success,cases:report.cases.length,provider:report.provider,errors:report.errors,failure:report.failure},null,2));if(browser)await browser.close();if(server)server.kill();}
})();
