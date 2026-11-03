#!/usr/bin/env python3
"""Generate photographer attribution and a category-to-subject review page."""
from pathlib import Path
import html
from photo_library import SITE,ROOT,records,image_html
from site_shell import apply_page

def esc(v):return html.escape(str(v),quote=True)
def build():
    for lang in ('ko','en'):
        t=lambda ko,en: ko if lang=='ko' else en
        cards=[]
        for p in records():
            title=p['category_ko'] if lang=='ko' else p['key']
            cards.append(f'''<figure data-photo-card="{esc(p['key'])}">{image_html(p['key'],lang)}<figcaption><h2>{esc(title)}</h2><p>{esc(p['subject_'+lang])}<br>{esc(p['author'])} / {esc(p['provider'])}</p><a href="{esc(p['source_url'])}" target="_blank" rel="noopener noreferrer">{t('촬영 원본 페이지','Original photo page')}</a><a href="{esc(p['license_url'])}" target="_blank" rel="noopener noreferrer">{t('이용 조건','License')}</a></figcaption></figure>''')
        page=f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{t('사진 출처','Photo credits')} | Y2C HOLDINGS</title><meta name="description" content="Y2C HOLDINGS website photo sources and category mapping."><meta name="robots" content="noindex,follow"><link rel="icon" href="./assets/favicon.png"><link rel="stylesheet" href="./assets/seo.css"></head><body><header></header><main id="main" class="section"><div class="container"><span class="section-label">PHOTOGRAPHY / CATEGORY REFERENCES</span><h1>{t('사진 출처와 사용 범위','Photography sources and context')}</h1><p class="credit-intro">{t('업무와 제품을 설명하기 위해 선정한 외부 사진자료입니다. 실제 Y2C 사업장·직원·고객·납품상품으로 오인하지 않도록 참고 사진으로 사용합니다. 사진 속 상표의 공급권이나 제휴 관계를 주장하지 않습니다. 차량용 매트의 재질·방향제 성분·유리 필름의 실제 부착 여부와 성능은 사진으로 확인되지 않습니다.','Selected stock photographs illustrate work categories and product contexts. They do not represent Y2C premises, employees, clients or confirmed supplies. Brand partnerships, mat materials, fragrance ingredients and window-film installation or performance are not inferred from these images.')}</p><div class="photo-credit-grid">{''.join(cards)}</div></div></main></body></html>'''
        path=SITE/('photo-credits-en.html' if lang=='en' else 'photo-credits.html')
        path.write_text(page,encoding='utf-8');apply_page(path)
    # Standalone source review: browser with internet loads originals, no local download claim.
    review='''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Y2C V22 사진 원본·카테고리 대조</title><style>body{margin:0;background:#f6f3ee;color:#242424;font-family:Arial,'Malgun Gothic',sans-serif;padding:40px}main{max-width:1200px;margin:auto}h1{font-size:30px}p{line-height:1.8}.note{padding:20px;background:#fff;border-left:3px solid #b79550}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:30px}figure{margin:0;background:white;padding:16px}img{width:100%;height:230px;object-fit:contain;background:#ece8e1}figcaption{font-size:13px;line-height:1.8}h2{font-size:19px}a{color:#725821}@media(max-width:800px){body{padding:20px}.grid{grid-template-columns:1fr}}</style></head><body><main><h1>Y2C V22 — 사진 원본·카테고리 대조표</h1><p class="note">인터넷 연결 상태에서 원본 사진을 불러옵니다. 이것은 최종 사이트 스크린샷이 아니라 사진 선별 대조표입니다. 실제 사이트에서는 명시한 주제에 맞춰 프레임을 정리합니다. GitHub 자동 배포는 사진을 다운로드·검증한 뒤 로컬 WebP로 포함합니다.</p><div class="grid">'''
    for p in records():
        preview=p.get('preview_url',p['download_url'])
        review+=f'<figure><img src="{esc(preview)}" alt="{esc(p["alt_ko"])}" loading="lazy" referrerpolicy="no-referrer"><figcaption><h2>{esc(p["category_ko"])}</h2><b>{esc(p["subject_ko"])}</b><p>{esc(p["review_note"])}</p><p>{esc(p["author"])} · {esc(p["provider"])}</p><a href="{esc(p["source_url"])}" target="_blank" rel="noopener noreferrer">원본 확인</a> / <a href="{esc(p["license_url"])}" target="_blank" rel="noopener noreferrer">사용 조건</a></figcaption></figure>'
    (ROOT/'PHOTO_REVIEW.html').write_text(review+'</div></main></body></html>',encoding='utf-8')
    print('Generated photo credits (KR/EN) and source review')
if __name__=='__main__':build()
