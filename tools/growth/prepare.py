#!/usr/bin/env python3
"""One-time, cited seed data and research report preparation for the four-app treatment."""
import csv
import datetime as dt
import hashlib
import json
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'tools/growth/data'
REPORT = ROOT / 'docs/app-growth/2026-10-26'
EVIDENCE = REPORT / 'evidence'
DATE = '2026-10-26'
APPS = {'timerbar': 6744717499, 'jet-lag-bye': 6747702706, 'quietsense': 6771237461, 'spinhop': 6809077488}

class Text(HTMLParser):
    def __init__(self):
        super().__init__(); self.ignored = 0; self.lines = []
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'): self.ignored += 1
    def handle_endtag(self, tag):
        if tag in ('script', 'style'): self.ignored = max(0, self.ignored - 1)
    def handle_data(self, value):
        if not self.ignored and value.strip(): self.lines.append(value.strip())

def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'}), timeout=25) as r:
        return r.read(), r.geturl(), r.status

def write_csv(name, rows):
    with (DATA / name).open('w') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def seed():
    airports = {
        'JFK': ('New York', 'America/New_York', -73.778), 'EWR': ('Newark', 'America/New_York', -74.175),
        'LAX': ('Los Angeles', 'America/Los_Angeles', -118.408), 'SFO': ('San Francisco', 'America/Los_Angeles', -122.375),
        'SEA': ('Seattle', 'America/Los_Angeles', -122.309), 'ORD': ('Chicago', 'America/Chicago', -87.904),
        'BOS': ('Boston', 'America/New_York', -71.005), 'IAD': ('Washington, DC', 'America/New_York', -77.456),
        'DFW': ('Dallas–Fort Worth', 'America/Chicago', -97.038), 'ATL': ('Atlanta', 'America/New_York', -84.428),
        'LHR': ('London', 'Europe/London', -0.454), 'HND': ('Tokyo Haneda', 'Asia/Tokyo', 139.780),
        'NRT': ('Tokyo Narita', 'Asia/Tokyo', 140.392), 'CDG': ('Paris', 'Europe/Paris', 2.550),
        'FRA': ('Frankfurt', 'Europe/Berlin', 8.570), 'SYD': ('Sydney', 'Australia/Sydney', 151.177)}
    ba = 'https://www.britishairways.com/content/en/us/information/flight-information/our-route-network'
    ana = 'https://www.ana.co.jp/ja/it/plan-book/routes/international-route-information/'
    af = 'https://wwws.airfrance.us/en-us/flights-from-united-states'
    qf = 'https://www.qantas.com/en-us/where-we-fly/international-flight-routes'
    pairs = [(a,'LHR',ba) for a in ['JFK','LAX','SFO','SEA','ORD','BOS','EWR','IAD','DFW','ATL']]
    pairs += [(a,'HND',ana) for a in ['JFK','LAX','SFO','SEA','ORD','IAD']]
    pairs += [('BOS','NRT','https://www.jal.co.jp/jp/en/info/2026/inter/north-america/second/')]
    pairs += [(a,'CDG',af) for a in ['JFK','LAX','SFO','SEA','BOS','ATL']]
    pairs += [(a,'FRA','https://www.lufthansa.com/lhg/us/en/o-d/cy-cy/frankfurt-'+city) for a,city in [
        ('ORD','chicago'),('EWR','new-york'),('IAD','washington'),('DFW','dallas-fort-worth')]]
    pairs += [(a,'SYD',qf) for a in ['LAX','SFO','DFW']]
    routes = []
    for a,b,source in pairs:
        for origin,destination in [(a,b),(b,a)]:
            oc,oz,ol = airports[origin]; dc,dz,dl = airports[destination]
            delta = (dl - ol + 180) % 360 - 180
            def shift(date):
                at = dt.datetime.fromisoformat(date+'T12:00:00+00:00')
                return (at.astimezone(ZoneInfo(dz)).utcoffset()-at.astimezone(ZoneInfo(oz)).utcoffset()).total_seconds()/3600
            routes.append(dict(origin=origin,destination=destination,origin_city=oc,destination_city=dc,
                origin_zone=oz,destination_zone=dz,direction='eastward' if delta>0 else 'westward',
                reference_date=DATE,shift_hours=shift(DATE),january_shift_hours=shift('2027-01-15'),
                july_shift_hours=shift('2027-07-15'),source_url=source,verified_on=DATE,flight_time_band=''))
    write_csv('routes.csv', routes)
    # Rehearsal durations are explicit choices, not claims that an organization mandates them.
    cases = [
        ('presentation','Presentation rehearsal',[3,5,7,10,15,20,30,45],
         'https://www.toastmasters.org/magazine/magazine-issues/2025/feb/manage-your-speaking-time',
         'Use the time your host actually assigned. Rehearse aloud with your slides and reserve a clear ending.',
         'Open with the one point the audience should remember.','Drop a supporting example before dropping the conclusion.','At the final cue, land your main message before inviting questions.'),
        ('speech','Speech practice',[1,2,3,4,5,6,7,10],
         'https://www.toastmasters.org/magazine/magazine-issues/2025/feb/manage-your-speaking-time',
         'This is a practice budget you choose, not an official contest timer. Check your organizer’s current timing rules.',
         'Practice the first sentence until it feels unhurried.','Use one story rather than racing through several.','Leave the last thirty seconds for a deliberate final line.'),
        ('pitch','Pitch rehearsal',[0.5,1,2,3,5,7,10,15],
         'https://www.ycombinator.com/library/4T-how-to-design-a-better-pitch-deck',
         'Pitch length depends on the event. These are optional rehearsal budgets; Y Combinator’s guidance emphasizes a clear, simple story.',
         'State the problem and your answer before the details.','Choose evidence that supports one claim.','End with a concrete next step while time remains.'),
        ('meeting','Meeting agenda slot',[1,2,3,5,10,15,20,30],
         'https://www.atlassian.com/team-playbook/plays/standups',
         'Set an explicit agenda budget before starting. These slots are your choices; a stand-up’s short timebox is context, not a rule for every meeting.',
         'Name the decision this slot needs to produce.','Move topics that need a deep dive into a separate discussion.','Use the closing cue to agree who does what next.'),
        ('classroom','Classroom activity',[1,2,3,5,10,15,20,30],
         'https://www.readingrockets.org/classroom/classroom-strategies/think-pair-share',
         'Choose a timebox that suits your learners. Think-pair-share provides the activity structure; these durations are adjustable examples, not pedagogical standards.',
         'Give the instructions before starting the clock.','Tell learners what they should have ready when time ends.','Use the closing cue to return attention to the group.')]
    timers=[]
    for slug,name,durations,source,context,t1,t2,t3 in cases:
        for minutes in durations:
            seconds=int(minutes*60); label=f'{seconds}-second' if minutes<1 else f'{int(minutes)}-minute'
            opening=max(5,round(seconds*.15)); closing=min(30,max(5,round(seconds*.1)))
            timers.append(dict(slug=f'{label}-{slug}-timer',use_case=slug,name=name,seconds=seconds,
                label=label,context=context,tip1=t1,tip2=t2,tip3=t3,opening_seconds=opening,
                closing_seconds=closing,source_url=source,verified_on=DATE))
    write_csv('use-cases.csv',timers)
    niosh='https://stacks.cdc.gov/view/cdc/78630'
    nps='https://www.nps.gov/teachers/classrooms/sound-intensity-and-loudness.htm'
    write_csv('db-reference.csv',[dict(db=db,sound=sound,source_url=source,verified_on=DATE) for db,sound,source in [
        (30,'whisper',niosh),(50,'noisy conversation (one illustrative NPS example)',nps),
        (60,'normal conversation',niosh),(70,'vacuum cleaner',nps),(90,'lawn mower',nps),(110,'car horn at one metre',nps)]])
    write_csv('db-pages.csv',[dict(db=x) for x in [30,35,40,45,50,55,60,65,70,75,80,85,90]])
    # No numeric quiet hours or legal thresholds are reproduced. Each summary stays source-specific.
    cities=[
      ('new-york','New York','https://portal.311.nyc.gov/article/?kanumber=KA-01017','NYC311 separates neighbor noise from other noise categories and lists building management and mediation as additional routes.','Note whether the sound is music, speech, or furniture movement; the city routes different sources differently.'),
      ('portland','Portland','https://www.portland.gov/ppd/noise/noise-concerns','Portland’s Noise Program prioritizes specific dates, times and detailed descriptions and explains which noise types fall outside its authority.','Describe a repeatable pattern and the source if you can identify it; vague reports may not be processed.'),
      ('seattle','Seattle','https://www.seattle.gov/police/need-help/neighborhood-issues/noise-complaints','Seattle Police distinguishes residential disturbances from other unreasonable noise. Different conditions apply to each category.','Separate a house party from mechanical equipment and check the source-specific guidance before reporting.'),
      ('washington-dc','Washington, DC','https://ouc.dc.gov/page/call-311-police-non-emergencies','DC’s Office of Unified Communications lists noise complaints among police non-emergencies handled through its current contact guidance.','Identify whether this is music, an animal or construction so your notes support the correct routing.'),
      ('philadelphia','Philadelphia','https://www.phila.gov/services/mental-physical-health/report-a-health-or-safety-concern/report-air-and-noise-pollution/','Philadelphia distinguishes commercial and industrial noise handled by Air Management Services from individual or residential sources.','Record whether the suspected source is a business, building equipment, or a residence; do not assume one contact handles all three.'),
      ('austin','Austin','https://www.austintexas.gov/development-services/common-austin-code-violations','Austin’s guidance distinguishes mechanical noise and provides a route through Austin 3-1-1. Other complaints may follow different processes.','For equipment, describe a fan, compressor or other observable source rather than guessing which neighbor caused it.'),
      ('san-diego','San Diego','https://www.sandiego.gov/police/community/noise-complaints','San Diego’s police guidance addresses noisy neighbors, ongoing noise and mediation. It directs barking-dog issues through a different process.','Write whether the sound is still occurring and keep each incident separate from your description of the overall pattern.'),
      ('phoenix','Phoenix','https://www.phoenix.gov/administration/departments/law/faq.html','Phoenix’s Law Department FAQ distinguishes non-emergency noise issues from property-code concerns and landlord–tenant disputes.','Keep the sound observations factual; a noise log alone does not resolve a separate landlord–tenant question.'),
      ('houston','Houston','https://www.houstontx.gov/ara/rp/chapter-30-faq.html','Houston’s Chapter 30 FAQ explains sound regulation and complaint handling, including how official measurements are taken.','Write where you placed your phone. Your indoor reference reading is different from an official measurement at a specified location.'),
      ('minneapolis','Minneapolis','https://www.minneapolismn.gov/report-an-issue/noise-complaint/','Minneapolis publishes separate guidance for construction, garbage collection, amplified sound and yard maintenance.','Classify the source first and use the city’s matching section; do not apply construction rules to every household sound.'),
      ('raleigh','Raleigh','https://raleighnc.gov/housing/services/public-nuisances','Raleigh’s public-nuisance guidance identifies its police department as the contact for noise complaints.','Include the local date and whether the noise is recurring. Check the current city process rather than relying on a saved phone number.'),
      ('los-angeles','Los Angeles','https://lacity.gov/residents/request-services-report-problems','Los Angeles separates general MyLA311 services from non-emergency police complaints, including noise.','Distinguish a city-service request from a current noise disturbance and follow the city’s relevant channel.')]
    rows=[dict(slug=s,city=c,source_url=u,verified_on=DATE,summary=summary,tip=tip) for s,c,u,summary,tip in cities]
    write_csv('cities.csv',rows)
    return routes,timers,rows

def sources(cities):
    urls=sorted({r['source_url'] for r in cities})
    urls+=['https://www.cdc.gov/yellow-book/hcp/travel-air-sea/jet-lag-disorder.html',
      'https://pmc.ncbi.nlm.nih.gov/articles/PMC6684967/',
      'https://www.toastmasters.org/magazine/magazine-issues/2025/feb/manage-your-speaking-time',
      'https://www.ycombinator.com/library/4T-how-to-design-a-better-pitch-deck',
      'https://www.atlassian.com/team-playbook/plays/standups',
      'https://www.readingrockets.org/classroom/classroom-strategies/think-pair-share',
      'https://www.nps.gov/teachers/classrooms/sound-intensity-and-loudness.htm']
    def one(url):
        try:
            body,final,status=fetch(url);p=Text();p.feed(body.decode(errors='replace'))
            text='\n'.join(p.lines)
            return dict(url=url,final_url=final,status=status,date=DATE,sha256=hashlib.sha256(body).hexdigest(),
                        excerpts=[line[:500] for line in p.lines if re.search(r'noise|time|sleep|minute|decibel|sound',line,re.I)][:30])
        except Exception as e:return dict(url=url,status='unavailable',error=str(e),date=DATE)
    results=list(ThreadPoolExecutor(max_workers=3).map(one,urls))
    (EVIDENCE/'source-checks.json').write_text(json.dumps(results,indent=2))
    print('sources',[(r['status'],r['url']) for r in results],flush=True)

def reports(routes,timers,cities):
    lookup=json.loads((EVIDENCE/'apple-lookup.json').read_text())['results']
    clusters={'timerbar':['presentation timer','speech timer','meeting timer'],
              'jet-lag-bye':['jet lag','travel sleep'],'quietsense':['decibel meter','noise meter','loud neighbor'],
              'spinhop':['one tap game','jump game']}
    for slug,app_id in APPS.items():
        app=next(a for a in lookup if a['trackId']==app_id);folder=REPORT/slug;folder.mkdir(exist_ok=True)
        evidence=EVIDENCE/slug
        parser=Text();parser.feed((evidence/'public-listing.html').read_text())
        public='\n'.join(parser.lines);(evidence/'public-listing.txt').write_text(public)
        info=json.loads((evidence/'asc-app-info.json').read_text())['data'][0]['attributes']
        iap=public[public.find('In-App Purchases\nYes'):];iap=iap[:iap.find('Learn More')] if 'Learn More' in iap else iap[:300]
        facts=[f'# Public listing — {DATE}', '',f"Source: {app['trackViewUrl'].split('?')[0]}",
          f"Title: {app['trackName']}",f"Subtitle (ASC): {info['subtitle']}",
          f"Public version: {app['version']}; released {app['currentVersionReleaseDate']}.",
          f"US download price: {app['formattedPrice']}; US rating count: {app.get('userRatingCount',0)}.",
          '', 'Public in-app purchase list (US storefront; not a promise of current in-app availability):','',iap,
          '', 'First three screenshot URLs:',*app.get('screenshotUrls',[])[:3],
          '', 'Live listing description:',app['description'],
          '', 'Duo optimization badge: UNVERIFIED. No public badge claim is made.']
        (folder/f'listing-{DATE}.md').write_text('\n'.join(facts)+'\n')
        lines=[f'# Phase 1 — {app["trackName"]}', '',f'Checked {DATE}. Live Apple lookup, public App Store HTML and Hwechul Cho ASC agree on version {app["version"]}.', '',
               f'US ratings: {app.get("userRatingCount",0)}. Free download does not mean free unlimited use. See [listing facts](listing-{DATE}.md).', '',
               '## Existing site and gap', '']
        if slug=='timerbar':
            lines+=['Existing `/timerbar/` and `/install-worthy/timerbar/` pages were found in the sitemap and source. The former still used TimerBar+ naming; neither provided a working web timer or use-case pages. Extend `/timerbar/`; preserve the newsletter catalog.', '',
              'Build 40 rehearsal pages: five contexts × eight explicitly selectable durations. Source articles support the context, not a mandated duration or verified search volume. No contest-compliance claim. The complete matrix is `tools/growth/data/use-cases.csv`.', '',
              'Native gap: no automatic completion review prompt. Add one after three naturally completed timers, at finished-timer controls. Premium value remains themes/fonts/colors; multi-stage speaker/Q&A packs remain an unpriced product proposal.']
        elif slug=='jet-lag-bye':
            lines+=['Existing `/JetLagBye/` and `/install-worthy/jet-lag-bye/` pages were found. No route index or route-clock tool existed. Extend the existing case-sensitive `/JetLagBye/` hub.', '',
              'Free first complete itinerary is confirmed in source and public listing; subsequent Single Trip Plan or Annual Unlimited access is implemented. Public listing still includes legacy monthly IAP; do not advertise it as the current purchase choice.', '',
              'Build 60 directional airport-pair guides from 30 airline-network pairs and their reverse journeys. Exact inputs, IANA zones, computed dated shifts and airline citations are in `tools/growth/data/routes.csv`. No flight-duration estimates or nonstop availability promises.', '',
              'CDC Yellow Book and the scholarly review inform general sleep/light context. Large shifts and date-line crossings are not reducible to a universal morning-light rule. Native review requests currently follow five checklist items or repeat visits; move to completion of a plan and retain the safe post-dismissal surface.']
        elif slug=='quietsense':
            lines+=['Existing `/quietsense/` and `/install-worthy/quietsense/` pages were found. The old hub emphasized outgoing sound and lacked a store download CTA, sample log, city guides and reference pages.', '',
              'The audit’s “no logged result” assumption is incorrect: the free 60-second check already saves a real report and makes it readable without Pro. Native PDF/CSV export is absent. Add a free CSV for the latest result; keep unlimited checks as Pro. This adds value without changing prices or promising all-night/background monitoring.', '',
              f'Build {len(cities)} source-specific city guides and 13 dB comparison pages. Cities: '+', '.join(c['city'] for c in cities)+'.',
              'Twenty candidates were considered. Drop San Francisco, Boston, Chicago, Denver, Miami, Dallas, Nashville and Atlanta from this initial batch: source extraction/fit was insufficient for a current, specific residential summary. No numeric legal limits or universal quiet hours will be republished.', '',
              'NIOSH provides whisper (30 dB) and normal conversation (60 dB); NPS provides contextual examples at 50, 70, 90 and 110 dB. Intermediate query levels are interpolated positions, not invented named-source measurements. dB, dBA and uncalibrated phone estimates are not interchangeable certification.', '',
              'Existing native review prompt already waits for a completed saved report and settled reading at its end. Retain it; suspend requests while the CSV save sheet is open.']
        else:
            lines+=['**MONETIZATION WIRED UP: YES.** Public listing explicitly discloses advertising and optional Remove Ads ($2.99 US) / Supporter Pack ($4.99 US); ASC shows both IAPs approved. Source has production AdMob units and StoreKit entitlements. No purchase or ad-income claim is made.', '',
              'Existing Firebase landing/support/privacy remain valid; no SpinHop entry existed in the studio collection/catalog. Add one asdftq landing/demo and link the existing legal/support pages; keep Firebase hosting intact.', '',
              'Core loop: ride a rotating spinner, tap to leap to another, land to score; miss and retry. Native source already has seeded challenges, local progress, score sharing and a cooldown-limited review request on settled Home after completed play. No duplicate rating system.', '',
              '**GO for one clearly labelled, simplified timing mini-demo and listing metadata only. Zero additional SEO pages.** First screenshot communicates “one tap”; second shows a best-score chase; third invites another run. The full native game has mechanics the mini-demo deliberately omits. Cross-promotion remains a noninterruptive product specification, not an inserted advertisement in tool flows.']
        lines+=['', '## Competition — public US Search API top ten', '',
                'These are public API search observations, not on-device rankings. “Free” is the download price only. Descriptions below are short publisher claim excerpts, not verified product outcomes.']
        for query in clusters[slug]:
            data=json.loads((EVIDENCE/f'search-{query.replace(" ","-")}.json').read_text())['results'][:10]
            lines+=['',f'### {query}', '', '| App | Download | US ratings | Publisher’s opening claim |','|---|---|---:|---|']
            for x in data:
                claim=re.split(r'[\n.!?]', x.get('description',''))[0][:110].replace('|','/')
                lines.append(f'| [{x["trackName"]}]({x["trackViewUrl"].split("?")[0]}) | {x.get("formattedPrice", "price unavailable")} | {x.get("userRatingCount", "unavailable")} | {claim} |')
        lines+=['', '## Source triangulation and intent limits', '',
                '- Product behavior is checked against the owning source and Apple metadata, rather than the audit’s assumptions.',
                '- General travel context: [CDC Yellow Book](https://www.cdc.gov/yellow-book/hcp/travel-air-sea/jet-lag-disorder.html) and [2019 scholarly review](https://pmc.ncbi.nlm.nih.gov/articles/PMC6684967/).',
                '- Speaking context: [Toastmasters](https://www.toastmasters.org/magazine/magazine-issues/2025/feb/manage-your-speaking-time); [YC pitch clarity](https://www.ycombinator.com/library/4T-how-to-design-a-better-pitch-deck); [Atlassian stand-ups](https://www.atlassian.com/team-playbook/plays/standups); [Reading Rockets think-pair-share](https://www.readingrockets.org/classroom/classroom-strategies/think-pair-share).',
                '- Noise references: [NIOSH poster](https://stacks.cdc.gov/view/cdc/78630), [NPS examples](https://www.nps.gov/teachers/classrooms/sound-intensity-and-loudness.htm), plus dated city sources in `cities.csv`.',
                '- Community signals are anecdotal: [travel discussion](https://www.reddit.com/r/travel/comments/16h1akb/timeshifter_app_and_approach_to_jet_lag_japan/) highlights practical flight constraints; [noise-app question](https://www.reddit.com/r/neighborsfromhell/comments/1ornd54/any_apps_for_recording_noisy_neighbors/) highlights logging uncertainty; [Toastmasters timing discussion](https://www.reddit.com/r/Toastmasters/comments/ldkk01) shows that club practices vary. They are query/context evidence, not medical/legal authority or market-size estimates.',
                '- No reliable search-volume, autocomplete-demand, Search Console, revenue or conversion data was obtained. Rehearsal durations and route coverage are explicitly editorial test inputs. Never relabel them as validated demand.', '',
                'Phase 1 is recorded before page generation. User’s current instruction authorizes implementation, release and submission; attachment-only “proposal only” text does not override that authorization. No prices, ad budgets, outreach, account creation or domains are changed.']
        (folder/'PHASE1-REPORT.md').write_text('\n'.join(lines)+'\n')
        (folder/'LIMITS.md').write_text('# Verification limits\n\nNo revenue, installs, paid conversion, Search Console impressions/clicks, actual indexing or Duo badge has been verified. Public US storefront facts are dated 2026-10-26 and can change. Search API results are not personalized device search. No legal certification, medical outcome or guaranteed ranking is claimed. Sources that could not be retrieved are listed in evidence/source-checks.json. See PHASE1-REPORT.md for dropped cities and product-specific limits.\n')
    (REPORT/'README.md').write_text('''# Four-app treatment — 2026-10-26

The attached audit is research material. The user's explicit instruction authorizes implementation, publishing, release and review submission. It overrides the attachment's proposal-only restriction. No outreach, ad spending, new accounts or price changes are included.

Each app folder contains its Phase 1 findings, dated listing evidence, ASO pack and product decisions. Public evidence and ASC snapshots are in `evidence/`; search observations are in `../rank-history.csv`.

## Regeneration and weekly observation

- `python3 tools/growth/research.py --date YYYY-MM-DD` refreshes Apple facts and appends/replaces that day's rank rows, then writes a weekly report. Unavailable results stay blank, never rank 0.
- `python3 tools/growth/generate.py` regenerates product hubs and all guide pages from checked-in CSV inputs.
- `python3 tools/growth/check.py` validates local pages; add `--base https://www.asdftq.com` to validate deployed pages.
- `node install-worthy/sync-catalog.mjs` and `node install-worthy/verify.mjs` maintain the shared catalog.

No automation is scheduled by this work. Run the observation weekly when assessing the treatment. A sitemap entry, live URL check, indexing request, actual indexing, ranking and revenue are separate facts.
''')

if __name__=='__main__':
    routes,timers,cities=seed()
    reports(routes,timers,cities)
    sources(cities)
    print('Prepared',len(routes),'routes,',len(timers),'timer pages,',len(cities),'cities and four Phase 1 reports.')
