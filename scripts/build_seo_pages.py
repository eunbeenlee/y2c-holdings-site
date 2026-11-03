#!/usr/bin/env python3
"""Generate fully crawlable SEO service pages and sitemap from PUBLIC Excel content.
No registrations, API calls or paid dependencies required.
"""
import argparse, html, json, re
from pathlib import Path
from xml.etree import ElementTree as ET
from build_site_data import read_excel, MAP, visible, build as load_public

VISUALS = {}

DOMAIN = 'https://y2choldings.co.kr'
HEADINGS = {
 'ko': {'home':'홈','services':'서비스','pricing':'요금 안내','free':'무료 진단','contact':'문의하기','what':'지원 업무','outputs':'산출물','steps':'진행 절차','faq':'자주 묻는 질문','caution':'안내사항','disclaimer':'사업·인증·수출 성과를 보장하지 않습니다. 확정 견적과 실행 범위는 개별 계약에 따라 정해지며, 법률·통관·세무 판단은 해당 전문가 확인이 필요할 수 있습니다.','cta':'프로젝트 상담하기','explore':'다른 서비스 보기','all':'전체 서비스','bottom':'Y2C가 수행할 수 있는 업무 범위를 명확하게 협의합니다.'},
 'en': {'home':'Home','services':'Services','pricing':'Pricing','free':'Free check','contact':'Contact','what':'Service scope','outputs':'Deliverables','steps':'Process','faq':'Frequently asked','caution':'Important note','disclaimer':'Outcomes, permits and export contracts are not guaranteed. Final scope and pricing depend on written agreements. Specialist advice may be needed for legal, customs and tax determinations.','cta':'Discuss your project','explore':'Explore other services','all':'All services','bottom':'Define the work clearly, then build a practical plan.'}
}

def h(x): return html.escape(str(x or ''),quote=True)
def bullet_items(value): return [s.strip() for s in str(value).split('|') if s.strip()]
def url(slug, lang): return f'{DOMAIN}/{slug}{"-en" if lang == "en" else ""}.html'
def li(value): return ''.join(f'<li>{h(item)}</li>' for item in bullet_items(value))

def make_head(title, meta, canonical, alternate, locale, schema, desc_short):
    slug=canonical.rsplit('/',1)[-1].replace('-en.html','.html').removesuffix('.html') or 'hub'
    photo=SERVICE_PHOTOS.get(slug,'hero-operations.webp')
    return f'''<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="index,follow,max-image-preview:large">
<title>{h(title)} | Y2C HOLDINGS</title><meta name="description" content="{h(meta)}">
<link rel="canonical" href="{h(canonical)}">
<link rel="alternate" hreflang="ko" href="{h(alternate['ko'])}">
<link rel="alternate" hreflang="en" href="{h(alternate['en'])}">
<meta property="og:site_name" content="Y2C HOLDINGS"><meta property="og:type" content="website">
<meta property="og:title" content="{h(title)} | Y2C HOLDINGS"><meta property="og:description" content="{h(meta)}">
<meta property="og:url" content="{h(canonical)}"><meta property="og:image" content="{DOMAIN}/assets/images/{photo}"><meta property="og:locale" content="{'ko_KR' if locale=='ko' else 'en_US'}">
<meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#f7f6f2">
<link rel="icon" href="./assets/favicon.png"><link rel="stylesheet" href="./assets/seo.css"><link rel="stylesheet" href="./assets/brand.css"><script defer src="./assets/brand.js"></script>
<script type="application/ld+json">{json.dumps(schema,ensure_ascii=False).replace('<','\\u003c')}</script>'''

def nav(lang, slug='', home=False):
    d=HEADINGS[lang]
    current = f'./{slug}{"-en" if lang=="en" else ""}.html' if slug else f'./services{"-en" if lang=="en" else ""}.html'
    ko = f'./{slug}.html' if slug else './services.html'
    en = f'./{slug}-en.html' if slug else './services-en.html'
    return f'''<header class="seo-top"><div class="seo-wrap seo-nav"><a class="seo-brand" href="./index{'-en' if lang=='en' else ''}.html" aria-label="Y2C HOLDINGS"><img src="./assets/y2c-logo.png" width="31" height="36" alt="Y2C Logo"><span><b>Y2C HOLDINGS</b><small>GLOBAL BUSINESS SERVICES</small></span></a><nav aria-label="Main navigation"><a href="./index{'-en' if lang=='en' else ''}.html">{h(d['home'])}</a><a href="./services{('-en' if lang=='en' else '')}.html">{h(d['services'])}</a><a href="./pricing.html{'?lang=en' if lang=='en' else ''}">{h(d['pricing'])}</a><a href="./free-report.html{'?lang=en' if lang=='en' else ''}">{h(d['free'])}</a></nav><div class="seo-langs" aria-label="Languages"><a href="{ko}" {'aria-current="page"' if lang=='ko' else ''} lang="ko">KR</a><a href="{en}" {'aria-current="page"' if lang=='en' else ''} lang="en">EN</a></div></div></header>'''

def footer(lang):
    d=HEADINGS[lang]
    return f'''<footer class="seo-footer"><div class="seo-wrap"><div><strong>Y2C HOLDINGS</strong><p>{h(d['bottom'])}</p></div><div class="seo-footnav"><a href="./index{'-en' if lang=='en' else ''}.html">{h(d['home'])}</a><a href="./services{('-en' if lang=='en' else '')}.html">{h(d['all'])}</a><a href="./pricing.html{'?lang=en' if lang=='en' else ''}">{h(d['pricing'])}</a><a href="./privacy.html">Privacy</a></div><small>{"사진은 사업영역 설명을 위한 연출 이미지입니다." if lang=="ko" else "Images are illustrative, not actual Y2C engagement photographs."}</small><small>© 2026 Y2C HOLDINGS · BUSAN, KOREA</small></div></footer>'''

SERVICE_PHOTOS = {
    'overseas-sales':'service-sales.webp',
    'market-research':'service-analysis.webp',
    'buyer-development':'service-buyer.webp',
    'export-consulting':'service-export.webp',
    'supply-chain':'service-logistics.webp',
    'franchise-development':'service-franchise-field.webp',
}

def seo_photo(slug,lang):
    v=VISUALS.get(slug) or VISUALS.get('hero', {})
    filename=Path(v['src']).name if v else SERVICE_PHOTOS.get(slug,'hero-operations.webp')
    alt=v.get('alt_'+lang,'Illustrative business scene')
    return f'<img class="seo-hero-image" src="./assets/images/{filename}" alt="{alt}" width="1100" height="740" fetchpriority="high" decoding="async">'

def service_page(row, records, lang):
    d=HEADINGS[lang]; slug=row['slug']; title=row[f'title_{lang}']; meta=row[f'meta_{lang}']
    alternate={x:url(slug,x) for x in ['ko','en']}; canonical=alternate[lang]
    schema={'@context':'https://schema.org','@type':'Service','name':title,'description':meta,'url':canonical,'provider':{'@type':'Organization','name':'Y2C HOLDINGS','url':DOMAIN}}
    head=make_head(title,meta,canonical,alternate,lang,schema,meta)
    cross = ''.join(f'<a class="service-link" href="./{p["slug"]}{"-en" if lang=="en" else ""}.html"><small>{i+1:02d}</small><strong>{h(p[f"title_{lang}"])}</strong><span aria-hidden="true">↗</span></a>' for i,p in enumerate(records) if p['slug']!=slug)
    body=f'''<!doctype html><html lang="{lang}"><head>{head}</head><body><a class="skip" href="#main">Skip to content</a>{nav(lang,slug)}
<main id="main"><section class="seo-hero">{seo_photo(slug,lang)}<div class="seo-wrap"><div class="seo-overline">Y2C / BUSINESS SOLUTIONS / {int(row['sort']):02d}</div><h1>{h(title)}</h1><p>{h(row[f'intro_{lang}'])}</p><div class="seo-actions"><a class="seo-btn" href="./index{'-en' if lang=='en' else ''}.html#contact">{h(d['cta'])} ↗</a><a class="seo-textlink" href="./services{('-en' if lang=='en' else '')}.html">{h(d['explore'])} ↗</a></div></div></section>
<section class="seo-section"><div class="seo-wrap two-col"><div class="seo-aside"><span>01 / SERVICE SCOPE</span><h2>{h(d['what'])}</h2><p>{h(meta)}</p></div><ul class="seo-list">{li(row[f'scope_{lang}'])}</ul></div></section>
<section class="seo-section alternate"><div class="seo-wrap two-col"><div class="seo-aside"><span>02 / DELIVERABLES</span><h2>{h(d['outputs'])}</h2></div><ul class="seo-list">{li(row[f'deliverables_{lang}'])}</ul></div></section>
<section class="seo-section"><div class="seo-wrap"><div class="section-label">03 / PROCESS</div><h2>{h(d['steps'])}</h2><ol class="seo-steps">{''.join(f'<li><span>{i:02d}</span>{h(item)}</li>' for i,item in enumerate(bullet_items(row[f'process_{lang}']),1))}</ol></div></section>
<section class="seo-section alternate"><div class="seo-wrap faq-wrap"><div class="section-label">04 / Q&A</div><h2>{h(d['faq'])}</h2><h3>{h(row[f'question_{lang}'])}</h3><p>{h(row[f'answer_{lang}'])}</p><div class="seo-disclaimer"><strong>{h(d['caution'])}</strong><p>{h(d['disclaimer'])}</p></div></div></section>
<section class="seo-section"><div class="seo-wrap"><div class="section-label">05 / RELATED SERVICES</div><h2>{h(d['explore'])}</h2><div class="service-links">{cross}</div></div></section>
<section class="seo-cta"><div class="seo-wrap"><strong>{h(d['bottom'])}</strong><a href="./index{'-en' if lang=='en' else ''}.html#contact">{h(d['cta'])} ↗</a></div></section></main>{footer(lang)}</body></html>'''
    return body

def hub_page(records,lang):
    d=HEADINGS[lang]
    title='기업 해외영업·해외시장조사 서비스' if lang=='ko' else 'International Business Services'
    meta='Y2C HOLDINGS의 해외영업 대행, 해외시장조사, 바이어 발굴, 수출 컨설팅, 공급망 구축, 해외 프랜차이즈 사업개발 서비스 안내.' if lang=='ko' else 'Explore overseas sales, market research, buyer discovery, export consulting, international sourcing and franchise development services at Y2C.'
    alternate={'ko':DOMAIN+'/services.html','en':DOMAIN+'/services-en.html'}; canonical=alternate[lang]
    schema={'@context':'https://schema.org','@type':'CollectionPage','name':title,'description':meta,'url':canonical,'publisher':{'@type':'Organization','name':'Y2C HOLDINGS','url':DOMAIN}}
    cards=''.join(f'<a class="service-link" href="./{p["slug"]}{"-en" if lang=="en" else ""}.html"><small>{i:02d}</small><span><strong>{h(p[f"title_{lang}"])}</strong><em>{h(p[f"meta_{lang}"])}</em></span><span aria-hidden="true">↗</span></a>' for i,p in enumerate(records,1))
    return f'''<!doctype html><html lang="{lang}"><head>{make_head(title,meta,canonical,alternate,lang,schema,meta)}</head><body><a class="skip" href="#main">Skip to content</a>{nav(lang)}<main id="main"><section class="seo-hero service-hub">{seo_photo("hub",lang)}<div class="seo-wrap"><div class="seo-overline">Y2C / BUSINESS DEVELOPMENT</div><h1>{h(title)}</h1><p>{h(meta)}</p><div class="seo-actions"><a class="seo-btn" href="./index{'-en' if lang=='en' else ''}.html#contact">{h(d['cta'])} ↗</a><a class="seo-textlink" href="./free-report.html{'?lang=en' if lang=='en' else ''}">{h(d['free'])} ↗</a></div></div></section><section class="seo-section"><div class="seo-wrap"><div class="section-label">01 / OUR SERVICES</div><div class="service-links hub">{cards}</div></div></section><section class="seo-cta"><div class="seo-wrap"><strong>{h(d['bottom'])}</strong><a href="./pricing.html{'?lang=en' if lang=='en' else ''}">{h(d['pricing'])} ↗</a></div></section></main>{footer(lang)}</body></html>'''

def create_sitemap(site,records):
    slugs=['','index-en.html','services.html','services-en.html','pricing.html','free-report.html','quick-report.html']
    for row in records:
        slugs.extend([row['slug']+'.html',row['slug']+'-en.html'])
    ns='http://www.sitemaps.org/schemas/sitemap/0.9'
    ET.register_namespace('',ns)
    root=ET.Element(f'{{{ns}}}urlset')
    for slug in slugs:
        entry=ET.SubElement(root,f'{{{ns}}}url'); ET.SubElement(entry,f'{{{ns}}}loc').text=DOMAIN+('/'+slug if slug else '/')
    xml=ET.tostring(root,encoding='utf-8',xml_declaration=True)
    (site/'sitemap.xml').write_bytes(xml)
    (site/'robots.txt').write_text('User-agent: *\nAllow: /\nDisallow: /admin.html\nSitemap: '+DOMAIN+'/sitemap.xml\n',encoding='utf-8')

def build(excel, site):
    global VISUALS, SERVICE_PHOTOS
    VISUALS=load_public(excel).get('visuals',{})
    for slug in list(SERVICE_PHOTOS):
        if slug in VISUALS: SERVICE_PHOTOS[slug]=Path(VISUALS[slug]['src']).name
    book=read_excel(excel); headers=MAP['검색서비스']; records=[]; used=set()
    for rr in book['검색서비스'][1:]:
        row=dict(zip(headers,rr+['']*(len(headers)-len(rr))))
        if not visible(row['visible']): continue
        slug=str(row['slug']).strip().lower()
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',slug): raise ValueError('Invalid SEO slug: '+slug)
        if slug in used: raise ValueError('Duplicate slug '+slug)
        used.add(slug);row['slug']=slug
        for field in headers[1:-2]:
            if not str(row[field]).strip(): raise ValueError('Missing SEO content: '+slug+' '+field)
        row['sort']=int(row['sort'] or 999)
        records.append(row)
    records.sort(key=lambda x:x['sort'])
    if len(records)<4: raise ValueError('Expected >=4 published service pages')
    for row in records:
        for lang in ['ko','en']:
            path=site/(row['slug']+('-en' if lang=='en' else '')+'.html')
            path.write_text(service_page(row,records,lang),encoding='utf8')
    for lang in ['ko','en']:
        path=site/('services'+('-en' if lang=='en' else '')+'.html')
        path.write_text(hub_page(records,lang),encoding='utf8')
    create_sitemap(site,records)
    print(f'Created {len(records)*2+2} indexable service pages and sitemap.xml (no external API)')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--excel',default='data/website_content.xlsx');parser.add_argument('--site',default='site');args=parser.parse_args()
    build(Path(args.excel),Path(args.site))
