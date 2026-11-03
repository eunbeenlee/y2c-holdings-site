"""V22 photo registry and one rendering path used by every category page."""
from __future__ import annotations
import html, json
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'site'
MANIFEST=ROOT/'data/photo_sources.json'

def records():
    data=json.loads(MANIFEST.read_text(encoding='utf-8'))['photos']
    keys,ids,files=set(),set(),set()
    for p in data:
        for field,seen in [('key',keys),('photo_id',ids),('file',files)]:
            if p[field] in seen: raise ValueError('Duplicate photo '+field+': '+p[field])
            seen.add(p[field])
        if Path(p['file']).name!=p['file'] or not p['file'].endswith('.webp'): raise ValueError('Unsafe photo file')
        if p['kind'] not in {'hero','service','product'}: raise ValueError('Invalid photo kind')
        if not all(0<=v<=1 for v in p['crop']) or p['crop'][0]>=p['crop'][2] or p['crop'][1]>=p['crop'][3]: raise ValueError('Invalid crop '+p['key'])
        if not all(p.get(k) for k in ['author','source_url','license_url','subject_ko','subject_en','alt_ko','alt_en','review_note']): raise ValueError('Incomplete photo metadata')
        for u in [p['download_url'],p['source_url'],p['license_url'],p.get('preview_url',p['download_url'])]:
            parsed=urlparse(u)
            if parsed.scheme!='https' or parsed.hostname not in {'www.pexels.com','images.pexels.com','unsplash.com','images.unsplash.com'}: raise ValueError('Photo URL not allowed')
    return data

def by_key(): return {p['key']:p for p in records()}

def image_path(key): return 'assets/images/'+by_key()[key]['file']

def resolved_url(key):
    p=by_key()[key]
    local=SITE/'assets/images'/p['file']
    # Only a successful acquisition receipt makes a local image production-ready.
    receipt=SITE/'data/photo-build.json'
    approved={}
    if receipt.exists(): approved={r['key']:r for r in json.loads(receipt.read_text())['photos']}
    if local.exists() and approved.get(key,{}).get('photo_id')==p['photo_id']:
        return './assets/images/'+p['file'], True
    return p.get('preview_url',p['download_url']), False

def image_html(key,lang='ko',css='',eager=False):
    p=by_key()[key];src,local=resolved_url(key)
    w,h=p['target'];alt=html.escape(p['alt_'+lang],quote=True)
    position='50% 50%' if local else p['position']
    cls=html.escape(css,quote=True)
    return (f'<img class="{cls}" src="{html.escape(src,quote=True)}" alt="{alt}" '
            f'data-photo-key="{html.escape(key,quote=True)}" data-asset-path="{image_path(key)}" '
            f'width="{w}" height="{h}" style="object-position:{position}" '
            f'loading="{"eager" if eager else "lazy"}" decoding="async" referrerpolicy="no-referrer"'
            +(' fetchpriority="high"' if eager else '')+'>')

def card_caption(key,lang='ko'):
    p=by_key()[key]
    return p['subject_'+lang]
