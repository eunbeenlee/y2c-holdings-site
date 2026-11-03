/* Shared navigation and language bridge. No authentication or tracking. */
(()=>{'use strict';
 const header=document.querySelector('.y2c-header');if(!header)return;
 const page=header.dataset.shellPage,menu=document.getElementById('mobileNav'),button=document.getElementById('menuBtn');
 const locales=new Set(['photo-credits','index','services','market-research','overseas-sales','buyer-development','export-consulting','supply-chain','franchise-development']);
 const lang=()=>document.documentElement.lang==='en'?'en':'ko';
 const href=(base,l)=>'./'+base+(l==='en'&&locales.has(base)?'-en':'')+'.html'+(l==='en'&&!locales.has(base)?'?lang=en':'');
 function close(){menu.hidden=true;button.setAttribute('aria-expanded','false');button.setAttribute('aria-label',lang()==='ko'?'메뉴 열기':'Open menu')}
 button.addEventListener('click',()=>{menu.hidden=!menu.hidden;button.setAttribute('aria-expanded',String(!menu.hidden));button.setAttribute('aria-label',menu.hidden?(lang()==='ko'?'메뉴 열기':'Open menu'):(lang()==='ko'?'메뉴 닫기':'Close menu'))});
 menu.querySelectorAll('a').forEach(a=>a.addEventListener('click',close));
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!menu.hidden){close();button.focus()}});
 window.matchMedia('(min-width:1081px)').addEventListener('change',e=>{if(e.matches)close()});
 function sync(){const l=lang();for(const root of [header,document.querySelector('.y2c-footer')]){if(!root)continue;
  root.querySelectorAll('[data-ko][data-en]').forEach(e=>e.textContent=e.dataset[l]);
  root.querySelectorAll('[data-shell-link]').forEach(a=>{let k=a.dataset.shellLink;a.href=['about','products','contact'].includes(k)?href('index',l)+'#'+k:href(k,l)});
  root.querySelectorAll('.y2c-brand').forEach(a=>a.href=href('index',l));
 }
 header.querySelectorAll('[data-shell-lang]').forEach(a=>{if(a.dataset.shellLang===l)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current')});
 try{localStorage.setItem('y2c_lang',l)}catch(_){}
 }
 header.querySelectorAll('[data-shell-lang]').forEach(a=>a.addEventListener('click',e=>{
  const target=a.dataset.shellLang;if(!['pricing','privacy','free-report','quick-report'].includes(page))return;
  e.preventDefault();if(target===lang())return;
  if(page==='pricing'||page==='privacy')document.querySelector(`button[data-lang="${target}"]`)?.click();
  if(page==='free-report')document.getElementById('toggleLang')?.click();
  if(page==='quick-report')document.getElementById('lang')?.click();
  sync();
 }));
 new MutationObserver(sync).observe(document.documentElement,{attributes:true,attributeFilter:['lang']});sync();
 const year=document.getElementById('copyrightYear');if(year)year.textContent=String(new Date().getFullYear());
})();
