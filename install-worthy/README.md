# Install Worthy welcome hub

All extension install flows point to this page with an `installed` query parameter:

- `?installed=equilzer`
- `?installed=focus-lane`
- `?installed=right-click-share`

## Update the project list

Edit [`catalog.js`](catalog.js) for project copy, first-use hints, icons, and platform links. Product artwork lives in [`icons/`](icons/) and should match the published app icon. A project can have Chrome, iOS, Android, or web links without changing the page renderer. Set `visible: false` to stage an entry without showing it.

Run `node install-worthy/sync-catalog.mjs` from the repository root after editing the catalog. It maintains the static catalog, product pages, and `install-worthy/sitemap.xml` from the same source. Commit the generated HTML too; hosting has no build step or dependencies. The page uses optional, consent-based GA4 through the shared `/analytics.js`; it loads no Google script before the visitor allows analytics. It uses no external fonts and works without JavaScript. Publish both `main` and `gh-pages` at <https://www.asdftq.com/install-worthy/>.

## Released mobile apps (verified 2026-10-26)

Hwechul Cho ASC and the public US App Store confirm TimerBar 1.4.2 (6744717499), Jet Lag Bye 1.8.6 (6747702706), QuietSense 1.1.3 (6771237461), and SpinHop 1.11.4 (6809077488). The catalog advertises those already-released products; update builds awaiting review are not presented as released.

All four icons are unmodified, official Apple-served 128×128 PNG renditions. Source URLs, date and owned screenshot provenance are checked in at `../assets/apps/<product-id>/sources.json`:

- jet-lag-bye: `https://is1-ssl.mzstatic.com/image/thumb/Purple221/v4/17/52/34/175234bc-4b2a-54d2-6c15-c046554cb1ba/AppIcon-0-0-1x_U007ephone-0-1-85-220.png/128x128bb.png`
- quietsense: `https://is1-ssl.mzstatic.com/image/thumb/Purple221/v4/b7/f6/1f/b7f61fc6-cb81-1f0e-f3d0-2405b040d28e/AppIcon-0-0-1x_U007ephone-0-1-85-220.png/128x128bb.png`
- spinhop: `https://is1-ssl.mzstatic.com/image/thumb/Purple211/v4/39/66/cb/3966cb2f-5258-883c-19b9-e57026a38edd/AppIcon-0-0-1x_U007emarketing-0-8-0-85-220.png/128x128bb.png`
- timerbar: `https://is1-ssl.mzstatic.com/image/thumb/Purple211/v4/2a/f5/d1/2af5d1b1-f6ea-712a-34c0-a562d4293513/AppIcon-0-0-1x_U007ephone-0-1-85-220.png/128x128bb.png`

Stable first-use links use `?installed=quietsense`, `?installed=jet-lag-bye`, `?installed=timerbar` and `?installed=spinhop`. They are voluntary and contain no personal app data. Every recognized link shows the actual icon, product name and first step beside the free newsletter offer. New product guide/web-preview links lead to the existing canonical product hub, not a duplicate catalog.

`sync-catalog.mjs` generates the HTML and scoped sitemap. The generator preserves shared consent controls. Product destination links use simple UTM labels; they are attribution labels, not a record of clicks. New tools contain no app telemetry or remote runtime dependencies.
