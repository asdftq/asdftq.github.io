# Phase 1 — QuietSense: Apartment dB Meter

Checked 2026-10-26. Live Apple lookup, public App Store HTML and Hwechul Cho ASC agree on version 1.1.3.

US ratings: 0. Free download does not mean free unlimited use. See [listing facts](listing-2026-10-26.md).

## Existing site and gap

Existing `/quietsense/` and `/install-worthy/quietsense/` pages were found. The old hub emphasized outgoing sound and lacked a store download CTA, sample log, city guides and reference pages.

The audit’s “no logged result” assumption is incorrect: the free 60-second check already saves a real report and makes it readable without Pro. Native PDF/CSV export is absent. Add a free CSV for the latest result; keep unlimited checks as Pro. This adds value without changing prices or promising all-night/background monitoring.

Build 12 source-specific city guides and 13 dB comparison pages. Cities: New York, Portland, Seattle, Washington, DC, Philadelphia, Austin, San Diego, Phoenix, Houston, Minneapolis, Raleigh, Los Angeles.
Twenty candidates were considered. Drop San Francisco, Boston, Chicago, Denver, Miami, Dallas, Nashville and Atlanta from this initial batch: source extraction/fit was insufficient for a current, specific residential summary. No numeric legal limits or universal quiet hours will be republished.

NIOSH provides whisper (30 dB) and normal conversation (60 dB); NPS provides contextual examples at 50, 70, 90 and 110 dB. Intermediate query levels are interpolated positions, not invented named-source measurements. dB, dBA and uncalibrated phone estimates are not interchangeable certification.

Existing native review prompt already waits for a completed saved report and settled reading at its end. Retain it; suspend requests while the CSV save sheet is open.

## Competition — public US Search API top ten

These are public API search observations, not on-device rankings. “Free” is the download price only. Descriptions below are short publisher claim excerpts, not verified product outcomes.

### decibel meter

| App | Download | US ratings | Publisher’s opening claim |
|---|---|---:|---|
| [Decibel X:dB Sound Level Meter](https://apps.apple.com/us/app/decibel-x-db-sound-level-meter/id448155923) | Free | 163476 | "Decibel X" is one of very few noise meter apps on the market that has highly reliable, pre-calibrated measure |
| [Decibel Meter Sound Detector](https://apps.apple.com/us/app/decibel-meter-sound-detector/id1254994873) | Free | 55775 | Track Environmental Noise with Ease |
| [NIOSH Sound Level Meter](https://apps.apple.com/us/app/niosh-sound-level-meter/id1096545820) | Free | 16938 | This award-winning app combines the best features of professional sound level meters and noise dosimeters into |
| [Sound Meter (Decibel)](https://apps.apple.com/us/app/sound-meter-decibel/id1626613141) | Free | 3252 | Sound level meter app is shows a decibel values by measure the environmental noise, displays measured dB value |
| [Decibel : dB sound level meter](https://apps.apple.com/us/app/decibel-db-sound-level-meter/id1227650795) | Free | 36154 | Decibel turns your device into a powerful sound level meter without any extra hardware |
| [Decibel Meter Ultra](https://apps.apple.com/us/app/decibel-meter-ultra/id1643525961) | Free | 2553 | Measure, record and track sound levels in your environment with Decibel Meter Ultra, the all-in-one sound leve |
| [Noise Meter - Sound & Decibel](https://apps.apple.com/us/app/noise-meter-sound-decibel/id6793926259) | Free | 3 | Noise Meter turns your iPhone into a simple, real-time sound level meter |
| [Decibel Metre (Sound Meter)](https://apps.apple.com/us/app/decibel-metre-sound-meter/id1590659820) | Free | 577 | Want to measure sound level |
| [Decibel Meter Master](https://apps.apple.com/us/app/decibel-meter-master/id1281344281) | Free | 3224 | Decibel Meter Master makes your iPhone as a sound level meter，it can measure noise level |
| [Decibel - sound level meter](https://apps.apple.com/us/app/decibel-sound-level-meter/id1485543216) | Free | 4706 | Decibel is the perfect app to evaluate the noise around you : measure the sound pressure, see the spectrum var |

### noise meter

| App | Download | US ratings | Publisher’s opening claim |
|---|---|---:|---|
| [NIOSH Sound Level Meter](https://apps.apple.com/us/app/niosh-sound-level-meter/id1096545820) | Free | 16938 | This award-winning app combines the best features of professional sound level meters and noise dosimeters into |
| [Decibel X:dB Sound Level Meter](https://apps.apple.com/us/app/decibel-x-db-sound-level-meter/id448155923) | Free | 163476 | "Decibel X" is one of very few noise meter apps on the market that has highly reliable, pre-calibrated measure |
| [Decibel Meter Sound Detector](https://apps.apple.com/us/app/decibel-meter-sound-detector/id1254994873) | Free | 55775 | Track Environmental Noise with Ease |
| [Noise Meter - Sound & Decibel](https://apps.apple.com/us/app/noise-meter-sound-decibel/id6793926259) | Free | 3 | Noise Meter turns your iPhone into a simple, real-time sound level meter |
| [Decibel : dB sound level meter](https://apps.apple.com/us/app/decibel-db-sound-level-meter/id1227650795) | Free | 36154 | Decibel turns your device into a powerful sound level meter without any extra hardware |
| [Sound Meter (Decibel)](https://apps.apple.com/us/app/sound-meter-decibel/id1626613141) | Free | 3252 | Sound level meter app is shows a decibel values by measure the environmental noise, displays measured dB value |
| [Decibel Meter - Sound Level.](https://apps.apple.com/us/app/decibel-meter-sound-level/id6757005588) | Free | 6 | Decibel Meter: Smart Noise Level Detector |
| [Decibel Meter: Sound dB](https://apps.apple.com/us/app/decibel-meter-sound-db/id1583767670) | Free | 347 | Turn your iPhone into a professional decibel meter with Noise Level: dB Tracker — the accurate sound meter app |
| [Decibel X PRO: dBA Noise Meter](https://apps.apple.com/us/app/decibel-x-pro-dba-noise-meter/id1257651611) | $69.99 | 6918 | "Decibel X" is the leading noise meter app on the market, which has highly reliable, pre-calibrated measuremen |
| [Decibel Meter Ultra](https://apps.apple.com/us/app/decibel-meter-ultra/id1643525961) | Free | 2553 | Measure, record and track sound levels in your environment with Decibel Meter Ultra, the all-in-one sound leve |

### loud neighbor

| App | Download | US ratings | Publisher’s opening claim |
|---|---|---:|---|
| [Neighbors by Ring](https://apps.apple.com/us/app/neighbors-by-ring/id1218902777) | Free | 304926 | Always know what’s happening in your neighborhood with real-time, hyper-local safety information from your nei |
| [Ring - Always Home](https://apps.apple.com/us/app/ring-always-home/id926252661) | Free | 1884849 | Know what’s happening at home from wherever you are with Ring Video Doorbells, Security Cameras and Alarm syst |
| [Hello Neighbor](https://apps.apple.com/us/app/hello-neighbor/id1386358600) | Free | 135033 | *Supported Devices: iPhone 6s, iPad 5 (2017), iPad Air 2, iPad Mini 4 and everything newer |
| [Key Ring Rewards Card Wallet](https://apps.apple.com/us/app/key-ring-rewards-card-wallet/id372547556) | Free | 20142 | Never carry loyalty, membership, or library cards again |
| [RingCentral](https://apps.apple.com/us/app/ringcentral/id715886894) | Free | 78212 | Run your business communications from anywhere with AI built in |
| [iSharing: GPS Location Tracker](https://apps.apple.com/us/app/isharing-gps-location-tracker/id416436167) | Free | 36373 | iSharing is the comprehensive family locator and GPS tracker app that keeps your loved ones safe and connected |
| [Adult Coloring Book - Pigment](https://apps.apple.com/us/app/adult-coloring-book-pigment/id1062006344) | Free | 219487 | = = = |
| [Super Loud Ringtones](https://apps.apple.com/us/app/super-loud-ringtones/id981537087) | Free | 671 | Super loud ringtones includes some of the most loud sounds and ringtones your phone can make |
| [Ringtones for iphone: Ringtune](https://apps.apple.com/us/app/ringtones-for-iphone-ringtune/id1036141497) | Free | 222177 | Don't settle for basic—try RingTune now and make your ringtone an extension of your personality with our ringt |
| [Glow Rings Puzzle](https://apps.apple.com/us/app/glow-rings-puzzle/id1407567943) | Free | 133 | Glow Rings Puzzle is a simple and addictive colorful puzzle game |

## Source triangulation and intent limits

- Product behavior is checked against the owning source and Apple metadata, rather than the audit’s assumptions.
- General travel context: [CDC Yellow Book](https://www.cdc.gov/yellow-book/hcp/travel-air-sea/jet-lag-disorder.html) and [2019 scholarly review](https://pmc.ncbi.nlm.nih.gov/articles/PMC6684967/).
- Speaking context: [Toastmasters](https://www.toastmasters.org/magazine/magazine-issues/2025/feb/manage-your-speaking-time); [YC pitch clarity](https://www.ycombinator.com/library/4T-how-to-design-a-better-pitch-deck); [Atlassian stand-ups](https://www.atlassian.com/team-playbook/plays/standups); [Reading Rockets think-pair-share](https://www.readingrockets.org/classroom/classroom-strategies/think-pair-share).
- Noise references: [NIOSH poster](https://stacks.cdc.gov/view/cdc/78630), [NPS examples](https://www.nps.gov/teachers/classrooms/sound-intensity-and-loudness.htm), plus dated city sources in `cities.csv`.
- Community signals are anecdotal: [travel discussion](https://www.reddit.com/r/travel/comments/16h1akb/timeshifter_app_and_approach_to_jet_lag_japan/) highlights practical flight constraints; [noise-app question](https://www.reddit.com/r/neighborsfromhell/comments/1ornd54/any_apps_for_recording_noisy_neighbors/) highlights logging uncertainty; [Toastmasters timing discussion](https://www.reddit.com/r/Toastmasters/comments/ldkk01) shows that club practices vary. They are query/context evidence, not medical/legal authority or market-size estimates.
- No reliable search-volume, autocomplete-demand, Search Console, revenue or conversion data was obtained. Rehearsal durations and route coverage are explicitly editorial test inputs. Never relabel them as validated demand.

Phase 1 is recorded before page generation. User’s current instruction authorizes implementation, release and submission; attachment-only “proposal only” text does not override that authorization. No prices, ad budgets, outreach, account creation or domains are changed.
