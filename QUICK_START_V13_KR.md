# V13 적용 방법 (기존 Y2C GitHub 저장소)

대상 저장소: https://github.com/eunbeenlee/y2c-holdings-site

1. `Y2C_HOLDINGS_V13_FULL_GitHub.zip`을 압축 해제합니다.
2. GitHub 저장소의 `main` 브랜치에서 압축 해제 폴더 **안에 있는 파일과 폴더**를 같은 경로로 업로드하고 변경사항을 Commit합니다. 루트에 `.github`, `data`, `scripts`, `site`, `supabase`, `tests`가 보여야 합니다.
3. 이 ZIP의 `site/assets/supabase-config.js`는 이전에 제공된 Y2C의 **공개 프로젝트 URL과 Publishable key**를 포함합니다. 비밀 키/비밀번호는 없습니다. 새로운 Supabase 프로젝트를 생성하지 않았다면 그대로 사용합니다.
4. GitHub `Settings > Pages > Source`가 `GitHub Actions`인지 확인합니다.
5. GitHub `Actions > Publish Y2C Excel Website`가 녹색 성공인지 확인합니다. `y2choldings.co.kr`의 DNS와 Custom domain은 기존 설정을 유지합니다.
6. 공개 요금: https://y2choldings.co.kr/pricing.html (KR/EN)
7. 회사계정 보고서 작성: https://y2choldings.co.kr/admin.html  → 기존 Supabase 회사 이메일과 비밀번호로 로그인 → 보고서 등급 선택 → 내용 작성/저장.
8. `data/website_content.xlsx`의 `요금정책` 시트에서 가격·설명을 수정한 뒤 Commit하면 공개 요금 페이지가 자동 갱신됩니다. 새 가격은 기존 고객과 이미 계약된 금액을 자동 변경하지 않습니다. 관리자 보고서의 실제 계약액은 보고서별로 수동 입력할 수 있습니다.
9. 부가세, 현장 업무 및 출입국 규정에 따라 견적 내용은 계약 전 검토합니다.
10. 문의폼은 현재 **실제 수신 채널이 연결되지 않은 복사용**입니다. 유료 광고를 시작하기 전에 보안 접수 시스템을 붙여야 합니다.

**업로드와 SQL 관련:** 이번 V13은 새 테이블이 필요하지 않으므로 이미 실행한 `supabase/01_schema.sql`을 다시 실행하지 않습니다. `.github/workflows` 자동백업 Secrets와 DB 활동점검 Secrets는 기존 설정이 유지됩니다.

**보안:** 공개용 엑셀 외에 고객정보·수수료 계약서·내부 운영 관리 엑셀을 공개 저장소에 올리지 마세요. `sb_publishable_*`만 공개 사용 가능합니다.
