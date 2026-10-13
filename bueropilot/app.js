(() => {
"use strict";
const $ = id => document.getElementById(id);
const cfg = window.RN_PUBLIC_CONFIG || {};
const configured = Boolean(/^https:\/\/[a-z0-9-]+\.supabase\.co\/?$/.test(cfg.supabaseUrl || "") && cfg.supabasePublishableKey && cfg.supabasePublishableKey.length > 20);
const supabase = configured && window.supabase?.createClient
 ? window.supabase.createClient(cfg.supabaseUrl.replace(/\/$/,""),cfg.supabasePublishableKey,{auth:{autoRefreshToken:true,persistSession:true,detectSessionInUrl:true}}) : null;
let session = null, staff = null, jobs = [], busy = false, speech = null, listening = false, recording = false;
let lastAudio = null, lastSpeech = "", initComplete = false;
function setStatus(msg,ready=false){$("connText").textContent=msg;$("connDot").className="status-dot "+(ready?"ready":"error");}
function setup(title,msg){$("setupNotice").hidden=false;$("setupTitle").textContent=title;$("setupMessage").textContent=msg;}
function hideSetup(){$("setupNotice").hidden=true;}
function showAuth(){staff=null;$("authScreen").hidden=false;$("appScreen").hidden=true;$("logoutBtn").hidden=!session;}
function showApp(){$("authScreen").hidden=true;$("appScreen").hidden=false;$("logoutBtn").hidden=false;hideSetup();}
function message(text){$("loginStatus").textContent=text;}
function escapeText(v){return typeof v==="string"?v:String(v??"");}
async function functionCall(name,payload){
  if(!supabase||!session)throw Error("Bitte zuerst anmelden.");
  const {data,error}=await supabase.functions.invoke(name,{body:payload||{}});
  if(error){
    let details="";
    try{details=(await error.context?.json())?.error||"";}catch(_){}
    throw Error(details||"Serverfunktion '"+name+"' ist noch nicht erreichbar.");
  }
  if(data?.error)throw Error(data.error);
  return data;
}
async function refreshSession(){
 const {data,error}=await supabase.auth.getSession();
 if(error)throw error;
 session=data?.session||null;
 if(!session){showAuth();setStatus("Nicht angemeldet");return;}
 try{
   const data=await functionCall("rn-auth-check",{});
   if(!data?.allowed)throw Error("Du bist noch nicht als RN-Mitarbeiter freigegeben.");
   staff=data;showApp();setStatus("Mitarbeiterzugang aktiv",true);await loadJobs();
 }catch(e){
   showAuth();setup("Noch kein Mitarbeiterzugang",e.message||"Keine Berechtigung.");setStatus("Zugang nicht freigegeben");
 }
}
async function loadJobs(){
 try{
   const r=await functionCall("rn-jobs-list",{});
   if(!Array.isArray(r.jobs))throw Error("Unerwartete Serverantwort.");
   jobs=r.jobs;
   renderJobs();
 }catch(e){jobs=[];renderJobs();setup("Disposition nicht verfügbar",e.message);}
}
function renderJobs(){
 $("metricAll").textContent=jobs.length;
 const day=d=>d.toLocaleDateString("sv-SE");
 const now=new Date(),tomorrow=new Date(now);tomorrow.setDate(now.getDate()+1);
 $("metricToday").textContent=jobs.filter(x=>x.date===day(now)).length;
 $("metricTomorrow").textContent=jobs.filter(x=>x.date===day(tomorrow)).length;
 $("overviewJobs").replaceChildren();
 $("jobsTbody").replaceChildren();
 if(!jobs.length){$("overviewJobs").innerHTML='<div class="empty">Noch keine freigegebenen Einsätze vorhanden.</div>';$("jobsTbody").innerHTML='<tr><td colspan="5" class="empty">Keine Einsätze geladen.</td></tr>';return;}
 const sorted=[...jobs].sort((a,b)=>String(a.date+" "+a.start_time).localeCompare(String(b.date+" "+b.start_time)));
 for(const j of sorted.slice(0,6)){
   const div=document.createElement("div");div.className="job-item";
   const one=document.createElement("div"),head=document.createElement("b"),sub=document.createElement("div"),side=document.createElement("span");
   head.textContent=escapeText(j.customer);sub.textContent=escapeText(j.site);sub.className="small-note";side.textContent=[j.date,String(j.start_time||"").slice(0,5),j.pump].filter(Boolean).join(" · ");
   one.append(head,sub);div.append(one,side);$("overviewJobs").append(div);
 }
 for(const j of sorted){
   const tr=document.createElement("tr");
   for(const value of [[j.date,String(j.start_time||"").slice(0,5)].join(" · "),j.customer,j.site,j.pump,j.status]){
     const td=document.createElement("td");td.textContent=escapeText(value);tr.append(td);
   }
   $("jobsTbody").append(tr);
 }
}
function tab(id){
 document.querySelectorAll(".tab").forEach(t=>{const active=t.dataset.tab===id;t.classList.toggle("active",active);t.setAttribute("aria-pressed",String(active));});
 ["overview","jobs","willi"].forEach(n=>$(n+"Panel").hidden=n!==id);
 if(id==="willi")$("chatInput").focus();
}
function bubble(text,me=false){
 const el=document.createElement("div");el.className="bubble "+(me?"me-bubble":"willi-bubble");el.textContent=text;$("chatMessages").append(el);
 $("chatMessages").scrollTop=$("chatMessages").scrollHeight;
}
async function playVoice(text){
 const v=window.RNWilliVoice;
 if(!v){$("voiceStatus").textContent="Die kostenlose Stimme konnte nicht geladen werden.";return;}
 const result=window.RNPiperVoice ? await window.RNPiperVoice.speak(text,{rate:$("williRate").value,onStatus:msg=>$("voiceStatus").textContent=msg}) : await v.speak(text);
 if(result.status==="unsupported"||result.status==="error")$("voiceStatus").textContent="Sprachausgabe nicht verfügbar: "+(result.message||result.status);
}
function initializeVoice(){
 const v=window.RNWilliVoice;
 if(!v)return;
 const select=$("williVoice"),tempo=$("williRate"),pitch=$("williPitch");
 const setting=v.getSettings();tempo.value=setting.rate;pitch.value=setting.pitch;
 const paint=()=>{$("williRateValue").textContent=Number(tempo.value).toFixed(2).replace(".",",");$("williPitchValue").textContent=Number(pitch.value).toFixed(2).replace(".",",");};
 function voices(){const saved=v.getSettings().voice;select.replaceChildren();const list=v.getVoices();if(!list.length){const o=document.createElement("option");o.textContent="Systemstimme (automatisch)";o.value="";select.append(o);}else for(const item of list){const o=document.createElement("option");o.textContent=item.label;o.value=item.id;select.append(o);}if(list.some(x=>x.id===saved))select.value=saved;}
 v.onVoicesChanged(voices);voices();paint();
 select.addEventListener("change",()=>v.setSettings({voice:select.value}));
 for(const x of [tempo,pitch])x.addEventListener("input",()=>{v.setSettings({rate:tempo.value,pitch:pitch.value});paint();});
 $("voiceSample").addEventListener("click",()=>playVoice("Moin Nils! Hier ist Willi. Ich bin startklar. Wat steht denn heut auf dem Zettel?"));
 $("voiceStop").addEventListener("click",()=>{v.stopSpeech();window.RNPiperVoice?.stop();});
 $("voiceStatus").textContent=window.RNPiperVoice?"Piper / Thorsten bereit zum Laden – Hörprobe starten.":"Browserstimme bereit – Hörprobe starten.";
}
async function sendText(text,fromMic=false){
 const q=String(text||"").trim();
 if(!q||busy)return "";
 busy=true;$("sendButton").disabled=true;bubble(q,true);
 try{
   const workerUrl=String(cfg.cloudflareWorkerUrl||"").replace(/\/$/,"");
   if(!/^https:\/\/[a-z0-9-]+(?:\.[a-z0-9-]+)*\.workers\.dev$/i.test(workerUrl))throw Error("Willi-KI ist noch nicht verbunden. Der Cloudflare-Worker muss zuerst eingerichtet werden.");
   if(!session?.access_token)throw Error("Bitte erneut anmelden.");
   const response=await fetch(workerUrl+"/chat",{method:"POST",headers:{"Content-Type":"application/json","Authorization":"Bearer "+session.access_token},body:JSON.stringify({text:q})});
   const r=await response.json().catch(()=>({error:"Unbekannte Serverantwort."}));
   if(!response.ok)throw Error(r.error||"Cloudflare-KI antwortet nicht.");
   const reply=typeof r.reply==="string"?r.reply:"Willi hat gerade keine Antwort geliefert.";
   bubble(reply);lastSpeech=reply;
   if(!fromMic){await playVoice(reply);}return reply;
 }catch(e){const errorText="Das klappt noch nicht: "+e.message;bubble(errorText);if(!fromMic)await playVoice(errorText);return errorText;}
 finally{busy=false;$("sendButton").disabled=false;}
}
function endMic(){
 listening=false;
 window.RNWilliVoice?.stopConversation();
 $("micToggle").textContent="🎙 Gespräch starten";
 $("voiceStatus").textContent="Gespräch beendet.";
}
function startMic(){
 const v=window.RNWilliVoice;
 if(!v){$("voiceStatus").textContent="Sprachsteuerung konnte nicht geladen werden.";return;}
 const state=v.startConversation(async text=>{
  if(!session)return "Du musst dich erst anmelden, damit ich mit den Aufträgen arbeiten kann.";
  return await sendText(text,true);
 },status=>{$("voiceStatus").textContent=status;});
 if(state.ok){listening=true;$("micToggle").textContent="■ Gespräch beenden";}
 else $("voiceStatus").textContent=state.message;
}
async function init(){
 if(initComplete)return;initComplete=true;
 $("loginForm").addEventListener("submit",async e=>{e.preventDefault();if(!supabase)return;const email=$("loginEmail").value.trim();$("loginButton").disabled=true;
  try{const {error}=await supabase.auth.signInWithOtp({email,options:{shouldCreateUser:false,emailRedirectTo:location.origin+location.pathname}});if(error)throw error;message("Prüfe deine E-Mails. Der Link führt dich zurück zu BüroPilot.");}
  catch(e){message(e.message);}finally{$("loginButton").disabled=false;}
 });
 $("logoutBtn").addEventListener("click",async()=>{endMic();if(supabase)await supabase.auth.signOut();session=null;showAuth();setStatus("Abgemeldet");});
 document.querySelectorAll(".tab").forEach(t=>t.addEventListener("click",()=>tab(t.dataset.tab)));
 $("refreshOverview").addEventListener("click",loadJobs);$("refreshJobs").addEventListener("click",loadJobs);$("openWilli").addEventListener("click",()=>tab("willi"));
 $("chatForm").addEventListener("submit",e=>{e.preventDefault();const x=$("chatInput");const t=x.value;x.value="";sendText(t);});
 $("micToggle").addEventListener("click",()=>listening?endMic():startMic());
 initializeVoice();
 if(!configured){showAuth();setup("Supabase noch nicht verbunden","Die GitHub-Pages-App ist vorbereitet. Sobald das Supabase-Projekt eingerichtet ist, wird hier der sichere Mitarbeiterzugang freigeschaltet. Trage niemals geheime API-Schlüssel in config.js ein.");setStatus("Supabase-Einrichtung fehlt");return;}
 if(!supabase){showAuth();setup("Supabase-Bibliothek nicht geladen","Prüfe die Internetverbindung oder den Script-Blocker.");setStatus("Verbindung nicht verfügbar");return;}
 supabase.auth.onAuthStateChange((e)=>{if(e==="SIGNED_OUT"){session=null;showAuth();}else if(e==="SIGNED_IN"||e==="TOKEN_REFRESHED"){queueMicrotask(()=>refreshSession().catch(console.warn));}});
 try{await refreshSession();}catch(e){showAuth();setup("Verbindungsfehler",e.message);setStatus("Verbindung fehlgeschlagen");}
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
})();
