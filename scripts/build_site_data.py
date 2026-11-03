#!/usr/bin/env python3
"""Build PUBLIC Y2C website content from a public-only Excel workbook.

No third-party dependencies: supports standard OOXML `.xlsx` shared/inline strings.
Do not feed the private Y2C management workbook to this script.
"""
import argparse
import json
import posixpath
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

N = {'x': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
     'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
     'pr': 'http://schemas.openxmlformats.org/package/2006/relationships'}
MAP = {
    '설정': ['key', 'ko', 'en'],
    '서비스': ['id', 'sector', 'icon', 'title_ko', 'title_en', 'description_ko', 'description_en', 'sort', 'visible'],
    '상품': ['sku', 'category', 'market', 'name_ko', 'name_en', 'description_ko', 'description_en', 'tariff_ko', 'tariff_en', 'hs_candidate', 'verification', 'source_url', 'sort', 'visible'],
    '파트너': ['id', 'symbol', 'title_ko', 'title_en', 'description_ko', 'description_en', 'sort', 'visible'],
    '진행절차': ['step', 'title_ko', 'title_en', 'description_ko', 'description_en', 'visible'],
    'FAQ': ['id', 'question_ko', 'question_en', 'answer_ko', 'answer_en', 'sort', 'visible'],
    '지원프로그램': ['id', 'title_ko', 'title_en', 'description_ko', 'description_en', 'official_url', 'status_ko', 'status_en', 'sort', 'visible'],
    '인사이트': ['id', 'label_ko', 'label_en', 'title_ko', 'title_en', 'description_ko', 'description_en', 'sort', 'visible'],
    '요금정책': ['id','group','title_ko','title_en','description_ko','description_en','unit_ko','unit_en','starting_price_krw','rate_min_pct','rate_max_pct','deliverables_ko','deliverables_en','notice_ko','notice_en','sort','visible'],
    '무료진단옵션': ['group','id','label_ko','label_en','description_ko','description_en','sort','visible'],
    '검색서비스': ['slug','title_ko','title_en','meta_ko','meta_en','intro_ko','intro_en','scope_ko','scope_en','deliverables_ko','deliverables_en','process_ko','process_en','question_ko','answer_ko','question_en','answer_en','sort','visible'],
}
OPTIONAL_MAP = {'이미지맵': ['key','src','alt_ko','alt_en','position','kind','visible']}

COLLECTIONS = {'서비스': 'services', '상품': 'products', '파트너': 'partners', '진행절차': 'steps', 'FAQ': 'faq', '지원프로그램': 'programs', '인사이트': 'insights', '요금정책': 'pricing', '무료진단옵션': 'free_report_options'}


def col_index(ref):
    letters = re.match(r'([A-Z]+)', ref)
    if not letters:
        raise ValueError(f'Invalid cell reference: {ref!r}')
    num = 0
    for char in letters.group(1):
        num = num * 26 + ord(char) - 64
    return num - 1


def get_strings(node):
    return ''.join(el.text or '' for el in node.findall('.//x:t', N))


def read_excel(path):
    out = {}
    with zipfile.ZipFile(path) as z:
        workbook = ET.fromstring(z.read('xl/workbook.xml'))
        rels = ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
        relationship_map = {e.attrib['Id']: e.attrib['Target'] for e in rels.findall('pr:Relationship', N)}
        strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            ss = ET.fromstring(z.read('xl/sharedStrings.xml'))
            strings = [get_strings(si) for si in ss.findall('x:si', N)]
        for sheet in workbook.findall('x:sheets/x:sheet', N):
            name = sheet.attrib['name']
            if name not in MAP and name not in OPTIONAL_MAP:
                continue  # Strict allowlist. Never publish additional/sensitive sheets.
            id_ = sheet.attrib[f'{{{N["r"]}}}id']
            target = relationship_map[id_].lstrip('/')
            sheet_path = target if target.startswith('xl/') else posixpath.normpath(posixpath.join('xl', target))
            root = ET.fromstring(z.read(sheet_path))
            rows = []
            for row in root.findall('x:sheetData/x:row', N):
                cells = {}
                for cell in row.findall('x:c', N):
                    typ = cell.attrib.get('t', '')
                    v = cell.find('x:v', N)
                    inline = cell.find('x:is', N)
                    if typ == 's' and v is not None:
                        value = strings[int(v.text or 0)]
                    elif typ == 'inlineStr' and inline is not None:
                        value = get_strings(inline)
                    elif typ == 'b' and v is not None:
                        value = v.text == '1'
                    elif v is not None and v.text is not None:
                        value = v.text
                        if typ not in ('str', 'e', 'd'):
                            try:
                                value = float(value) if '.' in value else int(value)
                            except (ValueError, TypeError):
                                pass
                    else:
                        value = ''
                    cells[col_index(cell.attrib['r'])] = value
                if cells:
                    rows.append([cells.get(i, '') for i in range(max(cells) + 1)])
            if not rows:
                raise ValueError(f'Required sheet empty: {name}')
            out[name] = rows
    for name, fields in MAP.items():
        if name not in out:
            raise ValueError(f'Required public sheet missing: {name}')
        actual = out[name][0]
        if actual[:len(fields)] != fields:
            raise ValueError(f'{name}: column headers changed. Expected {fields}; got {actual}')
    for name, fields in OPTIONAL_MAP.items():
        if name in out and out[name][0][:len(fields)] != fields:
            raise ValueError(f'{name}: invalid image map columns')
    return out


def safe_url(value):
    value = str(value or '').strip()
    if not value:
        return ''
    parsed = urlparse(value)
    return value if parsed.scheme == 'https' and parsed.netloc else ''


def visible(value):
    return str(value).strip().lower() in ('y', 'yes', 'true', '1', '공개')


def to_records(rows, fields):
    objects = []
    for rownum, row in enumerate(rows[1:], 2):
        rec = dict(zip(fields, row + [''] * max(0, len(fields) - len(row))))
        if not visible(rec.get('visible')):
            continue
        if not any(str(rec.get(field, '')).strip() for field in fields if field not in ('visible', 'sort')):
            continue
        for key, value in rec.items():
            if key not in ('sort', 'step', 'visible'):
                rec[key] = str(value or '').strip()[:2500]
        for key in ('source_url', 'official_url'):
            if key in rec:
                rec[key] = safe_url(rec[key])
        for key in ('starting_price_krw','rate_min_pct','rate_max_pct'):
            if key in rec:
                try: rec[key] = max(0, float(rec[key] or 0))
                except (TypeError, ValueError): raise ValueError(f'Invalid numeric fee in {key} on row {rownum}')
                if key in ('rate_min_pct','rate_max_pct') and rec[key] > 100: raise ValueError('Percentage cannot exceed 100')
        if rec.get('group') == 'commission' and rec.get('rate_min_pct',0)>rec.get('rate_max_pct',0):
            raise ValueError('Commission percentage range inverted')
        for key in ('sort', 'step'):
            if key in rec:
                try: rec[key] = int(float(rec[key]))
                except (TypeError, ValueError): rec[key] = 9999
        rec.pop('visible', None)
        objects.append(rec)
    return sorted(objects, key=lambda rec: rec.get('sort', rec.get('step', 9999)))


def build(excel_file):
    book = read_excel(excel_file)
    settings = {}
    for row in book['설정'][1:]:
        if len(row) < 3 or not str(row[0]).strip():
            continue
        key = str(row[0]).strip()
        if not re.fullmatch(r'[a-z][a-z0-9_]*', key):
            raise ValueError(f'Invalid settings key: {key}')
        settings[key] = {'ko': str(row[1] or '').strip()[:2000], 'en': str(row[2] or '').strip()[:2000]}
    for key in ('form_endpoint', 'site_domain'):
        if key in settings:
            for lng in ('ko', 'en'):
                settings[key][lng] = safe_url(settings[key][lng])
    if settings.get('contact_email', {}).get('ko'):
        for lng in ('ko', 'en'):
            em = settings['contact_email'][lng]
            if em and not re.fullmatch(r'[^@\s]+@[^@\s]+\.[^@\s]+', em):
                raise ValueError('Invalid company contact email')
    data = {'schema_version': 1, 'settings': settings}
    for sheet, key in COLLECTIONS.items():
        data[key] = to_records(book[sheet], MAP[sheet])
    if not data['free_report_options'] or len(data['free_report_options']) < 15:
        raise ValueError('Free report selections are missing')
    required_groups = {'country','industry','objective','channel','stage','readiness'}
    free_groups = {x['group'] for x in data['free_report_options']}
    if not required_groups.issubset(free_groups):
        raise ValueError('Free report required dropdown groups missing')
    for rec in data['free_report_options']:
        if not re.fullmatch(r'[A-Z][A-Z0-9_]{1,23}', rec['id']):
            raise ValueError('Invalid free report option ID')
        if not rec['label_ko'] or not rec['label_en']:
            raise ValueError('Free report option label required')
    if not data['services'] or not data['partners']:
        raise ValueError('At least one service and one partner type required')
    data['visuals'] = {}
    if '이미지맵' in book:
        for img in to_records(book['이미지맵'], OPTIONAL_MAP['이미지맵']):
            if not re.fullmatch(r'assets/images/[a-z0-9-]+\.(webp|jpg|png)',img['src']):
                raise ValueError('Unsafe image path: '+img['src'])
            if img['key'] in data['visuals']: raise ValueError('Duplicate image key: '+img['key'])
            if not re.fullmatch(r'\d{1,3}% \d{1,3}%',img['position']): raise ValueError('Invalid focal position')
            data['visuals'][img['key']] = img
    return data


def main(argv=None):
    arg = argparse.ArgumentParser(description='Public Excel → JSON for GitHub Pages')
    arg.add_argument('--excel', default='data/website_content.xlsx')
    arg.add_argument('--output', default='site/data/site-data.json')
    args = arg.parse_args(argv)
    data = build(Path(args.excel))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Exported public website data: {output} ({len(data["products"])} products, {len(data["services"])} services, {len(data["programs"])} programs)')

if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'BUILD FAILED: {exc}', file=sys.stderr)
        raise SystemExit(1)
