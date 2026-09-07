# Install Worthy welcome hub

All extension install flows point to this page with an `installed` query parameter:

- `?installed=equilzer`
- `?installed=focus-lane`
- `?installed=right-click-share`

## Update the project list

Edit [`catalog.js`](catalog.js) for project copy, first-use hints, icons, and platform links. Product artwork lives in [`icons/`](icons/) and should match the published app icon. A project can have Chrome, iOS, Android, or web links without changing the page renderer. Set `visible: false` to stage an entry without showing it.

The page uses no analytics, remote scripts, external fonts, or build step. Push the `gh-pages` branch to publish changes at <https://asdftq.github.io/install-worthy/>.

Recognized install links personalize the hero with the product's exact catalog icon, name, description, and first step. The free Substack offer appears beside the product on desktop and directly below it on mobile. Unknown or missing install identifiers show a general welcome without claiming an installation.
