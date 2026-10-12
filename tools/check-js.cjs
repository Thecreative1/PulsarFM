/* Syntax lint for external JS and every inline script in the static site. */
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
let checked = 0;
function walk(dir) {
  for (const entry of fs.readdirSync(dir,{withFileTypes:true})) {
    if(['.git','.pytest_cache','__pycache__','node_modules'].includes(entry.name)) continue;
    const filename=path.join(dir,entry.name);
    if(entry.isDirectory()) { walk(filename); continue; }
    if(entry.name.endsWith('.js') && dir===path.join(root,'assets')) {
      new vm.Script(fs.readFileSync(filename,'utf8'),{filename}); checked++;
    }
    if(entry.name.endsWith('.html') && !filename.includes(path.sep+'templates'+path.sep)) {
      for(const [i,match] of [...fs.readFileSync(filename,'utf8').matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/g)].entries()) {
        if(/\bsrc=/.test(match[1])||/application\/ld\+json/.test(match[1])) continue;
        new vm.Script(match[2],{filename:filename+':inline-'+i}); checked++;
      }
    }
  }
}
walk(root);
console.log('JavaScript syntax lint passed: '+checked+' scripts');
