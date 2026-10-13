/* RN BüroPilot: progressive enhancements - no changes to protected server data. */
(()=>{"use strict";
const $=id=>document.getElementById(id);const escape=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
function init(){
const week=$("weekGrid"),calendar=$("calendarView"),ts=$("timesheetsView");
if(week&&calendar){
  const switcher=document.createElement("div");switcher.className="calendar-extra";
  switcher.innerHTML='<div class="extra-top"><strong>Disposition nach Maschine</strong><div class="extra-modes"><button type="button" id="extraWeek" class="selected">Wochenplan</button><button type="button" id="extraDay">Tagesplan</button><input type="date" id="extraDate" aria-label="Kalendertag"></div></div><p class="extra-caption">Maschinen untereinander, Tage nebeneinander. Aufträge erscheinen nach Mitarbeiteranmeldung; bis dahin bleibt die Übersicht leer.</p><div class="resource-wrapper"><div id="resourceCalendar" class="resource-calendar"></div></div>';
  week.parentElement.insertBefore(switcher,week);week.classList.add("calendar-source");week.setAttribute("aria-hidden","true");
  let mode="week";const now=new Date();$("extraDate").value=[now.getFullYear(),String(now.getMonth()+1).padStart(2,"0"),String(now.getDate()).padStart(2,"0")].join("-");
  const pumps=["24er Pumpe","36er Pumpe","42er Pumpe","Weitere"];
  function render(){
    const cols=[...week.querySelectorAll(".week-day")].map(day=>({label:day.querySelector("strong")?.textContent||"",date:day.dataset.date,items:[...day.querySelectorAll(".week-item")].map(item=>item.textContent.trim())}));
    let selected=cols.map((x,i)=>({...x,i}));if(mode==="day"){const date=$("extraDate").value;selected=selected.filter(x=>x.date===date);}
    const h='<div class="resource-label resource-head">Maschine</div>'+selected.map(x=>'<div class="resource-head">'+escape(x.label)+'</div>').join("");
    const rows=pumps.map(p=>'<div class="resource-label"><span class="resource-dot"></span><strong>'+escape(p)+'</strong></div>'+selected.map(x=>{const matches=x.items.filter(y=>p==="Weitere"?!/(24er|36er|42er)/i.test(y):y.toLowerCase().includes(p.slice(0,2)));return '<div class="resource-cell">'+(matches.length?matches.map(y=>'<div class="resource-job">'+escape(y)+'</div>').join(""):'<span class="resource-empty">—</span>')+'</div>'}).join("")).join("");
    $("resourceCalendar").style.gridTemplateColumns="minmax(118px,165px) repeat("+selected.length+",minmax("+(mode==="day"?"240":"110")+"px,1fr))";
    $("resourceCalendar").innerHTML=h+rows;
  }
  new MutationObserver(()=>render()).observe(week,{childList:true});$("extraWeek").onclick=()=>{mode="week";$("extraWeek").classList.add("selected");$("extraDay").classList.remove("selected");render()};$("extraDay").onclick=()=>{mode="day";$("extraDay").classList.add("selected");$("extraWeek").classList.remove("selected");render()};$("extraDate").onchange=()=>{window.RNBuroPilotGoToCalendarDate?.($("extraDate").value);$("extraDay").click()};render();
}
if(ts){
 const original=ts.querySelector(".surface");if(original)original.hidden=true;
 const panel=document.createElement("div");panel.className="timesheet-workflow surface";
 panel.innerHTML='<div class="section-head"><div><h2>Stundenzettel fotografieren & prüfen</h2><p>Kostenlose Texterkennung auf dem Gerät · kein Upload an RN-Server</p></div><span class="tag tag-neutral">NEU · OCR</span></div><div class="ts-columns"><section><label class="scan-select" for="tsPhoto"><span style="font-size:28px">▧</span><strong>Foto aufnehmen oder auswählen</strong><small>JPG, PNG, WEBP · bis 10 MB</small><input type="file" id="tsPhoto" accept="image/png,image/jpeg,image/webp" capture="environment"></label><img id="tsImage" alt="Stundenzettelvorschau" hidden><button type="button" id="tsRead" class="button button-primary full" disabled>⌕ Text erkennen</button><div id="tsMessage" class="inline-feedback" role="status">Bitte ein gut lesbares Foto auswählen.</div><details><summary>Erkannter Text</summary><textarea id="tsRaw" rows="9" readonly placeholder="Hier erscheint der Text nach der Erkennung."></textarea></details></section><section><h3>Daten kontrollieren</h3><p class="extra-caption">Alle Angaben können korrigiert werden. OCR ist nicht fehlerfrei.</p><div class="ts-fields"><label>Fahrer<input id="tsDriver" placeholder="Name"></label><label>Datum<input id="tsDate" type="date"></label><label>Von<input id="tsFrom" type="time"></label><label>Bis<input id="tsTo" type="time"></label><label>Pause (Min.)<input id="tsBreak" type="number" min="0" max="900" placeholder="30"></label><label>Stunden<input id="tsHours" type="number" min="0" max="24" step=".01" placeholder="8"></label><label>Fahrzeug / Pumpe<input id="tsVehicle" placeholder="Kennzeichen"></label><label>Baustelle<input id="tsSite" placeholder="Baustelle / Kunde"></label></div><label class="ts-confirm"><input type="checkbox" id="tsConfirmed"> Angaben anhand des Fotos überprüft</label><button type="button" class="button button-primary full" id="tsDownload" disabled>Geprüften Stundenzettel als CSV speichern ↓</button><p class="extra-caption">Noch keine Speicherung in Supabase. Den Originalbeleg bitte aufbewahren.</p></section></div>';
 ts.append(panel);
 const photo=$("tsPhoto"),image=$("tsImage"),scan=$("tsRead"),message=$("tsMessage"),save=$("tsDownload"),confirm=$("tsConfirmed");let blobUrl=null;
 photo.onchange=()=>{const file=photo.files?.[0];scan.disabled=true;confirm.checked=false;save.disabled=true;image.hidden=true;$("tsRaw").value="";for(const id of ["tsDriver","tsDate","tsFrom","tsTo","tsBreak","tsHours","tsVehicle","tsSite"])$(id).value="";if(blobUrl){URL.revokeObjectURL(blobUrl);blobUrl=null}if(!file)return;if(file.size>10*1024*1024||!/^image\/(jpeg|png|webp)$/.test(file.type)){message.textContent="Nur JPG, PNG oder WEBP bis 10 MB erlaubt.";return}blobUrl=URL.createObjectURL(file);image.src=blobUrl;image.hidden=false;scan.disabled=false;message.textContent="Foto bereit. Auf „Text erkennen“ klicken."};
 function calculateHours(){
 const a=$("tsFrom").value,b=$("tsTo").value;
 if(!a||!b)return;
 const mins=t=>{const [h,m]=t.split(":").map(Number);return h*60+m};
 let length=mins(b)-mins(a);if(length<0)length+=1440;
 const breakMinutes=Math.max(0,Number($("tsBreak").value)||0);
 const worked=(length-breakMinutes)/60;
 if(worked>=0&&worked<=24)$("tsHours").value=worked.toFixed(2);
}
for(const id of ["tsFrom","tsTo","tsBreak"])$(id).addEventListener("change",calculateHours);
confirm.onchange=()=>{save.disabled=!confirm.checked};

 const loadOCR=()=>new Promise((resolve,reject)=>{if(window.Tesseract)return resolve(window.Tesseract);const s=document.createElement("script");s.src="https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js";s.onload=()=>window.Tesseract?resolve(window.Tesseract):reject(Error("Texterkennung fehlt"));s.onerror=()=>reject(Error("Texterkennungs-Bibliothek konnte nicht geladen werden"));document.head.append(s)});
 scan.onclick=async()=>{if(!photo.files?.[0])return;scan.disabled=true;message.textContent="Texterkennung wird geladen …";let worker;try{const api=await loadOCR();worker=await api.createWorker("deu",1,{logger:m=>{if(m.status){message.textContent=m.status+(Number.isFinite(m.progress)?" · "+Math.round(m.progress*100)+" %":"")}}});const result=await worker.recognize(photo.files[0]);const text=result.data?.text||"";$("tsRaw").value=text;message.textContent=text.trim()?"Text erkannt. Bitte alle Angaben prüfen und gegebenenfalls korrigieren.":"Kein Text erkannt. Bitte schärferes Foto verwenden.";const date=text.match(/\b(\d{1,2})[.\/-](\d{1,2})[.\/-](20\d{2})\b/);if(date)$("tsDate").value=date[3]+"-"+date[2].padStart(2,"0")+"-"+date[1].padStart(2,"0");const times=[...text.matchAll(/\b([01]?\d|2[0-3])[:.]([0-5]\d)\b/g)].map(m=>m[1].padStart(2,"0")+":"+m[2]);if(times.length>=2){$("tsFrom").value=times[0];$("tsTo").value=times[1];calculateHours()}}catch(e){message.textContent="Erkennung nicht möglich: "+(e.message||e)+". Du kannst die Felder trotzdem von Hand ausfüllen."}finally{try{await worker?.terminate()}catch(_){}scan.disabled=false}};
 const q=v=>'"'+String(v??"").replace(/"/g,'""')+'"';save.onclick=()=>{
 if(!confirm.checked||!photo.files?.[0]){message.textContent="Bitte zuerst einen Stundenzettel fotografieren und die Angaben prüfen.";return}
 const driver=$("tsDriver").value.trim(),date=$("tsDate").value,hours=Number($("tsHours").value);
 if(!driver||!date||!Number.isFinite(hours)||hours<=0||hours>24){
  message.textContent="Vor dem Export bitte mindestens Mitarbeiter, Datum und gültige Arbeitsstunden eintragen.";
  return;
 }
 const fields=["tsDriver","tsDate","tsFrom","tsTo","tsBreak","tsHours","tsVehicle","tsSite"];const hdr=["Fahrer","Datum","Von","Bis","Pause_Min","Stunden","Fahrzeug","Baustelle"];const csv="\ufeff"+hdr.map(q).join(";")+"\r\n"+fields.map(id=>q($(id).value)).join(";")+"\r\n";const url=URL.createObjectURL(new Blob([csv],{type:"text/csv;charset=utf-8"}));const link=document.createElement("a");link.href=url;link.download="RN-Stundenzettel-"+($("tsDate").value||"Entwurf")+".csv";link.click();setTimeout(()=>URL.revokeObjectURL(url),2000);message.textContent="Geprüfter CSV-Entwurf heruntergeladen. Nicht in Supabase gespeichert."};
}
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
})();