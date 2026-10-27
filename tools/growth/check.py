#!/usr/bin/env python3
"""Check generated HTML, assets, citations and sitemap ownership, locally or over HTTP."""
import argparse
import concurrent.futures
import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
class Page(HTMLParser):
    def __init__(self):super().__init__();self.tags=[];self.scripts=[];self.in_json=False
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs);self.tags.append((tag,attrs))
        self.in_json=tag=='script' and attrs.get('type')=='application/ld+json'
    def handle_endtag(self,tag):
        if tag=='script':self.in_json=False
    def handle_data(self,data):
        if self.in_json:self.scripts.append(json.loads(data))

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--base');args=parser.parse_args()
    rows=json.loads((ROOT/'tools/growth/data/pages.json').read_text());base=(args.base or '').rstrip('/')
    sources={x['slug']:x['source_url'] for x in __import__('csv').DictReader((ROOT/'tools/growth/data/cities.csv').open())}
    failures=[];titles=set()
    def load(path):
        if base:
            with urllib.request.urlopen(base+path,timeout=30) as r:
                assert r.status==200,f'{path}: HTTP {r.status}'
                return r.read().decode()
        return (ROOT/path.strip('/')/'index.html').read_text()
    def check(row):
        path=row['path'];source=load(path);page=Page();page.feed(source)
        def tags(name):return [a for t,a in page.tags if t==name]
        title=re.search('<title>(.*?)</title>',source).group(1)
        assert title==row['title'].replace('&','&amp;'),f'{path}: wrong title: {title}'
        assert len(tags('h1'))==1,f'{path}: expected one primary heading'
        assert [a['href'] for a in tags('link') if a.get('rel')=='canonical']==['https://www.asdftq.com'+path],f'{path}: canonical'
        assert any(a.get('name')=='description' and a.get('content') for a in tags('meta')),f'{path}: description'
        assert page.scripts,f'{path}: no schema'
        assert all(s.get('@context')=='https://schema.org' for s in page.scripts),f'{path}: schema context'
        scripts=[a['src'] for a in tags('script') if 'src' in a]
        assert scripts.count('/analytics.js')==1,f'{path}: analytics script'
        assert '/analytics.css' in [a.get('href') for a in tags('link')],f'{path}: consent style'
        assert 'data-analytics-settings' in source and 'href="/privacy.html"' in source,f'{path}: privacy controls'
        assert 'googletagmanager.com' not in source,f'{path}: direct Google tag'
        for script in row['scripts']:assert script in scripts,f'{path}: missing script {script}'
        app_links=[a['href'] for a in tags('a') if 'apps.apple.com/app/id' in a.get('href','')]
        if row['kind']!='index':assert app_links,f'{path}: missing store CTA'
        for href in app_links:
            query=urllib.parse.parse_qs(urllib.parse.urlsplit(href).query)
            assert query.get('utm_source')==['asdftq'] and query.get('utm_campaign')==[row['slug']] and query.get('utm_medium') and query.get('utm_content'),f'{path}: incomplete attribution'
        for tag in tags('img'):
            asset=tag.get('src','')
            if asset.startswith('/'):assert (ROOT/asset.lstrip('/')).is_file(),f'{path}: missing {asset}'
        if row['slug']=='quietsense':
            assert 'not certified' in source or 'not a certified' in source,f'{path}: missing accuracy limits'
            if '/cities/' in path:
                city=path.strip('/').split('/')[-1]
                assert sources[city] in source and 'checked 2026-10-26' in source,f'{path}: missing dated official citation'
        if '/timers/' in path:assert 'data-timer' in source and 'data-start' in source,f'{path}: timer component'
        for a in tags('a'):
            href=a.get('href','');url=urllib.parse.urlsplit(href)
            if url.netloc not in ('','www.asdftq.com'):continue
            if not url.path.startswith('/'):continue
            local=ROOT/url.path.lstrip('/')
            assert local.exists(),f'{path}: broken internal link {href}'
        return title
    with concurrent.futures.ThreadPoolExecutor(max_workers=6 if base else 1) as pool:
        for row,result in zip(rows,pool.map(lambda row: attempt(row,check),rows)):
            if isinstance(result,Exception):failures.append(str(result))
            elif result in titles:failures.append('Duplicate title: '+result)
            else:titles.add(result)
    ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'};ownership={}
    for child in ['site-pages.xml','install-worthy/sitemap.xml','nobadge/sitemap.xml','guides-sitemap.xml']:
        for loc in ET.parse(ROOT/child).findall('s:url/s:loc',ns):
            if loc.text in ownership:failures.append(f'Duplicate sitemap URL {loc.text}')
            ownership[loc.text]=child
    for row in rows:
        if 'https://www.asdftq.com'+row['path'] not in ownership:failures.append('Missing sitemap URL '+row['path'])
    if failures:raise SystemExit('\n'.join(failures))
    print(f'PASS: {len(rows)} pages ({"HTTP 200 + " if base else "local "}unique titles, canonical URLs, schema, CTAs, assets, citations and sitemap ownership).')
def attempt(row,check):
    try:return check(row)
    except Exception as e:return AssertionError(row['path']+': '+str(e))
if __name__=='__main__':main()
