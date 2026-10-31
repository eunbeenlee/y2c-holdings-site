(() => {
  'use strict';
  const $ = (q,p=document) => p.querySelector(q);
  const $$ = (q,p=document) => [...p.querySelectorAll(q)];
  const html = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const formatted = value => html(value).replace(/&lt;br\s*\/?&gt;/gi,'<br>').replace(/\n/g,'<br>');
  const https = value => typeof value==='string' && /^https:\/\/[A-Za-z0-9.-]+(?::\d+)?(?:[/?#]|$)/.test(value) ? value : '';
  let data, locale = 'ko', category='all';
  try { locale = localStorage.getItem('y2c_lang')==='en'?'en':'ko'; } catch (_) {}
  const dictionary={ko:{all:'전체',Interior:'실내 보호',Care:'디테일링',Film:'필름',source:'출처',copy:'내용을 복사했습니다.',copyFail:'복사 기능을 사용할 수 없습니다. 아래 내용을 직접 선택하여 복사하세요.',prepared:'문의 내용이 준비되었습니다. 복사하여 공식 연락 채널로 전달해 주세요.',fail:'전송에 실패했습니다. 문의 내용을 복사해 주세요.',received:'전송을 요청했습니다. 실제 접수 여부는 담당자에게 확인해 주세요.',email:'이메일 앱을 열었습니다. 전송 버튼을 눌러야 발송됩니다.',verify:'필수 항목과 이메일 형식을 확인해 주세요.'},en:{all:'All',Interior:'Interior',Care:'Detailing',Film:'Film',source:'Source',copy:'Copied to clipboard.',copyFail:'Unable to copy automatically. Select the text below and copy it.',prepared:'Inquiry ready. Copy the text and send it to an official contact channel.',fail:'Submission failed. Please copy and send the inquiry.',received:'Submission requested. Please verify receipt with our team.',email:'Your email app has opened. Press Send to complete delivery.',verify:'Check the required fields and business email.'}};
  const value = (row,key) => String(row?.[`${key}_${locale}`] || row?.[`${key}_ko`] || '');
  const setting = key => String(data?.settings?.[key]?.[locale] || data?.settings?.[key]?.ko || '');
  function refreshText(){
    document.documentElement.lang=locale;
    document.title=locale==='ko'?'Y2C HOLDINGS — 글로벌 비즈니스':'Y2C HOLDINGS — Global Partnerships';
    $$('[data-i18n]').forEach(el=>{const v=setting(el.dataset.i18n);if(v)el.innerHTML=formatted(v)});
    $$('[data-ko]').forEach(el=>{el.innerHTML=formatted(el.dataset[locale]||el.dataset.ko||'')});
    $$('[data-lang]').forEach(el=>{const on=el.dataset.lang===locale;el.classList.toggle('active',on);el.setAttribute('aria-pressed',String(on))});
    $('#copyrightYear').textContent=String(new Date().getFullYear());
    const hasChannel=!!https(setting('form_endpoint')) || /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(setting('contact_email'));
    $('#submitBtn').querySelector('span').textContent=hasChannel?(locale==='ko'?'문의 보내기':'Send inquiry'):(locale==='ko'?'문의 내용 준비하기':'Prepare inquiry');
    $('#formNote').textContent=hasChannel?(locale==='ko'?'실제 수신 여부는 연결된 서비스 상태에 따라 달라집니다.':'Delivery depends on the configured receiving channel.'):(locale==='ko'?'문의 수신 시스템 연결 전: 내용 복사 기능을 제공합니다.':'Receiving channel not connected: copy the prepared inquiry.');
  }
  function renderServices(){
    $('#servicesGrid').innerHTML=data.services.map((s,i)=>`<article class="service-item"><span class="service-idx">${String(i+1).padStart(2,'0')}</span><div><h3>${html(value(s,'title'))}</h3><p>${html(value(s,'description'))}</p></div></article>`).join('');
  }
  function renderFilters(){
    const cats=['all',...new Set(data.products.map(x=>x.category).filter(Boolean))];
    if(!cats.includes(category))category='all';
    $('#productFilters').innerHTML=cats.map(c=>`<button class="filter-btn${category===c?' active':''}" type="button" data-category="${html(c)}" aria-pressed="${category===c}">${html(c==='all'?dictionary[locale].all:(dictionary[locale][c]||c))}</button>`).join('');
    $$('#productFilters button').forEach(el=>el.addEventListener('click',()=>{category=el.dataset.category;renderFilters();renderProducts()}));
  }
  function renderProducts(){
    const products=data.products.filter(p=>category==='all'||p.category===category);
    $('#productCount').textContent=String(products.length).padStart(2,'0');
    $('#productsGrid').innerHTML=products.map((p,i)=>`<article class="product-card"><div class="product-card-top"><span>${html(p.sku||'SKU '+(i+1))}</span><span>${html(p.market||'GLOBAL')}</span></div><h3>${html(value(p,'name'))}</h3><p>${html(value(p,'description'))}</p><div class="product-card-bottom"><span class="tariff">${html(value(p,'tariff'))}</span>${https(p.source_url)?`<a href="${html(https(p.source_url))}" target="_blank" rel="noopener noreferrer" aria-label="${html(dictionary[locale].source)}: ${html(value(p,'name'))}">↗</a>`:'<span aria-hidden="true">↗</span>'}</div></article>`).join('');
  }
  function renderSteps(){
    $('#stepsGrid').innerHTML=data.steps.map((s,i)=>`<article class="process-step"><span class="number">0${Number(s.step)||i+1} —</span><h3>${html(value(s,'title'))}</h3><p>${html(value(s,'description'))}</p></article>`).join('');
  }
  function renderPartners(){
    $('#partnersGrid').innerHTML=data.partners.map((p,i)=>`<button type="button" class="partner-card" data-partner="${html(p.id)}"><div class="partner-top"><span>${String(i+1).padStart(2,'0')}</span><span>↗</span></div><h3>${html(value(p,'title'))}</h3><p>${html(value(p,'description'))}</p></button>`).join('');
    const select=$('#partnerType');const old=select.value;
    select.innerHTML=`<option value="">${locale==='ko'?'선택하세요':'Choose a category'}</option>` + data.partners.map(p=>`<option value="${html(p.id)}">${html(value(p,'title'))}</option>`).join('');
    if(old)select.value=old;
    $$('.partner-card').forEach(b=>b.addEventListener('click',()=>{select.value=b.dataset.partner;$('#contact').scrollIntoView({behavior:'smooth'});setTimeout(()=>$('#contactForm input[name="company"]').focus({preventScroll:true}),200)}));
  }
  function renderPrograms(){
    $('#programsGrid').innerHTML=data.programs.map((p,i)=>`<article class="resource-row"><span class="resource-idx">${String(i+1).padStart(2,'0')}</span><div><h3>${html(value(p,'title'))}</h3><p>${html(value(p,'description'))}</p></div><span class="resource-status">${html(value(p,'status'))}</span>${https(p.official_url)?`<a href="${html(https(p.official_url))}" class="resource-link" rel="noopener noreferrer" target="_blank" aria-label="${html(value(p,'title'))} — Official site"><span class="link-text">${locale==='ko'?'공식 안내':'Official site'}</span> ↗</a>`:'<span></span>'}</article>`).join('');
  }
  function renderFaq(){
    $('#faqList').innerHTML=data.faq.map(q=>`<details class="faq-item"><summary>${html(value(q,'question'))}</summary><p>${html(value(q,'answer'))}</p></details>`).join('');
  }
  function render(){refreshText();renderServices();renderFilters();renderProducts();renderSteps();renderPartners();renderPrograms();renderFaq()}
  const messageOf=v=>['Y2C HOLDINGS — Partnership inquiry',`Company: ${v.company}`,`Partner type: ${v.partner_type}`,`Contact: ${v.name}`,`Email: ${v.email}`,`Country: ${v.region}`,`Interest: ${v.interest}`,'','Project details:',v.message].join('\n');
  function state(msg,isError=false){const el=$('#formStatus');el.textContent=msg;el.classList.toggle('error',isError)}
  function fallback(text){$('#formFallback').hidden=false;$('#preparedText').value=text}
  async function submit(e){
    e.preventDefault(); const form=$('#contactForm');if(!form.reportValidity()){state(dictionary[locale].verify,true);return}
    const o={};['company','partner_type','name','email','region','interest','message'].forEach(k=>o[k]=String(form.elements[k].value||'').trim());const text=messageOf(o);
    const endpoint=https(setting('form_endpoint'));const email=setting('contact_email');state('');
    if(endpoint){const btn=$('#submitBtn');btn.disabled=true;try{const res=await fetch(endpoint,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(o)});if(!res.ok)throw Error('Submission error');state(dictionary[locale].received);form.reset();$('#formFallback').hidden=true}catch(_){fallback(text);state(dictionary[locale].fail,true)}finally{btn.disabled=false}}
    else if(/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)){fallback(text);window.location.href=`mailto:${email}?subject=${encodeURIComponent('Y2C Partnership — '+o.company)}&body=${encodeURIComponent(text)}`;state(dictionary[locale].email)}
    else{fallback(text);state(dictionary[locale].prepared)}
  }
  function initEvents(){
    $$('[data-lang]').forEach(btn=>btn.addEventListener('click',()=>{locale=btn.dataset.lang;try{localStorage.setItem('y2c_lang',locale)}catch(_){};render()}));
    $('#menuBtn').addEventListener('click',()=>{const menu=$('#mobileNav');menu.hidden=!menu.hidden;$('#menuBtn').setAttribute('aria-expanded',String(!menu.hidden))});
    $$('#mobileNav a').forEach(el=>el.addEventListener('click',()=>{$('#mobileNav').hidden=true;$('#menuBtn').setAttribute('aria-expanded','false')}));
    $('#contactForm').addEventListener('submit',submit);
    $('#copyBtn').addEventListener('click',async()=>{try{await navigator.clipboard.writeText($('#preparedText').value);state(dictionary[locale].copy)}catch(_){$('#preparedText').focus();$('#preparedText').select();state(dictionary[locale].copyFail,true)}});
  }
  async function run(){initEvents();try{const r=await fetch('./data/site-data.json',{cache:'no-store'});if(!r.ok)throw Error(`HTTP ${r.status}`);data=await r.json();if(!Array.isArray(data.products)||!Array.isArray(data.services)||!data.settings)throw Error('Malformed Excel output');render()}catch(err){console.error(err);$('#loadError').hidden=false;$$('.loading').forEach(el=>el.textContent='Website data unavailable / 데이터를 불러오지 못했습니다.') }}
  run();
})();
