"use client";
import { useEffect, useState } from "react";
import { createClient } from "@supabase/supabase-js";
const supaUrl=process.env.NEXT_PUBLIC_SUPABASE_URL;
const supaKey=process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
const auth=supaUrl&&supaKey?createClient(supaUrl,supaKey):null;
export default function Home(){
 const [email,setEmail]=useState("");const [session,setSession]=useState(null);const [notice,setNotice]=useState("");
 const [status,setStatus]=useState({});const [jobs,setJobs]=useState([]);
 const [message,setMessage]=useState("");const [history,setHistory]=useState([{who:"willi",text:"Moin! Ich bin Willi. Wir testen hier zuerst den sicheren Zugang. Echte Aufträge ändern kann ich noch nicht."}]);
 const [busy,setBusy]=useState(false);
 useEffect(()=>{fetch("/api/status").then(r=>r.json()).then(setStatus).catch(()=>{});
  if(auth){auth.auth.getSession().then(({data})=>setSession(data.session));const {data:sub}=auth.auth.onAuthStateChange((_e,s)=>setSession(s));return()=>sub.subscription.unsubscribe();}
 },[]);
 async function call(path,opts={}){if(!auth)throw Error("Anmeldung nicht konfiguriert.");const {data}=await auth.auth.getSession();if(!data.session)throw Error("Bitte zuerst anmelden.");const r=await fetch(path,{...opts,headers:{"Content-Type":"application/json",Authorization:"Bearer "+data.session.access_token,...opts.headers}});const d=await r.json();if(!r.ok)throw Error(d.error||"Fehler");return d;}
 async function login(e){e.preventDefault();setNotice("");if(!auth){setNotice("Die Anmeldung muss erst auf dem Server eingerichtet werden.");return;}const {error}=await auth.auth.signInWithOtp({email,emailRedirectTo:window.location.origin});setNotice(error?error.message:"Prüfe deine E-Mails für den Anmeldelink.");}
 async function listJobs(){try{const d=await call("/api/jobs");setJobs(d.jobs||[]);setNotice("Aufträge geladen (nur lesen).");}catch(e){setNotice(e.message)}}
 async function send(e){e.preventDefault();const q=message.trim();if(!q||busy)return;setMessage("");setHistory(h=>[...h,{who:"me",text:q}]);setBusy(true);
  try{const r=await call("/api/chat",{method:"POST",body:JSON.stringify({text:q})});setHistory(h=>[...h,{who:"willi",text:r.reply}]);}
  catch(e){setHistory(h=>[...h,{who:"willi",text:"Das klappt noch nicht: "+e.message}]);}finally{setBusy(false)}
 }
 async function speak(text){try{if(!auth)throw Error("Anmeldung fehlt.");const {data}=await auth.auth.getSession();const r=await fetch("/api/speech",{method:"POST",headers:{"Content-Type":"application/json",Authorization:"Bearer "+data.session?.access_token},body:JSON.stringify({text:text.slice(0,500)})});if(!r.ok){const x=await r.json();throw Error(x.error||"Keine Sprachausgabe");}const blob=await r.blob();const url=URL.createObjectURL(blob);const audio=new Audio(url);audio.onended=()=>URL.revokeObjectURL(url);await audio.play()}catch(e){setNotice(e.message)}}
 return <><header><div className="rn"><span className="logo">RN</span><span>BüroPilot</span></div><span className="small">Interne Vorschau · {session?"Angemeldet":"Nicht angemeldet"}</span></header><main className="shell"><div className="hero"><h1>Moin Nils, wie machen wir's?</h1><p>Disposition, Aufträge und Willi. Schrittweise und sicher eingerichtet.</p></div>
 <div className="warn"><b>Technischer Pilot:</b> Keine produktiven Daten, keine Auftragsänderungen und kein automatisches Mithören. Erst nach abgesicherter Einrichtung freischalten.</div>
 <div className="layout"><section className="panel"><h2>Mitarbeiterzugang</h2>{!session?<form onSubmit={login}><p>E-Mail-Adresse eingeben. Ein Link wird an deine Adresse versendet. Eine Freigabe als RN-Mitarbeiter ist zusätzlich erforderlich.</p><div className="line"><input type="email" placeholder="E-Mail-Adresse" value={email} onChange={e=>setEmail(e.target.value)} required/><button>Link anfordern</button></div></form>:<div><p>Du bist angemeldet. Die Freigabe wird bei jedem Zugriff geprüft.</p><button className="secondary" onClick={()=>auth.auth.signOut()}>Abmelden</button></div>}
 <h2 style={{marginTop:26}}>Dispositionsübersicht</h2><p>Nur für freigegebene Mitarbeiter sichtbar.</p><button disabled={!session} onClick={listJobs}>Aufträge laden</button>
 <ul>{jobs.map(j=><li key={j.id}><b>{j.date} {j.start_time}</b> · {j.pump} · {j.customer} · {j.site}</li>)}</ul>
 </section><section className="panel"><h2>Willi · Chat</h2><p>Freie KI-Unterhaltung wird über einen geschützten Server angeschlossen. Schreibaktionen sind gesperrt.</p>
 <div aria-live="polite">{history.map((m,i)=><div key={i} className={"msg "+(m.who==="me"?"me":"")}><b>{m.who==="me"?"Nils":"Willi"}:</b> {m.text} {m.who==="willi"&&status.speechConfigured&&session?<button className="secondary" onClick={()=>speak(m.text)} aria-label="Antwort anhören">▶ Anhören</button>:null}</div>)}</div>
 <form onSubmit={send} className="line"><input aria-label="Nachricht an Willi" value={message} onChange={e=>setMessage(e.target.value)} placeholder="Frag Willi etwas ..." disabled={!session||busy}/><button disabled={!session||busy||!message.trim()}>Senden</button></form>
 <p className="fine">KI: {status.aiConfigured?"konfiguriert, Erreichbarkeit nicht getestet":"noch nicht eingerichtet"} · ElevenLabs: {status.speechConfigured?"konfiguriert":"nicht aktiv"}</p></section></div>
 {notice&&<p className="warn" role="status">{notice}</p>}
 <p className="fine">RN BüroPilot ist eine nichtproduktive Entwicklungsvorschau. Für echte Betriebsdaten ist eine separate Freigabe erforderlich.</p>
 </main></>
}
