import assert from "node:assert/strict";
import { readFileSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import vm from "node:vm";
const root = fileURLToPath(new URL("./", import.meta.url));
const context = { window: {} };
vm.runInNewContext(readFileSync(`${root}catalog.js`, "utf8"), context);
const projects = context.window.INSTALL_WORTHY_CATALOG.filter(p => p.visible !== false);
const index = readFileSync(`${root}index.html`, "utf8");
assert.equal(new Set(projects.map(p => p.id)).size, projects.length);
assert.equal((index.match(/<article class="project">/g) || []).length, projects.length);
for (const p of projects) {
  assert(existsSync(`${root}${p.icon}`));
  const png = readFileSync(`${root}${p.icon}`);
  assert.equal(png.subarray(1, 4).toString(), "PNG");
  assert.equal(png.readUInt32BE(16), 128);
  assert.equal(png.readUInt32BE(20), 128);
  assert(index.includes(p.name));
  const html = readFileSync(`${root}${p.id}/index.html`, "utf8");
  const schema = JSON.parse(html.match(/<script type="application\/ld\+json">(.*?)<\/script>/s)[1]);
  assert.equal(schema.name, p.name);
  assert.equal(schema.description, p.description);
  assert(html.includes(`rel="canonical" href="https://asdftq.github.io/install-worthy/${p.id}/"`));
  assert(html.includes("https://installworthy.substack.com/subscribe"));
  assert(!html.includes("Thanks for installing"));
  for (const link of p.links) {
    const url = new URL(link.url);
    assert.equal(url.protocol, "https:");
    assert(["apps.apple.com", "chromewebstore.google.com"].includes(url.hostname));
    assert(index.includes(link.url));
  }
}
assert(index.includes('rel="canonical" href="https://asdftq.github.io/install-worthy/"'));
assert(!index.includes('JavaScript is needed'));
console.log(`PASS: ${projects.length} catalog entries, exact-size icons, static links, canonical pages, and matching structured data.`);
