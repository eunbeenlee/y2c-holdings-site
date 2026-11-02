/* Y2C HOLDINGS | Secure Market Research Report Studio, V12
 * No passwords / credentials are hard-coded. Auth + permissions are checked in Supabase.
 * The public GitHub repository contains only front-end code and public website Excel.
 */
(() => {
  'use strict';
  const $ = selector => document.querySelector(selector);
  const emailDomain = /@y2choldings\.co\.kr$/i;
  const SECTIONS = [
    {key:'executive_summary',n:'01',title:'요약 및 최종 판단',intro:'경영진이 2분 안에 결론과 핵심 근거를 파악하도록 작성합니다.',fields:[
      ['decision','핵심 결론','진출 여부와 권고 이유를 2~3문장으로 작성하세요.'],['facts','핵심 지표','시장규모·가격·성장률·관세 등 핵심 수치와 근거를 함께 입력하세요.'],['score','시장 진출 적합성','기회 점수(0~100)와 점수 산정 기준을 기록하세요.']]},
    {key:'research_scope',n:'02',title:'조사 범위 및 방법론',intro:'조사 대상과 자료의 신뢰 수준을 구분합니다.',fields:[
      ['objective','조사 목적 및 핵심 질문','고객사가 무엇을 판단하기 위해 이 보고서를 요청했는지 입력하세요.'],['scope','대상 국가·기간·시장 정의','조사 범위, 고객·제품·서비스 구분을 기록하세요.'],['method','자료 수집 방법·한계','정부통계, 현지 인터뷰, 시장견적 및 아직 확인되지 않은 가정을 구분하세요.']]},
    {key:'market_size',n:'03',title:'시장 규모 및 성장성',intro:'TAM·SAM·SOM을 구분하고 숫자의 산정식을 남깁니다.',fields:[
      ['tam_sam_som','TAM · SAM · SOM','각 시장규모의 값, 단위, 계산식 및 기준연도를 함께 기재하세요.'],['drivers','성장 요인·시장 세분화','시장의 확대/축소 요인, 고객군별 규모를 설명하세요.'],['implications','핵심 시사점','실제로 접근 가능한 고객과 수요를 중심으로 정리하세요.']]},
    {key:'customer',n:'04',title:'고객 수요 및 구매 구조',intro:'실제 구매 담당자와 승인 절차가 중요합니다.',fields:[
      ['segments','주요 고객 세그먼트','잠재 고객군과 우선 접촉 대상, 고객 규모를 작성하세요.'],['buying_process','구매 담당자·발주 절차','구매 승인권자, 평균 주문량, 결제조건, 구매주기를 기록하세요.'],['voice','현지 인터뷰·구매 장벽','구매자 발언, 기존 공급계약, 신규 업체 승인 요건 및 미확인 사항을 정리하세요.']]},
    {key:'competition',n:'05',title:'경쟁사 및 가격 비교',intro:'고객이 실제로 비교하는 경쟁사와 대체재를 분석합니다.',fields:[
      ['competitors','경쟁사 비교','업체·국가·제품/서비스·판매가격·강점·약점·출처를 기록하세요.'],['price','시장가격 및 거래조건','도매가격, 소비자가, 유통마진, 품질·보증·납기 차이를 구분하세요.'],['positioning','Y2C 차별화 전략','검증 가능한 경쟁우위 2~3개와 방어 가능성을 정리하세요.']]},
    {key:'products',n:'06',title:'상품 적합성 및 공급역량',intro:'제품 사양과 실제 공급·품질 책임을 함께 평가합니다.',fields:[
      ['offer','핵심 상품·서비스','대표 SKU, 제품규격, 적용 시장, 인증 상태 등을 입력하세요.'],['suppliers','제조사 및 파트너 평가','생산국, MOQ, 생산능력, 수출 경험, 실제 견적과 신뢰도를 기록하세요.'],['quality','품질·클레임·안전','불량·반품·보증 대응, 필수 검사와 안전 위험을 기재하세요.']]},
    {key:'tariffs',n:'07',title:'FTA·HS·규제 및 통관',intro:'한국산이라는 사실만으로 특혜관세가 확정되지는 않습니다.',fields:[
      ['classification','HS 품목분류·특혜원산지','국가별 HS 후보와 FTA 원산지 결정기준, 검증 상태를 입력하세요.'],['duties','일반·특혜·추가 관세','세율, 적용일, CBP/CBSA 등 공식자료 링크, 세율 불확실성을 기록하세요.'],['compliance','수입규제·담당 책임','수입자(Importer of Record), 허가, 라벨링, 통관사, Incoterms를 정리하세요.']]},
    {key:'supply_chain',n:'08',title:'공급망 및 수입 실행',intro:'수입·물류를 실제 실행할 수 있는 파트너가 있는지 확인합니다.',fields:[
      ['flow','물류 흐름·담당자','제조사→운송사→수입사→구매사 경로 및 책임자를 작성하세요.'],['costs','운송 방식·리드타임','항공/해상 운송, 배송비, 창고비, 예상 리드타임을 기록하세요.'],['risks','계약·납기·공급 리스크','발주 최소물량, 하자·재고 위험, 대체 공급망 등을 정리하세요.']]},
    {key:'economics',n:'09',title:'원가·가격·수익성',intro:'모든 금액은 동일한 통화·물량·시점으로 비교합니다.',fields:[
      ['landed','도착원가 산출','매입가, 운임, 관세, 통관비, 수입세, 반품충당액 등 산식 포함.'],['sell_price','납품가격 및 수익률','도매가, 권장소비자가, 단위당 마진·공헌이익률을 구분하세요.'],['y2c_fee','Y2C 수익모델','영업대행 수수료, 월정액, 조달관리비 및 직접매입 마진을 구분하세요.']]},
    {key:'entry_plan',n:'10',title:'시장 진입 및 영업 실행',intro:'상담 확보에서 최초 납품·재주문까지 연결합니다.',fields:[
      ['channels','목표 고객·영업 채널','딜러십, 수입사, 유통사, 프랜차이즈 운영사 등 우선순위를 작성하세요.'],['roadmap','30·60·90일 실행 계획','과제·담당자·예산·완료기준·의존조건을 명시하세요.'],['kpi','영업 KPI 및 광고예산','적격 리드, 샘플, 견적, 주문, 재주문, 고객획득비용을 기록하세요.']]},
    {key:'finance_risks',n:'11',title:'재무 시나리오 및 리스크',intro:'성장이 아니라 무엇이 손익을 흔드는지 보여줍니다.',fields:[
      ['scenarios','보수·기준·확장 시나리오','매출, 공헌이익, 고정비, 예상 손익과 각 가정을 작성하세요.'],['sensitivity','민감도 및 위험 분석','관세, 환율, 운임, 품질, 미수금, 계약 지연 등의 영향분석.'],['stop_rules','손익분기·사업 중단 기준','어떤 조건에서 투자·영업을 중단하거나 전략을 전환할지 명시하세요.']]},
    {key:'recommendation',n:'12',title:'최종 권고 및 의사결정',intro:'증거와 판단을 연결하고 선결과제를 명확히 합니다.',fields:[
      ['go_nogo','Go / Hold / No-go','추천 결론과 논리, 결론이 바뀌는 조건을 작성하세요.'],['conditions','선결 조건 및 담당','추가 검증 과제, 필요 증빙, 담당자와 완료일.'],['next','후속 실행 조치','우선 행동 3가지와 예상 성과를 명시하세요.']]},
    {key:'sources',n:'13',title:'참고자료 및 조사 근거',intro:'수치와 규제 해석에는 자료의 발행일·확인일을 반드시 기록합니다.',fields:[
      ['bibliography','공식기관·통계·자료 링크','제목 / 기관 / 발행일 / URL / 확인일을 기록하세요.'],['interviews','현지 조사·인터뷰 근거','담당자·조사일·견적서·확인 가능한 자료를 기록하세요.'],['limits','미확인 사항 및 유의사항','미확정 가격·HS 분류·공급계약 등 사실과 가정을 분리하세요.']]}
  ];
  const EXTRA = [
    {key:'industry_automotive',n:'A',title:'자동차·산업용품 선택 검증',intro:'해당 산업의 조사일 때만 입력하면 됩니다.',fields:[['fitment','차종·연식 호환성','실차 장착/검증 및 제조사 도면·시편 확인'],['liability','제품 안전·보증','페달 간섭, 리콜, 제조물책임, 인증 요건']]},
    {key:'industry_franchise',n:'B',title:'외식·프랜차이즈 선택 검증',intro:'가맹점 운영 및 해외 진출 조사에 활용합니다.',fields:[['franchise','가맹 조건 및 규제','국가별 가맹정보 공개, 상표, 모집권한 및 전문자문'],['food','식품 수입·현지 운영','현지 수입허가, 공급망, 냉장·냉동, 매장 운영']]},
    {key:'public_programs',n:'C',title:'정부지원사업 선택 검증',intro:'국비지원은 수혜 가능성·비용 적격성을 분리해 기록합니다.',fields:[['programs','지원사업 및 적격성','공고명, 운영기관, 자격, 기간, 지원비율, 자부담'],['constraints','신청·수행기관·정산','참여기업 자격, 수행기관 등록 여부, 증빙·정산조건']]}
  ];
  const ALL = [...SECTIONS,...EXTRA];
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const statusLabels = {draft:'초안',review:'검토',final:'최종'};
  let client=null,user=null,role=null,selected=null,rows=[],record=null;
  let busy=false,dirty=false,changeCounter=0,autoSaveTimer=null,loading=false;
  const show = (selector,yes) => { const node=$(selector); if(node)node.hidden=!yes; };
  function tell(msg,isError=false) {const el=$('#adminNotice');el.textContent=msg;el.hidden=!msg;el.classList.toggle('error',isError);}
  function saveState(msg,kind='') {const node=$('#saveState'); node.textContent=msg;node.className='save-state '+kind;}
  function fieldName(section,subkey) {return `s_${section}__${subkey}`;}
  function makeGroup(group) {
    return `<details class="report-section" id="section-${esc(group.key)}" ${group.n==='01'?'open':''}>
      <summary><span class="section-num">${esc(group.n)}</span><span class="section-name">${esc(group.title)}</span><span class="section-hint">${group.fields.length}개 입력항목</span><span class="section-chevron" aria-hidden="true">⌄</span></summary>
      <div class="section-body"><p class="section-intro">${esc(group.intro)}</p>${group.fields.map(([key,title,hint])=>`<div class="report-field"><label for="${esc(fieldName(group.key,key))}">${esc(title)}</label><textarea id="${esc(fieldName(group.key,key))}" name="${esc(fieldName(group.key,key))}" data-section="${esc(group.key)}" data-field="${esc(key)}" rows="4" maxlength="30000" placeholder="${esc(hint)}" spellcheck="true"></textarea><small>${esc(hint)}</small></div>`).join('')}</div>
    </details>`;
  }
  function initEditor() {
    $('#reportSections').innerHTML=SECTIONS.map(makeGroup).join('');
    $('#optionalModules').innerHTML=`<div class="optional-heading"><span class="eyebrow">OPTIONAL APPENDIX</span><h3>산업별 추가 조사</h3></div>${EXTRA.map(makeGroup).join('')}`;
    $('#sectionJump').innerHTML=SECTIONS.map(x=>`<a href="#section-${esc(x.key)}" data-jump="${esc(x.key)}">${esc(x.n)}</a>`).join('');
    $('#sectionJump').addEventListener('click',e=>{const anchor=e.target.closest('[data-jump]');if(!anchor)return;const det=$('#section-'+anchor.dataset.jump);if(det)det.open=true;});
  }
  function getForm() {
    const f=$('#reportForm'); const data={};
    for(const key of ['title','client_name','target_market','industry','status'])data[key]=String(f.elements[key].value??'').trim();
    const original=record?.sections && typeof record.sections==='object'?record.sections:{};
    data.sections={...original};
    ALL.forEach(section=>{
      const old=original[section.key];
      const value=old&&typeof old==='object'&&!Array.isArray(old)?{...old}:{};
      for(const [key] of section.fields)value[key]=String(f.elements[fieldName(section.key,key)].value||'');
      data.sections[section.key]=value;
    });
    return data;
  }
  function fillForm(row) {
    loading=true;
    const f=$('#reportForm'); const old=row?.sections||{};
    for(const key of ['title','client_name','target_market','industry','status'])f.elements[key].value=row?.[key]??(key==='status'?'draft':'');
    ALL.forEach(section=>{
      const previous=old[section.key];
      section.fields.forEach(([key],i)=>{
        // Migrate old V11 13-section text fields to the first structured field, without discarding content.
        f.elements[fieldName(section.key,key)].value= typeof previous==='string'?(i===0?previous:''):String(previous?.[key]??'');
      });
    });
    $('#reportSavedTime').textContent=row?.updated_at?'마지막 저장 '+new Date(row.updated_at).toLocaleString('ko-KR'):'아직 저장되지 않았습니다';
    $('#editorHeading').textContent=row?.title||'새 시장조사 보고서';
    $('#cloneBtn').hidden=!row;
    $('#deleteBtn').hidden=!row||role!=='admin';
    dirty=false;saveState(row?'저장 완료':'첫 저장 전');updateProgress();loading=false;
  }
  function updateProgress() {
    let complete=0;
    SECTIONS.forEach(section=>{
      const answered=section.fields.some(([key])=>String($('#reportForm').elements[fieldName(section.key,key)].value||'').trim());
      if(answered)complete++;
      const anchor=$(`[data-jump="${section.key}"]`);if(anchor)anchor.classList.toggle('done',answered);
    });
    $('#progressText').textContent=`${complete} / ${SECTIONS.length} 조사영역 작성`;
    $('#progressBar').style.width=`${Math.round(complete/SECTIONS.length*100)}%`;
  }
  function renderList() {
    const term=$('#reportSearch').value.toLowerCase().trim(),status=$('#statusFilter').value;
    const matching=rows.filter(r=>(status==='all'||r.status===status)&&[r.title,r.client_name,r.target_market,r.industry].join(' ').toLowerCase().includes(term));
    $('#reportCount').textContent=String(rows.length);
    $('#reportsList').innerHTML=matching.length?matching.map(r=>`<button class="report-list-item ${r.id===selected?'selected':''}" type="button" data-id="${esc(r.id)}"><strong>${esc(r.title)}</strong><small>${esc(r.client_name||r.target_market||'Y2C 내부 프로젝트')}</small><span class="status-tag ${esc(r.status)}">${esc(statusLabels[r.status]||r.status)}</span><time>${r.updated_at?esc(new Date(r.updated_at).toLocaleDateString('ko-KR')):''}</time></button>`).join(''):'<div class="report-list-empty">조건에 맞는 보고서가 없습니다.</div>';
    $('#reportsList').querySelectorAll('[data-id]').forEach(el=>el.addEventListener('click',()=>{
      if(dirty&&!confirm('저장되지 않은 수정사항이 있습니다. 보고서를 전환하시겠습니까?'))return;
      openReport(rows.find(r=>r.id===el.dataset.id));
    }));
  }
  function openReport(row) {
    clearTimeout(autoSaveTimer);selected=row?.id||null;record=row||null;fillForm(row);
    show('#emptyEditor',false);show('#editorPanel',true);renderList();tell('');
    if(!row) {$('#reportForm').elements.title.focus();$('#section-executive_summary').open=true;}
  }
  function markDirty() {
    if(loading)return;dirty=true;changeCounter++;
    $('#editorHeading').textContent=$('#reportForm').elements.title.value||'새 시장조사 보고서';
    saveState(selected?'수정 중 · 자동저장 예정':'저장 전 · 제목과 본문을 입력하면 자동 임시저장','dirty');updateProgress();
    clearTimeout(autoSaveTimer);
    autoSaveTimer=setTimeout(()=>{
      const value=getForm(),hasBody=SECTIONS.some(g=>g.fields.some(([k])=>String(value.sections[g.key]?.[k]||'').trim()));
      if(value.title.length>=3&&(selected||hasBody))saveReport(true);
    },4500);
  }
  async function fetchReports() {
    const {data,error}=await client.from('y2c_reports').select('*').order('updated_at',{ascending:false}).limit(300);
    if(error)throw error;
    rows=data||[];renderList();
  }
  async function saveReport(silent=false) {
    if(!client||!user||busy)return false;
    const payload=getForm();if(!payload.title) {if(!silent)tell('보고서 제목을 먼저 입력해주세요.',true);return false;}
    clearTimeout(autoSaveTimer); const revision=changeCounter;busy=true;
    for(const button of [$('#saveBtn'),$('#bottomSaveBtn')])button.disabled=true;
    saveState('Supabase 저장 중…');
    try {
      let result;
      if(selected)result=await client.from('y2c_reports').update(payload).eq('id',selected).select('*').single();
      else result=await client.from('y2c_reports').insert({...payload,created_by:user.id}).select('*').single();
      if(result.error)throw result.error;
      selected=result.data.id;record=result.data;
      const at=new Date(result.data.updated_at).toLocaleString('ko-KR');
      $('#reportSavedTime').textContent='마지막 저장 '+at;
      $('#cloneBtn').hidden=false;$('#deleteBtn').hidden=role!=='admin';
      try {await fetchReports();}catch(e){tell('저장은 완료됐지만 목록을 갱신하지 못했습니다: '+e.message,true);}
      if(changeCounter===revision) {dirty=false;saveState('저장 완료');if(!silent)tell('보고서를 Supabase에 저장했습니다.');}
      else {dirty=true;saveState('추가 수정사항 있음','dirty');autoSaveTimer=setTimeout(()=>saveReport(true),4000);}
      return true;
    } catch(error){saveState('저장 실패 · 다시 시도','error');tell('저장 실패: '+(error.message||'서버 응답 오류')+'\n연결 상태를 확인하고 다시 저장하거나 JSON으로 백업하세요.',true);return false;}
    finally {busy=false;for(const button of [$('#saveBtn'),$('#bottomSaveBtn')])button.disabled=false;}
  }
  async function checkAccess() {
    const {data,error}=await client.auth.getUser();
    if(error||!data?.user) {user=null;role=null;show('#workspace',false);show('#deniedPanel',false);show('#loginPanel',true);show('#signOutBtn',false);show('#signedInEmail',false);return;}
    user=data.user;
    show('#signOutBtn',true);show('#signedInEmail',true);$('#signedInEmail').textContent=user.email||'';
    if(!emailDomain.test(user.email||'')){show('#deniedPanel',true);show('#loginPanel',false);show('#workspace',false);$('#deniedReason').textContent='회사 이메일(@y2choldings.co.kr)로 생성한 승인 계정이 필요합니다.';return;}
    const {data:admins,error:roleError}=await client.from('y2c_admins').select('role,active').eq('user_id',user.id).limit(1);
    if(roleError) {tell('관리자 권한 확인 실패: '+roleError.message,true);show('#deniedPanel',true);show('#loginPanel',false);show('#workspace',false);return;}
    const match=admins?.[0];role=match?.active?match.role:null;
    show('#loginPanel',false);show('#deniedPanel',!role);show('#workspace',!!role);
    if(role) {try {await fetchReports();}catch(e){tell('보고서 목록 조회 오류: '+e.message,true);}}
  }
  async function signOut() {
    clearTimeout(autoSaveTimer);
    if(dirty&&!confirm('저장되지 않은 내용이 있습니다. 로그아웃하시겠습니까?'))return;
    const {error}=await client.auth.signOut();if(error){tell('로그아웃 실패: '+error.message,true);return;}
    dirty=false;selected=null;record=null;rows=[];tell('로그아웃했습니다.');await checkAccess();
  }
  function downloadJson() {
    const content=JSON.stringify({format:'y2c-market-report-v12',exported_at:new Date().toISOString(),data:getForm()},null,2);
    const blob=new Blob([content],{type:'application/json;charset=utf-8'}),url=URL.createObjectURL(blob),a=document.createElement('a');
    a.href=url;a.download=`Y2C_Report_${new Date().toISOString().slice(0,10)}.json`;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),800);
    tell('현재 작성 내용을 JSON 파일로 내보냈습니다. (DB 저장과는 별개)');
  }
  async function cloneReport() {
    if(dirty&&!confirm('현재 수정사항은 복제된 보고서에 포함됩니다. 계속할까요?'))return;
    const value=getForm(); selected=null;record=null;
    fillForm({...value,title:(value.title||'보고서')+' · 사본',sections:value.sections});
    dirty=true;changeCounter++;saveState('복제한 보고서 · 저장 전','dirty');renderList();tell('사본을 만들었습니다. 제목과 내용을 확인한 뒤 저장하세요.');
  }
  async function removeReport() {
    if(!selected||role!=='admin')return;
    if(!confirm('이 보고서를 영구 삭제합니다. 실행 후 되돌릴 수 없습니다. 계속하시겠습니까?'))return;
    const {error}=await client.from('y2c_reports').delete().eq('id',selected);
    if(error){tell('삭제 실패: '+error.message,true);return;}
    dirty=false;selected=null;record=null;show('#editorPanel',false);show('#emptyEditor',true);await fetchReports();tell('보고서를 삭제했습니다.');
  }
  function printReport() {
    const data=getForm();
    $('#printTitle').textContent=data.title||'시장조사 보고서';
    $('#printMeta').textContent=[data.client_name,data.target_market,data.industry,new Date().toLocaleDateString('ko-KR')].filter(Boolean).join('  |  ');
    const old=$('#printReport');if(old)old.remove();
    const wrapper=document.createElement('div');wrapper.id='printReport';wrapper.className='print-report';
    wrapper.innerHTML=ALL.filter(section=>section.fields.some(([key])=>String(data.sections[section.key]?.[key]||'').trim())).map(section=>`<section class="print-section"><div class="print-index">${esc(section.n)} / ${esc(section.title)}</div>${section.fields.filter(([key])=>String(data.sections[section.key]?.[key]||'').trim()).map(([key,label])=>`<div class="print-field"><strong>${esc(label)}</strong><p>${esc(data.sections[section.key][key])}</p></div>`).join('')}</section>`).join('');
    $('#reportForm').appendChild(wrapper);
    window.print();
  }
  function setupEvents() {
    $('#loginForm').addEventListener('submit',async event=>{
      event.preventDefault();const email=$('#loginEmail').value.trim(),password=$('#loginPassword').value;
      if(!emailDomain.test(email)){tell('Y2C 회사 이메일(@y2choldings.co.kr)로 로그인해주세요.',true);return;}
      $('#loginBtn').disabled=true;tell('회사 계정 로그인 확인 중…');
      try {const {error}=await client.auth.signInWithPassword({email,password});$('#loginPassword').value='';if(error)throw error;tell('');await checkAccess();}
      catch(e){tell('로그인 실패: '+(e.message||'계정을 확인해주세요.')+'\n이메일 확인 여부와 Supabase 승인 상태를 확인하세요.',true);}
      finally {$('#loginBtn').disabled=false;}
    });
    $('#signOutBtn').addEventListener('click',signOut);$('#deniedSignOutBtn').addEventListener('click',signOut);
    const newReport=()=>{if(dirty&&!confirm('저장되지 않은 수정사항이 있습니다. 새 문서를 시작하시겠습니까?'))return;openReport(null);};
    $('#newBtn').addEventListener('click',newReport);$('#emptyNewBtn').addEventListener('click',newReport);
    $('#reportSearch').addEventListener('input',renderList);$('#statusFilter').addEventListener('change',renderList);
    $('#reportForm').addEventListener('submit',e=>{e.preventDefault();saveReport(false)});
    $('#reportForm').addEventListener('input',markDirty);$('#reportForm').addEventListener('change',markDirty);
    $('#saveBtn').addEventListener('click',()=>saveReport(false));
    $('#cloneBtn').addEventListener('click',cloneReport);$('#deleteBtn').addEventListener('click',removeReport);
    $('#exportBtn').addEventListener('click',downloadJson);$('#printBtn').addEventListener('click',printReport);
    window.addEventListener('beforeunload',e=>{if(dirty){e.preventDefault();e.returnValue='';}});
  }
  async function boot() {
    initEditor();const config=window.Y2C_ADMIN_CONFIG||{};
    if(!config.url?.startsWith('https://')||!/\.supabase\.co\/?$/.test(config.url)||!config.publishableKey?.startsWith('sb_publishable_')&&!config.publishableKey?.startsWith('eyJ')) {show('#setupPanel',true);return;}
    if(!window.supabase?.createClient){show('#setupPanel',true);tell('Supabase 로그인 라이브러리를 불러오지 못했습니다. 인터넷 연결이나 브라우저 차단 설정을 확인해주세요.',true);return;}
    client=window.supabase.createClient(config.url,config.publishableKey,{auth:{persistSession:true,autoRefreshToken:true,detectSessionInUrl:true}});
    setupEvents();await checkAccess();
  }
  boot().catch(e=>{show('#setupPanel',true);tell('관리자 화면 시작 실패: '+e.message,true);});
})();
