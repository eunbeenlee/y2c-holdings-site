"""Photograph coverage remains strict; release CI requires acquired local bytes."""
import os,unittest,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_site_data import build
from photo_library import by_key,resolved_url
class ImageIntegrityTests(unittest.TestCase):
 def test_visuals_mapped_and_locally_buildable(self):
  d=build(ROOT/'data/website_content.xlsx');p=by_key()
  for key,v in d['visuals'].items():
   self.assertEqual(v['src'],'assets/images/'+p[key]['file']);self.assertTrue(v['alt_ko'] and v['alt_en'])
   if os.environ.get('Y2C_REQUIRE_LOCAL_PHOTOS')=='1':self.assertTrue(resolved_url(key)[1],key)
 def test_every_visible_product_has_exact_photo(self):
  d=build(ROOT/'data/website_content.xlsx')
  self.assertTrue(all(p['sku'] in d['visuals'] for p in d['products']))
  self.assertEqual(len({d['visuals'][p['sku']]['src'] for p in d['products']}),len(d['products']))
  self.assertFalse(any(p['sku']=='AUTO-004' for p in d['products']))
 def test_every_service_has_exact_photo(self):
  d=build(ROOT/'data/website_content.xlsx');self.assertTrue(all(s['id'] in d['visuals'] for s in d['services']))
 def test_no_fake_proof(self):
  h=(ROOT/'site/index.html').read_text();self.assertNotIn('100+ 프로젝트',h);self.assertNotIn('50+ 해외',h)
 def test_source_disclosure(self):
  meta=json.loads((ROOT/'data/asset-provenance.json').read_text())
  self.assertTrue(all(x['source_type'].startswith('External stock') for x in meta))
  self.assertTrue(all(x['source_url'].startswith('https://') and x['license_url'] for x in meta))
