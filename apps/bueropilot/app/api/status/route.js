export const runtime = "nodejs";
export async function GET() {
  return Response.json({
    app: "RN BüroPilot",
    mode: "pilot",
    authenticationConfigured: Boolean(process.env.NEXT_PUBLIC_SUPABASE_URL && process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY),
    aiConfigured: Boolean(process.env.RN_AI_CHAT_URL && process.env.RN_AI_API_KEY && process.env.RN_AI_MODEL),
    speechConfigured: Boolean(process.env.RN_VOICE_ENABLED === "true" && process.env.ELEVENLABS_API_KEY && process.env.ELEVENLABS_VOICE_ID)
  }, { headers: { "Cache-Control": "no-store" } });
}
