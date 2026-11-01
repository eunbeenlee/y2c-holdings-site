# Y2C HOLDINGS — Corporate Website V8

**Purpose:** A business-focused corporate website for Y2C HOLDINGS. This is a standalone, static GitHub Pages website with a public Excel content source.

## Design V8

- **Smaller actual Y2C logo** in the 78px desktop header and 67px mobile header; no giant logo in the hero.
- Corporate information hierarchy: Company → Business Portfolio → Industry Focus → Cross-border Business → How We Work → Partnerships → Business Inquiry.
- Public-facing business capabilities, not a narrowly defined product storefront.
- Original gold/white/charcoal logo palette with restrained typography and strong business labels.
- Korean / English toggle on desktop and mobile.
- No unverified customer logos, subsidiary claims, sales metrics, delivery commitments or public funding claims.
- Lead form is currently **prepare/copy only**; no receiving system is configured.

## Excel-controlled content

Edit `data/website_content.xlsx` and commit/push to `main`:

| Sheet | Editable public content |
|---|---|
| `설정` | Hero heading/subheading; company introduction; business and industry headings; industry titles/captions; network, process, partner and contact section copy; future contact email / approved submission endpoint |
| `서비스` | Four core business-area headings/descriptions and their order/visibility |
| `진행절차` | The three business execution stages |
| `파트너` | Manufacturer, buyer, franchise/brand and logistics partnership types |
| `상품`, `FAQ`, `지원프로그램`, `인사이트` | Public structured content retained for future secondary-page expansion; not featured on V8 homepage |

The structural page layout, illustrations, industry card count and navigation anchors are HTML/CSS/JavaScript and require code changes. **Excel content update is not the same as full website layout editing.**

Never put private Y2C CRM, actual pricing, personal contact lists, signed agreements, government IDs, or internal V3 workbooks into this public repository.

## Technical architecture

- `/site/` — deployed web root (HTML, CSS, JS and logo)
- `/data/website_content.xlsx` — PUBLIC website content Excel
- `/scripts/build_site_data.py` — Excel OOXML → allowlisted JSON, built with standard Python only
- `/site/data/site-data.json` — generated public JSON
- `/.github/workflows/main.yml` — GitHub Actions to test, transform and deploy
- `/tests/` — content, privacy and schema tests

### GitHub deploy

See `QUICK_START_KR.md`. The workflow requires `Settings > Pages > Source = GitHub Actions` and a correctly arranged repository root.

### Known limitation: no live inbound leads

The inquiry form is not an email-sending or database-sending system until a real receiving endpoint or company-owned email is configured. Before launch, finalize the privacy policy and legal review for cross-border lead collection.

### Testing

Run from the repository root:

```bash
python -m unittest discover -s tests -v
python scripts/build_site_data.py --excel data/website_content.xlsx --output site/data/site-data.json
python scripts/check_site.py
```

The local test renders of V8 use the same HTML/CSS/JS with an in-memory copy of `site-data.json`, because the QA browser environment disallows navigation to local file URLs; production GitHub Pages uses ordinary `fetch` of the generated JSON.

## Corporate design references

The concept is an original Y2C interpretation of a common business information hierarchy and does not copy third-party code, imagery, or logos:

- Samsung business areas: https://www.samsung.com/sec/ir/ir-resources/ourbusiness/
- LOTTE business areas: https://recruit.lotte.co.kr/about/group
- LG corporate information: https://www.lg.com/global/about-lg/corporate-information/
- POSCO Holdings portfolio: https://www.posco-inc.com/hs91a1-front/app/company/business-area.html
- HD Hyundai businesses: https://recruit.hd.com/kr/mainLayout/introduction
- CJ corporate introduction: https://www.cj.net/cj-introduction

All references are for navigation patterns and content grouping, not claims of Y2C affiliation.
