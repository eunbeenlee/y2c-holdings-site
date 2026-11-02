# V12 업데이트 상세

## 기능
- 회사 이메일(`@y2choldings.co.kr`) + Supabase 승인 사용자 기반 관리자 로그인
- 회사 로고와 동일한 차콜/골드/오프화이트 업무용 UI
- 13개 시장조사 영역, 각 3개 세부 입력란(총 39개)
- 자동차/프랜차이즈/정부지원 선택 모듈 3개(총 6개 세부 입력란)
- 기존 V11의 13개 단일 텍스트 항목을 새 구조 첫 번째 입력란에 자동 표시
- 기존 `y2c_reports.sections` JSONB 구조 사용: 추가 SQL 실행 불필요
- 자동 임시저장(약 4.5초), 수동 저장, 미저장 이탈 방지
- 보고서 목록 검색·상태 필터·복제·삭제, 작성률 표시
- 고객 제출용 전체 문장 PDF/인쇄 출력 및 JSON 내보내기
- GitHub 공개용 Excel과 5개 상품 카탈로그, KR/EN 홈페이지 유지
- 기존 암호화 이메일백업, Supabase 정기점검 파일 보존

## 배포 테스트 보완
- V11의 테스트 코드가 `supabase-config.js`의 `url:''`와 `publishableKey:''`만 허용하던 잘못된 조건 수정
- Supabase 공개키를 실제 입력해도 unittest에 실패하지 않도록 개선
- Actions checkout/setup-python/upload-pages-artifact 최신 메이저 사용
- GitHub Pages 배포 전에 HTML/JS/공개 Excel 구조 검증

## 보안·데이터 보존
- 새 ZIP에서 실제 `site/assets/supabase-config.js` 제외: 기존 GitHub의 입력된 공개 설정값 보호
- 새 설치자를 위한 `site/assets/supabase-config.example.js` 별도 제공
- 비밀번호, secret/service_role 키, 내부 고객보고서 파일은 ZIP과 공개 GitHub에 포함하지 않음
- 서버측 Supabase RLS를 통한 보고서 접근통제 유지
- 자동 저장실패 시 화면 오류 및 JSON 내보내기 제공

## 한계
- 실제 운영 Supabase 계정 접근이 없어서 실 DB 저장/인증은 검증하지 못함. 스텁 인증 및 데이터베이스 응답을 사용한 브라우저 UI 테스트 수행.
- 무료 호스팅/DB의 중단을 방지한다는 보장은 없음. 백업 및 연결 오류 시 수동 조치 필요.
