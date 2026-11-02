# Y2C HOLDINGS V13 — Corporate Website + Services & Pricing

Public GitHub Pages website and confidential, Supabase-backed report workspace.

- Home: `site/index.html`
- Services & pricing (KR/EN, Excel-driven): `site/pricing.html`
- Private report editor, tier-specific scope: `site/admin.html`
- Website PUBLIC content workbook: `data/website_content.xlsx` (including `요금정책`)
- Excel-to-JSON builder: `scripts/build_site_data.py`
- GitHub Pages: `.github/workflows/main.yml`
- Existing scheduled backup and DB activity monitor are retained.

**This is a public static site repository.** No CRM, report content, internal cost models, private documents, password spreadsheets or secret API keys belong here. Supabase RLS protects the private report table.

See `QUICK_START_V13_KR.md` and `V13_RELEASE_NOTES.md`.

## V16 — Free market entry snapshot
- `site/free-report.html`: no-login, no-cost public self-check and instant brief.
- `data/website_content.xlsx` → `무료진단옵션` for dropdown items.
- `site/assets/free-report.js` has curated sector/country/objective logic (no fabricated numbers).
- Details: `V16_무료시장진단_설치안내.md`.
