#!/usr/bin/env python3
"""One header, footer and brand layer for every public page."""
from pathlib import Path
import re,html,json
ROOT=Path(__file__).resolve().parents[1]
STATIC={'photo-credits','index','services','market-research','overseas-sales','buyer-development','export-consulting','supply-chain','franchise-development'}
def esc(v):return html.escape(str(v),quote=True)
def local(base,lang):return './'+base+('-en' if lang=='en' and base in STATIC else '')+'.html'+('?lang=en' if lang=='en' and base not in STATIC else '')
def tagtext(ko,en,lang):return f'data-ko="{esc(ko)}" data-en="{esc(en)}">{esc(ko if lang=="ko" else en)}'
def header(lang,page):
 base=page.replace('-en','').replace('.html','');home=local('index',lang)
 menu=[('about','회사소개','Company',home+'#about'),('services','사업영역','Services',local('services',lang)),('products','소싱 품목','Sourcing',home+'#products'),('pricing','보고서·요금','Research & Pricing',local('pricing',lang)),('free-report','무료 사전진단','Free Check',local('free-report',lang))]
 def links(mobile=False):
  out=[]
  for key,ko,en,url in menu:
   legacy=(' id="linkHome"' if key=='about' else ' id="linkPricing"' if key=='pricing' else '') if not mobile and base=='free-report' else ''
   cur=' aria-current="page"' if base==key or key=='services' and base in STATIC-{'index'} else ''
   out.append(f'<a href="{url}" data-shell-link="{key}"{legacy}{cur} {tagtext(ko,en,lang)}</a>')
  return ''.join(out)
 old=''
 if base=='free-report':old='<button id="toggleLang" type="button" hidden>EN</button>'
 if base=='quick-report':old='<button id="lang" type="button" hidden>EN</button>'
 if base in {'pricing','privacy'}:old='<span hidden><button type="button" data-lang="ko">KR</button><button type="button" data-lang="en">EN</button></span>'
 return f'''<header class="y2c-header" data-shell-page="{base}"><div class="y2c-nav-container"><a class="y2c-brand" href="{home}" aria-label="Y2C HOLDINGS"><img src="./assets/y2c-logo.png" width="31" height="36" alt="Y2C HOLDINGS"><span>Y2C HOLDINGS</span></a><nav class="y2c-desktop-nav" aria-label="Main navigation">{links()}</nav><div class="y2c-nav-tools"><div class="y2c-language" aria-label="Language"><a href="{local(base,'ko')}" data-shell-lang="ko" {'aria-current="true"' if lang=='ko' else ''}>KR</a><span aria-hidden="true">/</span><a href="{local(base,'en')}" data-shell-lang="en" {'aria-current="true"' if lang=='en' else ''}>EN</a></div><a class="y2c-nav-contact" href="{home}#contact" data-shell-link="contact" {tagtext('문의하기','Contact',lang)}</a><button id="menuBtn" class="y2c-menu-button" type="button" aria-controls="mobileNav" aria-expanded="false" aria-label="{'메뉴 열기' if lang=='ko' else 'Open menu'}"><span></span><span></span></button></div></div><nav id="mobileNav" class="y2c-mobile-nav" aria-label="Mobile navigation" hidden>{links(True)}<a href="{home}#contact" data-shell-link="contact" {tagtext('문의하기','Contact',lang)}</a></nav>{old}</header>'''
def footer(lang):
 home=local('index',lang)
 ko='사진은 업무·품목 이해를 위한 외부 참고자료입니다. Y2C 소유 시설·고객·실제 납품상품 또는 확정 제품 성능을 뜻하지 않습니다.'
 en='Stock photographs illustrate categories and application contexts; they do not represent Y2C premises, clients, supplied products or verified product performance.'
 return f'''<footer class="y2c-footer"><div class="y2c-footer-container"><div class="y2c-footer-top"><a class="y2c-brand" href="{home}"><img src="./assets/y2c-logo.png" width="28" height="33" alt="Y2C HOLDINGS"><span>Y2C HOLDINGS</span></a><nav aria-label="Footer"><a href="{local('services',lang)}" data-shell-link="services" {tagtext('사업영역','Services',lang)}</a><a href="{local('pricing',lang)}" data-shell-link="pricing" {tagtext('보고서·요금','Research & Pricing',lang)}</a><a href="{local('privacy',lang)}" {tagtext('개인정보 안내','Privacy',lang)}</a><a href="{local('photo-credits',lang)}" {tagtext('사진 출처','Photo credits',lang)}</a><a href="./admin.html" {tagtext('관리자','Admin',lang)}</a></nav></div><p class="y2c-visual-note" {tagtext(ko,en,lang)}</p><div class="y2c-footer-bottom"><span {tagtext('주식회사 와이투씨홀딩스 · 부산, 대한민국','Y2C HOLDINGS CO., LTD. · BUSAN, KOREA',lang)}</span><span>© <span id="copyrightYear">2026</span> Y2C HOLDINGS</span></div></div></footer>'''
def apply_page(path):
 path=Path(path);src=path.read_text(encoding='utf-8');lang='en' if '-en.html' in path.name else 'ko'
 base=path.stem.replace('-en','')
 src=re.sub(r'<body\b([^>]*)>',lambda m:'<body'+re.sub(r'\sdata-page=[\"\'][^\"\']*[\"\']','',m.group(1))+' data-page=\"'+base+'\">',src,count=1)
 src=re.sub(r'<link[^>]+(?:href=[\"\'][^\"\']*assets/brand\.css[^>]*|href=\"unused\")[^>]*>','',src)
 src=re.sub(r'<link\b[^>]*href=[\"\']https://fonts\.googleapis\.com/css[^>]*>','',src,flags=re.I)
 fonts='<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&amp;family=Noto+Sans+KR:wght@400;500;600;700&amp;display=swap">'
 src=src.replace('</head>',fonts+'</head>')
 src=re.sub(r'(assets/(?:theme\.css|site-shell\.js)\?v=)\d+',r'\g<1>22',src)
 if path.name=='admin.html':
  datafile=ROOT/'site/data/site-data.json'
  if datafile.exists():
   data=json.loads(datafile.read_text())
   src=re.sub(r'<datalist id="industrySuggestions">.*?</datalist>','',src,flags=re.S)
   src=re.sub(r'(<input\b[^>]*name="industry")([^>]*>)',lambda m:m[1]+re.sub(r' list="[^"]*"','',m[2])[:-1].rstrip().rstrip('/').rstrip()+' list="industrySuggestions">',src)
   src=src.replace('placeholder="Automotive / Franchise"','placeholder="산업 분야 선택 또는 직접 입력"')
   suggestions='<datalist id="industrySuggestions">'+''.join('<option value="'+esc(o['label_ko'])+'">'+esc(o['label_en'])+'</option>' for o in data['industries'])+'</datalist>'
   src=src.replace('</body>',suggestions+'</body>')
 if path.name!='admin.html':
  src=re.sub(r'<header\b[^>]*>.*?</header>',lambda _:header(lang,path.name),src,count=1,flags=re.S|re.I)
  if '<footer' not in src:src=src.replace('</body>',footer(lang)+'</body>')
  src=re.sub(r'<footer\b[^>]*>.*?</footer>',lambda _:footer(lang),src,count=1,flags=re.S|re.I)
 if 'assets/theme.css' not in src:src=src.replace('</head>','<link rel="stylesheet" href="./assets/theme.css?v=22"><script defer src="./assets/site-shell.js?v=22"></script></head>')
 path.write_text(src,encoding='utf-8')
def apply_all():
 for p in (ROOT/'site').glob('*.html'):apply_page(p)
if __name__=='__main__':apply_all();print('Shared V22 theme/header/footer applied')
