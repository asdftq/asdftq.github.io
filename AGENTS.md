# Repository instructions

## Install Worthy welcome hub

- `install-worthy/` is the single welcome page and project catalog for Equilzer, Focus Lane, Right Click Share, and future platform releases.
- Keep the page Substack-first, simple, responsive, dependency-free, and usable without analytics, tracking scripts, remote code, external fonts, or a deployment build step.
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

## Verification and deployment

- Treat `main` as the canonical source branch and `gh-pages` as the live Pages branch. A hub change is not deployed until the intended commit is present and pushed on both branches.
- Use explicit commit hashes when cherry-picking from `main` to `gh-pages`; do not use ambiguous reflog references.
- Run JavaScript syntax checks, validate that every visible catalog icon exists and is 128×128, and verify all store links before committing.
- After pushing `gh-pages`, wait for the GitHub Pages build to report `built` for that exact commit. Verify served icon checksums, then inspect the live page in Chrome at desktop and mobile widths.
- Clean up verification tabs after use, while preserving any Chrome Web Store dashboard tab intentionally left for user handoff.
- Commit completed work using Conventional Commits.
