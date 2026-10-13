// RN BüroPilot · Cloudflare Workers AI · Free plan
// Only PUBLIC Supabase credentials are included. Never add service_role or private keys.
// Add an AI binding named AI in Cloudflare Worker Settings > Bindings.
const SUPABASE_URL = "https://lsdjscvpbahvllwfzjhs.supabase.co";
const SUPABASE_KEY = "sb_publishable_roOWR9KPI_1ckEkdPPfixA_wew89Trk";
const MODEL = "@cf/zai-org/glm-4.7-flash";
const ALLOWED_ORIGINS = new Set(["https://rn-transporte.de", "https://www.rn-transporte.de"]);
const SYSTEM = [
  "Du bist Willi, der freundliche, bodenständige, erfahrene digitale Disponent von RN Torwesten Transporte.",
  "Sprich Hochdeutsch mit einer kleinen Prise westfälischer Umgangssprache, z.B. Moin, wat, jo.",
  "Du bist hilfreich, klar, sachlich, humorvoll, aber erfindest niemals Fakten, Aufträge, Preise oder Zusagen.",
  "WICHTIG: Der Chat kann in dieser Stufe ausschließlich beraten und antworten.",
  "Du kannst NICHT auf bestehende Aufträge, Kundendaten, Rechnungen oder Preise zugreifen und NICHTS speichern, buchen, ändern, versenden oder stornieren.",
  "Wenn der Nutzer eine Änderung oder Buchung verlangt: Erkläre, dass die Funktion erst sicher freigeschaltet werden muss; frage bei Bedarf nach den Angaben, bestätige aber niemals eine ausgeführte Aktion.",
  "Für sicherheitsrelevante Entscheidungen nenne Unsicherheiten und frage nach. Halte die Antworten meistens auf 1 bis 5 Sätze.",
  "Beantworte auch normale Wissensfragen so gut du kannst, aber behaupte keinen Internetzugriff.",
].join(" ");
function cors(origin) {
  return {
    "Access-Control-Allow-Origin": ALLOWED_ORIGINS.has(origin) ? origin : "https://rn-transporte.de",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "content-type, authorization",
    "Vary": "Origin",
    "Cache-Control": "no-store",
    "Content-Type": "application/json; charset=utf-8"
  };
}
function result(data, code, origin) {
  return new Response(JSON.stringify(data), { status: code, headers: cors(origin) });
}
function validId(s) { return /^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(s || ""); }
async function checkStaff(jwt) {
  if(!jwt || jwt.length < 60 || jwt.length > 5500 || !/^[A-Za-z0-9._-]+$/.test(jwt)) return false;
  const headers = { "apikey": SUPABASE_KEY, "Authorization": "Bearer " + jwt, "Accept": "application/json" };
  const userResponse = await fetch(SUPABASE_URL + "/auth/v1/user", { headers });
  if(!userResponse.ok) return false;
  const user = await userResponse.json();
  if(!validId(user?.id)) return false;
  // Query goes through the visitor's JWT and Supabase RLS. The Worker is not privileged.
  const endpoint = SUPABASE_URL + "/rest/v1/rn_staff?select=enabled&user_id=eq." + encodeURIComponent(user.id) + "&enabled=eq.true&limit=1";
  const staffResponse = await fetch(endpoint, {headers});
  if(!staffResponse.ok) return false;
  const staff = await staffResponse.json();
  return Array.isArray(staff) && staff.length === 1 && staff[0]?.enabled === true;
}
export default {
 async fetch(request, env) {
  const origin = request.headers.get("Origin") || "";
  const path = new URL(request.url).pathname;
  if (request.method === "OPTIONS") {
    return ALLOWED_ORIGINS.has(origin)
      ? new Response(null, {status:204,headers:cors(origin)})
      : result({error:"Origin nicht freigegeben."},403,origin);
  }
  if (request.method === "GET" && path === "/health") return result({status:"ok", ai:!!env.AI, model:MODEL},200,origin);
  if (request.method !== "POST" || path !== "/chat") return result({error:"Nicht verfügbar."},404,origin);
  if (!ALLOWED_ORIGINS.has(origin)) return result({error:"Origin nicht freigegeben."},403,origin);
  const len = Number(request.headers.get("content-length") || 0);
  if (len > 12000) return result({error:"Anfrage zu lang."},413,origin);
  const jwt = (request.headers.get("Authorization") || "").replace(/^Bearer\s+/i, "").trim();
  try {
    if(!(await checkStaff(jwt))) return result({error:"Keine gültige RN-Mitarbeiteranmeldung."},403,origin);
  } catch (_) {
    return result({error:"Mitarbeiteranmeldung konnte nicht geprüft werden."},503,origin);
  }
  if(!env.AI || typeof env.AI.run !== "function") return result({error:"Workers AI Binding namens AI fehlt."},503,origin);
  let data;
  try {
    data = await request.text();
    if (data.length > 11000) return result({error:"Anfrage zu lang."},413,origin);
    data = JSON.parse(data);
  } catch (_) { return result({error:"Ungültige Nachricht."},400,origin); }
  const text = typeof data?.text === "string" ? data.text.trim() : "";
  if(!text || text.length > 1200) return result({error:"Bitte eine Nachricht mit höchstens 1200 Zeichen senden."},400,origin);
  const history = Array.isArray(data.history) ? data.history.slice(-8)
    .filter(m => m && (m.role === "user" || m.role === "assistant") && typeof m.content === "string" && m.content.length <= 1200)
    .map(m=>({role:m.role,content:m.content})) : [];
  const messages = [{role:"system",content:SYSTEM},...history,{role:"user",content:text}];
  try {
    const ai = await env.AI.run(MODEL,{messages,max_tokens:450,temperature:0.4,stream:false});
    const answer = ai?.choices?.[0]?.message?.content || ai?.response;
    if (typeof answer !== "string" || !answer.trim())
      return result({error:"Willi hat noch keine brauchbare Antwort."},502,origin);
    return result({reply:answer.slice(0,2500),source:"cloudflare-workers-ai",writesEnabled:false},200,origin);
  } catch (e) {
    // No automatic billing, upgrades or third-party fallback.
    const s = String(e?.message || "");
    if(/limit|quota|neurons|3036|429/i.test(s)) return result({error:"Kostenloses KI-Kontingent erschöpft. Morgen geht es weiter."},429,origin);
    return result({error:"Die kostenlose KI ist gerade nicht erreichbar."},503,origin);
  }
 }
};
