import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
const root = path.dirname(new URL(import.meta.url).pathname);
const pages = fs.readdirSync(root).filter(f => f.endsWith('.html'));
for (const name of pages) {
 const html=fs.readFileSync(path.join(root,name),'utf8');
 assert.equal((html.match(/<h1[ >]/g)||[]).length,1,name+' h1');
 assert(html.includes('<html lang="en">'),name+' lang');
 assert.equal((html.match(/rel="canonical"/g)||[]).length,1,name+' canonical');
 assert(html.includes('name="description"'),name+' description');
 assert(!/aggregateRating|application\/ld\+json.*"offers"/.test(html),name+' truthful prelaunch schema');
 for(const j of html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)) JSON.parse(j[1]);
 for(const m of html.matchAll(/(?:src|href|poster)="([^"#]+)(?:#[^"]*)?"/g)) {
  const ref=m[1].split('#')[0]; if(/^(https?:|mailto:)/.test(ref))continue;
  assert(fs.existsSync(path.resolve(root,ref)),name+' missing '+ref);
 }
 for(const m of html.matchAll(/<img\b([^>]+)>/g)) assert(/\balt=/.test(m[1]),name+' image alt');
 assert(!/<script[^>]+src="https?:/.test(html),name+' no external scripts');
}
const release=JSON.parse(fs.readFileSync(path.join(root,'release.json'),'utf8'));
assert.equal(release.priceUSD,'2.99');assert.equal(release.saleEnabled,false);assert.equal(release.checkoutURL,null);
console.log(JSON.stringify({pages:pages.length,checks:'metadata, local links, image alt, structured data, no remote scripts, prelaunch price',passed:true}));
