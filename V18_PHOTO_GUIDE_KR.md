# Y2C V18 — 사진 통합 디자인 사용 가이드

## 적용 범위
- 메인 사진형 히어로, 사업영역 카드, 자동차·프랜차이즈·무역 관련 산업 카드
- 상품 소싱 카드, 기업 간 물류 협업 섹션, 검색용 업무별 12개 상세페이지 + 서비스 허브
- 시장조사 견적, 간편시장조사, 무료 시장진단 페이지의 사진 배너
- SEO 이미지 메타태그 및 WebP 최적화·모바일용 이미지

## 저작권·표현 정확성
모든 신규 사진은 사이트의 서비스 콘셉트를 보여주기 위해 생성한 **합성 연출 이미지**이며 실제 Y2C 임직원, 실제 고객사 또는 계약·수주 실적을 나타내지 않습니다.
인물·공간·자동차 이미지를 Y2C의 실제 사무실/직원/제휴 브랜드로 설명하거나 허위 레퍼런스로 사용하지 마세요.

## 사진 파일
`site/assets/images/` 안의 *.webp 파일은 사이트에서 바로 사용하는 최적화 사진 에셋입니다. 발매트·필름·방향제는 별도 제품 상세 크롭을 사용합니다. 1600px와 모바일용 960px을 모두 제공합니다. 홈페이지의 HTML 및 `site/assets/app.js`에서 사용합니다.

## Excel 업데이트와 사진의 유지
`data/website_content.xlsx`를 수정하고 GitHub에 Commit하면 `.github/workflows/main.yml`이 JSON + SEO 상세페이지를 재생성합니다.
사진 매핑은 `scripts/build_seo_pages.py`의 `SEO_VISUALS`와 `site/assets/app.js`의 `visualService`, `visualProduct`에서 관리합니다. 새로운 상품군에는 `visualProduct`의 해당 규칙 또는 별도 사진 파일을 추가하세요.

## GitHub 배포 절차
1. ZIP을 풀고 폴더 내부 전체 파일을 기존 `eunbeenlee/y2c-holdings-site` 저장소의 `main` 최상위에 업로드하세요.
2. 특히 `.github/workflows/main.yml`, `site/assets/visuals.css`, `site/assets/images/` 전체를 빠짐없이 업로드하세요.
3. `site/assets/supabase-config.js`에는 공개용 프로젝트 URL/Publishable key만 들어 있으며, 비밀번호나 `sb_secret_` 키는 없어야 합니다. 기존 배포에서 정상 로그인했다면 이 파일을 덮어쓰기 전에 현재 값과 비교해 보세요.
4. `Settings → Pages → GitHub Actions`를 확인하고 Actions의 `Publish Y2C Excel Website`가 초록색인지 확인하세요.
5. `https://y2choldings.co.kr/`, `/services.html`, `/market-research.html`, `/free-report.html`, `/admin.html`에서 화면·로그인·이미지 확인하세요.
6. 브라우저에서 구버전 이미지가 보이면 강력 새로고침(Ctrl+Shift+R)을 하세요.

## 비용
사용 이미지 파일은 자체 호스팅이며 외부 이미지 API 구독비가 없습니다. 기존 도메인 갱신비와 별도 백엔드 무료 서비스 사용 한도 조건은 계속 적용됩니다.
