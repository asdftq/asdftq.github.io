# Monitoring

Static pages in this repo are monitored in Uptime Kuma at `https://uptime.asdftq.com`.

## Uptime Kuma monitors

| Monitor | URL | Expected result | Interval |
| --- | --- | --- | --- |
| `QuietSense / GitHub Pages` | `https://asdftq.github.io/quietsense/` | HTTP `200` | 300s |
| `Jet Lag Bye / GitHub Pages` | `https://asdftq.github.io/JetLagBye/` | HTTP `200` | 300s |
| `Right Click Share / GitHub Pages` | `https://asdftq.github.io/right-click-share/` | HTTP `200` | 300s |

## Hosting notes

- Repo: `asdftq/asdftq.github.io`
- Provider: GitHub Pages
- Pages deployment currently serves project subdirectories rather than a root homepage; `https://asdftq.github.io/` may return `404` while monitored project pages are healthy.

Add a Uptime Kuma monitor for each new public project subdirectory that should be externally reachable.
