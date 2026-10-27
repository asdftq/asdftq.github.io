# Phase 1 — Jet Lag Bye: Travel Sleep Plan

Checked 2026-10-26. Live Apple lookup, public App Store HTML and Hwechul Cho ASC agree on version 1.8.6.

US ratings: 1. Free download does not mean free unlimited use. See [listing facts](listing-2026-10-26.md).

## Existing site and gap

Existing `/JetLagBye/` and `/install-worthy/jet-lag-bye/` pages were found. No route index or route-clock tool existed. Extend the existing case-sensitive `/JetLagBye/` hub.

Free first complete itinerary is confirmed in source and public listing; subsequent Single Trip Plan or Annual Unlimited access is implemented. Public listing still includes legacy monthly IAP; do not advertise it as the current purchase choice.

Build 60 directional airport-pair guides from 30 airline-network pairs and their reverse journeys. Exact inputs, IANA zones, computed dated shifts and airline citations are in `tools/growth/data/routes.csv`. No flight-duration estimates or nonstop availability promises.

CDC Yellow Book and the scholarly review inform general sleep/light context. Large shifts and date-line crossings are not reducible to a universal morning-light rule. Native review requests currently follow five checklist items or repeat visits; move to completion of a plan and retain the safe post-dismissal surface.

## Competition — public US Search API top ten

These are public API search observations, not on-device rankings. “Free” is the download price only. Descriptions below are short publisher claim excerpts, not verified product outcomes.

### jet lag

| App | Download | US ratings | Publisher’s opening claim |
|---|---|---:|---|
| [Timeshifter](https://apps.apple.com/us/app/timeshifter/id1380684374) | Free | 2678 | Reduce jet lag with personalized plans based on the latest sleep and circadian science |
| [Skiplagged: Travel Hacks](https://apps.apple.com/us/app/skiplagged-travel-hacks/id823443083) | Free | 336613 | We're the original hidden-city flight booking engine |
| [Reclock: Jet Lag Planner](https://apps.apple.com/us/app/reclock-jet-lag-planner/id6790334639) | Free | 0 | Your flights are already on your phone |
| [Jetlag - Travel & Timezone](https://apps.apple.com/us/app/jetlag-travel-timezone/id6444663705) | Free | 42 | Jetlag is the essential app for travelers who want to anticipate jet lag, organize their days abroad, and visu |
| [JetShift: Skip Jetlag](https://apps.apple.com/us/app/jetshift-skip-jetlag/id6744546503) | Free | 1 | Whether you're a frequent flyer, international traveler, or planning your first long-haul trip, JetShift helps |
| [Sandpiper: Jet Lag App](https://apps.apple.com/us/app/sandpiper-jet-lag-app/id6767356398) | Free | 2 | Sandpiper helps you reduce jet lag for your trip |
| [Private Web Browser - ORIN](https://apps.apple.com/us/app/private-web-browser-orin/id1237872910) | Free | 348 | Disclaimer: This is not the official Tor browser and is not affiliated with Tor Project Inc |
| [Flykitt](https://apps.apple.com/us/app/flykitt/id1571767892) | Free | 254 | Developed based on research with Navy SEALs and fighter pilots, loved by pro sports teams, and optimized for b |
| [LumiSync - Jet Lag Planner](https://apps.apple.com/us/app/lumisync-jet-lag-planner/id6789898622) | Free | 0 | Losing the first days of every trip to jet lag |
| [Jet Lag Time Zone Shifter](https://apps.apple.com/us/app/jet-lag-time-zone-shifter/id6670561167) | Free | 4 | Land ready, not wrecked |

### travel sleep

| App | Download | US ratings | Publisher’s opening claim |
|---|---|---:|---|
| [Timeshifter](https://apps.apple.com/us/app/timeshifter/id1380684374) | Free | 2678 | Reduce jet lag with personalized plans based on the latest sleep and circadian science |
| [TravelSleep Lite](https://apps.apple.com/us/app/travelsleep-lite/id355397579) | Free | 21 | [WARNING: Travel Sleep is extremely effective |
| [Jet Lag Bye: Travel Sleep Plan](https://apps.apple.com/us/app/jet-lag-bye-travel-sleep-plan/id6747702706) | Free | 1 | Jet lag is not just about bedtime |
| [Eight Sleep](https://apps.apple.com/us/app/eight-sleep/id1086913845) | Free | 17693 | Introducing Pod 6 |
| [Hatch Sleep](https://apps.apple.com/us/app/hatch-sleep/id1158048301) | Free | 62041 | Hey there |
| [Sleep Monitor: Sleep Tracker](https://apps.apple.com/us/app/sleep-monitor-sleep-tracker/id1510325113) | Free | 5323 | Ever wondered what really happens while you sleep |
| [Sleep Meister Lite](https://apps.apple.com/us/app/sleep-meister-lite/id599456380) | Free | 633 | Sleep Meister is a sleep aid app that uses the accelerometer sensor built into your device to monitor your bod |
| [Sleep Number](https://apps.apple.com/us/app/sleep-number/id811684463) | Free | 179668 | 5 |
| [Fan Noise Sleep Sounds](https://apps.apple.com/us/app/fan-noise-sleep-sounds/id1116451847) | Free | 23920 | Fall asleep faster with two high quality fan noises |
| [Sleep Music Timer](https://apps.apple.com/us/app/sleep-music-timer/id928930388) | Free | 7662 | This app allows you to fall asleep with favorite music |

## Source triangulation and intent limits

- Product behavior is checked against the owning source and Apple metadata, rather than the audit’s assumptions.
- General travel context: [CDC Yellow Book](https://www.cdc.gov/yellow-book/hcp/travel-air-sea/jet-lag-disorder.html) and [2019 scholarly review](https://pmc.ncbi.nlm.nih.gov/articles/PMC6684967/).
- Speaking context: [Toastmasters](https://www.toastmasters.org/magazine/magazine-issues/2025/feb/manage-your-speaking-time); [YC pitch clarity](https://www.ycombinator.com/library/4T-how-to-design-a-better-pitch-deck); [Atlassian stand-ups](https://www.atlassian.com/team-playbook/plays/standups); [Reading Rockets think-pair-share](https://www.readingrockets.org/classroom/classroom-strategies/think-pair-share).
- Noise references: [NIOSH poster](https://stacks.cdc.gov/view/cdc/78630), [NPS examples](https://www.nps.gov/teachers/classrooms/sound-intensity-and-loudness.htm), plus dated city sources in `cities.csv`.
- Community signals are anecdotal: [travel discussion](https://www.reddit.com/r/travel/comments/16h1akb/timeshifter_app_and_approach_to_jet_lag_japan/) highlights practical flight constraints; [noise-app question](https://www.reddit.com/r/neighborsfromhell/comments/1ornd54/any_apps_for_recording_noisy_neighbors/) highlights logging uncertainty; [Toastmasters timing discussion](https://www.reddit.com/r/Toastmasters/comments/ldkk01) shows that club practices vary. They are query/context evidence, not medical/legal authority or market-size estimates.
- No reliable search-volume, autocomplete-demand, Search Console, revenue or conversion data was obtained. Rehearsal durations and route coverage are explicitly editorial test inputs. Never relabel them as validated demand.

Phase 1 is recorded before page generation. User’s current instruction authorizes implementation, release and submission; attachment-only “proposal only” text does not override that authorization. No prices, ad budgets, outreach, account creation or domains are changed.
