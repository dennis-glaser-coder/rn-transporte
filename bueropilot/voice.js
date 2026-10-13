/* RN Willi voice engine - browser-only synthesis, no paid API */
(function(root){
"use strict";
const synth=root.speechSynthesis;
const Recognition=root.SpeechRecognition||root.webkitSpeechRecognition;
let voices=[],chosen="",rate=0.88,pitch=0.82,utterance=null,done=null;
let active=false,recognizer=null,processing=false,recording=false,restart=null,generation=0,errors=0,onText=null,onStatus=null;
const listeners=new Set();
const defaults={voice:"rn-willi-voice",rate:"rn-willi-rate",pitch:"rn-willi-pitch"};
function number(v,lo,hi,def){v=Number(v);return Number.isFinite(v)&&v>=lo&&v<=hi?v:def;}
try{chosen=root.localStorage.getItem(defaults.voice)||"";rate=number(root.localStorage.getItem(defaults.rate),0.65,1.3,0.88);pitch=number(root.localStorage.getItem(defaults.pitch),0.65,1.2,0.82);}catch(_){}
function sayStatus(v){if(typeof onStatus==="function")onStatus(v);}
function voiceId(v){return v.voiceURI||v.name;}
function voiceScore(v){const n=(v.name||"").toLowerCase();return (/male|markus|michael|florian|stefan|conrad|hans|bernd|wolfgang/.test(n)?70:0)+(/natural/.test(n)?8:0)+(/de-de/i.test(v.lang)?10:0)-(/female|katja|anna|hedda|helga/.test(n)?60:0);}
function getVoices(){return voices.map(v=>({id:voiceId(v),name:v.name,label:v.name+" · "+v.lang,lang:v.lang}));}
function refreshVoices(){voices=synth?(synth.getVoices()||[]).filter(v=>/^de([-_]|$)/i.test(v.lang)).sort((a,b)=>voiceScore(b)-voiceScore(a)||a.name.localeCompare(b.name,"de")):[];if(chosen&&!voices.some(v=>voiceId(v)===chosen))chosen="";const list=getVoices();listeners.forEach(fn=>{try{fn(list);}catch(_){}});return list;}
function stopSpeech(){if(synth)try{synth.cancel();}catch(_){}utterance=null;if(done){const end=done;done=null;end({status:"stopped"});}}
function speak(raw){const text=String(raw||"").trim().slice(0,1200);if(!text)return Promise.resolve({status:"empty"});if(!synth||!root.SpeechSynthesisUtterance)return Promise.resolve({status:"unsupported"});stopSpeech();refreshVoices();
  return new Promise(resolve=>{let finished=false;const finish=out=>{if(finished)return;finished=true;if(done===finish)done=null;utterance=null;resolve(out);};done=finish;
  const u=new root.SpeechSynthesisUtterance(text);u.lang="de-DE";u.rate=rate;u.pitch=pitch;u.volume=1;
  const v=voices.find(x=>voiceId(x)===chosen)||voices[0];if(v)u.voice=v;utterance=u;
  u.onstart=()=>sayStatus("Willi spricht …");u.onend=()=>finish({status:"spoken"});u.onerror=e=>finish({status:"error",message:e.error});
  try{synth.resume();synth.speak(u);}catch(e){finish({status:"error",message:String(e.message||e)});}
});}
function stopListening(){active=false;generation++;clearTimeout(restart);restart=null;try{recognizer?.abort();}catch(_){}recognizer=null;recording=false;processing=false;stopSpeech();sayStatus("Gespräch beendet.");}
function startRecording(){if(!active||recording||processing||!recognizer)return;clearTimeout(restart);try{recognizer.start();recording=true;sayStatus("Willi hört zu …");}catch(e){recording=false;active=false;sayStatus("Mikrofon konnte nicht gestartet werden. Erneut versuchen.");}}
function startConversation(handler,status){
 if(!Recognition)return {ok:false,message:"Spracherkennung wird hier nicht unterstützt. Bitte Text eingeben."};
 if(!root.isSecureContext)return {ok:false,message:"Mikrofon funktioniert nur über HTTPS."};
 if(typeof handler!=="function")return {ok:false,message:"Keine Gesprächsfunktion vorhanden."};
 stopListening();active=true;onText=handler;onStatus=status;errors=0;
 const rec=new Recognition();recognizer=rec;rec.lang="de-DE";rec.continuous=false;rec.interimResults=false;rec.maxAlternatives=1;const id=generation;
 rec.onresult=evt=>{if(!active||id!==generation||processing)return;const parts=[];for(let i=evt.resultIndex||0;i<evt.results.length;i++){if(evt.results[i].isFinal)parts.push(evt.results[i][0]?.transcript||"");}const phrase=parts.join(" ").trim();if(!phrase)return;processing=true;recording=false;errors=0;sayStatus("Willi überlegt …");
  Promise.resolve().then(()=>handler(phrase)).then(answer=>{if(active&&id===generation&&typeof answer==="string"&&answer.trim())return speak(answer);}).catch(e=>sayStatus("Antwortfehler: "+String(e.message||e))).finally(()=>{processing=false;if(active&&id===generation)restart=setTimeout(startRecording,800);});
 };
 rec.onend=()=>{recording=false;if(active&&id===generation&&!processing&&errors<4){clearTimeout(restart);restart=setTimeout(startRecording,700);}};
 rec.onerror=e=>{recording=false;if(!active||id!==generation)return;errors++;if(["not-allowed","service-not-allowed","audio-capture"].includes(e.error)){stopListening();sayStatus("Mikrofon nicht erlaubt. Bitte die Browserberechtigung prüfen.");return;}if(e.error==="network"||errors>=4){stopListening();sayStatus("Spracherkennung angehalten. Erneut starten.");return;}sayStatus("Nicht verstanden, versuche es noch einmal …");};
 startRecording();return {ok:active};
}
const api={
 capabilities:()=>({speaking:!!(synth&&root.SpeechSynthesisUtterance),listening:!!(Recognition&&root.isSecureContext),free:true}),
 getVoices,refreshVoices,onVoicesChanged:fn=>{listeners.add(fn);return()=>listeners.delete(fn);},
 getSettings:()=>({voice:chosen||voiceId(voices[0]||{name:""}),rate,pitch}),
 setSettings:obj=>{if(obj.voice!==undefined&&(obj.voice===""||voices.some(v=>voiceId(v)===obj.voice)))chosen=obj.voice;if(obj.rate!==undefined)rate=number(obj.rate,0.65,1.3,0.88);if(obj.pitch!==undefined)pitch=number(obj.pitch,0.65,1.2,0.82);try{root.localStorage.setItem(defaults.voice,chosen);root.localStorage.setItem(defaults.rate,String(rate));root.localStorage.setItem(defaults.pitch,String(pitch));}catch(_){}return api.getSettings();},
 speak,stopSpeech,startConversation,stopConversation:stopListening,isConversationActive:()=>active
};
root.RNWilliVoice=api;
if(synth){refreshVoices();if(synth.addEventListener)synth.addEventListener("voiceschanged",refreshVoices);else synth.onvoiceschanged=refreshVoices;}
})(window);
