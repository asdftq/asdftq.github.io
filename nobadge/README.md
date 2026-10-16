# NoBadge public release site

English static marketing and support site for NoBadge (`com.asdftq.nobadge`). Direct-sale distribution, USD 2.99 once through Lemon Squeezy. The public checkout is the verified Live product 1444435. Licensed update ZIPs are intentionally public under updates/; activation is enforced inside the app. Do not publish older unlicensed binaries or internal preparation kits.

Run `node nobadge/check.mjs` and `node --check nobadge/feedback.js` from the repository root. Verify desktop and mobile layouts in Chrome, local links, captioned video playback, and feedback draft encoding. The feedback form only prepares a mailto draft on the device. It has no server, analytics, storage or automatic sending.

Native source captures: NoBadge 0.1.20 on macOS 26.5.1 (25F80), Apple Silicon; setup capture is the unchanged 0.1.18 guide. Creative sources and SHA-256 manifest live in the NoBadge repository under `Sales/`. All UI artwork comes from the actual installed app. The walkthrough is an illustrated screenshot sequence, not a continuous recording of Dock behavior.

Released 2026-10-16 with explicit owner authorization after merchant approval, Test checkout/3DS/refund and Live zero-charge delivery verification. Final paid DMG 0.1.22 is signed/notarized; three customer downloads matched its hash, including fresh My Orders email authentication. This public repository contains marketing media only. `release.json`, static purchase links and truthful Offer metadata must agree. A rollback must remove purchase links/offers as well as disable release.json. Do not invent ratings, testimonials or support for other runtime builds. Keep the Install Worthy catalog within its App Store verification rules.

Deploy canonical main and the matching explicit cherry-pick to gh-pages, then verify the Pages build SHA and served checksums. Indexing and search traffic are separate from a successful deployment.

0.1.37 adds Lemon Squeezy license activation (up to 3 Macs, 30-day offline allowance) and a signed Sparkle feed at updates/appcast.xml. Stage future notarized updates using the native repository’s scripts/stage-update.py, then deploy and verify the exact Pages commit. Do not edit a signed appcast without re-signing it. Existing 0.1.35 users need one manual installer replacement before in-app updates are available.
