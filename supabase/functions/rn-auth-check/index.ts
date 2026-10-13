import {headers, preflight, reply, requireStaff, handledError} from "../_shared/rn-auth.ts";
Deno.serve(async r=>{
 const p=preflight(r);if(p)return p;
 if(r.method!=="POST")return reply({error:"Nicht erlaubt"},405);
 try{
  const {staff}=await requireStaff(r);
  return reply({allowed:true,role:staff.role});
 }catch(e){return handledError(e);}
});
