import unittest,json,re,os,sys
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from photo_library import by_key
SITE=ROOT/'site'
class Tags(HTMLParser):
 def __init__(self):super().__init__();self.tags=[]
 def handle_starttag(self,t,a):self.tags.append((t,dict(a)))
class V21AlignmentTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.data=json.loads((SITE/'data/site-data.json').read_text())
 def test_six_shared_service_ids_and_titles(self):
  expected=['market-research','overseas-sales','buyer-development','export-consulting','supply-chain','franchise-development']
  self.assertEqual([s['id'] for s in self.data['services']],expected)
  self.assertEqual([s['slug'] for s in self.data['seo_services']],expected)
  for a,b in zip(self.data['services'],self.data['seo_services']):
   for lang in ['ko','en']:self.assertEqual(a['title_'+lang],b['title_'+lang])
 def test_service_cards_and_details_have_same_photo(self):
  for lang in ['ko','en']:
   suffix='-en' if lang=='en' else ''
   home=(SITE/f'index{suffix}.html').read_text()
   for s in self.data['services']:
    src=self.data['visuals'][s['id']]['src']
    self.assertIn(src,home)
    self.assertIn(src,(SITE/f'{s["id"]}{suffix}.html').read_text())
 def test_product_classification_matches_image_key(self):
  self.assertEqual([c['id'] for c in self.data['product_categories']],['Interior','Care','Fragrance','Film'])
  self.assertEqual({x['sku']:x['category'] for x in self.data['products']},{'AUTO-001':'Interior','AUTO-002':'Care','AUTO-003':'Fragrance','AUTO-005':'Film'})
  for p in self.data['products']:self.assertIn(p['sku'],self.data['visuals'])
 def test_unique_image_files(self):
  values=list(self.data['visuals'].values());self.assertEqual(len(values),11)
  self.assertEqual(len({v['src'] for v in values}),11)
  self.assertEqual({p['file'] for p in by_key().values()},{Path(v['src']).name for v in values})
  if os.environ.get('Y2C_REQUIRE_LOCAL_PHOTOS')=='1':
   self.assertEqual(set(p.name for p in (SITE/'assets/images').glob('*.webp')),{Path(v['src']).name for v in values})
 def test_theme_header_footer_on_all_public_pages(self):
  for p in SITE.glob('*.html'):
   text=p.read_text();self.assertEqual(text.count('assets/theme.css'),1,p.name)
   self.assertNotIn('assets/brand.css',text,p.name)
   self.assertIn('data-page=',text,p.name)
   if p.name=='admin.html':continue
   self.assertEqual(text.count('class="y2c-header"'),1,p.name)
   self.assertEqual(text.count('class="y2c-footer"'),1,p.name)
   self.assertIn('data-shell-lang="ko"',text,p.name);self.assertIn('data-shell-lang="en"',text,p.name)
 def test_dom_ids_unique(self):
  for p in SITE.glob('*.html'):
   t=Tags();t.feed(p.read_text());ids=[a['id'] for tag,a in t.tags if 'id' in a]
   self.assertEqual(len(ids),len(set(ids)),p.name)
 def test_prices_and_reporting_not_replaced_by_placeholders(self):
  price={x['id']:int(x['starting_price_krw']) for x in self.data['pricing'] if x['group']=='report'}
  self.assertEqual(price,{'essential':490000,'business':1690000,'strategic':4500000,'enterprise':9000000})
  self.assertIn('signInWithPassword',(SITE/'assets/admin.js').read_text())
  self.assertIn('public.y2c_reports',(ROOT/'supabase/01_schema.sql').read_text())
  self.assertTrue((ROOT/'.github/workflows/backup-email.yml').is_file())
 def test_no_images_on_task_focused_forms(self):
  for name in ['pricing.html','quick-report.html','free-report.html','admin.html']:
   text=(SITE/name).read_text();self.assertNotIn('assets/images/',text,name)
if __name__=='__main__':unittest.main()
