# Install Worthy welcome hub

All extension install flows point to this page with an `installed` query parameter:

- `?installed=equilzer`
- `?installed=focus-lane`
- `?installed=right-click-share`

## Update the project list

Edit [`catalog.js`](catalog.js) for project copy, first-use hints, icons, and platform links. Product artwork lives in [`icons/`](icons/) and should match the published app icon. A project can have Chrome, iOS, Android, or web links without changing the page renderer. Set `visible: false` to stage an entry without showing it.

Run `node install-worthy/sync-catalog.mjs` from the repository root after editing the catalog. It maintains the static catalog, product pages, and `install-worthy/sitemap.xml` from the same source. Commit the generated HTML too; hosting has no build step or dependencies. The page uses no analytics, remote scripts, or external fonts. Publish both `main` and `gh-pages` at <https://asdftq.github.io/install-worthy/>.

## Released mobile apps (verified 2026-09-07)

Hwechul Cho ASC and the US public App Store both confirm QuietSense (6771237461, 1.1.0), Jet Lag Bye (6747702706, 1.8.0), and TimerBar (6744717499, 1.4.1). SpinHop is waiting for review; PassBasket, PronCoach, WayToSay, and TLDRFF are not released and are intentionally excluded.

Icons are unmodified Apple-served 128×128 PNG renditions from the public lookup `artworkUrl512` (replace the final size with `128x128bb.png`):

- QuietSense: `https://is1-ssl.mzstatic.com/image/thumb/Purple221/v4/b7/27/98/b7279821-b062-c77b-302b-2b7d1a47dc3c/AppIcon-0-0-1x_U007ephone-0-1-85-220.png/128x128bb.png`
- Jet Lag Bye: `https://is1-ssl.mzstatic.com/image/thumb/Purple211/v4/f4/97/17/f4971794-6cbe-3b5b-5867-047fe3c407c6/AppIcon-0-0-1x_U007ephone-0-1-85-220.png/128x128bb.png`
- TimerBar: `https://is1-ssl.mzstatic.com/image/thumb/Purple221/v4/08/2d/3d/082d3dfb-b44e-0c79-1b05-1f337107dadc/AppIcon-0-0-1x_U007ephone-0-1-85-220.png/128x128bb.png`

Native first-use links use `?installed=quietsense`, `?installed=jet-lag-bye`, or `?installed=timerbar`. They must be user-initiated, optional, and send no personal data. Adding an app here alone does not change the installed binary or App Store metadata. Use the stable product page as the App Store Marketing URL when preparing the next release.

Recognized install links personalize the hero with the product's exact catalog icon, name, description, and first step. The free Substack offer appears beside the product on desktop and directly below it on mobile. Unknown or missing install identifiers show a general welcome without claiming an installation.
