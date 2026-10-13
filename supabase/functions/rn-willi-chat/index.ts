import {preflight,reply,requireStaff,handledError} from "../_shared/rn-auth.ts";
Deno.serve(async r=>{
 const p=preflight(r);if(p)return p;
 if(r.method!=="POST")return reply({error:"Nicht erlaubt"},405);
 try{
   await requireStaff(r);
   const req=await r.json();
   const text=typeof req.text==="string"?req.text.trim():"";
   if(!text||text.length>1200)return reply({error:"Eine Nachricht mit 1 bis 1200 Zeichen eingeben."},400);
   const endpoint=Deno.env.get("RN_AI_CHAT_URL")||"",key=Deno.env.get("RN_AI_API_KEY")||"",model=Deno.env.get("RN_AI_MODEL")||"";
   if(!endpoint||!key||!model)return reply({error:"Willi-KI ist noch nicht eingerichtet."},503);
   const url=new URL(endpoint);
   if(url.protocol!=="https:")return reply({error:"KI-Dienst benötigt HTTPS."},503);
   const controller=new AbortController();const timer=setTimeout(()=>controller.abort(),16000);
   let res;
   try{
    res=await fetch(url.toString(),{
     method:"POST",headers:{"Authorization":"Bearer "+key,"Content-Type":"application/json"},
     body:JSON.stringify({
      model,temperature:0.2,max_tokens:500,stream:false,
      messages:[
       {role:"system",content:"Du bist Willi, ein erfahrener, freundlicher und knapper Disponent bei RN Torwesten. Antworte auf Deutsch, gerne bodenständig und mit leichter Baustellen-Umgangssprache. Du hast in dieser Pilotversion keinen Zugriff auf Aufträge, Preise, Kundendaten oder den Kalender und kannst nichts speichern. Behaupte niemals, etwas gebucht oder geändert zu haben. Bei Auftrags- oder Preisfragen erkläre, dass die Funktionen noch nicht freigegeben sind. Bei Missverständnissen frage nach. Keine erfundenen Fakten."},
       {role:"user",content:text}
      ]
     }),signal:controller.signal
    });
   }finally{clearTimeout(timer);}
   if(!res.ok)return reply({error:"KI-Dienst ist nicht erreichbar."},502);
   const body=await res.json();
   const answer=body?.choices?.[0]?.message?.content;
   if(typeof answer!=="string"||!answer.trim())return reply({error:"KI liefert keine gültige Antwort."},502);
   return reply({reply:answer.slice(0,1700),writesEnabled:false});
 }catch(e){return handledError(e);}
});
