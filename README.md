# Y2C HOLDINGS | Corporate Website & Secure Report Studio V12

## 주요 구성

- **공식 홈페이지**: `site/index.html` — 사업영역, 상품안내, KR/EN 전환
- **관리자 로그인**: `site/admin.html` — Supabase Auth 회사 계정 + `y2c_admins` 승인 검증
- **시장조사 보고서**: 표준 양식 기반 13개 기본 조사영역, 3개 산업별 선택 모듈
- **작성·관리 기능**: 목록·검색·초안/검토/최종·자동 임시저장·수동 저장·복제·PDF/인쇄·JSON 내보내기
- **공개용 엑셀**: `data/website_content.xlsx` 변경 후 GitHub Actions 자동 생성
- **민감한 보고서**: 공개 GitHub에 저장하지 않고 Supabase `y2c_reports`(RLS)에만 저장
- **백업/상태점검**: V11의 암호화 이메일 백업 및 DB 점검 GitHub Actions 보존
- **도메인**: `y2choldings.co.kr` (`site/CNAME`)

## 가장 중요한 사항: 기존 Supabase 설정 유지

이 배포 패키지는 **`site/assets/supabase-config.js`를 일부러 포함하지 않습니다.**

이유: 사용자 GitHub 저장소에 이미 입력한 Supabase 프로젝트 URL과 **공개용 Publishable key**를 ZIP 재업로드가 덮어쓰지 않도록 보호하기 위해서입니다.

1. 기존 GitHub 저장소 `eunbeenlee/y2c-holdings-site`를 **삭제하지 마세요**.
2. 이 ZIP의 내부 파일을 기존 저장소 `main` 브랜치 최상위에 업로드·덮어쓰세요.
3. 기존 `site/assets/supabase-config.js`는 GitHub에 그대로 남겨 둡니다.
4. 새 저장소에서 시작해야 한다면 `site/assets/supabase-config.example.js`를 복사해 `supabase-config.js`로 이름을 바꾸고, 공개 URL과 Publishable key만 입력합니다.
5. **비밀번호, `sb_secret_` 또는 service_role 키를 공개 웹파일에 넣지 마세요.**

## 기존 Supabase에 이미 설치한 테이블

`public.y2c_admins`, `public.y2c_reports`를 그대로 사용하며 **추가 SQL 실행이 필수는 아닙니다**. 계정이 이미 승인되었다면 다시 생성하지 마세요.

관리자 기본 로그인 이메일: `eunbeen.lee@y2choldings.co.kr` (Supabase에서 실제 생성한 계정과 동일한 비밀번호 사용).
로그인을 허용하려면 `auth.users`와 `y2c_admins(user_id,role,active)`가 일치하고 `active=true`여야 합니다.

## 배포

자세한 설명: `QUICK_START_KR.md`

- GitHub `Settings → Pages → Source = GitHub Actions`
- GitHub Actions `Publish Y2C Excel Website` 실행 성공 확인
- `https://y2choldings.co.kr/admin.html` 접속
- Supabase 회사 계정 로그인 → `새 보고서 작성` → 항목 입력 → `지금 저장`
- 보고서 재접속·조회 및 PDF 출력 테스트

## 무료 운용 조건

GitHub Pages(공개 저장소), Supabase Free, GitHub Actions 무료 할당량을 전제로 합니다. 도메인 갱신비와 외부 이메일/프로젝트의 무료 한도는 별도입니다. Supabase 무료 프로젝트 비활동 중지와 GitHub 예약 작업 중단 가능성은 남아 있으므로 정기 점검과 암호화 백업 복구 테스트를 해야 합니다.

## 주의

- 새 회사 계정 등록은 `Authentication → Users`에서 관리자가 직접 수행합니다. 일반인 자동 가입을 켜지 마세요.
- 비밀번호/고객사 정보가 포함된 내부 통합 관리 Excel은 절대 공개 GitHub 저장소에 올리지 마세요.
- 로그인 페이지 파일은 공개되지만, **보고서 접근 권한은 서버측 RLS**에서 강제됩니다.
- 이 패키지의 실제 Supabase 운영 계정 로그인·DB 저장은 계정 접근 권한이 없어 여기서는 수행하지 못했습니다. 브라우저 모의 데이터 테스트와 코드 검증은 진행했습니다.
