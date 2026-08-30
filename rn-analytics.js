(()=>{
'use strict';
if(window.__RN_ANONYMOUS_ANALYTICS__)return;
window.__RN_ANONYMOUS_ANALYTICS__=true;

const ENDPOINT='https://fcvffslhnaqlwitaeers.supabase.co/functions/v1/rn-analytics';
const params=()=>{try{return new URLSearchParams(location.search);}catch{return new URLSearchParams();}};
const clean=(value,max=120)=>String(value??'').replace(/[\r\n\t]/g,' ').trim().slice(0,max);
const token=(value,max=80)=>{const v=clean(value,max);return v&&/^[A-Za-z0-9._:-]+$/.test(v)?v:'';};
const referrerHost=()=>{try{return document.referrer?new URL(document.referrer).hostname.toLowerCase().slice(0,120):'';}catch{return '';}};
function sourceInfo(){
 const p=params();
 const utm={};
 for(const key of ['utm_source','utm_medium','utm_campaign']){
  const value=token(p.get(key),80);
  if(value)utm[key.replace('utm_','')]=value;
 }
 const ref=referrerHost();
 let source=utm.source||'';
 if(!source&&ref){
  if(/(^|\.)google\./.test(ref))source='google';
  else if(/(^|\.)instagram\.com$/.test(ref))source='instagram';
  else if(/(^|\.)facebook\.com$/.test(ref))source='facebook';
  else if(/(^|\.)bing\.com$/.test(ref))source='bing';
  else if(ref===location.hostname)source='internal';
  else source=ref;
 }
 if(!source)source='direct';
 return {source:token(source,80)||'direct',referrer_host:/^[a-z0-9.-]+$/.test(ref)?ref:null,utm};
}
function formArea(target){
 const root=target?.closest?.('[data-pump-form]');
 return clean(root?.getAttribute('data-pump-form')||'',60);
}
function payload(eventName,properties={}){
 const a=sourceInfo();
 return {
  event_name:eventName,
  path:clean(location.pathname||'/',240)||'/',
  source:a.source,
  referrer_host:a.referrer_host,
  utm:a.utm,
  properties
 };
}
function send(eventName,properties={}){
 try{
  fetch(ENDPOINT,{
   method:'POST',
   mode:'cors',
   credentials:'omit',
   cache:'no-store',
   keepalive:true,
   referrerPolicy:'no-referrer',
   headers:{'Content-Type':'application/json'},
   body:JSON.stringify(payload(eventName,properties))
  }).catch(()=>{});
 }catch{}
}
async function markInternal(){
 try{
  await fetch(ENDPOINT,{
   method:'POST',mode:'cors',credentials:'omit',cache:'no-store',keepalive:true,referrerPolicy:'no-referrer',
   headers:{'Content-Type':'application/json'},
   body:JSON.stringify({event_name:'internal_mark',path:clean(location.pathname||'/',240)||'/'})
  });
 }catch{}
}

let requestStarted=false;
document.addEventListener('click',event=>{
 const target=event.target instanceof Element?event.target.closest('a,button,[role="button"]'):null;
 if(!target)return;

 if(target instanceof HTMLAnchorElement){
  const href=target.getAttribute('href')||'';
  if(/^tel:/i.test(href))send('phone_click');
  try{
   const u=new URL(target.href,location.href);
   if(/(^|\.)wa\.me$|(^|\.)whatsapp\.com$/i.test(u.hostname))send('whatsapp_click');
  }catch{}
 }

 const form=target.closest('[data-pump-form]');
 if(!form)return;
 const area=formArea(target);
 const props=area?{form_area:area}:{};

 if(target.closest('[data-next]')&&!requestStarted){
  const project=form.querySelector('input[name="project"]:checked');
  if(project){requestStarted=true;send('pump_request_start',props);}
 }
 if(target.closest('[data-send]')){
  const project=form.querySelector('input[name="project"]:checked');
  const place=clean(form.querySelector('[data-place]')?.value||'',1);
  const name=clean(form.querySelector('[data-name]')?.value||'',1);
  if(project&&place&&name)send('pump_request_send',props);
 }
},true);

(async()=>{
 if(params().get('rn_internal')==='1')await markInternal();
 send('page_view');
})();
})();
