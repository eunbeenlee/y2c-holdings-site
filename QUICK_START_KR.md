# Y2C HOLDINGS V9 — GitHub + 보고서 관리자 연결

## 핵심 안내

- 사이트: `https://y2choldings.co.kr` (도메인 DNS와 GitHub Pages 배포 성공 시)
- 저장소: `https://github.com/eunbeenlee/y2c-holdings-site`
- 공개 상품 Excel: `data/website_content.xlsx` → 상품 시트
- 관리자 주소: `https://y2choldings.co.kr/admin.html`
- 관리자 DB: 별도 Supabase 프로젝트 (실제 연결 전에는 로그인 불가)
- **GitHub의 공개 Excel에 ID, 비밀번호, 계약서, 고객 보고서를 업로드하면 안 됩니다.**

## A. 공개 사이트 업로드

1. ZIP을 풀어 저장소 **최상위에 있는 기존 파일 전체**를 교체합니다. `.github` 숨김 폴더도 포함합니다.
2. `Settings → Pages → Source: GitHub Actions`를 선택합니다.
3. `Actions`에서 `Publish Y2C Excel Website` 실행의 성공 여부를 확인합니다.
4. 홈페이지에서 **상품 소싱 안내** 섹션을 열어 상품 5종이 보이는지 확인합니다.
5. 나중에 `data/website_content.xlsx`의 `상품` 시트를 수정하고 commit 하면 상품 카탈로그가 자동 갱신됩니다.

## B. 관리자 전용 보고서 저장 연결 — 직접 한 번 설정해야 합니다

1. `https://supabase.com/dashboard`에서 신규 프로젝트를 생성합니다. **프로젝트 비밀번호와 secret/service_role 키를 GitHub에 넣지 마세요.**
2. Supabase 대시보드 → `SQL Editor` → `supabase/01_schema.sql` 전체를 붙여 넣고 실행합니다.
3. `Authentication → Users`에서 **관리자 이메일 계정을 직접 생성**합니다. 실제 로그인 비밀번호는 Supabase Auth만 관리합니다. 공유 로그인 계정 대신 관리자별 계정을 권장합니다.
4. `supabase/02_approve_admin_example.sql` 파일에서 `REPLACE_WITH_ADMIN_EMAIL@example.com`을 실제 관리자 이메일로 바꾼 뒤 SQL Editor에서 실행합니다. 결과 행이 1개 나와야 합니다. 이를 생략하면 로그인해도 보고서 접근이 거부됩니다.
5. `Project Settings → API` 또는 `Connect` 메뉴에서 `Project URL`과 **publishable/anon key**를 확인합니다. *service_role / secret key는 절대 사용하지 마세요.*
6. `site/assets/supabase-config.js`의 빈 값에 다음과 같이 입력한 뒤 GitHub에 commit 합니다.

   ```js
   window.Y2C_ADMIN_CONFIG = {
     url: 'https://YOUR_PROJECT_REF.supabase.co',
     publishableKey: 'YOUR_PUBLISHABLE_OR_ANON_KEY'
   };
   ```

   URL과 publishable key는 **공개 가능한 프로젝트 식별 값**이며, 보고서 보호는 **Auth 로그인과 RLS 권한검증**에서 수행합니다.
7. Supabase `Authentication → URL Configuration`의 Site URL을 `https://y2choldings.co.kr`로 설정하고 필요 시 Redirect URLs에 `https://y2choldings.co.kr/**`를 추가합니다.
8. 브라우저에서 `https://y2choldings.co.kr/admin.html`에 접속해 만든 계정으로 로그인합니다. 새 보고서 → 작성 → 저장 → 목록 재조회로 DB 저장 여부를 검증합니다.
9. 외부 사용자/비승인 계정으로 로그인했을 때 보고서 접근이 차단되는지 확인합니다.

> 주의: 이 패키지는 **관리자 UI + SQL 설정 파일**까지 구성했습니다. 실제 Supabase 프로젝트 생성·관리자 초대·SQL 적용·키 입력은 사용자 계정에서 해야 하므로 배포 직후 자동으로 로그인되는 것은 아닙니다.

## C. 관리자 기능

- 이메일/비밀번호 로그인, 승인 계정만 접근
- 보고서 제목·고객사·국가·업종·초안/검토/최종 상태 관리
- 시장조사 표준 13개 섹션을 웹에서 직접 작성 및 수정
- DB 저장, 보고서 목록/검색, JSON 별도 백업, 브라우저 인쇄/PDF
- 삭제는 `admin` 역할만 허용

## D. 안전하게 운영하는 기준

- 웹사이트 public repository에 Excel 비밀번호·내부 V3 관리파일·고객정보를 올리지 않습니다.
- `service_role`, `sb_secret_*`, 데이터베이스 비밀번호, GitHub PAT 등을 HTML/JavaScript/Excel에 넣지 않습니다.
- Supabase Table Editor에서 민감한 데이터가 들어 있는 테이블은 반드시 RLS 상태를 확인합니다.
- DB 백업, 직원 퇴사 시 계정 비활성화, 관리자별 개별 계정, 다중요소 인증 제공 여부 검토가 필요합니다.
- 현재 공개 제휴 문의 폼은 별도 접수 DB가 연결되지 않았습니다. 완료된 등록접수처럼 안내하면 안 됩니다.
- GitHub Pages는 정적 호스팅이므로 서버의 엑셀 파일을 비공개 DB처럼 쓰는 구조를 지원하지 않습니다.


## E. 무료 이메일 자동백업
자세한 설정은 `BACKUP_EMAIL_SETUP_KR.md`를 참고합니다. GitHub Actions Secrets 5개를 설정한 뒤 수동 실행으로 첫 메일 수신과 복호화를 검사하세요.
