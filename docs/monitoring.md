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
- The canonical site is `https://www.asdftq.com/`, including the studio homepage and project subdirectories. The previous github.io hostname redirects to this custom domain.

Add a Uptime Kuma monitor for each new public project subdirectory that should be externally reachable.
