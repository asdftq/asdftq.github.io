# Four-app treatment — 2026-10-26

The attached audit is research material. The user's explicit instruction authorizes implementation, publishing, release and review submission. It overrides the attachment's proposal-only restriction. No outreach, ad spending, new accounts or price changes are included.

Each app folder contains its Phase 1 findings, dated listing evidence, ASO pack and product decisions. Public evidence and ASC snapshots are in `evidence/`; search observations are in `../rank-history.csv`.

## Regeneration and weekly observation

- `python3 tools/growth/research.py --date YYYY-MM-DD` refreshes Apple facts and appends/replaces that day's rank rows, then writes a weekly report. Unavailable results stay blank, never rank 0.
- `python3 tools/growth/generate.py` regenerates product hubs and all guide pages from checked-in CSV inputs.
- `python3 tools/growth/check.py` validates local pages; add `--base https://www.asdftq.com` to validate deployed pages.
- `node install-worthy/sync-catalog.mjs` and `node install-worthy/verify.mjs` maintain the shared catalog.

No automation is scheduled by this work. Run the observation weekly when assessing the treatment. A sitemap entry, live URL check, indexing request, actual indexing, ranking and revenue are separate facts.
