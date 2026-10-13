import {preflight,reply,requireStaff,handledError,headers} from "../_shared/rn-auth.ts";
Deno.serve(async r=>{
 const p=preflight(r);if(p)return p;
 if(r.method!=="POST")return reply({error:"Nicht erlaubt"},405);
 try{
   await requireStaff(r);
   if(Deno.env.get("RN_VOICE_ENABLED")!=="true")return reply({error:"Willis Stimme ist noch nicht eingeschaltet."},503);
   const key=Deno.env.get("ELEVENLABS_API_KEY")||"",voice=Deno.env.get("ELEVENLABS_VOICE_ID")||"";
   if(!key||!/^[A-Za-z0-9_-]{12,64}$/.test(voice))return reply({error:"ElevenLabs ist nicht vollständig eingerichtet."},503);
   const payload=await r.json();
   const text=typeof payload.text==="string"?payload.text.trim():"";
   if(!text||text.length>500)return reply({error:"Sprachtext muss 1 bis 500 Zeichen enthalten."},400);
   const controller=new AbortController();const timer=setTimeout(()=>controller.abort(),16000);
   let audioResponse;
   try{
    audioResponse=await fetch("https://api.elevenlabs.io/v1/text-to-speech/"+encodeURIComponent(voice),{
      method:"POST",headers:{"xi-api-key":key,"Content-Type":"application/json","Accept":"audio/mpeg"},
      body:JSON.stringify({text,model_id:Deno.env.get("ELEVENLABS_TTS_MODEL")||"eleven_multilingual_v2"}),signal:controller.signal
    });
   }finally{clearTimeout(timer);}
   if(!audioResponse.ok)return reply({error:"ElevenLabs antwortet nicht oder Kontingent reicht nicht."},502);
   const bytes=new Uint8Array(await audioResponse.arrayBuffer());
   if(bytes.byteLength>3_000_000)return reply({error:"Audio ist zu groß."},502);
   // Chunked base64 conversion avoids argument list limit.
   const chunks=[];
   for(let i=0;i<bytes.length;i+=8192)chunks.push(String.fromCharCode(...bytes.subarray(i,i+8192)));
   return reply({audioBase64:btoa(chunks.join(""))});
 }catch(e){return handledError(e);}
});
