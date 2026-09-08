// Maintenance only: checked-in HTML is served directly, with no deployment build.
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import vm from "node:vm";
const root = fileURLToPath(new URL("./", import.meta.url));
const context = { window: {} };
vm.runInNewContext(readFileSync(`${root}catalog.js`, "utf8"), context);
const projects = context.window.INSTALL_WORTHY_CATALOG.filter(p => p.visible !== false);
const base = "https://asdftq.github.io/install-worthy/";
const esc = value => String(value).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const json = value => JSON.stringify(value).replace(/</g, "\\u003c");
const links = p => p.links.map(l => `<a class="project-link" href="${esc(l.url)}" target="_blank" rel="noopener noreferrer">${esc(l.action || `Get for ${l.platform}`)}</a>`).join(" ");
const cards = projects.map(p => `<article class="project"><img class="project-icon" src="${esc(p.icon)}" width="42" height="42" alt=""><div class="project-copy"><h3><a href="${p.id}/">${esc(p.name)}</a></h3><p>${esc(p.description)}</p></div><div class="project-actions">${links(p)}</div></article>`).join("\n");
let index = readFileSync(`${root}index.html`, "utf8");
index = index.replace(/<!-- catalog:start -->[\s\S]*?<!-- catalog:end -->/, `<!-- catalog:start -->\n<div class="project-list" id="projectList">${cards}</div>\n<!-- catalog:end -->`);
writeFileSync(`${root}index.html`, index);
const newsletter = index.match(/<aside class="newsletter"[\s\S]*?<\/aside>/)[0];
for (const p of projects) {
  if (!/^[a-z0-9-]+$/.test(p.id)) throw new Error(`Invalid product id: ${p.id}`);
  const url = `${base}${p.id}/`;
  const schema = { "@context": "https://schema.org", "@type": "SoftwareApplication", name: p.name, description: p.description, url, image: `${base}${p.icon}`, operatingSystem: p.links.map(l => l.platform === "iOS" ? "iOS, iPadOS" : l.platform).join(", "), author: { "@type": "Person", name: "Hwechul Cho" }, sameAs: p.links.map(l => l.url) };
  const html = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light">
<title>${esc(p.name)} — Install Worthy</title><meta name="description" content="${esc(p.description)}"><link rel="canonical" href="${url}"><link rel="stylesheet" href="../styles.css?v=20260907-apps">
<meta property="og:title" content="${esc(p.name)}"><meta property="og:description" content="${esc(p.description)}"><meta property="og:url" content="${url}"><meta property="og:type" content="website">
<script type="application/ld+json">${json(schema)}</script></head>
<body><main class="page-shell"><header class="masthead"><a class="wordmark" href="../">← Install Worthy</a><span class="masthead-note">Apps by Hwechul Cho</span></header>
<section class="hero" aria-labelledby="hero-title"><div class="welcome"><img class="hero-icon" src="../${esc(p.icon)}" width="96" height="96" alt="${esc(p.name)} icon"><p class="eyebrow">${esc(p.links.map(l => l.platform).join(" · "))}</p><h1 id="hero-title">${esc(p.name)}</h1><p class="hero-copy">${esc(p.description)}</p><div class="project-actions">${links(p)}</div><div class="first-step"><strong>Start here</strong><p>${esc(p.firstStep)}</p></div></div>${newsletter}</section>
<section class="projects" aria-labelledby="about-title"><h2 id="about-title">About ${esc(p.name)}</h2><p>${esc(p.details || p.description)}</p><p>Made by Hwechul Cho. Check the official store listing for current availability, compatibility, pricing, and privacy details.</p><p><a href="../#projects">Explore all apps and Chrome extensions →</a></p></section>
<footer class="footer"><span>Newsletter signup is optional. No app account required to browse.</span><a href="https://installworthy.substack.com/subscribe">Subscribe free</a></footer></main></body></html>\n`;
  mkdirSync(`${root}${p.id}`, { recursive: true });
  writeFileSync(`${root}${p.id}/index.html`, html);
}
writeFileSync(`${root}sitemap.xml`, `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${[base, ...projects.map(p => `${base}${p.id}/`)].map(url => `<url><loc>${url}</loc></url>`).join("")}</urlset>\n`);
console.log(`Synced ${projects.length} products, static catalog, and sitemap.`);
