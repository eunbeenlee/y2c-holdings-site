import unittest, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_site_data import build
class ImageIntegrityTests(unittest.TestCase):
 def test_visuals_mapped_and_local(self):
  data=build(ROOT/'data/website_content.xlsx')
  for key,image in data['visuals'].items():
   self.assertTrue((ROOT/'site'/image['src']).is_file(),key)
   self.assertTrue(image['alt_ko'] and image['alt_en'])
 def test_every_visible_product_has_exact_photo(self):
  data=build(ROOT/'data/website_content.xlsx')
  self.assertTrue(all(p['sku'] in data['visuals'] for p in data['products']))
  names=[data['visuals'][p['sku']]['src'] for p in data['products']]
  self.assertEqual(len(names),len(set(names)))
  self.assertFalse(any(p['sku']=='AUTO-004' for p in data['products']))
 def test_every_service_has_exact_photo(self):
  data=build(ROOT/'data/website_content.xlsx')
  self.assertTrue(all(s['id'] in data['visuals'] for s in data['services']))
 def test_no_fake_proof(self):
  html=(ROOT/'site/index.html').read_text()
  self.assertNotIn('100+ 프로젝트',html)
  self.assertNotIn('50+ 해외',html)
 def test_source_disclosure(self):
  meta=json.loads((ROOT/'data/asset-provenance.json').read_text())
  self.assertTrue(all('AI-generated' in x['source_type'] for x in meta))
