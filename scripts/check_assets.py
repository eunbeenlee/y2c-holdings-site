#!/usr/bin/env python3
"""Offline validation: local assets, links, image mapping, and public release hygiene."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re,sys,os
from photo_library import by_key,resolved_url
ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'site'
class Page(HTMLParser):
 def __init__(self):super().__init__();self.refs=[];self.ids=set();self.images=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.add(a['id'])
  if tag=='img':self.images.append(a)
  key='href' if tag in ('a','link') else 'src' if tag in ('script','img','source','iframe') else None
  if key and a.get(key):self.refs.append((tag,a[key]))
pages={}
for p in SITE.glob('*.html'):
 parser=Page();parser.feed(p.read_text(encoding='utf-8'));pages[p.resolve()]=parser
errors=[];links=0
for path,page in pages.items():
 for tag,url in page.refs:
  u=urlsplit(url)
  if u.scheme or u.netloc or url.startswith('//'):continue
  dest=((SITE/u.path.lstrip('/')) if u.path.startswith('/') else path.parent/unquote(u.path)).resolve() if u.path else path
  if dest.is_dir():dest=dest/'index.html'
  if not dest.is_relative_to(SITE.resolve()):errors.append(f'{path.name}: outside site: {url}');continue
  if not dest.exists():errors.append(f'{path.name}: missing {tag}: {url}');continue
  if u.fragment and dest in pages and unquote(u.fragment) not in pages[dest].ids:errors.append(f'{path.name}: anchor not found: {url}')
  links+=1
 for i in page.images:
  if 'alt' not in i:errors.append(f'{path.name}: missing alt: {i.get("src")}')
for css in (SITE/'assets').glob('*.css'):
 for url in re.findall(r'url\(\s*[\'\"]?([^\'\"\)]+)',css.read_text()):
  if urlsplit(url).scheme or url.startswith('//') or url.startswith('#'):continue
  p=(css.parent/unquote(urlsplit(url).path)).resolve()
  if not p.exists():errors.append(f'{css.name}: missing CSS resource {url}')
data=json.loads((SITE/'data/site-data.json').read_text())
visuals=data.get('visuals',{})
for key,v in visuals.items():
 p=SITE/v['src']
 if key not in by_key():errors.append(f'Image map {key}: source not registered')
 if os.environ.get('Y2C_REQUIRE_LOCAL_PHOTOS')=='1' and not resolved_url(key)[1]:errors.append(f'Image map {key}: local photograph not acquired')
 if not all(v.get(x) for x in ('alt_ko','alt_en')):errors.append(f'Image map {key}: missing bilingual alt')
photos=[x['src'] for x in visuals.values()]
if len(photos)!=len(set(photos)):errors.append('Image map contains duplicate asset assignment')
for p in ROOT.rglob('*'):
 if p.is_file() and p.suffix.lower() in ('.woff','.woff2','.ttf','.otf','.ttc'):errors.append(f'Font file must not be in release: {p}')
config=(SITE/'assets/supabase-config.js').read_text()
if re.search(r'sb_secret_[A-Za-z0-9_]{10,}',config):errors.append('Secret key found in public config')
if '/rest/v1' in config:errors.append('Config must use Supabase base URL, not REST endpoint')
if errors:
 print('\n'.join(errors));sys.exit(1)
print(f'OK: {len(pages)} HTML pages, {links} local references, {len(visuals)} unique photo assignments; no missing code files or anchors. Local image verification is enforced when Y2C_REQUIRE_LOCAL_PHOTOS=1.')
