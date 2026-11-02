# Y2C HOLDINGS — Corporate Website V9 + Private Report Workspace

Y2C의 기존 V8 기업형 홈페이지를 계승한 GitHub Pages 배포 패키지입니다. 로고·한영 전환·엑셀 자동 배포 유지, 상품 소싱 카탈로그와 관리자 전용 시장조사 보고서 작성 화면을 추가했습니다.

## Architecture

| Area | Source | Public? |
|---|---|---|
| Corporate site and product catalog | `site/` + `data/website_content.xlsx` | YES |
| Excel build pipeline | `scripts/build_site_data.py` + GitHub Actions | YES |
| Login credentials | Supabase Auth | NO — never enter into Excel/GitHub |
| Market research reports | Supabase Postgres `y2c_reports` protected by RLS | NO |
| Approved admin roster | Supabase Postgres `y2c_admins` editable via trusted SQL Editor only | NO |

### Live deployment limitations

Until the organization creates/configures its own Supabase project, `site/admin.html` displays a setup notice. It **does not** provide fake login or local-only fake saving. Existing public partner form is still copy/prepare unless an independently verified receiving endpoint is set.

### Contents

- `site/index.html`: Corporate home with product sourcing section, KR/EN toggle
- `site/admin.html`: administrator report editor, 13 sections; report list, draft/review/final, print and JSON backup
- `site/assets/admin.js`/`admin.css`: authenticated UI
- `site/assets/supabase-config.js`: empty PUBLIC config; paste only URL and publishable key
- `supabase/01_schema.sql`: authenticated user table, admin allowlist and report RLS
- `supabase/02_approve_admin_example.sql`: trusted admin enrollment example (no passwords)
- `data/website_content.xlsx`: ONLY public product catalog & site data
- `.github/workflows/main.yml`: workflow to publish `site/` after Excel validation

### Local tests

```bash
python -m unittest discover -s tests -v
python scripts/build_site_data.py --excel data/website_content.xlsx --output site/data/site-data.json
python scripts/check_site.py
node --check site/assets/app.js
node --check site/assets/admin.js
```

Refer to `QUICK_START_KR.md` for full instructions. Do not upload private workbooks or sensitive customer information to this public repository.


## V10: encrypted email backups
See `BACKUP_EMAIL_SETUP_KR.md`. The new workflow `.github/workflows/backup-email.yml` is independently scheduled and does not change public site build. Private data and passwords must never be committed.

## V11 Supabase Free 자동 활동 점검

- `SUPABASE_자동활동점검_설치안내.md` 참조
- `.github/workflows/supabase-keepalive.yml` 별도 작업 하루 3회 DB 읽기·실패 알림
- V10의 `backup-email.yml` 일일 암호화 이메일 백업 그대로 유지
- Supabase 자동 일시 중지를 반드시 막는 기능은 아니며, GitHub 무료 예약 작업의 장기 비활성화에 주의
- `.github/workflows/repo-activity.yml` 월별 봇 빈 커밋으로 GitHub 60일 예약 중지 위험 완화(비보장)
