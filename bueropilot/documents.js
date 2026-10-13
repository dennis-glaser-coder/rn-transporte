/* RN BüroPilot – supporting workflows: sites, reviewed timesheets, weekly toll CSV archive, invoice drafts.
 * All company writes require authenticated and enabled dispatcher/admin staff. */
(()=>{"use strict";
const $=id=>document.getElementById(id),cfg=window.RN_PUBLIC_CONFIG||{};
const esc=s=>String(s??"").replace(/[&<>"']/g,ch=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[ch]));
let db=null,session=null,staff=null,writer=false,sites=[],customers=[],orders=[],imports=[],timesheets=[],invoices=[],csv=null,working=false;
function msg(id,v){if($(id))$(id).textContent=v}
function client(){if(!window.supabase?.createClient||!cfg.supabaseUrl||!cfg.supabasePublishableKey)throw Error("Datenbank nicht erreichbar");if(!db)db=window.RNBuroPilotSupabase||window.supabase.createClient(cfg.supabaseUrl,cfg.supabasePublishableKey,{auth:{persistSession:true,detectSessionInUrl:true,autoRefreshToken:true}});return db}
async function load(){
 try{
  const c=client(),a=await c.auth.getSession();if(a.error)throw a.error;session=a.data?.session||null;
  if(!session){writer=false;staff=null;setStatus("Nur Vorschau. Zum zentralen Speichern wird eine berechtigte Firmensitzung benötigt.");return}
  const sr=await c.from("rn_staff").select("org_id,role,enabled").eq("user_id",session.user.id).maybeSingle();
  if(sr.error)throw sr.error;staff=sr.data;
  if(!staff?.enabled){writer=false;setStatus("Ohne Mitarbeiterfreigabe können keine Firmendaten verändert werden.");return}
  writer=["admin","dispatcher"].includes(staff.role);
  const query=(t,fields)=>c.from(t).select(fields).eq("org_id",staff.org_id);
  const [s,cu,jo,imp,ts,inv]=await Promise.all([
   query("rn_customer_sites","id,customer_id,title,address,notes"),
   query("rn_customers","id,name"),
   query("rn_jobs","id,customer,site,date,start_time,pump,status"),
   query("rn_toll_imports","id,file_name,calendar_week,row_count,status,created_at"),
   query("rn_timesheets","id,employee_name,work_date,worked_hours,created_at"),
   query("rn_invoice_drafts","id,job_id,description,customer_snapshot,site_snapshot,net_amount,vat_percent,status,created_at")
  ]);
  const err=[s,cu,jo,imp,ts,inv].find(x=>x.error);if(err)throw err.error;
  sites=s.data||[];customers=cu.data||[];orders=jo.data||[];imports=imp.data||[];timesheets=ts.data||[];invoices=inv.data||[];
  setStatus(writer?"Firmendaten geladen · Speicherung aktiv.":"Leserechte aktiv · Änderungen für diese Rolle gesperrt.");
 }catch(e){writer=false;setStatus("Daten konnten nicht geladen werden: "+(e.message||String(e)))}
 finally{render()}
}
function setStatus(t){for(const id of ["docsSitesMsg","docsTollAccess","docsTimesheetAccess","docsInvoiceAccess"]){if($(id))$(id).textContent=t}}
function writable(){if(writer&&staff&&session)return true;setStatus("Speichern nicht möglich: Es ist ein berechtigter Mitarbeiterzugang erforderlich.");return false}
function mount(){
 const sitesEl=document.createElement("section");sitesEl.className="surface docs-append";
 sitesEl.innerHTML='<div class="section-head"><div><h2>Baustellen / Einsatzorte</h2><p>Wiederverwendbare Standorte pro Kunde</p></div></div><div class="ops-two-col"><form id="docsSiteForm" class="ops-form"><label>Kunde *<select id="docsSiteCustomer" required></select></label><label>Bezeichnung *<input id="docsSiteTitle" required maxlength="120" placeholder="z. B. Neubau Schule"></label><label>Adresse *<input id="docsSiteAddress" required maxlength="240" placeholder="Straße, Ort"></label><button class="button button-primary" type="submit">Baustelle speichern</button><p class="ops-feedback" id="docsSitesMsg" role="status"></p></form><div id="docsSiteList" class="ops-list"></div></div>';
 $("customersView").append(sitesEl);
 const quoteSite=document.createElement("div");quoteSite.className="ops-form-row";quoteSite.innerHTML='<label>Gespeicherte Baustelle übernehmen<select id="docsQuoteSite"><option value="">Baustelle optional wählen …</option></select></label>';
 const quoteForm=$("opsQuoteForm");quoteForm.querySelector('label:nth-child(2)').before(quoteSite);
 const toll=$("tollView").querySelector(".surface"),tollPanel=document.createElement("div");tollPanel.className="docs-import";
 tollPanel.innerHTML='<div class="docs-action-row"><button id="docsTollSave" class="button button-primary" type="button" disabled>Geprüfte Wochen-CSV in BüroPilot speichern</button><span id="docsTollMessage" class="ops-feedback" role="status">Bitte eine CSV-Datei und Kalenderwoche wählen.</span></div><p id="docsTollAccess" class="ops-feedback" role="status"></p><div class="section-head"><div><h2>Importhistorie</h2><p>Gespeicherte CSV-Dateien; Mautzeilen werden noch nicht automatisch Fahrzeugen zugeordnet</p></div></div><div id="docsTollHistory" class="ops-list"></div>';
 toll.append(tollPanel);
 const ts=$("timesheetsView");const tsPanel=document.createElement("section");tsPanel.className="surface docs-append";
 tsPanel.innerHTML='<div class="section-head"><div><h2>Geprüfte Stundenzettel</h2><p>Nach manueller Kontrolle in der geschützten Datenbank speichern</p></div></div><div class="docs-action-row"><label class="docs-job-label">Auftrag zuordnen (optional)<select id="docsTsJob"><option value="">Noch nicht zugeordnet</option></select></label><button class="button button-primary" type="button" id="docsTsStore">Prüfung bestätigen & speichern</button></div><p class="ops-feedback" id="docsTimesheetMessage" role="status">Zuerst oben Foto erfassen, prüfen und Bestätigung anhaken.</p><p id="docsTimesheetAccess" class="ops-feedback" role="status"></p><div id="docsTimesheetHistory" class="ops-list"></div><div class="subtle-note">Hier werden geprüfte Daten und OCR-Text, nicht das ursprüngliche Foto gespeichert. Original-Stundenzettel separat aufbewahren.</div>';
 ts.append(tsPanel);
 const iv=$("invoicesView");iv.innerHTML='<div class="page-heading"><div><div class="kicker">ABRECHNUNG</div><h1>Rechnungsentwürfe</h1><p>Aus abgeschlossenen Aufträgen einen überprüfbaren Abrechnungsentwurf erzeugen.</p></div></div><p class="ops-context">Noch keine rechtlich verbindliche Rechnungsausgabe: Nummernvergabe, archivierte Rechnungen und Verfahrensdokumentation fehlen noch.</p><div class="ops-two-col"><section class="surface"><div class="section-head"><div><h2>Neuer Entwurf</h2><p>Grundlage: abgeschlossener Auftrag</p></div></div><form class="ops-form" id="docsInvoiceForm"><label>Abgeschlossener Auftrag *<select id="docsInvoiceJob" required></select></label><label>Leistung / Beschreibung *<input id="docsInvoiceDescription" maxlength="500" required placeholder="Leistung laut Auftrag"></label><label>Nettobetrag in EUR *<input id="docsInvoiceNet" type="number" min="0" max="100000000" step=".01" required placeholder="0,00"></label><label>Umsatzsteuersatz *<select id="docsInvoiceVat"><option value="19">19 %</option><option value="7">7 %</option><option value="0">0 %</option></select></label><div id="docsInvoiceGross" class="docs-total">Brutto: –</div><button type="submit" class="button button-primary">Rechnungsentwurf speichern</button><span id="docsInvoiceMessage" class="ops-feedback" role="status"></span></form></section><section class="surface"><div class="section-head"><div><h2>Entwürfe</h2><p id="docsInvoiceAccess" class="ops-feedback">Noch keine Abrechnung geladen</p></div></div><div id="docsInvoiceList" class="ops-list"></div></section></div><div class="subtle-note">Aus dieser Funktion wird ausdrücklich keine Rechnung versandt oder als GoBD-konform ausgegeben. Steuerliche Angaben vor Freigabe durch das Büro prüfen.</div>';
}
function render(){
 if(!$("docsSiteCustomer"))return;
 const select=$("docsSiteCustomer"),previous=select.value;select.replaceChildren(new Option("Kunden auswählen",""));
 for(const c of customers)select.add(new Option(c.name,c.id));if(customers.some(c=>c.id===previous))select.value=previous;
 const sl=$("docsSiteList");sl.replaceChildren();if(!sites.length)sl.innerHTML='<p class="ops-empty">Noch keine Baustellen erfasst.</p>';
 for(const s of sites){const el=document.createElement("div");el.className="ops-record";const c=customers.find(c=>c.id===s.customer_id);el.innerHTML='<div><b>'+esc(s.title)+'</b><small>'+esc(s.address)+' · '+esc(c?.name||"Kunde")+'</small></div>';sl.append(el)}
 updateQuoteSites();
 const tl=$("docsTollHistory");tl.replaceChildren();if(!imports.length)tl.innerHTML='<p class="ops-empty">Bisher keine Wochen-CSV gespeichert.</p>';
 for(const x of [...imports].sort((a,b)=>String(b.created_at).localeCompare(String(a.created_at)))){const el=document.createElement("div");el.className="ops-record";el.innerHTML='<div><b>'+esc(x.file_name)+'</b><small>KW '+esc(x.calendar_week)+' · '+esc(x.row_count)+' Zeilen · '+esc(x.status)+'</small></div>';tl.append(el)}
 const jobSel=$("docsTsJob"),prev=jobSel.value;jobSel.replaceChildren(new Option("Kein Auftrag",""));for(const j of orders)jobSel.add(new Option(j.date+" · "+j.customer+" · "+j.pump,j.id));if(orders.some(j=>j.id===prev))jobSel.value=prev;
 const tsl=$("docsTimesheetHistory");tsl.replaceChildren();if(!timesheets.length)tsl.innerHTML='<p class="ops-empty">Noch keine geprüften Zettel in der Datenbank.</p>';
 for(const x of timesheets){const el=document.createElement("div");el.className="ops-record";el.innerHTML='<div><b>'+esc(x.employee_name)+'</b><small>'+esc(x.work_date)+' · '+esc(x.worked_hours)+' Stunden</small></div>';tsl.append(el)}
 const job=$("docsInvoiceJob"),val=job.value;job.replaceChildren(new Option("Abgeschlossenen Auftrag wählen …",""));
 for(const j of orders.filter(x=>x.status==="Abgeschlossen"&&!invoices.some(i=>i.job_id===x.id)))job.add(new Option(j.date+" · "+j.customer+" · "+j.pump,j.id));if(orders.some(x=>x.id===val))job.value=val;
 const il=$("docsInvoiceList");il.replaceChildren();if(!invoices.length)il.innerHTML='<p class="ops-empty">Noch keine Rechnungsentwürfe erfasst.</p>';
 for(const i of invoices){const gross=Number(i.net_amount)*(1+Number(i.vat_percent)/100);const el=document.createElement("div");el.className="ops-record";el.innerHTML='<div><b>'+esc(i.customer_snapshot)+'</b><small>'+esc(i.description)+' · Netto '+fmtMoney(i.net_amount)+' · Brutto '+fmtMoney(gross)+'</small><small>Rechnungsentwurf · keine Rechnungsnummer</small></div>';il.append(el)}
}
function fmtMoney(x){const n=Number(x);return Number.isFinite(n)?new Intl.NumberFormat("de-DE",{style:"currency",currency:"EUR"}).format(n):"–"}
function updateQuoteSites(){
 const select=$("docsQuoteSite");if(!select)return;const form=$("opsQuoteForm"),clientId=form.elements.namedItem("customer_id")?.value;
 select.replaceChildren(new Option("Baustelle optional wählen …",""));
 for(const s of sites.filter(x=>x.customer_id===clientId))select.add(new Option(s.title+" · "+s.address,s.address));
}
async function onSite(e){
 e.preventDefault();if(!writable()||working)return;working=true;
 try{const row={org_id:staff.org_id,customer_id:$("docsSiteCustomer").value,title:$("docsSiteTitle").value.trim(),address:$("docsSiteAddress").value.trim()};const r=await db.from("rn_customer_sites").insert(row).select("id");if(r.error||!r.data?.length)throw r.error||Error("Baustelle nicht gespeichert");$("docsSiteForm").reset();msg("docsSitesMsg","Baustelle gespeichert.");await load()}catch(err){msg("docsSitesMsg",err.message)}finally{working=false}
}
const getFile=()=>$("csvFile")?.files?.[0];
async function validateTollFile(){
 csv=null;$("docsTollSave").disabled=true;
 const f=getFile();if(!f){msg("docsTollMessage","Keine Datei ausgewählt.");return}
 try{
  if(f.size>8*1024*1024)throw Error("Maximal 8 MB pro Datei");
  const api=window.RNBuroPilotCSV;if(!api)throw Error("CSV-Prüfung nicht geladen");
  const text=(await f.text()).replace(/^\uFEFF/,"");
  if(text.includes("�"))throw Error("Unbekannte Zeichencodierung. Bitte UTF-8 verwenden");
  const sep=api.delimiter(text),lines=api.parseDelimited(text,sep);
  if(lines.length<2||lines[0].length<2)throw Error("Keine gültigen Tabellendaten gefunden");
  if(lines.slice(1).some(x=>x.length!==lines[0].length))throw Error("Zeilen haben unterschiedliche Spaltenanzahlen");
  const week=$("tollWeek").value;
  if(!/^\d{4}-W\d{2}$/.test(week))throw Error("Bitte zuerst eine Kalenderwoche angeben");
  csv={file_name:f.name,calendar_week:week,headers:lines[0],raw_rows:lines.slice(1),row_count:lines.length-1,source_text:text};
  $("docsTollSave").disabled=false;
  msg("docsTollMessage",csv.row_count+" Zeilen geprüft · Speichern möglich. Keine automatische Fahrzeugzuordnung.");
 }catch(e){msg("docsTollMessage","Dateiprüfung: "+e.message)}
}
async function saveToll(){
 if(!writable()||working||!csv)return;
 if(!window.confirm("Diese "+csv.row_count+" Maut-CSV-Zeilen in der RN-Datenbank archivieren? Es erfolgt noch keine automatische Mautzuordnung."))return;
 working=true;$("docsTollSave").disabled=true;
 try{
  if(!window.crypto?.subtle)throw Error("HTTPS / kryptografische Prüfsumme erforderlich");
  const bytes=new TextEncoder().encode(csv.source_text),hash=await crypto.subtle.digest("SHA-256",bytes);
  const hex=Array.from(new Uint8Array(hash),b=>b.toString(16).padStart(2,"0")).join("");
  const data={org_id:staff.org_id,file_name:csv.file_name,calendar_week:csv.calendar_week,
   file_sha256:hex,headers:csv.headers,raw_rows:csv.raw_rows,row_count:csv.row_count,created_by:session.user.id};
  const r=await db.from("rn_toll_imports").insert(data).select("id");
  if(r.error||!r.data?.length)throw r.error||Error("CSV nicht gespeichert");
  msg("docsTollMessage","Wochen-CSV zentral gespeichert. Importhistorie wurde ergänzt.");csv=null;await load()
 }catch(e){msg("docsTollMessage","Speichern fehlgeschlagen: "+(e.code==="23505"?"Diese Datei wurde bereits importiert.":e.message))}
 finally{working=false}
}
async function saveTimesheet(){
 if(!writable()||working)return;
 const photo=$("tsPhoto")?.files?.[0];if(!photo||!$("tsConfirmed")?.checked){msg("docsTimesheetMessage","Bitte Foto auswählen und die Angaben bestätigen.");return}
 const employee=$("tsDriver").value.trim(),date=$("tsDate").value,hours=Number($("tsHours").value),pause=Number($("tsBreak").value||0);
 if(employee.length<2||!date||!Number.isFinite(hours)||hours<=0||hours>24||!Number.isInteger(pause)||pause<0||pause>900){msg("docsTimesheetMessage","Mitarbeiter, Datum, Stunden oder Pause sind ungültig.");return}
 working=true;try{
  const row={org_id:staff.org_id,job_id:$("docsTsJob").value||null,employee_name:employee,work_date:date,
   start_time:$("tsFrom").value||null,end_time:$("tsTo").value||null,pause_minutes:pause,worked_hours:hours,
   vehicle_text:$("tsVehicle").value.trim(),site_text:$("tsSite").value.trim(),source_filename:photo.name,
   ocr_text:$("tsRaw").value.slice(0,20000),created_by:session.user.id};
  const r=await db.from("rn_timesheets").insert(row).select("id");
  if(r.error||!r.data?.length)throw r.error||Error("Stundenzettel nicht gespeichert");
  msg("docsTimesheetMessage","Geprüfte Stundendaten gespeichert. Originalfoto bitte weiter aufbewahren.");await load()
 }catch(e){msg("docsTimesheetMessage","Speichern fehlgeschlagen: "+e.message)}
 finally{working=false}
}
async function saveInvoice(e){
 e.preventDefault();if(!writable()||working)return;
 const id=$("docsInvoiceJob").value,job=orders.find(x=>x.id===id&&x.status==="Abgeschlossen");
 if(!job){msg("docsInvoiceMessage","Bitte einen abgeschlossenen Auftrag auswählen.");return}
 const amount=Number($("docsInvoiceNet").value),tax=Number($("docsInvoiceVat").value),description=$("docsInvoiceDescription").value.trim();
 if(!Number.isFinite(amount)||amount<0||!Number.isFinite(tax)||description.length<3){msg("docsInvoiceMessage","Betrag, Steuer oder Beschreibung ungültig.");return}
 working=true;try{
  const data={org_id:staff.org_id,job_id:job.id,customer_snapshot:job.customer,site_snapshot:job.site,
   description,net_amount:amount,vat_percent:tax,created_by:session.user.id};
  const r=await db.from("rn_invoice_drafts").insert(data).select("id");
  if(r.error||!r.data?.length)throw r.error||Error("Entwurf nicht gespeichert");
  $("docsInvoiceForm").reset();msg("docsInvoiceMessage","Rechnungsentwurf gespeichert; noch nicht versandt.");await load()
 }catch(e){msg("docsInvoiceMessage","Speichern fehlgeschlagen: "+e.message)}finally{working=false}
}
function weekNow(){
 const d=new Date(),t=new Date(Date.UTC(d.getFullYear(),d.getMonth(),d.getDate()));
 const day=t.getUTCDay()||7;t.setUTCDate(t.getUTCDate()+4-day);
 const start=new Date(Date.UTC(t.getUTCFullYear(),0,1));const n=Math.ceil((((t-start)/86400000)+1)/7);
 return t.getUTCFullYear()+"-W"+String(n).padStart(2,"0");
}
window.RNBuroPilotReloadDocuments=()=>load();
function init(){
 if(!$("opsCustomerForm")||!$("tsPhoto"))return;
 mount();$("tollWeek").value=$("tollWeek").value||weekNow();
 $("docsSiteForm").onsubmit=onSite;
 $("opsQuoteCustomer").onchange=updateQuoteSites;
 $("docsQuoteSite").onchange=()=>{if($("docsQuoteSite").value)$("opsQuoteForm").elements.namedItem("site").value=$("docsQuoteSite").value};
 $("csvFile").addEventListener("change",validateTollFile);$("tollWeek").addEventListener("change",validateTollFile);
 $("docsTollSave").onclick=saveToll;$("docsTsStore").onclick=saveTimesheet;$("docsInvoiceForm").onsubmit=saveInvoice;
 const calc=()=>{const value=Number($("docsInvoiceNet").value),tax=Number($("docsInvoiceVat").value);msg("docsInvoiceGross","Brutto: "+(Number.isFinite(value)&&$("docsInvoiceNet").value!==""?fmtMoney(value*(1+tax/100)):"–"))};
 $("docsInvoiceNet").oninput=calc;$("docsInvoiceVat").onchange=calc;
 for(const v of ["customers","offers","timesheets","toll","invoices"])document.querySelector('[data-view="'+v+'"]')?.addEventListener("click",load);
 window.addEventListener("hashchange",()=>{if(["#customers","#offers","#timesheets","#toll","#invoices"].includes(location.hash))load()});
 load();
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
})();