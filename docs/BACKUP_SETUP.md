> V20 안내: 기존 기능의 설정 방법입니다. 실제 발송/DB 접속은 배포 후 Secrets와 계정으로 확인해야 합니다. 무료 서비스의 일시 중지나 예약작업 지연 가능성이 없어지는 것은 아닙니다.

# Y2C HOLDINGS — 무료 이메일 자동백업 설정 (V10)

## 제공 기능
- 기존 Y2C GitHub Pages 홈페이지 및 공개 Excel 변경 없음
- `main.yml` 홈페이지 배포와 별개로 `backup-email.yml`에서 매일 03:17(한국시간) 예약 실행
- Supabase 공식 CLI로 `public` 스키마 정의+데이터를 각각 SQL로 추출
- ZIP 압축 후 AES-256-GCM으로 암호화, Gmail SMTP를 통해 첨부파일 발송
- 데이터베이스 비밀번호 및 메일 앱 비밀번호는 **GitHub Actions Secrets**에만 저장
- 공개 저장소, commit, GitHub Artifact, 실행 로그에 원본 데이터 백업하지 않음
- 실패 시 첨부파일 없는 실패 알림 이메일 시도
- `Actions → Y2C Secure Daily Database Backup → Run workflow`에서 수동 실행 가능

## 1. Github 저장소에 적용
`Y2C_HOLDINGS_Portal_V10_Email_Backup` ZIP 내부 파일을 기존 `eunbeenlee/y2c-holdings-site` 저장소 최상위에 업로드합니다. 특히 `.github/workflows/backup-email.yml`과 `scripts/backup/email_backup.py`를 확인하세요. **기존 자동 배포 `main.yml`은 변경하지 않았습니다.**

## 2. Supabase 데이터베이스 연결 문자열
Supabase Dashboard → 해당 프로젝트 → **Connect** → Connection string, `Session pooler` 모드의 PostgreSQL URI를 복사합니다. GitHub-hosted runner는 IPv4 환경일 수 있어 무료 프로젝트에서는 Supabase 공식 문서의 shared pooler session mode(:5432)가 현실적입니다. `postgresql://postgres.[PROJECT_REF]:[DB_PASSWORD]@[POOLER_HOST]:5432/postgres` 형태이며, 대괄호/호스트를 추측하지 말고 Supabase 콘솔의 값을 사용하세요. 비밀번호에 특수문자가 있으면 URL 인코딩이 필요합니다.

## 3. GitHub Actions Secrets 5개
`Settings → Secrets and variables → Actions → New repository secret`에서 설정합니다.

| Secret 이름 | 내용 | 주의 |
|---|---|---|
| `Y2C_SUPABASE_DB_URL` | Supabase 세션 풀러 연결 문자열 | DB 비밀번호 포함. 절대 코드에 붙여넣지 않음 |
| `Y2C_BACKUP_PASSWORD` | **16자 이상, 길고 고유한 암호화 비밀번호** | 이메일로 전송하지 않음. 잃으면 백업 복구 불가 |
| `Y2C_SMTP_USER` | 발송용 Gmail 주소 | 계정 직접 준비 |
| `Y2C_SMTP_APP_PASSWORD` | Gmail 앱 비밀번호 | Google 계정 2단계 인증 이후 발급 가능한 경우 사용 |
| `Y2C_BACKUP_TO` | 백업 수신 이메일 주소 | 회사 이메일 등 본인 제어 계정 |

**GitHub Pages URL, `site/assets/supabase-config.js`, 공개 Excel에는 위 Secret들을 입력하지 마세요.** Secret은 GitHub Actions 런타임에만 주입합니다. GitHub `Actions` 실행 화면이 보이는 누구에게도 로그에서 비밀번호가 출력되지 않아야 합니다.

Gmail 앱 비밀번호는 모든 Google 계정에서 생성 가능한 것은 아닙니다. 사용 불가능하면 별도 발송 서비스의 무료 SMTP 한도 또는 OAuth 기반 발송 방식으로 조정해야 합니다. 일반 Gmail 비밀번호 입력은 금지합니다.

## 4. 실행과 확인
- GitHub Actions 화면에서 `Y2C Secure Daily Database Backup` → `Run workflow` 1회 실행
- 성공 시 수신함에 `Y2C_<YYYY-MM-DD>.y2cbackup` 파일 도착
- `Actions`에서 성공한 실행 확인 (단, 이메일 수신 자체까지 GitHub가 증명하지는 못함)
- 실제 복구 가능성 검증을 위해 아래 복호화 테스트 필수

## 5. 백업 파일 복호화
컴퓨터에 Python 3.12 및 `cryptography` 설치 후, 백업 ZIP의 `scripts/backup/email_backup.py` 사용:

```bash
pip install cryptography
# macOS/Linux; Windows PowerShell에서는 $env:BACKUP_PASSWORD="..." 방식
export BACKUP_PASSWORD='별도 보관한 비밀번호'
python scripts/backup/email_backup.py decrypt --input Y2C_2026-11-02.y2cbackup --output ./recovery
```

결과: `public_schema.sql`, `public_data.sql`, `manifest.json`. SQL 파일에는 고객·보고서가 포함될 수 있으므로 외부 공유 및 GitHub 업로드 금지. 복호화 확인 이후 민감한 평문 파일은 안전하게 삭제하세요.

### 실제 DB 복구 주의
Supabase CLI 공식 복구 안내를 따라 **테스트 프로젝트**에서 schema/data 복구 검증 후 본 DB를 복구해야 합니다. `public.y2c_reports.created_by`와 `y2c_admins.user_id`는 `auth.users`를 참조하므로, **Auth 사용자 목록/계정은 이 백업에 포함되지 않으며** 신규 프로젝트에서는 사용자 계정 복원/ID 재연결이 필요합니다. 파일 스토리지도 별도입니다. 실서비스 프로젝트에 무작정 SQL을 실행하지 마세요.

## 6. 무료 플랜의 한계
- GitHub Actions 예약 실행은 지연/누락될 수 있으며 공개 저장소가 60일간 비활동이면 예약 실행이 비활성화될 수 있습니다.
- Supabase Free는 비활동 7일 후 일시 중지될 수 있습니다. 중지되면 백업 실패 알림이 오도록 시도합니다.
- Gmail 개인 계정 첨부파일 제한은 25MB입니다. 안전을 위해 암호화된 파일이 **14MiB 이상**이면 이메일 발송을 중단하고 실패 알림만 시도합니다.
- SMTP 로그인 정보가 바뀌거나 이메일 서비스 장애가 발생하면 **성공/실패 이메일 모두 못 받을 수 있으므로 Actions 실행내역을 정기 확인**하세요.
- Auth 사용자 계정, Storage 파일은 백업 범위에 포함되지 않습니다.
- 이메일 수신함 하나에만 장기 보관하지 말고, 복구용 사본을 다른 보호된 저장소에도 두는 것이 좋습니다.
- 개인정보가 포함된 백업을 이메일로 보내기 전에 수신 주소와 개인정보 보유·보호 정책을 확인하세요.

공식 참고: https://supabase.com/docs/guides/deployment/ci/backups
https://supabase.com/docs/guides/platform/migrating-within-supabase/backup-restore
https://docs.github.com/actions/reference/events-that-trigger-workflows
