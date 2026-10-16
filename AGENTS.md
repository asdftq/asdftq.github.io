# Repository instructions

## Install Worthy welcome hub

- `install-worthy/` is the single welcome page and project catalog for Equilzer, Focus Lane, Right Click Share, and future platform releases.
- Keep the page Substack-first, simple, responsive, dependency-free, and usable without analytics, external fonts, or a deployment build step. The user-authorized site-wide GA4 tag is the only remote runtime exception: load it only after analytics consent through `/analytics.js`, preserve the privacy controls, and never send app data or form contents.
- After editing `catalog.js`, run `node install-worthy/sync-catalog.mjs` to update checked-in static HTML, product pages, and the scoped sitemap. Commit these artifacts together. Product pages and the catalog must work without JavaScript; preserve canonical URLs and truthful SoftwareApplication metadata. Do not invent ratings, reviews, or search-ranking guarantees.
- Add only publicly released apps verified in the Hwechul Cho ASC profile and the public App Store. Mobile icons must be downloaded from the official Apple artwork URL at 128×128, with provenance recorded in the hub README. Never list review-pending apps as installable.
- Native apps should offer the free newsletter optionally during first use and from Settings, never gate core functionality or auto-open a browser. Only an explicit tap may open the hub; send only the stable product id, never app/user data.
- Manage product copy, first-use guidance, visibility, icons, and platform destinations in `install-worthy/catalog.js`. Add iOS, Android, browser, and web destinations to a product's `links` array; do not create platform-specific copies of the hub.
- Every visible product must use its real published app icon. Never use initials, generic tiles, emoji, placeholder artwork, or an AI-generated approximation.
- Store hub icons under `install-worthy/icons/` and copy them from the canonical product assets:
  - Equilzer: `../eq/icons/icon128.png` → `install-worthy/icons/equilzer.png`
  - Focus Lane: `../workmode/assets/icon-128.png` → `install-worthy/icons/focus-lane.png`
  - Right Click Share: `../right-click-share/extension/icons/icon-128.png` → `install-worthy/icons/right-click-share.png`
- If an icon changes in a product repository, update the hub in the same work item and verify the source and served files match by checksum.
- Preserve the stable install identifiers `equilzer`, `focus-lane`, and `right-click-share`; extension install hooks depend on them.
- On each recognized install URL, put the installed product's real icon, name, description, and first-use guidance in the hero. A catalog badge alone is not sufficient installation confirmation. Keep the free newsletter offer prominent beside it on desktop and directly below it on mobile.
- Keep first-use copy truthful and brief. The hub must never receive extension settings, captured audio, tab addresses, selected content, or share payloads.
- Keep hosted privacy pages consistent with the automatic first-install GitHub Pages visit.

## Adding a service or platform

- Before editing, identify the canonical product repository, stable product id, public URL, distribution platforms, release state, actual icon, and the user's publication scope. Pick the smallest check that demonstrates the requested flow. A website change does not authorize an app release, store submission, or change to native-app telemetry.
- For a product already in the catalog, extend its existing entry and `links` array. Preserve install ids and existing URLs. For a new product, use one stable lowercase, hyphenated id across catalog entries, product routes, and supported `?installed=<id>` links.
- Verify public availability before showing an install or purchase CTA. Use `asc` with `asc auth switch --name "Hwechul Cho"` for personal Apple apps and confirm the public App Store listing; use the Ainbr account only for its products. Use `gplay --profile asdftq` for Android. Use `cws doctor` and the `flrngel-chrome-webstore` project for Chrome extensions; specify `--extension-id` on uploads and publishing. Reauthorize only when needed.
- Keep direct-sale products separate from the App Store-qualified hub unless their distribution is deliberately added to the catalog. For a direct sale, verify the released download, checkout destination, price, compatibility, required permissions, license/setup instructions, and support/refund information before advertising availability. Never present a draft checkout or review-pending binary as released.
- Update the studio collection in root `index.html` as well as `install-worthy/catalog.js` when the product belongs on both surfaces; the catalog generator does not maintain the studio homepage. Reuse the real product artwork and record its source. Do not add a second platform-specific product page just to add another store destination.
- Add the appropriate support, privacy, and terms destinations. Distinguish app data practices from website analytics, and describe only implemented behavior. Preserve existing legal/store URLs, `app-ads.txt`, and update/download endpoints. Update `app-ads.txt` only with verified publisher information when a product actually needs it.
- Change product version numbers only when doing extension/package implementation or deployment work; a website listing or documentation edit alone does not require a new app version.

## SEO and discovery for new pages

- Use `https://www.asdftq.com/` for this site's canonical URLs and internal absolute links. Give each indexable page a meaningful unique title and description, one canonical link, a clear primary heading, language, and viewport metadata. Use directory URLs for `index.html` pages; do not list both URL forms in a sitemap.
- Keep Open Graph metadata consistent with the page. Use real artwork for social images when adding them. Add truthful structured data appropriate to the page, preserving the homepage's `WebSite` identity `asdftq`; never fabricate ratings, prices, platform support, offers, or release status for search appearance.
- Add standalone public pages to `site-pages.xml`. Catalog pages belong in the generated `install-worthy/sitemap.xml`; NoBadge pages belong in `nobadge/sitemap.xml`. If a new section gets its own sitemap, register it in root `sitemap.xml`. Keep each indexable canonical URL in one child sitemap, exclude private/unreleased material, and change `lastmod` only when the underlying content changes.
- Keep `robots.txt` pointing to `https://www.asdftq.com/sitemap.xml` and preserve crawl access to public pages. New pages under this hostname use the existing `asdftq.com` Search Console domain property and submitted sitemap index; do not create a property or resubmit every existing URL for each product.
- For an actual new domain, configure its canonical host, DNS, HTTPS, and redirects, then add and verify the appropriate Search Console domain property and submit its sitemap. Preserve existing DNS records and verification TXT records. Do not grant new broad DNS access merely to automate verification when a manual TXT record suffices.
- After publishing a new service, check its important landing URL with Search Console's live URL test and request indexing once when appropriate. Distinguish an accepted sitemap, an indexable live page, an indexing request, actual indexing, and ranking; none proves the next stage. Do not wait for reporting delays or promise search placement as a deployment gate.

## Shared GA4 integration

- Reuse the existing website property and stream for pages on this site: account `40330748`, property `559357630` (`asdftq.com`), web stream `16145236003`, measurement ID `G-16EJGQ5TKK`. One measurement ID covers all product paths; never create one property or stream per page. This setup measures the website, not installed apps.
- Include the following once in every new HTML page's head, including support/legal pages. Preserve these includes in generators so regeneration cannot remove analytics:

  ```html
  <link rel="stylesheet" href="/analytics.css">
  <script src="/analytics.js" defer></script>
  ```

- Preserve the following footer controls, including a static privacy link that works without JavaScript:

  ```html
  <div class="site-data-note"><a href="/privacy.html">Website privacy</a><button type="button" data-analytics-settings hidden>Analytics settings</button></div>
  ```

- Keep consent and tag loading centralized in `/analytics.js`. No Google tag loads before Allow analytics; No thanks keeps it unloaded, and Analytics settings allows withdrawal. Keep the entire service usable when analytics is declined, blocked, or unavailable. Do not add a second gtag/GTM snippet or duplicate manual page views.
- Preserve URL/query/fragment sanitization, shortened referrals, approved simple UTM labels, disabled advertising personalization/Google signals, and disabled enhanced measurement. Never send form contents, feedback, ratings, email drafts, license keys, user ids, arbitrary URLs, or installed-app data. If collection changes, update `/privacy.html`, affected app website disclosures, and documentation together.
- A service on another domain/subdomain needs an explicit analytics ownership/scope decision. The shared script currently allows only `www.asdftq.com` and `asdftq.com`; copying it elsewhere will not collect data. Deliberately configure the correct stream, hostname allowlist, canonical URLs, privacy controls, and asset paths for an authorized new host. Do not silently mix an unrelated service into this property's data.
- For a new integration or a changed shared analytics flow, verify consent behavior and one real page navigation, then confirm its `page_view` in the matching GA4 realtime report. Inspect the canonical page path and measurement ID if the event is missing. The current Chrome setup can redirect the Google tag to a uBlock extension resource; use an already-available unblocked environment for this narrowly scoped check and leave the user's blocker settings intact. Do not turn every catalog addition into another full analytics audit.

## Verification and deployment

- Treat `main` as the canonical source branch and `gh-pages` as the live Pages branch. A hub change is not deployed until the intended commit is present and pushed on both branches.
- Use explicit commit hashes when cherry-picking from `main` to `gh-pages`; do not use ambiguous reflog references.
- Run JavaScript syntax checks, validate that every visible catalog icon exists and is 128×128, and verify all store links before committing.
- After pushing `gh-pages`, wait for the GitHub Pages build to report `built` for that exact commit. Verify served icon checksums, then inspect the live page in Chrome at desktop and mobile widths.
- Clean up verification tabs after use, while preserving any Chrome Web Store dashboard tab intentionally left for user handoff.
- Commit completed work using Conventional Commits.
- Match verification to the change: catalog edits use `node install-worthy/sync-catalog.mjs` and `node install-worthy/verify.mjs`; shared scripts need syntax checks; NoBadge page changes use `node nobadge/check.mjs` when relevant. Check new links/assets and the requested core flow once. Do not add cross-platform matrices, repeat passing checks, or rerun unrelated release tests.
- Documentation-only edits need a source/diff review and `git diff --check`, not store-link checks, browser layout QA, or analytics traffic generation. Keep the instructions synchronized on `main` and `gh-pages`; when pushing the Pages branch, confirm its build for the exact commit without expanding into unrelated UI testing.
- Report the source and deployed commits, relevant public URLs, what was actually verified, and any concrete pending external state. Close temporary browser/DevTools tabs, stop processes started for verification, and retain only intentional handoff tabs and useful evidence.
