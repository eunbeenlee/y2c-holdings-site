# Y2C V12 — GitHub에 전체 파일 교체하는 순서

## 사전 상태

- 저장소: https://github.com/eunbeenlee/y2c-holdings-site
- 도메인: https://y2choldings.co.kr
- Supabase Free 프로젝트는 생성됨
- SQL `01_schema.sql` 실행 및 회사 관리자 계정 승인도 이미 완료됨
- 지난번 GitHub에 `site/assets/supabase-config.js`를 직접 수정한 상태

**이번 설치에서는 비밀번호·공개키를 새로 만들거나 SQL을 다시 실행할 필요가 없습니다.**

## 1. 기존 Supabase 설정 보호 (중요)

GitHub 저장소에서 이 주소가 열리는지 먼저 확인합니다:

https://github.com/eunbeenlee/y2c-holdings-site/blob/main/site/assets/supabase-config.js

이 파일은 이전에 직접 입력한 URL/Publishable key가 저장된 것으로 간주합니다. **이번 ZIP에는 해당 파일을 포함하지 않았으므로**, 새 파일을 업로드해도 기존 파일이 유지됩니다. 다른 경로로 저장소 전체를 삭제 후 재생성하면 로그인 설정을 잃습니다.

## 2. ZIP 업로드

1. ZIP 압축을 풉니다.
2. 내부의 `.github`, `data`, `scripts`, `site`, `supabase`, `tests`와 README 등 전체 내용을 저장소 루트에 올립니다. ZIP 자체를 업로드하지 않습니다.
3. 변경사항을 `main`에 커밋합니다. 기존 `site/assets/supabase-config.js` 파일은 **삭제하지 않습니다**.
4. 원격에 과거 `deploy.yml` 등 중복 배포 워크플로가 있다면 확인하여 `main.yml` 하나만 Pages 배포에 사용합니다. 백업/keepalive 워크플로는 별도 기능이므로 유지합니다.
5. GitHub 웹 업로드가 중복 파일 교체에 실패하면 GitHub Desktop에서 저장소 Clone → 압축 해제 파일 덮어쓰기 → Commit → Push 방법을 사용하세요.

## 3. GitHub Pages 확인

- https://github.com/eunbeenlee/y2c-holdings-site/settings/pages
- Source: `GitHub Actions`
- Custom domain: `y2choldings.co.kr`
- DNS 레코드는 가비아에 이미 등록되어 있으므로 다시 수정하지 않습니다.
- https://github.com/eunbeenlee/y2c-holdings-site/actions 에서 `Publish Y2C Excel Website`의 최신 실행이 초록색인지 확인합니다.
- 새 테스트는 공개 Supabase 키가 들어 있어도 실패하지 않도록 수정했습니다.

## 4. 회사 관리자 로그인

1. `https://y2choldings.co.kr/admin.html`로 접속합니다.
2. 회사 계정 `eunbeen.lee@y2choldings.co.kr`과 **Supabase에서 만든 비밀번호**로 로그인합니다.
3. 로그인이 거부되면 Supabase `Authentication → Users`의 계정 이메일/확인 상태와 `Table Editor → y2c_admins`의 `active=true`, `role=admin`을 확인합니다. 계정 권한은 사용자 ID(UUID)로 연결됩니다.
4. 새 사용자 공개 회원가입은 필요하지 않으며 기본 비활성화를 권장합니다.
5. Supabase `Authentication → URL Configuration`: Site URL = `https://y2choldings.co.kr`, 추가 Redirect URL = `https://y2choldings.co.kr/**`.

## 5. 보고서 저장 테스트

1. `새 보고서 작성`을 클릭합니다.
2. 제목, 고객사, 국가, 산업 분야를 입력합니다.
3. 01번 `요약 및 최종 판단`을 입력하고 `지금 저장`을 클릭합니다.
4. 왼쪽 보고서 목록에 생성된 제목이 표시되고, `저장 완료`가 나타나는지 확인합니다.
5. 새로고침하고 동일 보고서를 선택해 내용이 유지되는지 확인합니다.
6. 항목을 수정하면 약 4.5초 뒤 자동 저장됩니다. 저장 실패 시 화면에 오류가 나타나므로 JSON으로 내보내 백업하세요.
7. `PDF / 인쇄` 버튼을 클릭한 뒤 브라우저의 `PDF로 저장`을 선택합니다.

## 6. SQL 참고

이미 V11의 `supabase/01_schema.sql`을 실행했다면 **반복 실행할 필요가 없습니다**. 이 패키지에 SQL은 신규 설치 또는 복구 시 참고용으로 유지합니다.

## 7. 자동 이메일 백업 및 DB 점검 (선택적으로 활성화)

기존 V11의 3개 워크플로를 유지합니다:

- `backup-email.yml`: 암호화된 public 스키마 백업을 회사 이메일로 전송
- `supabase-keepalive.yml`: Supabase DB 상태 점검
- `repo-activity.yml`: GitHub 예약 실행 비활성화 위험 완화

설정은 `BACKUP_EMAIL_SETUP_KR.md` 및 `SUPABASE_자동활동점검_설치안내.md`를 따릅니다. 이 기능은 GitHub Secrets 없이는 실행되지 않으며, 로그인과 보고서 사용에는 **필수 조건이 아닙니다**.

## 8. 공개용 Excel 수정

`data/website_content.xlsx`를 수정하고 GitHub에 Commit하면 홈페이지 공개 콘텐츠가 자동 재생성됩니다. 보고서 원본과 로그인 정보는 **절대로** Excel이나 공개 GitHub에 저장하지 않습니다.

## 실패 시 점검 경로

- 빌드 실패: Actions → `Publish Y2C Excel Website` → `build-and-deploy` → 실패 단계 펼치기
- 로그인 화면 대신 설정 필요: `site/assets/supabase-config.js` 보존 여부와 실제 Project URL/공개 키
- 로그인 오류: 비밀번호, Supabase `auth.users` 이메일 확인, 회사 도메인
- 로그인은 되는데 권한 없음: `y2c_admins` 승인/활성 상태 및 UID 일치 여부
- 저장 오류: Supabase RLS 및 `y2c_reports` 테이블 존재 여부
