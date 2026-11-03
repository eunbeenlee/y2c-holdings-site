import io,json,sys,unittest,tempfile
from pathlib import Path
from html.parser import HTMLParser
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from photo_library import records,by_key,image_html
from prepare_photos import convert
class Images(HTMLParser):
 def __init__(self):super().__init__();self.images=[]
 def handle_starttag(self,t,a):
  if t=='img':self.images.append(dict(a))
class CategoryPhotoTests(unittest.TestCase):
 def setUp(self):self.d=json.loads((ROOT/'site/data/site-data.json').read_text());self.p=by_key()
 def test_all_slots_have_one_unique_source(self):
  self.assertEqual(len(self.p),11);self.assertEqual(len({p['photo_id'] for p in self.p.values()}),11)
 def test_explicit_photo_subject(self):
  subjects={'hero':'터미널','market-research':'차트','overseas-sales':'헤드셋','buyer-development':'부스','export-consulting':'문서','supply-chain':'창고','franchise-development':'매장','AUTO-001':'매트','AUTO-002':'타월','AUTO-003':'방향제','AUTO-005':'유리'}
  for k,s in subjects.items():self.assertIn(s,self.p[k]['subject_ko'])
 def test_rubber_material_and_window_context_not_misrepresented(self):
  prod={p['sku']:p for p in self.d['products']}
  self.assertNotIn('TPE',prod['AUTO-001']['name_ko'])
  self.assertIn('적용 환경',self.p['AUTO-005']['subject_ko'])
  home=(ROOT/'site/index.html').read_text();self.assertIn('필름 원단이 아닌',home)
 def test_all_service_image_tags_match_on_three_surfaces(self):
  for lang in ('ko','en'):
   suffix='-en' if lang=='en' else ''
   pages={x:(ROOT/'site'/f'{x}{suffix}.html').read_text() for x in ['index','services']+[s['id'] for s in self.d['services']]}
   for s in self.d['services']:
    k=s['id'];matches=[]
    for page in ['index','services',k]:
     parser=Images();parser.feed(pages[page]);imgs=[i for i in parser.images if i.get('data-photo-key')==k]
     self.assertEqual(len(imgs),1,(lang,page,k));matches.append((imgs[0]['src'],imgs[0]['alt']))
    self.assertEqual(len(set(matches)),1,(lang,k))
 def test_quick_and_free_industries_are_shared(self):
  q=json.loads((ROOT/'site/data/quick-report-options.json').read_text())
  opts=[o for o in self.d['free_report_options'] if o['group']=='industry']
  self.assertEqual(q['industries'],[x['label_ko'] for x in opts])
  for o in opts:self.assertEqual(q['option_labels_en'][o['label_ko']],o['label_en'])
 def test_home_and_admin_use_same_industries(self):
  h=(ROOT/'site/index.html').read_text();a=(ROOT/'site/admin.html').read_text()
  for o in self.d['industries']:
   self.assertIn('data-industry-id="'+o['id']+'"',h);self.assertIn('value="'+o['label_ko']+'"',a)
 def test_image_acquisition_is_before_deploy(self):
  w=(ROOT/'.github/workflows/main.yml').read_text()
  self.assertLess(w.index('python scripts/prepare_photos.py'),w.index('actions/deploy-pages'))
  self.assertIn('Y2C_REQUIRE_LOCAL_PHOTOS=1',w);self.assertNotIn('continue-on-error',w)
 def test_conversion_and_manifest_checks(self):
  b=io.BytesIO();Image.new('RGB',(3000,2000),'#d3d0c8').save(b,'JPEG')
  p=dict(self.p['market-research'])
  with tempfile.TemporaryDirectory() as d:
   path=Path(d)/'sample.webp';result=convert(p,b.getvalue(),path)
   self.assertTrue(path.is_file());self.assertEqual(result['output_size'],[1400,875]);self.assertEqual(len(result['sha256']),64)
 def test_source_resolution_rejected(self):
  b=io.BytesIO();Image.new('RGB',(385,428)).save(b,'JPEG')
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaisesRegex(ValueError,'resolution'):convert(self.p['hero'],b.getvalue(),Path(d)/'bad.webp')
 def test_no_paid_font_or_private_workbook(self):
  self.assertFalse([p for p in ROOT.rglob('*') if p.suffix in {'.ttf','.woff','.woff2','.otf'}])
 def test_credit_links_documented(self):
  h=(ROOT/'site/photo-credits.html').read_text()
  for p in records():self.assertIn(p['source_url'],h);self.assertIn(p['author'],h)
