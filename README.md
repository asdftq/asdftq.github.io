# asdftq

Independent app studio homepage. Buildless HTML and CSS, system fonts, no tracking or third-party runtime dependencies.

Canonical URL: https://www.asdftq.com/

## Deployment

`main` is source; `gh-pages` is the live GitHub Pages branch. Commit on main, cherry-pick the explicit commit to gh-pages, push both, and verify the Pages build matches the deployed SHA.

Cloudflare DNS: DNS-only CNAME `www` → `asdftq.github.io`; apex A records → GitHub Pages addresses 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153. GitHub Pages custom domain `www.asdftq.com` redirects apex and default github.io host, preserving paths. Enable HTTPS enforcement after certificate provisioning.

Existing app pages, Install Worthy, legal pages, app-ads.txt, and unrelated service DNS must remain available. Homepage product links and artwork reuse the existing catalog. Test desktop/mobile layouts, local destinations, production redirects, HTTPS, and app-ads.txt before considering a deployment complete.

## Direct-sale Mac app

The studio homepage also lists NoBadge, released directly for Mac at `/nobadge/` for USD 2.99 once through Lemon Squeezy. Its card links to the dedicated product page, which states the required runtime builds and Full Disk Access before purchase. NoBadge is separate from the App Store-qualified Install Worthy catalog. `nobadge/assets/icon-128.png` is a 128×128 derivative of the existing actual app artwork in `nobadge/assets/icon.png`; preserve that source rather than substituting generated artwork.

## Search and SEO

The canonical hostname is `https://www.asdftq.com/`. Every public HTML page declares its canonical URL and a unique description. Keep internal links on that hostname when adding pages; the previous github.io hostname redirects here. The homepage declares `WebSite` structured data with the site name `asdftq`.

Submit `https://www.asdftq.com/sitemap.xml` in the `asdftq.com` Search Console domain property. This sitemap index includes `site-pages.xml` for studio and standalone app pages, plus the existing scoped Install Worthy and NoBadge sitemaps. Add new standalone public pages to `site-pages.xml`; regenerate the Install Worthy sitemap with its catalog sync script. List only canonical URLs and use `lastmod` only for actual content updates. `robots.txt` advertises the root index.

Ownership uses a Google verification TXT record at the domain root in Cloudflare. Keep that record after verification succeeds. Search Console reports and indexing take time to populate; sitemap submission or an indexing request does not guarantee inclusion or ranking.

References: [Google canonical URL guidance](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls), [sitemap guidance](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap), and [site-name metadata](https://developers.google.com/search/docs/appearance/site-names).
