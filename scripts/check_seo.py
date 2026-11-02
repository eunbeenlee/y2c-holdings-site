#!/usr/bin/env python3
"""Check indexable page metadata, policy and sitemap without any external service."""
from pathlib import Path
import re, sys, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]/'site'
NS={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
root=ET.fromstring((ROOT/'sitemap.xml').read_bytes())
urls=[e.find('s:loc',NS).text for e in root.findall('s:url',NS)]
assert len(urls)==len(set(urls)) and len(urls)>=18
assert all(u.startswith('https://y2choldings.co.kr/') for u in urls)
for u in urls:
    name=u.removeprefix('https://y2choldings.co.kr/') or 'index.html'
    path=ROOT/name
    assert path.exists(),f'Sitemap page missing: {name}'
    txt=path.read_text(encoding='utf8')
    assert '<title>' in txt and 'name="description"' in txt, name
    assert 'rel="canonical"' in txt and u in txt, f'Missing canonical: {name}'
    assert 'noindex' not in txt, f'Incorrect noindex on {name}'
    assert len(re.findall(r'<h1(?:\s|>)',txt))==1, f'Expected exactly one H1: {name}'
    if name.endswith('-en.html'):
        assert '<html lang="en"' in txt,name
    if name not in ('index.html','pricing.html','free-report.html','quick-report.html'):
        assert 'hreflang="ko"' in txt and 'hreflang="en"' in txt
assert '/admin.html' not in urls
admin=(ROOT/'admin.html').read_text(encoding='utf8')
assert 'noindex' in admin
robots=(ROOT/'robots.txt').read_text(encoding='utf8')
assert 'Sitemap: https://y2choldings.co.kr/sitemap.xml' in robots
assert 'Disallow: /admin.html' in robots
print(f'OK: {len(urls)} public URL(s) with canonical/meta + sitemap; admin excluded')
