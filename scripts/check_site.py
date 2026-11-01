#!/usr/bin/env python3
"""Fail deployment if critical website files or fields are broken."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
for name in ['site/index.html','site/privacy.html','site/assets/styles.css','site/assets/app.js','site/data/site-data.json','data/website_content.xlsx','.github/workflows/main.yml']:
    path=root/name
    assert path.is_file() and path.stat().st_size>0, f'Missing or empty: {name}'
obj=json.loads((root/'site/data/site-data.json').read_text(encoding='utf-8'))
assert obj['schema_version']==1
assert len(obj['services'])>=2 and len(obj['partners'])>=4 and len(obj['products'])>=3
assert all(p.get('sku') for p in obj['products'])
assert all(p.get('question_ko') and p.get('question_en') for p in obj['faq'])
assert 'contact_email' in obj['settings']
assert 'form_endpoint' in obj['settings']
html=(root/'site/index.html').read_text(encoding='utf-8')
for name in ['servicesGrid','stepsGrid','partnersGrid','contactForm','menuBtn']:
    assert f'id="{name}"' in html, f'Missing HTML mount point: {name}'
assert 'data-lang="ko"' in html and 'data-lang="en"' in html
assert (root/'site/assets/y2c-logo.png').exists()
print('OK: site content and expected assets present, public data valid.')
