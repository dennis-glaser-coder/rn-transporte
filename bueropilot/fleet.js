/* RN BueroPilot: simple fleet list and safe trailer connections. */
(()=>{"use strict";
const $=id=>document.getElementById(id);
const initial=[
["PB RN3240","Betonmischer 4 Achser"],["PB RN4241","Betonmischer 4 Achser"],["PB RN3242","Betonmischer 4 Achser"],["PB RN784","Sattelzugmaschine"],["PB RN2646","Sattelzugmaschine"],["PB RN1833","Betonpumpe M24"],["PB RN2636","Betonpumpe M36"],["PB RN 2412","Kippauflieger"],["PB RN 2312","Mischauflieger"],["PB RN 847","Mischauflieger"]
];
const previewKey="rn-bueropilot-trailer-selection-v1";
const trailerIds=new Set(initial.filter(([,kind])=>kind==="Kippauflieger"||kind==="Mischauflieger").map(([registration])=>registration));
const tractorIds=new Set(initial.filter(([,kind])=>kind==="Sattelzugmaschine").map(([registration])=>registration));
let localPairs={};
let localStorageAvailable=true;
try{
 const parsed=JSON.parse(localStorage.getItem(previewKey)||"{}");
 if(parsed&&typeof parsed==="object"&&!Array.isArray(parsed)){
  const used=new Set();
  for(const [tractor,trailer] of Object.entries(parsed)){
   if(tractorIds.has(tractor)&&trailerIds.has(trailer)&&!used.has(trailer)){localPairs[tractor]=trailer;used.add(trailer)}
  }
 }
}catch(_){localStorageAvailable=false}
function previewRows(){
 const rows=initial.map(([registration,kind])=>({id:registration,registration,kind,active:true,note:"",preview:true}));
 for(const [tractor,trailer] of Object.entries(localPairs)){
  const item=rows.find(x=>x.registration===trailer);
  if(item)item.connected_tractor_id=tractor;
 }
 return rows
}
function saveLocalPair(tractorId,trailerId){
 if(!tractorIds.has(tractorId))throw Error("Unbekannte Zugmaschine");
 if(trailerId&&!trailerIds.has(trailerId))throw Error("Unbekannter Auflieger");
 for(const [tractor,attached] of Object.entries(localPairs)){
  if(tractor!==tractorId&&trailerId&&attached===trailerId)throw Error("Der Auflieger ist bereits einer anderen Zugmaschine zugeordnet.")
 }
 if(trailerId)localPairs[tractorId]=trailerId;else delete localPairs[tractorId];
 try{localStorage.setItem(previewKey,JSON.stringify(localPairs))}catch(_){localStorageAvailable=false}
}
const isTrailer=v=>v.kind==="Kippauflieger"||v.kind==="Mischauflieger";
let db=null,rows=previewRows(),live=false,canWrite=false,org=null,editing=null,tractor=null,busy=false,loadPending=false;
const safe=t=>String(t??"");
function info(msg){$("fleetInfo").textContent=msg;$("fleetInfo").classList.toggle("live",live)}
function currentTrailer(v){return rows.find(x=>x.connected_tractor_id&&x.connected_tractor_id===v.id)}
function connectedTractor(v){return rows.find(x=>x.id===v.connected_tractor_id)}
function sorted(xs){return [...xs].sort((a,b)=>{const i=initial.findIndex(x=>x[0]===a.registration),j=initial.findIndex(x=>x[0]===b.registration);if(i>=0||j>=0)return (i<0?100+i:i)-(j<0?100+j:j);return a.registration.localeCompare(b.registration,"de")})}
function tag(tag,cls,value){const x=document.createElement(tag);if(cls)x.className=cls;if(value!=null)x.textContent=safe(value);return x}
function draw(){
 const active=rows.filter(x=>x.active&&!isTrailer(x));
 $("fleetTotal").textContent=String(active.length);
 $("fleetMixers").textContent=String(active.filter(x=>x.kind==="Betonmischer 4 Achser").length);
 $("fleetTractors").textContent=String(active.filter(x=>x.kind==="Sattelzugmaschine").length);
 $("fleetPumps").textContent=String(active.filter(x=>x.kind.startsWith("Betonpumpe")).length);
 document.querySelectorAll(".fleet-nav-count").forEach(x=>x.textContent=String(rows.length));
 const query=$("fleetSearch").value.trim().toLocaleLowerCase("de"),kind=$("fleetFilter").value,includeInactive=$("fleetInactive").checked;
 const filtered=sorted(rows.filter(v=>(includeInactive||v.active)&&(kind==="all"||kind==="Auflieger"&&isTrailer(v)||kind==="Betonpumpe"&&v.kind.startsWith("Betonpumpe")||kind===v.kind)&&[v.registration,v.kind,v.note,currentTrailer(v)?.registration,connectedTractor(v)?.registration].join(" ").toLocaleLowerCase("de").includes(query)));
 $("fleetEmpty").hidden=filtered.length>0;$("fleetList").replaceChildren();
 for(const [label,group] of [["Fahrzeuge",filtered.filter(v=>!isTrailer(v))],["Auflieger",filtered.filter(isTrailer)]]){
  if(!group.length)continue;const section=tag("section","fleet-group");
  const header=tag("div","fleet-group-header");header.append(tag("strong","",label),tag("span","",String(group.length)));section.append(header);
  for(const v of group){
   const row=tag("article","fleet-row"+(v.active?"":" inactive")),ty=isTrailer(v)?"trailer":v.kind==="Sattelzugmaschine"?"tractor":v.kind.startsWith("Betonpumpe")?"pump":"mixer";
   row.append(tag("div","fleet-type-icon "+ty,ty==="pump"?"◉":ty==="tractor"?"▰":ty==="trailer"?"▱":"▥"));
   const desc=tag("div","fleet-description");desc.append(tag("b","",v.registration),tag("span","",v.kind));
   if(v.note)desc.append(tag("small","",v.note));
   if(v.kind==="Sattelzugmaschine"){const attached=currentTrailer(v);desc.append(tag("small","fleet-attached",attached?"Auflieger: "+attached.registration:"Kein Auflieger verbunden"))}
   if(isTrailer(v)){const linked=connectedTractor(v);desc.append(tag("small","fleet-attached",linked?"Verbunden mit "+linked.registration:"Nicht verbunden"))}
   row.append(desc);
   const right=tag("div","fleet-row-right");right.append(tag("span","fleet-state "+(!v.active?"off":!live?"preview":""),live?(v.active?"Aktiv":v.unavailable_reason||"Inaktiv"):"Vorschau"));
   if(v.kind==="Sattelzugmaschine"){const btn=tag("button","fleet-connect","Auflieger wählen");btn.type="button";btn.disabled=!v.active;btn.title=!v.active?"Inaktive Zugmaschine":canWrite?"Auflieger firmenweit verbinden oder lösen":"Auflieger auf diesem Gerät auswählen";btn.onclick=()=>openTrailer(v);right.append(btn)}
   const editBtn=tag("button","fleet-edit","Bearbeiten");editBtn.type="button";editBtn.disabled=!canWrite;editBtn.onclick=()=>openEdit(v);right.append(editBtn);row.append(right);section.append(row);
  }
  $("fleetList").append(section);
 }
}
async function refresh(){
 if(loadPending)return;loadPending=true;
 try{
  const cfg=window.RN_PUBLIC_CONFIG||{};
  if(!window.supabase?.createClient||!cfg.supabaseUrl||!cfg.supabasePublishableKey)throw Error("Verbindung noch nicht bereit");
  if(!db)db=window.supabase.createClient(cfg.supabaseUrl,cfg.supabasePublishableKey,{auth:{autoRefreshToken:true,persistSession:true,detectSessionInUrl:true}});
  const {data:auth,error:authErr}=await db.auth.getSession();if(authErr)throw authErr;
  if(!auth?.session){live=false;canWrite=false;rows=previewRows();info("Vorschau · Auflieger lassen sich auswählen. Ohne Anmeldung gilt die Verbindung nur auf diesem Gerät.");return}
  const {data:staff,error:staffErr}=await db.from("rn_staff").select("org_id,role,enabled").eq("user_id",auth.session.user.id).maybeSingle();
  if(staffErr||!staff?.enabled){live=false;canWrite=false;rows=previewRows();info("Vorschau · Auflieger auswählen funktioniert bereits lokal. Für firmweite Speicherung fehlt noch die Mitarbeiterfreigabe.");return}
  const {data,error}=await db.from("rn_vehicles").select("id,org_id,registration,kind,note,active,unavailable_reason,connected_tractor_id").eq("org_id",staff.org_id).order("registration");
  if(error)throw error;
  rows=data;org=staff.org_id;live=true;canWrite=["admin","dispatcher"].includes(staff.role);
  info(canWrite?"Fuhrpark aktuell · Auflieger können direkt bei der Sattelzugmaschine verbunden werden.":"Fuhrpark aktuell · du hast nur Leserechte.");
 }catch(e){live=false;canWrite=false;rows=previewRows();info("Nur lokale Vorschau – die Datenbank ist nicht erreichbar: "+(e.message||"Fehler"))}
 finally{loadPending=false;draw()}
}
function checkWrite(){if(live&&canWrite)return true;info("Zum Bearbeiten bitte als freigegebener Mitarbeiter der Disposition anmelden.");return false}
function openTrailer(v){
 if(!v.active)return;
 tractor=v;const select=$("fleetTrailerChoice");select.replaceChildren(new Option("Keinen Auflieger verbinden","none"));
 const attached=currentTrailer(v);
 for(const x of sorted(rows.filter(x=>isTrailer(x)&&x.active))){
  const other=x.connected_tractor_id&&x.connected_tractor_id!==v.id;
  const label=x.registration+" · "+x.kind+(other?" (bereits verbunden)":"");
  const option=new Option(label,x.id);option.disabled=Boolean(other);select.append(option)
 }
 select.value=attached?.id||"none";$("fleetTrailerTractor").textContent="Zugmaschine: "+v.registration;
 const msg=$("fleetTrailerDialog").querySelector(".fleet-field-note");
 msg.textContent=canWrite?"Die Verbindung wird firmenweit gespeichert. Ein Auflieger kann nur an einer Zugmaschine hängen.":"Diese Auswahl wird nur auf deinem Gerät gespeichert – nicht in der Firmen-Datenbank. Ein Auflieger kann nur einmal ausgewählt werden.";
 $("fleetTrailerSave").textContent=canWrite?"Verbindung speichern":"Auf diesem Gerät speichern";
 $("fleetTrailerError").textContent="";$("fleetTrailerDialog").showModal();
}
async function saveTrailer(event){
 event.preventDefault();if(!tractor||busy)return;busy=true;$("fleetTrailerSave").disabled=true;
 try{
  const id=$("fleetTrailerChoice").value;
  if(live&&canWrite){
   const result=await db.rpc("rn_connect_trailer",{p_tractor_id:tractor.id,p_trailer_id:id==="none"?null:id});
   if(result.error)throw result.error;
   $("fleetTrailerDialog").close();await refresh();
   info(id==="none"?"Aufliegerverbindung gelöst.":"Aufliegerverbindung firmenweit gespeichert.");
  }else{
   // Never write to the company database from an unapproved session.
   const tractorRegistration=tractor.registration;
   const selected=id==="none"?null:rows.find(x=>x.id===id)?.registration;
   saveLocalPair(tractorRegistration,selected);
   rows=previewRows();
   live=false;canWrite=false;
   $("fleetTrailerDialog").close();
   draw();
   info((selected?"Auflieger "+selected+" mit "+tractorRegistration+" verbunden.":"Aufliegerverbindung gelöst.")+(localStorageAvailable?" Nur auf diesem Gerät gespeichert.":" Nur für diese Sitzung gespeichert."));
  }
 }catch(e){$("fleetTrailerError").textContent=e.message||"Verbindung nicht gespeichert."}
 finally{busy=false;$("fleetTrailerSave").disabled=false}
}
function openEdit(v){
 if(!checkWrite())return;
 editing=v||null;$("fleetDialogTitle").textContent=v?"Fahrzeug bearbeiten":"Fahrzeug hinzufügen";
 $("fleetRegistration").value=v?.registration||"";$("fleetKind").value=v?.kind||"Betonmischer 4 Achser";
 $("fleetNote").value=v?.note||"";$("fleetActive").value=v?.active===false?(v.unavailable_reason||"Sonstiges"):"active";
 $("fleetFormError").textContent="";$("fleetDialog").showModal()
}
async function saveVehicle(event){
 event.preventDefault();if(!checkWrite()||busy)return;
 const registration=$("fleetRegistration").value.trim().toUpperCase().replace(/\s+/g," ");
 const kind=$("fleetKind").value,reason=$("fleetActive").value,note=$("fleetNote").value.trim();
 const valid=["Betonmischer 4 Achser","Sattelzugmaschine","Betonpumpe M24","Betonpumpe M36","Kippauflieger","Mischauflieger","Sonstiges"];
 if(!/^[A-ZÄÖÜ0-9 -]{4,30}$/.test(registration)||!valid.includes(kind)){$("fleetFormError").textContent="Kennzeichen oder Fahrzeugtyp ungültig.";return}
 if(editing?.connected_tractor_id&&kind!=="Mischauflieger"&&kind!=="Kippauflieger"){$("fleetFormError").textContent="Bitte den Auflieger zuerst von der Zugmaschine lösen.";return}
 busy=true;$("fleetSave").disabled=true;
 try{
  const values={registration,kind,note,active:reason==="active",unavailable_reason:reason==="active"?null:reason};
  let res;
  if(editing)res=await db.from("rn_vehicles").update(values).eq("id",editing.id).eq("org_id",org).select("id");
  else res=await db.from("rn_vehicles").insert({...values,org_id:org}).select("id");
  if(res.error)throw res.error;if(!res.data?.length)throw Error("Änderung konnte nicht bestätigt werden");
  $("fleetDialog").close();await refresh();info("Fahrzeug erfolgreich gespeichert.")
 }catch(e){$("fleetFormError").textContent=e.message||"Fahrzeug konnte nicht gespeichert werden"}
 finally{busy=false;$("fleetSave").disabled=false}
}
function init(){
 $("fleetAdd").onclick=()=>openEdit(null);$("fleetRefresh").onclick=refresh;
 $("fleetSearch").oninput=draw;$("fleetFilter").onchange=draw;$("fleetInactive").onchange=draw;
 $("fleetCancel").onclick=$("fleetCancelX").onclick=()=>$("fleetDialog").close();
 $("fleetForm").onsubmit=saveVehicle;
 $("fleetTrailerCancel").onclick=$("fleetTrailerCloseX").onclick=()=>$("fleetTrailerDialog").close();
 $("fleetTrailerForm").onsubmit=saveTrailer;
 window.addEventListener("hashchange",()=>{if(location.hash==="#vehicles")refresh()});
 document.querySelector('[data-view="vehicles"]')?.addEventListener("click",refresh);
 draw();refresh()
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
})();