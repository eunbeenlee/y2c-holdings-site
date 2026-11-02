(()=>{'use strict';
const $=s=>document.querySelector(s);
const sections=[
  ['executive_summary','01','Executive Summary / 핵심 결론','시장성, 진출 권고, 주요 리스크를 3~5개 문장으로 정리합니다.'],
  ['research_scope','02','조사 개요 및 방법론','조사목적·기간·대상국가·조사 방법·한계'],
  ['market_size','03','시장규모 및 성장성','TAM·SAM·SOM, 성장률, 시장 지표와 근거'],
  ['customer','04','수요·바이어 분석','고객 세그먼트·구매 결정자·구매주기·예산'],
  ['competition','05','경쟁업체 및 가격','주요 경쟁사, 현지가격, 포지셔닝, 차별화'],
  ['products','06','제품·공급업체 검증','SKU, 제조사·MOQ·품질·적합성·인증'],
  ['tariffs','07','FTA·HS·규제','HS 분류, 원산지 기준, 일반/특혜 관세, 추가 관세, 인증'],
  ['supply_chain','08','공급망 및 수입구조','Importer of Record, 운송, Incoterms, 유통·물류사, 납기'],
  ['economics','09','원가·수익성 분석','FOB, 국제운임, 관세, 현지 배송, 공급가, 수수료, 마진'],
  ['entry_plan','10','시장진입 및 영업계획','타깃 고객, 채널, 샘플, KPI, 30/60/90일 일정'],
  ['finance_risks','11','재무·리스크 평가','보수·기준·확장 시나리오, 현금흐름, 규제·품질 위험'],
  ['recommendation','12','최종 권고 및 의사결정','Go/Hold/No-go, 추진 조건, 담당자, 후속조치'],
  ['sources','13','참고자료 및 근거','원본 자료 URL·기관명·발표일·확인일·자료의 한계']
];
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let client=null, user=null, role=null, selected=null, rows=[], busy=false;
const toggle=(id,show)=>{$('#'+id).hidden=!show};
const tell=(msg,isError=false)=>{let n=$('#adminNotice');n.textContent=msg;n.hidden=!msg;n.classList.toggle('error',isError)};
function initFields(){
  $('#reportSections').innerHTML=sections.map(([key,n,name,hint])=>`<label class="report-section"><span class="section-num">${n} / REPORT</span><strong>${esc(name)}</strong><small>${esc(hint)}</small><textarea name="s_${key}" rows="5" maxlength="30000" spellcheck="true"></textarea></label>`).join('');
}
function currentForm(){const f=$('#reportForm'),o={};for(const name of ['title','client_name','target_market','industry','status'])o[name]=String(f.elements[name].value||'').trim();o.sections={};for(const [k] of sections)o.sections[k]=String(f.elements['s_'+k].value||'');return o;}
function fillForm(row){const f=$('#reportForm');for(const field of ['title','client_name','target_market','industry','status'])f.elements[field].value=row?.[field]|| (field==='status'?'draft':'');for(const [key] of sections)f.elements['s_'+key].value=String(row?.sections?.[key]||'');$('#reportSavedTime').textContent=row?.updated_at?'마지막 저장: '+new Date(row.updated_at).toLocaleString('ko-KR'):'';}
function selectReport(row){selected=row?.id||null;fillForm(row);toggle('editorPanel',true);toggle('emptyEditor',false);$('#deleteBtn').hidden=!row||role!=='admin';renderList();tell('');}
function renderList(){const term=$('#reportSearch').value.toLowerCase();const filtered=rows.filter(r=>([r.title,r.client_name,r.target_market,r.industry].join(' ').toLowerCase().includes(term)));$('#reportsList').innerHTML=filtered.length?filtered.map(r=>`<button type="button" data-report-id="${esc(r.id)}" class="report-list-item ${r.id===selected?'selected':''}"><strong>${esc(r.title)}</strong><small>${esc(r.client_name||r.target_market||'Y2C HOLDINGS')} · ${esc(r.status)}</small><time>${r.updated_at?esc(new Date(r.updated_at).toLocaleDateString('ko-KR')):''}</time></button>`).join(''):'<div class="report-list-empty">보고서가 없습니다.</div>';
  $('#reportsList').querySelectorAll('[data-report-id]').forEach(btn=>btn.addEventListener('click',()=>selectReport(rows.find(r=>r.id===btn.dataset.reportId))));}
async function checkAccess(){
  const {data:auth,error}=await client.auth.getUser(); if(error||!auth?.user){user=null;toggle('loginPanel',true);toggle('workspace',false);toggle('deniedPanel',false);$('#signOutBtn').hidden=true;return;}
  user=auth.user; $('#signOutBtn').hidden=false;
  const {data:admins,error:roleError}=await client.from('y2c_admins').select('role, active').eq('user_id',user.id).limit(1);
  if(roleError){tell('관리자 권한 확인 실패: '+roleError.message,true);toggle('loginPanel',false);toggle('workspace',false);toggle('deniedPanel',true);return;}
  const allowed=admins?.[0]?.active;role=allowed?admins[0].role:null;
  toggle('loginPanel',false);toggle('deniedPanel',!allowed);toggle('workspace',!!allowed);
  if(allowed)await loadReports();
}
async function loadReports(){const {data,error}=await client.from('y2c_reports').select('*').order('updated_at',{ascending:false}).limit(200);if(error){tell('보고서를 불러오지 못했습니다: '+error.message,true);return}rows=data||[];renderList();}
async function doSave(e){e.preventDefault();if(busy)return;const v=currentForm();if(!v.title){tell('보고서 제목을 입력해주세요.',true);return;}busy=true;$('#saveBtn').disabled=true;tell('저장 중…');try{
 let result;if(selected){result=await client.from('y2c_reports').update(v).eq('id',selected).select('*').single();}else{result=await client.from('y2c_reports').insert({...v,created_by:user.id}).select('*').single();}
 if(result.error)throw result.error;selected=result.data.id;await loadReports();selectReport(result.data);tell('비공개 데이터베이스에 저장했습니다.');
}catch(e){tell('저장 실패: '+(e.message||'서버 오류'),true)}finally{busy=false;$('#saveBtn').disabled=false;}}
async function doDelete(){if(!selected||role!=='admin'||!confirm('이 보고서를 영구 삭제하시겠습니까?'))return;const {error}=await client.from('y2c_reports').delete().eq('id',selected);if(error){tell('삭제 실패: '+error.message,true);return}selected=null;toggle('editorPanel',false);toggle('emptyEditor',true);tell('보고서를 삭제했습니다.');await loadReports();}
function backup(){const v=currentForm();const data={format:'y2c-market-report-v1',exported_at:new Date().toISOString(),...v};const str=JSON.stringify(data,null,2);const url=URL.createObjectURL(new Blob([str],{type:'application/json;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download='Y2C_Report_'+new Date().toISOString().slice(0,10)+'.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),2000);tell('현재 편집 내용을 JSON으로 내려받았습니다. (서버 저장 여부와 별개)');}
function setupEvents(){
  $('#loginForm').addEventListener('submit',async e=>{e.preventDefault();tell('로그인 확인 중…');$('#loginBtn').disabled=true;const email=$('#loginEmail').value,password=$('#loginPassword').value;try{const {error}=await client.auth.signInWithPassword({email,password});$('#loginPassword').value='';if(error)throw error;tell('');await checkAccess()}catch(e){tell('로그인 실패: '+(e.message||'계정을 확인해주세요.'),true)}finally{$('#loginBtn').disabled=false;}});
  $('#signOutBtn').addEventListener('click',async()=>{await client.auth.signOut();selected=null;rows=[];tell('로그아웃했습니다.');await checkAccess()});
  $('#newBtn').addEventListener('click',()=>selectReport(null));$('#reportSearch').addEventListener('input',renderList);
  $('#reportForm').addEventListener('submit',doSave);$('#deleteBtn').addEventListener('click',doDelete);
  $('#exportBtn').addEventListener('click',backup);$('#printBtn').addEventListener('click',()=>window.print());
}
async function boot(){initFields();const c=window.Y2C_ADMIN_CONFIG||{};
 if(!c.url?.startsWith('https://')||!c.publishableKey||!/\.supabase\.co\/?$/.test(c.url)){
  toggle('setupPanel',true);return;
 }
 if(!window.supabase?.createClient){tell('로그인 모듈을 불러오지 못했습니다. 네트워크를 확인해주세요.',true);return;}
 client=window.supabase.createClient(c.url,c.publishableKey,{auth:{persistSession:true,autoRefreshToken:true}});
 setupEvents();await checkAccess();
}
boot().catch(e=>tell('관리자 화면 초기화 실패: '+e.message,true));
})();
