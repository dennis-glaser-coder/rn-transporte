/* RN BüroPilot – genuine customer, quote, order and workforce workflows.
 * No mock records are ever written to company data. Every write is gated by Supabase RLS. */
(()=>{"use strict";
const $=id=>document.getElementById(id);
const H=s=>String(s??"").replace(/[&<>"']/g,ch=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[ch]));
const cfg=window.RN_PUBLIC_CONFIG||{};
let db=null,session=null,staff=null,write=false;
let customers=[],quotes=[],orders=[],vehicles=[],employees=[];
let editingQuote=null,convertingQuote=null,busy=false;
const viewIds=["customersView","offersView","jobsView","teamView"];
const banner='<p class="ops-context" role="status">Die geschützten Unternehmensdaten werden geladen …</p>';
function currency(n){return n==null?"":new Intl.NumberFormat("de-DE",{style:"currency",currency:"EUR"}).format(n)}
function mount(){
 $("customersView").innerHTML='<div class="page-heading"><div><div class="kicker">STAMMDATEN</div><h1>Kunden & Baustellen</h1><p>Kunden einmal erfassen und für Angebote wiederverwenden.</p></div></div>'+banner+
 '<div class="ops-two-col"><section class="surface"><div class="section-head"><div><h2>Kunde anlegen</h2><p>Zentrale Kundenkartei</p></div></div><form id="opsCustomerForm" class="ops-form"><label>Name / Firma *<input name="name" required maxlength="160" placeholder="Firma oder Ansprechpartner"></label><label>Telefon<input name="phone" maxlength="70" autocomplete="tel"></label><label>E-Mail<input name="email" type="email" maxlength="180" autocomplete="email"></label><label>Adresse<input name="address" maxlength="300" placeholder="Straße, Ort"></label><button class="button button-primary" type="submit">Kunden speichern</button><span class="ops-feedback" id="opsCustomerMessage" role="status"></span></form></section><section class="surface"><div class="section-head"><div><h2>Kundenübersicht</h2><p id="opsCustomerCount">Keine Kunden geladen</p></div><button class="button button-outline" id="opsReloadCustomers">↻ Aktualisieren</button></div><div id="opsCustomerList" class="ops-list"></div></section></div>';
 $("offersView").innerHTML='<div class="page-heading"><div><div class="kicker">ANGEBOTE</div><h1>Angebote erstellen</h1><p>Entwurf speichern und anschließend mit einem Klick in einen Auftrag umwandeln.</p></div></div>'+banner+
 '<div class="ops-two-col"><section class="surface"><div class="section-head"><div><h2 id="opsQuoteFormTitle">Neuer Angebotsentwurf</h2><p>Unverbindlicher Entwurf ohne automatische Preisberechnung</p></div></div><form class="ops-form" id="opsQuoteForm"><label>Kunde *<select name="customer_id" id="opsQuoteCustomer" required><option value="">Kunde wählen …</option></select></label><label>Baustelle / Einsatzort *<input name="site" required maxlength="240" placeholder="Adresse / Baustelle"></label><label>Leistung *<select name="service" required><option>Betonpumpe</option><option>Betontransport</option><option>Transport</option><option>Sonstige Dienstleistung</option></select></label><div class="ops-input-row"><label>Einsatzdatum *<input name="service_date" type="date" required></label><label>Beginn *<input name="start_time" type="time" required value="07:00"></label></div><label>Geplante Dauer (Minuten) *<input name="duration_minutes" type="number" required min="30" max="720" step="30" value="180"></label><label>Bemerkungen<textarea name="notes" rows="3" maxlength="2000" placeholder="z. B. Menge, Besonderheiten, Ansprechpartner"></textarea></label><div class="ops-inline-actions"><button class="button button-primary" type="submit" id="opsQuoteSave">Entwurf speichern</button><button class="button button-outline" type="button" id="opsQuoteReset">Zurücksetzen</button></div><span class="ops-feedback" id="opsQuoteMessage" role="status"></span></form><div class="subtle-note">Preise, Versand und rechtsverbindliche Angebote sind noch nicht eingerichtet. Hier wird der Auftragsentwurf mit Einsatzdaten gespeichert.</div></section><section class="surface"><div class="section-head"><div><h2>Gespeicherte Angebote</h2><p id="opsQuoteCount">Noch keine Angebote</p></div><button class="button button-outline" id="opsReloadQuotes">↻ Aktualisieren</button></div><div id="opsQuoteList" class="ops-list"></div></section></div>';
 $("jobsView").innerHTML='<div class="page-heading"><div><div class="kicker">EINSÄTZE</div><h1>Aufträge</h1><p>Angenommene Einsätze, Fahrzeuge, Zeiten und Status.</p></div></div>'+banner+
 '<section class="surface"><div class="section-head"><div><h2>Auftragsübersicht</h2><p>Über Angebote erfasste und bereits vorhandene RN-Aufträge</p></div><button id="opsReloadJobs" class="button button-outline">↻ Aktualisieren</button></div><div class="lifecycle"><span>Geplant</span><span>In Ausführung</span><span>Abgeschlossen</span><span>Storniert</span></div><div id="opsOrderList" class="ops-list"></div><div class="subtle-note">Die Rechnungserstellung wird separat freigeschaltet. „Abgerechnet“ wird hier noch nicht automatisch gesetzt.</div></section>';
 $("teamView").innerHTML='<div class="page-heading"><div><div class="kicker">MITARBEITER & FUHRPARK</div><h1>Mitarbeiter</h1><p>Mitarbeiter anlegen und fest einem Fahrzeug zuordnen.</p></div></div>'+banner+
 '<div class="ops-two-col"><section class="surface"><div class="section-head"><div><h2>Mitarbeiter erfassen</h2><p>Nur tatsächliche Mitarbeiter – keine Testnamen</p></div></div><form class="ops-form" id="opsEmployeeForm"><label>Name *<input name="display_name" required minlength="2" maxlength="100"></label><label>Tätigkeit<select name="role_name"><option>Fahrer</option><option>Pumpenmaschinist</option><option>Disposition</option><option>Büro</option></select></label><button class="button button-primary" type="submit">Mitarbeiter speichern</button><span class="ops-feedback" id="opsEmployeeMessage" role="status"></span></form></section><section class="surface"><div class="section-head"><div><h2>Mitarbeiter & Zuordnung</h2><p>Stammfahrzeug kann gewechselt werden</p></div><button class="button button-outline" id="opsReloadTeam">↻ Aktualisieren</button></div><div id="opsEmployeeList" class="ops-list"></div></section></div><div class="subtle-note">Hier wird ein zuständiger Mitarbeiter im Fahrzeugstamm hinterlegt. Fahrerlogin und rollenbezogene Tagesansichten sind ein gesonderter Entwicklungsschritt.</div>';
 const dialog=document.createElement("dialog");dialog.id="opsConvertDialog";dialog.className="fleet-dialog";dialog.innerHTML='<form id="opsConvertForm"><div class="fleet-dialog-head"><div><div class="kicker">AUFTRAG EINPLANEN</div><h2>Angebot umwandeln</h2></div><button type="button" class="fleet-dialog-close" id="opsConvertX" aria-label="Schließen">×</button></div><p id="opsConvertTitle"></p><label>Fahrzeug / Pumpe *<select id="opsConvertVehicle" required></select></label><label>Mitarbeiter (optional)<select id="opsConvertEmployee"><option value="">Noch nicht zugeordnet</option></select></label><p class="fleet-field-note">Bestätigung erstellt einen Auftrag und blockiert das Fahrzeug für die angegebene Einsatzzeit. Bei Überschneidung wird nichts gespeichert.</p><p class="ops-feedback" id="opsConvertMessage" role="alert"></p><div class="fleet-dialog-actions"><button class="button button-outline" type="button" id="opsConvertCancel">Abbrechen</button><button class="button button-primary" type="submit" id="opsConvertSave">Auftrag verbindlich einplanen</button></div></form>';
 document.body.append(dialog);
 document.querySelectorAll("[data-go='offers']").forEach(b=>b.addEventListener("click",()=>{}));
}
function context(msg){for(const id of viewIds){const el=$(id).querySelector(".ops-context");if(el)el.textContent=msg}}
function message(id,text){const el=$(id);if(el)el.textContent=text}
function writing(){if(write)return true;context("Nur Vorschau: Firmendaten dürfen hier ausschließlich mit einem freigegebenen Mitarbeiterkonto gespeichert werden.");return false}
async function getData(table,columns="*"){
 const r=await db.from(table).select(columns).eq("org_id",staff.org_id);
 if(r.error)throw r.error;return r.data||[];
}
async function refresh(){
 try{
  if(!window.supabase?.createClient||!cfg.supabaseUrl||!cfg.supabasePublishableKey)throw Error("Geschützte Datenbank nicht geladen");
  if(!db)db=window.RNBuroPilotSupabase||window.supabase.createClient(cfg.supabaseUrl,cfg.supabasePublishableKey,{auth:{persistSession:true,detectSessionInUrl:true,autoRefreshToken:true}});
  const auth=await db.auth.getSession();if(auth.error)throw auth.error;
  session=auth.data?.session||null;
  if(!session){staff=null;write=false;context("Du siehst die fertige Oberfläche. Für echte Speicherung ist eine gültige Mitarbeitersitzung erforderlich.");return}
  const r=await db.from("rn_staff").select("org_id,role,enabled").eq("user_id",session.user.id).maybeSingle();
  if(r.error)throw r.error;
  staff=r.data;
  if(!staff?.enabled){write=false;context("Mitarbeiterrechte sind für dieses Konto noch nicht freigeschaltet. Die Oberfläche bleibt ohne Schreibzugriff.");return}
  write=["admin","dispatcher"].includes(staff.role);
  const found=await Promise.all([
   getData("rn_customers","id,name,phone,email,address,created_at"),
   getData("rn_quotes","id,customer_id,site,service,service_date,start_time,duration_minutes,notes,status,created_at"),
   getData("rn_jobs","id,customer,site,date,start_time,duration_minutes,pump,status,vehicle_id,employee_id,quote_id"),
   getData("rn_vehicles","id,registration,kind,active,assigned_employee_id"),
   getData("rn_employees","id,display_name,role_name,active")
  ]);
  [customers,quotes,orders,vehicles,employees]=found;
  context(write?"Verbunden · Änderungen werden in der RN-Firmendatenbank gespeichert.":"Angemeldet · nur Leseberechtigung.");
 }catch(e){write=false;context("Die Daten können zurzeit nicht geladen werden: "+(e.message||String(e)))}
 finally{renderAll()}
}
function renderAll(){renderCustomers();renderQuotes();renderOrders();renderTeam()}
function renderCustomers(){
 const list=$("opsCustomerList");list.replaceChildren();
 const ordered=[...customers].sort((a,b)=>a.name.localeCompare(b.name,"de"));
 $("opsCustomerCount").textContent=ordered.length+" Kunden";
 if(!ordered.length)list.innerHTML='<div class="ops-empty">Noch keine Kunden erfasst.</div>';
 for(const c of ordered){const row=document.createElement("div");row.className="ops-record";row.innerHTML='<div><b>'+H(c.name)+'</b><small>'+H([c.address,c.phone,c.email].filter(Boolean).join(" · "))+'</small></div>';list.append(row)}
 const sel=$("opsQuoteCustomer"),selected=sel.value;sel.replaceChildren(new Option("Kunde wählen …",""));
 for(const c of ordered)sel.add(new Option(c.name,c.id));
 if(customers.some(x=>x.id===selected))sel.value=selected;
}
function renderQuotes(){
 const list=$("opsQuoteList");list.replaceChildren();
 const ordered=[...quotes].sort((a,b)=>String(b.created_at).localeCompare(String(a.created_at)));
 $("opsQuoteCount").textContent=ordered.length+" Entwürfe / Vorgänge";
 if(!ordered.length)list.innerHTML='<div class="ops-empty">Noch keine Angebote. Erstelle links den ersten Entwurf.</div>';
 for(const q of ordered){const name=customers.find(c=>c.id===q.customer_id)?.name||"Kunde";
  const row=document.createElement("article");row.className="ops-record ops-record-stacked";
  row.innerHTML='<div><div class="ops-record-top"><b>'+H(name)+'</b><span class="tag tag-neutral">'+H(q.status)+'</span></div><small>'+H(q.site)+' · '+H(q.service)+'</small><small>'+H(q.service_date)+' · '+H(String(q.start_time).slice(0,5))+' Uhr · '+H(q.duration_minutes)+' min</small></div>';
  if(q.status==="Entwurf"){
   const actions=document.createElement("div");actions.className="ops-inline-actions";
   const edit=document.createElement("button");edit.className="button button-outline";edit.textContent="Bearbeiten";edit.disabled=!write;edit.onclick=()=>editQuote(q);actions.append(edit);
   const convert=document.createElement("button");convert.className="button button-primary";convert.textContent="In Auftrag umwandeln ↗";convert.disabled=!write;convert.onclick=()=>convertQuote(q);actions.append(convert);row.append(actions)
  }
  list.append(row)
 }
}
function renderOrders(){
 const list=$("opsOrderList");list.replaceChildren();
 const ordered=[...orders].sort((a,b)=>String(a.date+" "+a.start_time).localeCompare(String(b.date+" "+b.start_time)));
 if(!ordered.length)list.innerHTML='<div class="ops-empty">Noch keine Aufträge. Ein freigegebenes Angebot erzeugt hier einen Auftrag und einen Kalendereintrag.</div>';
 for(const o of ordered){
  const row=document.createElement("article");row.className="ops-record ops-order";
  const start=String(o.start_time||"").slice(0,5);
  row.innerHTML='<div><div class="ops-record-top"><b>'+H(o.customer)+'</b><span class="tag tag-neutral">'+H(o.status)+'</span></div><small>'+H(o.date)+' · '+H(start)+' Uhr · '+H(o.duration_minutes)+' min</small><small>'+H(o.site)+' · '+H(o.pump)+'</small></div>';
  const target=o.status==="Geplant"?"In Ausführung":o.status==="In Ausführung"?"Abgeschlossen":null;
  if(target){const controls=document.createElement("div");controls.className="ops-inline-actions";const button=document.createElement("button");button.className="button button-outline";button.textContent=target==="In Ausführung"?"Einsatz starten":"Einsatz abschließen";button.disabled=!write;button.onclick=()=>advance(o,target);controls.append(button);
   if(o.status==="Geplant"){const cancel=document.createElement("button");cancel.className="button button-outline";cancel.textContent="Stornieren";cancel.disabled=!write;cancel.onclick=()=>advance(o,"Storniert");controls.append(cancel)}row.append(controls)}
  list.append(row)
 }
}
function renderTeam(){
 const list=$("opsEmployeeList");list.replaceChildren();
 const ordered=[...employees].sort((a,b)=>a.display_name.localeCompare(b.display_name,"de"));
 if(!ordered.length)list.innerHTML='<div class="ops-empty">Noch keine Mitarbeiter angelegt.</div>';
 for(const emp of ordered){
  const row=document.createElement("div");row.className="ops-record ops-record-stacked";
  row.innerHTML='<div><b>'+H(emp.display_name)+'</b><small>'+H(emp.role_name)+' · '+(emp.active?"Aktiv":"Inaktiv")+'</small></div>';
  const select=document.createElement("select");select.className="ops-car-select";select.disabled=!write;select.add(new Option("Kein Stammfahrzeug zugeordnet",""));
  for(const v of vehicles.filter(v=>v.active&&!/auflieger$/.test(v.kind)))select.add(new Option(v.registration+" · "+v.kind,v.id));
  const current=vehicles.find(v=>v.assigned_employee_id===emp.id);select.value=current?.id||"";
  select.onchange=()=>assignVehicle(emp.id,select.value);
  row.append(select);list.append(row)
 }
}
function editQuote(q){
 if(!writing())return;editingQuote=q;
 const f=$("opsQuoteForm");for(const field of ["customer_id","site","service","service_date","start_time","duration_minutes","notes"]){const el=f.elements.namedItem(field);if(el)el.value=q[field]??""}
 $("opsQuoteFormTitle").textContent="Entwurf bearbeiten";$("opsQuoteSave").textContent="Änderungen speichern";message("opsQuoteMessage","");$("offersView").scrollIntoView({behavior:"smooth"});
}
function resetQuote(){$("opsQuoteForm").reset();editingQuote=null;$("opsQuoteFormTitle").textContent="Neuer Angebotsentwurf";$("opsQuoteSave").textContent="Entwurf speichern";message("opsQuoteMessage","")}
function convertQuote(q){
 if(!writing())return;
 convertingQuote=q;
 const sel=$("opsConvertVehicle");sel.replaceChildren(new Option("Fahrzeug auswählen …",""));
 for(const v of vehicles.filter(v=>v.active&&!/auflieger$/.test(v.kind)&&(q.service!=="Betonpumpe"||v.kind.startsWith("Betonpumpe"))&&(q.service!=="Betontransport"||["Betonmischer 4 Achser","Sattelzugmaschine"].includes(v.kind))))sel.add(new Option(v.registration+" · "+v.kind,v.id));
 const emp=$("opsConvertEmployee");emp.replaceChildren(new Option("Noch nicht zugeordnet",""));for(const person of employees.filter(x=>x.active))emp.add(new Option(person.display_name,person.id));
 $("opsConvertTitle").textContent=(customers.find(c=>c.id===q.customer_id)?.name||"Angebot")+" · "+q.service_date+" · "+String(q.start_time).slice(0,5)+" Uhr";
 message("opsConvertMessage","");$("opsConvertDialog").showModal()
}
async function onCustomer(e){
 e.preventDefault();if(!writing()||busy)return;const form=e.currentTarget,fd=new FormData(form),name=String(fd.get("name")||"").trim();
 if(name.length<2)return;busy=true;
 try{const r=await db.from("rn_customers").insert({org_id:staff.org_id,name,phone:String(fd.get("phone")||"").trim(),email:String(fd.get("email")||"").trim(),address:String(fd.get("address")||"").trim()}).select("id");
  if(r.error||!r.data?.length)throw r.error||Error("Kunde nicht gespeichert");form.reset();message("opsCustomerMessage","Kunde wurde gespeichert.");await refresh()
 }catch(err){message("opsCustomerMessage","Speichern fehlgeschlagen: "+err.message)}finally{busy=false}
}
async function onQuote(e){
 e.preventDefault();if(!writing()||busy)return;const form=e.currentTarget,fd=new FormData(form);
 const record={customer_id:String(fd.get("customer_id")||""),site:String(fd.get("site")||"").trim(),service:String(fd.get("service")||"").trim(),service_date:String(fd.get("service_date")||""),start_time:String(fd.get("start_time")||""),duration_minutes:Number(fd.get("duration_minutes")),notes:String(fd.get("notes")||"").trim()};
 if(!record.customer_id||!record.site||!record.service_date||!record.start_time||record.duration_minutes<30||record.duration_minutes>720){message("opsQuoteMessage","Bitte alle Pflichtfelder korrekt ausfüllen.");return}
 busy=true;try{let r;if(editingQuote)r=await db.from("rn_quotes").update(record).eq("id",editingQuote.id).eq("org_id",staff.org_id).select("id");else r=await db.from("rn_quotes").insert({...record,org_id:staff.org_id,created_by:session.user.id,status:"Entwurf"}).select("id");if(r.error||!r.data?.length)throw r.error||Error("Entwurf nicht gespeichert");resetQuote();message("opsQuoteMessage","Angebotsentwurf erfolgreich gespeichert.");await refresh()}catch(err){message("opsQuoteMessage","Speichern fehlgeschlagen: "+(err.message||String(err)))}finally{busy=false}
}
async function onConvert(e){
 e.preventDefault();if(!writing()||!convertingQuote||busy)return;
 const vehicle=$("opsConvertVehicle").value,employee=$("opsConvertEmployee").value;
 if(!vehicle){message("opsConvertMessage","Bitte ein Fahrzeug auswählen.");return}
 if(!window.confirm("Aus dem Angebot jetzt einen echten Auftrag erstellen und das Fahrzeug verbindlich einplanen?"))return;
 busy=true;$("opsConvertSave").disabled=true;
 try{const r=await db.rpc("rn_quote_to_job",{p_quote_id:convertingQuote.id,p_vehicle_id:vehicle,p_employee_id:employee||null});
  if(r.error)throw r.error;
  $("opsConvertDialog").close();convertingQuote=null;await refresh();
  document.querySelector('[data-view="jobs"]')?.click();
  $("opsOrderList").prepend(Object.assign(document.createElement("p"),{className:"ops-feedback",textContent:"Auftrag gespeichert und Fahrzeugzeit eingeplant."}));
  window.RNBuroPilotReloadJobs?.();
 }catch(err){message("opsConvertMessage","Auftrag konnte nicht gespeichert werden: "+(err.code==="23P01"?"Fahrzeug ist zu dieser Zeit bereits eingeplant.":err.message||String(err)))}
 finally{busy=false;$("opsConvertSave").disabled=false}
}
async function advance(job,to){
 if(!writing()||busy)return;if(!window.confirm("Auftrag auf „"+to+"“ setzen?"))return;busy=true;
 try{const r=await db.rpc("rn_job_advance",{p_job_id:job.id,p_target_status:to});if(r.error)throw r.error;await refresh();document.querySelector("#refreshJobs")?.click()}
 catch(err){window.alert("Statusänderung nicht möglich: "+(err.message||String(err)))}finally{busy=false}
}
async function onEmployee(e){
 e.preventDefault();if(!writing()||busy)return;busy=true;const f=e.currentTarget,fd=new FormData(f);
 try{const r=await db.from("rn_employees").insert({org_id:staff.org_id,display_name:String(fd.get("display_name")||"").trim(),role_name:String(fd.get("role_name")||"Fahrer")}).select("id");if(r.error||!r.data?.length)throw r.error||Error("Mitarbeiter nicht gespeichert");f.reset();message("opsEmployeeMessage","Mitarbeiter gespeichert.");await refresh()}catch(err){message("opsEmployeeMessage","Speichern fehlgeschlagen: "+err.message)}finally{busy=false}
}
async function assignVehicle(employeeId,vehicleId){
 if(!writing()||busy)return;busy=true;
 try{
  const current=vehicles.find(v=>v.assigned_employee_id===employeeId);
  if(current&&current.id!==vehicleId){const r=await db.from("rn_vehicles").update({assigned_employee_id:null}).eq("id",current.id).eq("org_id",staff.org_id).select("id");if(r.error)throw r.error}
  if(vehicleId){const r=await db.from("rn_vehicles").update({assigned_employee_id:employeeId}).eq("id",vehicleId).eq("org_id",staff.org_id).select("id");if(r.error)throw r.error}
  await refresh()
 }catch(err){window.alert("Fahrzeugzuordnung fehlgeschlagen: "+err.message);await refresh()}finally{busy=false}
}
function init(){
 mount();
 $("opsCustomerForm").addEventListener("submit",onCustomer);
 $("opsQuoteForm").addEventListener("submit",onQuote);
 $("opsQuoteReset").onclick=resetQuote;
 $("opsConvertForm").addEventListener("submit",onConvert);
 $("opsConvertCancel").onclick=$("opsConvertX").onclick=()=>$("opsConvertDialog").close();
 $("opsEmployeeForm").addEventListener("submit",onEmployee);
 for(const [id,handler] of [["opsReloadCustomers",refresh],["opsReloadQuotes",refresh],["opsReloadJobs",refresh],["opsReloadTeam",refresh]])$(id).onclick=handler;
 for(const view of ["customers","offers","jobs","team"])document.querySelector('[data-view="'+view+'"]')?.addEventListener("click",refresh);
 window.addEventListener("hashchange",()=>{if(["#offers","#jobs","#customers","#team"].includes(location.hash))refresh()});
 refresh();
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
})();