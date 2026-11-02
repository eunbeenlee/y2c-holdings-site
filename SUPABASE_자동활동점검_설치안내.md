# Y2C HOLDINGS — Supabase 무료 프로젝트 자동 활동 점검 V11

## 목적
관리자가 매일 로그인하지 않아도 무료 Supabase 프로젝트에 실제 DB 읽기 요청을 주기적으로 보내 비활동 일시 중지 가능성을 **낮춥니다**. 단, Supabase 무료 플랜의 중지를 완전히 방지한다는 보장은 없습니다.

- 기존 회사 홈페이지와 공개 Excel, 보고서 관리자 페이지, V10 암호화 이메일 백업 코드는 변경하지 않음
- `Y2C Supabase Activity Monitor` GitHub Actions 워크플로: 하루 3회, 한국시간 **09:23, 17:23, 익일 01:23**
- PostgreSQL `public.y2c_reports` 실제 테이블에서 **1행만 읽기** (데이터가 없더라도 DB 요청을 수행). INSERT/UPDATE/DELETE 없음.
- 연결 실패 시 3회 재시도 → 계속 실패 시 Y2C 회사 이메일로 경고 발송 시도
- 정상 점검 시 메일을 보내지 않음(메일 과다 발송 방지)
- 기존 `backup-email.yml`은 매일 03:17 한국시간 별도 백업/이메일 발송

## 파일 추가
기존 GitHub `eunbeenlee/y2c-holdings-site` 저장소 루트에 아래 파일 **4개**를 추가하세요.

```
.github/workflows/supabase-keepalive.yml
.github/workflows/repo-activity.yml
scripts/monitor/supabase_keepalive.py
scripts/monitor/test_keepalive.py
```

- 다른 V9/V10 소스파일을 덮어쓸 필요가 **없는 추가 전용 ZIP**도 함께 제공합니다.
- 파일을 `.github/workflows/` 등에 올바르게 업로드했는지 확인하세요. 루트에 추가 상위 폴더가 생기지 않게 하세요.

## GitHub Secrets — V10 백업과 공유
GitHub 저장소 → Settings → Secrets and variables → Actions에서 아래 값이 있는지 확인합니다.

| Secret | 용도 |
|---|---|
| `Y2C_SUPABASE_DB_URL` | Supabase Dashboard `Connect → Session pooler`의 실제 PostgreSQL URI. DB 비밀번호 포함. **공개 금지** |
| `Y2C_SMTP_USER` | 경고 이메일 발송 Gmail 주소 |
| `Y2C_SMTP_APP_PASSWORD` | Gmail 앱 비밀번호 |
| `Y2C_BACKUP_TO` | Y2C 회사 이메일 수신 주소 |

기존 백업의 `Y2C_BACKUP_PASSWORD`는 이번 활동 점검에는 필요 없지만 **V10 백업 작업에는 계속 필요**합니다. 이미 설정한 Secrets는 중복 생성하지 않습니다.

**중요:** DB URI, Gmail 앱 비밀번호를 채팅이나 스크린샷으로 공유하지 마세요. `site/`, Excel, HTML, JSON이나 공개 GitHub 코드에 붙이지 마세요.

## 검증 순서
1. Supabase Dashboard에서 Free 프로젝트가 **Active** 상태인지 확인합니다. 아직 프로젝트를 생성하지 않았다면 먼저 프로젝트 생성/스키마 설치가 필요합니다.
2. GitHub → Actions → **Y2C Supabase Activity Monitor** → `Run workflow`로 수동 시험합니다.
3. 최신 실행이 초록색인지 확인하고 `Check Supabase database` 단계에서 `read-only check OK`가 나오는지 봅니다.
4. Actions → **Y2C Secure Daily Database Backup**에서도 별도로 `Run workflow`를 실행해 회사 이메일에 백업이 도착하는지 확인합니다.
5. Supabase가 이미 `Paused` 상태라면 자동으로 복구되지 않습니다. Dashboard → `Resume project`를 누르고 Secrets 설정을 확인한 뒤 다시 실행하세요.

## GitHub 60일 비활성 중지 완화 로직 (추가)
- `.github/workflows/repo-activity.yml`을 별도 작업으로 추가합니다.
- **매월 1일 09:41 KST**, 최근 커밋이 20일 이상 없으면 내용 변경 없이 `github-actions[bot]`의 빈 커밋을 자동으로 생성합니다.
- GitHub Actions가 장기간 무활동 저장소의 예약 실행을 끄는 문제를 완화하기 위한 조치입니다. 실제 커밋 기록은 남으나 사이트 데이터, 공개 Excel, DB, 비밀번호는 변경하지 않습니다.
- **이 방식 역시 GitHub의 60일 제한을 영구적으로 우회한다고 보장되지는 않습니다.** 예: 워크플로 비활성화, 쓰기권한 차단, 보호 브랜치, GitHub 자체 오류, 봇 커밋을 활동으로 집계하지 않는 변경 등.
- `Settings → Actions → General → Workflow permissions`의 `Read and write permissions` 상태가 이 워크플로의 push와 호환되는지 확인하세요. **DB 점검 작업에는 쓰기 권한을 주지 않습니다.**
- 매월 `Actions → Y2C Scheduled Workflow Activity Guard` 성공 여부를 확인하세요. 저장소 전체에 과도한 권한을 줄 필요는 없고 파일별 `permissions`로 제한합니다.

## 무료 서비스의 한계 (중요)
- Supabase Free: 최근 7일간 사용자 DB 활동이 적으면 중지될 수 있습니다. 하루 몇 건의 실제 요청이 대개 도움이 되지만 **공식적인 24시간 무중단 보장은 유료 플랜에서만** 제공합니다.
- GitHub Actions: 예약 실행이 지연되거나 누락될 수 있습니다. 공개 저장소에서 **60일간 저장소 활동이 없으면 예약 실행이 중단**될 수 있습니다. 이번 V11에는 월별 자동 활동 커밋을 추가해 위험을 줄였지만, GitHub 동작 변경 또는 실행 실패 등에 대비해 주기적으로 Actions 실행내역을 확인하세요. 무기한 무중단을 보장할 수는 없습니다.
- 이메일 서버 오류가 발생하면 실패 경고도 전달되지 않습니다. **매일 받는 백업 이메일이 끊기면** GitHub Actions 상태를 확인하세요.
- 기존 백업은 `public` 스키마만 포함합니다. `auth.users`, Storage 파일, 프로젝트 설정 등은 별도 보관이 필요합니다.
- 비용은 GitHub 공개 저장소 + Supabase Free의 현행 무료 한도 내에서 0원입니다(도메인 갱신비 별도).

## 공식 참고
- https://supabase.com/docs/guides/platform/free-project-pausing
- https://docs.github.com/en/actions/reference/events-that-trigger-workflows
- https://docs.github.com/en/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows
