import { requireStaff, jsonError, ApiError } from "../../../lib/auth";
export const runtime = "nodejs";
export async function POST(request) {
 try {
   const { staff } = await requireStaff(request);
   const { text } = await request.json();
   if (typeof text !== "string" || text.trim().length < 1 || text.length > 1200) throw new ApiError(400, "Bitte eine Nachricht mit maximal 1200 Zeichen senden.");
   const endpoint = process.env.RN_AI_CHAT_URL;
   const key = process.env.RN_AI_API_KEY;
   const model = process.env.RN_AI_MODEL;
   if (!endpoint || !key || !model) throw new ApiError(503, "Die KI ist noch nicht eingerichtet.");
   const url = new URL(endpoint);
   if (url.protocol !== "https:") throw new ApiError(503, "Die KI-Verbindung muss HTTPS verwenden.");
   const controller = new AbortController();
   const timeout = setTimeout(() => controller.abort(), 15000);
   let result;
   try {
     result = await fetch(url, {
       method: "POST",
       headers: { Authorization: "Bearer " + key, "Content-Type": "application/json" },
       body: JSON.stringify({
         model, stream: false, temperature: 0.2, max_tokens: 500,
         messages: [
           { role: "system", content: "Du bist Willi, der ruhige, erfahrene Disponent von RN Torwesten. Antworte auf Deutsch kurz, freundlich, auch auf Umgangssprache. Du hast in dieser Testversion KEINEN Zugriff auf Kunden, Aufträge oder Kalender und darfst NIE behaupten, eine Buchung/Änderung ausgeführt zu haben. Frage bei zweideutigen Angaben nach. Preise und Termine niemals erfinden. Keine Speicherung anbieten. Erwähne bei Auftragswünschen, dass die Funktion derzeit nur in Vorbereitung ist." },
           { role: "user", content: text }
         ]
       }),
       cache: "no-store", signal: controller.signal
     });
   } finally { clearTimeout(timeout); }
   if (!result.ok) throw new ApiError(502, "KI-Dienst ist momentan nicht erreichbar.");
   const reply = (await result.json())?.choices?.[0]?.message?.content;
   if (typeof reply !== "string" || !reply.trim()) throw new ApiError(502, "Keine gültige KI-Antwort erhalten.");
   return Response.json({ reply: reply.slice(0, 1800), writesEnabled: false, mode: "pilot" }, { headers: { "Cache-Control": "no-store" } });
 } catch (error) { return jsonError(error); }
}
