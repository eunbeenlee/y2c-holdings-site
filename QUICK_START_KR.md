# Y2C HOLDINGS V8 — GitHub 교체 / Excel 수정

저장소: https://github.com/eunbeenlee/y2c-holdings-site

## 1. 기존 GitHub 저장소에 올리기 (추천: GitHub Desktop)

1. GitHub Desktop에서 `eunbeenlee/y2c-holdings-site`를 **Clone**합니다.
2. 이 ZIP 파일을 별도 폴더에 압축 해제합니다.
3. ZIP의 **내부 폴더·파일 전체**를 로컬 저장소의 **최상위 폴더**에 덮어씁니다. `.git` 폴더는 삭제하지 마세요.
4. `.github/workflows/main.yml`, `site/index.html`, `data/website_content.xlsx`, `scripts/build_site_data.py`, `tests/test_pipeline.py`가 저장소 최상위에서 확인되어야 합니다.
5. 이전 버전의 `.github/workflows/deploy.yml`이 있다면 **삭제**해 중복 실행을 막습니다. 현재 패키지는 `main.yml` 하나를 사용합니다.
6. GitHub Desktop에서 변경사항을 확인하고 `Y2C corporate website V8`로 Commit → Push origin 합니다.
7. GitHub `Settings → Pages → Build and deployment → Source = GitHub Actions`를 확인합니다.
8. `Actions → Publish Y2C Excel Website`의 최신 실행 결과가 초록색인지 확인합니다.

> 압축파일 자체를 GitHub에 업로드하지 마세요. ZIP 속 **파일**을 업로드해야 합니다. 웹 업로드를 사용하면 숨김 폴더 `.github`의 누락에 주의하세요.

## 2. 홈페이지 수정 (Excel만)

`data/website_content.xlsx`를 열고 `설정`(메인/회사/산업/섹션 문구), `서비스`(4개 사업영역), `진행절차`, `파트너`를 수정합니다.

- `설정`의 `ko`·`en`은 각각 홈페이지 언어 토글에 대응합니다.
- `<br>`은 제목의 줄바꿈으로 쓸 수 있습니다.
- 행 숨기기는 `visible` 열에서 `N`, 공개는 `Y`로 설정합니다.
- **시트명과 1행 열 제목은 변경하지 마세요.**
- 수정한 파일을 같은 위치에 Commit/Push하면 GitHub Actions가 JSON을 재생성하고 사이트를 배포합니다.
- 산업 카드의 개수/그래픽이나 화면 레이아웃을 변경할 때는 HTML/CSS 작업이 필요합니다.

## 3. 홈페이지 주소

https://eunbeenlee.github.io/y2c-holdings-site/

URL은 배포 완료 후에 작동합니다. 기존 Pages가 404인 경우 먼저 Actions 오류를 확인하세요.

## 4. 광고 시작 전 필수

- 법인 공식 이메일 또는 보안된 문의 접수 API 연결
- 실제 수신·보유·파기 절차에 맞는 개인정보처리방침 확정
- 국가별 개인정보 규정과 광고·수신거부 정책 점검
- 실제 계약이나 검증되지 않은 공급품에 대해 확정 납품·파트너십 표현 금지

**현재는 문의 내용 복사 기능만 정상 동작하며 자동 접수되지 않습니다.**

## 5. 에러 시 확인

- Actions의 빨간 X → 실행 클릭 → 실패 단계 로그
- `main.yml`과 `deploy.yml` 중복 여부 확인
- 파일이 루트가 아니라 추가 하위 폴더에 업로드되지 않았는지 확인
- 수정한 공개 Excel에 개인정보·내부 단가 포함 여부 확인
- 브라우저 캐시: `Ctrl + Shift + R`
