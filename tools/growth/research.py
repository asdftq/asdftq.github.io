#!/usr/bin/env python3
"""Refresh public Apple evidence and US search ranks; no credentials or telemetry."""
import argparse
import csv
import datetime as dt
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'tools/growth/data'
REPORTS = ROOT / 'docs/app-growth'

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'asdftq-public-listing-check/1.0'})
    with urllib.request.urlopen(req, timeout=35) as response:
        return response.read()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', default=dt.date.today().isoformat())
    parser.add_argument('--listings-only', action='store_true')
    args = parser.parse_args()
    out = REPORTS / args.date / 'evidence'
    out.mkdir(parents=True, exist_ok=True)
    apps = {'timerbar': 6744717499, 'jet-lag-bye': 6747702706,
            'quietsense': 6771237461, 'spinhop': 6809077488}
    listing = json.loads(fetch('https://itunes.apple.com/lookup?' + urllib.parse.urlencode({
        'id': ','.join(map(str, apps.values())), 'country': 'us'})))
    (out / 'apple-lookup.json').write_text(json.dumps(listing, indent=2))
    for slug, app_id in apps.items():
        app = next(x for x in listing['results'] if x['trackId'] == app_id)
        folder = out / slug
        folder.mkdir(exist_ok=True)
        url = app['trackViewUrl'].split('?')[0]
        try:
            (folder / 'public-listing.html').write_bytes(fetch(url))
        except Exception as error:
            (folder / 'public-listing-error.txt').write_text(str(error))
        (folder / 'listing.json').write_text(json.dumps(app, indent=2))
        print(slug, app['version'], app.get('userRatingCount'), url, flush=True)
    if args.listings_only:
        return
    rows = list(csv.DictReader((DATA / 'keywords.csv').open()))
    history = REPORTS / 'rank-history.csv'
    fields = ['date', 'app', 'app_id', 'keyword', 'rank', 'baseline_2026_10_24', 'status', 'result_count']
    existing = list(csv.DictReader(history.open())) if history.exists() else []
    # Re-running a day replaces that day's observations; unavailable is never rank zero.
    existing = [r for r in existing if r['date'] != args.date]
    snapshots = {}
    for row in rows:
        keyword = row['keyword']
        result = {'date': args.date, 'app': row['app'], 'app_id': row['app_id'],
                  'keyword': keyword, 'baseline_2026_10_24': row['rank_2026-10-24']}
        try:
            if keyword not in snapshots:
                url = 'https://itunes.apple.com/search?' + urllib.parse.urlencode({
                    'term': keyword, 'entity': 'software', 'country': 'us', 'limit': 50})
                snapshots[keyword] = json.loads(fetch(url))
                slug = keyword.replace(' ', '-')
                (out / f'search-{slug}.json').write_text(json.dumps(snapshots[keyword], indent=2))
                time.sleep(3.1)  # Respect the public Search API's published approximate rate limit.
            found = snapshots[keyword]['results'][:50]
            rank = next((i for i, x in enumerate(found, 1) if str(x.get('trackId')) == row['app_id']), 0)
            result.update(rank=rank, status='ok', result_count=len(found))
        except Exception as error:
            result.update(rank='', status=f'unavailable: {error}', result_count='')
        existing.append(result)
        with history.open('w') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(existing)
        print(keyword, result.get('rank'), result['status'], flush=True)
    lines = [f'# Weekly observation — {args.date}', '',
             'US public iTunes Search API, first 50 results. Rank 0 means absent from the returned first 50; blank means unavailable. This is not a personalized on-device App Store search measurement.', '',
             '| App | Keyword | Rank | Oct 24 baseline | Status |', '|---|---|---:|---:|---|']
    for row in existing:
        if row['date'] == args.date:
            lines.append(f"| {row['app']} | {row['keyword']} | {row['rank']} | {row['baseline_2026_10_24']} | {row['status']} |")
    lines += ['', 'Search Console impressions/clicks, GA4 funnel events, installs, purchases and revenue have not been observed by this script. A sitemap entry is not proof of indexing. UTM links are attribution labels, not click counts.', '',
              'Decision dates (from 2026-10-26): day 30 = 2026-11-25; day 60 = 2026-12-25; day 90 = 2027-01-24. See each app’s success/stop criteria in its report. Do not expand SpinHop beyond one demo without evidence.']
    (REPORTS / args.date / 'weekly-report.md').write_text('\n'.join(lines) + '\n')

if __name__ == '__main__':
    main()
