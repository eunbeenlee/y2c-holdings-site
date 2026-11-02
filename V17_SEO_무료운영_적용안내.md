# Y2C HOLDINGS V17 — 무료 검색엔진 최적화 적용 안내

## 비용과 등록

- 구글 광고·네이버 광고·유료 SEO 대행 불필요
- **Google Search Console / 네이버 서치어드바이저 회원 가입·사이트 등록 없이도** 검색 로봇이 공개 페이지를 자동 발견할 수 있습니다.
- 별도의 검색엔진 계정 등록 없이 진행하는 대신 수집 상태의 상세 통계나 강제 수집 요청 기능은 제공되지 않습니다.
- **SEO는 검색 노출이나 상위 순위를 보장하지 않습니다.** 새 사이트가 자동 수집되기까지 시간이 걸릴 수 있습니다.
- GitHub Pages 공개 저장소의 기본 범위 내에서 정적 페이지와 Excel 자동 빌드를 운영합니다. 기존 가비아 도메인의 갱신 비용은 별도입니다.

## 기존 GitHub 저장소에 업로드

1. 전체 ZIP을 압축 해제합니다. ZIP 파일 자체가 아니라 **내부에 있는 전체 파일과 폴더**를 기존 저장소 `eunbeenlee/y2c-holdings-site`의 `main` 브랜치에 올립니다.
2. `.github/workflows/main.yml`, `data/website_content.xlsx`, `scripts/build_seo_pages.py`, `scripts/check_seo.py`, `site/` 등을 포함해야 합니다.
3. `Settings → Pages → Source: GitHub Actions`, Custom domain `y2choldings.co.kr` 유지.
4. `Actions → Publish Y2C Excel Website`에서 초록색 성공 표시 확인.
5. 아래 주소를 웹브라우저에서 확인합니다.

- `https://y2choldings.co.kr/`
- `https://y2choldings.co.kr/services.html`
- `https://y2choldings.co.kr/market-research.html`
- `https://y2choldings.co.kr/overseas-sales.html`
- `https://y2choldings.co.kr/buyer-development.html`
- `https://y2choldings.co.kr/sitemap.xml`
- `https://y2choldings.co.kr/robots.txt`

## 검색용 페이지 6개 × 한국어·영어

| 국문 | 영문 | 대상 검색어 |
|---|---|---|
| overseas-sales.html | overseas-sales-en.html | 해외영업 대행 / international sales development |
| market-research.html | market-research-en.html | 해외시장조사 / international market research |
| buyer-development.html | buyer-development-en.html | 해외 바이어 발굴 / buyer discovery |
| export-consulting.html | export-consulting-en.html | 수출 컨설팅 / export consulting |
| supply-chain.html | supply-chain-en.html | 해외 소싱·공급망 / international sourcing |
| franchise-development.html | franchise-development-en.html | 해외 프랜차이즈 사업개발 / franchise development |

목록 페이지는 `services.html` 및 `services-en.html`입니다. 별도 회원 가입이나 키가 필요 없습니다.

## 앞으로 Excel만 업데이트하기

`data/website_content.xlsx`의 **`검색서비스`** 시트에서 각 페이지의 제목, 검색 설명, 소개, 서비스 범위, 산출물, 진행절차, FAQ, 공개여부를 수정합니다.

- `slug`는 주소이므로 기존 값 변경 비추천 (기존 검색 주소가 끊길 수 있음).
- `scope_ko/en`, `deliverables_ko/en`, `process_ko/en`의 항목은 `|`로 구분.
- `visible`은 `Y` 또는 `N`으로 설정. `N`은 다음 빌드의 사이트맵에는 제외되지만, 기존 공개 파일을 삭제하지 않는 한 오래된 페이지가 남을 수 있으니 관리자가 GitHub에서 해당 파일을 직접 제거해야 합니다.
- 공개 Excel에는 내부 계약·수수료·고객 연락처·회사 기밀을 넣지 마세요.
- Excel을 변경한 다음 GitHub에 Commit하면 정적 검색 페이지와 사이트맵이 자동 갱신됩니다.

## 주요 SEO 조치

- 정적 HTML 본문과 페이지별 고유 `<title>`, 검색 설명, `<h1>`
- 각 국문·영문 페이지의 canonical / hreflang / 공유 메타
- 서비스별 구조화 데이터(JSON-LD, 공식 실적·인증·평점 주장 없음)
- 내부 서비스 연결 링크, 무료 진단 및 가격표로 이어지는 안내
- `robots.txt`와 18개 공개 URL을 포함하는 `sitemap.xml`
- 관리자 페이지는 `noindex` 상태이며 사이트맵에서 제외

## 한계 및 운영

- 유료 광고를 쓰지 않는다고 순위가 낮아지는 것은 아닙니다. 다만 공개 문서의 품질, 다른 신뢰 가능한 사이트의 자연 링크, 검색엔진 수집 시점이 중요합니다.
- 실제 고객사 수행사례가 확보되면 사전 동의와 증빙을 갖추어 별도 **실제 사례** 페이지를 작성하는 것이 좋습니다. 지금은 확인되지 않은 실적·고객사를 넣지 않았습니다.
- 파트너 문의 폼의 실제 수신은 기존 버전처럼 별도 설정이 필요합니다.
- `site/assets/supabase-config.js`에는 Supabase 공개용 Publishable key만 있으며 관리용 비밀키는 넣으면 안 됩니다.
- `robots.txt`와 `noindex`는 인증/보안기능이 아니며 비공개 데이터는 반드시 Supabase 인증·RLS를 사용해야 합니다.

## 공식 참고

- Google Search Central: https://developers.google.com/search/docs/fundamentals/seo-starter-guide?hl=ko
- 네이버: https://searchadvisor.naver.com/guide/faq-start-register
- 네이버 메타 태그: https://searchadvisor.naver.com/guide/seo-help
- GitHub Pages: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
