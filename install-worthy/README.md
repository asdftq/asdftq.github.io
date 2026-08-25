# Install Worthy welcome hub

All extension install flows point to this page with an `installed` query parameter:

- `?installed=equilzer`
- `?installed=focus-lane`
- `?installed=right-click-share`

## Update the project list

Edit only [`catalog.js`](catalog.js). Each project owns its copy, first-use hint, and one or more platform links. A project can have Chrome, iOS, Android, or web links without changing the page renderer. Set `visible: false` to stage an entry without showing it.

The page uses no analytics, remote scripts, external fonts, or build step. Push the `gh-pages` branch to publish changes at <https://asdftq.github.io/install-worthy/>.
