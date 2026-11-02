import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_site_data import read_excel, build, safe_url, visible, to_records, MAP

class ExcelDrivenSiteTests(unittest.TestCase):
    def setUp(self):
        self.file=ROOT/'data/website_content.xlsx'
    def test_excel_sheet_names_and_header(self):
        rows=read_excel(self.file)
        self.assertTrue(all(x in rows for x in MAP))
    def test_data_from_excel(self):
        data=build(self.file)
        self.assertEqual(data['schema_version'],1)
        self.assertEqual(data['settings']['company']['ko'],'Y2C HOLDINGS')
        self.assertGreaterEqual(len(data['products']),4)
        self.assertIn('industry_auto_title', data['settings'])
        self.assertIn('network_title', data['settings'])
        self.assertTrue(any('TPE' in p['name_ko'] for p in data['products']))
    def test_allowlist_ignores_extra_columns(self):
        fields=MAP['상품']
        row=['X9','Care','CA','상품','Item','A','B','TARIFF','TARIFF','', '검토','https://example.org',1,'Y','PRIVATE_NOT_FOR_WEBSITE']
        res=to_records([fields+['private_contact'],row],fields)
        self.assertEqual(len(res),1)
        self.assertNotIn('private_contact',res[0])
    def test_hidden_rows_excluded(self):
        fields=MAP['서비스']
        row=['test','automotive','car','테스트','Test','설명','Description',1,'N']
        self.assertEqual(to_records([fields,row],fields),[])
    def test_reject_non_https_urls(self):
        self.assertEqual(safe_url('javascript:alert(1)'),'')
        self.assertEqual(safe_url('http://example.com'),'')
        self.assertEqual(safe_url('https://www.kotra.or.kr/'),'https://www.kotra.or.kr/')
    def test_private_management_workbook_not_in_project(self):
        self.assertFalse(list(ROOT.rglob('*사업전략_운영관리*.xlsx')))
    def test_no_claimed_contact(self):
        data=build(self.file)
        self.assertEqual(data['settings']['contact_email']['ko'],'')
        self.assertEqual(data['settings']['form_endpoint']['ko'],'')

if __name__ == '__main__':
    unittest.main()

class PortalSecurityAndCatalogTests(unittest.TestCase):
    def test_catalog_is_rendered_from_excel_data(self):
        html=(ROOT/'site/index.html').read_text(encoding='utf-8')
        js=(ROOT/'site/assets/app.js').read_text(encoding='utf-8')
        self.assertIn('id="productsGrid"',html)
        self.assertIn("data.products",js)
        self.assertIn('function products()',js)
    def test_admin_requires_database_auth(self):
        admin=(ROOT/'site/admin.html').read_text(encoding='utf-8')
        script=(ROOT/'site/assets/admin.js').read_text(encoding='utf-8')
        self.assertIn('signInWithPassword',script)
        self.assertIn('y2c_admins',script)
        self.assertIn('y2c_reports',script)
        self.assertIn('id="loginForm"',admin)
    def test_no_credential_excel_in_public_project(self):
        self.assertFalse(list(ROOT.rglob('*password*.xlsx')))
        self.assertFalse(list(ROOT.rglob('*login*.xlsx')))
        self.assertFalse(list(ROOT.rglob('*계정*.xlsx')))
        # The real deployed public Supabase configuration is intentionally preserved
        # from the user's GitHub repository; NEVER assert that its legitimate values are blank.
        existing=ROOT/'site/assets/supabase-config.js'
        if existing.exists():
            config=existing.read_text(encoding='utf-8')
            self.assertIn('Y2C_ADMIN_CONFIG',config)
            self.assertIn('publishableKey',config)
            self.assertNotIn('sb_secret_',config)
            self.assertNotIn("publishableKey: 'sb_secret_",config)
        sql=(ROOT/'supabase/01_schema.sql').read_text(encoding='utf-8')
        self.assertIn('row level security',sql.lower())
        self.assertIn('revoke all',sql.lower())


class ReportStudioV12Tests(unittest.TestCase):
    def test_report_template_sections_and_company_login(self):
        js=(ROOT/'site/assets/admin.js').read_text(encoding='utf-8')
        html=(ROOT/'site/admin.html').read_text(encoding='utf-8')
        self.assertIn('eunbeen.lee@y2choldings.co.kr',html)
        self.assertIn('signInWithPassword',js)
        self.assertIn('y2c_admins',js)
        self.assertIn('y2c_reports',js)
        self.assertIn('autoSaveTimer',js)
        self.assertIn('MARKET RESEARCH',html.upper())
        for key in ['executive_summary','market_size','tariffs','supply_chain','economics','recommendation','sources']:
            self.assertIn(key,js)
    def test_no_private_api_keys_or_real_credentials(self):
        for source in [ROOT/'site/assets/admin.js',ROOT/'site/admin.html',ROOT/'site/assets/supabase-config.example.js']:
            body=source.read_text(encoding='utf-8')
            self.assertNotIn("publishableKey: 'sb_secret_",body)
            self.assertNotIn("publishableKey: \"sb_secret_",body)
        self.assertFalse((ROOT/'data'/'credentials.xlsx').exists())
    def test_site_structure(self):
        self.assertTrue((ROOT/'site'/'admin.html').is_file())
        self.assertTrue((ROOT/'site/assets/admin.css').is_file())
        self.assertTrue((ROOT/'site/assets/admin.js').is_file())
        self.assertTrue((ROOT/'supabase/01_schema.sql').is_file())
