/* RN BüroPilot · Piper/Thorsten TTS, vollständig im Browser.
   Piper-Webbibliothek MIT; Stimme de_DE-thorsten-medium. Kein kostenpflichtiger TTS-Dienst.
   Modell (~63 MB) und WASM-Laufzeit werden beim ersten Gebrauch extern geladen. */
(function(root){
"use strict";
const MODEL="de_DE-thorsten-medium";
const MODULE_URL="https://esm.sh/@mintplex-labs/piper-tts-web@1.0.5?bundle";
let modulePromise=null,player=null,wavUrl=null,finishCurrent=null,sequence=0;

function notify(handler,text){if(typeof handler==="function")handler(text);}
function loadModule(){
  if(!modulePromise){
    modulePromise=import(MODULE_URL).catch(err=>{modulePromise=null;throw err;});
  }
  return modulePromise;
}
function cleanupPlayer(){
  if(player){try{player.pause();player.removeAttribute("src");player.load();}catch(_){}player=null;}
  if(wavUrl){URL.revokeObjectURL(wavUrl);wavUrl=null;}
}
function stop(){
  sequence++;
  if(finishCurrent){const cb=finishCurrent;finishCurrent=null;cb({status:"stopped"});}
  cleanupPlayer();
}
async function speak(value,options={}){
  const text=String(value||"").trim().slice(0,900);
  if(!text)return {status:"empty"};
  if(!root.isSecureContext||!root.WebAssembly)return {status:"unsupported",message:"Piper braucht einen aktuellen Browser mit HTTPS und WebAssembly."};
  stop();
  const id=sequence;
  const inform=msg=>{if(id===sequence)notify(options.onStatus,msg);};
  try{
    inform("Thorsten wird vorbereitet – beim ersten Mal wird die kostenlose Piper-Stimme geladen (rund 63 MB) …");
    const tts=await loadModule();
    if(id!==sequence)return {status:"stopped"};
    if(typeof tts.TtsSession!=="function")throw Error("Piper-Modul konnte nicht geladen werden.");
    const session=new tts.TtsSession({
      voiceId:MODEL,
      wasmPaths:{
        onnxWasm:"https://cdn.jsdelivr.net/npm/onnxruntime-web@1.18.0/dist/",
        piperData:"https://cdn.jsdelivr.net/npm/@diffusionstudio/piper-wasm@1.0.0/build/piper_phonemize.data",
        piperWasm:"https://cdn.jsdelivr.net/npm/@diffusionstudio/piper-wasm@1.0.0/build/piper_phonemize.wasm"
      },
      progress:progress=>{
        if(id!==sequence||!progress||!Number.isFinite(progress.total)||progress.total<=0)return;
        inform("Piper-Stimme wird geladen: "+Math.min(100,Math.round(100*progress.loaded/progress.total))+" % …");
      }
    });
    const wav=await session.predict(text);
    if(id!==sequence)return {status:"stopped"};
    if(!(wav instanceof Blob))throw Error("Piper hat keine Audiodatei erzeugt.");
    wavUrl=URL.createObjectURL(wav);
    const audio=new Audio(wavUrl);
    player=audio;
    audio.preload="auto";
    audio.playbackRate=Math.max(0.75,Math.min(1.25,Number(options.rate)||1));
    inform("Willi spricht mit Piper / Thorsten …");
    return await new Promise(resolve=>{
      let ended=false;
      function finish(result){
        if(ended)return;
        ended=true;
        if(finishCurrent===finish)finishCurrent=null;
        resolve(result);
      }
      finishCurrent=finish;
      audio.onended=()=>finish({status:"spoken",url:wavUrl});
      audio.onerror=()=>finish({status:"error",message:"Audio konnte nicht abgespielt werden.",url:wavUrl});
      audio.play().catch(e=>{
        if(id!==sequence){finish({status:"stopped"});return;}
        if(e.name==="NotAllowedError"){
          inform("Piper ist fertig. Tippe unten im Audioplayer auf Play.");
          finish({status:"ready",message:"Bitte Audio manuell abspielen.",url:wavUrl});
        }else finish({status:"error",message:e.message||"Wiedergabe nicht möglich.",url:wavUrl});
      });
    });
  }catch(e){
    if(id!==sequence)return {status:"stopped"};
    const message=String(e&&e.message||e);
    inform("Piper konnte nicht gestartet werden: "+message);
    return {status:"error",message};
  }
}
root.RNPiperVoice={speak,stop,getAudioUrl:()=>wavUrl,model:MODEL};
})(window);
