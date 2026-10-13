# asdftq

Independent app studio homepage. Buildless HTML and CSS, system fonts, no tracking or third-party runtime dependencies.

Canonical URL: https://www.asdftq.com/

## Deployment

`main` is source; `gh-pages` is the live GitHub Pages branch. Commit on main, cherry-pick the explicit commit to gh-pages, push both, and verify the Pages build matches the deployed SHA.

Cloudflare DNS: DNS-only CNAME `www` → `asdftq.github.io`; apex A records → GitHub Pages addresses 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153. GitHub Pages custom domain `www.asdftq.com` redirects apex and default github.io host, preserving paths. Enable HTTPS enforcement after certificate provisioning.

Existing app pages, Install Worthy, legal pages, app-ads.txt, and unrelated service DNS must remain available. Homepage product links and artwork reuse the existing catalog. Test desktop/mobile layouts, local destinations, production redirects, HTTPS, and app-ads.txt before considering a deployment complete.
