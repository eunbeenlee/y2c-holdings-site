# Y2C HOLDINGS — Corporate Website V4

**GitHub Pages + Excel-driven public website**  
한국어/English · responsive · original supplied Y2C logo · refined corporate style

## Upload to GitHub

1. Create a new GitHub repository (public if using free GitHub Pages on your plan).
2. Upload **the contents of this folder** to the repository root, including the hidden `.github` directory.
3. In repository **Settings → Pages → Build and deployment → Source**, choose **GitHub Actions**.
4. Push to `main`, or run the **Publish Y2C Excel Website** workflow manually.
5. Deployment URL is shown in the `Deploy` step after GitHub Pages succeeds. The site is not deployed merely by opening this ZIP.

## Updating through Excel

Modify `data/website_content.xlsx` and commit/push the changed file. GitHub Actions:

1. validates the workbook,
2. generates `site/data/site-data.json`,
3. tests the site structure,
4. publishes the `site/` folder to GitHub Pages.

**Editable from Excel:** bilingual hero, navigation and section settings (`설정`), services (`서비스`), products and tariff notes (`상품`), partners (`파트너`), steps (`진행절차`), FAQ, export resources and insights. For homepage layout, custom visual typography or section arrangement, edit `site/index.html` and `site/assets/styles.css` directly. Not every decorative/static phrase is controlled by Excel.

**Do not upload** internal business-management Excel files, contract lists, leads, costs, CRM, contact information or private financial records to this repository. This project includes only `data/website_content.xlsx`, with public-website-ready entries.

## Inquiry settings — important

The site is **not a live CRM**. By default, the form validates input and allows copying the prepared inquiry. It does not silently claim to receive or store personal information. Before enabling live submissions, configure a secure receiving service and finalize the privacy notice. `설정` has fields `contact_email` and `form_endpoint` intentionally blank. The frontend currently supports a mailto or HTTPS JSON form endpoint; verify the provider's CORS, privacy, anti-spam and security requirements. Never place API keys or CRM secrets in the public workbook.

## Local commands (optional)

```bash
python -m unittest discover -s tests -v
python scripts/build_site_data.py --excel data/website_content.xlsx --output site/data/site-data.json
python scripts/check_site.py
python -m http.server 8000 --directory site
```
Open `http://localhost:8000` to view locally. `file://` is not supported for JSON loading in standard browsers; use a server or GitHub Pages.

## Design assets

The logo asset `site/assets/y2c-logo.png` is derived from the user-provided Y2C HOLDINGS logo, with white background removed for web use. Font choices are browser/system fallbacks plus public CSS-loaded Google Fonts; **no font files are included**. Other hero graphics and business illustrations are created with CSS and inline SVG. The site makes no claim to have executed supply or government provider contracts.

## Files

- `.github/workflows/deploy.yml` — auto deployment
- `data/website_content.xlsx` — **PUBLIC** bilingual website content
- `scripts/` — Excel parser and validation, no external Python dependencies required for deployment
- `site/` — GitHub Pages website
- `tests/` — parser regression tests
- `QUICK_START_KR.md` — Korean setup guide
