import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
export const headers = {
  "Access-Control-Allow-Origin": Deno.env.get("RN_APP_ORIGIN") || "https://rn-transporte.de",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Content-Type": "application/json; charset=utf-8",
  "Cache-Control": "no-store"
};
export const preflight = (r: Request) => r.method === "OPTIONS" ? new Response(null,{status:204,headers}) : null;
export function reply(data: unknown,status=200){return new Response(JSON.stringify(data),{status,headers});}
export async function requireStaff(r:Request) {
 const auth=r.headers.get("Authorization")||"";
 if(!/^Bearer [A-Za-z0-9_\-.]+$/.test(auth)) throw Error("Bitte anmelden.");
 const url=Deno.env.get("SUPABASE_URL");
 const key=Deno.env.get("SUPABASE_ANON_KEY");
 if(!url||!key)throw Error("Supabase ist nicht konfiguriert.");
 const token=auth.slice(7);
 const client=createClient(url,key,{global:{headers:{Authorization:auth}},auth:{persistSession:false}});
 const {data:userData,error:userError}=await client.auth.getUser(token);
 if(userError||!userData.user)throw Error("Sitzung ungültig.");
 const {data:staff,error:staffError}=await client.from("rn_staff").select("org_id,role,enabled").eq("user_id",userData.user.id).eq("enabled",true).maybeSingle();
 if(staffError||!staff)throw Error("Kein freigegebener RN-Mitarbeiterzugang.");
 return {client,staff,user:userData.user};
}
export function handledError(e:unknown){return reply({error:e instanceof Error?e.message:"Unbekannter Fehler"},403);}
