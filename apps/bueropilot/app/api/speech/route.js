import { requireStaff, jsonError, ApiError } from "../../../lib/auth";
export const runtime = "nodejs";
export async function POST(request) {
 try {
   await requireStaff(request);
   if (process.env.RN_VOICE_ENABLED !== "true") throw new ApiError(503, "Sprachausgabe ist noch deaktiviert.");
   const key = process.env.ELEVENLABS_API_KEY, voice = process.env.ELEVENLABS_VOICE_ID;
   if (!key || !voice || !/^[A-Za-z0-9_-]{12,64}$/.test(voice)) throw new ApiError(503, "ElevenLabs ist noch nicht eingerichtet.");
   const { text } = await request.json();
   if (typeof text !== "string" || !text.trim() || text.length > 500) throw new ApiError(400, "Text muss zwischen 1 und 500 Zeichen lang sein.");
   const response = await fetch("https://api.elevenlabs.io/v1/text-to-speech/" + encodeURIComponent(voice), {
     method: "POST",
     headers: { "xi-api-key": key, "Content-Type": "application/json", Accept: "audio/mpeg" },
     body: JSON.stringify({ text, model_id: process.env.ELEVENLABS_TTS_MODEL || "eleven_multilingual_v2" }),
     signal: AbortSignal.timeout(15000),
     cache: "no-store"
   });
   if (!response.ok) throw new ApiError(502, "ElevenLabs ist momentan nicht erreichbar oder dein Kontingent ist aufgebraucht.");
   const data = await response.arrayBuffer();
   if (data.byteLength > 4_000_000) throw new ApiError(502, "Audiodatei ist zu groß.");
   return new Response(data, { status: 200, headers: { "Content-Type": "audio/mpeg", "Cache-Control": "no-store" } });
 } catch (error) { return jsonError(error); }
}
