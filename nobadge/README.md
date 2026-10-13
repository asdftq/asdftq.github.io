# NoBadge prelaunch site

English static marketing and support site for NoBadge (`com.asdftq.nobadge`). Direct-sale distribution, planned USD 2.99 once through Lemon Squeezy. No checkout is published. No DMG/ZIP belongs in this public repository.

Run `node nobadge/check.mjs` and `node --check nobadge/feedback.js` from the repository root. Verify desktop and mobile layouts in Chrome, local links, captioned video playback, and feedback draft encoding. The feedback form only prepares a mailto draft on the device. It has no server, analytics, storage or automatic sending.

Native source captures: NoBadge 0.1.20 on macOS 26.5.1 (25F80), Apple Silicon; setup capture is the unchanged 0.1.18 guide. Creative sources and SHA-256 manifest live in the NoBadge repository under `Sales/`. All UI artwork comes from the actual installed app. The walkthrough is an illustrated screenshot sequence, not a continuous recording of Dock behavior.

Release gates: activated merchant, supported-runtime verification, explicit public launch authorization, final launch packaging, and a separately authorized live purchase/delivery check. Lemon Squeezy test mode does not enable file downloads. Keep `release.json` saleEnabled false and checkoutURL null until the actual live URL is verified. Do not invent offers, availability, ratings or testimonials. Do not add this unreleased app to the released-app catalog.

Deploy canonical main and the matching explicit cherry-pick to gh-pages, then verify the Pages build SHA and served checksums. Indexing and search traffic are separate from a successful deployment.
