/* Y2C V21. Static content remains readable if JavaScript is unavailable. */
(()=>{'use strict';
const $=s=>document.querySelector(s),$$=s=>Array.from(document.querySelectorAll(s));
const locale=document.documentElement.lang==='en'?'en':'ko';
const t=(ko,en)=>locale==='ko'?ko:en;
let data=null; // data.products remains the source of public SKU visibility, not private CRM.
function notice(message){$('#formStatus').textContent=message;}
function products(){
 const cards=$$('.catalog-card'),bar=$('#productFilters');
 bar.querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>{
  const key=b.dataset.category;bar.querySelectorAll('button').forEach(x=>{x.classList.toggle('active',x===b);x.setAttribute('aria-pressed',String(x===b))});
  let n=0;cards.forEach(c=>{c.hidden=key!=='all'&&c.dataset.productCategory!==key;if(!c.hidden)n++});
  $('#productCount').textContent=n+' '+t('개 품목','items');
 }));
}

function init(){
 try{localStorage.setItem('y2c_lang',locale)}catch(_){}
 $$('[data-lang]').forEach(el=>el.addEventListener('click',()=>{try{localStorage.setItem('y2c_lang',el.dataset.lang)}catch(_){}}));
 $('#copyrightYear').textContent=new Date().getFullYear();
 $$('[data-partner]').forEach(b=>b.addEventListener('click',()=>{$('#partnerType').value=b.dataset.partner;$('#contact').scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});$('#contactForm input[name="company"]').focus({preventScroll:true})}));
 $$('[data-product]').forEach(a=>a.addEventListener('click',()=>{$('#contactForm input[name="interest"]').value=a.dataset.product;}));
 $('#contactForm').addEventListener('submit',e=>{e.preventDefault();const form=e.currentTarget;if(!form.reportValidity())return;
  const o=Object.fromEntries(new FormData(form));
  const msg=['Y2C HOLDINGS — Business Inquiry',`Company: ${o.company}`,`Contact: ${o.name}`,`Email: ${o.email}`,`Target market: ${o.region}`,`Partnership: ${o.partner_type}`,`Interest: ${o.interest}`,'',o.message].join('\n');
  $('#preparedText').value=msg;$('#formFallback').hidden=false;
  const email=data?.settings?.contact_email?.ko||'eunbeen.lee@y2choldings.co.kr';
  if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)){notice(t('내용을 복사해 회사 이메일로 보내주세요.','Copy your inquiry and send it by email.'));return;}
  location.href=`mailto:${email}?subject=${encodeURIComponent('Y2C Inquiry — '+o.company)}&body=${encodeURIComponent(msg)}`;
  notice(t('메일 앱에서 전송을 눌러주세요. 앱이 열리지 않으면 아래 내용을 복사해 회사 이메일로 보내주세요.','Press Send in your mail app. If it did not open, copy the message below and email it to us.'));
 });
 $('#copyBtn').addEventListener('click',async()=>{try{await navigator.clipboard.writeText($('#preparedText').value);notice(t('내용을 복사했습니다.','Message copied.'))}catch(_){$('#preparedText').select();notice(t('선택된 내용을 Ctrl+C로 복사해주세요.','Copy the selected text.'))}});
 products();
 fetch('./data/site-data.json').then(r=>{if(!r.ok)throw new Error('Content HTTP '+r.status);return r.json()}).then(o=>{data=o}).catch(()=>{/* Built HTML already contains the same content. */});
}
init();
})();
