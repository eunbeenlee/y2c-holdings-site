# Y2C HOLDINGS | V13 SERVICE & PRICING UPDATE

업데이트 기준: 2026-11-02

## 변경 내용

1. `site/pricing.html` 신규: 시장조사 보고서 4단계 + 프로젝트 업무대행 + 국내·해외 현장 프로젝트 + 거래 수수료 + 간편 예산 계산기.
2. `data/website_content.xlsx`의 `요금정책` 시트(11개 항목)에서 공개 요금을 관리합니다. GitHub에 이 Excel 파일을 Commit하면 Actions가 `site/data/site-data.json`을 다시 생성합니다.
3. `site/index.html`에 `서비스·요금` 메뉴와 소개 섹션을 추가했습니다.
4. `site/admin.html`에 보고서 상품등급 및 계약금액 입력 항목을 추가했습니다. `site/assets/admin.js`는 보고서 등급에 따라 조사영역을 보여주며, 가격 및 등급은 기존 `y2c_reports.sections._pricing` JSON에 저장합니다. DB 테이블 변경 및 SQL 재실행은 필요하지 않습니다.
5. V12의 GitHub Pages, 회사계정 Supabase Auth, 상품안내, 자동이메일 백업, DB 활동점검 워크플로 유지.
6. 배포용 `site/assets/supabase-config.js`에는 사용자가 이미 제공한 **public publishable key**와 수정한 Supabase 프로젝트 URL만 포함합니다. `secret`, `service_role`, 회사계정 비밀번호는 포함하지 않습니다.
7. 가격은 **Y2C 시험용 제안 시작가**입니다. 시장 평균이나 이미 체결한 계약가격이 아닙니다.

## 공개 가격 정책

| 서비스 | 시작가/요율 | 기본 단위 |
|---|---:|---|
| Essential 보고서 | 490,000원 | 건 |
| Business 보고서 | 1,900,000원 | 건 |
| Strategic 보고서 | 4,500,000원 | 건 |
| Enterprise 보고서 | 9,000,000원 | 건 |
| 파트너 발굴·검증 | 1,500,000원 | 프로젝트 |
| 해외 사업개발 대행 | 1,800,000원 | 월 |
| 공급망 구축 | 2,500,000원 | 프로젝트 |
| 국내 현장 프로젝트 수행 | 800,000원 | 인일 |
| 해외 현장 프로젝트 수행 | 1,300,000원 | 인일 |
| 제조사 해외영업대행 성과수수료 | 5–9% (기본 제안 7%) | 실제 회수된 계약상 순상품매출 |
| 소싱·조달관리 수수료 | 3–5% | 계약상 조달금액 |

*VAT 별도, 출장·숙박·해외 세무·인허가·전문가 비용은 계약범위에 따라 추가됩니다. 견적과 일정은 착수 전에 합의해야 합니다.*

## 법률 및 출입국 관련 필수 검토

- 근로자파견사업은 허가가 필요하며(파견법 제7조), 고객이 파견근로자를 직접 지휘하는 경우에는 계약 명칭을 '용역'이라고 썼더라도 실질에 따라 파견으로 판단할 수 있습니다. Y2C의 '현장 프로젝트 수행'은 Y2C의 자체 지휘·감독 아래 수행하는 과업·산출물 중심 서비스로만 제안합니다. 일반 근로자파견을 제공한다는 뜻이 아닙니다.
- 해외 현지 파견은 미국 B-1/ESTA, 캐나다 Business Visitor 등으로 유상 현지 취업/현지 노동시장 참가가 가능한지 따로 확인해야 합니다. 현지 고용에 해당하는 업무라면 별도 취업허가 등이 필요할 수 있습니다.
- 유료 취업알선은 별도 직업안정법 검토 대상이므로 현재 메뉴에 포함하지 않았습니다.
- 프랜차이즈 로열티는 가맹본부 권리입니다. Y2C는 그 자체를 징수하는 구조를 공개가격에 포함하지 않았습니다.

## 근거 (요율·법률)

- KOTRA 조사 가격 예시: https://dream.kotra.or.kr/dream/cms/com/index.do?MENU_ID=3880
- MANA 제조사 영업대행 요율 (과거 조사 기준): https://members.manaonline.org/step-3-create-fair-and-balanced-written-agreements
- 근로자파견법 제5조/7조: https://law.go.kr/lsLinkCommonInfo.do?chrClsCd=010202&lsJoLnkSeq=1007688641
- 고용노동부 파견 실질 판단: https://labor.moel.go.kr/reportCntr/dispatchedWorker.do
- 미국 B-1 관련: https://travel.state.gov/content/travel/en/us-visas/business/b-1-fact-sheet.html
- 캐나다 Business Visitor: https://www.ircc.canada.ca/english/helpcentre/answer.asp?qnum=434&top=5

## 주의

공개 GitHub 저장소에 내부 사업관리 V13 Excel, 고객 명단, 견적 계약서, 비밀번호, `service_role`/secret API 키를 추가하면 안 됩니다. 별도로 제공한 내부 사업관리 Excel은 로컬/비공개 장소에서 보관하세요.
