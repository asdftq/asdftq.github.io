import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
const root = path.dirname(new URL(import.meta.url).pathname);
const pages = fs.readdirSync(root).filter(f => f.endsWith('.html'));
const release=JSON.parse(fs.readFileSync(path.join(root,'release.json'),'utf8'));
const schemas=[];
for (const name of pages) {
 const html=fs.readFileSync(path.join(root,name),'utf8');
 assert.equal((html.match(/<h1[ >]/g)||[]).length,1,name+' h1');
 assert(html.includes('<html lang="en">'),name+' lang');
 assert.equal((html.match(/rel="canonical"/g)||[]).length,1,name+' canonical');
 assert(html.includes('name="description"'),name+' description');
 assert(!/aggregateRating/.test(html),name+' no invented ratings');
 for(const j of html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)) schemas.push(JSON.parse(j[1]));
 for(const m of html.matchAll(/(?:src|href|poster)="([^"#]+)(?:#[^"]*)?"/g)) {
  const ref=m[1].split(/[?#]/)[0]; if(/^(https?:|mailto:)/.test(ref))continue;
  assert(fs.existsSync(ref.startsWith("/") ? path.resolve(root,"..",`.${ref}`) : path.resolve(root,ref)),name+' missing '+ref);
 }
 for(const m of html.matchAll(/<img\b([^>]+)>/g)) assert(/\balt=/.test(m[1]),name+' image alt');
 assert(!/<script[^>]+src="https?:/.test(html),name+' no external scripts');
}
assert.equal(release.priceUSD,'2.99');
const app=schemas.find(s=>s['@type']==='SoftwareApplication');
assert(app,'SoftwareApplication metadata');
assert.equal(app.softwareVersion,release.appVersion,'metadata matches release');
const landing=fs.readFileSync(path.join(root,'index.html'),'utf8');
const purchaseLinks=[...landing.matchAll(/<a\b[^>]*\bdata-purchase-link\b[^>]*href="([^"]+)"/g)].map(m=>m[1]);
if(release.saleEnabled){
 assert.equal(release.status,'released');
 const checkout=new URL(release.checkoutURL);
 assert.equal(checkout.origin,'https://asdftq.lemonsqueezy.com');
 assert(/^\/checkout\/buy\/[0-9a-f-]+$/.test(checkout.pathname));
 assert(purchaseLinks.length>=2,'primary and pricing purchase paths');
 for(const href of purchaseLinks)assert.equal(href,release.checkoutURL);
 assert.equal(app.offers?.url,release.checkoutURL);
 assert.equal(app.offers?.price,release.priceUSD);
 assert.equal(app.offers?.priceCurrency,'USD');
 assert.equal(app.offers?.availability,'https://schema.org/InStock');
 assert(!/planned|in development|not available to purchase|purchases are not open/i.test(landing),'current sales copy');
 const support=fs.readFileSync(path.join(root,'support.html'),'utf8');
 assert(support.includes('id="refunds"')&&support.includes('14 days'),'refund help');
}else{
 assert.equal(release.checkoutURL,null);
 assert.equal(purchaseLinks.length,0);
 assert(!app.offers,'no inactive product offers');
}
console.log(JSON.stringify({pages:pages.length,checks:'metadata, local links, image alt, schema, no remote scripts, price and release consistency',saleEnabled:release.saleEnabled,passed:true}));
