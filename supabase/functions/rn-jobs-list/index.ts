import {preflight,reply,requireStaff,handledError} from "../_shared/rn-auth.ts";
Deno.serve(async r=>{
 const p=preflight(r);if(p)return p;
 if(r.method!=="POST")return reply({error:"Nicht erlaubt"},405);
 try{
  const {client,staff}=await requireStaff(r);
  const {data,error}=await client.from("rn_jobs").select("id,customer,site,date,start_time,pump,status,volume_m3")
   .eq("org_id",staff.org_id).order("date",{ascending:true}).order("start_time",{ascending:true}).limit(100);
  if(error)throw error;
  return reply({jobs:data||[]});
 }catch(e){return handledError(e);}
});
