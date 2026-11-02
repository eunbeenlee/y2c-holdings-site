# Y2C HOLDINGS — V17 Free Organic SEO

Complete GitHub Pages corporate website plus bilingual organic-search service pages generated from the **public-only** Excel workbook.

**No SEO agency, paid ads, indexing API or Google/Naver account is required.** Automatic discovery/indexing is not guaranteed.

`data/website_content.xlsx` → `scripts/build_site_data.py` + `scripts/build_seo_pages.py` → `site/` → GitHub Actions Pages deployment.

Run locally:

```bash
python -m unittest discover -s tests -v
python scripts/build_site_data.py --excel data/website_content.xlsx --output site/data/site-data.json
python scripts/build_seo_pages.py --excel data/website_content.xlsx --site site
python scripts/check_seo.py
```

See `V17_SEO_무료운영_적용안내.md` for Korean deployment instructions. **The private management workbook is not included.**
