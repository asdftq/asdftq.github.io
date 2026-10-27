#!/usr/bin/env python3
"""Regenerate buildless product hubs and useful, cited guide pages from CSV inputs."""
import csv
import datetime as dt
import html
import itertools
import json
import re
from pathlib import Path
from urllib.parse import urlencode
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'tools/growth/data'
BASE = 'https://www.asdftq.com'
DATE = '2026-10-26'
CDC = 'https://www.cdc.gov/yellow-book/hcp/travel-air-sea/jet-lag-disorder.html'
PRODUCTS = {
 'timerbar': dict(name='TimerBar', app=6744717499, path='/timerbar/', category='ProductivityApplication',
     line='A presentation clock with a live progress bar.', terms='/timerbar/terms.html', privacy='/timerbar/privacy.html', support='/timerbar/support.html'),
 'jet-lag-bye': dict(name='Jet Lag Bye', app=6747702706, path='/JetLagBye/',category='TravelApplication',
     line='A travel sleep plan built around your itinerary and usual sleep.',terms='https://www.apple.com/legal/internet-services/itunes/dev/stdeula/',privacy='/JetLagBye/privacy.html',support='/JetLagBye/support.html'),
 'quietsense': dict(name='QuietSense',app=6771237461,path='/quietsense/',category='UtilitiesApplication',
     line='Reference sound readings and a report for your shared home.',terms='/quietsense/terms.html',privacy='/quietsense/privacy.html',support='/quietsense/support.html'),
 'spinhop':dict(name='SpinHop',app=6809077488,path='/spinhop/',category='GameApplication',
     line='Ride the spinner. Time the leap. Chase your next landing.',terms='https://www.apple.com/legal/internet-services/itunes/dev/stdeula/',privacy='https://spinhop-mvp-2026.web.app/privacy/',support='https://spinhop-mvp-2026.web.app/support/')}
MANIFEST=[]
esc=lambda x:html.escape(str(x),quote=True)
json_safe=lambda x:json.dumps(x,ensure_ascii=False).replace('<','\\u003c')
def read(name):return list(csv.DictReader((DATA/name).open()))
def absolute(url):return BASE+url if url.startswith('/') else url
def store(slug,medium,content):
    return 'https://apps.apple.com/app/id'+str(PRODUCTS[slug]['app'])+'?'+urlencode(dict(
      utm_source='asdftq',utm_medium=medium,utm_campaign=slug,utm_content=content))
def cta(slug,medium,content,label=None):
    return f'<a class="button" href="{esc(store(slug,medium,content))}">{esc(label or "Get "+PRODUCTS[slug]["name"]+" on the App Store")} ↗</a>'
def paragraph(text):return '<p>'+esc(text)+'</p>'
def sources(items):
    return '<p class="source">Sources · '+ ' · '.join(f'<a href="{esc(url)}">{esc(name)}</a>' for name,url in items)+f' · checked {DATE}</p>'
def faq(items):
    return '<section class="section"><h2>A few useful answers.</h2>'+''.join(
      f'<details><summary>{esc(q)}</summary>{paragraph(a)}</details>' for q,a in items)+'</section>'
def newsletter():
    return '<aside class="newsletter"><div><h2>Your next useful app. In your inbox.</h2><p>Install Worthy is the free newsletter from asdftq. Signup is optional, and you can unsubscribe anytime.</p></div><a class="button secondary" href="https://installworthy.substack.com/subscribe">Subscribe free ↗</a></aside>'
def identity(slug):
    return f'<div class="app-identity"><img src="/install-worthy/icons/{slug}.png" width="48" height="48" alt=""><span>{PRODUCTS[slug]["name"]} <span class="small">by asdftq</span></span></div>'
def screens(slug,captions):
    return '<section class="section"><p class="eyebrow">IN THE IPHONE APP</p><h2>See what you’ll use.</h2><div class="screens">'+''.join(
      f'<figure><img src="/assets/apps/{slug}/{i:02}.jpg" width="600" height="1200" loading="lazy" alt="{esc(text)}"><figcaption>{esc(text)}</figcaption></figure>' for i,text in enumerate(captions,1))+'</div></section>'
def page(path,slug,title,description,body,questions=(),scripts=(),kind='guide'):
    p=PRODUCTS[slug];url=BASE+path
    schema={'@context':'https://schema.org','@graph':[{'@type':'WebPage','name':title,'description':description,'url':url}]}
    if kind=='hub':schema['@graph'].append({'@type':'SoftwareApplication','name':p['name'],'url':url,
        'applicationCategory':p['category'],'operatingSystem':'iOS','image':BASE+f'/install-worthy/icons/{slug}.png',
        'sameAs':'https://apps.apple.com/app/id'+str(p['app']),'author':{'@type':'Organization','name':'asdftq'}})
    if questions:schema['@graph'].append({'@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in questions]})
    content=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(description)}"><link rel="canonical" href="{url}">
<meta name="theme-color" content="#f6f5f0"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{url}"><meta property="og:type" content="website"><meta property="og:image" content="{BASE}/install-worthy/icons/{slug}.png">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/app-guides.css"><link rel="stylesheet" href="/analytics.css"><script src="/analytics.js" defer></script>
{''.join(f'<script src="{script}" defer></script>' for script in scripts)}
<script type="application/ld+json">{json_safe(schema)}</script></head><body><a class="skip" href="#main">Skip to content</a><div class="shell"><header class="masthead"><a class="wordmark" href="{BASE}/">asdftq.</a><nav aria-label="Main"><a href="{BASE+p['path']}">{p['name']}</a><a href="{BASE}/install-worthy/">All apps ↗</a></nav></header><main id="main">{body}</main>{newsletter()}<footer class="footer"><span>© 2026 asdftq · Small apps. Thoughtfully made.</span><nav aria-label="Product links"><a href="{absolute(p['support'])}">Support</a><a href="{absolute(p['privacy'])}">App privacy</a><a href="{absolute(p['terms'])}">Terms</a></nav></footer></div><div class="site-data-note"><a href="/privacy.html">Website privacy</a><button type="button" data-analytics-settings hidden>Analytics settings</button></div></body></html>
'''
    target=ROOT/path.strip('/')/'index.html';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(content)
    MANIFEST.append(dict(path=path,slug=slug,kind=kind,title=title,scripts=list(scripts)))

def timer(seconds):
    return f'''<div class="timer" data-timer data-seconds="{seconds}" data-state="ready"><p class="eyebrow">YOUR TIME, AT A GLANCE</p><div class="timer-digits" data-digits aria-label="Time remaining">{seconds//60:02}:{seconds%60:02}</div><progress max="1" value="0" aria-label="Elapsed timer progress"></progress><p class="timer-label" data-timer-status role="status">Ready when you are.</p><div class="timer-controls"><button type="button" data-start>Start timer</button><button type="button" data-reset>Reset</button></div><div class="timer-config"><label for="timer-minutes">Minutes</label><input id="timer-minutes" data-minutes type="number" min="0.0166666667" max="360" step="any" value="{seconds/60:g}" inputmode="decimal"></div><noscript>The timer needs JavaScript. The guide and app link work without it.</noscript></div>'''

def timer_pages():
    rows=read('use-cases.csv');groups={r['use_case']:[] for r in rows}
    for r in rows:groups[r['use_case']].append(r)
    questions=[('Is the web timer free?','Yes. Start, pause and reset it without signing up. It runs in your browser; no timer settings are sent to us.'),
      ('What does TimerBar+ include?','The iPhone/iPad app’s paid monthly or yearly subscription adds premium themes, fonts and colors. The core clock and timer are free. Current regional prices appear in the App Store.'),
      ('Will the web timer keep my screen awake?','This web timer does not prevent your device from sleeping or play a background alarm. Keep the page visible for rehearsal. The native app supports an always-on display.'),
      ('Can I use it for a speech contest?','Use it for rehearsal and check your organizer’s current rules. The closing cue is not an official Toastmasters green/yellow/red contest signal sequence.'),
      ('Can I save timers in the app?','Yes. The current app supports named presets and duration editing. The web timer keeps only the current page’s timer in memory.')]
    cards=''.join(f'<a class="card" href="/timerbar/{group}/"><p class="eyebrow">{len(items)} READY-TO-USE TIMERS</p><h3>{esc(items[0]["name"])}</h3><p>Choose a duration. Practice the part that matters.</p></a>' for group,items in groups.items())
    body=f'''<section class="hero"><div>{identity('timerbar')}<p class="eyebrow">PRESENTATIONS · SPEECHES · MEETINGS</p><h1>Make the ending<br>feel intentional.</h1><p class="lead">A big clock. A quiet progress bar. A clear sense of how much room your next point has.</p><div class="actions">{cta('timerbar','timer_page','hub')}<a class="button secondary" href="#timers">Find your timer ↓</a></div><p class="small">Free core timer · Optional TimerBar+ customization</p></div><div>{timer(300)}<p class="small">Try a five-minute rehearsal here. Keep this page visible while it runs.</p></div></section><section class="section" id="timers"><div class="section-head"><h2>What are you timing?</h2><p>Forty adjustable rehearsal timers. Choose your own timebox; your host’s actual schedule comes first.</p></div><div class="cards">{cards}</div></section>'''
    body+=screens('timerbar',['Stay on time with a fullscreen clock.','Read your progress in one glance.','Hide the clock and focus on time remaining.'])+faq(questions)
    page('/timerbar/','timerbar','TimerBar — Presentation timer & free online rehearsal timers','Start a free presentation timer online, or use TimerBar on iPhone and iPad for a fullscreen clock, live progress bar and named presets.',body,questions,['/app-timer.js'],'hub')
    for group,items in groups.items():
        links=''.join(f'<a href="/timerbar/timers/{r["slug"]}/">{esc(r["label"].capitalize()+" "+r["name"].lower())} →</a>' for r in items)
        body=f'<section class="hero single"><p class="eyebrow">TIMERBAR · CHOOSE A TIMEBOX</p><h1>{esc(items[0]["name"])} timers.</h1><p class="lead">{esc(items[0]["context"])}</p></section><section class="section"><div class="guide-list">{links}</div>{sources([(items[0]["name"]+" context",items[0]["source_url"])])}</section>'
        page(f'/timerbar/{group}/','timerbar',items[0]['name']+' timers — TimerBar','Choose an adjustable '+items[0]['name'].lower()+' timer. Free start, pause and reset; no signup.',body,kind='index')
        for index,r in enumerate(items):
            seconds=int(r['seconds']);opening=int(r['opening_seconds']);closing=int(r['closing_seconds']);middle=seconds-opening-closing
            quick=seconds<=180
            strategy=('A short slot rewards a single clear idea. Practice one opening, one example and one final sentence.' if quick else
              'A longer slot needs structure, not extra slides. Divide the middle into distinct points and rehearse the transitions aloud.')
            agenda=[('Opening',opening,'State the purpose before adding detail.'),('Main idea' if quick else 'Main points',middle,'One example is enough.' if quick else 'Leave space between points instead of filling every second.'),('Closing',closing,'Deliver your final line and stop.')]
            agenda_html='<div class="table-wrap"><table><caption>An optional practice budget — adjust to your material</caption><thead><tr><th>Part</th><th>Seconds</th><th>Purpose</th></tr></thead><tbody>'+''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a,b,c in agenda)+'</tbody></table></div>'
            q=[(f'Is {r["label"]} an official requirement?',r['context']),('What happens at the end?','The digits reach zero, the progress bar fills, and the label says “Time is up.” There is no alarm or automatic upload.')]
            others=[items[(index-1)%len(items)],items[(index+1)%len(items)]]
            related=''.join(f'<a href="/timerbar/timers/{x["slug"]}/">{esc(x["label"].capitalize())} {esc(x["name"].lower())} →</a>' for x in others)
            body=f'<div class="breadcrumb"><a href="/timerbar/">TimerBar</a> / <a href="/timerbar/{group}/">{esc(r["name"])}</a></div><section class="hero"><div><p class="eyebrow">FREE ONLINE REHEARSAL TIMER</p><h1>{esc(r["label"].capitalize())}<br>{esc(r["name"].lower())}.</h1><p class="lead">{esc(strategy)}</p><div class="actions">{cta("timerbar","timer_page",r["slug"],"Take TimerBar to your next talk")}</div><p class="small">Native app: fullscreen clock, always-on support and named presets.</p></div>{timer(seconds)}</section><article class="article"><p>{esc(r["context"])}</p>{agenda_html}<h2>Three ways to keep your pace.</h2><ol>'+''.join('<li>'+esc(r[k])+'</li>' for k in ['tip1','tip2','tip3'])+f'</ol>{sources([("Context and practice guidance",r["source_url"])])}<p class="notice">The live text cue and digits carry the timing information; color is an additional cue. Keep the page visible. This is a rehearsal aid for everyday talks, meetings and classes.</p>{faq(q)}<section class="section"><h2>Try a different timebox.</h2><div class="guide-list">{related}<a href="/timerbar/">All TimerBar timers →</a></div></section></article>'
            page(f'/timerbar/timers/{r["slug"]}/','timerbar',f'{r["label"].capitalize()} {r["name"].lower()} timer — TimerBar',f'A free {r["label"]} timer for {r["name"].lower()}: start, pause, reset, a readable progress bar and a practical rehearsal outline.',body,q,['/app-timer.js'])

def route_clock(r):
    origin,dest=r['origin'],r['destination'];shift=float(r['shift_hours'])
    return f'''<div class="clock-widget" data-route-clock data-origin-zone="{r['origin_zone']}" data-destination-zone="{r['destination_zone']}"><p class="eyebrow">CHECK THE CLOCKS FIRST</p><label for="clock-date">Your travel date</label><br><input id="clock-date" type="date" value="{DATE}" min="2020-01-01" max="2035-12-31"><p data-clock-output role="status">On {DATE}, the destination clock is {abs(shift):g} hours {'ahead of' if shift>=0 else 'behind'} the origin clock.</p><p class="small">Date changes stay in this browser. This compares time zones; it does not create a personal sleep plan.</p></div>'''
def route_slug(r):return (r['origin']+'-to-'+r['destination']).lower()
def route_label(r):return f'{r["origin_city"]} ({r["origin"]}) → {r["destination_city"]} ({r["destination"]})'
def travel_pages():
    rows=read('routes.csv');origins=sorted({r['origin'] for r in rows})
    q=[('Is my first plan free?','Your first complete one-way or round-trip itinerary is free as a one-time local offer, without a card. Additional plans use a Single Trip Plan purchase or Annual Unlimited. Reinstalling does not reset the offer.'),
      ('What does the app plan?','Sleep, waking, light exposure and caffeine timing around your itinerary and usual sleep schedule. Recommendations use the correct departure or destination clock.'),
      ('Can I save the plan for travel?','Yes. Revisit locally saved plans, check off actions and save the full itinerary as an image in Photos.'),
      ('Do the route guides tell me exactly when to seek light?','No. Precise timing depends on your sleep schedule and flights. Large time changes and date-line crossings need special care; a route’s compass direction alone is insufficient.'),
      ('Is it medical advice?','No. This is general educational information and individual results vary. Ask a qualified clinician before changing sleep routines or using sleep aids, including melatonin.')]
    links=''.join(f'<a href="/JetLagBye/routes/from-{a.lower()}/">Routes from {a} →</a>' for a in origins)
    sample=next(r for r in rows if r['origin']=='JFK' and r['destination']=='LHR')
    body=f'<section class="hero"><div>{identity("jet-lag-bye")}<p class="eyebrow">FOR TRAVEL ACROSS TIME ZONES</p><h1>A new city.<br>A clearer sleep plan.</h1><p class="lead">Turn your itinerary and usual sleep schedule into a day-by-day plan for sleep, light and caffeine, in the right local time.</p><div class="actions">{cta("jet-lag-bye","route_page","hub","Create your first free plan")}<a class="button secondary" href="#routes">Explore your route ↓</a></div><p class="small">First complete itinerary free · No card required</p></div>{route_clock(sample)}</section><section class="section" id="routes"><div class="section-head"><h2>Start with your route.</h2><p>Sixty route guides. Compare the clocks, see an example preparation outline, then create a plan for your actual dates in the app.</p></div><div class="guide-list">{links}</div></section>'
    body+=screens('jet-lag-bye',['Your first complete travel plan is free.','A day-by-day itinerary for your trip.','Timing tailored to your sleep and travel.'])
    body+='<div class="disclaimer">General educational information only. Individual results vary. Ask a qualified clinician about changing sleep routines or using sleep aids. No medication dose or guaranteed outcome is provided.</div>'+faq(q)
    page('/JetLagBye/','jet-lag-bye','Jet Lag Bye — Travel sleep plans & route guides','Compare time zones on 60 travel routes and create your first complete travel sleep plan free with Jet Lag Bye for iPhone.',body,q,['/route-clock.js'],'hub')
    for origin in origins:
        subset=[r for r in rows if r['origin']==origin]
        body=f'<section class="hero single"><p class="eyebrow">JET LAG BYE · ROUTE INDEX</p><h1>From {esc(subset[0]["origin_city"])}.</h1><p class="lead">Choose a destination for a dated clock comparison and a general preparation outline. These pages do not replace a plan for your actual flights.</p></section><section class="section"><div class="guide-list">'+''.join(f'<a href="/JetLagBye/routes/{route_slug(r)}/">{esc(route_label(r))} →</a>' for r in subset)+'</div><p><a href="/JetLagBye/#routes">All departure airports →</a></p></section>'
        page(f'/JetLagBye/routes/from-{origin.lower()}/','jet-lag-bye',f'Travel sleep routes from {subset[0]["origin_city"]} ({origin}) — Jet Lag Bye',f'Compare time zones and prepare for travel from {subset[0]["origin_city"]}. Dated route-clock examples and general sleep-planning context.',body,kind='index')
    for r in rows:
        slug=route_slug(r);shift=float(r['shift_hours']);size=abs(shift);ahead='ahead of' if shift>=0 else 'behind'
        oz,dz=ZoneInfo(r['origin_zone']),ZoneInfo(r['destination_zone'])
        clocks=[]
        for hour in [7,12,18,22]:
            at=dt.datetime.fromisoformat(DATE).replace(hour=hour,tzinfo=oz);there=at.astimezone(dz)
            clocks.append((at.strftime('%H:%M'),there.strftime('%H:%M'),there.strftime('%b %d')))
        clocktable=f'<div class="table-wrap"><table><caption>The same moments on {DATE}, using IANA time zones</caption><thead><tr><th>{r["origin"]} clock</th><th>{r["destination"]} clock</th><th>Destination date</th></tr></thead><tbody>'+''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a,b,c in clocks)+'</tbody></table></div>'
        seasonal=(f'January 15, 2027: {float(r["january_shift_hours"]):+g} hours; July 15, 2027: {float(r["july_shift_hours"]):+g} hours (destination minus origin). '
          +('The difference changes seasonally, so a saved offset can be wrong for another departure date.' if r['january_shift_hours']!=r['july_shift_hours'] else 'These two seasonal examples have the same difference; always check your own travel date.'))
        direction=('Eastward travel often asks for an earlier body-clock schedule. A smaller pre-trip advance can help some travelers, while a late bedtime in the departure city may make the first local night harder.' if r['direction']=='eastward' else 'Westward travel often asks for a later body-clock schedule. Holding out for an appropriate local bedtime can be difficult when the departure clock already feels late.')
        if size>=12:shape='This large civil-clock gap crosses a calendar boundary in many schedules. Do not turn the printed hour difference into hours of forced wakefulness. Check both arrival date and clock time before planning rest.'
        elif size>=8:shape='This is a substantial clock change. Build rest around your actual arrival hour, and leave room for a less demanding first local day. A universal morning-light instruction can be mistimed for some travelers.'
        else:shape='This smaller long-haul clock difference can still disturb sleep. Anchor your first local evening to the destination date rather than treating tiredness as a cue to take a long late nap.'
        examples=[('Two or three days before departure',f'Look at the {r["origin"]} evening row above beside the {r["destination"]} clock. If feasible, make a modest sleep-schedule shift toward your destination without cutting your sleep short.'),
          ('Flight day',f'Keep the ticket’s {r["origin"]} departure date and {r["destination"]} arrival date visible. Plan a realistic opportunity to rest; avoid relying on alcohol for sleep. Caffeine close to intended sleep can make rest harder.'),
          ('First local day',f'Use {r["destination_city"]} local time for meals, activities and the coming bedtime. {shape}'),
          ('Following days','Recheck how rested you feel before adding demanding activities. General advice is not a promise of a fixed adjustment time; use your personalized schedule and clinical guidance when appropriate.')]
        plan=''.join(f'<h3>{esc(a)}</h3><p>{esc(b)}</p>' for a,b in examples)
        related=[x for x in rows if x['origin']==r['destination'] and x['destination']==r['origin']]
        related += [x for x in rows if route_slug(x)!=slug and x['origin']==r['origin']][:2]
        related += [x for x in rows if route_slug(x)!=slug and x['destination']==r['destination']][:2]
        unique={route_slug(x):x for x in related}
        q=[(f'What is the {r["origin"]} to {r["destination"]} time difference?',f'On {DATE}, {r["destination_city"]} is {size:g} hours {ahead} {r["origin_city"]}. Seasonal offset examples: {seasonal}'),
          (f'Is this an {r["direction"]} trip?',f'The shorter geographic direction from {r["origin"]} to {r["destination"]} is {r["direction"]}. Direction and civil-clock offset are different concepts, especially around the date line. Neither alone determines your personal light schedule.'),
          ('Is the sample a personal plan?','No. It is an educational outline, not advice for your sleep schedule or health. The app uses your itinerary and usual sleep to create a plan; your first complete itinerary is free.')]
        body=f'<div class="breadcrumb"><a href="/JetLagBye/">Jet Lag Bye</a> / <a href="/JetLagBye/routes/from-{r["origin"].lower()}/">From {r["origin"]}</a></div><section class="hero"><div><p class="eyebrow">{r["direction"].upper()} · ROUTE CLOCK GUIDE</p><h1>{esc(r["origin_city"])}<br>to {esc(r["destination_city"])}.</h1><p class="lead">{r["origin"]} → {r["destination"]} is an {r["direction"]} journey. On {DATE}, the destination clock is {size:g} hours {ahead} the origin clock. Your travel date can change the difference.</p><div class="actions">{cta("jet-lag-bye","route_page",slug,"Generate your own travel plan")}</div><p class="small">Your first complete one-way or round-trip itinerary is free.</p></div>{route_clock(r)}</section><article class="article"><h2>Read both clocks before planning sleep.</h2>{clocktable}<p>{esc(seasonal)}</p><p>{esc(direction)}</p><h2>An example shape for this trip.</h2><p class="notice">An educational example, not a personal schedule. Precise light timing depends on your internal clock as well as the itinerary.</p>{plan}{sources([("CDC jet lag guidance",CDC),("Airline route/network reference",r["source_url"])])}<p class="source">Airline service and dates can change. This is a travel-planning guide, not a timetable or a claim that a nonstop flight operates on your date. Flight-duration estimates are omitted.</p><div class="disclaimer">General educational information only; individual results vary. This is not medical advice. Ask a qualified clinician before changing sleep routines or using sleep aids, including melatonin. No dose is recommended here.</div>{faq(q)}<section class="section"><h2>Compare another journey.</h2><div class="guide-list">'+''.join(f'<a href="/JetLagBye/routes/{key}/">{esc(route_label(x))} →</a>' for key,x in unique.items())+'</div><p><a href="/JetLagBye/">Back to Jet Lag Bye →</a></p></section></article>'
        page(f'/JetLagBye/routes/{slug}/','jet-lag-bye',f'{r["origin"]} to {r["destination"]} jet lag: {r["direction"]} travel guide',f'{r["origin_city"]} to {r["destination_city"]}: compare dated local clocks, understand the {r["direction"]} journey and see a general preparation outline.',body,q,['/route-clock.js'])

NOISE_DISCLAIMER='Phone readings are reference/comparison estimates, not certified measurements or legal certification. Accuracy varies by device, microphone, placement and room. Rules vary by city, property and lease; check the current local ordinance and your lease. This is general information, not legal advice.'
def sample_log():
    return '''<div class="panel" id="sample-log"><p class="eyebrow">FICTIONAL SAMPLE · ILLUSTRATIVE READINGS</p><h3>Start with a clear, factual record.</h3><div class="table-wrap"><table><caption>Illustrative logging worksheet — not a real complaint or app screenshot</caption><thead><tr><th>Date &amp; local time</th><th>Duration</th><th>Avg / peak estimate</th><th>Observation</th></tr></thead><tbody><tr><td>Oct 20, 2026 · 22:15</td><td>60 seconds</td><td>48 / 61 dB</td><td>Repeated bass rhythm; source unconfirmed.</td></tr><tr><td>Oct 21, 2026 · 22:40</td><td>60 seconds</td><td>43 / 57 dB</td><td>Brief impacts, then quiet; phone in same place.</td></tr></tbody></table></div><p class="small">The current published app saves a latest-check summary on device. A pending update adds a CSV with UTC start/end times, active duration, estimated average/peak, environment, activity and accuracy limits. The narrative notes column above is a worksheet example; the app does not currently capture freeform complaint notes or certify timestamps. PDF export and all-night/background logging are not offered.</p><a href="/assets/apps/quietsense/sample-log.csv" download>Download the fictional worksheet (CSV) ↓</a></div>'''
def log_link():
    return '<aside class="panel"><h3>What does a factual log look like?</h3><p><a href="/quietsense/#sample-log">See the fictional two-night worksheet and download its CSV →</a></p><p class="small">Illustrative readings only. Separate what you observed from what you inferred.</p></aside>'
def noise_pages():
    cities=read('cities.csv');refs=read('db-reference.csv');levels=read('db-pages.csv')
    q=[('What can I try free?','One 60-second room check, with its real report saved on your device. Reading that report does not require a subscription. Pro adds unlimited checks and other monitoring controls.'),
      ('Can it measure my neighbor’s room?','No. The microphone reads sound at your phone. Any nearby-room values in the app are modeled estimates, not measurements of what a neighbor hears.'),
      ('Does it record conversations?','No. Sound level is processed on device; raw audio is not saved, uploaded or transcribed.'),
      ('Can I export a report?','The current published version stores reports in the app. A pending update adds a free CSV of the latest completed check. The downloadable web worksheet is a clearly fictional example, not a real measurement or a claim of PDF export.'),
      ('Can I use a phone reading as legal proof?','Do not treat it as certified evidence or a decision about a violation. Accuracy varies by hardware and placement; timestamps follow the device clock. Check the current city process and lease, and ask the relevant authority what documentation it accepts.')]
    cards=''.join(f'<a href="/quietsense/guides/{x["db"]}-db/">What does {x["db"]} dB mean? →</a>' for x in levels)
    citylinks=''.join(f'<a href="/quietsense/cities/{c["slug"]}/">{esc(c["city"])} noise guidance →</a>' for c in cities)
    body=f'<section class="hero"><div>{identity("quietsense")}<p class="eyebrow">EVERYDAY SOUND · SHARED HOMES</p><h1>Less guessing.<br>A clearer next step.</h1><p class="lead">Check sound where your phone is, read a simple report, and keep your observations factual.</p><div class="actions">{cta("quietsense","evidence_page","hub","Try your free 60-second check")}<a class="button secondary" href="#sample-log">See a sample log ↓</a></div><p class="small">One free check and its saved report · Unlimited checks with Pro</p></div><div class="panel"><p class="eyebrow">A REFERENCE, WITH LIMITS</p><h2>A phone estimate.<br>Useful context.</h2><p>Placement, walls and the microphone affect the result. Compare readings in the same spot and write what happened, not what you assume caused it.</p><p class="small">Not a certified, legal, medical or safety meter. Nearby-room values are modeled, not measured.</p></div></section>{sample_log()}<section class="section"><h2>Put the numbers in context.</h2><div class="guide-list">{cards}</div></section><section class="section"><h2>Check your city’s process.</h2><p class="prose-width">Source-specific guides for everyday logging. Each links to official city guidance. No universal quiet hours or legal dB limits are assumed.</p><div class="guide-list">{citylinks}</div></section>'
    body+=screens('quietsense',['Read a calm live sound-awareness signal.','See when sound may carry nearby.','Read what your first free check found.'])+f'<div class="disclaimer">{NOISE_DISCLAIMER}</div>'+faq(q)
    page('/quietsense/','quietsense','QuietSense — Apartment sound checks, noise logs & city guides','Try one free 60-second sound check. Understand phone-reading limits, see a fictional noise log and find official noise guidance for your city.',body,q,kind='hub')
    folder=ROOT/'assets/apps/quietsense';folder.mkdir(parents=True,exist_ok=True)
    (folder/'sample-log.csv').write_text('sample_only,date,local_time,time_zone,duration_seconds,illustrative_average_db,illustrative_peak_db,fictional_observation\nTRUE,2026-10-20,22:15,local unspecified,60,48,61,"Repeated bass rhythm; source unconfirmed. Fictional sample; not certified."\nTRUE,2026-10-21,22:40,local unspecified,60,43,57,"Brief impacts then quiet. Fictional sample; not certified."\n')
    for level in levels:
        db=int(level['db']);exact=next((r for r in refs if int(r['db'])==db),None)
        low=max((r for r in refs if int(r['db'])<=db),key=lambda x:int(x['db']))
        high=min((r for r in refs if int(r['db'])>=db),key=lambda x:int(x['db']))
        comparison=(f'A published reference example at {db} dB is {exact["sound"]}. Actual sound depends on distance, the source and the room.' if exact else
          f'{db} dB sits between the published reference examples of {low["sound"]} ({low["db"]} dB) and {high["sound"]} ({high["db"]} dB). That is context, not a claim that a particular appliance measures {db} dB.')
        context=('A small background sound can be noticeable in an otherwise quiet bedroom. Listen for repetitions and note whether it interrupted a rest period.' if db<50 else
          'At conversation-like levels, the pattern can matter as much as a single number. Describe whether the sound is steady, intermittent, bass-heavy or a brief impact.' if db<70 else
          'A louder source can mask surrounding sounds. Move away from uncomfortable sound and avoid deliberately recreating it to compare a phone reading. This page does not set a safe exposure duration.')
        difference=db-30;ratio=10**(difference/10)
        q=[(f'Is {db} dB too loud at night?',f'A single {db} dB value cannot decide that. Background sound, duration, frequency, room, sleep needs and the applicable rule all matter. Check the current ordinance and lease; a phone estimate is not legal certification.'),
          (f'What should I record beside a {db} dB estimate?','The local date/time and time zone, active duration, phone position, average and peak if available, what you heard and any uncertainty about its source. A phone cannot identify who caused it.')]
        table='<div class="table-wrap"><table><caption>Published everyday comparisons — approximate, source-dependent</caption><thead><tr><th>Reference</th><th>Level</th><th>Source</th></tr></thead><tbody>'+''.join(f'<tr><td>{esc(x["sound"])}</td><td>{x["db"]} dB</td><td><a href="{x["source_url"]}">Reference</a></td></tr>' for x in {x['db']:x for x in [low,high]}.values())+'</tbody></table></div>'
        related=''.join(f'<a href="/quietsense/cities/{c["slug"]}/">{esc(c["city"])} guidance →</a>' for c in cities[:3])
        neighbors=[x for x in levels if x!=level and abs(int(x['db'])-db)<=10]
        related+=''.join(f'<a href="/quietsense/guides/{x["db"]}-db/">Compare {x["db"]} dB →</a>' for x in neighbors)
        body=f'<div class="breadcrumb"><a href="/quietsense/">QuietSense</a> / Sound references</div><section class="hero single"><p class="eyebrow">REFERENCE SOUND LEVEL · {db} dB</p><h1>What does {db} dB<br>tell you?</h1><p class="lead">{esc(comparison)}</p></section><article class="article">{table}<h2>Daytime and nighttime need context.</h2><p>{esc(context)}</p><p>A daytime reading beside an active source is different from an overnight reading at your bed. Keep the microphone position and source distance in your notes. These examples do not reproduce your room or your phone’s calibration.</p><div class="panel"><h3>The scale is logarithmic.</h3><p>{db} dB is {difference} dB above the 30 dB reference. On a sound-intensity scale that is approximately {ratio:,.0f} times the reference intensity. It does not mean it sounds that many times louder, and this calculation does not certify a phone reading.</p></div><h2>A number needs a record around it.</h2><p>Note time, duration and context alongside the reading. Avoid identifying a source as a particular person unless you actually know. Keep personal notes on your device rather than entering them on this website.</p>{log_link()}{sources([(x["sound"]+" example",x["source_url"]) for x in {x['db']:x for x in [low,high]}.values()])}<div class="disclaimer">{NOISE_DISCLAIMER}</div><div class="actions">{cta("quietsense","evidence_page",str(db)+"-db","Try QuietSense for a reference check")}</div>{faq(q)}<section class="section"><h2>Keep the context.</h2><div class="guide-list">{related}<a href="/quietsense/">All sound and city guides →</a></div></section></article>'
        page(f'/quietsense/guides/{db}-db/','quietsense',f'What does {db} dB sound like? Apartment context — QuietSense',f'Understand a {db} dB reading with cited everyday comparisons, day/night context and a fictional logging worksheet. Phone estimates are not certified.',body,q)
    for c in cities:
        q=[(f'What are quiet hours in {c["city"]}?',f'There is no single quiet-hours rule reproduced here. Check {c["city"]}’s current official guidance for the source, property and situation, plus your lease. Construction rules do not automatically apply to every household sound.'),
          ('Does a noise log prove a violation?','No. It describes your observations. A city may require a particular measurement method, location, duration or other documentation. Ask the relevant authority what it accepts.')]
        body=f'<div class="breadcrumb"><a href="/quietsense/">QuietSense</a> / City guidance</div><section class="hero single"><p class="eyebrow">OFFICIAL SOURCE CHECKED {DATE}</p><h1>Apartment noise<br>in {esc(c["city"])}.</h1><p class="lead">Find the right local guidance, then keep a factual record of what happened.</p></section><article class="article"><h2>Start with the city’s own guidance.</h2><p>{esc(c["summary"])}</p>{sources([(c["city"]+" official guidance",c["source_url"])])}<p class="notice">This is a dated summary of the linked source, not a determination about your situation. We do not publish a universal quiet-hours window or numeric legal noise limit.</p><h2>What to put in your log.</h2><p>{esc(c["tip"])}</p><ol><li>Write the local date, start/end time and time zone. A device timestamp follows the device clock; it is not independently certified.</li><li>Describe the sound, how long it lasted and whether it repeated. Mark an unknown source as unknown.</li><li>Record the phone position and estimated average/peak if available. Use the same position for comparisons.</li><li>Keep your own notes private. This website has no complaint form and receives no recordings, addresses or report contents.</li></ol>{log_link()}<div class="disclaimer">{NOISE_DISCLAIMER}</div><div class="actions">{cta("quietsense","evidence_page",c["slug"],"Try a free reference sound check")}</div>{faq(q)}<section class="section"><h2>Understand the reading.</h2><div class="guide-list"><a href="/quietsense/guides/40-db/">40 dB context →</a><a href="/quietsense/guides/60-db/">60 dB context →</a><a href="/quietsense/guides/70-db/">70 dB context →</a><a href="/quietsense/">All QuietSense guides →</a></div></section></article>'
        page(f'/quietsense/cities/{c["slug"]}/','quietsense',f'{c["city"]} apartment noise: local guidance & logging — QuietSense',f'Find {c["city"]}’s official noise guidance and learn what a factual noise log can contain. Dated sources, fictional example and phone-reading limits.',body,q)

def spinhop():
    q=[('Is this the full SpinHop game?','No. This is a simplified web timing mini-demo with original geometric artwork. The native game adds moving spinner fields, characters, coins, combos, Fever and seeded challenges.'),
      ('How does the full game make money?','SpinHop is free to download with advertising and optional one-time purchases. Remove Ads stops automatic between-run ads; optional rewarded videos remain. The Supporter Pack includes Remove Ads and the six launch characters. Prices vary by storefront.'),
      ('Where is my demo best saved?','Only in this browser’s local storage when available. It is separate from the app’s score and is never uploaded by the demo. Sharing occurs only when you tap Share demo best.')]
    demo='''<div class="game-panel" data-spinhop-demo><div class="game-stats"><span>DEMO HOPS <span data-score>0</span></span><span>BEST <span data-best>0</span></span></div><canvas width="420" height="420" tabindex="0" role="img" aria-label="SpinHop timing mini-demo. A marker circles a ring. Hop while it crosses the green opening; use the Tap to hop button or focus the canvas and press Space."></canvas><p class="game-message" data-game-message role="status">Wait for the green opening. Tap to leap.</p><div class="game-controls"><button type="button" data-hop>Tap to hop</button><button type="button" data-share-score>Share demo best</button></div><p class="small">Simplified web demo · Original geometric art · Scores stay here</p><noscript>Enable JavaScript to play this mini-demo, or get the full game from the App Store.</noscript></div>'''
    body=f'<section class="hero"><div>{identity("spinhop")}<p class="eyebrow">ONE TAP · ONE MORE TRY</p><h1>Wait for it.<br>Now hop.</h1><p class="lead">Catch the opening, leap to the next spinner, and see how far your timing takes you.</p><div class="actions">{cta("spinhop","demo_page","hub","Play the full SpinHop game")}</div><p class="small">Free to play · Advertising and optional one-time purchases</p><p class="small">Try the timing idea here. This mini-demo is separate from the native game and its scores.</p></div>{demo}</section><section class="section"><div class="cards"><article class="card"><p class="eyebrow">01 · READ IT</p><h3>Watch the rotation.</h3><p>Your marker circles the ring. The green opening points toward the next platform.</p></article><article class="card"><p class="eyebrow">02 · TIME IT</p><h3>Tap at the opening.</h3><p>A clean hop lands and scores. Miss the window and try the same simple idea again.</p></article><article class="card"><p class="eyebrow">03 · OWN IT</p><h3>Chase your demo best.</h3><p>Your best stays in this browser. Share only when you choose; every shared demo score is labelled.</p></article></div></section>'
    body+=screens('spinhop',['One tap starts the next leap.','Chase your personal best in the native game.','Miss, learn the timing and play another run.'])+faq(q)
    page('/spinhop/','spinhop','SpinHop — One tap, big leaps. Try the web timing demo.','Try a free SpinHop timing mini-demo: wait for the opening, tap to leap and chase a local demo best. Get the full one-tap arcade game for iPhone and iPad.',body,q,['/spinhop-demo.js'],'hub')

def duplicate_check():
    # Compare representative samples before keeping the full generated batch.
    groups={'routes':['/JetLagBye/routes/jfk-to-lhr/','/JetLagBye/routes/lax-to-hnd/','/JetLagBye/routes/syd-to-dfw/','/JetLagBye/routes/cdg-to-bos/','/JetLagBye/routes/ord-to-fra/'],
      'timers':['/timerbar/timers/3-minute-presentation-timer/','/timerbar/timers/1-minute-speech-timer/','/timerbar/timers/30-second-pitch-timer/','/timerbar/timers/30-minute-meeting-timer/','/timerbar/timers/10-minute-classroom-timer/'],
      'noise':['/quietsense/cities/new-york/','/quietsense/cities/portland/','/quietsense/cities/houston/','/quietsense/guides/30-db/','/quietsense/guides/85-db/']}
    results={}
    for name,paths in groups.items():
        shingles=[]
        for path in paths:
            source=(ROOT/path.strip('/')/'index.html').read_text()
            source=re.sub(r'<script[\s\S]*?</script>|<style[\s\S]*?</style>','',source)
            source=re.search(r'<main[^>]*>([\s\S]*)</main>',source).group(1)
            words=re.findall(r'[a-z0-9]+',html.unescape(re.sub('<[^>]+>',' ',source)).lower())
            shingles.append(set(tuple(words[i:i+8]) for i in range(max(0,len(words)-7))))
        pairs=[dict(a=paths[i],b=paths[j],shared_ratio=round(len(shingles[i]&shingles[j])/max(1,min(len(shingles[i]),len(shingles[j]))),3)) for i,j in itertools.combinations(range(5),2)]
        results[name]=pairs
        if max(x['shared_ratio'] for x in pairs)>.82:raise SystemExit(f'{name}: sample prose is too repetitive; improve the template before publishing')
    output=ROOT/'docs/app-growth/2026-10-26/duplicate-samples.json';output.write_text(json.dumps(results,indent=2))

def main():
    timer_pages();travel_pages();noise_pages();spinhop();duplicate_check()
    guides=[m for m in MANIFEST if m['kind']!='hub']
    (ROOT/'guides-sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{BASE+m["path"]}</loc></url>\n' for m in guides)+'</urlset>\n')
    sitemap=ROOT/'sitemap.xml';text=sitemap.read_text()
    if '/guides-sitemap.xml' not in text:sitemap.write_text(text.replace('</sitemapindex>',f'  <sitemap><loc>{BASE}/guides-sitemap.xml</loc></sitemap>\n</sitemapindex>'))
    site=ROOT/'site-pages.xml';text=site.read_text()
    if BASE+'/spinhop/' not in text:site.write_text(text.replace('</urlset>',f'  <url><loc>{BASE}/spinhop/</loc></url>\n</urlset>'))
    (DATA/'pages.json').write_text(json.dumps(MANIFEST,indent=2)+'\n')
    print(f'Generated {len(MANIFEST)} pages: 4 hubs, 60 route guides, 40 timer pages, 25 noise guides and 21 compact indexes.')

if __name__=='__main__':main()
