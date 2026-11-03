# Y2C HOLDINGS · V20 Full Revision

기존 골드·차콜·오프화이트와 원본 로고를 유지한 전체 소스입니다. 파란색 시안이나 다른 로고를 사용하지 않습니다.

## 바로 적용하기

1. ZIP을 `C:\Y2C` 등 짧은 경로에 압축 해제합니다. ZIP 내부에는 긴 상위 폴더를 두지 않았습니다.
2. 기존 저장소 `eunbeenlee/y2c-holdings-site`의 `main`에 **내부 파일과 폴더**를 같은 경로로 업로드합니다. `.github`도 포함합니다. 저장소 자체를 지우지 마세요.
3. 최근에 Supabase URL/공개 키를 변경했다면 **현재 저장소의 `site/assets/supabase-config.js`를 먼저 보관**하고 해당 파일만 기존 최신 값을 유지합니다. 이번 소스는 이전 대화에서 제공된 공개 연결값을 사용합니다. 비밀번호·서비스 비밀키는 포함하지 않았습니다.
4. `Settings → Pages → Source: GitHub Actions`, Custom domain: `y2choldings.co.kr`를 유지합니다.
5. `Publish Y2C Excel Website`가 성공한 뒤 사이트를 강력 새로고침합니다. 브라우저 업로드가 한 번에 전부 안 되면 `.github`, `data`, `scripts`, `site`, `supabase`, `tests`, `docs` 순으로 폴더별 업로드한 뒤 마지막 배포 결과를 확인합니다.

**기존 SQL·관리자 계정은 다시 만들지 않습니다. 데이터베이스를 초기화하거나 기존 보고서를 지우는 마이그레이션은 없습니다.**

## 유지한 기능

- 회사 홈페이지 / 한국어·영어 정적 페이지 / 서비스별 상세페이지
- 공개 Excel 콘텐츠 빌드 / 상품 필터 / 요금 안내 / 간편 견적
- 무료 시장진출 사전진단 / 선택형 유료조사 견적
- 회사 계정 로그인 / 보고서 작성·저장·등급·복제·삭제·인쇄
- 기존 백업 이메일·DB 활동 점검 워크플로 및 Secrets 이름
- 도메인, robots.txt, sitemap.xml, canonical/hreflang

## 콘텐츠와 이미지 변경

`data/website_content.xlsx`는 공개 홈페이지용입니다. 민감한 고객·계약·계정 데이터를 넣지 않습니다.

- 회사 문구: `설정` 시트
- 상품 이름·노출: `상품` 시트 (현재 4종 공개; 트렁크 라이너는 별도 이미지/사양 확인 전 비공개)
- 서비스/요금/무료 진단 선택지/SEO: 기존 해당 시트
- **사진 연결: `이미지맵` 시트** — `key`, `src`, `alt_ko`, `alt_en`, `position`, `kind`, `visible`
- 사진 파일은 `site/assets/images/`에 추가하고 `src`는 `assets/images/파일명.webp`로 입력합니다.
- 공개 상품이나 사업영역의 이미지 매핑이 없으면 빌드가 실패합니다. 무관한 기본 이미지를 임의로 대신 넣지 않습니다.
- 드롭다운 유료조사 세부 옵션/추가금은 기존 `site/data/quick-report-options.json`에서 관리합니다. 기본금 199,000원은 이 파일과 메인 안내에 함께 맞춥니다.

수정한 Excel을 GitHub에 Commit해야 공개 사이트에 반영됩니다. PC에서 저장만 해서는 갱신되지 않습니다.

## 검증 및 운영 범위

`docs/QA_V20.md`를 먼저 확인하세요. 소스·빌드·화면 검증과 실제 운영 시스템의 검증은 구분했습니다.

- 이 패키지는 GitHub에 자동 업로드하지 않습니다.
- 실제 계정 로그인/DB 쓰기/백업 발송은 운영 계정 권한 없이 실행하지 않았습니다.
- 문의 폼은 **메일 앱 열기 + 내용 복사**입니다. 메일 앱에서 직접 전송해야 하며 자동 접수·결제 기능이 아닙니다.
- 무료 진단서는 선택 규칙 기반 사전점검이며 실시간 시장조사 결과나 관세 확정 의견이 아닙니다.
- 사진은 기존 생성 이미지를 업무/제품에 맞게 재편집한 **설명용 연출 이미지**입니다. 실제 직원·고객·공장·납품 상품의 촬영 실적으로 표시하지 않습니다.
- 별도 유료 플러그인을 추가하지 않았습니다. 기존 서비스 무료 한도와 도메인 비용은 별도이며 영구 무료·무중단을 보장하지 않습니다.

## 로컬 빌드

```sh
python scripts/build_site_data.py --excel data/website_content.xlsx --output site/data/site-data.json
python scripts/build_seo_pages.py --excel data/website_content.xlsx --site site
python scripts/build_home.py
python -m unittest discover -s tests -v
python scripts/check_site.py
python scripts/check_assets.py
python scripts/check_seo.py
python -m http.server 8000 --directory site
```

Python 표준 라이브러리만으로 공개 Excel을 읽고 사이트를 빌드합니다. 관리자 로그인 라이브러리와 웹폰트는 기존 CDN 경로를 이용하며 네트워크가 필요합니다. 폰트 파일 자체는 포함하지 않았습니다.
