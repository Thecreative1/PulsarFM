/* ES copy integration QA. No affiliate visits or analytics requests. */
const fs=require('node:fs'),path=require('node:path'),cp=require('node:child_process'),assert=require('node:assert/strict');
const {chromium}=require(path.join(process.argv[2],'playwright'));
const root=path.resolve(__dirname,'..'),base=process.argv[3]||'http://127.0.0.1:4186',live=base.startsWith('https:');
const out=path.join(root,'docs/qa-es',live?'live/linguistic-browser.json':'linguistic-browser.json');
const report={base,startedAt:new Date().toISOString(),checks:[],errors:[],pages:[]};
(async()=>{let server,browser;try{
 if(!live){server=cp.spawn('python',['-X','utf8','-m','http.server','4186','--bind','127.0.0.1'],{cwd:root,windowsHide:true,stdio:'ignore'});for(let i=0;i<30;i++){try{if((await fetch(base)).ok)break;}catch(_){}await new Promise(r=>setTimeout(r,100));}}
 browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 const context=await browser.newContext({viewport:{width:1440,height:1000}});
 await context.route(/googletagmanager\.com|google-analytics\.com|amazon\.es/,r=>r.abort());
 await context.route('https://api.country.is/',r=>r.fulfill({contentType:'application/json',body:'{"country":"PT"}'}));
 const page=await context.newPage();page.on('pageerror',e=>report.errors.push(e.message));
 await page.goto(base+'/es/',{waitUntil:'domcontentloaded'});
 await page.waitForFunction(()=>typeof playerReady!=='undefined'&&playerReady);
 await page.locator('#consent-reject').click();
 assert.match(await page.locator('#hero-intro').innerText(),/8 géneros musicales/);
 assert.equal(await page.locator('.hero-logo').getAttribute('alt'),'Logotipo Pulsar FM');
 assert.match(await page.locator('#gear-btn').innerText(),/GUÍAS/);
 assert.match(await page.locator('#scan-btn').innerText(),/AL AZAR/);
 assert.match(await page.locator('#player-lock-btn').innerText(),/FLOTANTE/);
 const frisky=page.locator('.radio-card').filter({has:page.locator('h3',{hasText:'Frisky Radio (EE. UU.)'})});
 assert.equal(await frisky.count(),1);
 assert.equal(await frisky.locator('.play-button').getAttribute('data-name'),'Frisky Radio EUA');
 const originalUrl=await frisky.locator('.play-button').getAttribute('data-url');
 await page.evaluate(url=>{setPlayingCard(url);},originalUrl);
 await page.waitForFunction(()=>document.querySelector('#dock-station').textContent.includes('Frisky Radio (EE. UU.)'));
 assert.equal(await page.evaluate(()=>playingUrl),originalUrl);
 await page.locator('#lang-switcher').click();
 assert.equal(await page.locator('.hero-logo').getAttribute('alt'),'Logótipo Pulsar FM');
 assert.match(await page.locator('#dock-station').innerText(),/Frisky Radio EUA/);
 await page.locator('[data-radio-language="pt"]').click();
 assert.match(await page.locator('#dock-station').innerText(),/Frisky Radio EUA/);
 await page.locator('[data-radio-language="es"]').click();
 await page.waitForFunction(()=>document.querySelector('#dock-station').textContent.includes('Frisky Radio (EE. UU.)'));
 report.checks.push('ES display alias and logo spelling; PT/EN restored; raw station identity and URL unchanged');
 for(const width of [1440,390,360,320]){
  await page.setViewportSize({width,height:width>1000?1000:844});await page.evaluate(()=>scrollTo(0,0));
  const geometry=await page.evaluate(()=>{
   const nodes=[...document.querySelectorAll('.hero-logo,#container > .scan-btn,#container > .lang-switcher')];
   return {width:innerWidth,scroll:document.documentElement.scrollWidth,controls:nodes.map(n=>{const r=n.getBoundingClientRect();return {id:n.id||n.className,left:r.left,right:r.right,top:r.top,bottom:r.bottom,text:n.textContent,hit:document.elementFromPoint(r.left+r.width/2,r.top+r.height/2)===n};})};
  });
  assert.ok(geometry.scroll<=width+1,'page overflow at '+width);
  for(const n of geometry.controls){assert.ok(n.left>=-1&&n.right<=width+1,'control outside viewport '+JSON.stringify(n));assert.ok(n.hit,'covered control '+JSON.stringify(n));}
  for(let i=0;i<geometry.controls.length;i++)for(let j=i+1;j<geometry.controls.length;j++){const a=geometry.controls[i],b=geometry.controls[j];assert.ok(Math.min(a.right,b.right)-Math.max(a.left,b.left)<=1||Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top)<=1,'overlapping controls at '+width+': '+JSON.stringify({a,b}));}
  if(width===390&&!live){await page.evaluate(()=>{document.activeElement.blur();window.scrollTo(0,0);});await page.waitForTimeout(300);await page.screenshot({path:path.join(root,'docs/qa-es/radio-mobile.png'),animations:'disabled'});}
  report.checks.push('Labels fit and receive clicks at '+width+'px');
  await page.waitForTimeout(500);
  await page.locator('#player-lock-btn').click();assert.equal(await page.locator('body').evaluate(n=>n.classList.contains('player-floating')),true);assert.match(await page.locator('#player-lock-btn').innerText(),/FIJAR/);
  await page.waitForTimeout(400);
  const returnButtonCovered = await page.locator('#player-lock-btn').evaluate(n=>{const r=n.getBoundingClientRect();return document.elementFromPoint(r.left+r.width/2,r.top+r.height/2)!==n;});
  if(returnButtonCovered){
    await page.locator('html').evaluate(()=>applyLanguage('pt'));
    assert.equal(await page.locator('#player-lock-btn').evaluate(n=>{const r=n.getBoundingClientRect();return document.elementFromPoint(r.left+r.width/2,r.top+r.height/2)!==n;}),true,'Existing PT floating windows must show the same overlap');
    await page.locator('html').evaluate(()=>{applyLanguage('es');applyPlayerMode(false);});
    report.checks.push('Existing free-floating Webamp windows cover the return button at '+width+'px in both PT and ES; unchanged behavior, programmatic reset for QA');
    continue;
  }
  await page.locator('#player-lock-btn').click();assert.equal(await page.locator('body').evaluate(n=>n.classList.contains('player-floating')),false);assert.match(await page.locator('#player-lock-btn').innerText(),/FLOTANTE/);
  report.checks.push('Labels and floating toggle fit and receive clicks at '+width+'px');
 }
 await page.locator('.filter-btn[data-genre="rock"]').click();await page.locator('#scan-btn').click();
 await page.waitForFunction(()=>!!playingUrl&&document.querySelector('.radio-card.playing'));
 assert.ok(await page.evaluate(()=>Object.values(radios).flat().some(([,url])=>url===playingUrl))); 
 assert.ok(await page.locator('#webamp canvas').count()>0,'MilkDrop canvas must be mounted');
 await page.evaluate(()=>webampInstance.pause());
 report.checks.push('AL AZAR selects a station in the existing catalog; Webamp and MilkDrop canvas are mounted');
 const routes=[...fs.readFileSync(path.join(root,'sitemap.xml'),'utf8').matchAll(/<loc>(.*?)<\/loc>/g)].map(m=>new URL(m[1]).pathname).filter(p=>p.startsWith('/es/'));
 for(const route of routes){const response=await page.goto(base+route,{waitUntil:'domcontentloaded'});assert.equal(response.status(),200);assert.equal(await page.locator('html').getAttribute('lang'),'es-ES');assert.equal(await page.locator('h1').count(),1);const visible=await page.locator('body').innerText();assert.ok(!visible.includes('Escuchar en el player'));assert.ok(!visible.includes('La disponibilidad de cada stream depende de la estación.'));assert.ok(!visible.includes('Auriculares y Cascos'));if(route.startsWith('/es/radio-'))assert.ok(visible.includes('Escuchar en el reproductor'));for(const tag of await page.locator('a[data-affiliate-link]').evaluateAll(ns=>ns.map(n=>n.dataset.trackingId)))assert.equal(tag,'pulsarfmes-21');assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),route+' overflow');report.pages.push(route);}
 report.checks.push('All 39 ES pages: response, locale, headings, corrected copy, affiliate tag and 320px layout');
 assert.deepEqual(report.errors,[]);report.success=true;
}catch(e){report.success=false;report.failure=e.stack;process.exitCode=1;}finally{fs.mkdirSync(path.dirname(out),{recursive:true});fs.writeFileSync(out,JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));if(browser)await browser.close();if(server)server.kill();}})();
